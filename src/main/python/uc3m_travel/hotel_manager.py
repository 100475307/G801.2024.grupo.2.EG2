"""
clase hotel_manager
"""
import json
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
        # PLEASE INCLUDE HERE THE CODE FOR VALIDATING THE GUID
        # RETURN TRUE IF THE GUID IS RIGHT, OR FALSE IN OTHER CASE
        contador = 0
        suma = 0
        for pares in reversed(x):
            contador += 1
            pares = int(pares)
            if contador%2 != 0:
                pares = 2*pares
                if pares > 9:
                    pares = pares - 9
            suma += pares

        comprobar = suma%10
        if comprobar == 0:
            print("número de tarjeta válido")
        else:
            print("número de tarjeta erróneo")
            return False
        return True

    def ReaddatafromJSOn(self, fi):
        """
        funcion leer datos de json
        """
        try:
            with open(fi) as f:
                DATA = json.load(f)
        except FileNotFoundError as e:
            raise hotel_management_exception("Wrong file or file path") from e
        except json.JSONDecodeError as e:
            raise hotel_management_exception("JSON Decode Error - Wrong JSON Format") from e


        try:
            c = DATA["CreditCard"]
            p = DATA["phoneNumber"]
            req = hotel_reservation(IDCARD="12345678Z",creditcardNumb=c,nAMeAndSURNAME="John Doe",phonenumber=p,room_type="single",numdays=3)
        except KeyError as e:
            raise hotel_management_exception("JSON Decode Error - Invalid JSON Key") from e
        if not self.validatecreditcard(c):
            raise hotel_management_exception("Invalid credit card number")

        # Close the file
        return req
