import pandas as pd
import pickle
import os

# Define settings similar to Django settings
class settings:
    MODEL_PATH = 'C:/Users/User/Backend/AI/models/'

def load_model_and_scaler(model_name, scaler_name):
    model_path = os.path.join(settings.MODEL_PATH, model_name)
    scaler_path = os.path.join(settings.MODEL_PATH, scaler_name)
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file '{model_path}' does not exist.")
    if not os.path.exists(scaler_path):
        raise FileNotFoundError(f"Scaler file '{scaler_path}' does not exist.")
    
    try:
        with open(model_path, 'rb') as model_file, open(scaler_path, 'rb') as scaler_file:
            model = pickle.load(model_file)
            scaler = pickle.load(scaler_file)
    except Exception as e:
        raise RuntimeError(f"Failed to load model and scaler: {str(e)}")
    
    return model, scaler

    
def process_file(file_path):
    df = pd.read_excel(file_path)
    return df

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

# Main function to test the models locally
def main():
    # Path to the Excel file
    file_path = 'C:/Users/User/Backend/file.xlsx'
    
    # Process the Excel file
    dataframe = process_file(file_path)
    
    # Run all models
    results = run_all_models(dataframe)
    
    # Print the results
    for model_name, predictions in results.items():
        print(f"Model: {model_name}, Predictions: {predictions}")

if __name__ == '__main__':
    main()
