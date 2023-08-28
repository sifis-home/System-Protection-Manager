import json

import rel
import websocket


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("### Connection closed ###")


def on_open(ws):
    print("### Connection established ###")


def publish():
    ws = websocket.WebSocketApp(
        "ws://sifis-device3.iit.cnr.it:3000/ws",
        on_open=on_open,
        on_error=on_error,
        on_close=on_close,
    )

    ws.run_forever(dispatcher=rel)  # Set dispatcher to automatic reconnection
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    dictionary = {
        "domo_ble_thermometer": 700,
        "shelly_25": 400,
        "domo_light": 4,
        "domo_switch": 1,
    }
    ws_req = {
        "RequestPostTopicUUID": {
            "topic_name": "SIFIS:Privacy_Aware_Device_DHT_monitor",
            "topic_uuid": "Privacy_Aware_Device_DHT_monitor_uuid",
            "value": {
                "Dictionary": str(dictionary),
                "requestor_id": "1",
                "request_id": "1",
            },
        }
    }
    ws.send(json.dumps(ws_req))


publish()
