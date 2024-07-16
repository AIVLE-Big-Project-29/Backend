from rest_framework import serializers

class ImageUploadSerializer(serializers.Serializer):
    init_image = serializers.ImageField()
    image_strength = serializers.FloatField(default=0.5)
    text_prompts = serializers.CharField(default="Default prompt")
    cfg_scale = serializers.IntegerField(default=7)
    samples = serializers.IntegerField(default=1)
    steps = serializers.IntegerField(default=30)
    style_preset = serializers.CharField(default="photographic")