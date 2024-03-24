"""
clase hotel_manager
"""
import json
import hashlib
from luhn import verify
from .hotel_management_exception import hotel_management_exception
from .hotel_reservation import hotel_reservation


class hotel_manager:
    """
    clase hotel_manager
    """
    def __init__(self):
        """
        hace pass del init
        """

    def validatecreditcard(self, x):
        """
        funcion para verificar tarjeta
        """
        verify (x)

    def validateidcard(self, x):
        """
        funcion para verificar tarjeta
        """
        pass

    def read_data_from_json(self, fi):
        """
        funcion leer datos de json
        """
        try:
            with open(fi, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError as e:
            raise hotel_management_exception("Wrong file or file path") from e
        except json.JSONDecodeError as e:
            raise hotel_management_exception("JSON Decode Error - Wrong JSON Format") from e


        try:
            c = data["CreditCard"]
            p = data["phoneNumber"]
            req = hotel_reservation(id_card="12345678Z",credit_card_numb=c,name_and_surname="John Doe",phone_number=p,room_type="single",num_days=3)
        except KeyError as e:
            raise hotel_management_exception("JSON Decode Error - Invalid JSON Key") from e
        if not self.validatecreditcard(c):
            raise hotel_management_exception("Invalid credit card number")

        # Close the file
        return req
