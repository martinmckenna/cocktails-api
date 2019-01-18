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


def send_400(error="Invalid Payload", meta="", location='/'):
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


def send_401(location='/'):
    return Response(
        json.dumps({
            'error': 'Unauthorized',
            'meta': 'You do not have privledges to perform this action'
        }),
        status=401,
        headers={
            'location': location
        }
    )
