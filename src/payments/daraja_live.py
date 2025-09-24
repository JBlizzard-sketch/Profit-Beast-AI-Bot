"""Daraja (M-Pesa) integration scaffold. Requires MPESA_CONSUMER_KEY and MPESA_CONSUMER_SECRET.
This module provides token retrieval and STK push initiation placeholders.
""" 
import os, requests
from logger_setup import get_logger
log = get_logger(__name__)

BASE_URL = os.getenv('MPESA_BASE_URL','https://sandbox.safaricom.co.ke')

def get_token():
    key = os.getenv('MPESA_CONSUMER_KEY')
    secret = os.getenv('MPESA_CONSUMER_SECRET')
    if not key or not secret:
        raise RuntimeError('MPESA credentials not set')
    resp = requests.get(f'{BASE_URL}/oauth/v1/generate?grant_type=client_credentials', auth=(key, secret), timeout=10)
    resp.raise_for_status()
    return resp.json()

def stk_push(phone_number, amount, account_ref='AltTrade', description='Payment'):
    token = get_token().get('access_token')
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    payload = {
        'BusinessShortCode': os.getenv('MPESA_SHORTCODE','174379'),
        'Password': 'GENERATED_PASSWORD',
        'Timestamp': 'YYYYMMDDHHMMSS',
        'TransactionType': 'CustomerPayBillOnline',
        'Amount': amount,
        'PartyA': phone_number,
        'PartyB': os.getenv('MPESA_SHORTCODE','174379'),
        'PhoneNumber': phone_number,
        'CallBackURL': os.getenv('MPESA_CALLBACK_URL','https://example.com/mpesa/callback'),
        'AccountReference': account_ref,
        'TransactionDesc': description
    }
    resp = requests.post(f'{BASE_URL}/mpesa/stkpush/v1/processrequest', headers=headers, json=payload, timeout=10)
    resp.raise_for_status()
    return resp.json()
