# Generated by Django 5.1 on 2024-09-17 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_exhibit_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyinfo',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='company_videos/'),
        ),
    ]