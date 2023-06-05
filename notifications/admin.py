from .main import Notification
from promocode.models import NotificationRecipients


class AdminNotification(Notification):
    APP_ERROR = "[APP ERROR]"
    DATA_ERROR = "[DATA_ERROR]"

    def get_admin_recipients(self):
        return [(recipient.name, recipient.email) for recipient in NotificationRecipients.objects.all()]

    def send_promocodes_error(self, order_id):
        subject = f"{self.DATA_ERROR} Уведомление с промокодами не отправлено покупателю"
        content = f"Доступных для отправки промокодов нет или их недостаточно для всех заказанных товаров\n" \
                  f"Номер заказа: {order_id}"
        self.send(recipients=self.get_admin_recipients(),
                  subject=subject,
                  content=content)

    def order_webhook_payload_handling_error(self, traceback):
        subject = f"{self.APP_ERROR} Ошибка при обработке данных поступивших через через вебхук"
        content = traceback
        self.send(recipients=self.get_admin_recipients(),
                  subject=subject,
                  content=content)

    def get_email_notification_template_error(self, order_id):
        subject = f"{self.DATA_ERROR} Шаблона email уведомления не существует"
        content = f"Уведомление с промокодами не отправлено покупателю\nНомер заказа: {order_id}"
        self.send(recipients=self.get_admin_recipients(),
                  subject=subject,
                  content=content)