from rest_framework import serializers

from .models import User, Relationship


class FollowerSerializer(serializers.ModelSerializer):
    from_user = serializers.StringRelatedField()

    class Meta:
        model = Relationship
        fields = [
            'from_user_id', 'from_user',
            'is_agree', 'is_deleted'
        ]


class FollowingSerializer(serializers.ModelSerializer):
    to_user = serializers.StringRelatedField()

    class Meta:
        model = Relationship
        fields = [
            'to_user_id', 'to_user',
            'is_agree',
        ]


class UserSerializer(serializers.ModelSerializer):
    follower = FollowerSerializer(many=True, read_only=True)
    following = FollowingSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username', 'first_name', 'last_name',
            'email', 'is_public', 'introduction',
            'password', 'follower', 'following',
        ]
        # write_only_fields = ['password']
        read_only_field = ['id']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def set_password(self, user, validated_data):
        if 'password' in validated_data:
            user.set_password(validated_data['password'])
            user.save()

    def create(self, validated_data):
        user = super().create(validated_data)
        self.set_password(user, validated_data)

        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        self.set_password(user, validated_data)

        return user


class RelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relationship
        fields = '__all__'

    def validate(self, data):
        if data['from_user'] == data['to_user']:
            raise serializers.ValidationError('不可以追蹤自己')

        return data
