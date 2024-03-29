"""
clase hotel_manager
"""
import json
import hashlib
from luhn import verify
import sys

sys.path.append(r'C:\Users\ghija\PycharmProjects\G801.2024.grupo.2.EG2\src\main\python\uc3m_travel')

from hotel_management_exception import hotel_management_exception as hme
from hotel_reservation import hotel_reservation as hr
from hotel_stay import hotel_stay
from stdnum.es import nif
import re
from datetime import datetime, timedelta


class hotel_manager:
    """
    clase hotel_manager
    """
    __json_path = str(r"C:\Users\ghija\PycharmProjects\G801.2024.grupo.2.EG2\src\main\python\json_files")

    def init(self):
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
        return verify(x)

    def validateidcard(self, x):
        #Comprobamos la longitud del DNI
        if len(x) != 9:
            return False
        #Verificar que está formado por 8 dígitos + 1 letra
        if not x[:1].isdigit() or not x[-1].isalpha():
            return False
        #calculamos la letra esperada a partir de los números
        letras_validas = "TRWAGMYFPDXBNJZSQVHLCKE"
        dni_numeros = int(x[:-1])
        letra_esperada = letras_validas[dni_numeros % 23]
        #si no coincide la letra esperada con la obtenida, False
        if x[-1].upper() != letra_esperada:
            return False
        return True

    def es_bisiesto(self, ano):
        return ano % 4 == 0 and (ano % 100 != 0 or ano % 400 == 0)
    def validatearrival(self, x):
        partesfecha = x.split('/')
        #Si no solo contiene día, fecha y hora
        if len(partesfecha) != 3:
            return False
        #si día o mes más de 2 dígitos y año más de 4
        if len(partesfecha[0]) != 2 or len(partesfecha[1]) != 2 or len(partesfecha[2]) != 4:
            return False

        #verificar que no tiene dígitos
        if not partesfecha[0].isdigit() or not partesfecha[1].isdigit():
            return False
        #verificar que máximo 31 días y mínimo 1
        dia = int(partesfecha[0])
        if dia < 1 or dia > 31:
            return False

        # Verificar que el mes esté entre 1 y 12
        mes = int(partesfecha[1])
        if mes < 1 or mes > 12:
            return False

        #verificar febrero y días en función de si es bisiesto
        if mes == 2:
            if self.es_bisiesto(int(partesfecha[2])):
                if dia < 1 or dia > 29:
                    return False
            elif dia < 1 or dia > 28:
                return False
        #verifica que el mes tiene el número de días que corresponde
        elif mes in [4, 6, 8, 11]:
            if dia < 1 or dia > 30:
                return False
        return True

    def validatenumdays(self, x):
        # Verificar si el número es dígito y está entre 1 y 10
        if x.isdigit():
            numero = int(x)
            if numero >= 1 and numero <= 10:
                return True
        return False

    def read_data_from_json(self, fi, mode):
        """
        funcion leer datos de json
        """
        try:
            with open(fi, encoding="UTF-8", mode=mode) as f:
                data = json.load(f)
        except FileNotFoundError: #en diapositivas, estas dos líneas !=
            data = []
        except json.JSONDecodeError:
            data = []
        return data

    def writeDataToJson(self, fi, data, mode):
        """write data to json file"""
        try:
            with open(fi, encoding='UTF-8', mode=mode) as f:
                json.dump(data, f, indent=4)
        except FileNotFoundError as e:
            raise hme("Wrong file or file path") from e
        except json.JSONDecodeError as e:
            raise hme("JSON Decode Error - Wrong JSON Format") from e
        return data

    def room_reservation(self, credit_card_number, id_card, name_and_surname, phone_number, room_type, arrival, num_days):
        '''Room Reservation'''
        if not self.validatecreditcard(credit_card_number):
            raise hme(
                "Tarjeta erronea. No cumple con el algoritmo de Luhn")
        if len(credit_card_number) > 16:
            raise hme(
                "Tarjeta erronea. Más de 16 dígitos")
        if len(credit_card_number) < 16:
            raise hme(
                "Tarjeta erronea. Menos de 16 dígitos")
        if not credit_card_number.isdigit():
            raise hme(
                "Tarjeta erronea. Contiene letras")
        if not self.validateidcard(id_card):
            raise hme(
                "DNI erróneo")
        if len(name_and_surname) > 50:
            raise hme(
                "Nombre y/o apellido erróneos. Más de 50 caracteres")
        if len(name_and_surname) < 10:
            raise hme(
                "Nombre y/o apellido erróneos. Menos de 10 caracteres")
        if len(name_and_surname.split()) <2:
            raise hme(
                "Nombre y apellidos erroneos. Tiene que tener al menos un nombre y un apellido")

        if name_and_surname.startswith(' ') or name_and_surname.startswith(' '):
            raise hme(
                "Nombre y/o apellido erróneos. No puede empezar ni terminar por espacio")

        if '  ' in name_and_surname:
            raise hme(
                "Nombre y/o apellido erróneos. No puede usar dos espacios consecutivos")

        if len(phone_number) > 9:
            raise hme(
                "Número de teléfono erróneo. Más de 9 números")
        if len(phone_number) < 9:
            raise hme(
                "Número de teléfono erróneo. Menos de 9 números")
        if not phone_number.isdigit():
            raise hme(
                "Número de teléfono erróneo. Contiene letras")

        if room_type not in {'single', 'double', 'suite'}:
            raise hme(
                "Tipo de habitación errónea")

        if not self.validatearrival(arrival):
            raise hme("Fecha de llegada errónea")

        if not self.validatenumdays(num_days):
            raise hme("Número de días no válido")
        #Si hemos pasado todas las pruebas, tenemos datos correctos
        # Comprobamos que el cliente no tenga ya reservas
        reservas = self.read_data_from_json(self.__json_path + r"\reservas.json", "r")
        for reserva in reservas:
            if reserva["id_card"] == id_card:
                raise hme(
                    "There can´t be more than 1 reservation per client")
        # Creamos el localizador
        booking = hr(credit_card_number, id_card, name_and_surname,
                     phone_number, room_type, arrival, num_days)
        localizador = booking.localizer
        print("Localizador creado:", localizador)

        # Almacenar los datos de la reserva en el archivo
        reserva_actual = {
            "credit_card_number": credit_card_number,
            "id_card": id_card,
            "name_and_surname": name_and_surname,
            "phoneNumber": phone_number,
            "roomType": room_type,
            "arrival": arrival,
            "numDays": num_days,
            "localizador": localizador
        }
        reservas.append(reserva_actual)
        self.writeDataToJson(self.__json_path + r"\reservas.json", reservas, "w")
        print("Reserva almacenada con éxito.")
        return localizador

#################################################### FUNCION 2 ####################################################
class HotelStay:
    def _init_(self, alg, typ, localizer, idcard, arrival, departure, room_key):
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
        raise hme.hotel_management_exception("El localizador de reserva no esta en el fichero de reservas")
