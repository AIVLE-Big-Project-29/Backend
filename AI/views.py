from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import FileUploadSerializer
import pandas as pd
import numpy as np
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings
import os
import joblib

class FileUploadView(APIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            dataframe = process_file(file)
            model_results = run_all_models(dataframe)
            existing_results = load_existing_results()
             # actual 값에 따라 데이터프레임 분리
            existing_actual_0 = existing_results[existing_results['actual'] == 0]
            existing_actual_1 = existing_results[existing_results['actual'] == 1]
            return Response({
                "model_results": model_results,
                "existing_results_actual_0": existing_actual_0.to_dict(orient='records'),
                "existing_results_actual_1": existing_actual_1.to_dict(orient='records')
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
def process_file(file):
    if file.endswith('.csv'):
        df = pd.read_csv(file)
    elif file.endswith('.xlsx') or file.endswith('.xls'):
        df = pd.read_excel(file)
    else:
        raise ValueError("지원하지 않는 파일 형식입니다. CSV 또는 엑셀 파일을 제공하세요.")
    return df

def load_existing_results():
    # 서버에 저장된 기존 CSV 파일의 경로
    existing_path = os.path.join(settings.BASE_DIR, 'result.csv')
    existing_df = pd.read_csv(existing_path)
    return existing_df

def load_model_and_scaler(model_name, scaler_name):
    model_path = os.path.join(settings.MODEL_PATH, model_name)
    scaler_path = os.path.join(settings.MODEL_PATH, scaler_name)
    try:
        with open(model_path, 'rb') as model_file, open(scaler_path, 'rb') as scaler_file:
            model = joblib.load(model_file)
            scaler = joblib.load(scaler_file)
            
        return model, scaler
    except Exception as e:
        print(f"Failed to load model and scaler: {e}")
        return None, None
    
def run_model(model, scaler, dataframe, columns):
    df = dataframe.loc[:, columns]
    scaled_data = scaler.transform(df)
    predictions = []
    for test in scaled_data:
        predictions.append(np.array([tree.predict([test]) for tree in model.estimators_]))

    li_comp = []
    # 0과 1의 개수 세기
    for prediction in predictions:
        num_ones = np.sum(prediction == 1)
        li_comp.append(round(num_ones / len(model.estimators_) * 100, 2))
    # predictions = model.predict(scaled_data)
    return li_comp

def run_all_models(dataframe):
    compatibility_columns = [
        '면적', '전', '답', '과수원', '목장용지', '임야', '염전', '대', '공장용지', '학교용지',
        '주차장', '주유소용지', '창고용지', '도로', '철도용지', '하천', '제방', '구거', '유지',
        '양어장', '수도용지', '공원', '체육용지', '유원지', '종교용지', '사적지', '묘지', '잡종지',
        '광천지', '세대수', '인구수', '인구수_남', '인구수_여', '한국인', '한국인_남',
        '한국인_여', '외국인', '외국인_남', '외국인_여', '65세 이상 고령자'
    ]

    necessity_columns = [
        'BOD', 'COD', 'TOC', 'SS','DO',	'T-P', '총대장균군', '분원성대장균군', '암모니아성질소', '질산성질소',	
        '용존총질소', '인산염인', '용존총인', '클로로필A', 'pH분류', '수온분류', '전도분류', 'PM-2.5', 'PM-10',
        '오존', '일산화탄소', '일산화질소', '이산화황', '평균_기온', '최고_기온', '최저_기온', '강수총계', '평균 풍속', '최대 순간풍속'
    ]

    all_columns = list(dataframe.columns)
    all_columns.remove('동')
    locations = list(dataframe['동'])
    
    models_info = [
        {"name": "compatibility", "model_name": "compatibility_model.pkl", "scaler_name": "compatibility_scaler.pkl", "columns": compatibility_columns},
        {"name": "necessity", "model_name": "necessity_model.pkl", "scaler_name": "necessity_scaler.pkl", "columns": necessity_columns},
        {"name": "life", "model_name": "life_model.pkl", "scaler_name": "life_scaler.pkl", "columns": all_columns},
    #     {"name": "생태숲", "model_name": "eco_model.pkl", "scaler_name": "eco_scaler.pkl", "columns": all_columns},
        {"name": "env", "model_name": "env_model.pkl", "scaler_name": "env_scaler.pkl", "columns": all_columns},
    ]

    results = {}
    for info in models_info:
        model, scaler = load_model_and_scaler(info["model_name"], info["scaler_name"])
        predictions = run_model(model, scaler, dataframe, info['columns'])
        results["location"] = locations
        results[info["name"]] = predictions
        

    return results

