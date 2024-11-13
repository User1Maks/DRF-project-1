# Generated by Django 5.1.3 on 2024-11-12 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_payments_paid_lesson'),
    ]

    operations = [
        migrations.AddField(
            model_name='payments',
            name='link',
            field=models.URLField(blank=True, max_length=400, null=True, verbose_name='Ссылка на оплату'),
        ),
        migrations.AddField(
            model_name='payments',
            name='session_id',
            field=models.CharField(blank=True, help_text='Id сессии для оплаты через платежную систему', max_length=255, null=True, verbose_name='Id сессии'),
        ),
    ]