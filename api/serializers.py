from rest_framework import serializers


class ServiceInfoPointSerializer(serializers.Serializer):
    text = serializers.CharField()


class ServiceInfoSerializer(serializers.Serializer):
    description = serializers.CharField()
    type = serializers.CharField()
    category = serializers.CharField(required=False, allow_null=True)
    points = ServiceInfoPointSerializer(many=True, required=False)


class ServiceURLSerializer(serializers.Serializer):
    url_type = serializers.CharField()
    url = serializers.URLField()


class ServiceSerializer(serializers.Serializer):
    name = serializers.CharField()
    website = serializers.URLField(required=False, allow_null=True)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, required=False)
    slug = serializers.SlugField()
    image = serializers.URLField(required=False, allow_null=True)
    icon_class = serializers.CharField(required=False, allow_null=True)
    service_urls = ServiceURLSerializer(many=True, required=False)
    service_infos = ServiceInfoSerializer(many=True, required=False)
