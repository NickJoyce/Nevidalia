# Generated by Django 4.2.1 on 2023-05-31 09:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('promocode', '0003_ticketdaytype_ticketlimit_ticketpark_tickettype_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ticket',
            options={'verbose_name': 'Билет', 'verbose_name_plural': 'Билеты'},
        ),
    ]