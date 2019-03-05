from django.contrib import admin
from django.urls import path

from notifier.views import HomeView, SingleView

urlpatterns = [
    path('single/', SingleView.as_view()),
#    path('', HomeView.as_view()),
    path('admin/', admin.site.urls),
]
