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


def send_400(error="Invalid Payload", field="", location='/'):
    return Response(
        json.dumps({
            "error": error,
            "field": field
        }),
        status=400,
        mimetype='application/json',
        headers={
            "location": location
        }
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


def send_401(error='Unauthorized', location='/'):
    return Response(
        json.dumps({
            'error': error,
        }),
        status=401,
        headers={
            'location': location
        }
    )
