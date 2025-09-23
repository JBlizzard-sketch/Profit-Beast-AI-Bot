import pytest
from src.ml.rug_detector import generate_synthetic_dataset, train_and_save, predict

def test_synthetic_and_train():
    X,y = generate_synthetic_dataset(50)
    assert X.shape[0] == 50
    path = train_and_save(50)
    assert path.exists()
    p,prob = predict([0,0,0,0])
    assert isinstance(p, int)
    assert 0.0 <= prob <= 1.0
