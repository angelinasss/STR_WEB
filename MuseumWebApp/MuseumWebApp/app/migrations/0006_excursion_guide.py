# Generated by Django 5.1 on 2024-09-02 03:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_employee_hall'),
    ]

    operations = [
        migrations.AddField(
            model_name='excursion',
            name='guide',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.employee'),
        ),
    ]
