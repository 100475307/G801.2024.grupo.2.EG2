import json
from .HotelManagementException import HotelManagementException
from .HotelReservation import HotelReservation

class HotelManager:
    def __init__(self):
        pass

    def validatecreditcard( self, x ):
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
            return True
        else:
            print("número de tarjeta erróneo")
            return False

    def ReaddatafromJSOn( self, fi):

        try:
            with open(fi) as f:
                DATA = json.load(f)
        except FileNotFoundError as e:
            raise HotelManagementException("Wrong file or file path") from e
        except json.JSONDecodeError as e:
            raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from e


        try:
            c = DATA["CreditCard"]
            p = DATA["phoneNumber"]
            req = HotelReservation(IDCARD="12345678Z",creditcardNumb=c,nAMeAndSURNAME="John Doe",phonenumber=p,room_type="single",numdays=3)
        except KeyError as e:
            raise HotelManagementException("JSON Decode Error - Invalid JSON Key") from e
        if not self.validatecreditcard(c):
            raise HotelManagementException("Invalid credit card number")

        # Close the file
        return req
