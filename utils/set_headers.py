from flask import Response
import json


def send_200(data, location='/'):
  return Response(
      json.dumps(data),
      status=200,
      mimetype='application/json',
  )


def send_400(data, location='/'):
    return Response(
        json.dumps(data),
        status=400,
        mimetype='application/json'
    )
