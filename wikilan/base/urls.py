from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # path('route', views.view_function, name='name'),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('profile/', views.profile, name='profile'),
    path('resources/', views.resources, name='book'),
    path('signup', views.signup, name='signup'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('add_book', views.add_book, name='add_book'),
    path('show_book/<int:id>', views.show_book, name='show_book'),
    path('download_book/<int:id>', views.download_book, name='download_book'),
    path('create_profile/', views.create_profile, name='create_profile'),
]
# ]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)