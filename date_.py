def convert_secs_to_string(secs):
    """초(second)를 HH:mm:ss 문자 형태로 변환한다.

    Parameters:
        secs (integer): 초
    """
    secs = int(secs)
    mins, secs = divmod(secs, 60)
    hours, mins = divmod(mins, 60)
    days, hours = divmod(hours, 24)
    if days > 0:
        return '%ddays %02d:%02d:%02d' % (days, hours, mins, secs)
    else:
        return '%02d:%02d:%02d' % (hours, mins, secs)
