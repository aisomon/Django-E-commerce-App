# Generated by Django 3.0.8 on 2021-01-08 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20210109_0002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(blank=True, upload_to='static/images/users/'),
        ),
    ]