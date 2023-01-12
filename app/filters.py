def valid_req_params(params):
    return {key:params[key] for key in params if params[key] is not None}