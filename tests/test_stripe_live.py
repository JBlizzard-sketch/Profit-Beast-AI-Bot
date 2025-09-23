import os
import pytest
from unittest import mock
from src.payments import stripe_live
def test_stripe_init_no_key():
    # Ensure that missing key raises
    with pytest.raises(RuntimeError):
        stripe_live.init_stripe()
