from rest_framework import serializers
from .models import Clients, Contrats, Events


class ClientsSerializer(serializers.ModelSerializer):

	class Meta:
		model = Clients
		fields = '__all__'

		extra_kwargs = {
			"datecreated": {'read_only': True},
			"dateupdated": {'read_only': True},
			"salescontact": {'read_only': True},
		}


class ContratsSerializer(serializers.ModelSerializer):
	client = ClientsSerializer(read_only=True)

	class Meta:
		model = Contrats
		fields = '__all__'

		extra_kwargs = {
			"client": {'read_only': True},
			"id": {'read_only': True},
			"datecreated": {'read_only': True},
			"dateupdated": {'read_only': True},
			"salescontact": {'read_only': True},
		}


class EventsSerializer(serializers.ModelSerializer):
	contrat = ContratsSerializer(read_only=True)

	class Meta:
		model = Events
		fields = '__all__'

		extra_kwargs = {
			"client": {'read_only': True},
			"contrat": {'read_only': True},
			"id": {'read_only': True},
			"datecreated": {'read_only': True},
			"dateupdated": {'read_only': True},
			"eventdate": {'read_only': True},
		}
