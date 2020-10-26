# 配置 sqlalchemy
HOST = '8.129.163.104'
PORT = '3306'
DATABASE = 'kaoqin'
USERNAME = 'root'
PASSWORD = '45f0970b12f1dd5b'

DB_URI = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8".format(
    username=USERNAME, password=PASSWORD, host=HOST, port=PORT, db=DATABASE)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True
JSON_SORT_KEYS = False  # don't sort when jsonify