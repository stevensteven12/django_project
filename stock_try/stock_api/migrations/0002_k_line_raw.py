# Generated by Django 2.0 on 2017-12-29 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='K_Line_Raw',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('StockNO', models.CharField(max_length=20)),
                ('published_date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]