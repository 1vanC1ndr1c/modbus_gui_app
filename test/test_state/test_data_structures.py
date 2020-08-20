from modbus_gui_app.state import data_structures


def test_init_user_action_state_dict():
    action_state_dict = data_structures._init_user_action_state_dict()
    assert len(action_state_dict) != 0
    assert type(action_state_dict) == dict


def test_init_live_update_states():
    live_dict = data_structures._init_live_update_states()
    assert len(live_dict) != 0
    assert type(live_dict) == dict

    dict_cnt = 0
    for key in live_dict:
        if type(live_dict[key]) == dict:
            dict_cnt = dict_cnt + 1

    assert dict_cnt == 4
