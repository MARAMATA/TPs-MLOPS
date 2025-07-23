import hydra
from omegaconf import DictConfig
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
from models import create_model

@hydra.main(config_path="../configs", config_name="config", version_base=None)
def train(cfg: DictConfig):
    # Charger les données
    data = load_iris()
    X, y = data.data, data.target
    
    # Split des données
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=1-cfg.train.split_ratio, 
        random_state=cfg.train.random_seed
    )
    
    # Créer et entraîner le modèle
    model = create_model(cfg)
    model.fit(X_train, y_train)
    
    # Évaluer le modèle
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.4f}")
    
    # Sauvegarder le modèle
    joblib.dump(model, "model.pkl")
    print("Modèle sauvegardé sous 'model.pkl'")

if __name__ == "__main__":
    train()
