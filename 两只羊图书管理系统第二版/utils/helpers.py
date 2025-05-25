import datetime

def get_current_date():
    """获取当前日期"""
    return datetime.date.today().strftime("%Y-%m-%d")

def calculate_due_date(borrow_date, days=30):
    """计算应还日期"""
    borrow = datetime.datetime.strptime(borrow_date, "%Y-%m-%d").date()
    due_date = borrow + datetime.timedelta(days=days)
    return due_date.strftime("%Y-%m-%d")

def format_borrow_status(borrow_date):
    """格式化借阅状态"""
    today = datetime.date.today()
    borrow = datetime.datetime.strptime(borrow_date, "%Y-%m-%d").date()
    due_date = borrow + datetime.timedelta(days=30)
    
    if today > due_date:
        overdue_days = (today - due_date).days
        return f"已逾期{overdue_days}天"
    elif today == due_date:
        return "今日到期"
    else:
        days_left = (due_date - today).days
        return f"剩余{days_left}天"