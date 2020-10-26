from models.leave import Leave
from utils.exts import db
import json
import datetime

from utils.class2data import Class2Data
from service.department_service import DepartmentService
from service.employee_service import EmployeeService

employeeService = EmployeeService()
departmentService = DepartmentService()


class LeaveService:
    def __init__(self):
        self.__fields__ = [
            'leave_id', 'starttime', 'endtime', 'pushtime', 'handletime',
            'employee_id', 'reason', 'handlemode', 'processmode', 'file'
        ]

    #查找，通过employee_id查找所有的请假单
    def findLeaveByeid(self, eid):
        leaveList = Leave.query.filter_by(employee_id=eid).filter_by(
            issubmit=1).all()
        leaveListData = Class2Data(leaveList, self.__fields__, 0)
        leaveNum = Leave.query.filter_by(employee_id=eid).filter_by(
            issubmit=1).count()
        doingNum = Leave.query.filter_by(employee_id=eid).filter_by(
            processmode='审核中').filter_by(issubmit=1).count()
        passNum = Leave.query.filter_by(employee_id=eid).filter_by(
            processmode='已通过').filter_by(issubmit=1).count()
        rejectedNum = Leave.query.filter_by(employee_id=eid).filter_by(
            processmode='未通过').filter_by(issubmit=1).count()
        data = {
            'leaveNum': leaveNum,
            'doingNum': doingNum,
            'passNum': passNum,
            'rejectedNum': rejectedNum,
            'mess': leaveListData
        }
        return data

    # 查找，通过employee_id和 日期 查找所有的请假单
    def findLeaveByeid_date(self, eid, date):
        leaveList = Leave.query.filter_by(employee_id=eid).filter_by(
            issubmit=1).all()
        searchLeaveList = []
        doingNum = 0
        passNum = 0
        rejectedNum = 0

        for item in leaveList:
            starttime = getattr(item, 'starttime')
            startday = datetime.datetime.strftime(starttime, '%Y-%m-%d')
            if date == startday:
                searchLeaveList.append(item)
                processmode = getattr(item, 'processmode')
                if processmode == '审核中':
                    doingNum += 1
                if processmode == '已通过':
                    passNum += 1
                if processmode == '未通过':
                    rejectedNum += 1

        searchLeaveListData = Class2Data(searchLeaveList, self.__fields__, 0)
        leaveNum = len(searchLeaveList)

        data = {
            'leaveNum': leaveNum,
            'doingNum': doingNum,
            'passNum': passNum,
            'rejectedNum': rejectedNum,
            'mess': searchLeaveListData
        }
        return data

    #删除请假单
    def deleteByLid(self, leaveid):
        if (self.findCountByLid(leaveid) == 1):
            try:
                leave = self.findByLid(leaveid)
                db.session.delete(leave)
                db.session.commit()
                return {'code': 200, 'data': '删除成功'}
            except Exception as e:
                db.session.rollback()
                raise e
        else:
            return {'code': 202, 'data': '查找的数据不存在'}

    #查找，通过leave_id查找
    def findCountByLid(self, leaveid):
        return Leave.query.filter_by(leave_id=leaveid).count()

    def findByLid(self, leaveid):
        return Leave.query.filter_by(leave_id=leaveid).first()

    #新增请假单
    def add_leave(self, starttime, endtime, employee_id, reason, handlemode,
                  file):
        pushtime = datetime.datetime.now()
        leave = Leave(starttime, endtime, pushtime, employee_id, reason,
                      handlemode, "审核中", file, 1)
        try:
            db.session.add(leave)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e

    #更新请假单并提交
    def update_leave(self, leave_id, starttime, endtime, employee_id, reason,
                     handlemode, file):
        pushtime = datetime.datetime.now()
        print(leave_id)
        leave = Leave.query.filter_by(leave_id=leave_id).first()

        leave.starttime = starttime
        leave.endtime = endtime
        leave.employee_id = employee_id
        leave.reason = reason
        leave.handlemode = handlemode
        leave.pushtime = pushtime
        leave.file = file
        leave.issubmit = 1

        db.session.commit()
        return True

    #新的请假单保存至草稿箱
    def add_draft(self, starttime, endtime, employee_id, reason, handlemode,
                  file):
        pushtime = datetime.datetime.now()
        leave = Leave(starttime, endtime, pushtime, employee_id, reason,
                      handlemode, "审核中", file, 0)
        try:
            db.session.add(leave)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e

    #更新请假单并保存至草稿箱
    def update_draft(self, leave_id, starttime, endtime, employee_id, reason,
                     handlemode, file):
        pushtime = datetime.datetime.now()
        leave = Leave.query.filter_by(leave_id=leave_id).first()

        leave.starttime = starttime
        leave.endtime = endtime
        leave.employee_id = employee_id
        leave.reason = reason
        leave.handlemode = handlemode
        leave.pushtime = pushtime
        leave.file = file
        leave.issubmit = 0

        db.session.commit()
        return True

    #查找，员工草稿箱
    def findDraftByeid(self, eid):
        leaveList = Leave.query.filter_by(employee_id=eid).filter_by(
            issubmit=0).all()
        leaveListData = Class2Data(leaveList, self.__fields__, 0)
        return leaveListData

    #查找，超级管理员界面初始化
    def findAllSubmit(self):
        leaveList = Leave.query.filter_by(issubmit=1).all()
        leaveListData = []
        for item in leaveList:
            temp = {}
            for f in self.__fields__:
                if f in ['starttime', 'endtime', 'pushtime', 'handletime'
                         ] and getattr(item, f):
                    # 特殊数据处理 举例：时间戳——>2020-02-02 20:02:02
                    temp[f] = datetime.datetime.strftime(
                        getattr(item, f), "%Y-%m-%d %H:%M:%S")
                elif f == 'employee_id':
                    e_id = getattr(item, f)

                    employee = employeeService.find_by_eid(e_id)
                    department_id = employee.department_id
                    department_name = departmentService.find_name_by_id(
                        department_id)
                    temp[f] = e_id
                    temp['employee_name'] = employee.employee_name
                    temp['department_name'] = department_name
                else:
                    temp[f] = getattr(item, f)
            leaveListData.append(temp)

        leaveNum = Leave.query.filter_by(issubmit=1).count()
        doingNum = Leave.query.filter_by(processmode='审核中').filter_by(
            issubmit=1).count()
        data = {
            'leaveNum': leaveNum,
            'doingNum': doingNum,
            'mess': leaveListData
        }
        return data

    #查找，部门经理界面初始化
    def findDepSubmit(self, leader_id):
        leaveListData = []
        leaveNum = 0
        doingNum = 0
        employee_ids = employeeService.find_employee_by_leader_id(leader_id)
        for employee_id in employee_ids:
            leaveList = Leave.query.filter_by(
                employee_id=employee_id).filter_by(issubmit=1).all()
            for item in leaveList:
                temp = {}
                for f in self.__fields__:
                    if f in ['starttime', 'endtime', 'pushtime', 'handletime'
                             ] and getattr(item, f):
                        # 特殊数据处理 举例：时间戳——>2020-02-02 20:02:02
                        temp[f] = datetime.datetime.strftime(
                            getattr(item, f), "%Y-%m-%d %H:%M:%S")
                    elif f == 'employee_id':
                        e_id = getattr(item, f)

                        employee = employeeService.find_by_eid(e_id)
                        department_id = employee.department_id
                        department_name = departmentService.find_name_by_id(
                            department_id)
                        temp[f] = e_id
                        temp['employee_name'] = employee.employee_name
                        temp['department_name'] = department_name
                    elif f == 'processmode':
                        leaveNum += 1
                        temp[f] = getattr(item, f)
                        if (getattr(item, f) == "审核中"):
                            doingNum += 1
                    else:
                        temp[f] = getattr(item, f)
                leaveListData.append(temp)
        data = {
            'leaveNum': leaveNum,
            'doingNum': doingNum,
            'mess': leaveListData
        }
        return data

    #查询操作，超级管理员
    def searchByInfo_0(self, date, searchid, searchhandlemode,
                       searchprocessmode):
        leaveList = Leave.query.filter_by(issubmit=1).all()
        if date:
            leaveList = self.filterbydate(leaveList, date)
        if searchid:
            leaveList = self.myfilter(leaveList, 'employee_id', searchid)
        if searchhandlemode:
            leaveList = self.myfilter(leaveList, 'handlemode',
                                      searchhandlemode)
        if searchprocessmode:
            leaveList = self.myfilter(leaveList, 'processmode',
                                      searchprocessmode)
        leaveListData = []
        for item in leaveList:
            temp = {}
            for f in self.__fields__:
                if f in ['starttime', 'endtime', 'pushtime', 'handletime'
                         ] and getattr(item, f):
                    # 特殊数据处理 举例：时间戳——>2020-02-02 20:02:02
                    temp[f] = datetime.datetime.strftime(
                        getattr(item, f), "%Y-%m-%d %H:%M:%S")
                elif f == 'employee_id':
                    e_id = getattr(item, f)

                    employee = employeeService.find_by_eid(e_id)
                    department_id = employee.department_id
                    department_name = departmentService.find_name_by_id(
                        department_id)
                    temp[f] = e_id
                    temp['employee_name'] = employee.employee_name
                    temp['department_name'] = department_name
                else:
                    temp[f] = getattr(item, f)
            leaveListData.append(temp)

        leaveNum = Leave.query.filter_by(issubmit=1).count()
        doingNum = Leave.query.filter_by(processmode='审核中').filter_by(
            issubmit=1).count()
        data = {
            'leaveNum': leaveNum,
            'doingNum': doingNum,
            'mess': leaveListData
        }
        return data

    #按照属性过滤
    def myfilter(self, datalist, f, filter_f):
        returnlist = []
        for item in datalist:
            if (getattr(item, f) == filter_f):
                returnlist.append(item)
        return returnlist

    #按照日期过滤
    def filterbydate(self, datalist, date):
        returnlist = []
        for item in datalist:
            starttime = getattr(item, 'starttime')
            startday = datetime.datetime.strftime(starttime, '%Y-%m-%d')
            if date == startday:
                returnlist.append(item)
        return returnlist

    # 查询操作，部长
    def searchByInfo_1(self, leader_id, date, searchid, searchhandlemode,
                       searchprocessmode):
        leaveListData = []
        leaveNum = 0
        doingNum = 0
        employee_ids = employeeService.find_employee_by_leader_id(leader_id)

        for employee_id in employee_ids:
            leaveList = Leave.query.filter_by(
                employee_id=employee_id).filter_by(issubmit=1).all()

            if date:
                leaveList = self.filterbydate(leaveList, date)
            if searchid:
                leaveList = self.myfilter(leaveList, 'employee_id', searchid)
            if searchhandlemode:
                leaveList = self.myfilter(leaveList, 'handlemode',
                                          searchhandlemode)
            if searchprocessmode:
                leaveList = self.myfilter(leaveList, 'processmode',
                                          searchprocessmode)
            for item in leaveList:
                temp = {}
                for f in self.__fields__:
                    if f in ['starttime', 'endtime', 'pushtime', 'handletime'
                             ] and getattr(item, f):
                        # 特殊数据处理 举例：时间戳——>2020-02-02 20:02:02
                        temp[f] = datetime.datetime.strftime(
                            getattr(item, f), "%Y-%m-%d %H:%M:%S")
                    elif f == 'employee_id':
                        e_id = getattr(item, f)

                        employee = employeeService.find_by_eid(e_id)
                        department_id = employee.department_id
                        department_name = departmentService.find_name_by_id(
                            department_id)
                        temp[f] = e_id
                        temp['employee_name'] = employee.employee_name
                        temp['department_name'] = department_name
                    elif f == 'processmode':
                        leaveNum += 1
                        temp[f] = getattr(item, f)
                        if (getattr(item, f) == "审核中"):
                            doingNum += 1
                    else:
                        temp[f] = getattr(item, f)
                leaveListData.append(temp)
        data = {
            'leaveNum': leaveNum,
            'doingNum': doingNum,
            'mess': leaveListData
        }
        return data

    #请求审核操作
    def update_processmode(self, leave_id, processmode):
        handletime = datetime.datetime.now()
        leave = Leave.query.filter_by(leave_id=leave_id).first()
        leave.handletime = handletime
        print(processmode)
        leave.processmode = processmode
        db.session.commit()
        return True
