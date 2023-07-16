import json
from unittest import mock

import system_protection_manager

# Importare le funzioni dallo script
from system_protection_manager import (
    connect_to_node_manager,
    dht_monitor,
    on_close,
    on_error,
    on_message,
    on_open,
    publish_dht_data,
    publish_temperature,
    temperature_monitor,
)


# Test per la funzione connect_to_node_manager
def test_connect_to_node_manager():
    # Definire gli input di esempio per la funzione
    node_id = "node_id_example"

    # Chiamare la funzione e verificare l'output o il comportamento atteso
    data = connect_to_node_manager(node_id)

    # Verificare che i dati di output siano corretti
    expected_data = {
        "RequestPostTopicUUID": {
            "topic_name": "SIFIS:node-manager-kick-vote-sugg",
            "topic_uuid": f"72b880d0fdc9a9a00dde4180727e908feb60e07bd614db710f606ca02f209153:{node_id}",
            "value": {"kick": True, "time": 1234},
        }
    }
    assert data == expected_data


# Test per la funzione publish_dht_data
def test_publish_dht_data():
    # Definire gli input di esempio per la funzione
    dht_data = {"data": "example"}

    # Chiamare la funzione e verificare l'output o il comportamento atteso
    with mock.patch("websocket.WebSocketApp") as mock_websocket:
        publish_dht_data(dht_data)

    # Verificare che il WebSocketApp sia stato creato con i parametri corretti
    assert mock_websocket.call_args_list == [
        mock.call(
            "ws://146.48.62.99:3000/ws",
            on_open=on_open,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close,
        )
    ]

    # Verificare che il metodo run_forever sia stato chiamato sul WebSocketApp
    assert mock_websocket.return_value.run_forever.call_args_list == [
        mock.call(dispatcher=mock.ANY)
    ]

    # Verificare che il metodo send sia stato chiamato sul WebSocketApp con i dati corretti
    assert mock_websocket.return_value.send.call_args_list == [
        mock.call(json.dumps(dht_data))
    ]


# Test per la funzione publish_temperature
def test_publish_temperature():
    # Definire gli input di esempio per la funzione
    data = {"temperature": 25.5}

    # Chiamare la funzione e verificare l'output o il comportamento atteso
    with mock.patch("websocket.WebSocketApp") as mock_websocket:
        publish_temperature(data)

    # Verificare che il WebSocketApp sia stato creato con i parametri corretti
    assert mock_websocket.call_args_list == [
        mock.call(
            "ws://146.48.62.99:3000/ws",
            on_open=on_open,
            on_error=on_error,
            on_close=on_close,
        )
    ]

    # Verificare che il metodo run_forever sia stato chiamato sul WebSocketApp
    assert mock_websocket.return_value.run_forever.call_args_list == [
        mock.call(dispatcher=mock.ANY)
    ]

    # Verificare che il metodo send sia stato chiamato sul WebSocketApp con i dati corretti
    assert mock_websocket.return_value.send.call_args_list == [
        mock.call(json.dumps(data))
    ]


# Test per la funzione dht_monitor
def test_dht_monitor():
    # Definire gli input di esempio per la funzione
    dictionary = {"key": "value"}
    requestor_id = "requestor_id_example"
    request_id = "request_id_example"

    # Chiamare la funzione e verificare l'output o il comportamento atteso
    data = dht_monitor(dictionary, requestor_id, request_id)

    # Verificare che i dati di output siano corretti
    expected_data = {
        "RequestPostTopicUUID": {
            "topic_name": "SIFIS:Privacy_Aware_Device_DHT_inquiry",
            "topic_uuid": "DHT_inquiry",
            "value": {
                "description": "DHT inquiry",
                "requestor_id": requestor_id,
                "request_id": request_id,
                "requestor_type": "Pippo",
                "connected": True,
                "Data Type": "String",
                "Dictionary": str(dictionary),
            },
        },
    }
    assert data == expected_data


# Test per la funzione temperature_monitor
def test_temperature_monitor():
    # Definire gli input di esempio per la funzione
    temperature = [25.5, 26.5, 24.5]
    requestor_id = "requestor_id_example"
    request_id = "request_id_example"

    # Chiamare la funzione e verificare l'output o il comportamento atteso
    data = temperature_monitor(temperature, requestor_id, request_id)

    # Verificare che i dati di output siano corretti
    expected_data = {
        "RequestPostTopicUUID": {
            "topic_name": "SIFIS:Privacy_Aware_Device_Anomaly_Detection",
            "topic_uuid": "Anomaly_Detection",
            "value": {
                "description": "Device Anomaly Detection",
                "requestor_id": requestor_id,
                "request_id": request_id,
                "requestor_type": "Pippo",
                "connected": True,
                "Data Type": "List",
                "Temperatures": temperature,
            },
        },
    }
    assert data == expected_data


# Test per la funzione on_error
def test_on_error():
    # Definire gli input di esempio per la funzione
    ws = mock.Mock()
    error = "Error message"


# Importare le funzioni dallo script
from system_protection_manager import (
    connect_to_node_manager,
    dht_monitor,
    on_close,
    on_error,
    on_message,
    on_open,
    publish_dht_data,
    publish_temperature,
)


# Test per la funzione on_error
def test_on_error():
    ws = mock.Mock()
    error = "Error message"
    with mock.patch("builtins.print") as mock_print:
        on_error(ws, error)
        mock_print.assert_called_once_with(error)


# Test per la funzione on_close
def test_on_close():
    ws = mock.Mock()
    close_status_code = 1001
    close_msg = "Connection closed"
    with mock.patch("builtins.print") as mock_print:
        on_close(ws, close_status_code, close_msg)
        mock_print.assert_called_once_with("### Connection closed ###")


# Test per la funzione on_open
def test_on_open():
    ws = mock.Mock()
    with mock.patch("builtins.print") as mock_print:
        on_open(ws)
        mock_print.assert_called_once_with("### Connection established ###")


# Test per la funzione connect_to_node_manager
def test_connect_to_node_manager():
    node_id = "node_id_example"
    data = connect_to_node_manager(node_id)
    expected_data = {
        "RequestPostTopicUUID": {
            "topic_name": "SIFIS:node-manager-kick-vote-sugg",
            "topic_uuid": f"72b880d0fdc9a9a00dde4180727e908feb60e07bd614db710f606ca02f209153:{node_id}",
            "value": {"kick": True, "time": 1234},
        }
    }
    assert data == expected_data


# Test per la funzione publish_dht_data
def test_publish_dht_data():
    dht_data = {"data": "example"}
    with mock.patch("websocket.WebSocketApp") as mock_websocket:
        publish_dht_data(dht_data)
        expected_websocket_calls = [
            mock.call(
                "ws://146.48.62.99:3000/ws",
                on_open=on_open,
                on_message=on_message,
                on_error=on_error,
                on_close=on_close,
            ),
        ]
        assert mock_websocket.call_args_list == expected_websocket_calls
        assert mock_websocket.return_value.run_forever.call_args_list == [
            mock.call(dispatcher=mock.ANY)
        ]
        assert mock_websocket.return_value.send.call_args_list == [
            mock.call(json.dumps(dht_data))
        ]


# Test per la funzione publish_temperature
def test_publish_temperature():
    data = {"temperature": 25.5}
    with mock.patch("websocket.WebSocketApp") as mock_websocket:
        publish_temperature(data)
        expected_websocket_calls = [
            mock.call(
                "ws://146.48.62.99:3000/ws",
                on_open=on_open,
                on_error=on_error,
                on_close=on_close,
            ),
        ]
        assert mock_websocket.call_args_list == expected_websocket_calls
        assert mock_websocket.return_value.run_forever.call_args_list == [
            mock.call(dispatcher=mock.ANY)
        ]
        assert mock_websocket.return_value.send.call_args_list == [
            mock.call(json.dumps(data))
        ]


def test_dht_monitor():
    dictionary = {"key": "value"}
    requestor_id = "requestor_id_example"
    request_id = "request_id_example"
    data = dht_monitor(dictionary, requestor_id, request_id)
    expected_data = {
        "RequestPostTopicUUID": {
            "topic_name": "SIFIS:Privacy_Aware_Device_DHT_inquiry",
            "topic_uuid": "DHT_inquiry",
            "value": {
                "description": "DHT inquiry",
                "requestor_id": requestor_id,
                "request_id": request_id,
                "requestor_type": "Pippo",
                "connected": True,
                "Data Type": "String",
                "Dictionary": str(dictionary),
            },
        },
    }
    assert data == expected_data


# Nuovo test per la funzione mock_websocket_send
def test_mock_websocket_send():
    data = {"key": "value"}
    with mock.patch("websocket.WebSocketApp") as mock_websocket:
        system_protection_manager.publish_dht_data(data)
        mock_websocket.return_value.send.assert_called_once_with(
            json.dumps(data)
        )
