from django.urls import path
from . import views

urlpatterns = [
    path("reservations",views.cart,name='reservations'),
    path("add-reservation/<int:id>",views.add_to_cart,name='add_reservation'),
    path("edit-reservation/<int:id>",views.editCart,name='edit_reservation'),
    path("remove-reservation/<int:id>",views.remove_from_cart,name='remove_reservation')
]