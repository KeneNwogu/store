import secrets


def create_transaction_reference():
    return secrets.token_hex(16)
