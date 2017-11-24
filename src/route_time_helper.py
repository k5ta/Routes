def calc_time(last_time, additive_time):
    new_minutes = new_hours = 0
    if type(additive_time) == int:
        new_minutes = int(last_time[-2:]) + additive_time
        new_hours = int(last_time[-5:-3])
    else:
        new_minutes = int(last_time[-2:]) + int(additive_time[-2:])
        new_hours = int(last_time[-5:-3]) + int(additive_time[-5:-3])
    if new_minutes >= 60:
        new_minutes = new_minutes - 60
        new_hours = new_hours + 1
    new_time = (str(new_hours) if new_hours >= 10 else "0" + str(new_hours)) + ":"
    return new_time + (str(new_minutes) if new_minutes >= 10 else "0" + str(new_minutes))
