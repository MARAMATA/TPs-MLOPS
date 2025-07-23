import hydra
from omegaconf import DictConfig
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

@hydra.main(config_path="../configs", config_name="config", version_base=None)
def main(cfg: DictConfig):
    print("Config utilisée :")
    print(cfg)
    
    # Exemple d'utilisation de la configuration
    print(f"Modèle: {cfg.model.name}")
    print(f"Nombre d'estimateurs: {cfg.model.n_estimators}")
    print(f"Ratio de split: {cfg.train.split_ratio}")

if __name__ == "__main__":
    main()
