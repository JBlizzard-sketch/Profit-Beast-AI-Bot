"""Stripe live provider integration. Requires STRIPE_API_KEY env var.
Provides create_payment_intent and webhook verification functions.
"""
import os
from logger_setup import get_logger
log = get_logger(__name__)

try:
    import stripe
except Exception:
    stripe = None

def init_stripe():
    key = os.getenv('STRIPE_API_KEY') or os.getenv('STRIPE_SECRET_KEY')
    if not key:
        raise RuntimeError('STRIPE_API_KEY not set in env')
    if not stripe:
        raise RuntimeError('stripe library not installed')
    stripe.api_key = key
    return stripe

def create_payment_intent(amount_cents, currency='usd', metadata=None):
    s = init_stripe()
    intent = s.PaymentIntent.create(amount=amount_cents, currency=currency, metadata=metadata or {})
    log.info('Created Stripe PaymentIntent %s', intent.id)
    return intent

def verify_webhook(payload, sig_header, endpoint_secret):
    s = init_stripe()
    try:
        event = s.Webhook.construct_event(payload, sig_header, endpoint_secret)
        return event
    except Exception as e:
        log.exception('Stripe webhook verification failed.')
        raise
