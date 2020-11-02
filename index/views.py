from django.shortcuts import render
from django.http import HttpResponse
from index.feedback import dealWithStr
import json
import os
from django.conf import settings
from index.feedback import SVMModelName
import base64


file_ = open(os.path.join(settings.BASE_DIR, "index/"+SVMModelName))

def index_view(request):
    global resp
    #解码
    encodeData = request.GET.get('data')


    try:
        base64_decrypt = base64.b64decode(encodeData.encode('utf-8'))
        decodeData = str(base64_decrypt, 'utf-8')

        print("BASE64解密串（UTF-8）:\n", decodeData)
        resp = {
            'code': '200',
            'message': 'success',
            'data': {
                'default': str(dealWithStr( decodeData )),
            }
        }
    except Exception:
        resp = {
            'code': '200',
            'message': 'failure',
            'data': {
                'default': "True",
            }
        }
    finally:
        response = HttpResponse(content=json.dumps(resp), content_type='application/json;charset = utf-8',
                                status='200',
                                reason='success',
                                charset='utf-8')
        return response


# Create your views here.
