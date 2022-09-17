from django.contrib import admin
from .models import Lesson, Schedule, PermanentBooking, Booking


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'date_begin', 'date_end')


class BookingAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'lesson', 'date', 'status')
    list_display_links = ('student_name', 'lesson')
    empty_value_display = '-empty-'

    def student_name(self, obj):
        return obj.student.get_full_name()


admin.site.register(Lesson)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(PermanentBooking)
