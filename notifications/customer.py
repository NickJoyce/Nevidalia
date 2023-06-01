from .main import Notification


class CustomerNotification(Notification):

    def send_promocodes(self, recipient, subject, content):
        self.send(recipients=[recipient,],
                  subject=subject,
                  content=content)