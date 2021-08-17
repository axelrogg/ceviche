from cryptography.hazmat.primitives.asymmetric import ed448
from os import getenv


_REFRESH_TOKEN_PRIVATE_KEY_ENV_VAR = getenv("REFRESH_TOKEN_PRIVATE_KEY")


def load_private_key_from_env_var(private_key: str) -> ed448.Ed448PrivateKey:
    private_bytes = bytes(private_key, "utf8")
    return ed448.Ed448PrivateKey.from_private_bytes(private_bytes)


_PRIV_KEY = load_private_key_from_env_var(_REFRESH_TOKEN_PRIVATE_KEY_ENV_VAR)
