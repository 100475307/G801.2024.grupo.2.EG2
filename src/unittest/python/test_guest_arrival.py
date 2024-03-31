"""incluir casos de prueba de la función 2"""
from unittest import TestCase
import json
import os.path
import hashlib
from src.main.python.uc3m_travel.hotel_stay import hotel_stay
from src.main.python.uc3m_travel.hotel_manager import hotel_manager
from src.main.python.uc3m_travel.hotel_management_exception import hotel_management_exception


class test_guest_arrival(TestCase):
    """clase para los test de la función 2"""
    __path_tests = str(r"C:\Users\inest\PycharmProjects\Desarrollo de Software"
                       r"\G801.2024.grupo.2.EG2\src\main\python\json_files")
    __path_tests2 = str(r"C:\Users\inest\PycharmProjects\Desarrollo de Software"
                        r"\G801.2024.grupo.2.EG2\src\main\python\json_files")
    __path_data = str(r"C:\Users\inest\PycharmProjects\Desarrollo de Software"
                      r"\G801.2024.grupo.2.EG2\src\main\python\json_files")

    def setUp(self):
        """funcion setUp"""
        try:
            with open(self.__path_tests2 + r"\tests2.json", encoding='UTF-8', mode="r") as f:
                testroomreservation = json.load(f)
        except FileNotFoundError as e:
            raise hotel_management_exception("error en fichero o camino") from e
        except json.JSONDecodeError:
            testroomreservation = []
        self.__test_room_reservation = testroomreservation
        # cerramos el fichero de las reservas
        ficheroreservas = self.__path_data + r"\reservas.json"
        if os.path.isfile(ficheroreservas):
            os.remove(ficheroreservas)
        self.__test_data_f2 = [room['data'] for room in self.__test_room_reservation]

    def get_store_hash(self):
        """gets md5 hash for the stay store"""
        try:
            with open(self.__path_tests + r"\tests1.json", encoding='UTF-8', mode="r") as f:
                filehash = hashlib.md5(f.__str().encode()).hexdigest()
        except FileNotFoundError:
            filehash = ""
        return filehash

    def test_reservation_ok(self):
        """Casos de test incorrectos"""
        for index, inputdata in enumerate(self.__path_tests2):
            if index + 1 == 2:
                testid = "TC" + str(index + 1)
                with self.subTest(testid):
                    print("Executing: " + testid + ":" + inputdata)
                    self.generate_tmp_test_data_file(inputdata)
                    hm = hotel_manager()
                    roomkey = hm.guest_arrival(self.__path_tests + self.__tmp_test_data_file)
                    if testid == "TC1":
                        self.assertEqual(roomkey,
                                         ({"Localizer": "123456789ABCDEF1234567890ABCEDF1", "IdCard": "53994572A"}))

    def test_reservation_ko(self):
        """Casos de test incorrectoss"""
        for index, inputdata in enumerate(self.__test_data_f2):
            if index + 1 in [9, 12, 13, 16, 19, 20]:
                testid = "TC" + str(index + 1)
                with self.subTest(testid):
                    print("Executing: " + testid + ":" + inputdata)
                    self.generate_tmp_test_data_file(inputdata)
                    hm = hotel_manager()
                    roomkey = hm.guest_arrival(self.__path_tests + self.__tmp_test_data_file)
                    if testid == "TC11":
                        self.assertEqual(roomkey.exception.message,
                                         "Longitud del valor de la etiqueta 1 incorrecto")
                    if testid == "TC12":
                        self.assertEqual(roomkey.exception.message,
                                         "Formato del valor de la etiqueta 1 incorrecto")
                    if testid == "TC15":
                        self.assertEqual(roomkey.exception.message,
                                         "Etiqueta 2 nulo")
                    if testid == "TC18":
                        self.assertEqual(roomkey.exception.message,
                                         "Formato del valor de la etiqueta 2 incorrecto")
                    if testid == "TC19":
                        self.assertEqual(roomkey.exception.message,
                                         "Longitud del valor de la etiqueta 2 incorrecto")
                    if testid == "TC8":
                        self.assertEqual(roomkey.exception.message,
                                         "Etiqueta 1 nulo")
            else:
                testid = "TC" + str(index + 1)
                with self.subTest(testid):
                    print("Executing: " + testid + ":" + inputdata)
                    self.generate_tmp_test_data_file(inputdata)
                    hm = hotel_manager()
                    roomkey = hm.guest_arrival(self.__path_tests + self.__tmp_test_data_file)
                    self.assertEqual(roomkey.exception.message,
                                     "Formato del archivo JSON incorrecto")
