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
    code = models.CharField(max_length=255, verbose_name="Код", unique=True)
    status = models.BooleanField(verbose_name="Статус", default=False)
    date_of_use = models.DateField(verbose_name="Дата использования", null=True, blank=True, default=None)

    class Meta:
        verbose_name = "Промокод"
        verbose_name_plural = "Промокоды"

    def __str__(self):
        return f"{self.code}"


class TicketType(models.Model):
    type = models.CharField(max_length=255, verbose_name="Тип билета", unique=True)

    class Meta:
        verbose_name = "Тип билета"
        verbose_name_plural = "Типы билета"

class TicketLimit(models.Model):
    name = models.CharField(max_length=255, verbose_name="Лимит", unique=True)

    class Meta:
        verbose_name = "Лимит"
        verbose_name_plural = "Лимиты"

class TicketDayType(models.Model):
    name = models.CharField(max_length=255, verbose_name="Тип дней недели", unique=True)

    class Meta:
        verbose_name = "Тип дней недели"
        verbose_name_plural = "Типы дней недели"

class TicketPark(models.Model):
    name = models.CharField(max_length=255, verbose_name="Парк", unique=True)

    class Meta:
        verbose_name = "Парк"
        verbose_name_plural = "Парки"


class Ticket(models.Model):
    name = models.CharField(max_length=255, verbose_name="Произвольное наименование", null=True, blank=True,)
    tilda_external_product_id = models.CharField(max_length=255, verbose_name="Внешний код товара (Тильда)",
                                                 unique=True)
    park = models.ForeignKey(TicketPark, verbose_name="Парк", null=True, blank=True,
                             on_delete=models.SET_NULL,
                             related_name='ticket_park')
    type = models.ForeignKey(TicketType, verbose_name="Тип билета",  null=True, blank=True,
                             on_delete=models.SET_NULL,
                             related_name='ticket_type')
    limit = models.ForeignKey(TicketLimit, verbose_name="Лимит",  null=True, blank=True,
                              on_delete=models.SET_NULL,
                              related_name='ticket_limit')
    day_type = models.ForeignKey(TicketDayType, verbose_name="Тип дней недели",  null=True, blank=True,
                                 on_delete=models.SET_NULL,
                                 related_name='ticket_day_type')

    class Meta:
        verbose_name = "Билет"
        verbose_name_plural = "Билеты"




