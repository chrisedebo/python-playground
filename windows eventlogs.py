import win32evtlog

server = 'localhost' # name of the target computer to get event logs
logtype = 'System'
hand = win32evtlog.OpenEventLog(server,logtype)
flags = win32evtlog.EVENTLOG_BACKWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ
total = win32evtlog.GetNumberOfEventLogRecords(hand)

print ('I made it to here!')

events = win32evtlog.ReadEventLog(hand, flags,0)
i = 0
while True:
    if events:
        for event in events:
            print ('Event Category:', event.EventCategory)
            print ('Time Generated:', event.TimeGenerated)
            print ('Source Name:', event.SourceName)
            print ('Event ID:', event.EventID)
            print ('Event Type:', event.EventType)
            data = event.StringInserts
            if data:
                print ('Event Data:')
                for msg in data:
                    print (msg)
            break

