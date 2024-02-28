import json

import requests
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status

from rest_framework.parsers import BaseParser
from rest_framework.views import APIView

class OctetStreamParser(BaseParser):
    charset = None
    format = None
    media_type = "application/octet-stream"
    render_style = "binary"

    def parse(self, stream, media_type=None, parser_context=None):
        return stream.read()


class DRMProxyView(APIView):
    parser_classes = [OctetStreamParser]

    def post(self, request, *args, **kwargs):
        asset_id = kwargs.get('asset_id')
        access_token = self.request.query_params.get("access_token", "")
        body = {
            "player_payload": self.request.data,
            "license_specs": {
                "security_level": 1,
                "required_output_protection": {
                    "hdcp": "HDCP_NO_DIGITAL_OUTPUT"
                }
            }
        }
        license_url = f"https://8bde-49-43-249-218.ngrok-free.app/api/v1/k6gdyc/assets/{asset_id}/drm_license/?access_token={access_token}"

        license_response = requests.post(license_url, data=self.request.data, headers={"content-type": "application/octet-stream"} )
        license_data = license_response.content
        license_response.raise_for_status()

        return HttpResponse(
            license_data,
            status=status.HTTP_200_OK,
            content_type="application/octet-stream",
        )


def index_view(request):
    return render(request, template_name="index.html")