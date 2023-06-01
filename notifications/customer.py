from .main import Notification


class CustomerNotification(Notification):

    def promocodes(self, recipient, subject, content):
        self.send(recipients=[recipient,],
                  subject=subject,
                  content=content)