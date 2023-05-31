from django.shortcuts import render, redirect
import json
from secrets import compare_digest
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .tasks import test_task
from django.views.decorators.http import require_POST
from django.db.transaction import atomic, non_atomic_requests
from project.settings.base import WEBHOOK_API_KEY
from .utils import Order, Customer, OrderItem
from .models import Promocode

# Create your views here.
# celery
def celery_task_inside(request):
    test_task.delay()
    return redirect('index')

#webhooks
@csrf_exempt
@require_POST
@non_atomic_requests
def order_webhook(request):
    given_token = request.headers.get("webhook-api-key", "")
    if compare_digest(given_token, WEBHOOK_API_KEY):
        payload = json.loads(request.body)
        order_webhook_payload_handling(payload)
        return HttpResponse(status=200, reason="OK")
    else:
        return HttpResponse(status=403, reason="API key isn't valid")


@atomic
def order_webhook_payload_handling(payload):
    order = Order(customer=Customer(name=payload['name'],
                                    email=payload['email'],
                                    phone=payload['phone']),
                  order_id=payload['payment']['orderid'],
                  amount=payload['amount'],
                  park=payload['park'],
                  items=[OrderItem(**item) for item in payload['payment']['products']])

    print()





    Parks = ["волгоград", "сергиев посад", "сургут", "тюмень", "улан-удэ"]
    ProductActionIdentWords = ["будни", "выходные", "двухчасовой", "часовой"]




    # логика выбора промокодов
    # qnt - кол - во промокодов
    # name - тариф промокода
    # парк - город
    # Тюмень Будни 1



    promocodes = ...






