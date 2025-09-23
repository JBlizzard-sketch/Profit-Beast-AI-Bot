from prometheus_client import Gauge, Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response

# Metrics
TRADE_COUNTER = Counter('alttrade_trades_total', 'Total trades executed', ['mode'])
ALERT_COUNTER = Counter('alttrade_alerts_total', 'Total ML alerts', ['type'])
MODEL_RETRAIN_COUNTER = Counter('alttrade_model_retrains_total', 'Model retrains', ['model'])
LATENCY_HIST = Histogram('alttrade_request_latency_seconds', 'Request latency')

def metrics_response():
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)
