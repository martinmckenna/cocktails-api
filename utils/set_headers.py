from flask import Response
import json


def send_200(data, location='/'):
  return Response(
      json.dumps(data),
      status=200,
      mimetype='application/json',
      headers={
          "location": location
      }
  )


def send_400(error, meta="", location='/'):
    return Response(
        json.dumps({
            "error": error,
            "meta": meta
        }),
        status=400,
        mimetype='application/json'
    )


def send_404(location='/'):
  return Response(
      json.dumps({
          'error': 'Entity not found'
      }),
      status=404,
      mimetype='application/json',
      headers={
          "location": location
      }
  )
