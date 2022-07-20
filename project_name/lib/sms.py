import requests
import json
from django.core.cache import cache
from rest_framework import status
from rest_framework.exceptions import APIException
from decouple import config

from project_name.lib.logger import logger


class SMS:
    url = ""
    payload = {
        "CommandData": {}
    }
    headers = {"Authorization": "", "Content-Type": "application/json"}

    def __init__(self):
        token = cache.get("token")
        if token:
            self.headers["Authorization"] = token
        else:
            url = ""
            payload = {
                "CommandData":
                    {
                        "username": "",
                        "password": ""
                    }
            }
            headers = {"Content-Type": "application/json"}
            try:
                response = requests.request(
                    "POST", url, json=payload, headers=headers
                )
            except Exception as e:
                logger.error(f"error request: {e}")
                error = APIException()
                error.status_code = 503
                raise error

            json_response = json.loads(response.text)
            token = json_response["contentData"]["token"]
            cache.set("token", token, timeout=1260)
            self.headers["Authorization"] = token

    def send(self, message, mobile, *args, **kwargs):
        self.payload["CommandData"] = {
            "SMSQueueList": [
                {
                    "Message": message,
                    "Mobile": mobile,
                }
            ]
        }
        try:
            logger.info("send_sms payload: %s", self.payload)
            response = requests.request(
                "POST", self.url, json=self.payload, headers=self.headers
            )
            
        except Exception as e:
            logger.error(f"error request: {e}")
            error = APIException()
            error.status_code = 503
            raise error

        logger.info("send_sms respons: %s", response.text)
        if status.is_server_error(response.status_code):
            error = APIException()
            error.status_code = 503
            raise error
        if status.is_client_error(response.status_code):
            error = APIException()
            error.status_code = 500
            raise error
        if json.loads(response.text)["header"]["status"]:
            return True
        return False
        
            
