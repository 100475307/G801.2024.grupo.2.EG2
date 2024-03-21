import json
import unittest

from unittest import TestCase
from uc3m_travel import hotel_management_exception
from uc3m_travel import hotel_manager


class TestRoomReservation(TestCase):
    """Test room reservation"""
    def setUp(self):
        """setUp"""
        try:
            with open(self.__path_tests + "f1_json.load", encoding = 'UTF-8', mode = "r") as f:
                test_room_reservation = json.load(f)
        except FileNotFoundError as e:
            raise hotel_management_exception("error en fichero o camino") from e
        except json.JSONDecodeError:
            test_room_reservation = []
        self.__test_room_reservation = test_room_reservation

    def test_hotel_reservation_ok1(self):
        """Test hotel reservation"""
        for input_data in self.__test_data_credit_card:
            if input_data["idTest"] == "TC1":
                hm = hotel_manager()
                localizer = hm.room_reservation(input_data["credit_card_number"], input_data["hotel_name"], input_data["id_card"],
                                                input_data["name_surname"], input_data["phone_number"],
                                                input_data["room_type"], input_data["arrival"],
                                                input_data["num_days"])
                self.assertEqual(localizer, ".......")



if __name__ == '__main__':
    unittest.main()
