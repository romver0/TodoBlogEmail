from rest_framework import serializers

from TodoWoo.settings import ALLOWED_HOSTS
from .models import Blog


class BlogSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = '__all__'

    def get_url(self, obj):
        schema = f'{ALLOWED_HOSTS[0]}:8000'  #
        endpoint = 'blog'  #
        id = obj.pk  #
        return f'{schema}/{endpoint}/{id}'
