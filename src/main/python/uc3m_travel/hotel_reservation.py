"""
clase hotel_reservation
"""
import hashlib
from datetime import datetime, timezone


class hotel_reservation:
    """
    clase hotel_reservation
    """
    def __init__(self, id_card, credit_card_numb, name_and_surname, phone_number, room_type, arrival, num_days):
        """
        funcion init
        """
        self.__credit_card_number = credit_card_numb
        self.__id_card = id_card
        justnow = datetime.now(timezone.utc)
        self.__today = datetime.timestamp(justnow)
        self.__arrival = arrival
        self.__name_and_surname = name_and_surname
        self.__phone_number = phone_number
        self.__room_type = room_type
        self.__num_days = num_days

    def __str__(self):
        """return a json string with the elements required to calculate the localizer"""
        #VERY IMPORTANT: JSON KEYS CANNOT BE RENAMED
        jsonInfo = {"credit_card": self.__credit_card_number,
                    "id_card": self.__id_card,
                     "name_and_surname": self.__name_and_surname,
                     "phone_number:": self.__phone_number,
                    "room_type": self.__room_type,
                    "arrival": self.__arrival,
                     "num_days": self.__num_days,
                     }
        return "HotelReservation:" + jsonInfo.__str__()
    @property
    def credit_card(self):
        """
        funcion que devuelve el numero de tarjeta
        """
        return self.__credit_card_number
    @credit_card.setter
    def credit_card(self, value):
        """
        funcion que lo devuelve igualado a un valor
        """
        self.__credit_card_number = value

    @property
    def id_card(self):
        """
        funcion que devuelve el numero de id
        """
        return self.__id_card
    @id_card.setter
    def id_card(self, value):
        """
        funcion que lo iguala a un valor
        """
        self.__id_card = value


    @property
    def localizer( self ):
        """Returns the md5 signature"""
        return hashlib.md5(str(self).encode()).hexdigest()
