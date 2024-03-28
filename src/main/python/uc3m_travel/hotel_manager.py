"""
clase hotel_manager
"""
import json
import hashlib
from luhn import verify
import hotel_management_exception as hme
import hotel_reservation
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
        funcion para verificar tarjeta. Devuelve True o False
        """
        if not x.isdigit():
            return False
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
            raise hme.hotel_management_exception("Wrong file or file path") from e
        except json.JSONDecodeError as e:
            raise hme.hotel_management_exception("JSON Decode Error - Wrong JSON Format") from e


        try:
            c = data["credit_card_number"]
            p = data["phoneNumber"]
            req = hotel_reservation(id_card="12345678Z",credit_card_number=c,name_and_surname="John Doe",phone_number=p,room_type="single",num_days=3)
        except KeyError as e:
            raise hme.hotel_management_exception("JSON Decode Error - Invalid JSON Key") from e
        if not self.validatecreditcard(c):
            raise hme.hotel_management_exception("Invalid credit card number")

        # Close the file
        return req

    def room_reservation(self, credit_card_number, id_card, name_and_surname, phone_number, room_type, arrival, num_days):
        """Devuelve una cadena que representa HM-FR-01-O1
        En caso de errores, devuelve una hotel_management_exception representa HM-FR-01-O2"""
        # Verificar HM-FR-01-I1: Número de tarjeta de crédito válido
        if not self.validatecreditcard(credit_card_number):
            print("ENTRA EN CREDIT CARD")
            raise hme.hotel_management_exception("Invalid credit card number provided")

        # Verificar HM-FR-01-I2: DNI válido
        if not self.validateidcard(id_card):
            raise hme.hotel_management_exception("Invalid identification number")

        # Verificar HM-FR-01-I3: Nombre y apellidos válidos
        if len(name_and_surname.split()) < 2 or len(name_and_surname) < 10 or len(name_and_surname) > 50:
            raise hme.hotel_management_exception("Invalid name and surname")

        # Verificar HM-FR-01-I4: Número de teléfono válido
        if not phone_number.isdigit() or len(phone_number) != 9:
            raise hme.hotel_management_exception("Invalid phone number")

        # Verificar HM-FR-01-I5: Tipo de habitación válido
        if room_type not in {'single', 'double', 'suite'}:
            raise hme.hotel_management_exception("Invalid room type")

        # Verificar HM-FR-01-I6: Formato de fecha de llegada válido
        try:
            datetime.strptime(arrival, '%d/%m/%Y')
        except ValueError:
            raise hme.hotel_management_exception("HM-FR-01-I6: Formato de fecha de llegada inválido")

        # Verificar HM-FR-01-I7: Número de noches válido
        try:
            num_days = int(num_days)
            if num_days < 1 or num_days > 10:
                raise ValueError
        except ValueError:
            raise hme.hotel_management_exception("HM-FR-01-I7: Número de noches inválido")


        # hemos pasado las pruebas por lo que datos correctos
        # añadimos información al fichero json
        reserva = self.read_data_from_json(self.__json_path + r"\reservas.json", "r")
        for i in reserva:
            if reserva["id_card"] == id_card:
                raise hme.hotel_management_exception("No puede haber más de una reserva por cliente")

        booking = hotel_reservation(credit_card_number, id_card, name_and_surname, phone_number, room_type, arrival, num_days)
        localizador = booking.localizer

        print("localizador", localizador)


        #almacenamos los datos de la reserva en el json de reservas
        pedido = {"credit_card_number": credit_card_number, "id_card": id_card, "name_and_surname": name_and_surname, "phone_number": phone_number, "room_type": room_type, "arrival": arrival, "num_days": num_days, "localizador": localizador}
        reserva.append(pedido)
        self.read_data_from_json(self.__json_path + r"\reservas.json")


        # Todo está correcto, se puede proceder con la reserva
        print("Reserva realizada exitosamente.")
        return localizador

#######################     FUNCION 2      ###################################################
class HotelStay:
    def __init__(self, alg, typ, localizer, idcard, arrival, departure, room_key):
        self.alg = alg
        self.typ = typ
        self.localizer = localizer
        self.idcard = idcard
        self.arrival = arrival
        self.departure = departure
        self.room_key = room_key


def guest_arrival(fichero_reservas):
    try:
        with open(fichero_reservas, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError as e:
        raise hme.hotel_management_exception("Wrong file or file path") from e
    except json.JSONDecodeError as e:
        raise hme.hotel_management_exception("JSON Decode Error - Wrong JSON Format") from e
    with open(fichero_reservas, 'r') as file:
        data = json.load(file)

    localizer = data.get('Localizer')

    with open(fichero_reservas, 'r') as file:
        reservations_data = file.read()

    #comprobar que el localizador está en reservas
    if localizer in reservations_data:
        num_days = data.get('num_days')

        #salida = llegada mas dias de estancia en segundos
        arrival = datetime.utcnow().timestamp()
        departure = arrival + (num_days * 86400)

        room_key_data = {
            "alg": "SHA-256",
            "typ": "room_key",
            "localizer": localizer,
            "arrival": arrival,
            "departure": departure
        }
        room_key_text = json.dumps(room_key_data, separators=(',', ':'))#Convertir a JSON sin espacios

        # Calcula el SHA-256
        room_key_hash = hashlib.sha256(room_key_text.encode()).hexdigest()

        #guardamos el hash en un fichero
        with open('hotel_stays.txt', 'a') as file:
            file.write(f"Localizer: {localizer}, Room Key: {room_key_hash}\n")

        return room_key_hash
    else:
        #el localizador no esta en reservas
        raise hme.hotel_management_exception("El localizador de reserva no esta en el fichero de reservas")
