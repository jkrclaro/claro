# Generated by Django 3.0.1 on 2020-01-31 17:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pxdcast', '0010_auto_20200131_1739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='podcast',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='episodes', to='pxdcast.Podcast'),
        ),
    ]
