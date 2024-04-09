# Generated by Django 4.2.6 on 2024-04-09 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_customuser_is_user_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(max_length=50),
        ),
    ]
