from django import template
from datetime import datetime
import pytz
register = template.Library()

@register.filter
def mul(value, arg):
    return value * arg

@register.filter
def number_format(value):
    try:
        value = int(value)
        return "{:,}".format(value)
    except (ValueError, TypeError):
        return value
    
@register.filter
def get_hour(value):
    return value.hour

@register.filter
def get_minute(value):
    return value.minute

@register.filter
def custom_date_format(value):
    datetime_obj = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")
    
    formatted_date = datetime_obj.strftime("%d/%m/%Y")
    
    return formatted_date

@register.filter
def custom_datetime_format(value):
    # Chuyển đổi chuỗi ngày tháng thành đối tượng datetime
    # datetime_obj = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")

    # Chuyển múi giờ sang múi giờ Việt Nam
    vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    datetime_obj = value.replace(tzinfo=pytz.utc).astimezone(vn_tz)

    # Format lại đối tượng datetime thành chuỗi theo định dạng mong muốn
    formatted_date = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")  
    
    return formatted_date
