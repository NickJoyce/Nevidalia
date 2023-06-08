from .main import Notification
from promocode.models import NotificationRecipients


class AdminNotification(Notification):
    APP_ERROR = "[APP ERROR]"
    DATA_ERROR = "[DATA_ERROR]"
    COPY = "[COPY]"

    def get_admin_recipients(self):
        return [(recipient.name, recipient.email) for recipient in NotificationRecipients.objects.all()]

    def send_promocodes_error(self, order_id):
        subject = f"{self.DATA_ERROR} Уведомление с промокодами не отправлено покупателю"
        content = f"Доступных для отправки промокодов нет или их недостаточно для всех заказанных товаров\n" \
                  f"Номер заказа: {order_id}"
        self.send(recipients=self.get_admin_recipients(),
                  subject=subject,
                  content=content)

    def order_webhook_payload_handling_error(self, traceback, body):
        subject = f"{self.APP_ERROR} 500 Internal Server Error"
        content = f"{traceback}\nrequest body:\n{body}"
        self.send(recipients=self.get_admin_recipients(),
                  subject=subject,
                  content=content)

    def get_email_notification_template_error(self, order_id):
        subject = f"{self.DATA_ERROR} Шаблона email уведомления не существует"
        content = f"Уведомление с промокодами не отправлено покупателю\nНомер заказа: {order_id}"
        self.send(recipients=self.get_admin_recipients(),
                  subject=subject,
                  content=content)

    def send_promocodes_copy(self, subject, content):
        """Пересылка дубликата сообщения с промокодами администратору"""
        subject = f"{self.COPY} --- {subject} ---"
        self.send(recipients=self.get_admin_recipients(),
                  subject=subject,
                  content=content)