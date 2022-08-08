from django.contrib import admin
from django.urls import path, include
from crm.views import CrudClientViewSet, CrudContratViewSet, CrudEventViewSet
from rest_framework_extensions.routers import ExtendedDefaultRouter

from rest_framework import routers


router = ExtendedDefaultRouter()

router.register(r'client', CrudClientViewSet, basename='client').register(r'contrat', CrudContratViewSet, basename='contrat-list', 
                    parents_query_lookups=['contrat']).register(r'event', CrudEventViewSet, basename='event-list', 
                    parents_query_lookups=['contrat__event', 'event'] )

urlpatterns = [
    path('', include(router.urls)), 

]
