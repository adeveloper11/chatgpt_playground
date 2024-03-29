# Generated by Django 4.2.3 on 2023-08-22 09:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plyapp', '0009_alter_feedbackdata_mobile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedbackdata',
            name='Mobile',
            field=models.CharField(max_length=13, validators=[django.core.validators.RegexValidator(message='Mobile number must be 10 to 13 digits.', regex='^\\d{10,13}$')]),
        ),
    ]
