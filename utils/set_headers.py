from flask import Response


def send_200(data, location='/'):
  return Response(
      data,
      status=200,
      mimetype='application/json',
  )
