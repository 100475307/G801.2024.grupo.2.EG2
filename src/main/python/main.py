"""
clase principal, main
"""
# THIS MAIN PROGRAM IS ONLY VALID FOR THE FIRST THREE WEEKS OF CLASS
# IN GUIDED EXERCISE 2.2, TESTING MUST BE PERFORMED USING UNITTESTS.

from src.main.python.uc3m_travel import hotel_manager


def main():
    """
    funcion principal del main
    """
    mng = hotel_manager()
    res = mng.read_data_from_json("test.json")
    strRes = str(res)
    print(strRes)
    print("CreditCard: " + res.credit_card)
    print(res.localizer)


if __name__ == "__main__":
    main()
