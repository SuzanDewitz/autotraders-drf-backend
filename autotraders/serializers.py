from rest_framework import serializers
from .models import autotraders



class AutotraderSerializer(serializers.ModelSerializer):
    """ Autotrader Serializer """ 

    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    save_id = serializers.SerializerMethodField()

     def validate_image(self, value):
        if value.size > 4096 * 4096 * 2:
            raise serializers.ValidationError('Image size larger than 2mb')
        if value.image.width > 4096:
            raise serializers.ValidationError('Image width to large')
        if value.image.height > 4096:
            raise serializers.ValidationError('Image height to large')

        return value

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_save_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            save = Save.objects.filter(
                owner=user, car=obj
            ).first()
            return save.id if save else None
        return None

    class Meta:
        model = Car
        fields = '__all__'   