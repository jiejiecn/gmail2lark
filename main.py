import zmail
import requests, json, time, re
from datetime import datetime
import message, gmail, feishu
import msg_cleared, msg_html
import logger, timeshift


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
    logger.log(' Inbox: ', count)

    for n in range(1, count + 1):
        mail = server.get_mail(1)
        logger.log(' Get mail: ', n)
        logger.log(' Subject: ', mail['subject'])

        if (len(mail['content_text']) <= 0):
            msg = msg_html.msg_card
            msg['card']['header']['title']['content'] = mail['subject']
            msg['card']['header']['template'] = 'blue'

        else:

            if (mail['subject'].find('Alert Cleared') >= 0):
                msg = msg_cleared.msg_card                                         #Cleared Email Template
                msg['card']['header']['title']['content'] = mail['subject']
                msg['card']['header']['template'] = 'green'


                content = mail['content_text'][0]

                result = re.search(name_pattern, content, flags=re.M)
                if result:
                    name = result.group()
                    msg['card']['header']['title']['content'] = name.replace('NAME:', 'Alert Cleared =>')
                    #msg['card']['elements'][0]['text']['content'] = result.group()

                result = re.search(cpcode_pattern, content, flags=re.M)
                if result:
                    cpcode = result.group()
                    cpcode = ' '.join(cpcode.split())
                    msg['card']['elements'][0]['text']['content'] = cpcode

                result = re.search(cpdesc_pattern, content, flags=re.M)
                if result:
                    desc = result.group()
                    desc = ' '.join(desc.split())
                    msg['card']['elements'][1]['text']['content'] = desc
                
                result = re.search(time_pattern, content, flags=re.M)
                if result:
                    start_time = result.group()
                    start_time = start_time.replace('START TIME:', '')
                    cst_time = timeshift.toCST(start_time)
                    start_time = "START TIME: " + cst_time.strftime("%Y-%m-%d %H:%M %Z%z")
                    msg['card']['elements'][2]['text']['content'] = start_time

                result = re.search(endtime_pattern, content, flags=re.M)            #Add stop time for alert cleared
                if result:
                    end_time = result.group()
                    end_time = end_time.replace('STOP TIME:', '')
                    cst_endtime = timeshift.toCST(end_time)
                    end_time = "STOP TIME: " + cst_endtime.strftime("%Y-%m-%d %H:%M %Z%z")
                    msg['card']['elements'][3]['text']['content'] = end_time
                
                logger.log(" ", msg)


                resp = requests.post(webhook, data=json.dumps(msg), headers=header)
                logger.log(" Response: ", resp.text)

            else:
                msg = message.msg_card
                msg['card']['header']['title']['content'] = mail['subject']
                msg['card']['header']['template'] = 'red'


                content = mail['content_text'][0]

                result = re.search(name_pattern, content, flags=re.M)
                if result:
                    name = result.group()
                    msg['card']['header']['title']['content'] = name.replace('NAME:', 'New Alert =>')
                    #msg['card']['elements'][0]['text']['content'] = result.group()

                result = re.search(cpcode_pattern, content, flags=re.M)
                if result:
                    cpcode = result.group()
                    cpcode = ' '.join(cpcode.split())
                    msg['card']['elements'][0]['text']['content'] = cpcode

                result = re.search(cpdesc_pattern, content, flags=re.M)
                if result:
                    desc = result.group()
                    desc = ' '.join(desc.split())
                    msg['card']['elements'][1]['text']['content'] = desc
                
                result = re.search(time_pattern, content, flags=re.M)
                if result:
                    start_time = result.group()
                    start_time = start_time.replace('START TIME:', '')
                    cst_time = timeshift.toCST(start_time)
                    start_time = "START TIME: " + cst_time.strftime("%Y-%m-%d %H:%M %Z%z")
                    msg['card']['elements'][2]['text']['content'] = start_time

                logger.log(" ", msg)


                resp = requests.post(webhook, data=json.dumps(msg), headers=header)
                logger.log(" Response: ", resp.text)


    time.sleep(30)






