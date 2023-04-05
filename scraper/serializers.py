from rest_framework import serializers
from .models import Page, Link

class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ('url', 'name')

class PageSerializer(serializers.ModelSerializer):
    links = LinkSerializer(many=True, read_only=True)

    class Meta:
        model = Page
        fields = ('url', 'title', 'num_links', 'is_processing', 'links')
