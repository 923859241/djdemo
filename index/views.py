from django.shortcuts import render
from django.http import HttpResponse
from index.feedback import dealWithStr
import json


def index_view(request):
    resp = {
        'code': '200',
        'message': 'success',
        'data': {
            'default': str(dealWithStr(request.GET.get('data'))),
        },
    }
    response = HttpResponse(content=json.dumps(resp), content_type='application/json;charset = utf-8',
                            status='200',
                            reason='success',
                            charset='utf-8')

    return response

# Create your views here.
