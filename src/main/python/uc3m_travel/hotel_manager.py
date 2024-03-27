"""
clase hotel_manager
"""
import json
import hashlib
from luhn import verify
from src.main.python.uc3m_travel import hotel_management_exception
from src.main.python.uc3m_travel import hotel_reservation
from stdnum import es
import re
from datetime import datetime, timedelta

class hotel_manager:
    """
    clase hotel_manager
    """
    _json_path = str(r"C:\Users\inest\PycharmProjects\Desarrollo de Software"
                     r"\G801.2024.grupo.2.EG2\src\main\python\uc3m_travel\json_files")
    def __init__(self):
        """
        hace pass del init
        """
        pass

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

    def room_reservation(self, credit_card_numb, name_and_surname, id_card, phone_number, room_type, arrival, num_days):
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


        # hemos pasado las pruebas por lo que datos correctos
        # añadimos información al fichero json
        reserva = self.read_data_from_json(self.__json_path + r"\reservas.json", "r")
        for i in reserva:
            if reserva["id_card"] == id_card:
                raise hotel_management_exception("No puede haber más de una reserva por cliente")

        booking = hotel_reservation(credit_card_numb, id_card, name_and_surname, phone_number, room_type, arrival, num_days)
        localizador = booking.localizer

        print("localizador", localizador)


        #almacenamos los datos de la reserva en el json de reservas
        pedido = {"credi_card_numb": credit_card_numb, "id_card": id_card, "name_and_surname": name_and_surname, "phone_number": phone_number, "room_type": room_type, "arrival": arrival, "num_days": num_days, "localizador": localizador}
        reserva.append(pedido)
        self.read_data_from_json(self.__json_path + r"\reservas.json")


        # Todo está correcto, se puede proceder con la reserva
        print("Reserva realizada exitosamente.")
        return localizador



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