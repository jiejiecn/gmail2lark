from datetime import datetime
from pytz import timezone

#_time = "Fri, Aug 25, 11:54 GMT 2023"
akamai_format = "%a, %b %d, %H:%M %Z %Y"
tz_utc = timezone('UTC')
tz_cst = timezone('Asia/Shanghai')


def toCST(str_time: str, format: str = akamai_format, tz: timezone = tz_utc):
    str_time = str_time.strip()
    dt_time = datetime.strptime(str_time, format)
    dt_time = dt_time.replace(tzinfo=tz_utc)
    cst_time = dt_time.astimezone(tz_cst)

    return cst_time
    # print(dt_time)
    # print(dt_time.tzinfo)
    # print(cst_time.strftime("%Y-%m-%d %H:%M %Z%z"))
