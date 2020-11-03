from django.shortcuts import render
from django.http import HttpResponse
from index.feedback import dealWithStr
import json
import os
from django.conf import settings
from index.feedback import SVMModelName
import base64

file_ = open(os.path.join(settings.BASE_DIR, "index/" + SVMModelName))


def index_view(request):
    global resp
    # 解码
    encodeData = str(request.GET.get('data'))
    encodeData = encodeData.replace(" ", '+')

    print(encodeData)

    try:
        base64_decrypt = base64.b64decode(encodeData)
        print(base64_decrypt)
        decodeData = str(base64_decrypt, 'utf-8')

        print("BASE64解密串（UTF-8）:\n", decodeData)
        resp = {
            'code': '200',
            'message': 'success',
            'data': {
                'meaningful': str(dealWithStr(decodeData)),
            }
        }
        print("结果:\n", resp['data'])
    except Exception:
        print(Exception.args)
        resp = {
            'code': '200',
            'message': 'failure',
            'data': {
                'meaningful': "True",
            }
        }
    finally:
        response = HttpResponse(content=json.dumps(resp), content_type='application/json;charset = utf-8',
                                status='200',
                                reason='success',
                                charset='utf-8')
        return response


if __name__ == '__main__':
    encodeData = '77yf44CBOu+8geWugw=='
    base64_decrypt = base64.b64decode(encodeData)
    decodeData = str(base64_decrypt, 'utf-8')
    print(decodeData)
# Create your views here.
