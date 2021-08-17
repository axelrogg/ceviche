from base64 import b64encode, b64decode
from datetime import datetime
from json import dumps as json_dumps
from typing import Optional
from uuid import uuid4

from passlib.hash import argon2
from pydantic import BaseModel, PrivateAttr
from pydantic.json import pydantic_encoder

from ceviche.tokens.key import _PRIV_KEY
from ceviche.types import UserID


class RefreshToken(BaseModel):
    token: str
    _created_at: datetime = PrivateAttr()

    class Config:
        allow_mutation = False


class RefreshTokenPayload(BaseModel):
    # TODO: session_ticket_id: SessionTicketID
    user_id: UserID
    parent_refresh_token_key_hash: Optional[str] = None
    nonce: str
    # TODO: anti_csrf_token: str

    class Config:
        allow_mutation = False


class RefreshTokenInfo(BaseModel):
    # TODO: session_ticket_id: SessionTicketID
    user_id: UserID
    parent_refresh_token_key_hash: Optional[str] = None
    nonce: str
    _created_at: datetime = PrivateAttr()
    # TODO: anti_csrf_token: str

    class Config:
        allow_mutation = False


class RefreshTokenGenerator:

    def __init__(
            self,
            # TODO: session_ticket_id: SessionTicketID,
            user_id: UserID,
            parent_refresh_token_key_hash: Optional[str] = None,
            # TODO: anti_csrf_token: AntiCSRFToken,
    ) -> None:
        self.user_id = user_id
        self.parent_refresh_token_key_hash = parent_refresh_token_key_hash
        self._created_at = None

    def b64token(self) -> bytes:
        rft = self.token()
        brft = bytes(rft.token, "utf8")
        return b64encode(brft)

    @staticmethod
    def b64token_decode(b64token: bytes) -> bytes:
        return b64decode(b64token)

    def info(self) -> RefreshTokenInfo:
        if self._created_at is None:
            raise ValueError("A new Refresh Token has not been created yet.")

        info_ = RefreshTokenInfo(
            # TODO: session_ticket_id=self.session_ticket_id,
            user_id=self.user_id,
            parent_refresh_token_key_hash=self.parent_refresh_token_key_hash,
            _created_at=self._created_at,
            # TODO: anti_csrf_token=self.anti_csrf_token,
        )
        return info_

    def token(self) -> RefreshToken:
        now = datetime.utcnow()
        self._created_at = now

        key_hash = self.__gen_key_hash().decode("utf8")
        nonce = self.__gen_nonce()
        payload = _PRIV_KEY.sign(self.__payload())
        r_token = key_hash + "." + nonce + "." + payload
        return RefreshToken(token=r_token, _created_at=now)

    def serialize_payload(self) -> str:
        payload = self.__payload()
        return json_dumps(payload, indent=2, default=pydantic_encoder)

    def __payload(self) -> RefreshTokenPayload:
        payload_ = RefreshTokenPayload(
            # TODO: session_ticket_id=self.session_ticket_id,
            user_id=self.user_id,
            parent_refresh_token_key_hash=self.parent_refresh_token_key_hash,
            nonce=self.__gen_nonce(),
            # TODO: anti_csrf_token=self.anti_csrf_token,
        )
        return payload_

    def __gen_key_hash(self) -> bytes:
        key = bytes(self.__gen_key(), "utf8")
        return _PRIV_KEY.sign(key)

    def __gen_key(self) -> str:
        rand_val = str(uuid4())
        key = rand_val + "." + self.user_id.value
        if self.parent_refresh_token_key_hash:
            key += "." + self.parent_refresh_token_key_hash
        return key

    @staticmethod
    def __gen_nonce() -> str:
        return generate_hashed_nonce()


def generate_hashed_nonce() -> str:
    nonce = str(uuid4())
    return argon2.hash(nonce)
