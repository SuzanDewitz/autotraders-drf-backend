from django.db import IntegrityError
from rest_framework import serializers
from .models import Follower


class FollowerSerializer(serializers.ModelSerializer):
    """ Follower Serializer """

    owner = serializers.ReadOnlyField(source='owner.user')
    followed_name = serializers.ReadOnlyField(source='followed.user')

    class Meta:
        model = Follower
        fields = '__all__'

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                 'detail: possible duplicate'
            })