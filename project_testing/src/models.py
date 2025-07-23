from sklearn.ensemble import RandomForestClassifier
from omegaconf import DictConfig

def create_model(config: DictConfig):
    """Créer un modèle basé sur la configuration"""
    if config.model.name == "RandomForest":
        return RandomForestClassifier(
            n_estimators=config.model.n_estimators,
            max_depth=config.model.max_depth,
            random_state=config.train.random_seed
        )
    else:
        raise ValueError(f"Modèle non supporté: {config.model.name}")
