from PySide2.QtWidgets import QLineEdit, QComboBox

from request_processing import send_request
from window import init_error_window

is_valid = False


def validate_input_data(index, stacked_widget, window, request_queue):
    inputs = stacked_widget.findChildren(QLineEdit)  # get children that are used for data input

    if index == 0 or index == 1 or index == 2 or index == 3 or index == 4 or index == 5:
        valid_start_address_hex = False
        start_address_hex = inputs[0].text()
        valid_no_of_elements = False
        no_of_elements = inputs[1].text()
        valid_unit_address = False
        if index != 4:
            unit_address = inputs[2].text()
        else:
            unit_address = inputs[1].text()

        try:
            start_address_hex = int(str(start_address_hex), 16)
            if start_address_hex < 0x0001 or start_address_hex > 0xFFFF:
                init_error_window(window, "Start address needs to be [0x0001, 0xFFFF]")
            else:
                valid_start_address_hex = True
        except:
            init_error_window(window, "Start address needs to be in hexadecimal format.")

        if index == 5:
            try:
                no_of_elements = int(str(no_of_elements), 16)
                if no_of_elements < 0x0000 or no_of_elements > 0xFFFF:
                    init_error_window(window, "Number of elements needs to be [0x0000, 0xFFFF]")
                else:
                    valid_start_address_hex = True
            except:
                init_error_window(window, "Number of elements needs  in hexadecimal format.")

        try:
            if index != 5:
                no_of_elements = int(str(no_of_elements))
            if index == 4:
                if no_of_elements < 0x01 or no_of_elements > 0xFF:
                    init_error_window(window, "Coil Value needs to be [0x00, 0xFF]")
                else:
                    valid_no_of_elements = True
            else:
                if no_of_elements < 1 or no_of_elements > 2000:
                    if index == 0:
                        init_error_window(window, "Number of coils  needs to be [1, 2000]")
                    elif index == 1:
                        init_error_window(window, "Number of inputs  needs to be [1, 2000]")
                    elif index == 2 or index == 3:
                        init_error_window(window, "Number of registers  needs to be [1, 2000]")
                else:
                    valid_no_of_elements = True
        except:
            if index == 0:
                init_error_window(window, "Number of coils needs to be a base 10 number.")
            elif index == 1:
                init_error_window(window, "Number of inputs needs to be a base 10 number.")
            elif index == 2 or index == 3:
                init_error_window(window, "Number of registers needs to be a base 10 number.")
            elif index == 4:
                init_error_window(window, "Coil value needs to be a base 10 number.")

        try:
            unit_address = int(str(unit_address))
            if unit_address < 1 or unit_address > 255:
                init_error_window(window, "Unit address  needs to be [1, 255]")
            else:
                valid_unit_address = True
        except:
            init_error_window(window, "Unit address needs to be a base 10 number.")

        if valid_no_of_elements is True and valid_start_address_hex is True and valid_unit_address is True:
            data = [start_address_hex, no_of_elements]
            if index == 4:
                select_state = stacked_widget.findChildren(QComboBox)[0].currentIndex()
                data = [start_address_hex, select_state]
            send_request(unit_address, index + 1, data, request_queue)
            global is_valid
            is_valid = True
        else:
            is_valid = False
