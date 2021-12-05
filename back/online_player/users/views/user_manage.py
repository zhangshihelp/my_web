import logging

from rest_framework import status
from rest_framework.views import APIView

from online_player.pub.response.common_response import OnlinePlayerResponse
from online_player.pub.tools.http import get_http_head_param


log = logging.getLogger('users')


class UserManage(APIView):

    def get(self, request):
        language = get_http_head_param(request, 'language', log)
        data = ''
        return OnlinePlayerResponse(status=True, data=data, http_status=status.HTTP_200_OK, language=language)
