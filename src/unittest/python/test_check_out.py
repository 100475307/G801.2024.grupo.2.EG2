"""Fichero para incluir los casos de pruebas de la funcion 1"""
import json
import os.path
from unittest import TestCase
import sys

sys.path.append(
    r'C:\Users\inest\PycharmProjects\Desarrollo de Software\G801.2024.grupo.2.EG2\src\main\python\uc3m_travel')

from src.main.python.uc3m_travel.hotel_manager import hotel_manager
from src.main.python.uc3m_travel.hotel_management_exception import hotel_management_exception
from src.main.python.uc3m_travel.hotel_stay import hotel_stay


class test_check_out(TestCase):
    """Clase para crear los test de prueba de la funcion 1: Room Reservation"""
    __path_tests = str(
        r"C:\Users\inest\PycharmProjects\Desarrollo de Software"
        r"\G801.2024.grupo.2.EG2\src\main\python\json_files")
    __path_data = str(
        r"C:\Users\inest\PycharmProjects\Desarrollo de Software"
        r"\G801.2024.grupo.2.EG2\src\main\python\json_files")

    @classmethod
    def setUp(cls):
        """función setUp"""
        try:
            with open(cls.__path_tests + r"\tests3.json",
                      encoding='UTF-8', mode='r') as f:
                testscheckout = json.load(f)
        except FileNotFoundError as e:
            raise hotel_management_exception("Wrong file or file path") from e
        except json.JSONDecodeError:
            testscheckout = []
        cls.__test_check_out = testscheckout
        # cerramos el fichero de checkouts
        ficherocheckout = cls.__path_data + r"/checkouts.json"
        if os.path.isfile(ficherocheckout):
            os.remove(ficherocheckout)

    def test_check_outs_ok(self):
        """Tests función 1 que se esperan correctos"""
        for inputData in self.__test_check_out:
            if inputData["id_test"] in ["TC7", "TC8"]:
                with self.subTest(inputData["id_test"]):
                    print("Ejecutando: " + inputData["id_test"])
                hm = hotel_manager()
                localizer = hm.guest_departure(inputData["room_key"])
                # print (localizer)
                if inputData["id_test"] == "TC7":
                    print("entra en test1 ****")
                    self.assertEqual(localizer, "57d92f8f3073e778b64570f1db3007da")
                elif inputData["id_test"] == "TC8":
                    print("entra en test6 ****")
                    self.assertEqual(localizer, "d58de8fcfd3e26087ac677355c008ffd")

                try:
                    with open(self.__path_data + r"\checkouts.json", encoding='UTF-8', mode='r') as f:
                        checkout = json.load(f)
                except FileNotFoundError as e:
                    raise hotel_management_exception("error en fichero o camino") from e
                except json.JSONDecodeError:
                    checkout = []
                encontradocheckout = False
                if not isinstance(checkout, list):
                    # solucionar error si no se trata de una lista de diccionarios
                    checkout = [checkout]
                for c in checkout:
                    if c["room_key"] == inputData["room_key"]:
                        encontradocheckout = True
                self.assertTrue(encontradocheckout)

    def test_check_outs_ko(self):
        """TestCases - Expected NOT OK."""
        for inputData in self.__test_check_out:
            if inputData["id_test"] not in ["TC7", "TC8"]:
                print("ENTRA EN NOT OK *****************+")
                with self.subTest(inputData["id_test"]):
                    print("Ejecutando: " + inputData["id_test"])
                    hm = hotel_manager()
                    print("id_test", inputData["id_test"])
                    with self.assertRaises(hotel_management_exception) as result:
                        print("HOLA*****************")
                        hm.guest_departure(inputData["room_key"])
                        print("room_key", inputData["room_key"], "departure", inputData["departure"])
                        if inputData["id_test"] == "TC1":
                            print("entra en test1 ****")
                            self.assertEqual(result.exception.message,
                                             "No hay datos de estancias")
                        elif inputData["id_test"] == "TC2":
                            print("entra en test2 ****")
                            self.assertEqual(result.exception.message,
                                             "Código de habitación no cumple con el formato correcto")
                        elif inputData["id_test"] == "TC3":
                            print("entra en test3 ****")
                            self.assertEqual(result.exception.message,
                                             "La llave de la habitación no existe")
                        elif inputData["id_test"] == "TC4":
                            print("entra en test4 ****")
                            self.assertEqual(result.exception.message,
                                             "La fecha de salida no coincide con la de hoy")
                        elif inputData["id_test"] == "TC5":
                            print("entra en test5 ****")
                            self.assertEqual(result.exception.message,
                                             "La fecha de salida no coincide con la de hoy")
                        elif inputData["id_test"] == "TC6":
                            print("entra en test6 ****")
                            self.assertEqual(result.exception.message,
                                             "La persona ya ha hecho checkout hoy")


    def test_guest_departure(self, mock_datetime):
        # definimos la fecha de entrada
        mock_datetime.utcnow.return_value = datetime(2020, 12, 1)
        # definimos la fecha de salida
        mock_datetime.timestamp.return_value = 1606780800
        # creamos una instancia de hotel_manager
        hm = hotel_manager()
        # creamos una instancia de hotel_stay y le damos los datos del primer caso de prueba del
        # fichero hotel_stays.json, leido en setUp() como file
        try:
            with open(cls.__path_tests, "r") as file:
                cls.data = json.load(file)
        except FileNotFoundError:
            print("File not found")
        hs1 = hotel_stay(cls.data[0]["id_card"], cls.data[0]["localizer"],
                         cls.data[0]["num_days"], cls.data[0]["room_type"])
        hs2 = hotel_stay(cls.data[1]["id_card"], cls.data[1]["localizer"],
                         cls.data[1]["num_days"], cls.data[1]["room_type"])

        # probamos para los dos, la función guest_departure(room_key) con la room_key correcta
        # y comprobamos que la salida es la esperada
        self.assertEqual(hm.guest_departure(hs1.room_key), "OK")
        self.assertEqual(hm.guest_departure(hs2.room_key), "ERROR")


if _name_ == '_main_':
    unittest.main()