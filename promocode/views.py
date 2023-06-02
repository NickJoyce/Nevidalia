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
from .models import Promocode, Settings, NotificationRecipients
from jinja2 import Template
from project.settings.base import BASE_DIR
from notifications.customer import CustomerNotification
from notifications.admin import AdminNotification
import traceback

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
        try:
            order_webhook_payload_handling(json.loads(request.body))
        except:
            AdminNotification().order_webhook_payload_handling_error(traceback.format_exc())
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


        need_to_send = False
        # отправка уведомлений с промокодами активирована
        if Settings.load().is_active_promocode_notification:
            need_to_send = True
        else:
            notification_recipients = NotificationRecipients.objects.all()
            # email из заказа есть в списке получателей уведомлений
            if order.customer.email in [recipient.email for recipient in notification_recipients]:
                # получатель уведомлений активен
                if [r.is_active for r in notification_recipients if r.email == order.customer.email][0]:
                    need_to_send = True

        if need_to_send:
            recipient = (order.customer.name, order.customer.email)
            CustomerNotification().send_promocodes(recipient=recipient, subject=subject, content=content)
    else:
        AdminNotification().send_promocodes_error(order_id=order.order_id)

















