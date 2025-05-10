import json
from rest_framework import renderers


class UserRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_typr=None, renderer_contex=None):
        response = ""
        if 'ErrorDetail' in str(data):
            response = json.dumps({"error" : data })
        else:
            response = json.dumps(data)
        
        return response