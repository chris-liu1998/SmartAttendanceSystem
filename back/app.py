from flask import Flask, request, Response, session, jsonify
from flask_cors import CORS
import json, base64
import os
import datetime
import time
import numpy as np
from face_recognize import face_rec

from service.department_service import DepartmentService
from service.account_service import AccountService
from service.employee_service import EmployeeService
from service.leave_service import LeaveService
from service.att_record_service import AttendanceRecordService
from service.checkinfo_service import CheckInfoService
from service.att_setting_service import AttendanceSettingService
from service.ind_record_service import IndividualRecordService
from service.todo_service import TodoService

import configs

from utils.exts import db
from utils.class2data import Class2Data
from utils.class2data import Class2Data_dealDatetime
from utils.captcha import Captcha

app = Flask(__name__)
# 加载配置文件
app.config.from_object(configs)
# db绑定app
db.init_app(app)
# 解决跨域问题
CORS(app, supports_credentials=True)
# 配置session
# 设置24位随机变量
# os.urandom(24) 会从 0-9，a-z A-Z中随机选中24个字符串用做加密session的秘钥
app.config['SECRET_KEY'] = os.urandom(24)

# Service
account = AccountService()
department = DepartmentService()
employee = EmployeeService()
leaveService = LeaveService()
att_record = AttendanceRecordService()
checkinfo = CheckInfoService()
att_setting = AttendanceSettingService()
ind_record = IndividualRecordService()
todo = TodoService()
np.set_printoptions(suppress=True)
face = face_rec()


@app.route('/')
def test():
    now_time = datetime.datetime.now().strftime('%H:%M:%S')
    now_time = now_time.split(":")
    now_time = [int(time) for time in now_time]
    print(int("09"))
    print(type(now_time[0]))
    return "ok"


# 上传头像
@app.route('/api/account/avatar', methods=['POST'])
def classfy():
    avatar = request.files.get('avatar')
    avataraccount = request.form.get('account')
    name, ext = os.path.splitext(avatar.filename)
    newfilename = avataraccount + ext
    avatar.save('./avatar/' + newfilename)
    return '头像更换成功'


# 验证码图片
@app.route('/api/captchaimg', methods=['GET'])
def captchaImg():
    img, session["captchacode"] = Captcha().getCaptcha()
    print("生成验证码 " + session.get("captchacode"))
    return img


"""
部门相关
"""


# 获取部门信息
@app.route('/api/department/all', methods=['GET'])
def departmentall():
    data = department.find_all()
    # 处理 data
    result = Class2Data(data, department.__fields__, 0)
    return Response(json.dumps({'code': 200, 'data': result}))


# 新增部门
@app.route('/api/department/addone', methods=['GET'])
def departmentaddone():
    data = department.add_one_department('技术部')
    return Response(json.dumps(data))


@app.route('/api/department/attendsetting', methods=['POST'])
def set_att_setting():
    setting_id = request.values.get('setting_id')
    # print(setting_id)
    # return setting_id
    data = department.update_setting(setting_id)
    if data:
        response = jsonify({"code": 0, "message": "激活考勤设置成功！"})
    else:
        response = jsonify({"code": 1, "message": "激活考勤设置失败！"})
    return response


# 账户相关
# 获取账户信息
@app.route('/api/account/all', methods=['GET'])
def accountall():
    data = account.find_all()
    # 处理 data
    result = Class2Data(data, account.__fields__, 0)
    return Response(json.dumps({'code': 200, 'data': result}))


@app.route('/api/account/one', methods=['POST'])
def accountone():
    oneaccount = request.form.get('account')
    data = account.find_by_account(oneaccount)
    # 处理 data
    result = Class2Data(data, account.__fields__, 1)
    return Response(json.dumps({'code': 200, 'data': result}))


# 新建账号
@app.route('/api/account/addone', methods=['POST'])
def accountaddone():
    addaccount = request.form.get('account')
    pwd = request.form.get('password')
    flag = request.form.get('flag')
    data = account.add_one_account(addaccount, pwd, flag)

    return Response(json.dumps(data))


# 删除账号
@app.route('/api/account/delete/<delaccout>', methods=['POST'])
def accountdelete(delaccout):
    data = account.delete_account(delaccout)
    return Response(json.dumps(data))


# 重置密码
@app.route('/api/account/updatepwd', methods=['POST'])
def accountupdatepwd():
    updateaccount = request.form.get('account')
    password = request.form.get('password')
    data = account.update_pwd(updateaccount, password)
    return Response(json.dumps(data))


# 用户登录
# 200 登陆成功 返回该用户基本信息
# 201 验证码错误
# 202 密码错误
# 203 账户不存在
@app.route('/api/login', methods=['POST'])
def login():
    loginaccount = request.values.get('account')
    pwd = request.values.get('password')
    captchacode = request.values.get('captcha')
    if captchacode.lower() == session.get('captchacode').lower():
        data = employee.user_login(loginaccount, pwd)
        return Response(json.dumps(data))
    else:
        return Response(json.dumps({'code': 201, 'data': '验证码错误'}))


"""
员工相关
"""


# 获取员工信息
@app.route('/api/employee/all', methods=['GET'])
def employeeall():
    data = employee.find_all()
    # 处理 data
    result = Class2Data(data, employee.__fields__, 0)
    return Response(json.dumps({'code': 200, 'data': result}))


@app.route('/api/employee/one', methods=['POST'])
def employeeone():
    employee_id = request.form.get('employee_id')
    data = employee.find_by_e_id(employee_id)
    # 处理 data
    result = Class2Data(data, employee.__fields__, 1)
    return Response(json.dumps({'code': 200, 'data': result}))


# 新增员工(单个)
@app.route('/api/employee/addone', methods=['POST'])
def employeeaddone():
    employee_id = request.form.get('employee_id')
    employee_name = request.form.get('employee_name')
    employee_title = request.form.get('employee_title')
    department_name = request.form.get('department_name')
    leader_id = request.form.get('leader_id')
    phone = request.form.get('phone')
    qq = request.form.get('qq')
    wechat = request.form.get('wechat')
    data = employee.add_one_employee(employee_id, employee_name,
                                     employee_title, department_name,
                                     leader_id, phone, qq, wechat)
    return Response(json.dumps(data))


# 一键导入员工EXCEL
@app.route('/api/employee/add', methods=['POST'])
def employeeadd():
    employeeInfo = json.loads(request.get_data(as_text=True))
    # 添加部门
    for d_name in employeeInfo['department_names']:
        department.add_one_department(d_name)
    # 添加员工
    for e in employeeInfo['employees']:
        employee.add_one_employee(e['employee_id'], e['employee_name'],
                                  e['employee_title'], e['department_name'],
                                  e['leader_id'], e['phone'], e['qq'],
                                  e['wechat'])
    return Response(json.dumps({'code': 200, 'data': '一键导入员工基本信息成功'}))


# 删除员工
@app.route('/api/employee/delete', methods=['POST'])
def employeedelete():
    employee_id = request.form.get('employee_id')
    data = employee.delete_employee(employee_id)
    return Response(json.dumps(data))


# 更新员工基本信息
@app.route('/api/employee/update', methods=['POST'])
def employeeupdate():
    employee_id = request.form.get('employee_id')
    employee_name = request.form.get('employee_name')
    employee_title = request.form.get('employee_title')
    department_name = request.form.get('department_name')
    leader_id = request.form.get('leader_id')
    phone = request.form.get('phone')
    qq = request.form.get('qq')
    wechat = request.form.get('wechat')
    data = employee.update_employee(employee_id, employee_name, employee_title,
                                    department_name, leader_id, phone, qq,
                                    wechat)
    return Response(json.dumps(data))


# 各部门员工个数
@app.route('/api/employee/d_nums', methods=['GET'])
def employeenumsindepartment():
    data = employee.find_counts_in_department()
    return Response(json.dumps(data))


"""
请假相关
"""


#员工请假列表界面
@app.route('/api/leave/eLeaveList/initialize', methods=['POST'])
def findByEid():
    employee_id = request.values.get('userid')
    result = leaveService.findLeaveByeid(employee_id)

    data = {'code': 200, 'data': result}
    return Response(json.dumps(data))
    '''
    except:
        data = {
            'code': 203,
            'data': '查找失败'
        }
        return Response(json.dumps(data))
    '''


@app.route('/api/leave/eLeaveList/search', methods=['POST'])
def findByEidAndDate():
    employee_id = request.values.get('userid')
    date = request.values.get('date')
    result = leaveService.findLeaveByeid_date(employee_id, date)

    data = {'code': 200, 'data': result}
    return Response(json.dumps(data))
    '''
        except:
            data = {
                'code': 203,
                'data': '查找失败'
            }
            return Response(json.dumps(data))
    '''


@app.route('/api/leave/eLeaveList/delete', methods=['POST'])
def deleteByLid():
    leave_id = request.values.get('leave_id')
    print("前端传来的" + leave_id)

    data = leaveService.deleteByLid(leave_id)

    return Response(json.dumps(data))
    '''
        except:
            data = {
                'code': 203,
                'data': '查找失败'
            }
            return Response(json.dumps(data))
    '''


#新增请假单界面
#初始化
@app.route('/api/leave/newLeave/find', methods=['POST'])
def findByLid():
    leave_id = request.values.get('leave_id')
    if leave_id is None:
        return {"error": "无对应请假单"}
    findresult = leaveService.findByLid(leave_id)
    result = Class2Data_dealDatetime(findresult, leaveService.__fields__)
    print(result)
    data = {'code': 200, 'data': result}
    return Response(json.dumps(data))


#提交请假单
@app.route('/api/leave/new', methods=['POST'])
def newList():
    employee_id = request.values.get('userid')
    startday = request.values.get('startDay')
    startti = request.values.get('startTime')
    endday = request.values.get('endDay')
    endti = request.values.get('endTime')
    reason = request.values.get('reason')
    handlemode = request.values.get('handle')
    file = ""

    starttime_str = startday + ' ' + startti + ":00"
    starttime = datetime.datetime.strptime(starttime_str, '%Y-%m-%d %H:%M:%S')
    endtime_str = endday + ' ' + endti + ":00"
    endtime = datetime.datetime.strptime(endtime_str, '%Y-%m-%d %H:%M:%S')

    if leaveService.add_leave(starttime, endtime, employee_id, reason,
                              handlemode, file):
        data = {'code': 200, 'data': '添加成功'}
        return Response(json.dumps(data))


#更新请假单
@app.route('/api/leave/update', methods=['POST'])
def updateList():
    leave_id = request.values.get('leaveid')
    employee_id = request.values.get('userid')
    startday = request.values.get('startDay')
    startti = request.values.get('startTime')
    endday = request.values.get('endDay')
    endti = request.values.get('endTime')
    reason = request.values.get('reason')
    handlemode = request.values.get('handle')
    file = ""

    starttime_str = startday + ' ' + startti + ":00"
    starttime = datetime.datetime.strptime(starttime_str, '%Y-%m-%d %H:%M:%S')
    endtime_str = endday + ' ' + endti + ":00"
    endtime = datetime.datetime.strptime(endtime_str, '%Y-%m-%d %H:%M:%S')

    if leaveService.update_leave(leave_id, starttime, endtime, employee_id,
                                 reason, handlemode, file):

        data = {'code': 200, 'data': '更新成功'}
        return Response(json.dumps(data))


#保存新的请假单至草稿箱
@app.route('/api/leave/save', methods=['POST'])
def newDraft():
    employee_id = request.values.get('userid')
    startday = request.values.get('startDay')
    startti = request.values.get('startTime')
    endday = request.values.get('endDay')
    endti = request.values.get('endTime')
    reason = request.values.get('reason')
    handlemode = request.values.get('handle')
    file = ""

    print("从前端获得的endday")
    print(endday)

    if startday:
        if startti:
            starttime_str = startday + ' ' + startti + ":00"
            starttime = datetime.datetime.strptime(starttime_str,
                                                   '%Y-%m-%d %H:%M:%S')
        else:
            starttime_str = startday
            starttime = datetime.datetime.strptime(starttime_str, '%Y-%m-%d')
    else:
        if startti:
            starttime_str = startti + ":00"
            starttime = datetime.datetime.strptime(starttime_str, '%H:%M:%S')
        else:
            starttime = None
    if endday:
        if endti:
            endtime_str = endday + ' ' + endti + ":00"
            endtime = datetime.datetime.strptime(endtime_str,
                                                 '%Y-%m-%d %H:%M:%S')
        else:
            endtime_str = endday
            endtime = datetime.datetime.strptime(endtime_str, '%Y-%m-%d')
    else:
        if endti:
            endtime_str = endti + ":00"
            endtime = datetime.datetime.strptime(endtime_str, '%H:%M:%S')
        else:
            endtime = None

    if leaveService.add_draft(starttime, endtime, employee_id, reason,
                              handlemode, file):
        data = {'code': 200, 'data': '添加成功'}
        return Response(json.dumps(data))


#更新请假单至草稿箱
@app.route('/api/leave/updatetodraft', methods=['POST'])
def updateDraft():
    leave_id = request.values.get('leaveid')
    employee_id = request.values.get('userid')
    startday = request.values.get('startDay')
    startti = request.values.get('startTime')
    endday = request.values.get('endDay')
    endti = request.values.get('endTime')
    reason = request.values.get('reason')
    handlemode = request.values.get('handle')
    file = ""

    if startday:
        if startti:
            starttime_str = startday + ' ' + startti + ":00"
            starttime = datetime.datetime.strptime(starttime_str,
                                                   '%Y-%m-%d %H:%M:%S')
        else:
            starttime_str = startday
            starttime = datetime.datetime.strptime(starttime_str, '%Y-%m-%d')
    else:
        if startti:
            starttime_str = startti + ":00"
            starttime = datetime.datetime.strptime(starttime_str, '%H:%M:%S')
        else:
            starttime = None
    if endday:
        if endti:
            endtime_str = endday + ' ' + endti + ":00"
            endtime = datetime.datetime.strptime(endtime_str,
                                                 '%Y-%m-%d %H:%M:%S')
        else:
            endtime_str = endday
            endtime = datetime.datetime.strptime(endtime_str, '%Y-%m-%d')
    else:
        if endti:
            endtime_str = endti + ":00"
            endtime = datetime.datetime.strptime(endtime_str, '%H:%M:%S')
        else:
            endtime = None

    if leaveService.update_draft(leave_id, starttime, endtime, employee_id,
                                 reason, handlemode, file):

        data = {'code': 200, 'data': '更新成功'}
        return Response(json.dumps(data))


#请假草稿箱界面
#界面初始化
@app.route('/api/leave/draft/initialize', methods=['POST'])
def findDraft():
    employee_id = request.values.get('userid')
    result = leaveService.findDraftByeid(employee_id)
    data = {'code': 200, 'data': result}
    return Response(json.dumps(data))


#请假处理界面
#界面初始化
@app.route('/api/leave/manage/initialize', methods=['POST'])
def findAll():
    userid = request.values.get('userid')
    flag = request.values.get('flag')

    if flag == '0':
        result = leaveService.findAllSubmit()
        data = {'code': 200, 'data': result}
    elif flag == '1':
        result = leaveService.findDepSubmit(userid)
        data = {'code': 200, 'data': result}
    else:
        data = {'code': 205, 'data': '你不应该能够操作这个板块'}

    return Response(json.dumps(data))


#操作同意或反对
@app.route('/api/leave/manage/handle', methods=['POST'])
def handle():
    leave_id = request.values.get('leaveid')
    processmode = request.values.get('processmode')
    if leaveService.update_processmode(leave_id, processmode):
        return {'code': 200, 'data': '更新成功'}


#查询操作
@app.route('/api/leave/manage/search', methods=['POST'])
def searchByInfo():
    flag = request.values.get('flag')
    userid = request.values.get('userid')

    date = request.values.get('date')
    searchid = request.values.get('searchid')
    searchhandlemode = request.values.get('searchhandlemode')
    searchprocessmode = request.values.get('searchprocessmode')

    if flag == '0':
        result = leaveService.searchByInfo_0(date, searchid, searchhandlemode,
                                             searchprocessmode)
        data = {'code': 200, 'data': result}
    elif flag == '1':
        result = leaveService.searchByInfo_1(userid, date, searchid,
                                             searchhandlemode,
                                             searchprocessmode)

        data = {'code': 200, 'data': result}
    else:
        data = {'code': 205, 'data': '你不应该能够操作这个板块'}
    return Response(json.dumps(data))


"""
考勤记录相关
"""


@app.route('/api/record_all', methods=['GET'])
def record_all():
    """
    获取所有考勤记录
    """
    data = att_record.find_all()
    result = Class2Data(data, att_record.__fields__, type=0)
    return Response(json.dumps({"code": 0, "data": result}))


@app.route('/api/record')
def individual_record():
    employee_id = request.args.get('employee')
    data = att_record.find_by_employee(employee_id)
    result = Class2Data(data, att_record.__fields__, type=0)
    print(result)
    return Response(json.dumps({"code": 0, "data": result}))


@app.route('/api/rank', methods=['GET'])
def rank():
    """
    获取员工考勤状况的统计
    """
    data = employee.find_all()
    data = Class2Data(data, employee.__fields__, type=0)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    if end_date is None:
        end_date = datetime.datetime.today()
    result = []
    for d in data:
        status = att_record.count_status(employee_id=d['employee_id'],
                                         start_date=start_date,
                                         end_date=end_date)
        print(status)
        item = {
            'employee_id': d['employee_id'],
            'name': d['employee_name'],
            'role': d['employee_title'],
            'dep': department.find_name_by_id(d['department_id']),
            'leave': status['leave'],
            'absence': status['absent'],
            'leave_early': status['early_out'],
            'late': status['late_in'],
        }
        if status['total'] == 0:
            item['attend_rate'] = 0
        else:
            item['attend_rate'] = format(status['finished'] / status['total'],'.2f')
        result.append(item)
        print(end_date)
    response = jsonify({"code": 0, "data": result})
    # return Response(json.dumps({"code": 0, "data": result}), content_type="application/json")
    return response


@app.route('/api/record_id')
def get_record_id():
    employee_id = request.args.get('employee_id')
    record_id = ind_record.find_by_employee_id(employee_id).record_id
    response = {"code": 0, "record_id": record_id}
    return jsonify(response)


@app.route("/api/face/verify", methods=["POST"])
def verify_face():
    employee_id = request.values.get('employee_id')
    setting_id = department.find_setting_by_did(
        employee.find_did_by_eid(employee_id))
    if setting_id is None:
        return jsonify({"code": 1, "message": "无考勤设置，请联系管理员"})
    # record_id = request.values.get('record_id')
    # print(record_id)
    face_data = request.get_json(silent=True)
    if face_data is None:
        return {"code": 0, "message": "无数据"}
    faces_b64 = face_data['face_data']

    try:
        known_faces = face.load_embeddings(employee_id)
        face.known_face_encodings = known_faces
    except FileNotFoundError as e:
        return jsonify({"code": 1, "error": f"没有{employee_id}的人脸数据"})

    data = {"code": 0, "result": 0, "time": "null", "status": "null"}
    for face_b64 in faces_b64:
        face_img_data = base64.b64decode(
            face_b64.strip("data:image/png;base64"))
        face_img = np.fromstring(face_img_data, np.uint8)
        if face.verify_faces(img=face_img):
            now_time = datetime.datetime.now().strftime('%H:%M:%S')
            show_now_time = now_time
            now_time = now_time.split(":")
            now_time = [int(time) for time in now_time]
            setting = att_setting.find_by_id(setting_id)
            total_now = now_time[0] * 3600 + now_time[1] * 60 + now_time[2]
            status = ["0", "0", "0", "0"]
            if ind_record.find_by_employee_id(employee_id).record_id is None:
                print("test")
                get_time = f'{setting.start}'
                get_time = get_time.split(":")
                get_time = [int(time) for time in get_time]
                total_get = get_time[0] * 3600 + get_time[1] * 60 + get_time[2]
                delta_time = total_now - total_get
                if delta_time > setting.elastic_time * 60:
                    status[2] = "1"
                status = "/".join(status)
                record_id = att_record.add_record(employee_id, setting_id,
                                                  datetime.datetime.now(),
                                                  None, status)
                ind_record.update(employee_id, record_id)
            else:
                get_time = f'{setting.end}'
                get_time = get_time.split(":")
                get_time = [int(time) for time in get_time]
                total_get = get_time[0] * 3600 + get_time[1] * 60 + get_time[2]
                delta_time = total_get - total_now
                record_id = ind_record.find_by_employee_id(
                    employee_id).record_id
                print(record_id)
                record = att_record.find_by_record_id(record_id)
                status = record.status
                status = status.split("/")
                if delta_time < setting.elastic_time * 60:
                    status[1] = "1"

                att_record.update_record(record_id, None,
                                         datetime.datetime.now(), status)
                ind_record.update(employee_id, None)
            now_date = datetime.datetime.now().strftime("%Y-%m-%d")
            data = {
                "code": 0,
                "nowtime": f'{now_date} {show_now_time}'
            }
            # now_time = datetime.datetime.now().strftime('%H:%M:%S')
            # now_date = datetime.datetime.now().strftime('%y-%m-%d')
            # now_time = datetime.datetime.strptime(now_time, '%H:%M:%S')
            # setting = att_setting.find_by_id(setting_id)
            # # get_time = setting.start

            # if ind_record.find_by_employee_id(employee_id) is None:
            #     get_time = datetime.datetime.strptime(
            #     f'{now_date} {setting.start}', '%y-%m-%d %H:%M:%S')
            #     delta = now_time - get_time
            #     time_limit = delta.seconds
            #     stats = 0
            #     if now_time < get_time:
            #         time_limit = -delta.seconds
            #     if time_limit <= 0:
            #         status = "0/0/0/0"
            #     elif time_limit > 0 and time_limit <= setting.elastic_time * 60:
            #         status = "0/0/1/0"
            #     elif time_limit > setting.elastic_time * 60:
            #         status = "1/0/0/0"
            #     record_id = att_record.add_record(employee_id, setting_id,
            #                                       datetime.datetime.now(),
            #                                       None, status)
            #     ind_record.add_record(employee_id, record_id)
            #     stats = 1
            # elif ind_record.find_by_employee_id(employee_id).record_id is None:
            #     get_time = datetime.datetime.strptime(
            #     f'{now_date} {setting.start}', '%y-%m-%d %H:%M:%S')
            #     delta = now_time - get_time
            #     time_limit = delta.seconds
            #     stats = 0
            #     if now_time < get_time:
            #         time_limit = -delta.seconds
            #     print(time_limit)
            #     if time_limit <= 0:
            #         status = "0/0/0/0"
            #     elif time_limit > 0 and time_limit <= setting.elastic_time * 60:
            #         status = "0/0/1/0"
            #     elif time_limit > setting.elastic_time * 60:
            #         status = "1/0/0/0"
            #     record_id = att_record.add_record(employee_id, setting_id,
            #                                       datetime.datetime.now(),
            #                                       None, status)
            #     ind_record.update(employee_id, record_id)
            #     stas = 1
            # else:
            #     get_time = datetime.datetime.strptime(
            #     f'{now_date} {setting.end}', '%y-%m-%d %H:%M:%S')
            #     delta = now_time - get_time
            #     time_limit = delta.seconds
            #     stats = 0
            #     if now_time < get_time:
            #         time_limit = -delta.seconds
            #     # status = att_record.find_by_record_id(record_id).status
            #     # if time_limit <= 0:
            #     #     status = status.split('/')
            #     #     status[2] = "1"
            #     #     status = "/".join(status)
            #     # ind_record.update(employee_id, None)
            #     # att_record.update_record(record_id, setting_id,
            #     #                          datetime.datetime.now(), status)
            # data = {
            #     "code": 0,
            #     "record_id": record_id,
            #     "time": "",
            #     "nexttime": "",
            #     "stats": stats
            # }
            break

    response = jsonify(data)
    return response


@app.route('/api/face/save', methods=['POST'])
def save_faces():
    employee_id = request.values.get('employee_id')
    face_data = request.get_json(silent=True)
    if face_data is None:
        return {"code": 1, "message": "无数据"}
    faces_b64 = face_data['face_data']
    path = f'./face_dataset/{employee_id}'
    if not os.path.exists(path):
        os.makedirs(path)

    lengnth = len(os.listdir(path))
    if lengnth < 5:
        index = lengnth
        code = 0
        useless_count = 0
        face_embeddings = []
        for face_b64 in faces_b64:
            face_img_data = base64.b64decode(
                face_b64.strip("data:image/png;base64"))
            face_img = np.fromstring(face_img_data, np.uint8)
            face_encodings = face.detect_and_align_face(face_img)
            if face_encodings is None:
                useless_count += 1
                code = 1
                continue
            face_encoding = face_encodings[0]
            face_embeddings.append(face_encoding)
            index += 1
            with open(f'./face_dataset/{employee_id}/{index}.png', 'wb') as f:
                f.write(face_img_data)
        face.save_embeddings(face_embeddings, employee_id)

        data = {"code": code, "useful": index, "useless": useless_count}
    else:
        code = 1
        data = {
            "code": code,
            "message": "已经有足够数据，无需再收集",
        }
    response = jsonify(data)
    return response


# 个人考勤记录
@app.route('/api/selfrecord')
def selfrecord():
    user_id = request.args.get('user_id')

    # 字符串
    start = request.args.get('start_day')
    end = request.args.get('end_day')
    # 转为date格式
    start_day = datetime.datetime.strptime(start, "%Y-%m-%d").date()
    end_day = datetime.datetime.strptime(end, "%Y-%m-%d").date()

    # 由于数据库between函数左闭右开，需要将end_day延后一天
    firstDay = start_day
    lastDay = end_day + datetime.timedelta(days=1)

    # 查表，并将结果转为python对象
    data = att_record.find_by_range(firstDay, lastDay, user_id)
    data = Class2Data(data, att_record.__fields__, type=0)

    #
    list = []
    for d in data:
        status = att_record.identify_status(d['status'])
        name = ''
        for s in status:
            if s == "finished":
                name = "出勤"
                break
            elif s == "leave":
                name = "请假"
                break
            elif s == "absent":
                name = "缺勤"
                break
            else:
                name = "迟到早退"
        item = {"name": name, "start": d['start_time'], "end": d['end_time']}
        list.append(item)
    return Response(json.dumps({"code": 0, "data": list}))


@app.route('/api/simplerecord', methods=['GET'])
def simplerecord():
    user_id = request.args.get('user_id')
    today = datetime.date.today()
    start_time = today + datetime.timedelta(days=-7)
    end_time = today

    list = []

    deltatime = (end_time - start_time).days
    for i in range(deltatime):
        temp_start = start_time + datetime.timedelta(days=i)
        temp_end = temp_start + datetime.timedelta(days=1)
        data = att_record.find_by_range(temp_start, temp_end, user_id)
        # data_temp = Class2Data(data, att_record.__fields__, type=0)
        hours = 0
        for d in data:
            print("------------------------")
            # 根据打卡情况进行统计判断
            temp_status = {'status': getattr(d, 'status')}
            status = att_record.identify_status(temp_status['status'])
            print(status)
            for s in status:
                if s == "finished" or s == 'early_out' or s == 'late_in':  # 仅有迟到早退和正常打卡才能计算时间
                    # 获得当次的起始时间和结束时间
                    temp_start_time = getattr(d, 'start_time')
                    temp_end_time = getattr(d, 'end_time')
                    hours += (temp_end_time -
                              temp_start_time).total_seconds() / 60 / 60
                    break
                else:
                    break
        list.append(hours)
    print(list)
    return Response(json.dumps({"code": 0, "data": list}))


@app.route('/api/simplerank', methods=['GET'])
def simplerank():
    """
    获取员工考勤状况的统计
    """
    today = datetime.date.today()
    yesterday = today + datetime.timedelta(days=-1)
    # print(yesterday,today)

    # 找到所有员工
    data = employee.find_all()
    data = Class2Data(data, employee.__fields__, type=0)
    result = []
    rank = []
    for d in data:
        status = att_record.count_status(employee_id=d['employee_id'],
                                         start_date=yesterday,
                                         end_date=today)
        rate = 0
        if status['total'] != 0:
            rate = (status['finished'] / status['total'])
        rank.append(rate)
        rate = '{:.0%}'.format(rate)
        item = {"姓名": d['employee_name'], "出勤率": rate}
        result.append(item)

    # 冒泡排序
    L = len(rank)
    for i in range(L - 1):
        for j in range(L - 1 - i):
            if rank[j] < rank[j + 1]:
                temp = rank[j]
                rank[j] = rank[j + 1]
                rank[j + 1] = temp

                temp = result[j]
                result[j] = result[j + 1]
                result[j + 1] = temp

    # 截取前10个员工
    if L > 6:
        result = result[0:6]
    return Response(json.dumps({"code": 0, "data": result}))


@app.route('/api/facechecked', methods=['GET'])
def facechecked():
    user_id = request.args.get('user_id')
    return "ok"


@app.route('/api/deleteattsetting', methods=['POST'])
def deleteattsetting():
    id = request.form.get('id')
    setting_id = int(id)
    print(setting_id)
    result = att_setting.delete_setting(setting_id=setting_id)
    return Response(json.dumps(result))


@app.route('/api/attsettinglist', methods=['GET'])
def attsettinglist():
    data = att_setting.find_all()
    data = Class2Data(data, att_setting.__fields__, type=0)

    result = []
    for d in data:
        id = int(d["setting_id"])

        timeDelta = datetime.time.strftime(
            d['start'], "%H:%M:%S") + "-" + datetime.time.strftime(
                d['end'], "%H:%M:%S")
        dateDelta = datetime.date.strftime(
            d['date_start'], "%Y-%m-%d") + "/" + datetime.date.strftime(
                d['date_end'], "%Y-%m-%d")
        # str(d['date_start'])+":"+str(getattr(d,'date_end'))
        elasticTime = int(d['elastic_time'])
        weekDays = str(d['week_days'])
        state = "待激活"
        if department.find_setting_by_did(1) == id:
            state = "已激活"
        temp = {
            'id': id,
            'timeDelta': timeDelta,
            'dateDelta': dateDelta,
            'elasticTime': elasticTime,
            'state': state,
            'weekDays': weekDays
        }
        result.append(temp)
    return Response(json.dumps({"code": 0, "data": result}))


@app.route('/api/newattsetting', methods=['POST'])
def newattsetting():
    startDay = request.form.get('startDay')
    endDay = request.form.get('endDay')
    startTime = request.form.get('startTime')
    endTime = request.form.get('endTime')
    weekDays = request.form.get('weekDays')
    elasticTime = request.form.get('elasticTime')
    #    def add_setting(self, start, end, elastic_time, date_start, date_end,
    #                    week_days):
    date_start = datetime.datetime.strptime(startDay, "%Y-%m-%d").date()
    date_end = datetime.datetime.strptime(endDay, "%Y-%m-%d").date()

    start = datetime.datetime.strptime(startTime, "%H:%M").time()
    end = datetime.datetime.strptime(endTime, "%H:%M").time()
    elastic_time = int(elasticTime)
    result = att_setting.add_setting(date_start=date_start,
                                     date_end=date_end,
                                     start=start,
                                     end=end,
                                     elastic_time=elastic_time,
                                     week_days=weekDays)

    return Response(json.dumps(result))


@app.route('/api/updateattsetting', methods=['POST'])
def updateattsetting():
    id = request.form.get('id')
    startDay = request.form.get('startDay')
    endDay = request.form.get('endDay')
    startTime = request.form.get('startTime')
    endTime = request.form.get('endTime')
    weekDays = request.form.get('weekDays')
    elasticTime = request.form.get('elasticTime')
    #    def add_setting(self, start, end, elastic_time, date_start, date_end,
    #                    week_days):
    date_start = datetime.datetime.strptime(startDay, "%Y-%m-%d").date()
    date_end = datetime.datetime.strptime(endDay, "%Y-%m-%d").date()

    start = datetime.datetime.strptime(startTime, "%H:%M:%S").time()
    end = datetime.datetime.strptime(endTime, "%H:%M:%S").time()
    elastic_time = int(elasticTime)
    setting_id = int(id)
    result = att_setting.update_setting(setting_id=setting_id,
                                        date_start=date_start,
                                        date_end=date_end,
                                        start=start,
                                        end=end,
                                        elastic_time=elastic_time,
                                        week_days=weekDays)

    return Response(json.dumps(result))


@app.route('/api/addtodo', methods=['POST'])
def add_todo():
    employee_id = request.values.get('employee_id')
    title = request.form.get('title')
    subtitle = request.form.get('subtitle')
    content = request.form.get('content')
    deadline = request.form.get('deadline')
    deadline = datetime.datetime.strptime(deadline, '%Y-%m-%d %H:%M:%S')
    state = request.form.get('state')
    checked = 0
    if state == "true":
        state = 1
    else:
        state = 0
    starttime = datetime.datetime.now()
    if todo.add_todo(employee_id, title, subtitle, content, deadline,
                     starttime, state, checked):
        response = jsonify({"code": 0, "result": "OK"})
    else:
        response = jsonify({"code": 1, "result": "NOT OK"})
    return response


@app.route('/api/gettodo', methods=['GET'])
def get_todo():
    employee_id = request.args.get('employee_id')
    todo_list = todo.find_by_eid(employee_id)
    data = []
    try:
        for t in todo_list:
            item = {
                'id': t.id,
                'employee_id': t.employee_id,
                'title': t.title,
                'subtitle': t.subtitle,
                'deadline': t.deadline.strftime('%Y-%m-%d %H:%M:%S'),
                'starttime': t.starttime.strftime('%Y-%m-%d %H:%M:%S'),
                'content': t.content,
                'state': t.state,
                'checked': t.checked,
            }
            data.append(item)
        response = jsonify({"code": 0, "data": data})
    except Exception as e:
        response = jsonify({"code": 1, "result": "获取失败"})
    return response


# 入口
if __name__ == '__main__':

    app.run(debug=True)