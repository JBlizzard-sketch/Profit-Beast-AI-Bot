"""Payments: sandbox stubs for Stripe, M-Pesa, Binance Pay, and Telegram TON wallet.
Real implementations require API keys and webhook endpoints."""
from logger_setup import get_logger
from config import ENV_MODE
log = get_logger(__name__)

class PaymentStub:
    def __init__(self, provider='stripe'):
        self.provider = provider

    def create_payment_intent(self, amount_cents, currency='USD', metadata=None):
        log.info("Sandbox payment intent created: %s %s %s", amount_cents, currency, metadata)
        return {'id': 'pi_mock_123', 'amount': amount_cents, 'currency': currency, 'status': 'requires_payment_method'}

    def verify_webhook(self, payload, signature):
        log.info("Sandbox webhook verify for provider %s", self.provider)
        return True

if __name__ == "__main__":
    p = PaymentStub()
    print(p.create_payment_intent(999))
