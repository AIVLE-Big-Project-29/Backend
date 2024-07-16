from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import FileUploadSerializer
import pandas as pd
import pickle
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
import os

class FileUploadView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            dataframe = process_file(file)
            result = run_all_models(dataframe)
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def process_file(file):
    df = pd.read_excel(file)
    return df

def load_model_and_scaler(model_name, scaler_name):
    model_path = os.path.join(settings.MODEL_PATH, model_name)
    scaler_path = os.path.join(settings.MODEL_PATH, scaler_name)
    try:
        with open(model_path, 'rb') as model_file, open(scaler_path, 'rb') as scaler_file:
            model = pickle.load(model_file)
            scaler = pickle.load(scaler_file)
        return model, scaler
    except Exception as e:
        print(f"Failed to load model and scaler: {e}")
        return None, None
    
def run_model(model, scaler, dataframe):
    scaled_data = scaler.transform(dataframe)
    predictions = model.predict(scaled_data)
    return predictions

def run_all_models(dataframe):
    models_info = [
        {"name": "도시숲 적합성", "model_name": "compatibility_model.pkl", "scaler_name": "compatibility_scaler.pkl"},
        {"name": "도시숲 필요성", "model_name": "necessity_model.pkl", "scaler_name": "necessity_scaler.pkl"},
        # {"name": "생활숲", "model_name": "living_forest_model.pkl", "scaler_name": "living_forest_scaler.pkl"},
        # {"name": "생태숲", "model_name": "ecological_forest_model.pkl", "scaler_name": "ecological_forest_scaler.pkl"},
        # {"name": "환경숲", "model_name": "environmental_forest_model.pkl", "scaler_name": "environmental_forest_scaler.pkl"},
    ]
    
    results = {}
    for info in models_info:
        model, scaler = load_model_and_scaler(info["model_name"], info["scaler_name"])
        predictions = run_model(model, scaler, dataframe)
        results[info["name"]] = predictions.tolist()
    
    return results
