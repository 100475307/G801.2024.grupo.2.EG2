"""Fichero para incluir los casos de pruebas de la funcion 1"""
import copy
import json
import os.path
from unittest import TestCase
from freezegun import freeze_time
from pathlib import Path
from datetime import datetime
from src.main.python.uc3m_travel.hotel_manager import hotel_manager
from src.main.python.uc3m_travel.hotel_management_exception import hotel_management_exception
from src.main.python.uc3m_travel.hotel_stay import hotel_stay


class test_check_out(TestCase):
    """Clase para crear los test de prueba de la funcion 1: Room Reservation"""
    __path_tests = str(
        r"C:\Users\jcamp\PycharmProjects\G801.2024.grupo.2.EG2\src\main\python\json_files")
    __path_data = str(
        r"C:\Users\jcamp\PycharmProjects\G801.2024.grupo.2.EG2\src\main\python\json_files")

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

    @freeze_time("2024-06-16")
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
                    print("entra en test1 **")
                    self.assertTrue(localizer)
                elif inputData["id_test"] == "TC8":
                    print("entra en test6 ****")
                    self.assertEqual(localizer, "d58de8fcfd3e26087ac677355c008ffd")

    @freeze_time("2024-06-16")
    def test_check_outs_ko(self):
        """TestCases - Expected NOT OK."""
        for inputData in self.__test_check_out:
            if inputData["id_test"] not in ["TC7", "TC8", "TC1"]:
                print("ENTRA EN NOT OK *****************+")
                with self.subTest(inputData["id_test"]):
                    print("Ejecutando: " + inputData["id_test"])
                    hm = hotel_manager()
                    print("id_test", inputData["id_test"])
                    with self.assertRaises(hotel_management_exception) as result:
                        print("HOLA*")
                        hm.guest_departure(inputData["room_key"])
                    if inputData["id_test"] == "TC2":
                        print("entra en test2 ****")
                        self.assertEqual(result.exception.message,
                                         "Código de habitación no cumple con el formato correcto")
                    elif inputData["id_test"] == "TC3":
                        print("entra en test3 ****")
                        self.assertEqual(result.exception.message,
                                         "La llave de la habitación no existe")
                    elif inputData["id_test"] == "TC4":
                        print("entra en test4 **")

                        @freeze_time("2024-06-01")
                        def tc14(self):
                            self.assertEqual(result.exception.message,
                                             "La fecha de salida no coincide con la de hoy")

                        tc14(self)

                    elif inputData["id_test"] == "TC5":
                        print("entra en test5 **")

                        @freeze_time("2024-08-01")
                        def tc15(self):
                            self.assertEqual(result.exception.message,
                                             "La fecha de salida no coincide con la de hoy")

                        tc15(self)
                    elif inputData["id_test"] == "TC6":
                        print("entra en test6 ****")
                        self.assertEqual(result.exception.message,
                                         "La persona ya ha hecho checkout hoy")

    def test_check_outs_ko_vacio(self):
        """TestCases - Expected NOT OK."""
        for inputData in self.__test_check_out:
            if inputData["id_test"] in ["TC1"]:
                print("ENTRA EN NOT OK *****************+")
                with self.subTest(inputData["id_test"]):
                    print("Ejecutando: " + inputData["id_test"])
                    hm = hotel_manager()
                    print("id_test", inputData["id_test"])
                    with open(self.__path_tests + r'\reservas2.json', encoding="UTF-8", mode="r") as f:
                        data = json.load(f)
                    data = copy.deepcopy(data)
                    with open(self.__path_tests + r'\reservas2.json', encoding="UTF-8", mode="w") as f:
                        json.dump("", f)
                    with self.assertRaises(hotel_management_exception) as result:
                        hm.guest_departure(inputData["room_key"])
                    with open(self.__path_tests + r'\reservas2.json', encoding="UTF-8", mode="w") as f:
                        json.dump(data, f)
                    if inputData["id_test"] == "TC1":
                        print("entra en test1 ****")
                        self.assertEqual(result.exception.message,
                                         "No hay datos de estancias")