from passlib.hash import sha256_crypt


def encrypt_password(password):
    """Ecrypt raw passwords."""
    return sha256_crypt.hash(password, rounds=1000)


def check_password(password, password_hash):
    """Compare raw password with encrypted password."""
    return sha256_crypt.verify(password, password_hash)
