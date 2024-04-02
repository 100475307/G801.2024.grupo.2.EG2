"""
clase hotel_manager
"""
import json
import hashlib
from freezegun import freeze_time
from datetime import datetime, timedelta
import os
import re
import sys
from jsonschema import validate, ValidationError
from luhn import verify
from stdnum.es import nif
import sys
sys.path.append(r'C:\Users\ghija\PycharmProjects\G801.2024.grupo.2.EG2\src\main\python\uc3m_travel')

from hotel_reservation import hotel_reservation as hr
from hotel_management_exception import hotel_management_exception as hme
from hotel_stay import hotel_stay


class hotel_manager:
    """
    clase hotel_manager
    """
    __json_path = str(r"C:\Users\ghija\PycharmProjects\G801.2024.grupo.2.EG2\src\main\python\json_files")
    def init(self):
        """
        hace pass del init
        """


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
        letrasValidas = "TRWAGMYFPDXBNJZSQVHLCKE"
        dniNumeros = int(x[:-1])
        letraEsperada = letrasValidas[dniNumeros % 23]
        #si no coincide la letra esperada con la obtenida, False
        if x[-1].upper() != letraEsperada:
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

    def write_data_to_json(self, fi, data, mode):
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
        if len(credit_card_number) > 16:
            raise hme(
                "Tarjeta erronea. Más de 16 dígitos")
        if len(credit_card_number) < 16:
            raise hme(
                "Tarjeta erronea. Menos de 16 dígitos")
        if not credit_card_number.isdigit():
            raise hme(
                "Tarjeta erronea. Contiene letras")
        if not self.validatecreditcard(credit_card_number):
            print("PASA POR AQUIIII")
            raise hme(
                "Tarjeta erronea. No cumple con el algoritmo de Luhn")

        if not self.validateidcard(id_card):
            raise hme(
                "DNI erróneo")

        if len(name_and_surname.split()) <2:
            raise hme(
                "Nombre y apellidos erroneos. Tiene que tener al menos un nombre y un apellido")

        if len(name_and_surname) > 50:
            raise hme(
                "Nombre y/o apellido erróneos. Más de 50 caracteres")
        if len(name_and_surname) < 10:
            raise hme(
                "Nombre y/o apellido erróneos. Menos de 10 caracteres")

        if name_and_surname.startswith(' ') or name_and_surname.startswith(' '):
            raise hme(
                "Nombre y/o apellido erróneos. No puede empezar ni terminar por espacio")

        if '  ' in name_and_surname:
            raise hme(
                "Nombre y/o apellido erróneos. No puede usar dos espacios consecutivos")

        if not all(caracter.isalpha() or caracter.isspace() for caracter in name_and_surname):
            raise hme("Nombre y/o apellido erróneos. Contiene letras")

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

        print("DATOOOOS: ", credit_card_number, id_card, name_and_surname, phone_number, room_type, arrival, num_days)
        print("Localizador creado:", localizador)

        # Almacenar los datos de la reserva en el archivo
        reservaActual = {
            "credit_card_number": credit_card_number,
            "id_card": id_card,
            "name_and_surname": name_and_surname,
            "phoneNumber": phone_number,
            "roomType": room_type,
            "arrival": arrival,
            "numDays": num_days,
            "localizador": localizador
        }
        reservas.append(reservaActual)
        self.write_data_to_json(self.__json_path + r"\reservas.json", reservas, "w")
        print("Reserva almacenada con éxito.")
        return localizador

    def guest_arrival(self, fichero_reservas):
        hotel_stays = [] #lista vacía para almacenar todas las estancias
        # esquema correcto para los archivos json
        esquema = {
            "type": "object",
            "properties": {
                "Localizer": {"type": "string"},
                "IdCard": {"type": "string"}
            },
            "required": ["Localizer", "IdCard"]
        }
        print("Esquemaaaaaaaaaa", esquema)
        try:
            if os.stat(fichero_reservas).st_size == 0:
                print("RESERVAS VACIOOOO")
                raise hme("El fichero de reservas está vacío")
            with open(fichero_reservas, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not data:
                print("FICHERO RESERVAS VACIOOOO")
                raise hme("El archivo está vacío")
            """for key, value in data.items():
                print("entra en bucle:", key, value)
                if not value and key == "Localizer":
                    raise hme("Valor de localizador vacío")
                if not value and key == "IdCard":
                    raise hme("Valor de IdCard vacío")"""

            if "Localizer" not in data or "IdCard" not in data:
                raise hme("Hay un fallo de escritura en alguna de las claves")

            if data["Localizer"] == "":
                print("entra en etiqueta 1 nulo")
                raise hme("Valor etiqueta 1 nulo")
            if not data['IdCard']:
                print("entra en etiqueta 2 nula")
                raise hme("Valor etiqueta 2 nulo")
            if len(data['Localizer']) != 32:
                print("longitud de la etiqueta 1")
                raise hme("Longitud del valor de la etiqueta 1 incorrecto")
            if len(data['IdCard']) != 9:
                print("longitud de la etiqueta 2")
                raise hme("Longitud del valor de la etiqueta 2 incorrecto")
            if not data['Localizer'].isalnum():
                print("formato de la etiqueta 1")
                raise hme("Formato del valor de la etiqueta 1 incorrecto")
            if nif.is_valid(data['IdCard']) == False:
                print("id card 8 numeros y una letra")
                raise hme("Los primeros 8 caracteres del campo 'IdCard' deben ser números y el último una letra.")

            try:
                validate(instance=data, schema=esquema)
            except ValidationError as e:
                print("formato del archivo json incorrecto despues de ifssss")
                raise hme("Formato del archivo JSON incorrecto") from e

            #HM-FR-02-P1:control para ver que el localizador esta en reservas y tiene el mismo ID
            reservas = self.read_data_from_json(self.__json_path + r"\reservas.json", "r")

            for reserva in reservas:
                print("entra en bucle reservas")
                if data["Localizer"] in reserva["localizador"]:
                    if reserva["id_card"] != data["IdCard"]:
                        print("entra en localizador e id no coinciden")
                        raise hme('El localizador de la reserva y el ID no coinciden')
                    numero_de_dias = reserva["numDays"]
                    print(numero_de_dias)
                    tipo_de_habitacion = reserva["roomType"]
                    break
                else:
                    print("entra en else con localizador no en reservas")
                    raise hme('El localizador no está en las reservas')

            #HM-FR-02-P2: creación de la instancia

            #crear el room_key
            estancia = hotel_stay(data["IdCard"], data["Localizer"], numero_de_dias, tipo_de_habitacion)
            arrival = str(estancia.arrival)
            departure = estancia.departure.strftime("%d/%m/%Y")

            room_key = estancia.room_key
            # Almacenar los datos de la estancia en el archivo
            estanciaA = {
                "id_card": data['IdCard'],
                "room_type": tipo_de_habitacion,
                "arrival": arrival,
                "num_days": numero_de_dias,
                "departure": departure,
                "localizador": data['Localizer'],
                "room_key": room_key
            }
            hotel_stays.append(estanciaA)
            self.write_data_to_json(self.__json_path + r"\estancias.json", hotel_stays, "w")

            return room_key

        except FileNotFoundError as e:
            print("entra en final wrong file or path")
            raise hme("Archivo o camino incorrecto") from e
        except json.JSONDecodeError as e:
            print("entra en final formato de json incorrecto")
            raise hme("Formato del archivo JSON incorrecto") from e



    @freeze_time("2024-06-16")
    def guest_departure(self, room_key):
        checkouts = self.read_data_from_json(self.__json_path + r"\estancias.json", "r")
        if not checkouts:
            raise hme("No hay datos de estancias")

        # Comprueba que el room_key esté en un formato correcto
        if not re.match(r"^[a-fA-F0-9]{64}$", room_key):
            raise hme("Código de habitación no cumple con el formato correcto")


        # Para cada entrada de chechout, miramos si la llave de la habitación coincide con la que se ha pasado como argumento
        # Si la llave de la habitación existe, ponemos una booleana EntraCkeckout a True
        entracheckout, entrafecha = False, False
        hoy = datetime.now().date().strftime("%d/%m/%Y")
        print(checkouts)
        for checkout in checkouts:
            print('holaaaaaaaaaaaaaaaaaaaaaaaaaaa')
            if checkout["room_key"] == room_key:
                entracheckout = True
                print('ha comprobado la roomkey')
                print('la fecha de salida es:',checkout["departure"])
                print('la fecha de hoy es:',   hoy)
                print('fecha salida',hoy + timedelta(days=int(checkout["num_days"])))
                checkout_departure = datetime.strptime(checkout["departure"], "%d-%m-%Y")
                if checkout_departure == hoy + timedelta(days=int(checkout["num_days"])):
                    entrafecha = True

        # Si el room_key existe, verificar que la fecha de salida esperada coincida con hoy
        if entracheckout == False:
            raise hme("La llave de la habitación no existe")
        if entrafecha == False:
            raise hme("La fecha de salida no coincide con la de hoy")

        # Si lo anterior es correcto, guardar los datos (fecha de salida + llave de la habitación) en un nuevo archivo checkouts.json mediante writeDataToJson
        # si falla la apetura del archivo porque no existe, crearlo
        checkouts2 = self.read_data_from_json(self.__json_path + r"\checkouts.json", "r")
        if not checkouts2:
            checkouts2 = []

        # Escribir los datos en el archivo mediante writeDataToJson salvo que esa persona ya haya hecho checkout ese dia
        # Tiene que ser ubn archivo tipo json con la forma: "departure": hoy, "room_key": room_key
        for checkout in checkouts2:
            if checkout["room_key"] == room_key:
                raise hme("La persona ya ha hecho checkout hoy")
        # checkouts2["Room_key"] = room_key
        # checkouts2["departure"] = hoy
        checkoutactual = {
            "Room_key": room_key,
            "departure": hoy,
        }
        if checkoutactual not in checkouts2:
            checkouts2.append(checkoutactual)
        self.write_data_to_json(self.__json_path + r"\checkouts.json", checkouts2, "w")

        return "Salida registrada con éxito"