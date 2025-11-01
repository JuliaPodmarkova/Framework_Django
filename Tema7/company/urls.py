from django.urls import path
from .views import PositionCreateView

urlpatterns = [

    path('positions/add/', PositionCreateView.as_view(), name="position_create"),

]