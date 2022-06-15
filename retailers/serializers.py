from users.models import User
from users.serializers import RegistrationSerializer


class RetailerRegistrationSerializer(RegistrationSerializer):
    def create(self, validated_data):
        validated_data.pop('password2')
        validated_data['is_staff'] = True
        user = User.objects.create(**validated_data)
        user.set_password(validated_data.get('password'))
        user.save()

        return user
