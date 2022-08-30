from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.sign_up, name='sign_up'),
    path('signin', views.sign_in, name='sign_in'),
    path('logout', views.log_out, name='log_out'),
    path('setting', views.setting, name='setting'),
]
