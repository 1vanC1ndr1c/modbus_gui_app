from PySide2.QtWidgets import QLineEdit, QComboBox


def get_request_validation_result(function_code, stacked_widget):
    if function_code == 1:
        return validate_read_coils(function_code, stacked_widget)
    elif function_code == 2:
        return validate_read_discrete_inputs(function_code, stacked_widget)
    elif function_code == 3:
        return validate_read_holding_registers(function_code, stacked_widget)
    elif function_code == 4:
        return validate_read_input_registers(function_code, stacked_widget)
    elif function_code == 5:
        return validate_write_single_coil(function_code, stacked_widget)
    elif function_code == 6:
        return validate_write_single_register(function_code, stacked_widget)
    else:
        return False, "Invalid Function Code!"


# function specific validations

def validate_read_coils(function_code, stacked_widget):
    inputs = stacked_widget.findChildren(QLineEdit)
    start_address_hex = inputs[0].text()
    no_of_elements = inputs[1].text()
    unit_address = inputs[2].text()

    valid_start_address_hex, err_msg, start_address_hex = validate_start_address(start_address_hex)
    if valid_start_address_hex is False:
        return valid_start_address_hex, err_msg

    try:
        no_of_elements = int(str(no_of_elements))
        if no_of_elements < 1 or no_of_elements > 2000:
            return False, "Number of coils  needs to be [1, 2000]"
        else:
            valid_no_of_elements = True
    except:
        return False, "Number of coils needs to be a base 10 number."

    valid_unit_address, err_msg, unit_address = validate_unit_address(unit_address)
    if valid_unit_address is False:
        return valid_unit_address, err_msg

    if valid_no_of_elements is True and valid_start_address_hex is True and valid_unit_address is True:
        data = [start_address_hex, no_of_elements, unit_address, function_code]
        return True, data


def validate_read_discrete_inputs(function_code, stacked_widget):
    inputs = stacked_widget.findChildren(QLineEdit)  # get children that are used for data input
    start_address_hex = inputs[0].text()
    no_of_elements = inputs[1].text()
    unit_address = inputs[2].text()

    valid_start_address_hex, err_msg, start_address_hex = validate_start_address(start_address_hex)
    if valid_start_address_hex is False:
        return valid_start_address_hex, err_msg

    try:
        no_of_elements = int(str(no_of_elements))
        if no_of_elements < 1 or no_of_elements > 2000:
            return False, "Register count  needs to be [1, 2000]"
        else:
            valid_no_of_elements = True
    except:
        return False, "Register count needs to be a base 10 number."

    valid_unit_address, err_msg, unit_address = validate_unit_address(unit_address)
    if valid_unit_address is False:
        return valid_unit_address, err_msg

    if valid_no_of_elements is True and valid_start_address_hex is True and valid_unit_address is True:
        data = [start_address_hex, no_of_elements, unit_address, function_code]
        return True, data


def validate_read_holding_registers(function_code, stacked_widget):
    inputs = stacked_widget.findChildren(QLineEdit)  # get children that are used for data input
    start_address_hex = inputs[0].text()
    no_of_elements = inputs[1].text()
    unit_address = inputs[2].text()

    valid_start_address_hex, err_msg, start_address_hex = validate_start_address(start_address_hex)
    if valid_start_address_hex is False:
        return valid_start_address_hex, err_msg

    try:
        no_of_elements = int(str(no_of_elements))
        if no_of_elements < 1 or no_of_elements > 2000:
            return False, "Number of registers  needs to be [1, 2000]"
        else:
            valid_no_of_elements = True
    except:
        return False, "Number of registers needs to be a base 10 number."

    valid_unit_address, err_msg, unit_address = validate_unit_address(unit_address)
    if valid_unit_address is False:
        return valid_unit_address, err_msg

    if valid_no_of_elements is True and valid_start_address_hex is True and valid_unit_address is True:
        data = [start_address_hex, no_of_elements, unit_address, function_code]
        return True, data


def validate_read_input_registers(function_code, stacked_widget):
    inputs = stacked_widget.findChildren(QLineEdit)  # get children that are used for data input
    start_address_hex = inputs[0].text()
    no_of_elements = inputs[1].text()
    unit_address = inputs[2].text()

    valid_start_address_hex, err_msg, start_address_hex = validate_start_address(start_address_hex)
    if valid_start_address_hex is False:
        return valid_start_address_hex, err_msg

    try:
        no_of_elements = int(str(no_of_elements))
        if no_of_elements < 1 or no_of_elements > 2000:
            return False, "Number of registers  needs to be [1, 2000]"
        else:
            valid_no_of_elements = True
    except:
        return False, "Number of registers needs to be a base 10 number."

    valid_unit_address, err_msg, unit_address = validate_unit_address(unit_address)
    if valid_unit_address is False:
        return valid_unit_address, err_msg

    if valid_no_of_elements is True and valid_start_address_hex is True and valid_unit_address is True:
        data = [start_address_hex, no_of_elements, unit_address, function_code]
        return True, data


def validate_write_single_coil(function_code, stacked_widget):
    inputs = stacked_widget.findChildren(QLineEdit)  # get children that are used for data input
    start_address_hex = inputs[0].text()
    unit_address = inputs[1].text()

    valid_start_address_hex, err_msg, start_address_hex = validate_start_address(start_address_hex)
    if valid_start_address_hex is False:
        return valid_start_address_hex, err_msg

    valid_unit_address, err_msg, unit_address = validate_unit_address(unit_address)
    if valid_unit_address is False:
        return valid_unit_address, err_msg

    if valid_start_address_hex is True and valid_unit_address is True:
        select_state = stacked_widget.findChildren(QComboBox)[0].currentIndex()
        if select_state == 0:
            select_state = 1
        else:
            select_state = 0
        data = [start_address_hex, select_state, unit_address, function_code]
        return True, data


def validate_write_single_register(function_code, stacked_widget):
    inputs = stacked_widget.findChildren(QLineEdit)  # get children that are used for data input
    start_address_hex = inputs[0].text()
    no_of_elements = inputs[1].text()
    unit_address = inputs[2].text()

    valid_start_address_hex, err_msg, start_address_hex = validate_start_address(start_address_hex)
    if valid_start_address_hex is False:
        return valid_start_address_hex, err_msg

    try:
        no_of_elements = int(str(no_of_elements), 16)
        if no_of_elements < 0x0000 or no_of_elements > 0xFFFF:
            return False, "Register value needs to be [0x0000, 0xFFFF]"
        else:
            valid_no_of_elements = True
    except:
        return False, "Register value needs to be in hexadecimal format."

    valid_unit_address, err_msg, unit_address = validate_unit_address(unit_address)
    if valid_unit_address is False:
        return valid_unit_address, err_msg

    if valid_no_of_elements is True and valid_start_address_hex is True and valid_unit_address is True:
        data = [start_address_hex, no_of_elements, unit_address, function_code]
        return True, data


# validations that are same for every function
def validate_start_address(start_address_hex):
    try:
        start_address_hex = int(str(start_address_hex), 16)
        if start_address_hex < 0x0001 or start_address_hex > 0xFFFF:
            return False, "Start address needs to be [0x0001, 0xFFFF]", None
    except:
        return False, "Start address needs to be in hexadecimal format.", None
    return True, "-", start_address_hex


def validate_unit_address(unit_address):
    try:
        unit_address = int(str(unit_address))
        if unit_address < 1 or unit_address > 254:
            return False, "Unit address  needs to be [1, 254]", None
    except:
        return False, "Unit address needs to be a base 10 number.", None
    return True, "-", unit_address


def validate_current_state_data(function_name, input_data):
    if function_name == "READ_COILS":
        if len(input_data) == 0:
            return False, "Insert the coil address."
        try:
            input_data = int(str(input_data), 16)
            if input_data < 0000 or input_data > 2000:
                return False, "Coil address needs to be [0000, 2000]"
        except:
            return False, "Coil address needs to be in hexadecimal format."

        return True, input_data
