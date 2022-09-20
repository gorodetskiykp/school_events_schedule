# Generated by Django 4.1.1 on 2022-09-19 23:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('booking', '0015_event'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Запись на мероприятие',
                'verbose_name_plural': 'Записи на мероприятия',
                'ordering': ('event', 'student'),
            },
        ),
        migrations.AddConstraint(
            model_name='event',
            constraint=models.CheckConstraint(check=models.Q(('datetime_begin__lt', models.F('datetime_end'))), name='check_events_dates'),
        ),
        migrations.AddConstraint(
            model_name='event',
            constraint=models.CheckConstraint(check=models.Q(('deadline_booking__lt', models.F('datetime_begin'))), name='check_events_deadlines'),
        ),
        migrations.AddField(
            model_name='eventbooking',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_bookings', to='booking.event', verbose_name='Мероприятие'),
        ),
        migrations.AddField(
            model_name='eventbooking',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_bookings', to=settings.AUTH_USER_MODEL, verbose_name='Ученик'),
        ),
        migrations.AddConstraint(
            model_name='eventbooking',
            constraint=models.UniqueConstraint(fields=('student', 'event'), name='unique_student_event'),
        ),
    ]