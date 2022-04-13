from rest_framework import serializers

from .models import Domain

class DomainSerializer(serializers.HyperlinkedModelSerializer):
    subdomains = serializers.StringRelatedField(many=True)
    class Meta:
        model = Domain
        fields = ("name", "subdomains")