"""ML pipeline orchestrator: version models, trigger retrains, evaluate and save artifacts.""" 
import os
from pathlib import Path
from logger_setup import get_logger
from . import rug_detector, whale_detector, sentiment_fusion
from joblib import dump
import json
import datetime

log = get_logger(__name__)
MODELS_DIR = Path(__file__).parent.parent.parent / 'models'
MODELS_DIR.mkdir(parents=True, exist_ok=True)
META_FILE = MODELS_DIR / 'models_meta.json'

def _load_meta():
    if META_FILE.exists():
        return json.loads(META_FILE.read_text())
    return {}

def _save_meta(meta):
    META_FILE.write_text(json.dumps(meta, indent=2))
    return META_FILE

def retrain_all(prefer='auto'):
    meta = _load_meta()
    ts = datetime.datetime.utcnow().isoformat()
    rug_path = rug_detector.train_and_save(1000, prefer=prefer)
    whale_path = whale_detector.train_and_save(1000, prefer=prefer)
    sentiment_fusion.save_dummy()
    meta['last_retrain'] = ts
    meta['rug_model'] = str(rug_path.name)
    meta['whale_model'] = str(whale_path.name)
    _save_meta(meta)
    log.info('Retrained all models and updated meta: %s', META_FILE)
    return meta

if __name__ == '__main__':
    print('Retraining models (pipeline)...')
    print(retrain_all())
