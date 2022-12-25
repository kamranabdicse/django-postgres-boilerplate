import jwt
import datetime
import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser

from django.conf import settings

from config.lib.base_model import SafeTemplate


class UserORM(AbstractUser):
    can_use_basic_token = models.BooleanField(default=False)
    cell_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def _generate_jwt_token(self):
        token_lifetime = datetime.datetime.now() + datetime.timedelta(hours=3)

        token = jwt.encode(
            {
                "jti": uuid.uuid4().hex[:15].lower(),
                "user_id": self.pk,
                "username": self.username,
                "exp": int(datetime.datetime.timestamp(token_lifetime)),
            },
            settings.JWT.get("SIGNING_KEY"),
            algorithm="HS256",
        )

        return token


class BookORM(SafeTemplate):
    title = models.CharField(max_length=150)
    author_name = models.CharField(max_length=50)
    price = models.PositiveIntegerField(default=0)


class OrderORM(SafeTemplate):
    book = models.ManyToManyField(BookORM, related_name="order_book")
    user = models.ForeignKey(UserORM, on_delete=models.CASCADE)
    total_price = models.PositiveIntegerField(default=0)
    status_choices = models.TextChoices(
        "status",
        "choose purchased",
    )
    status = models.CharField(
        max_length=20,
        choices=status_choices.choices,
        default=status_choices.choose.value,
    )
    choose_time = models.DateTimeField(null=True)
    purchased_time = models.DateTimeField(null=True)


class BlacklistedToken(models.Model):
    id = models.BigAutoField(primary_key=True, serialize=False)
    token = models.TextField()
    blacklisted_at = models.DateTimeField(auto_now_add=True)
