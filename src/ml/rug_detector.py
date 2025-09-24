"""Rug detector: prefers XGBoost (XGBClassifier) when available, otherwise falls back to RandomForest.
Includes training pipeline, model saving, and inference. Uses env var to force algorithm choice if needed.
"""
import os
import numpy as np
from pathlib import Path
from joblib import dump, load
from logger_setup import get_logger

log = get_logger(__name__)
MODEL_PATH = Path(__file__).parent.parent.parent / 'models' / 'rug_model.joblib'
MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

def generate_synthetic_dataset(n=1000):
    rng = np.random.RandomState(42)
    X = rng.normal(size=(n,4))
    y = ((X[:,1] > 1.0) | (X[:,2] < -1.0)).astype(int)
    return X, y

def _train_xgboost(X,y):
    try:
        from xgboost import XGBClassifier
    except Exception as e:
        raise RuntimeError('xgboost not available') from e
    clf = XGBClassifier(use_label_encoder=False, eval_metric='logloss', verbosity=0, n_estimators=200)
    clf.fit(X,y)
    return clf

def _train_random_forest(X,y):
    from sklearn.ensemble import RandomForestClassifier
    clf = RandomForestClassifier(n_estimators=100, random_state=0)
    clf.fit(X,y)
    return clf

def train_and_save(n=1000, prefer='auto'):
    X,y = generate_synthetic_dataset(n)
    prefer_env = os.getenv('PREFER_MODEL','auto').lower()
    if prefer_env != 'auto':
        prefer = prefer_env
    clf = None
    if prefer in ('xgboost','auto'):
        try:
            clf = _train_xgboost(X,y)
            log.info('Trained rug detector using XGBoost')
        except Exception as e:
            log.warning('XGBoost train failed or not available, falling back: %s', e)
    if clf is None:
        clf = _train_random_forest(X,y)
        log.info('Trained rug detector using RandomForest')
    dump(clf, MODEL_PATH)
    log.info('Saved rug detector model to %s', MODEL_PATH)
    return MODEL_PATH

def load_model():
    if MODEL_PATH.exists():
        return load(MODEL_PATH)
    raise RuntimeError('Model not found. Call train_and_save() first.')

def predict(features):
    clf = load_model()
    arr = np.array(features).reshape(1,-1)
    pred = int(clf.predict(arr)[0])
    prob = None
    # try predict_proba if available
    if hasattr(clf, 'predict_proba'):
        prob = float(clf.predict_proba(arr)[0].max())
    else:
        # try margin/score
        try:
            prob = float(clf.predict(arr)[0])
        except Exception:
            prob = 0.5
    return pred, prob

if __name__ == '__main__':
    train_and_save(500)
    print('Self-test prediction:', predict([0.1, 1.2, -1.5, 10]))
