import json
from unittest import mock


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


# Test per la funzione on_message
def test_on_message():
    # Definire gli input di esempio per la funzione
    ws = mock.Mock()
    message = json.dumps(
        {"Persistent": {"topic_name": "SIFIS:node-manager-id-ip-mapping"}}
    )

    # Chiamare la funzione e verificare l'output o il comportamento atteso
    with mock.patch("builtins.print") as mock_print:
        on_message(ws, message)

    # Verificare che la funzione print sia stata chiamata con i messaggi corretti
    assert mock_print.call_args_list == [
        mock.call("Received:\n"),
        mock.call(
            {"Persistent": {"topic_name": "SIFIS:node-manager-id-ip-mapping"}}
        ),
    ]


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
