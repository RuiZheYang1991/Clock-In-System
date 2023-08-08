from datetime import datetime

def str_to_dtNow(clock_time):
    # 將 clock_time 字串轉換為 datetime 物件
    dt_object = datetime.strptime(clock_time, '%Y-%m-%d %H:%M')

    # 提取時間部分
    dtNow = dt_object.time()

    return dtNow
def check_data_format(clock_type_str):
    try:
        # 檢查 clock_type 是否為 'clockIn' 或 'clockOut'
        if clock_type_str not in ('clockIn', 'clockOut'):
            raise ValueError('Invalid clock_type')
        # 如果資料格式都正確，回傳 True
        return True

    except ValueError:
        # 若有任何錯誤發生，回傳 False
        return False