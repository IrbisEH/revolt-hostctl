from revolt_hostctl.app.utils import to_snake, to_camel

def test_to_snake():
    assert to_snake("LocalVm") == "local_vm"
    assert to_snake("Network") == "network"
    assert to_snake("Host") == "host"
    assert to_snake("myLongClassName") == "my_long_class_name"
    assert to_snake("snake_case") == "snake_case"

def test_to_camel():
    assert to_camel("local_vm") == "LocalVm"
    assert to_camel("network") == "Network"
    assert to_camel("host") == "Host"
    assert to_camel("my_long_class_name") == "MyLongClassName"
    assert to_camel("CamelCase") == "Camelcase"  # word.capitalize() makes 'CamelCase' -> 'Camelcase'
    assert to_camel("already_camel") == "AlreadyCamel"
