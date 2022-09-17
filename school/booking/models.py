from datetime import date, datetime, timedelta, time

from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.exceptions import ValidationError

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
    bootstrap_icon = models.CharField('Иконка', max_length=50, default='bi-emoji-smile')

    class Meta:
        ordering = ('title',)
        verbose_name = 'Занятие'
        verbose_name_plural = 'Занятия'

    def __str__(self):
        return self.title


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


class Booking(models.Model):
    student = models.ForeignKey(User, verbose_name='Ученик', on_delete=models.CASCADE, related_name='bookings')
    lesson = models.ForeignKey(Schedule, verbose_name='Занятие', on_delete=models.CASCADE, related_name='bookings')
    date = models.DateField('День проведения занятия')
    status = models.BooleanField('Решение идти на занятие', default=True)

    class Meta:
        ordering = ('-date', 'lesson', 'student')
        verbose_name = 'Запись на занятие'
        verbose_name_plural = 'Записи на занятия'
        constraints = [
            models.UniqueConstraint(fields=('student', 'lesson', 'date'), name='unique_student_lesson_date'),
        ]

    def __str__(self):
        return '{0} {1} {2}'.format(self.date, self.lesson, self.student)


class PermanentBooking(models.Model):
    student = models.ForeignKey(User, verbose_name='Ученик', on_delete=models.CASCADE, related_name='permanent_bookings')
    lesson = models.ForeignKey(Schedule, verbose_name='Занятие', on_delete=models.CASCADE, related_name='permanent_bookings')

    class Meta:
        ordering = ('lesson', 'student')
        verbose_name = 'Постоянная запись на занятие'
        verbose_name_plural = 'Постоянные записи на занятия'
        constraints = [
            models.UniqueConstraint(fields=('student', 'lesson'), name='unique_student_lesson'),
        ]

    def __str__(self):
        return '{0} {1}'.format(self.lesson, self.student)