# Generated by Django 4.0.3 on 2022-03-05 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operation_name', models.CharField(max_length=100)),
                ('number_of_arguments', models.IntegerField(default=1)),
                ('argument_type', models.CharField(choices=[('number', 'number'), ('text', 'text')], default='number', max_length=10)),
                ('example_text', models.TextField(blank=True, null=True)),
                ('operation_code', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
