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


# Test per la funzione on_error
def test_on_error():
    # Definire gli input di esempio per la funzione
    ws = mock.Mock()
    error = "Error message"

    # Chiamare la funzione e verificare l'output o il comportamento atteso
    with mock.patch("builtins.print") as mock_print:
        on_error(ws, error)

    # Verificare che la funzione print sia stata chiamata con il messaggio di errore corretto
    mock_print.assert_called_once_with(error)


# Test per la funzione on_close
def test_on_close():
    # Definire gli input di esempio per la funzione
    ws = mock.Mock()
    close_status_code = 1001
    close_msg = "Connection closed"

    # Chiamare la funzione e verificare l'output o il comportamento atteso
    with mock.patch("builtins.print") as mock_print:
        on_close(ws, close_status_code, close_msg)

    # Verificare che la funzione print sia stata chiamata con il messaggio di chiusura corretto
    mock_print.assert_called_once_with("### Connection closed ###")


# Test per la funzione on_open
def test_on_open():
    # Definire gli input di esempio per la funzione
    ws = mock.Mock()

    # Chiamare la funzione e verificare l'output o il comportamento atteso
    with mock.patch("builtins.print") as mock_print:
        on_open(ws)

    # Verificare che la funzione print sia stata chiamata con il messaggio corretto
    mock_print.assert_called_once_with("### Connection established ###")


# Nuovo test per la funzione mock_websocket_send
def test_mock_websocket_send():
    # Definire gli input di esempio per la funzione
    data = {"key": "value"}

    # Chiamare la funzione e verificare l'output o il comportamento atteso
    with mock.patch("websocket.WebSocketApp") as mock_websocket:
        system_protection_manager.publish_dht_data(data)

    # Verificare che il metodo send sia stato chiamato sul WebSocketApp con i dati corretti
    mock_websocket.return_value.send.assert_called_once_with(json.dumps(data))


# Test for the temperature_monitor function
def test_temperature_monitor():
    # Define example input for the function
    temperature = [25.5, 26.5, 24.5]
    requestor_id = "requestor_id_example"
    request_id = "request_id_example"

    # Call the function and verify the output or expected behavior
    data = temperature_monitor(temperature, requestor_id, request_id)

    # Verify that the output data is correct
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


# Test per la funzione on_message
def test_on_message():
    # Definire gli input di esempio per la funzione
    ws = mock.Mock()
    message = '{"Persistent": {"topic_name": "SIFIS:Privacy_Aware_Speech_Recognition_Results", "value": {"Dictionary": {"key": "value"}, "requestor_id": "requestor_id_example", "request_id": "request_id_example"}}}'

    # Chiamare la funzione e verificare l'output o il comportamento atteso
    with mock.patch("builtins.print") as mock_print:
        with mock.patch(
            "system_protection_manager.dht_monitor"
        ) as mock_dht_monitor:
            with mock.patch(
                "system_protection_manager.publish_dht_data"
            ) as mock_publish_dht_data:
                system_protection_manager.on_message(ws, message)

    # Verificare che la funzione print sia stata chiamata con il messaggio corretto
    mock_print.assert_any_call("Received:\n")
    mock_print.assert_any_call(json.loads(message))

    # Verificare che la funzione dht_monitor sia stata chiamata con i parametri corretti
    mock_dht_monitor.assert_called_once_with(
        {"key": "value"}, "requestor_id_example", "request_id_example"
    )

    # Verificare che la funzione publish_dht_data sia stata chiamata con i parametri corretti
    mock_publish_dht_data.assert_called_once_with(
        mock_dht_monitor.return_value
    )
