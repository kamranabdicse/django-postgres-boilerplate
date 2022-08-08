import jwt
import datetime
import uuid
from django.conf import settings

def generate_jwt_token(username, id):
    token_lifetime = datetime.datetime.now() + datetime.timedelta(hours=3)

    token = jwt.encode(
        {
            "jti": uuid.uuid4().hex[:15].lower(),
            "user_id": id,
            "username": username,
            "exp": int(datetime.datetime.timestamp(token_lifetime)),
        },
        settings.JWT.get("SIGNING_KEY"),
        algorithm="HS256",
    )

    return token