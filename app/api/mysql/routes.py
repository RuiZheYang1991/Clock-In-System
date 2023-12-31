from api.mysql.controllers.controller import EmployeeAPI, ClockRecordAPI,EarlyClockIn,MissingClockOut

def register_routes(api):

    #查詢員工資料
    api.add_resource(EmployeeAPI, '/api/employee')
    # 打卡功能API
    api.add_resource(ClockRecordAPI, '/api/clock-record')
    # 早到員工API
    api.add_resource(EarlyClockIn, '/api/early-clockin')
    # 未打下班卡員工API
    api.add_resource(MissingClockOut, '/api/missing-clockout')