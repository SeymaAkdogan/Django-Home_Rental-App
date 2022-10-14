from django.urls import path
from . import views

urlpatterns = [
    path("",views.index,name='index'),
    path("be-host",views.createHome,name='be-host'),
    path("home/<slug:slug>",views.homeDetails,name='home_details'),

]