def weekday_month_day_year(dt):
    if dt:
        return dt.strftime("%A, %B %d, %Y")
    else:
        return ""
