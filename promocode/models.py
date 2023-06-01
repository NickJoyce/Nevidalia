from django.db import models

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
    tilda_external_product_id = models.CharField(max_length=255, verbose_name="Внешний код товара (Тильда)")
    code = models.CharField(max_length=255, verbose_name="Код", unique=True)
    status = models.BooleanField(verbose_name="Статус", default=False)
    date_of_use = models.DateField(verbose_name="Дата использования", null=True, blank=True, default=None)
    ticket_limit = models.CharField(max_length=255, verbose_name="Лимит", null=True, blank=True,
                             default="часовой")
    ticket_day_type = models.CharField(max_length=255, verbose_name="Тип дня недели", null=True, blank=True,
                                       default="будние")

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
        verbose_name = "Получатель уведомлений"
        verbose_name_plural = "Получатели уведомлений"

    def __str__(self):
        return f"{self.name}"



