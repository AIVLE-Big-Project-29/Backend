from rest_framework import serializers

class ImageUploadSerializer(serializers.Serializer):
    init_image = serializers.ImageField()
    image_strength = serializers.FloatField(default=0.5)
    text_prompts = serializers.CharField(default="Transform the urban area shown in the attached image into a lush urban forest.\
                                         Replace the buildings with a variety of trees, plants, and greenery. Include walking paths,\
                                         benches, and open spaces for people to relax. Ensure the area is filled with diverse vegetation,\
                                         creating a natural and serene environment within the city.")
    cfg_scale = serializers.IntegerField(default=7)
    samples = serializers.IntegerField(default=1)
    steps = serializers.IntegerField(default=30)
    style_preset = serializers.CharField(default="photographic")