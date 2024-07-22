# myapp/views.py
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from requests.auth import HTTPBasicAuth
import uuid
import json

clientId = 'S2_c69537fcca7b470ea19db11a7f5dcf84'
secretKey = 'fef1725500514b5e96605e5d82ab1c0b'

def index(request):
    return render(request, 'index.html', {
        'orderId': uuid.uuid4(),
        'clientId': clientId
    })

def cancel(request):
    return render(request, 'cancel.html')

@csrf_exempt
def server_auth(request):
    if request.method == 'POST':
        try:
            print('https://sandbox-api.nicepay.co.kr/v1/payments/' + request.POST['tid'])
            response = requests.post(
                'https://sandbox-api.nicepay.co.kr/v1/payments/' + request.POST['tid'],
                json={
                    'amount': request.POST['amount']
                },
                headers={
                    'Content-type': 'application/json',
                    'Authorization': 'Basic ' + secretKey
                },
                auth=HTTPBasicAuth(clientId, secretKey)
            )

            res_dict = response.json()
            print(res_dict)

            return render(request, 'payment/response.html', {
                'resultMsg': res_dict['resultMsg']
            })

        except requests.exceptions.RequestException as e:
            return HttpResponse(str(e), status=500)
    return HttpResponse(status=405)

@csrf_exempt
def cancel_auth(request):
    if request.method == 'POST':
        try:
            response = requests.post(
                'https://sandbox-api.nicepay.co.kr/v1/payments/' + request.POST['tid'] + '/cancel',
                json={
                    'amount': request.POST['amount'],
                    'reason': 'test',
                    'orderId': str(uuid.uuid4())
                },
                headers={
                    'Content-type': 'application/json'
                },
                auth=HTTPBasicAuth(clientId, secretKey)
            )

            res_dict = response.json()
            print(res_dict)

            return render(request, 'payment/response.html', {
                'resultMsg': res_dict['resultMsg']
            })

        except requests.exceptions.RequestException as e:
            return HttpResponse(str(e), status=500)
    return HttpResponse(status=405)

@csrf_exempt
def hook(request):
    if request.method == 'POST':
        print(request.body)
        return HttpResponse("ok", status=200)
    return HttpResponse(status=405)