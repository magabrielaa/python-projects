def get_unauthorized_accesses(security_log):

    d = {}
    access = True

    for log, (event, id, room, time) in enumerate(security_log):
        if id not in d:
            d[id] = []
            if event == "REVOKE":
                access = False
            elif event == "GRANT":
                access = True
            elif event == "SWIPE":
                access = False

            log += 1
            if not access and event == "SWIPE":
                d[id].append(room)
                d[id].append(time)
        
    return d 