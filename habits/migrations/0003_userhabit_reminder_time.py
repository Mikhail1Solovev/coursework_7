# Generated by Django 5.1.2 on 2024-10-13 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userhabit',
            name='reminder_time',
            field=models.PositiveIntegerField(default=60, help_text='Через сколько минут отправить напоминание о привычке'),
        ),
    ]
