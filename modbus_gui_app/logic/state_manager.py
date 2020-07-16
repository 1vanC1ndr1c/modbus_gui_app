# TODO megageneric dictionary that contains all the required data to form requests and responses

# TODO class
# TODO async same thread as communication
def send_request(args):
    dict = form_request(args)
    send_formed_request_to_modbus(dict)
    send_formed_request_to_database(dict)


def form_request(args):
    # TODO get the arguments from GUI and form a dictionary with the request
    return


def send_formed_request_to_modbus(formed_request):
    # TODO get the formed request and send it to modbus
    return


def send_formed_request_to_database(formed_request):
    # TODO get the formed request and send it to the database
    return


def form_response(args):
    # TODO get the arguments from modbus_communication and  form a dictionary with the response
    return


def send_formed_response_to_gui(formed_response):
    # TODO get the formed response and send it to GUI
    return


def send_formed_response_to_database(formed_response):
    # TODO get the formed response and send it to the database
    return
