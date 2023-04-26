class JSONException(Exception):
    def __init__(self, status_code: int=500, error_msg: str="Internal Server Error"):
        self.status_code = status_code
        self.error_msg = error_msg