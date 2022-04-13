from rest_framework import serializers

from .models import Domain

class DomainSerializer(serializers.HyperlinkedModelSerializer):
    subdomains = serializers.StringRelatedField(many=True)
    subdomains.field_name = "name"
    class Meta:
        model = Domain
        fields = ("name", "creation_date", "expiration_date", "name_servers", "registrant_name", "subdomains")