"""incluir casos de prueba de la función 2"""
from unittest import TestCase
import json
import os.path
import hashlib
from freezegun import freeze_time
import sys

sys.path.append(r'C:\Users\jcamp\PycharmProjects\G801.2024.grupo.2.EG2\src\main\python\uc3m_travel')
from hotel_stay import hotel_stay
from hotel_manager import hotel_manager
from hotel_management_exception import hotel_management_exception


class test_guest_arrival(TestCase):
    """clase para los test de la función 2"""
    __path_tests = str(r"C:\Users\jcamp\PycharmProjects\G801.2024.grupo.2.EG2\src\main\python\json_files")
    __path_data = str(r"C:\Users\jcamp\PycharmProjects\G801.2024.grupo.2.EG2\src\main\python\json_files")

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

    @freeze_time("2024-06-16")
    def test_reservation_ok(self):
        """Casos de test incorrectos"""
        index = 0
        if index + 1 == 1:
            testid = "TC" + str(index + 1)
            with self.subTest(testid):
                inputdata = r"C:\Users\jcamp\PycharmProjects\G801.2024.grupo.2.EG2\src\main\python\json_files" + r"\test2" + r"\test" + str(index+1) + r".json"
                print("Executing: " + testid + ":" + inputdata)
                with open(inputdata, 'r') as archivo_prueba:
                    datos = json.load(archivo_prueba)
                print('los datos que esta comprobando son: ',datos)
                hm = hotel_manager()
                roomkey = hm.guest_arrival(inputdata)
                print('el room key desl test es :', roomkey)
                if testid == "TC1":
                    self.assertEqual(roomkey,
                                     "f3ca36cc66ed95a19b8ed0786ee5dc64348e8d84a812fb0d54f07419d95487bf")

    @freeze_time("2024-06-16")
    def test_reservation_ko(self):
        """Casos de test incorrectoss"""

        for index in range(70):
            if index + 1 in [1]:
                pass
            elif index + 1 in [8, 11, 12, 15, 18, 19, 21, 25, 49, 50, 55, 56, 61, 62, 67, 68]:
                testid = "TC" + str(index + 1)
                inputdata = r"C:\Users\jcamp\PycharmProjects\G801.2024.grupo.2.EG2\src\main\python\json_files" + r"\test2" + r"\test" + str(
                    index + 1) + r".json"
                with self.subTest(testid):
                    print("Executing: " + testid + ":" + inputdata)
                    hm = hotel_manager()
                    print('antes de entrar a al with')
                    with self.assertRaises(hotel_management_exception) as result:
                        print('entra en el result')
                        roomkey = hm.guest_arrival(inputdata)
                        print('sale del with +++++++++++++++++++++++++++++')
                    if testid == "TC8":
                        self.assertEqual(result.exception.message,
                                         "Hay un fallo de escritura en alguna de las claves")
                    if testid == "TC11":
                        self.assertEqual(result.exception.args[0],
                                         "Longitud del valor de la etiqueta 1 incorrecto")
                    if testid == "TC12":
                        self.assertEqual(result.exception.message,
                                         "Formato del valor de la etiqueta 1 incorrecto")
                    if testid == "TC15":
                        self.assertEqual(result.exception.message,
                                         "Hay un fallo de escritura en alguna de las claves")
                    if testid == "TC18":
                        self.assertEqual(result.exception.message,
                                         "Los primeros 8 caracteres del campo 'IdCard' deben ser números y el último una letra.")
                    if testid == "TC19":
                        self.assertEqual(result.exception.message,
                                         "Longitud del valor de la etiqueta 2 incorrecto")
                    if testid == "TC21":
                        self.assertEqual(result.exception.message,
                                         "El fichero de reservas está vacío")
                    if testid == "TC25":
                        self.assertEqual(result.exception.message,
                                         "El archivo está vacío")
                    if testid == "TC49":
                        self.assertEqual(result.exception.message,
                                         "Hay un fallo de escritura en alguna de las claves")
                    if testid == "TC50":
                        self.assertEqual(result.exception.message,
                                         "Hay un fallo de escritura en alguna de las claves")
                    if testid == "TC55":
                        self.assertEqual(result.exception.message,
                                         "Valor etiqueta 1 nulo")
                    if testid == "TC56":
                        self.assertEqual(result.exception.message,
                                         "Longitud del valor de la etiqueta 1 incorrecto")
                    if testid == "TC61":
                        self.assertEqual(result.exception.message,
                                         "Hay un fallo de escritura en alguna de las claves")
                    if testid == "TC62":
                        self.assertEqual(result.exception.message,
                                         "Hay un fallo de escritura en alguna de las claves")
                    if testid == "TC67":
                        self.assertEqual(result.exception.message,
                                         "Valor etiqueta 2 nulo")
                    if testid == "TC68":
                        self.assertEqual(result.exception.message,
                                         "Longitud del valor de la etiqueta 2 incorrecto")
            else:
                testid = "TC" + str(index + 1)
                with self.subTest(testid):
                    inputdata = r"C:\Users\jcamp\PycharmProjects\G801.2024.grupo.2.EG2\src\main\python\json_files" + r"\test2" + r"\test" + str(index + 1) + r".json"
                    print("Executing: " + testid + ":" + inputdata)
                    hm = hotel_manager()

                    with self.assertRaises(hotel_management_exception) as result:
                        print('entra en el result')
                        roomkey = hm.guest_arrival(inputdata)
                        print('sale del with del segundo caso  +++++++++++++++++++++++++++++')
                    self.assertEqual(result.exception.message,
                                     "Formato del archivo JSON incorrecto")