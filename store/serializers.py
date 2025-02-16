from rest_framework import serializers
from .models import Beat

class BeatSerializer(serializers.ModelSerializer):
    producer = serializers.ReadOnlyField(source='producer.username')
    class Meta:
        model = Beat
        fields = ('id', 'title', 'producer', 'audio_file', 'price', 'created_at', 'updated_at')



