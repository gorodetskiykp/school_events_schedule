from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Booking, Schedule, PermanentBooking
from datetime import date, timedelta
from django.conf import settings

@login_required
def cabinet(request):
    template = 'booking/cabinet.html'
    days_before = settings.ACCESS_BOOKING_DAYS_BEFORE_BEGIN_LESSONS
    schedule = Schedule.objects.filter(date_begin__lte=date.today() + timedelta(days=days_before), date_end__gt=date.today())
    booked = Booking.objects.filter(student=request.user).filter(date__gte=date.today()).all()
    permanent_booking = PermanentBooking.objects.filter(student=request.user)
    bookings = {}
    permanent_bookings = []
    for line in schedule:
        for booking in booked:
            if booking.lesson.lesson.id == line.lesson.id and booking.date == line.next_lesson_day:
                bookings[line.id] = booking.id
        try:
            permanent_booking.get(lesson=line)
            permanent_bookings.append(line.id)
        except:
            pass
    print(permanent_bookings)
    context = {
        'schedule': schedule,
        'bookings': bookings,
        'permanent_bookings': permanent_bookings,
    }
    return render(request, template, context)


@login_required
def booking(request, lesson_id):
    lesson = get_object_or_404(Schedule, pk=lesson_id)
    try:
        new_booking = Booking.objects.get(
            student=request.user,
            lesson=lesson,
            date=lesson.next_lesson_day,
        )
        new_booking.status = True
    except:
        new_booking = Booking(
            student=request.user,
            lesson=lesson,
            date=lesson.next_lesson_day,
        )
    new_booking.clean()
    new_booking.save()
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
        booking.status = False
        booking.save()
    template = 'booking/message.html'
    context = {
        'icon': 'bi-emoji-smile-upside-down',
        'message': 'Вы успешно отписались!',
        'lesson': booking.lesson,
    }
    return render(request, template, context)


@login_required
def multi_booking(request):
    template = 'booking/multi_booking.html'
    context = {}
    return render(request, template, context)


@login_required
def permanent_booking(request, lesson_id):
    lesson = get_object_or_404(Schedule, pk=lesson_id)
    new_booking = PermanentBooking(
        student=request.user,
        lesson=lesson,
    )
    try:
        new_booking.clean()
        new_booking.save()
    except:
        return redirect('booking:cabinet')
    template = 'booking/message.html'
    context = {
        'icon': 'bi-emoji-smile',
        'message': 'Вы успешно записались на эти занятия!',
        'lesson': lesson,
        'permanent': True,
    }
    return render(request, template, context)


@login_required
def cancel_permanent_booking(request, lesson_id):
    try:
        booking = PermanentBooking.objects.get(lesson=lesson_id, student=request.user)
    except:
        return redirect(reverse('booking:cabinet'))
    booking.delete()
    template = 'booking/message.html'
    context = {
        'icon': 'bi-emoji-smile-upside-down',
        'message': 'Вы успешно отписались от этих занятий!',
        'lesson': booking.lesson,
        'permanent': True,
    }
    return render(request, template, context)