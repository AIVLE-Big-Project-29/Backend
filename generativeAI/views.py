from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
import base64
import os
import requests
from django.conf import settings
from .serializers import ImageUploadSerializer  # serializers.py에서 ImageUploadSerializer 임포트

# 테스트 용
from django.http import FileResponse
from io import BytesIO

class ImageGenerateView(APIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def post(self, request, *args, **kwargs):
        # Stability API 설정
        engine_id = "stable-diffusion-v1-6"
        api_host = os.getenv("API_HOST", "https://api.stability.ai")
        api_key = os.getenv("STABILITY_API_KEY", settings.STABILITY_API_KEY)

        if api_key is None:
            return Response({"error": "Missing Stability API key."}, status=400)

        # 직렬화기 사용하여 요청 데이터 검증
        serializer = ImageUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        init_image = serializer.validated_data["init_image"]

        # Stability API 호출
        try:
            response = requests.post(
                f"{api_host}/v1/generation/{engine_id}/image-to-image",
                headers={
                    "Accept": "application/json",
                    "Authorization": f"Bearer {api_key}".encode('latin-1', 'replace').decode('latin-1')
                },
                files={
                    "init_image": init_image.read()
                },
                data={
                    "image_strength": serializer.validated_data["image_strength"],
                    "init_image_mode": "IMAGE_STRENGTH",
                    "text_prompts[0][text]": serializer.validated_data["text_prompts"],
                    "cfg_scale": serializer.validated_data["cfg_scale"],
                    "samples": serializer.validated_data["samples"],
                    "steps": serializer.validated_data["steps"],
                    "style_preset": serializer.validated_data["style_preset"]
                }
            )
        except UnicodeEncodeError as e:
            return Response({"error": "Encoding error occurred.", "details": str(e)}, status=500)

        if response.status_code != 200:
            return Response({"error": "API request failed.", "details": response.text}, status=response.status_code)

        # API 응답 처리
        # data = response.json()
        # images = []
        # for i, image in enumerate(data["artifacts"]):
        #     img_data = base64.b64decode(image["base64"])
        #     file_path = f"./imgs/v1_img2img{i}.png"
        #     with open(file_path, "wb") as f:
        #         f.write(img_data)
        #     images.append(file_path)

        # return Response({"message": "Image processed successfully", "images": images}, status=200)

        # API 응답 처리 테스트용
        data = response.json()
        if not data["artifacts"]:
            return Response({"error": "No image generated."}, status=500)

        # 첫 번째 이미지를 파일로 반환
        image = data["artifacts"][0]
        img_data = base64.b64decode(image["base64"])
        img_io = BytesIO(img_data)
        img_io.seek(0)

        return FileResponse(img_io, as_attachment=True, filename="generated_image.png")