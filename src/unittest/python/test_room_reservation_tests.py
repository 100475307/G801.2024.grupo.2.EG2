"""Fichero para incluir los casos de pruebas"""
import json
import os.path
from unittest import TestCase
import sys
sys.path.append(r'C:\Users\ghija\PycharmProjects\G801.2024.grupo.2.EG2\src\main\python\uc3m_travel')

from hotel_manager import hotel_manager
from hotel_management_exception import hotel_management_exception


class TestRoomReservation(TestCase):
    """Clase para crear los test de prueba de la funcion 1: Room Reservation"""
    __path_tests = str(r"C:\Users\ghija\PycharmProjects"
                       r"\G801.2024.grupo.2.EG2\src\main\python\json_files")
    __path_data = str(r"C:\Users\ghija\PycharmProjects"
                      r"\G801.2024.grupo.2.EG2\src\main\python\json_files")
    @classmethod
    def setUpClass(cls):
        try:
            with open(cls.__path_tests + r"\tests1.json",
                      encoding='UTF-8', mode='r') as f:
                test_data = json.load(f)
        except FileNotFoundError as e:
            raise hotel_management_exception("Wrong file or file path") from e
        except json.JSONDecodeError:
            test_data = []
        cls.__test_data = test_data
        #Cerramos fichero reservas para comprobar que se crea correctamente
        file_booking = cls.__path_data + r"/reservas.json"
        if os.path.isfile(file_booking):
            os.remove(file_booking)

    def testPruebas1OK(self):
        """TestCase: TC1 - Expected OK"""
        for input_data in self.__test_data:
            if input_data["id_test"] in ["TC1","TC9","TC20","TC21"]:
                with self.subTest(input_data["id_test"]):
                    print("Executing: " + input_data["id_test"])
                    hm = hotel_manager()
                localizer = hm.room_reservation(input_data["credit_card_number"],
                                                input_data["id_card"],
                                                input_data["name_and_surname"],
                                                input_data["phone_number"],
                                                input_data["room_type"],
                                                input_data["arrival"],
                                                input_data["num_days"])
                if input_data["id_test"] == "TC1":
                    print("entra en test1 **********************************")
                    self.assertEqual(localizer, "43d9d717214b9f6858bd2b55be901645")
                if input_data["id_test"] == "TC9":
                    self.assertEqual(localizer, "54cca441cb9f3b3194a55e1750adee53")
                if input_data["id_test"] == "TC20":
                    self.assertEqual(localizer, "764201ba1928e25e5358a31d941df35c")
                if input_data["id_test"] == "TC21":
                    self.assertEqual(localizer, "058c33c4ee931eb831db4adc8617307b")
                try:
                    with open(self.__path_data + r"\reservas.json",
                              encoding= 'UTF-8', mode='r') as f:
                        bookings = json.load(f)
                except FileNotFoundError as e:
                    raise hotel_management_exception("Fichero reservas no generado") from e
                except json.JSONDecodeError:
                    bookings = []
                booking_found = False
                if not isinstance(bookings, list):
                    # If bookings is not a list,
                    # make it a list that contains one dictionary
                    bookings = [bookings]
                for booking in bookings:
                    if booking["id_card"] == input_data["id_card"]:
                        booking_found = True
                self.assertTrue(booking_found)


    def testPruebas2KO(self):
        """TestCases - Expected NOT OK."""
        for input_data in self.__test_data:
            if input_data["id_test"] not in ["TC1","TC9","TC20","TC21"]:
                with self.subTest(input_data["id_test"]):
                    print("Executing: " + input_data["id_test"])
                    hm = hotel_manager()
                    with self.assertRaises(hotel_management_exception) as result:
                        hm.room_reservation(input_data["credit_card_number"],
                                                input_data["id_card"],
                                                input_data["name_and_surname"],
                                                input_data["phone_number"],
                                                input_data["room_type"],
                                                input_data["arrival"],
                                                input_data["num_days"])
                        if input_data["id_test"] == "TC2":
                            self.assertEqual(result.exception.message,
                                                "Invalid credit card number provided, "
                                                "Luhn´s algorithm")
                        if input_data["id_test"] == "TC3":

                            self.assertEqual(result.exception.message,
                                                "Invalid credit card number provided, "
                                                "only numbers are allowed")
                        if input_data["id_test"] == "TC4":

                            self.assertEqual(result.exception.message,
                                                "Invalid credit card number provided, "
                                                "more than 16 numbers")
                        if input_data["id_test"] == "TC5":

                            self.assertEqual(result.exception.message,
                                                "Invalid credit card number provided, "
                                                "less than 16 numbers")
                        if input_data["id_test"] == "TC6":

                            self.assertEqual(result.exception.message,
                                                "Invalid identification number provided, "
                                                "more than 9 characters")
                        if input_data["id_test"] == "TC7":

                            self.assertEqual(result.exception.message,
                                                "Invalid identification number provided, "
                                                "less than 9 characters")
                        if input_data["id_test"] == "TC8":

                            self.assertEqual(result.exception.message,
                                                "Invalid identification number provided, "
                                                "NIF´s algorithm")
                        if input_data["id_test"] == "TC10":

                            self.assertEqual(result.exception.message,
                                                "Invalid name provided, "
                                                "less than 10 characters")
                        if input_data["id_test"] == "TC11":

                            self.assertEqual(result.exception.message,
                                                "Invalid name provided, "
                                                "more than 50 characters")
                        if input_data["id_test"] == "TC12":

                            self.assertEqual(result.exception.message,
                                                "Invalid name provided, "
                                                "only letters/whitespaces allowed")
                        if input_data["id_test"] == "TC13":

                            self.assertEqual(result.exception.message,
                                                "Invalid name provided, "
                                                "use whitespaces to separate "
                                                "the name from the surname")
                        if input_data["id_test"] == "TC14":

                            self.assertEqual(result.exception.message,
                                                "Invalid name provided, "
                                                "don´t use two consecutive whitespaces")
                        if input_data["id_test"] == "TC15":

                            self.assertEqual(result.exception.message,
                                                "Invalid name provided, "
                                                "don´t use a whitespace at the beginning")
                        if input_data["id_test"] == "TC16":

                            self.assertEqual(result.exception.message,
                                                "Invalid name provided, "
                                                "don´t use a whitespace at the end")
                        if input_data["id_test"] == "TC17":

                            self.assertEqual(result.exception.message,
                                                "Invalid phone number provided, "
                                                "more than 9 numbers")
                        if input_data["id_test"] == "TC18":

                            self.assertEqual(result.exception.message,
                                                "Invalid phone number provided, "
                                                "less than 9 numbers")
                        if input_data["id_test"] == "TC19":

                            self.assertEqual(result.exception.message,
                                                "Invalid phone number provided, "
                                                "only numbers allowed")
                        if input_data["id_test"] == "TC22":

                            self.assertEqual(result.exception.message,
                                                "Invalid room type provided, "
                                                "it must be SINGLE, DOUBLE or SUITE")
                        if input_data["id_test"] == "TC23":

                            self.assertEqual(result.exception.message,
                                                "Invalid arrival date provided, "
                                                "it must follow the format DD/MM/YYYY")
                        if input_data["id_test"] == "TC24":
                            self.assertEqual(result.exception.message,
                                                "Invalid arrival date provided, "
                                                "it can´t be a date that has already passed")
                        if input_data["id_test"] == "TC25":

                            self.assertEqual(result.exception.message,
                                                "Invalid number of days provided, "
                                                "less than 1 day")
                        if input_data["id_test"] == "TC26":

                            self.assertEqual(result.exception.message,
                                                "Invalid number of days provided, "
                                                "more than 10 days")
                        if input_data["id_test"] == "TC27":

                            self.assertEqual(result.exception.message,
                                                "Invalid number of days provided, "
                                                "only numbers allowed")
                        if input_data["id_test"] == "TC28":

                            self.assertEqual(result.exception.message,
                                                "There can´t be more "
                                                "than 1 reservation per client")
                        if input_data["id_test"] == "TC29":
                            self.assertEqual(result.exception.message,
                                                "Invalid arrival date provided, "
                                                "the day must be bigger than 0")
                        if input_data["id_test"] == "TC30":

                            self.assertEqual(result.exception.message,
                                                "Invalid arrival date provided, "
                                                "the day must be smaller than 32")
                        if input_data["id_test"] == "TC31":

                            self.assertEqual(result.exception.message,
                                                "Invalid arrival date provided, "
                                                "the day must be smaller "
                                                "than 31 for this month")
                        if input_data["id_test"] == "TC32":

                            self.assertEqual(result.exception.message,
                                                "Invalid arrival date provided, "
                                                "the day must be smaller "
                                                "than 29 for February this year")
                        if input_data["id_test"] == "TC33":

                            self.assertEqual(result.exception.message,
                                                "Invalid arrival date provided, "
                                                "the day must be smaller "
                                                "than 30 for February this year")
                        if input_data["id_test"] == "TC34":

                            self.assertEqual(result.exception.message,
                                                "Invalid arrival date provided, "
                                                "the month must be bigger than 0")
                        if input_data["id_test"] == "TC35":

                            self.assertEqual(result.exception.message,
                                                "Invalid arrival date provided, "
                                                "the month must be smaller than 13")
