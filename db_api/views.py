import logging
import random

from django.http import JsonResponse, Http404
from rest_framework.schemas.openapi import AutoSchema
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, schema

from project_name.lib.sms import SMS
from project_name.lib.openapi import CustomSchema
from project_name.lib.logger import logger
from db_api.serializers import GenerateOTPSerializer, LoginSerializer
from db_api.models import UserORM


logger = logging.getLogger(__name__)


@api_view(["POST"])
@schema(
    CustomSchema(
        tags=["user otp"],
        operation_id_base="generate_otp",
        extra_info={
            "serializer": GenerateOTPSerializer(),
        },
    )
)
def generate_otp(request):
    """
    post:
      summary: send otp for mobile
      description: this method doesn't need to authorization
    """
    serializer = GenerateOTPSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    mobile = serializer.validated_data.get("mobile")
    user = UserORM.objects.filter(username=mobile).first()
    created = False

    if not user:
        user = UserORM.objects.create(username=mobile)
        print("----------> create user")
        created = True

    # rnd = random.SystemRandom()
    # otp = rnd.randrange(100000, 999999)
    otp = 123
    user.set_password(str(otp))
    user.save()

    sms_text = "کد فعال سازی شما جهت ثبت نام در سامانه :\n" + str(otp)
    sms = SMS()
    sent = sms.send(sms_text, mobile)
    if not sent:
        logger.error("Can't send sms")
        raise Http404
    data_response = {"success": True, "created": created}
    return JsonResponse(data_response, safe=False)


class LoginView(generics.GenericAPIView):
    """
    Media Crud
    """

    schema = AutoSchema(tags=["user"], operation_id_base="login")
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return JsonResponse(serializer.data, safe=False)
