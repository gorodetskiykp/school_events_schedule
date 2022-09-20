from datetime import date, datetime, timedelta, time

from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone

User = get_user_model()


def validate_schedule_week_days(value):
    if '1' not in value:
        raise ValidationError('Нет единиц в расписании на неделю')
    if value.count('0') + value.count('1') != len(value):
        raise ValidationError('В расписании на неделю есть символы кроме 0 и 1')
    if len(value) != 7:
        raise ValidationError('Длина расписания на неделю не равна 7')


class Lesson(models.Model):
    title = models.CharField('Название занятия', max_length=100, unique=True)
    description = models.TextField('Описание', null=True, blank=True)
    bootstrap_icon = models.CharField(
        'Иконка',
        max_length=50,
        default='bi-emoji-smile',
        help_text='https://icons.getbootstrap.com/icons/'
    )

    class Meta:
        ordering = ('title',)
        verbose_name = 'Занятие'
        verbose_name_plural = 'Занятия'

    def __str__(self):
        return self.title


class Event(Lesson):
    datetime_begin = models.DateTimeField('Время начала мероприятия')
    datetime_end = models.DateTimeField('Время завершения мероприятия')
    deadline_booking = models.DateTimeField('Время завершения бронирования')
    price = models.PositiveIntegerField('Стоимость')

    class Meta:
        ordering = ('-datetime_begin',)
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'
        constraints = [
            models.CheckConstraint(check=models.Q(datetime_begin__lt=models.F('datetime_end')), name='check_events_dates'),
            models.CheckConstraint(check=models.Q(deadline_booking__lt=models.F('datetime_begin')),
                                   name='check_events_deadlines'),
        ]

    def __str__(self):
        return self.title

    @property
    def is_deadline(self):
        return timezone.now() >= self.deadline_booking


class Schedule(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name='Занятие', on_delete=models.CASCADE, related_name='schedules')
    date_begin = models.DateField('Дата начала занятий')
    date_end = models.DateField('Дата завершения занятий')
    week_days = models.CharField('Дни проведения занятий', max_length=7, validators=[validate_schedule_week_days])

    class Meta:
        ordering = ('-date_begin', 'lesson')
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписания'
        constraints = [
            models.CheckConstraint(check=models.Q(date_begin__lt=models.F('date_end')), name='check_dates'),
        ]

    def __str__(self):
        return self.lesson.title

    def clean(self):
        if self.date_begin >= self.date_end:
            raise ValidationError('Дата начала занятий не может быть позже даты их завершения')

    @property
    def is_deadline(self):
        return datetime.now() >= self.deadline_time

    @property
    def next_lesson_day(self):
        if date.today() >= self.date_begin:
            evaluation_day = date.today()
        else:
            evaluation_day = self.date_begin

        weekday = evaluation_day.weekday()
        next_lesson_day = self.week_days.find('1', weekday + 1)
        next_lesson_delta = next_lesson_day - weekday
        if next_lesson_day == -1:
            next_lesson_day = self.week_days.find('1')
            next_lesson_delta = 7 - weekday + next_lesson_day
        next_lesson_date = evaluation_day + timedelta(days=next_lesson_delta)
        return next_lesson_date

    @property
    def is_next_lesson_tomorrow(self):
        return self.next_lesson_day - date.today() == timedelta(days=1)

    @property
    def deadline_time(self):
        day = self.next_lesson_day - timedelta(days=1)
        return datetime.combine(day, time(hour=settings.DEADLINE_TIME))

    @property
    def week_schedule(self):
        week_days = [
            'Понедельник',
            'Вторник',
            'Среда',
            'Четверг',
            'Пятница',
            'Суббота',
            'Воскресенье',
        ]
        return ', '.join([item[1].lower() for item in zip(self.week_days, week_days) if int(item[0])])

    @property
    def lesson_days(self):
        lessons = {}
        lesson_day = self.next_lesson_day
        if (self.next_lesson_day - date.today()).days == 1:
            if datetime.now().hour >= settings.DEADLINE_TIME:
                lesson_day += timedelta(days=1)
        week_schedule = [num for num, day in enumerate(self.week_days) if int(day)]
        while lesson_day < self.date_end:
            if lesson_day.weekday() in week_schedule:
                key = lesson_day.replace(year=lesson_day.year, day=1)
                if lessons.get(key):
                    lessons[key].append(lesson_day)
                else:
                    lessons[key] = [lesson_day]
            lesson_day += timedelta(days=1)
        return lessons


class Booking(models.Model):
    student = models.ForeignKey(User, verbose_name='Ученик', on_delete=models.CASCADE, related_name='bookings')
    lesson = models.ForeignKey(Schedule, verbose_name='Занятие', on_delete=models.CASCADE, related_name='bookings')
    date = models.DateField('День проведения занятия')

    class Meta:
        ordering = ('-date', 'lesson', 'student')
        verbose_name = 'Запись на занятие'
        verbose_name_plural = 'Записи на занятия'
        constraints = [
            models.UniqueConstraint(fields=('student', 'lesson', 'date'), name='unique_student_lesson_date'),
        ]

    def __str__(self):
        return '{0} {1} {2}'.format(self.date, self.lesson, self.student)


class EventBooking(models.Model):
    student = models.ForeignKey(User, verbose_name='Ученик', on_delete=models.CASCADE, related_name='event_bookings')
    event = models.ForeignKey(Event, verbose_name='Мероприятие', on_delete=models.CASCADE, related_name='event_bookings')

    class Meta:
        ordering = ('event', 'student')
        verbose_name = 'Запись на мероприятие'
        verbose_name_plural = 'Записи на мероприятия'
        constraints = [
            models.UniqueConstraint(fields=('student', 'event'), name='unique_student_event'),
        ]

    def __str__(self):
        return '{0} {1}'.format(self.event, self.student)
