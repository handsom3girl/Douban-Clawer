# Generated by Django 2.0 on 2020-05-02 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('show', '0008_auto_20200428_2049'),
    ]

    operations = [
        migrations.AddField(
            model_name='doubansubject',
            name='district',
            field=models.CharField(default='', max_length=10),
        ),
    ]