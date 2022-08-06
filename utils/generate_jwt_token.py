import jwt
import datetime
import uuid
from django.conf import settings

def generate_jwt_token(pk, username):
    token_lifetime = datetime.datetime.now() + datetime.timedelta(hours=3)

    token = jwt.encode(
        {
            "jti": uuid.uuid4().hex[:15].lower(),
            "user_id": pk,
            "username": username,
            "exp": int(datetime.datetime.timestamp(token_lifetime)),
        },
        settings.JWT.get("SIGNING_KEY"),
        algorithm="HS256",
    )

    return token