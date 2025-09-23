from src.ml import rug_detector, whale_detector, sentiment_fusion
def test_rug_training_and_predict():
    # Train (will use XGBoost if available; else RandomForest)
    p = rug_detector.train_and_save(200)
    assert p.exists()
    pred,prob = rug_detector.predict([0.1,1.2,-1.5,10])
    assert isinstance(pred, int)
def test_whale_training_and_predict():
    p = whale_detector.train_and_save(200)
    assert p.exists()
    pred,score = whale_detector.predict([2.0,0.1,-2.0])
    assert isinstance(pred, int)
def test_sentiment():
    s = sentiment_fusion.compute_sentiment_scores(0.3, -0.1, 0.05)
    assert 'fused_score' in s
