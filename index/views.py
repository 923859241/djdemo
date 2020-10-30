from django.shortcuts import render
from django.http import HttpResponse
from index.feedback import dealWithStr
import json
import os
from django.conf import settings
from index.feedback import SVMModelName


file_ = open(os.path.join(settings.BASE_DIR, "index/"+SVMModelName))

def index_view(request):
    global resp
    try:
        resp = {
            'code': '200',
            'message': 'success',
            'data': {
                'default': str(dealWithStr(request.GET.get('data'))),
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
