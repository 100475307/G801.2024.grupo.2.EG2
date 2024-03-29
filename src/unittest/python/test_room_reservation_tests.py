"""Fichero para incluir los casos de pruebas"""
import json
import os.path
from unittest import TestCase
import sys

sys.path.append(
    r'C:\Users\jcamp\PycharmProjects\G801.2024.grupo.2.EG2\src\main\python\uc3m_travel')

from hotel_manager import hotel_manager
from hotel_management_exception import hotel_management_exception


class TestRoomReservation(TestCase):
    """Clase para crear los test de prueba de la funcion 1: Room Reservation"""
    __path_tests = str(
        r"C:\Users\jcamp\PycharmProjects\G801.2024.grupo.2.EG2\src\main\python\json_files")
    __path_data = str(
        r"C:\Users\jcamp\PycharmProjects\G801.2024.grupo.2.EG2\src\main\python\json_files")

    @classmethod
    def setUp(cls):
        """función setUp"""
        try:
            with open(cls.__path_tests + r"\tests1.json",
                      encoding='UTF-8', mode='r') as f:
                testroomreservation = json.load(f)
        except FileNotFoundError as e:
            raise hotel_management_exception("Wrong file or file path") from e
        except json.JSONDecodeError:
            testroomreservation = []
        cls.__test_room_reservation = testroomreservation
        # cerramos el fichero de reservas
        fichero_reservas = cls.__path_data + r"/reservas.json"
        if os.path.isfile(fichero_reservas):
            os.remove(fichero_reservas)

    def test_reservation_ok(self):
        """Tests función 1 que se esperan correctos"""
        for inputData in self.__test_room_reservation:
            if inputData["id_test"] in ["TC1", "TC6", "TC8", "TC13", "TC17", "TC18", "TC21", "TC31"]:
                with self.subTest(inputData["id_test"]):
                    print("Ejecutando: " + inputData["id_test"])
                hm = hotel_manager()
                localizer = hm.room_reservation(inputData["credit_card_number"],
                                                inputData["id_card"],
                                                inputData["name_and_surname"],
                                                inputData["phone_number"],
                                                inputData["room_type"],
                                                inputData["arrival"],
                                                inputData["num_days"])
                # print (localizer)
                if inputData["id_test"] == "TC1":
                    print("entra en test1 ****")
                    self.assertEqual(localizer, "bb8663219e19cc5c0f02415ddceca060")
                elif inputData["id_test"] == "TC6":
                    print("entra en test9 ****")
                    self.assertEqual(localizer, "54cca441cb9f3b3194a55e1750adee53")
                elif inputData["id_test"] == "TC8":
                    print("entra en test20 ****")
                    self.assertEqual(localizer, "764201ba1928e25e5358a31d941df35c")
                elif inputData["id_test"] == "TC13":
                    print("entra en test21 ****")
                    self.assertEqual(localizer, "058c33c4ee931eb831db4adc8617307b")
                elif inputData["id_test"] == "TC17":
                    print("entra en test21 ****")
                    self.assertEqual(localizer, "058c33c4ee931eb831db4adc8617307b")
                elif inputData["id_test"] == "TC18":
                    print("entra en test21 ****")
                    self.assertEqual(localizer, "058c33c4ee931eb831db4adc8617307b")
                elif inputData["id_test"] == "TC19":
                    print("entra en test21 ****")
                    self.assertEqual(localizer, "058c33c4ee931eb831db4adc8617307b")
                elif inputData["id_test"] == "TC21":
                    print("entra en test21 ****")
                    self.assertEqual(localizer, "058c33c4ee931eb831db4adc8617307b")
                elif inputData["id_test"] == "TC31":
                    print("entra en test21 ****")
                    self.assertEqual(localizer, "058c33c4ee931eb831db4adc8617307b")

                try:
                    with open(self.__path_data + r"\reservas.json", encoding='UTF-8', mode='r') as f:
                        bookings = json.load(f)
                except FileNotFoundError as e:
                    raise hotel_management_exception("error en fichero o camino") from e
                except json.JSONDecodeError:
                    bookings = []
                bookingfound = False
                if not isinstance(bookings, list):
                    # solucionar error si no se trata de una lista de diccionarios
                    bookings = [bookings]
                for booking in bookings:
                    if booking["id_card"] == inputData["id_card"]:
                        bookingfound = True
                self.assertTrue(bookingfound)

    def testPruebas2KO(self):
        """TestCases - Expected NOT OK."""
        for inputData in self.__test_room_reservation:
            if inputData["id_test"] not in ["TC1", "TC6", "TC8", "TC13", "TC17", "TC18", "TC21", "TC31"]:
                with self.subTest(inputData["id_test"]):
                    print("Ejecutando: " + inputData["id_test"])
                    hm = hotel_manager()
                    with self.assertRaises(hotel_management_exception) as result:
                        hm.room_reservation(inputData["credit_card_number"],
                                            inputData["id_card"],
                                            inputData["name_and_surname"],
                                            inputData["phone_number"],
                                            inputData["room_type"],
                                            inputData["arrival"],
                                            inputData["num_days"])
                        if inputData["id_test"] == "TC2":
                            self.assertEqual(result.exception.message,
                                             "Tarjeta erronea. No cumple con el algoritmo de Luhn")
                        elif inputData["id_test"] == "TC3":
                            self.assertEqual(result.exception.message,
                                             "Tarjeta erronea. Contiene letras")
                        elif inputData["id_test"] == "TC4":
                            self.assertEqual(result.exception.message,
                                             "Tarjeta erronea. Más de 16 dígitos")
                        elif inputData["id_test"] == "TC5":
                            self.assertEqual(result.exception.message,
                                             "Tarjeta erronea. Menos de 16 dígitos")
                        elif inputData["id_test"] == "TC7":
                            self.assertEqual(result.exception.message,
                                             "DNI erróneo")
                        elif inputData["id_test"] == "TC9":
                            self.assertEqual(result.exception.message,
                                             "Nombre y/o apellido erróneos. Menos de 10 caracteres")
                        elif inputData["id_test"] == "TC10":
                            self.assertEqual(result.exception.message,
                                             "Tarjeta erronea. Contiene letras")
                        elif inputData["id_test"] == "TC11":
                            self.assertEqual(result.exception.message,
                                             "Nombre y/o apellido erróneos. Más de 50 caracteres")
                        elif inputData["id_test"] == "TC12":
                            self.assertEqual(result.exception.message,
                                             "Nombre y apellidos erroneos. Tiene que tener al menos un nombre y un apellido")
                        elif inputData["id_test"] == "TC14":
                            self.assertEqual(result.exception.message,
                                             "Número de teléfono erróneo. Contiene letras")
                        elif inputData["id_test"] == "TC15":
                            self.assertEqual(result.exception.message,
                                             "Número de teléfono erróneo. Más de 9 números")
                        elif inputData["id_test"] == "TC16":
                            self.assertEqual(result.exception.message,
                                             "Número de teléfono erróneo. Menos de 9 números")
                        elif inputData["id_test"] == "TC20":
                            self.assertEqual(result.exception.message,
                                             "Tipo de habitación errónea")
                        elif inputData["id_test"] == "TC22":
                            self.assertEqual(result.exception.message,
                                             "Fecha de llegada errónea")
                        elif inputData["id_test"] == "TC23":
                            self.assertEqual(result.exception.message,
                                             "Fecha de llegada errónea")
                        elif inputData["id_test"] == "TC24":
                            self.assertEqual(result.exception.message,
                                             "Fecha de llegada errónea")
                        elif inputData["id_test"] == "TC25":
                            self.assertEqual(result.exception.message,
                                             "Fecha de llegada errónea")
                        elif inputData["id_test"] == "TC26":
                            self.assertEqual(result.exception.message,
                                             "Fecha de llegada errónea")
                        elif inputData["id_test"] == "TC27":
                            self.assertEqual(result.exception.message,
                                             "Fecha de llegada errónea")
                        elif inputData["id_test"] == "TC28":
                            self.assertEqual(result.exception.message,
                                             "Fecha de llegada errónea")
                        elif inputData["id_test"] == "TC29":
                            self.assertEqual(result.exception.message,
                                             "Fecha de llegada errónea")
                        elif inputData["id_test"] == "TC30":
                            self.assertEqual(result.exception.message,
                                             "Fecha de llegada errónea")
                        elif inputData["id_test"] == "TC32":
                            self.assertEqual(result.exception.message,
                                             "Número de días no válido")
                        elif inputData["id_test"] == "TC33":
                            self.assertEqual(result.exception.message,
                                             "Número de días no válido")
                        elif inputData["id_test"] == "TC34":
                            self.assertEqual(result.exception.message,
                                             "Número de días no válido")
                        elif inputData["id_test"] == "TC35":
                            self.assertEqual(result.exception.message,
                                             "Nombre y/o apellido erróneos. No puede usar dos espacios consecutivos")
                        elif inputData["id_test"] == "TC36":
                            self.assertEqual(result.exception.message,
                                             "Nombre y/o apellido erróneos. No puede empezar ni terminar por espacio")
                        elif inputData["id_test"] == "TC37":
                            self.assertEqual(result.exception.message, "Invalid name and surname, no trailing spaces allowed")
                        elif inputData["id_test"] == "TC38":
                            self.assertEqual(result.exception.message, "No more than one reservation per client")