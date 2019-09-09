from django import http
from .encoders import BaseObjectSerializer as _S


def cors(response, origin='*'):
    response["Access-Control-Allow-Origin"] = origin
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


class JSONResponse(http.HttpResponse):
    def __init__(self, obj='', json_opts=None, mimetype='application/json',
                 *args, **kwargs):
        json_opts = json_opts if isinstance(json_opts, dict) else {}
        content = _S.to_json(obj, **json_opts)
        super().__init__(content, mimetype, *args, **kwargs)
        cors(self)


def page_not_found():
    raise http.Http404
