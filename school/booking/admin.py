from django.contrib import admin
from .models import Lesson, Schedule, Booking, Event, EventBooking


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'date_begin', 'date_end')


class BookingAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'lesson', 'date')
    list_display_links = ('student_name', 'lesson')
    empty_value_display = '-empty-'

    def student_name(self, obj):
        return obj.student.get_full_name()


class EventBookingAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'event')
    list_display_links = ('student_name', 'event')
    empty_value_display = '-empty-'

    def student_name(self, obj):
        return obj.student.get_full_name()


admin.site.register(Lesson)
admin.site.register(Event)
admin.site.register(Booking, BookingAdmin)
admin.site.register(EventBooking, EventBookingAdmin)
admin.site.register(Schedule, ScheduleAdmin)
