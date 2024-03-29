"""
clase hotel_management_exception
"""

class hotel_management_exception(Exception):
    """
    clase hotel_management_exception
    """
    def __init__(self, message: object) -> object:
        """
        init
        """
        self.__message = message
        super().__init__(self.message)

    @property
    def message(self):
        """
        hace un return
        :return:
        """
        return self.__message

    @message.setter
    def message(self, value):
        """
        convierte message en value
        """
        self.__message = value