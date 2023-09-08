import zmail
import requests, json, time, re
from datetime import datetime
import message, gmail, feishu
import msg_cleared


now = datetime.now()
log_time = now.strftime("%Y-%m-%d %H:%M:%S")


alert_in_dt_format = "%a, %b %d, %H:%M %Z %Y"                         #Tue, Sep 5, 08:45 GMT 2023
alert_out_dt_format = "YYYY/MM/DD HH:mm"        #2023/09/04 11:43

name_pattern = 'NAME\:.*'
time_pattern = 'START TIME\:.*'
endtime_pattern = 'STOP TIME\:.*'
cpcode_pattern = 'CP Code\:.*'
cpdesc_pattern = 'CP Code Description\:.*'

webhook = feishu.webhook
header = {'Content-Type': 'application/json'}


while(True):
    server = zmail.server(gmail.username, gmail.password, pop_host=gmail.popserver, pop_ssl=True)

    count,size = server.stat()
    print(log_time, ' Inbox: ', count)

    for n in range(1, count + 1):
        print(log_time, ' Get mail: ', n)
        mail = server.get_mail(1)
        print(log_time, ' Subject: ', mail['subject'])


        if (mail['subject'].find('Alert Cleared') >= 0):
            msg = msg_cleared.msg_card                                         #Cleared Email Template
            msg['card']['header']['title']['content'] = mail['subject']
            msg['card']['header']['template'] = 'green'


            content = mail['content_text'][0]

            result = re.search(name_pattern, content, flags=re.M)
            if result:
                msg['card']['elements'][0]['text']['content'] = result.group()

            result = re.search(time_pattern, content, flags=re.M)
            if result:
                str_starttime = result.group()
                starttime = datetime.strptime(str_starttime, alert_in_dt_format)
                msg['card']['elements'][3]['text']['content'] = starttime.strftime(alert_out_dt_format)

            result = re.search(cpcode_pattern, content, flags=re.M)
            if result:
                msg['card']['elements'][1]['text']['content'] = result.group()

            result = re.search(cpdesc_pattern, content, flags=re.M)
            if result:
                msg['card']['elements'][2]['text']['content'] = result.group()
            
            result = re.search(endtime_pattern, content, flags=re.M)            #Add stop time for alert cleared
            if result:
                str_endtime = result.group()
                endtime = datetime.strptime(str_endtime, alert_in_dt_format)
                msg['card']['elements'][4]['text']['content'] = endtime.strftime(alert_out_dt_format)
            


            print(log_time, " ", msg)


            resp = requests.post(webhook, data=json.dumps(msg), headers=header)
            print(log_time, " Response: ", resp.text)

        else:
            msg = message.msg_card
            msg['card']['header']['title']['content'] = mail['subject']
            msg['card']['header']['template'] = 'red'


            content = mail['content_text'][0]

            result = re.search(name_pattern, content, flags=re.M)
            if result:
                msg['card']['elements'][0]['text']['content'] = result.group()

            result = re.search(time_pattern, content, flags=re.M)
            if result:
                str_starttime = result.group()
                starttime = datetime.strptime(str_starttime, alert_in_dt_format)
                msg['card']['elements'][3]['text']['content'] = starttime.strftime(alert_out_dt_format)

            result = re.search(cpcode_pattern, content, flags=re.M)
            if result:
                msg['card']['elements'][1]['text']['content'] = result.group()

            result = re.search(cpdesc_pattern, content, flags=re.M)
            if result:
                msg['card']['elements'][2]['text']['content'] = result.group()

            print(log_time, " ", msg)


            resp = requests.post(webhook, data=json.dumps(msg), headers=header)
            print(log_time, " Response: ", resp.text)


    time.sleep(30)






