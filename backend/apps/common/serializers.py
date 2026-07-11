from rest_framework import serializers


class ReadOnlyIdSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

