class PhoneNumberStatus:
    PENDING = 0
    CODE_RECEIVED = 1
    BANNED = 2
    TIMEOUT = 3


class PhoneNumber:
    STATUS: str
    CODE: str
    PHONE_NUMBER: str

    def __init__(self, status: str, code: str, phone_number: str):
        self.STATUS = status
        self.CODE = code
        self.PHONE_NUMBER = phone_number
