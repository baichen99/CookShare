class JSONException(Exception):
    def __init__(self, error_msg: str, status_code: int=500):
        self.status_code = status_code
        self.error_msg = error_msg