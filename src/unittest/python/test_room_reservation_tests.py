"""tests"""
import json
import os.path
from pathlib import Path
import unittest
import hashlib

from unittest import TestCase
from src.main.python.uc3m_travel.hotel_management_exception import hotel_management_exception
from src.main.python.uc3m_travel.hotel_manager import hotel_manager



class test_room_reservation(TestCase):
    """Test room reservation"""
    __path_tests = str("C:\Users\inest\PycharmProjects\Desarrollo de Software\G801.2024.grupo.2.EG2\src\main\python\test.json")
    __path_data = str("C:\Users\inest\PycharmProjects\Desarrollo de Software\G801.2024.grupo.2.EG2\src\main\python\test.json")
    def setUp(self):
        """setUp"""
        try:
            with open(self.__path_tests + "tests1.json", encoding='UTF-8', mode="r") as f:
                test_room_reservation = json.load(f)
        except FileNotFoundError as e:
            raise hotel_management_exception("error en fichero o camino") from e
        except json.JSONDecodeError:
            test_room_reservation = []
        self.__test_room_reservation = test_room_reservation

    def test_hotel_reservation_ok(self):
        """Test hotel reservation"""
        for input_data in self.__test_room_reservation:
            if input_data["id_test"] == ["TC1", "TC6", "TC8", "TC13", "TC17", "TC18", "TC19", "TC21", "TC31"]:
                hm = hotel_manager()
                localizer = hm.room_reservation(input_data["credit_card_number"], input_data["id_card"],
                                                input_data["name_surname"], input_data["phone_number"],
                                                input_data["room_type"], input_data["arrival"],
                                                input_data["num_days"])
                self.assertEqual(localizer, "d41d8cd98f00v204e9800998ecf8427e") #rellenar bien con localizador*************************************************************
            try:
                with open(self.__path_data + "/all_bookings.json", encoding='UTF-8', mode="r") as f: #ver json
                    bookings = json.load(f)
            except FileNotFoundError as e:
                raise hotel_management_exception("error en fichero o camino") from e
            except json.JSONDecodeError:
                bookings = []
            booking_found = False
            for booking in bookings:
                if booking["id_card"] == input_data["id_card"]:
                    booking_found = True
            self.assertTrue(booking_found)

    def test_hotel_reservation_ko(self):
        """Test hotel reservation"""
        for input_data in self.__test_room_reservation:
            if input_data["id_test"] not in ["TC1", "TC6", "TC8", "TC13", "TC17", "TC18", "TC19", "TC21", "TC31"]:
                with self.subTest(input_data["idTest"]):
                    hm = hotel_manager()
                    with self.assertRaises(hotel_management_exception) as result:
                        hm.room_reservation(input_data["credit_card_number"],
                                                        input_data["id_card"],
                                                        input_data["name_surname"], input_data["phone_number"],
                                                        input_data["room_type"], input_data["arrival"],
                                                        input_data["num_days"])
                        if input_data["id_test"] == "TC2":
                            self.assertEqual(result.exception.message, "Invalid credit card number provided, Luhn's algorithm")
                        elif input_data["id_test"] == "TC3":
                            self.assertEqual(result.exception.message,"Invalid credit card number provided, no letters allowed")
                        elif input_data["id_test"] == "TC4":
                            self.assertEqual(result.exception.message,"Invalid credit card number provided, long number")
                        elif input_data["id_test"] == "TC5":
                            self.assertEqual(result.exception.message,"Invalid credit card number provided, short number")
                        elif input_data["id_test"] == "TC7":
                            self.assertEqual(result.exception.message,"Invalid identification number")
                        elif input_data["id_test"] == "TC9":
                            self.assertEqual(result.exception.message,"Invalid name and surname, too short")
                        elif input_data["id_test"] == "TC10":
                            self.assertEqual(result.exception.message,"Invalid name and surname, no numbers are allowed")
                        elif input_data["id_test"] == "TC11":
                            self.assertEqual(result.exception.message,"Invalid name and surname, too long")
                        elif input_data["id_test"] == "TC12":
                            self.assertEqual(result.exception.message,"Invalid name and surname, spaces are needed")
                        elif input_data["id_test"] == "TC14":
                            self.assertEqual(result.exception.message,"Invalid phone number, contains a letter")
                        elif input_data["id_test"] == "TC15":
                            self.assertEqual(result.exception.message,"Invalid phone number, needs to be shorter")
                        elif input_data["id_test"] == "TC16":
                            self.assertEqual(result.exception.message,"Invalid phone number, needs to be longer")
                        elif input_data["id_test"] == "TC20":
                            self.assertEqual(result.exception.message,"Invalid room type, must be single, double or suite")
                        elif input_data["id_test"] == "TC22":
                            self.assertEqual(result.exception.message,"Invalid arrival date, contains letters")
                        elif input_data["id_test"] == "TC23":
                            self.assertEqual(result.exception.message,"Invalid arrival date, year not accepted")
                        elif input_data["id_test"] == "TC24":
                            self.assertEqual(result.exception.message,"Invalid arrival date, month not accepted")
                        elif input_data["id_test"] == "TC25":
                            self.assertEqual(result.exception.message,"Invalid arrival date, day not accepted")
                        elif input_data["id_test"] == "TC26":
                            self.assertEqual(result.exception.message,"Invalid arrival date, must follow DD/MM/YYYY")
                        elif input_data["id_test"] == "TC27":
                            self.assertEqual(result.exception.message,"Invalid arrival date, few digits in day")
                        elif input_data["id_test"] == "TC28":
                            self.assertEqual(result.exception.message,"Invalid arrival date, many digits in day")
                        elif input_data["id_test"] == "TC29":
                            self.assertEqual(result.exception.message,"Invalid arrival date, few digits in month")
                        elif input_data["id_test"] == "TC30":
                            self.assertEqual(result.exception.message,"Invalid arrival date, many digits in month")
                        elif input_data["id_test"] == "TC32":
                            self.assertEqual(result.exception.message,"Invalid number of days, less than 1")
                        elif input_data["id_test"] == "TC33":
                            self.assertEqual(result.exception.message,"Invalid number of days, more than 10")
                        elif input_data["id_test"] == "TC34":
                            self.assertEqual(result.exception.message,"Invalid number of days, invalid response")


                        elif input_data["id_test"] == "TC35":
                            self.assertEqual(result.exception.message,"Invalid name and surname, no leading spaces allowed")
                        elif input_data["id_test"] == "TC36":
                            self.assertEqual(result.exception.message,"Invalid name and surname, no consecutive spaces allowed")
                        elif input_data["id_test"] == "TC37":
                            self.assertEqual(result.exception.message,"Invalid name and surname, no trailing spaces allowed")
                        elif input_data["id_test"] == "TC38":
                            self.assertEqual(result.exception.message,"No more than one reservation per client")




    def localizer(self):
        return hashlib.md5(str().encode()).hexdigest()

#carmen .............................
"""TestCases - Expected NOT OK.
        for input_data in self.__test_data:
            if input_data["idTest"] not in ["TC1","TC9","TC20","TC21"]:
                with self.subTest(input_data["idTest"]):
                    print("Executing: "+ input_data["idTest"])
                    hm = HotelManager()
                    with self.assertRaises(HotelManagementException) as result:
                        hm.room_reservation(input_data["creditCardNumber"],
                                            input_data["idCard"],
                                            input_data["name Surname"],
                                            input_data["phoneNumber"],
                                            input_data["roomType"],
                                            input_data["arrival"],
                                            input_data["numDays"])
                    match input_data["idTest"]:
                        case "TC2":
                            self.assertEqual(result.exception.message,
                                             "Invalid credit card number provided, Luhn´s algorithm")
                        case "TC3":
                            self.assertEqual(result.exception.message,
                                             "Invalid credit card number provided, only numbers are allowed")
                        case "TC4":
                            self.assertEqual(result.exception.message,
                                             "Invalid credit card number provided, more than 16 numbers")
                        case "TC5":
                            self.assertEqual(result.exception.message,
                                             "Invalid credit card number provided, less than 16 numbers")
                        case "TC6":
                            self.assertEqual(result.exception.message,
                                             "Invalid identification number provided, more than 9 characters")
                        case "TC7":
                            self.assertEqual(result.exception.message,
                                             "Invalid identification number provided, less than 9 characters")
                        case "TC8":
                            self.assertEqual(result.exception.message,
                                             "Invalid identification number provided, NIF´s algorithm")
                        case "TC10":
                            self.assertEqual(result.exception.message,
                                             "Invalid name provided, less than 10 characters")
                        case "TC11":
                            self.assertEqual(result.exception.message,
                                             "Invalid name provided, more than 10 characters")
                        case "TC12":
                            self.assertEqual(result.exception.message,
                                             "Invalid name provided, only letters/whitespaces allowed")
                        case "TC13":
                            self.assertEqual(result.exception.message,
                                             "Invalid name provided, "
                                             "use whitespaces to separate the name from the surname")
                        case "TC14":
                            self.assertEqual(result.exception.message,
                                             "Invalid name provided, don´t use two consecutive whitespaces")
                        case "TC15":
                            self.assertEqual(result.exception.message,
                                             "Invalid name provided, don´t use a whitespace at the beginning")
                        case "TC16":
                            self.assertEqual(result.exception.message,
                                             "Invalid name provided, don´t use a whitespace at the end")
                        case "TC17":
                            self.assertEqual(result.exception.message,
                                             "Invalid phone number provided, more than 9 numbers")
                        case "TC18":
                            self.assertEqual(result.exception.message,
                                             "Invalid phone number provided, less than 9 numbers")
                        case "TC19":
                            self.assertEqual(result.exception.message,
                                             "Invalid phone number provided, only numbers allowed")
                        case "TC22":
                            self.assertEqual(result.exception.message,
                                             "Invalid room type provided, it must be single, double or suite")
                        case "TC23":
                            self.assertEqual(result.exception.message,
                                             "Invalid arrival date provided, it must follow the format DD/MM/YYYY")
                        case "TC24":
                            self.assertEqual(result.exception.message,
                                             "Invalid arrival date provided, "
                                             "it can´t be a date that has already passed")
                        case "TC25":
                            self.assertEqual(result.exception.message,
                                             "Invalid number of days provided, less than 2 days")
                        case "TC26":
                            self.assertEqual(result.exception.message,
                                             "Invalid number of days provided, more than 10 days")
                        case "TC27":
                            self.assertEqual(result.exception.message,
                                             "Invalid number of days provided, only numbers allowed")
                        case "TC28":
                            self.assertEqual(result.exception.message,
                                             "There can´t be more than 1 reservation per client")"""
if __name__ == '__main__':
    unittest.main()
