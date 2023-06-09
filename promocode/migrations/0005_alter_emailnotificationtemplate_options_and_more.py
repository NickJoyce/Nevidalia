# Generated by Django 4.2.1 on 2023-06-08 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promocode', '0004_emailnotificationtemplate_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='emailnotificationtemplate',
            options={'verbose_name': 'Шаблон email уведомления', 'verbose_name_plural': 'Шаблоны email уведомлений'},
        ),
        migrations.AlterModelOptions(
            name='notificationrecipients',
            options={'verbose_name': 'Получатель служебных уведомлений', 'verbose_name_plural': 'Получатели служебных уведомлений'},
        ),
        migrations.AddField(
            model_name='promocode',
            name='customer_email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Телефон'),
        ),
        migrations.AddField(
            model_name='promocode',
            name='customer_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Имя'),
        ),
        migrations.AddField(
            model_name='promocode',
            name='customer_phone',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Телефон'),
        ),
        migrations.AddField(
            model_name='promocode',
            name='sending_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата отправки уведомления'),
        ),
    ]