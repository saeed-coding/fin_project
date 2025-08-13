from django.contrib import admin
from django.urls import path
from fastinn_app.views import *
from users.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('fin/get_data/', get_data, name="get_data"),
    path('fin/data/<int:pk>/', get_single_entry, name='get-single-entry'),
    path('fin/register/', RegisterView.as_view(), name='RegisterView'),
    path("fin/login/", LoginView.as_view(), name="login"),
    path('fin/change-password/', ChangePasswordView.as_view(), name='change-password'),

]
