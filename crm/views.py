from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from crm.serializers import ClientsSerializer, ContratsSerializer, EventsSerializer
from crm.permissions import ClientsPermissions, ContratsPermissions, EventsPermissions
from rest_framework.exceptions import PermissionDenied

from authenticate.models import User
from .models import Clients, Contrats, Events


class CrudClientViewSet(ModelViewSet):
	serializer_class = ClientsSerializer
	permission_classes = (IsAuthenticated, ClientsPermissions)
	queryset = Clients.objects.all()
	filter_backends = (SearchFilter, DjangoFilterBackend, )
	search_fields = ['^firstname', '^lastname', '^companyname', '^email']
	filterset_fields = ['firstname', 'lastname']

	def get_queryset(self):
		user = User.objects.get(username=self.request.user)
		if user.role == "support":
			return self.queryset.filter(contrat__event__supportcontact=self.request.user).distinct()
		elif user.role == "vente":
			data = self.queryset.filter(salescontact=self.request.user) | self.queryset.filter(clientstatus=False)
			return data
		return self.queryset

	def partial_update(self, request, *args, **kwargs):
		instance = self.get_object()
		serializer = self.serializer_class(instance, data=request.data, partial=True)
		serializer.is_valid(raise_exception=True)
		# MAJ de salescontact
		serializer.validated_data['salescontact'] = self.request.user
		serializer.save()
		return Response(serializer.data)


class CrudContratViewSet(ModelViewSet):
	serializer_class = ContratsSerializer
	queryset = Contrats.objects.all()
	permission_classes = (IsAuthenticated, ContratsPermissions)
	filter_backends = (SearchFilter, DjangoFilterBackend,)
	search_fields = ['^client__firstname', '^client__lastname', '^client__email']
	filterset_fields = ['contratstatus']

	def get_queryset(self):
		user = User.objects.get(username=self.request.user)
		if user.role == "support":
			data = self.queryset.filter(client=self.kwargs['parent_lookup_contrat']).filter(
										event__supportcontact=user.id)
			if data is None:
				raise PermissionDenied("Accès à ce contrat non permis")
			return data
		elif user.role == "vente":
			data = self.queryset.filter(client=self.kwargs['parent_lookup_contrat']).filter(
			 							salescontact=user.id)
			if data is None:
				raise PermissionDenied("Accès à ce contrat non permis")
			return data
		return self.queryset

	def partial_update(self, request, *args, **kwargs):
		instance = self.get_object()
		serializer = self.serializer_class(instance, data=request.data, partial=True)
		serializer.is_valid(raise_exception=True)
		# MAJ de salescontact
		serializer.validated_data['salescontact'] = self.request.user
		serializer.save()
		return Response(serializer.data)

	def create(self, request, *args, **kwargs):
		instance_client = Clients.objects.get(id=self.kwargs['parent_lookup_contrat'])
		serializer = self.serializer_class(data=request.data, context={'request': request})
		serializer.is_valid(raise_exception=True)
		serializer.validated_data['salescontact'] = self.request.user
		serializer.validated_data['contratstatus'] = False
		serializer.save(client=instance_client)
		return Response(serializer.data)


class CrudEventViewSet(ModelViewSet):
	serializer_class = EventsSerializer
	queryset = Events.objects.all()
	permission_classes = (IsAuthenticated, EventsPermissions)
	filter_backends = (SearchFilter, DjangoFilterBackend,)
	search_fields = ['^contrat__client__firstname', '^contrat__client__lastname', ]
	filterset_fields = ['eventstatus']

	def get_queryset(self):
		user = User.objects.get(username=self.request.user)
		if user.role == "support":
			data = self.queryset.filter(client=self.kwargs['parent_lookup_contrat__event']).filter(
										contrat=self.kwargs['parent_lookup_event']).filter(
										supportcontact=user.id)
			if data is None:
				raise PermissionDenied("Accès à cet évènement non permis")
			return data
		elif user.role == "vente":
			data = self.queryset.filter(client=self.kwargs['parent_lookup_contrat__event']).filter(
										contrat=self.kwargs['parent_lookup_event']).filter(
										contrat__salescontact=user.id)
			if data is None:
				raise PermissionDenied("Accès à cet évènement non permis")
			return data
		return self.queryset

	def partial_update(self, request, *args, **kwargs):
		instance = self.get_object()
		serializer = self.serializer_class(instance, data=request.data, partial=True)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return Response(serializer.data)

	def create(self, request, *args, **kwargs):
		if Events.objects.filter(client=self.kwargs['parent_lookup_contrat__event']).filter(contrat=self.kwargs['parent_lookup_event']).exists():
			raise PermissionDenied("Un évènement existe déjà pour ce contrat")
		else:
			instance_contrat = Contrats.objects.get(client=self.kwargs['parent_lookup_contrat__event'], id=self.kwargs['parent_lookup_event'])
			if instance_contrat.contratstatus is False:
				raise PermissionDenied("Le contrat n'est pas signé")
		instance_client = Clients.objects.get(id=self.kwargs['parent_lookup_contrat__event'])
		serializer = self.serializer_class(data=request.data, context={'request': request})
		serializer.is_valid(raise_exception=True)
		serializer.validated_data['eventstatus'] = False
		serializer.save(client=instance_client, contrat=instance_contrat)
		return Response(serializer.data)
