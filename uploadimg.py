import requests, json, os
from requests_toolbelt import MultipartEncoder

import feishu, logger

def upload(imageFile):
    url = "https://open.feishu.cn/open-apis/im/v1/images"
    
    form = {'image_type': 'message',
            'image': (open(imageFile, 'rb'))}  
    
    headers = {
        'Authorization': 'Bearer ' + getToken()
    }
    
    multi_form = MultipartEncoder(form)
    
    headers['Content-Type'] = multi_form.content_type

    response = requests.request("POST", url, headers=headers, data=multi_form)
    logger.log(response.text)

    image_key = "N/A"

    if response.status_code == 200:
        raw_data = str(response.text)
        data = json.loads(raw_data)
        image_key = data["data"]["image_key"]    
    
    os.remove(imageFile)

    return image_key



def getToken():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"

    headers = {
        'Content-Type': 'application/json; charset=utf-8'
    }

    body = {
        'app_id': feishu.app_id,
        'app_secret': feishu.app_secret
    }

    response = requests.request("POST", url, headers=headers, data=json.dumps(body))
    logger.log(response.text)
    
    tenant_token = "Token_Error"

    if response.status_code == 200:
        data = json.loads(response.text)
        tenant_token = data["tenant_access_token"]

    return tenant_token
