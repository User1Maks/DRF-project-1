# Generated by Django 5.1.3 on 2024-11-12 20:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0004_lesson_owner'),
        ('users', '0004_subscriptions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payments',
            name='paid_lesson',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='education.lesson', verbose_name='Оплаченный урок'),
        ),
    ]
