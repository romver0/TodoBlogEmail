from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Todo


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = (
            'title',
            'description',
            'created',
            'datecompleted',
            'is_important',
            'done',
            'user',
        )


class UserSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    def get_id(self,obj):
        return obj.pk
