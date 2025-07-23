import joblib
import numpy as np
from omegaconf import DictConfig

def load_model(model_path: str = "model.pkl"):
    """Charger un modèle sauvegardé"""
    return joblib.load(model_path)

def predict(model, features):
    """Faire une prédiction"""
    return model.predict(features)

def predict_uranium_proliferation(features):
    """Prédire la prolifération d'uranium du futur"""
    model = load_model()
    prediction = predict(model, features)
    return prediction
