# Generated by Django 4.2.1 on 2023-05-31 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promocode', '0004_alter_ticket_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Произвольное наименование'),
        ),
    ]