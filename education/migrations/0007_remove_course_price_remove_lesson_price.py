# Generated by Django 5.1.3 on 2024-11-13 15:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0006_alter_course_price_alter_lesson_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='price',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='price',
        ),
    ]
