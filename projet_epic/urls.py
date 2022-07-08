from django.contrib import admin
from django.urls import path, include
from authenticate.views import login


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', login),
    path('', include('crm.urls')), 
]
