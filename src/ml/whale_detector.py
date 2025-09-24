"""Whale detector: uses XGBoost classifier when available to predict anomaly (whale activity).
Fallback to IsolationForest if XGBoost not available or preferred.
"""
import os
import numpy as np
from pathlib import Path
from joblib import dump, load
from logger_setup import get_logger

log = get_logger(__name__)
MODEL_PATH = Path(__file__).parent.parent.parent / 'models' / 'whale_model.joblib'
MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)

def generate_synthetic_whale_data(n=1000):
    rng = np.random.RandomState(1)
    X = rng.normal(size=(n,3))
    # label ~1 for anomalies when tx_size high or holder_balance_change large negative
    y = ((X[:,0] > 1.5) | (X[:,2] < -1.5)).astype(int)
    return X, y

def _train_xgboost(X,y):
    try:
        from xgboost import XGBClassifier
    except Exception as e:
        raise RuntimeError('xgboost not available') from e
    clf = XGBClassifier(use_label_encoder=False, eval_metric='logloss', verbosity=0, n_estimators=200)
    clf.fit(X,y)
    return clf

def _train_isolation_forest(X,y):
    from sklearn.ensemble import IsolationForest
    clf = IsolationForest(random_state=0, n_estimators=100, contamination=0.05)
    clf.fit(X)
    return clf

def train_and_save(n=1000, prefer='auto'):
    X,y = generate_synthetic_whale_data(n)
    prefer_env = os.getenv('PREFER_WHALE_MODEL','auto').lower()
    if prefer_env != 'auto':
        prefer = prefer_env
    clf = None
    if prefer in ('xgboost','auto'):
        try:
            clf = _train_xgboost(X,y)
            log.info('Trained whale detector using XGBoost')
        except Exception as e:
            log.warning('XGBoost for whale failed, falling back: %s', e)
    if clf is None:
        clf = _train_isolation_forest(X,y)
        log.info('Trained whale detector using IsolationForest')
    dump(clf, MODEL_PATH)
    log.info('Saved whale detector model to %s', MODEL_PATH)
    return MODEL_PATH

def load_model():
    if MODEL_PATH.exists():
        return load(MODEL_PATH)
    raise RuntimeError('Model not found. Call train_and_save() first.')

def predict(features):
    clf = load_model()
    arr = np.array(features).reshape(1,-1)
    if hasattr(clf, 'predict'):
        pred = clf.predict(arr)[0]
        return int(pred), None
    else:
        # isolation forest: -1 anomaly
        score = float(clf.decision_function(arr)[0])
        is_anom = int(clf.predict(arr)[0] == -1)
        return is_anom, score

if __name__ == '__main__':
    train_and_save(500)
    print('Whale self-test:', predict([2.0,0.1,-2.0]))
