from PySide2.QtWidgets import QLineEdit


def get_response(response_queue):
    if response_queue.empty() is True:
        return -1
    else:
        return response_queue.get()


def process_response(response, stacked_widget):
    modbus_response = str(response).split("\\x")
    modbus_response = modbus_response[10:]

    binary_data = ""
    for r in modbus_response:
        r = r.replace("\'", "")
        r = r.replace("\"", "")
        scale = 16  # equals to hexadecimal
        num_of_bits = 8
        # get the reversed the bits
        bin_data_byte = bin(int(r, scale))[2:].zfill(num_of_bits)
        bin_data_byte = str(bin_data_byte)
        bin_data_byte = bin_data_byte[len(bin_data_byte)::-1]
        binary_data = binary_data + bin_data_byte

    indices = []
    inputs = stacked_widget.findChildren(QLineEdit)  # get the number of coils
    start_add = inputs[0].text()
    start_add = int(str(start_add), 16)
    start_add = hex(start_add)

    for i, bit in enumerate(binary_data):
        if bit == '1':
            res = i + int(start_add, 16)
            res = hex(res)
            indices.append(res)

    return indices
