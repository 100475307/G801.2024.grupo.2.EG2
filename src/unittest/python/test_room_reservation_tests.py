"""tests"""
import json
import os.path
from pathlib import Path
import unittest
from unittest import TestCase
from src.main.python.uc3m_travel import hotel_management_exception as hme
from src.main.python.uc3m_travel import hotel_manager as hm


class test_room_reservation(TestCase):
    """clase para crear los test de prueba de la función 1"""
    __path_tests = str(r"C:\Users\inest\PycharmProjects\Desarrollo de Software"
                       r"\G801.2024.grupo.2.EG2\src\main\python\uc3m_travel\json_files")
    __path_data = str(r"C:\Users\inest\PycharmProjects\Desarrollo de Software"
                      r"\G801.2024.grupo.2.EG2\src\main\python\uc3m_travel\json_files")

    def setUp(self):
        """funcion setUp"""
        try:
            with open(self.__path_tests + r"\tests1.json", encoding='UTF-8', mode="r") as f:
                testroomreservation = json.load(f)
        except FileNotFoundError as e:
            raise hme.hotel_management_exception("error en fichero o camino") from e
        except json.JSONDecodeError:
            testroomreservation = []
        self.__test_room_reservation = testroomreservation
        #cerramos el fichero de las reservas
        fichero_reservas = self.__path_data + r"\reservas.json"
        if os.path.isfile(fichero_reservas):
            os.remove(fichero_reservas)

    def test_reservation_ok(self):
        """Tests función 1 que se esperan correctos"""
        for inputData in self.__test_room_reservation:
            if inputData["id_test"] == ["TC1", "TC6", "TC8", "TC13", "TC17", "TC18", "TC19", "TC21", "TC31"]:
                #hm = hotel_manager()
                localizer = hm.room_reservation(inputData["credit_card_number"], inputData["id_card"],
                                                inputData["name_surname"], inputData["phone_number"],
                                                inputData["room_type"], inputData["arrival"],
                                                inputData["num_days"])
                print(localizer)
                if inputData["id_test"] == "TC1":
                    self.assertEqual(localizer, "d41d8cd98f00v204e9800998ecf8427e") #rellenar
                if inputData["id_test"] == "TC6":
                    self.assertEqual(localizer, "d41d8cd98f00v204e9800998ecf8427e") #rellenar bien *******
                if inputData["id_test"] == "TC8":
                    self.assertEqual(localizer, "d41d8cd98f00v204e9800998ecf8427e") #rellenar bien *******
                if inputData["id_test"] == "TC13":
                    self.assertEqual(localizer, "d41d8cd98f00v204e9800998ecf8427e") #rellenar bien *******
                if inputData["id_test"] == "TC17":
                    self.assertEqual(localizer, "d41d8cd98f00v204e9800998ecf8427e") #rellenar bien *******
                if inputData["id_test"] == "TC18":
                    self.assertEqual(localizer, "d41d8cd98f00v204e9800998ecf8427e") #rellenar bien *******
                if inputData["id_test"] == "TC9":
                    self.assertEqual(localizer, "d41d8cd98f00v204e9800998ecf8427e") #rellenar bien *******
                if inputData["id_test"] == "TC21":
                    self.assertEqual(localizer, "d41d8cd98f00v204e9800998ecf8427e") #rellenar bien *******
                if inputData["id_test"] == "TC31":
                    self.assertEqual(localizer, "d41d8cd98f00v204e9800998ecf8427e") #rellenar bien *******
            try:
                with open(self.__path_data + r"\reservas.json", encoding='UTF-8', mode="r") as f: #ver json
                    bookings = json.load(f)
            except FileNotFoundError as e:
                raise hme.hotel_management_exception("error en fichero o camino") from e
            except json.JSONDecodeError:
                bookings = []
            bookingfound = False
            for booking in bookings:
                if booking["id_card"] == inputData["id_card"]:
                    bookingfound = True
            self.assertTrue(bookingfound)

    def test_reservation_ko(self):
        """Tests función 1 que se esperan not ok"""
        for inputData in self.__test_room_reservation:
            if inputData["id_test"] not in ["TC1", "TC6", "TC8", "TC13", "TC17", "TC18", "TC19", "TC21", "TC31"]:
                with self.subTest(inputData["id_test"]):
                    #hm = hotel_manager()
                    with self.assertRaises(hme.hotel_management_exception) as result:
                        hm.room_reservation(inputData["credit_card_number"], inputData["id_card"],
                                                        inputData["name_surname"], inputData["phone_number"],
                                                        inputData["room_type"], inputData["arrival"],
                                                        inputData["num_days"])
                        if inputData["id_test"] == "TC2":
                            self.assertEqual(result.exception.message, "Invalid credit card number provided, Luhn's algorithm")
                        elif inputData["id_test"] == "TC3":
                            self.assertEqual(result.exception.message, "Invalid credit card number provided, no letters allowed")
                        elif inputData["id_test"] == "TC4":
                            self.assertEqual(result.exception.message, "Invalid credit card number provided, long number")
                        elif inputData["id_test"] == "TC5":
                            self.assertEqual(result.exception.message, "Invalid credit card number provided, short number")
                        elif inputData["id_test"] == "TC7":
                            self.assertEqual(result.exception.message, "Invalid identification number")
                        elif inputData["id_test"] == "TC9":
                            self.assertEqual(result.exception.message, "Invalid name and surname, too short")
                        elif inputData["id_test"] == "TC10":
                            self.assertEqual(result.exception.message, "Invalid name and surname, no numbers are allowed")
                        elif inputData["id_test"] == "TC11":
                            self.assertEqual(result.exception.message, "Invalid name and surname, too long")
                        elif inputData["id_test"] == "TC12":
                            self.assertEqual(result.exception.message, "Invalid name and surname, spaces are needed")
                        elif inputData["id_test"] == "TC14":
                            self.assertEqual(result.exception.message, "Invalid phone number, contains a letter")
                        elif inputData["id_test"] == "TC15":
                            self.assertEqual(result.exception.message, "Invalid phone number, needs to be shorter")
                        elif inputData["id_test"] == "TC16":
                            self.assertEqual(result.exception.message, "Invalid phone number, needs to be longer")
                        elif inputData["id_test"] == "TC20":
                            self.assertEqual(result.exception.message, "Invalid room type, must be single, double or suite")
                        elif inputData["id_test"] == "TC22":
                            self.assertEqual(result.exception.message, "Invalid arrival date, contains letters")
                        elif inputData["id_test"] == "TC23":
                            self.assertEqual(result.exception.message, "Invalid arrival date, year not accepted")
                        elif inputData["id_test"] == "TC24":
                            self.assertEqual(result.exception.message, "Invalid arrival date, month not accepted")
                        elif inputData["id_test"] == "TC25":
                            self.assertEqual(result.exception.message, "Invalid arrival date, day not accepted")
                        elif inputData["id_test"] == "TC26":
                            self.assertEqual(result.exception.message, "Invalid arrival date, must follow DD/MM/YYYY")
                        elif inputData["id_test"] == "TC27":
                            self.assertEqual(result.exception.message, "Invalid arrival date, few digits in day")
                        elif inputData["id_test"] == "TC28":
                            self.assertEqual(result.exception.message, "Invalid arrival date, many digits in day")
                        elif inputData["id_test"] == "TC29":
                            self.assertEqual(result.exception.message, "Invalid arrival date, few digits in month")
                        elif inputData["id_test"] == "TC30":
                            self.assertEqual(result.exception.message, "Invalid arrival date, many digits in month")
                        elif inputData["id_test"] == "TC32":
                            self.assertEqual(result.exception.message, "Invalid number of days, less than 1")
                        elif inputData["id_test"] == "TC33":
                            self.assertEqual(result.exception.message, "Invalid number of days, more than 10")
                        elif inputData["id_test"] == "TC34":
                            self.assertEqual(result.exception.message, "Invalid number of days, invalid response")
#a partir de aquí no seee
                        elif inputData["id_test"] == "TC35":
                            self.assertEqual(result.exception.message, "Invalid name and surname, no leading spaces allowed")
                        elif inputData["id_test"] == "TC36":
                            self.assertEqual(result.exception.message, "Invalid name and surname, no consecutive spaces allowed")
                        elif inputData["id_test"] == "TC37":
                            self.assertEqual(result.exception.message, "Invalid name and surname, no trailing spaces allowed")
                        elif inputData["id_test"] == "TC38":
                            self.assertEqual(result.exception.message, "No more than one reservation per client")

if __name__ == '__main__':
    unittest.main()

