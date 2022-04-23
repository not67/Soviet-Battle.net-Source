from models.PhoneNumbers import PhoneNumber


class FiveSimPhoneNumber(PhoneNumber):
    
    def __init__(self, status: str, code: str, phone_number: str):
        super().__init__(status, code, phone_number)