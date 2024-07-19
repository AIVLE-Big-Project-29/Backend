from rest_framework import serializers

class ImageUploadSerializer(serializers.Serializer):
    init_image = serializers.ImageField()
    image_strength = serializers.FloatField(default=0.45)
    text_prompts = serializers.CharField(default="Detailed, highly photorealistic,\
                                         and sharply focused scene of a lush, vibrant urban forest landscape.\
                                         Replace all buildings, roads, and infrastructure with a diverse array of tall trees,\
                                         dense foliage, winding gravel paths, natural boulders, and flowing streams.\
                                         Showcase the seamless integration of nature and the built environment in a clear,\
                                         crisp, and lifelike manner.")
    cfg_scale = serializers.IntegerField(default=7)
    samples = serializers.IntegerField(default=1)
    steps = serializers.IntegerField(default=30)
    style_preset = serializers.CharField(default="photographic")