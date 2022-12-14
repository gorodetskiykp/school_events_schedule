# Generated by Django 4.1.1 on 2022-09-13 22:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='Название занятия')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Занятие',
                'verbose_name_plural': 'Занятия',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_begin', models.DateField(verbose_name='Дата начала занятий')),
                ('date_end', models.DateField(verbose_name='Дата завершения занятий')),
                ('week_days', models.CharField(max_length=7, verbose_name='Дни проведения занятий')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to='booking.lesson', verbose_name='Занятие')),
            ],
            options={
                'verbose_name': 'Расписание',
                'verbose_name_plural': 'Расписания',
                'ordering': ('-date_begin', 'lesson'),
            },
        ),
        migrations.CreateModel(
            name='PermanentBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='permanent_bookings', to='booking.lesson', verbose_name='Занятие')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='permanent_bookings', to=settings.AUTH_USER_MODEL, verbose_name='Ученик')),
            ],
            options={
                'verbose_name': 'Постоянная запись на занятие',
                'verbose_name_plural': 'Постоянные записи на занятия',
                'ordering': ('lesson', 'student'),
            },
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='День проведения занятия')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='booking.lesson', verbose_name='Занятие')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to=settings.AUTH_USER_MODEL, verbose_name='Ученик')),
            ],
            options={
                'verbose_name': 'Запись на занятие',
                'verbose_name_plural': 'Записи на занятия',
                'ordering': ('-date', 'lesson', 'student'),
            },
        ),
    ]
