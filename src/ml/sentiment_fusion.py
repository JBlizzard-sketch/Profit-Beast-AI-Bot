"""Simple sentiment fusion across sources."""
import numpy as np
from joblib import dump, load
from pathlib import Path
from ..logger_setup import get_logger
MODEL_PATH = Path(__file__).parent.parent.parent / 'models' / 'sentiment_dummy.joblib'
MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
log = get_logger(__name__)

def compute_sentiment_scores(twitter_score, reddit_score, news_score):
    # naive weighted average
    weights = np.array([0.5, 0.3, 0.2])
    vals = np.array([twitter_score, reddit_score, news_score])
    fused = float((weights * vals).sum())
    return {'fused_score': fused, 'breakdown': {'twitter':twitter_score, 'reddit':reddit_score, 'news':news_score}}

def save_dummy():
    dump({'meta':'dummy'}, MODEL_PATH)
    return MODEL_PATH

if __name__ == '__main__':
    save_dummy()
    print(compute_sentiment_scores(0.1, -0.2, 0.05))
