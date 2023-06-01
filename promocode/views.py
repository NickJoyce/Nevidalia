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
from jinja2 import Template
from project.settings.base import BASE_DIR
from notifications.customer import CustomerNotification

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
    # данные поступающие через вебхук
    order = Order(customer=Customer(name=payload['name'],
                                    email=payload['email'],
                                    phone=payload['phone']),
                  order_id=payload['payment']['orderid'],
                  amount=payload['payment']['amount'],
                  park=payload['park'],
                  items=[OrderItem(**item) for item in payload['payment']['products']])

    # Добавляем промокоды к позициям заказа
    for item in order.items:
        all_active_promocodes = Promocode.objects.filter(tilda_external_product_id=item.externalid, status=False)
        if len(all_active_promocodes) >= item.quantity:
            for promocode in all_active_promocodes[:item.quantity]:
                item.promocodes.append(promocode)
        else:
            break

    # если у всех позиций есть хоть 1 промокод
    if all([item.promocodes for item in order.items]):
        # Меняем статусы у промокодов и сохраняем их
        for item in order.items:
            for promocode in item.promocodes:
                print(promocode.pk)
                promocode.status = True
                promocode.save()

        with open(f"{BASE_DIR}/notifications/templates/promocodes_subject.txt", encoding="utf-8") as f:
            subject = Template(f.read()).render(order=order)

        with open(f"{BASE_DIR}/notifications/templates/promocodes_content.txt", encoding="utf-8") as f:
            content = Template(f.read()).render(order=order)

        recipient = (order.customer.name, order.customer.email)
        CustomerNotification().promocodes(recipient=recipient, subject=subject, content=content)




        print("Отправляем уведомление")
    else:
        print("Уведомление покупателю не отправлено: Доступных для отправки промокодов нет или их недостаточно для всех заказанных товаров")






    # if products_with_promocodes:
    #     # меняем статусы у отправлемых промокодов
    #     for tilda_external_product_id, promocodes in products_with_promocodes.values():
    #         for promocode in promocodes:
    #             promocode.status = True
    #             promocode.save()

    #     with open(f"{BASE_DIR}/notifications/templates/promocodes_content.txt", encoding="utf-8") as f:
    #         xml_file = f.read()
    #         rendered_template = Template(xml_file).render(
    #             order=order
    #         )
    #         # print(rendered_template)
    # else:
    #     pass













