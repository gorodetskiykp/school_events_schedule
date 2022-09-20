from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Booking, Schedule, Event, EventBooking
from datetime import date, timedelta
from django.utils import timezone
from django.conf import settings

@login_required
def cabinet(request):
    template = 'booking/cabinet.html'
    days_before = settings.ACCESS_BOOKING_DAYS_BEFORE_BEGIN_LESSONS
    schedule = Schedule.objects.filter(date_begin__lte=date.today() + timedelta(days=days_before), date_end__gt=date.today())
    booked = Booking.objects.filter(student=request.user).filter(date__gte=date.today()).all()
    bookings = {}
    for line in schedule:
        for booking in booked:
            if booking.lesson.lesson.id == line.lesson.id and booking.date == line.next_lesson_day:
                bookings[line.id] = booking.id
    context = {
        'schedule': schedule,
        'bookings': bookings,
    }
    return render(request, template, context)


@login_required
def events(request):
    template = 'booking/events.html'
    events = Event.objects.filter(datetime_begin__gt=timezone.now())
    booked = EventBooking.objects.filter(student=request.user).filter(event__in=events).values_list('event', flat=True)
    context = {
        'events': events,
        'booked': booked,
    }
    return render(request, template, context)


@login_required
def booking(request, lesson_id):
    lesson = get_object_or_404(Schedule, pk=lesson_id)
    Booking.objects.get_or_create(
        student=request.user,
        lesson=lesson,
        date=lesson.next_lesson_day,
    )
    template = 'booking/message.html'
    context = {
        'icon': 'bi-emoji-smile',
        'message': 'Вы успешно записались!',
        'lesson': lesson,
    }
    return render(request, template, context)


@login_required
def cancel_booking(request, booking_id):
    try:
        booking = Booking.objects.get(pk=booking_id)
    except:
        return redirect(reverse('booking:cabinet'))
    if booking.student == request.user:
        booking.delete()
    template = 'booking/message.html'
    context = {
        'icon': 'bi-emoji-smile-upside-down',
        'message': 'Вы успешно отписались!',
        'lesson': booking.lesson,
    }
    return render(request, template, context)


@login_required
def multi_booking(request, lesson_id):
    lesson = Schedule.objects.get(pk=lesson_id)
    booked = Booking.objects.filter(
        lesson=lesson_id,
        student=request.user,
        date__gte=date.today(),
    ).values_list('date', flat=True)
    if request.POST:
        post_booking = [
            date.fromisoformat(book_date) for book_date in request.POST.getlist('lesson_date')
        ]
        bookings = []
        for book_date in post_booking:
            bookings.append(
                Booking(
                    student=request.user,
                    lesson=lesson,
                    date=book_date,
                ),
            )
        Booking.objects.bulk_create(bookings, ignore_conflicts=True)
        Booking.objects.filter(
            lesson=lesson_id,
            student=request.user).exclude(
            date__in=post_booking,
        ).delete()


    template = 'booking/multi_booking.html'
    context = {
        'lesson': lesson,
        'booked': booked,
    }
    return render(request, template, context)
