from django.urls import path
from . import views

app_name = 'booking'
urlpatterns = [
    path('', views.cabinet, name='cabinet'),
    path('booking_next_lesson/<int:lesson_id>', views.booking, name="booking_next_lesson"),
    path('permanent_booking/<int:lesson_id>', views.permanent_booking, name="permanent_booking"),
    path('cancel_booking_next_lesson/<int:booking_id>', views.cancel_booking, name="cancel_booking_next_lesson"),
    path('cancel_permanent_booking/<int:lesson_id>', views.cancel_permanent_booking, name="cancel_permanent_booking"),
    path('multi_booking', views.multi_booking, name="multi_booking"),
]
