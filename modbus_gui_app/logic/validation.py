from PySide2.QtWidgets import QLineEdit, QComboBox


def get_validation_result(function_code, stacked_widget):
    is_valid = False
    inputs = stacked_widget.findChildren(QLineEdit)  # get children that are used for data input

    if function_code == 1 or function_code == 2 or function_code == 3 \
            or function_code == 4 or function_code == 5 or function_code == 6:

        valid_start_address_hex = False
        start_address_hex = inputs[0].text()
        valid_no_of_elements = False
        no_of_elements = inputs[1].text()
        valid_unit_address = False
        if function_code != 5:
            unit_address = inputs[2].text()
        else:
            unit_address = inputs[1].text()

        try:
            start_address_hex = int(str(start_address_hex), 16)
            if start_address_hex < 0x0001 or start_address_hex > 0xFFFF:
                return False, "Start address needs to be [0x0001, 0xFFFF]"
            else:
                valid_start_address_hex = True
        except:
            return False, "Start address needs to be in hexadecimal format."

        if function_code == 6:
            try:
                no_of_elements = int(str(no_of_elements), 16)
                if no_of_elements < 0x0000 or no_of_elements > 0xFFFF:
                    return False, "Number of elements needs to be [0x0000, 0xFFFF]"
                else:
                    valid_start_address_hex = True
            except:
                return False, "Number of elements needs to be in hexadecimal format."

        try:
            if function_code != 6:
                no_of_elements = int(str(no_of_elements))
            if function_code == 5:
                if no_of_elements < 0x01 or no_of_elements > 0xFF:
                    return False, "Coil Value needs to be [0x00, 0xFF]"
                else:
                    valid_no_of_elements = True
            else:
                if no_of_elements < 1 or no_of_elements > 2000:
                    if function_code == 1:
                        return False, "Number of coils  needs to be [1, 2000]"
                    elif function_code == 2:
                        return False, "Number of inputs  needs to be [1, 2000]"
                    elif function_code == 3 or function_code == 4:
                        return False, "Number of registers  needs to be [1, 2000]"
                else:
                    valid_no_of_elements = True
        except:
            if function_code == 1:
                return False, "Number of coils needs to be a base 10 number."
            elif function_code == 2:
                return False, "Number of inputs needs to be a base 10 number."
            elif function_code == 3 or function_code == 4:
                return False, "Number of registers needs to be a base 10 number."
            elif function_code == 5:
                return False, "Coil value needs to be a base 10 number."

        try:
            unit_address = int(str(unit_address))
            if unit_address < 1 or unit_address > 255:
                return False, "Unit address  needs to be [1, 255]"
            else:
                valid_unit_address = True
        except:
            return False, "Unit address needs to be a base 10 number."

        if valid_no_of_elements is True and valid_start_address_hex is True and valid_unit_address is True:
            data = [start_address_hex, no_of_elements, unit_address, function_code]
            if function_code == 5:
                select_state = stacked_widget.findChildren(QComboBox)[0].currentIndex()
                data = [start_address_hex, select_state, unit_address, function_code]
            return True, data
