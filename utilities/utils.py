import datetime
import secrets
import jwt


def create_transaction_reference():
    return secrets.token_hex(16)


def generate_unique_state_identifier():
    payload = {"exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24), "iat": datetime.datetime.utcnow()}

