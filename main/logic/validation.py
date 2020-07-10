import sys

from PySide2.QtWidgets import QLineEdit

from request_processing import send_request
from window import init_error_window

is_valid = False


def validate_input_data(index, stacked_widget, window, request_queue):
    if index == 0:  # read coils, 2 inputs (starting address and no. of coils)
        inputs = stacked_widget.findChildren(QLineEdit)  # get children that are used for data input

        valid_start_address_hex = False
        start_address_hex = inputs[0].text()
        valid_no_of_coils = False
        no_of_coils = inputs[1].text()

        valid_unit_address = False
        unit_address = inputs[2].text()

        try:
            start_address_hex = int(str(start_address_hex), 16)
            if start_address_hex < 0x0001 or start_address_hex > 0xFFFF:
                init_error_window(window, "Start address needs to be [0x0000, 0xFFFF]")
            else:
                valid_start_address_hex = True
        except:
            init_error_window(window, "Start address needs to be in hexadecimal format.")

        try:
            no_of_coils = int(str(no_of_coils))
            if no_of_coils < 1 or no_of_coils > 2000:
                init_error_window(window, "Number of coils  needs to be [1, 2000]")
            else:
                valid_no_of_coils = True
        except:
            init_error_window(window, "Number of coils needs to be a base 10 number.")

        try:
            unit_address = int(str(unit_address))
            if unit_address < 1 or unit_address > 255:
                init_error_window(window, "Unit address  needs to be [1, 255]")
            else:
                valid_unit_address = True
        except:
            init_error_window(window, "Unit address needs to be a base 10 number.")

        if valid_no_of_coils is True and valid_start_address_hex is True and valid_unit_address:
            data = [start_address_hex, no_of_coils]
            send_request(unit_address, index + 1, data, request_queue)
            global is_valid
            is_valid = True
        else:
            is_valid = False
    if index == 1:
        print("F2")
        sys.exit()
