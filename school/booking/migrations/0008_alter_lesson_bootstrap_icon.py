# Generated by Django 4.1.1 on 2022-09-15 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0007_lesson_bootstrap_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='bootstrap_icon',
            field=models.CharField(default='bi-emoji-smile', max_length=50, verbose_name='Иконка'),
        ),
    ]