from django.urls import path
from . import views

urlpatterns = [
    path('', views.lobby, name='lobby'),
    path('start/', views.start, name="start_session"),
    path('session/<str:id>', views.session, name="session"),
    path('search/', views.search, name="search"),
    path('add_thread/', views.add_thread, name="add_thread"),
    path('thread/<int:id>', views.thread, name="thread"),
]
