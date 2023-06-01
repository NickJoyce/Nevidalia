from smtplib import SMTP_SSL
from email.message import EmailMessage
import os

from jinja2 import Template
from email.utils import make_msgid
import imghdr


class Notification():
    def __init__(self):
        self.host = os.getenv('EMAIL_HOST')
        self.port = int(os.getenv('EMAIL_PORT'))
        self.user = os.getenv('EMAIL_HOST_USER')
        self.password = os.getenv('EMAIL_HOST_PASSWORD')
        self.from_name = "Никита Смирнов"
        self.from_email = self.user


    def add_content(self, msg, content):
        msg.set_content(content)
        return msg


    def attach_images(self, msg, images: list[tuple]):
        """attach images
        images - [(image, filename), ...]
        """
        for image, filename in images:
            with open(image, 'rb') as f:
                img_data = f.read()
            msg.add_attachment(img_data, maintype='image', subtype=imghdr.what(None, img_data), filename=filename)
        return msg


    def attach_files(self, msg, files: list[tuple]):
        """attach files with internal format of the application programme: pdf, docx, xlsx, etc. from files list
        files - [(file, filename), ...]
        """
        for file, filename in files:
            msg.add_attachment(file, subtype='octet-stream', filename=filename)
        return msg


    def add_html(self, msg, html, template_images, template_data):
        img_dict = {}
        # add modified file name as a key and cid as a value to the dictionary
        # the modification is that the dots are replaced with underscores in the file names
        if template_images:
            for image in template_images:
                template_var = os.path.basename(image).replace('.', '_')
                img_dict[template_var] = make_msgid()[1:-1]

        with open(html) as f:
            t = Template(f.read())

        msg.add_alternative(t.render(**img_dict, **template_data if template_data else dict()), subtype='html')

        if template_images:
            # adds images to html
            for image in template_images:
                with open(image, 'rb') as img:
                    img_data = img.read()
                    template_filename = os.path.basename(image).replace('.', '_')
                    ind = len(msg.get_payload()) - 1
                    msg.get_payload()[ind].add_related(img_data,
                                                       'image',
                                                       imghdr.what(None, img_data),
                                                       cid=img_dict[template_filename],
                                                       filename=image)
        return msg


    def send(self, recipients, subject, content,
             images=None,
             files=None,
             html=None, template_images=None, template_data=None):
        """recipients - list of tuples
         tuple - содержит 2 элемента: имя и email получателя"""
        messages = []
        for name, email in recipients:
            msg = EmailMessage()
            msg['subject'] = subject
            msg['from'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = email

            if content:
                self.add_content(msg, content)

            # add html
            if html:
                msg = self.add_html(msg, html, template_images, template_data)

            # add images
            if images:
                msg = self.attach_images(msg, images)

            # add files
            if files:
                msg = self.attach_files(msg, files)

            messages.append(msg)
        self.send_messages(messages)



    def send_messages(self, messages):
        with SMTP_SSL(self.host, self.port) as smtp:
            smtp.ehlo()
            smtp.login(self.user, self.password)

            for message in messages:
                smtp.send_message(message)


    def msg_template(self):
        recipients = [('Никита', 'actan-spb@mail.ru'),]

        subject = f"[TEST]"

        # plain text
        content = ""

        # images
        images = [('images/photo.jpeg', "photo.jpeg"),]

        # files
        files = [('images/sample.pdf', "sample_changed.pdf"),]

        # html
        html = "templates/notification_theme_kotlavas.html"
        # html = "templates/simple.html"
        template_images = ["images/photo.jpeg"]
        template_data = dict(a=[1, 2, 3, 4])

        self.send(recipients=recipients,
                  subject=subject,
                  content=None,
                  images=None,
                  files=None,
                  html=html, template_images=template_images, template_data=template_data)




if __name__ == "__main__":
    Notification().msg_template()
