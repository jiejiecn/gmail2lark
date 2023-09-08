import zmail
import requests, json, time, re, datetime
import message, gmail, feishu


now = datetime.datetime.now()
log_time = now.strftime("%Y-%m-%d %H:%M:%S")

name_pattern = 'NAME\:.*'
time_pattern = 'START TIME\:.*'
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
    
        msg = message.msg_card
        msg['card']['header']['title']['content'] = mail['subject']

        if (mail['subject'].find('Alert Cleared') >= 0):
            msg['card']['header']['template'] = 'green'
        else:
            msg['card']['header']['template'] = 'red'

        content = mail['content_text'][0]

        result = re.search(name_pattern, content, flags=re.M)
        if result:
            msg['card']['elements'][0]['text']['content'] = result.group()

        result = re.search(time_pattern, content, flags=re.M)
        if result:
            msg['card']['elements'][3]['text']['content'] = result.group()

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






