from django.db import models
from django.core.cache import cache

# Create your models here.
class CustomAdminPage(models.Model):
    class Meta:
        verbose_name = 'Загрузка файла'
        verbose_name_plural = "Загрузка файла"
        app_label = 'promocode'


class Promocode(models.Model):
    date_of_create = models.DateField(verbose_name="Дата создания")
    start_date = models.DateField(verbose_name="Начало")
    end_date = models.DateField(verbose_name="Окончание")
    park = models.CharField(max_length=255, verbose_name="Парк")
    creator = models.CharField(max_length=255, verbose_name="Создатель")
    action_name = models.CharField(max_length=255, verbose_name="Название акции")
    tilda_external_product_id = models.CharField(max_length=255, verbose_name="Внешний код")
    code = models.CharField(max_length=255, verbose_name="Код", unique=True)
    status = models.BooleanField(verbose_name="Статус", default=False)
    date_of_use = models.DateField(verbose_name="Дата использования", null=True, blank=True, default=None)
    ticket_limit = models.CharField(max_length=255, verbose_name="Лимит билета", null=True, blank=True)
    ticket_day_type = models.CharField(max_length=255, verbose_name="День недели", null=True, blank=True)
    customer_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Имя")
    customer_phone = models.CharField(max_length=255, null=True, blank=True, verbose_name="Телефон")
    customer_email = models.EmailField(null=True, blank=True, verbose_name="email")
    sending_date = models.DateTimeField(null=True, blank=True, verbose_name="Дата отправки уведомления")

    class Meta:
        verbose_name = "Промокод"
        verbose_name_plural = "Промокоды"

    def __str__(self):
        return f"{self.code}"




class NotificationRecipients(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(null=True, blank=True, verbose_name="Email")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Получатель служебных уведомлений"
        verbose_name_plural = "Получатели служебных уведомлений"

    def __str__(self):
        return f"{self.name}"


class EmailNotificationTemplate(models.Model):
    code = models.IntegerField(verbose_name="Код уведомления")
    name = models.CharField(max_length=100, verbose_name="Наименование уведомления")
    subject = models.CharField(max_length=255, verbose_name="Тема")
    content = models.TextField(max_length=2000, verbose_name="Сообщение")

    class Meta:
        verbose_name = "Шаблон email уведомления"
        verbose_name_plural = "Шаблоны email уведомлений"

    def __str__(self):
        return f"{self.name}"


class SingletonModel(models.Model):

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        pass

    def set_cache(self):
        cache.set(self.__class__.__name__, self)

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

        self.set_cache()

    @classmethod
    def load(cls):
        if cache.get(cls.__name__) is None:
            obj, created = cls.objects.get_or_create(pk=1)
            if not created:
                obj.set_cache()
        return cache.get(cls.__name__)


class Settings(SingletonModel):
    is_active_promocode_notification = models.BooleanField(default=False,
                                                           verbose_name="Email уведомление покупателю после оплаты заказа",
                                                           help_text="В выключенном состоянии уведомления отправляются "
                                                                     "только если email адрес указанный при оформлении"
                                                                     " есть в списке раздела Получатели Уведомлений")

    class Meta:
        verbose_name = "Настройки"
        verbose_name_plural = "Настройки"

    def __str__(self):
        return "Настройки"