# Generated by Django 4.2.6 on 2024-04-09 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_customuser_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_user_active',
            field=models.BooleanField(default=False),
        ),
    ]
