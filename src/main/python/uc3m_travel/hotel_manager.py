"""
clase hotel_manager
"""
import json
import hashlib
from luhn import verify
from .hotel_management_exception import hotel_management_exception
from .hotel_reservation import hotel_reservation
from stdnum import es
import re
from datetime import datetime, timedelta

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
        return es.dni.validate(x)


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

def room_reservation(credit_card_numb, name_and_surname, id_card, phone_number, room_type, arrival, num_days):
    """Devuelve una cadena que representa HM-FR-01-O1
    En caso de errores, devuelve una hotel_management_exception representa HM-FR-01-O2"""
    # Verificar HM-FR-01-I1: Número de tarjeta de crédito válido
    if not verify(credit_card_numb):
        raise hotel_management_exception("HM-FR-01-I1: Número de tarjeta de crédito inválido")

    # Verificar HM-FR-01-I2: DNI válido
    if not es.dni.is_valid(id_card):
        raise hotel_management_exception("HM-FR-01-I2: DNI inválido")

    # Verificar HM-FR-01-I3: Nombre y apellidos válidos
    if len(name_and_surname.split()) < 2 or len(name_and_surname) < 10 or len(name_and_surname) > 50:
        raise hotel_management_exception("HM-FR-01-I3: Nombre y apellidos inválidos")

    # Verificar HM-FR-01-I4: Número de teléfono válido
    if not phone_number.isdigit() or len(phone_number) != 9:
        raise hotel_management_exception("HM-FR-01-I4: Número de teléfono inválido")

    # Verificar HM-FR-01-I5: Tipo de habitación válido
    if room_type not in {'single', 'double', 'suite'}:
        raise hotel_management_exception("HM-FR-01-I5: Tipo de habitación inválido")

    # Verificar HM-FR-01-I6: Formato de fecha de llegada válido
    try:
        datetime.strptime(arrival, '%d/%m/%Y')
    except ValueError:
        raise hotel_management_exception("HM-FR-01-I6: Formato de fecha de llegada inválido")

    # Verificar HM-FR-01-I7: Número de noches válido
    try:
        num_days = int(num_days)
        if num_days < 1 or num_days > 10:
            raise ValueError
    except ValueError:
        raise hotel_management_exception("HM-FR-01-I7: Número de noches inválido")

    # Todo está correcto, se puede proceder con la reserva
    print("Reserva realizada exitosamente.")


# Ejemplo de uso
try:
    room_reservation('1234567812345678', 'John Doe', '12345678Z', '123456789', 'single', '01/07/2024', '5')
except hotel_management_exception as e:
    print("Error:", e)


"""
    def validateidcard(self, x):

        #funcion para verificar id
        #compramos que tiene la longitud correcta
        if len(x) != 9:
            return False #devolver el error *****************

        #comprobamos que los 8 primeros caracteres son dígitos
        if not x[:8].isdigit():
            return False #devolver el error **********

        #comprobamos que el último caracter es una letra
        if not x[8].isalpha():
            return False #devolver el error ********

        letras_validas = 'TRWAGMYFPDXBNJZSQVHLCKE'

        id_number = int(x[:8])

        #calculo la letra esperada
        letra_esperada = id_number % 23

        #comparo la letra esperada con la real
        if x[8].upper() != letras_validas[letra_esperada]:
            return False #devolver el error *********
        return True #no da error ******
"""