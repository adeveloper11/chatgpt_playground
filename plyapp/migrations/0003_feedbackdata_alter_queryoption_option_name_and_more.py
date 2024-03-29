# Generated by Django 4.2.3 on 2023-08-11 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plyapp', '0002_queryoption'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedbackdata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=50)),
                ('Mobile', models.IntegerField()),
                ('Email', models.EmailField(max_length=300)),
                ('Feedback', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='queryoption',
            name='option_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='queryoption',
            name='option_value',
            field=models.CharField(max_length=100),
        ),
    ]
