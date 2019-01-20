# @returns true if row already exists in database
def check_for_duplicate(Model, filter_key, client_request_value):
  return [
      Model.query.filter(getattr(Model, filter_key)==client_request_value).first()
  ][0] is not None
