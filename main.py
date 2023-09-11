import zmail
import requests, json, time, re
from datetime import datetime
import message, gmail, feishu
import msg_cleared, msg_html, msg_error, msg_hitserror
import logger, timeshift


name_pattern = 'NAME\:.*'
time_pattern = 'START TIME\:.*'
endtime_pattern = 'STOP TIME\:.*'
cpcode_pattern = 'CP Code\:.*'
cpdesc_pattern = 'CP Code Description\:.*'

#############################################


#############################################
condition_pattern = ""


#############################################
hits_pattern = "Hits\:.*"
errors_pattern = "Errors\:.*"
hits_keywords = ["Edge Errors", "HTTP Status", "Server Failure"]

#############################################
traffic_pattern = ""
traffic_keywords = ["Low Traffic", "High Traffic"]



webhook = feishu.webhook
header = {'Content-Type': 'application/json'}


while(True):
    try:
        server = zmail.server(gmail.username, gmail.password, pop_host=gmail.popserver, pop_ssl=True)
        count,size = server.stat()
        logger.log('Inbox:', count)

        for n in range(1, count + 1):
            mail = server.get_mail(1)
            logger.log('Get mail:', n)
            logger.log('From:', mail['from'])
            logger.log('Subject:', mail['subject'])

            # mail_from = str(mail['from'])
            # if(mail_from.find('noreply@akamai.com') < 0):           #Not from Akamai, drop it
            #    break

            if (len(mail['content_text']) <= 0):                    #Html content, skip
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
                        name = result.group().strip()
                        msg['card']['header']['title']['content'] = name.replace('NAME:', 'Alert Cleared =>')

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

                    result = re.search(endtime_pattern, content, flags=re.M)           
                    if result:
                        end_time = result.group()
                        end_time = end_time.replace('STOP TIME:', '')
                        cst_endtime = timeshift.toCST(end_time)
                        end_time = "STOP TIME:  " + cst_endtime.strftime("%Y-%m-%d %H:%M %Z%z")
                        msg['card']['elements'][3]['text']['content'] = end_time
                    
                    # duration = cst_endtime - cst_time                   
                    # msg['card']['elements'][4]['text']['content'] = duration

                    logger.log(msg)


                    resp = requests.post(webhook, data=json.dumps(msg), headers=header)
                    logger.log("Response:", resp.text)

                else:
                    subject = mail['subject']
                    if any(e in subject for e in hits_keywords):            #Origin Server Failure, Origin HTTP Status, Edge Error
                        msg = msg_hitserror.msg_card
                        msg['card']['header']['title']['content'] = mail['subject']
                        msg['card']['header']['template'] = 'red'


                        content = mail['content_text'][0]

                        result = re.search(name_pattern, content, flags=re.M)
                        if result:
                            name = result.group().strip()
                            msg['card']['header']['title']['content'] = name.replace('NAME:', 'New Alert =>')

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
                        
                        result = re.search(hits_pattern, content, flags=re.M)
                        if result:
                            hits = result.group()
                            msg['card']['elements'][3]['text']['content'] = hits

                        result = re.search(errors_pattern, content, flags=re.M)
                        if result:
                            errors = result.group()
                            msg['card']['elements'][4]['text']['content'] = errors



                        logger.log(msg)


                        resp = requests.post(webhook, data=json.dumps(msg), headers=header)
                        logger.log("Response:", resp.text)


                    if any(e in content for e in traffic_keywords):                     #Low Traffice, High Traffic
                        msg = message.msg_card
                        msg['card']['header']['title']['content'] = mail['subject']
                        msg['card']['header']['template'] = 'red'

                        content = mail['content_text'][0]

                        result = re.search(name_pattern, content, flags=re.M)
                        if result:
                            name = result.group().strip()
                            msg['card']['header']['title']['content'] = name.replace('NAME:', 'New Alert =>')

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
                        
                        # result = re.search(hits_pattern, content, flags=re.M)
                        # if result:
                        #     hits = result.group()
                        #     msg['card']['elements'][3]['text']['content'] = hits

                        # result = re.search(errors_pattern, content, flags=re.M)
                        # if result:
                        #     errors = result.group()
                        #     msg['card']['elements'][4]['text']['content'] = errors



                        logger.log(msg)


                        resp = requests.post(webhook, data=json.dumps(msg), headers=header)
                        logger.log("Response:", resp.text)

        
        time.sleep(30)

    except Exception as ex:
        msg = msg_error.msg_card
        msg['card']['header']['title']['content'] = mail['subject']
        msg['card']['header']['template'] = 'blue'

        logger.log(msg)
        logger.log(ex)

        resp = requests.post(webhook, data=json.dumps(msg), headers=header)
        logger.log("Response:", resp.text)

        time.sleep(5)
    