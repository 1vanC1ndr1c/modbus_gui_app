from PySide2.QtWidgets import QLineEdit


def get_response(response_queue):
    try:
        r = response_queue.get(block=True, timeout=1.5)
        return r
    except:
        print("No Data in Queue")
        return -1
    # return b'\x00\x01\x00\x07\x01\x03\x04\x03\xE8\x13\x88'


def process_response(response, stacked_widget):
    try:
        if str(response).split('\\')[8].startswith('x8'):  # check for errors in the response
            err_msg = str(response).split('\\')[9]
            err_msg = err_msg.replace("\'", "")
            err_msg = err_msg.replace("\"", "")
            err_msg = err_msg.replace("x", "")
            if err_msg == "01":
                err_msg = "ERROR: Illegal function"
            elif err_msg == "02":
                err_msg = "ERROR: Illegal data address"
            elif err_msg == "03":
                err_msg = "ERROR: Illegal data value"
            else:
                err_msg = "ERROR: Slave device failure"
            return [-1, err_msg]
    except:
        # db_write("Request not processed.")
        print("Response not processed.")

    if stacked_widget.currentIndex() == 0 or stacked_widget.currentIndex() == 1:
        modbus_response = str(response).split("\\x")
        modbus_response = modbus_response[10:]
        binary_data = ""
        for r in modbus_response:
            r = r.replace("\'", "")
            r = r.replace("\"", "")
            scale = 16
            num_of_bits = 8
            # get the reversed the bits
            bin_data_byte = bin(int(r, scale))[2:].zfill(num_of_bits)
            bin_data_byte = str(bin_data_byte)
            bin_data_byte = bin_data_byte[len(bin_data_byte)::-1]
            binary_data = binary_data + bin_data_byte

        indices = []

        inputs = stacked_widget.widget(stacked_widget.currentIndex()).findChildren(QLineEdit)
        start_add = inputs[0].text()
        start_add = int(str(start_add), 16)
        start_add = hex(start_add)

        for i, bit in enumerate(binary_data):
            if bit == '1':
                res = i + int(start_add, 16)
                res = hex(res)
                indices.append(res)

        return indices

    elif stacked_widget.currentIndex() == 2 or stacked_widget.currentIndex() == 3:
        modbus_response = str(response).split("\\x")
        modbus_response = modbus_response[10:]
        inputs = stacked_widget.widget(stacked_widget.currentIndex()).findChildren(QLineEdit)
        start_add = inputs[0].text()
        start_add = int(str(start_add), 16)
        start_add = hex(start_add)
        values = []
        for i in range(0, len(modbus_response), 2):
            try:
                values.append((modbus_response[i] + modbus_response[i + 1]).replace("\'", ""))
            except:
                pass
        if len(values) == 0:
            return []
        location_and_value = []
        for i, val in enumerate(values):
            location = i + int(start_add, 16)
            location = hex(location)
            location_and_value.append([location, val])
        return location_and_value

    elif stacked_widget.currentIndex() == 4 or stacked_widget.currentIndex() == 5:
        return [1]
