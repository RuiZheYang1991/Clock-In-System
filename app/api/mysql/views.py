from flask import Blueprint, request
from flask_restful import Resource, Api,abort
from .models import db, Employee, ClockRecord,MySQLModel
from datetime import datetime, time
from ..utils.helpers import check_data_format
from sqlalchemy import func,and_,asc
import time as times
mysql_bp = Blueprint('mysql', __name__)

class MyTest(Resource):
    def get(self,text):
        times.sleep(1)
        return {'message':text}

    def post(self, text):
        new_data = MySQLModel(data=text)

        try:
            db.session.add(new_data)
            db.session.commit()
            return {'message': 'Data added successfully', 'data': text}, 201
        except:
            db.session.rollback()
            return {'message': 'Failed to add data'}, 500


# 員工資料查詢API
class EmployeeAPI(Resource):
    def get(self):
        rest_time = 90*60 #休息時間
        rest_line = datetime.strptime('13:30', '%H:%M').time()
        str_date = request.args.get('date')  # 2023-08-04
        #若沒有提供日期 則默認查詢當天
        if not str_date:
            date = datetime.now().date()
        else:
            date = datetime.strptime(str_date, "%Y-%m-%d").date()
        record_data = ClockRecord.query.filter(
            func.DATE(ClockRecord.clockIn) == date).all()
        #將員工編號和上下班時間寫入字典
        employee_times = {}
        for record in record_data:
            employee_number = record.employeeNumber
            if employee_number not in employee_times:
                employee_times[employee_number] = {'clockIn': record.clockIn, 'clockOut': record.clockOut}
            else:
                # 更新員工的下班時間
                employee_times[employee_number]['clockOut'] = record.clockOut

            # 計算每位員工的總工時
        for employee_number, times in employee_times.items():
            clock_in = times['clockIn']
            clock_out = times['clockOut']
            if clock_in and clock_out:
                # 計算工時差異，得到總工時（以小時為單位）
                if clock_out.time()>rest_line:
                    #下班時間超過午休 工時減去90分鐘
                    total_hours = ((clock_out - clock_in).seconds- rest_time) / 3600
                else:
                    total_hours = (clock_out - clock_in).seconds / 3600
                times['totalHours'] = round(total_hours, 2)
                times['clockIn'] = clock_in.strftime('%Y-%m-%d %H:%M:%S')
                times['clockOut'] = clock_out.strftime('%Y-%m-%d %H:%M:%S')
            else:
                # 如果員工有缺席打卡，將總工時設為 None
                times['totalHours'] = None
                times['clockIn'] = clock_in.strftime('%Y-%m-%d %H:%M:%S') if clock_in else None
                times['clockOut'] = clock_out.strftime('%Y-%m-%d %H:%M:%S') if clock_out else None
        return employee_times

# 打卡功能API
class ClockRecordAPI(Resource):
    def post(self):
        data = request.get_json()
        employee_number = data.get('employeeNumber')
        dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        msg=""
        clock_record = None
        # 檢查員工是否存在
        employee = Employee.query.filter_by(employeeNumber=employee_number).first()
        if not employee:
            abort (404, message = 'Employee not found')


        # 檢查員工今天是否已經進行過上班或下班打卡
        today = datetime.now().date()
        existing_clock_in = ClockRecord.query.filter(
            and_(func.DATE(ClockRecord.clockIn) == today, ClockRecord.employeeNumber == employee_number)).first()

        existing_clock_out = ClockRecord.query.filter(
            and_(func.DATE(ClockRecord.clockOut) == today, ClockRecord.employeeNumber == employee_number)).first()


        if not existing_clock_in:
            # 今天尚未打卡，進行打卡紀錄
            msg = '上班打卡'
            clock_record = ClockRecord(employeeNumber=employee_number, clockIn=dt)
        else:
            #已打上班卡，判定下班打卡
            if not existing_clock_out:
                msg = '下班打卡'
                existing_clock_in.clockOut = dt
                db.session.commit()
            else:
                abort(422, message='error: 請勿重複打卡(下班)')

        if clock_record is not None:
            db.session.add(clock_record)
            db.session.commit()
        db.session.close()
        retmsg = {'message': msg}
        return retmsg, 201

    # 補打卡功能API
    def put(self):
        data = request.get_json()
        employee_number = data.get('employeeNumber')
        clock_time = data.get('clockTime')#"YYYY-MM-DD HH:MM:SS"
        clock_type = data.get('clockType')#clockIn or clockOut
        clock_record = None
        check_ret = check_data_format(clock_type_str=clock_type)
        # 檢查員工是否存在
        employee = Employee.query.filter_by(employeeNumber=employee_number).first()
        if not employee:
            abort(404, message='error: Employee not found')
        if not check_ret:
            abort(404, message=f'error: Invalid "clockType"')
        msg=""
        try:
            if not clock_time:
                clock_time = datetime.now()
                clock_date = datetime.now().date()
            else:
                clock_time = datetime.strptime(clock_time, "%Y-%m-%d %H:%M:%S")
                clock_date = clock_time.date()
        except ValueError as e:
            abort(404, message=f'error: {str(e)}"')


        # today = datetime.now().date()
        existing_clock_out = ClockRecord.query.filter(
            and_(func.DATE(ClockRecord.clockOut) == clock_date, ClockRecord.employeeNumber == employee_number)).first()

        existing_clockIn = ClockRecord.query.filter(
            and_(func.DATE(ClockRecord.clockIn) == clock_date, ClockRecord.employeeNumber == employee_number)).first()
        # 檢查員工今天是否已經進行過上班或下班打卡
        if clock_type == "clockIn":
            if not existing_clockIn:
                # 今天尚未打卡，進行打卡紀錄
                msg = '補打卡成功(上班)'
                clock_record = ClockRecord(employeeNumber=employee_number, clockIn=clock_time)
            else:
                abort(422 , message='error: 已有打卡紀錄(上班)')

        elif clock_type == "clockOut":
            if not existing_clock_out:
                if existing_clockIn:
                    msg = '補打卡成功(下班)'
                    existing_clockIn.clockOut = clock_time
                    db.session.commit()
                else:
                    abort(422, message='error: 今日尚無打卡紀錄，請先打上班卡')
            else:
                abort(422 , message='error: 重複補打卡(下班)')
        if clock_record is not None:
            db.session.add(clock_record)
            db.session.commit()
        db.session.close()

        retmsg = {'message': msg}
        return retmsg, 201


#查日期區間未打下班卡
class MissingClockOut(Resource):
    def get(self):
        date_range = request.args.get('date')
        try:
            start_date_str, end_date_str = date_range.split(':')
        except:
            abort(404,message="error: chack query 'date'")
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

        # 從資料庫查詢指定日期區間未打下班卡的員工
        missing_clock_out_employees = {}
        records = ClockRecord.query.filter(and_(ClockRecord.clockOut == None, ClockRecord.clockIn != None)).all()
        for record in records:
            if record.clockIn:
                if start_date <= record.clockIn.date() <= end_date:
                    clock_date = datetime.strftime(record.clockIn,"%Y-%m-%d")
                    if clock_date in missing_clock_out_employees:
                        missing_clock_out_employees[clock_date].append(record.employeeNumber)
                    else:
                        missing_clock_out_employees[clock_date]=list()
                        missing_clock_out_employees[clock_date].append(record.employeeNumber)

        return missing_clock_out_employees

# 早到員工API
class EarlyClockIn(Resource):
    def get(self):
        date_str = request.args.get('date')
        if not date_str:
            target_date = datetime.now().date()
        else:
            target_date = datetime.strptime(date_str, '%Y-%m-%d')

        # 從資料庫查詢指定日期當天前五名最早打卡上班的員工
        early_clock_in_employees = []
        records = ClockRecord.query.filter(ClockRecord.clockIn >= target_date).order_by(asc(ClockRecord.clockIn)).limit(5).all()
        for record in records:
            early_clock_in_employees.append({
                'employeeNumber': record.employeeNumber,
                'clockIn': record.clockIn.strftime('%Y-%m-%d %H:%M:%S'),
            })

        return early_clock_in_employees