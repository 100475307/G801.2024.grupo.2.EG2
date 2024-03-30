import unittest
from unittest import TestCase
import json
"""from uc3m_travel import hotel_management_exception
from uc3m_travel import hotel_management_exception
from uc3m_travel import hotel_stay
import hotel_management_exception"""
from src.main.python.uc3m_travel.hotel_stay import hotel_stay
from src.main.python.uc3m_travel.hotel_manager import hotel_manager
from src.main.python.uc3m_travel.hotel_management_exception import hotel_management_exception
import os.path
import hashlib
class test_guest_arrival(TestCase):
    """clase para los test de la función 2"""
    __path_tests = str(r"C:\Users\ghija\PycharmProjects"
                       r"\G801.2024.grupo.2.EG2\src\main\python\uc3m_travel\json_files")
    __path_data = str(r"C:\Users\ghija\PycharmProjects"
                      r"\G801.2024.grupo.2.EG2\src\main\python\uc3m_travel\json_files")

    def setUp(self):
        """funcion setUp"""
        try:
            with open(self.__path_tests + r"\tests2.json", encoding='UTF-8', mode="r") as f:
                testroomreservation = json.load(f)
        except FileNotFoundError as e:
            raise hotel_management_exception("error en fichero o camino") from e
        except json.JSONDecodeError:
            testroomreservation = []
        self.__test_room_reservation = testroomreservation
        #cerramos el fichero de las reservas
        fichero_reservas = self.__path_data + r"\reservas.json"
        if os.path.isfile(fichero_reservas):
            os.remove(fichero_reservas)

    def get_store_hash(self):
        """gets md5 hash for the stay store"""
        try:
            with open(self.__path_tests + r"\tests1.json", encoding='UTF-8', mode="r") as f:
                file_hash = hashlib.md5(f.__str().encode()).hexdigest()
        except FileNotFoundError:
            file_hash = ""
        return file_hash
    def test_reservation_OK(self):
        """Casos de test correctos"""
        for index, input_data in enumerate(self.__test_data_f2):
            if index + 1 == 1:
                test_id = "TC" + str(index + 1)
                with self.subTest(test_id):
                    print("Executing: " + test_id + ":" + input_data)
                    self.generate_tmp_test_data_file(input_data)
                    hm = hotel_manager()
                    room_key = hm.guest_arrival(self.__path_tests + self.__tmp_test_data_file)
                    if test_id == "TC1":
                        self.assertEqual(room_key, ({"Localizer":"123456789ABCDEF1234567890ABCEDF1","IdCard": "53994572A"}))
                                                        #cambiar por el localizador correcto
    def test_reservation_KO(self):
        """Casos de test incorrectos"""
        for index, input_data in enumerate(self.__test_data_f2):
            if index + 1 in [2,71]:
                test_id = "TC" + str(index + 1)
                with self.subTest(test_id):
                    print("Executing: " + test_id + ":" + input_data)
                    self.generate_tmp_test_data_file(input_data)
                    hm = hotel_manager()
                    room_key = hm.guest_arrival(self.__path_tests + self.__tmp_test_data_file)
                    if test_id == "TC1":
                        self.assertEqual(room_key, ({"Localizer":"123456789ABCDEF1234567890ABCEDF1","IdCard": "53994572A"}))