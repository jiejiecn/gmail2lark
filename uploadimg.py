import requests
from requests_toolbelt import MultipartEncoder

import feishu

def upload(imageFile):
    url = "https://open.feishu.cn/open-apis/im/v1/images"
    
    form = {'image_type': 'message',
            'image': (open(imageFile, 'rb'))}  
    
    headers = {
        'Authorization': 'Bearer ' + feishu.image_token
    }
    
    
    multi_form = MultipartEncoder(form)
    
    headers['Content-Type'] = multi_form.content_type

    response = requests.request("POST", url, headers=headers, data=multi_form)
    
    print(response.headers['X-Tt-Logid'])  # for debug or oncall
    print(response.content)  # Print Response

