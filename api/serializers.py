from rest_framework import serializers
from .models import User, Client, Automation, Workflow, GlobalSetting


class ObjectIdField(serializers.Field):
    """
    Custom field that serializes MongoDB ObjectId to a plain string
    and deserializes a string back to an ObjectId-compatible value.
    """
    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        return data


class ClientSerializer(serializers.ModelSerializer):
    # Expose id as both 'id' and '_id' as strings (for frontend compatibility)
    id = ObjectIdField(read_only=True)
    _id = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = '__all__'

    def get__id(self, obj):
        return str(obj.id)


class UserSerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)
    client = ObjectIdField(read_only=True)
    name = serializers.CharField(source='first_name', required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'name', 'first_name', 'role', 'status', 'client')
        extra_kwargs = {'password': {'write_only': True}}


class AutomationSerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)
    client = ObjectIdField(read_only=True)

    class Meta:
        model = Automation
        fields = '__all__'
        read_only_fields = ('client',)


class WorkflowSerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)
    client = ObjectIdField(read_only=True)

    class Meta:
        model = Workflow
        fields = '__all__'
        read_only_fields = ('client',)


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    name = serializers.CharField()
    businessName = serializers.CharField(required=False)

    def validate_email(self, value):
        email = value.lower().strip()
        if User.objects.filter(email=email).exists() or User.objects.filter(username=email).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return email

    def create(self, validated_data):
        email = validated_data['email'].lower().strip()
        business_name = validated_data.get('businessName', f"{validated_data['name']}'s Business")

        client = Client.objects.create(business_name=business_name)

        user = User.objects.create_user(
            username=email,
            email=email,
            password=validated_data['password'],
            first_name=validated_data['name'],
            role='CLIENT',
            status='PENDING',
            client=client
        )
        return user


class GlobalSettingSerializer(serializers.ModelSerializer):
    id = ObjectIdField(read_only=True)

    class Meta:
        model = GlobalSetting
        fields = '__all__'
