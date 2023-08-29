from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('redirect/<str:short_code>/',views.redirect_to_original,name='redirect_to_original'),
    path('delete/<str:short_cod>',views.deleteLink,name='deleteLink'),
    path('features/',views.feature,name="feature")
]
