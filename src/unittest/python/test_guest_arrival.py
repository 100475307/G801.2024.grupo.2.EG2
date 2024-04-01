"""incluir casos de prueba de la función 2"""
from unittest import TestCase
import json
import os.path
import hashlib
from freezegun import freeze_time
from src.main.python.uc3m_travel.hotel_stay import hotel_stay
from src.main.python.uc3m_travel.hotel_manager import hotel_manager
from src.main.python.uc3m_travel.hotel_management_exception import hotel_management_exception


class test_guest_arrival(TestCase):
    """clase para los test de la función 2"""
    __path_tests = str(r"C:\Users\inest\PycharmProjects\Desarrollo de Software\G801.2024.grupo.2.EG2\src\main\python\json_files")
    __path_data = str(r"C:\Users\inest\PycharmProjects\Desarrollo de Software\G801.2024.grupo.2.EG2\src\main\python\json_files")

    def setUp(self):
        """funcion setUp"""
        jsonFilesPath = self.__path_tests
        # Path del archivo de reservas para borrarlo si existe
        fileStore = jsonFilesPath + r"\estancias.json"
        if os.path.isfile(fileStore):
            os.remove(fileStore)

    def get_store_hash(self):
        """gets md5 hash for the stay store"""
        try:
            with open(self.__path_tests + r"\reservas.json", encoding='UTF-8', mode="r") as f:
                filehash = hashlib.md5(f.__str().encode()).hexdigest()
        except FileNotFoundError:
            filehash = ""
        return filehash

    @freeze_time("2024-12-31 12:00:00")
    def test_reservation_ok(self):
        """Casos de test incorrectos"""
        index = 0
        if index + 1 == 1:
            testid = "TC" + str(index + 1)
            with self.subTest(testid):
                inputdata = r"C:\Users\inest\PycharmProjects\Desarrollo de Software\G801.2024.grupo.2.EG2\src\main\python\json_files" + r"\test2" + r"\test" + str(index+1) + r".json"
                print("Executing: " + testid + ":" + inputdata)
                ''' with open(inputdata, 'r') as archivo_prueba:
                    datos = json.load(archivo_prueba)
                print('los datos que esta comprobando son: ',datos)'''
                hm = hotel_manager()
                roomkey = hm.guest_arrival(inputdata)
                print('el room key desl test es :',roomkey)
                if testid == "TC1":

                    self.assertEqual(roomkey,
                                     "65377f12f7892239d712f2c687e5029f4133fcd7c885774da5a3e1c76fad7fbd")

    @freeze_time("2024-12-31 12:00:00")
    def test_reservation_ko(self):
        """Casos de test incorrectoss"""

        for index in range(70):
            if index + 1 in [1]:
                pass
            if index + 1 in [9, 12, 13, 16, 19, 20]:
                testid = "TC" + str(index + 1)
                inputdata = r"C:\Users\inest\PycharmProjects\Desarrollo de Software\G801.2024.grupo.2.EG2\src\main\python\json_files" + r"\test2" + r"\test" + str(
                    index + 1) + r".json"
                with self.subTest(testid):
                    print("Executing: " + testid + ":" + inputdata)
                    hm = hotel_manager()
                    print('antes de entrar a al with')
                    with self.assertRaises(hotel_management_exception) as result:
                        print('entra en el result')
                        roomkey = hm.guest_arrival(inputdata)
                        print('sale del with +++++++++++++++++++++++++++++')
                    if testid == "TC11":
                        self.assertEqual(result.exception.args[0],
                                         "Longitud del valor de la etiqueta 1 incorrecto")
                    if testid == "TC12":
                        self.assertEqual(result.exception.message,
                                         "Formato del valor de la etiqueta 1 incorrecto")
                    if testid == "TC15":
                        self.assertEqual(result.exception.message,
                                         "Etiqueta 2 nulo")
                    if testid == "TC18":
                        self.assertEqual(result.exception.message,
                                         "Formato del valor de la etiqueta 2 incorrecto")
                    if testid == "TC19":
                        self.assertEqual(result.exception.message,
                                         "Longitud del valor de la etiqueta 2 incorrecto")
                    if testid == "TC8":
                        self.assertEqual(result.exception.message,
                                         "Etiqueta 1 nulo")

            else:
                testid = "TC" + str(index + 1)
                with self.subTest(testid):
                    inputdata = r"C:\Users\inest\PycharmProjects\Desarrollo de Software\G801.2024.grupo.2.EG2\src\main\python\json_files" + r"\test2" + r"\test" + str(index + 1) + r".json"
                    print("Executing: " + testid + ":" + inputdata)
                    hm = hotel_manager()

                    with self.assertRaises(hotel_management_exception) as result:
                        print('entra en el result')
                        roomkey = hm.guest_arrival(inputdata)
                        print('sale del with del segundo caso  +++++++++++++++++++++++++++++')
                    self.assertEqual(result.exception.message,
                                     "Formato del archivo JSON incorrecto")
