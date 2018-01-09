from django.urls import path

from demo import views

urlpatterns = (
  path('upload/', views.upload, name='upload'),
)
