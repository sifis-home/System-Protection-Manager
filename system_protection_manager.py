import json

import rel
import requests
import websocket

rest_url = "http://localhost:3000/"

table = {
    "146.48.62.97": "72b880d0fdc9a9a00dde4180727e908feb60e07bd614db710f606ca02f209153",
    "146.48.62.98": "f198e31671aa7c23318359ad3df4d13bf4e13e7f8243794877598cbb2c953421",
    "146.48.62.99": "c3dc86dfbe0e01b0c3ccdbe71100f186d1e533d5be97260b6adffa3c6ad34f98",
    "146.48.62.107": "482b1af0889dd80ba89b2e89692c73529dbf26a00360c02e01de36778e0c3ee2",
    "146.48.62.198": "fe7b6135e1549190588fbb083edd1e4e6ef0d1c738f57a9af5fa28a5a1296946",
    "146.48.62.109": "69cdbfa97b3e1a859ff7042370acd200fe89499028dfa90370dc23f4fb0552960",
}


def notify_mobile_application(topic_uuid, notification, notification_data):
    topic_name = "SIFIS:notification_message"
    requests.post(
        rest_url + "topic_name/" + topic_name + "/topic_uuid/" + topic_uuid,
        json=notification_data,
    )
    print("[!] The following message has been forwarded: " + notification)
    return


def on_message(ws, message):
    print("Received:\n")

    json_message = json.loads(message)
    print(json_message)

    if "Persistent" in json_message:
        json_message = json_message["Persistent"]

        try:
            topic_name = json_message["topic_name"]
            # handle topic name
            topic_uuid = json_message["topic_uuid"]
            if topic_name == "SIFIS:node-manager-id-ip-mapping":
                uuid = json_message["topic_uuid"]
                # print(uuid)
                if "value" in json_message:
                    value = json_message["value"]
                    ip_list = value["ip_list"]
                    ip = ip_list[1]["ip"]
                    if ip not in table:
                        table[ip] = uuid
                        print("IP Added:", ip)
                        print(table)
                    else:
                        if table[ip] != uuid:
                            table[ip] = uuid
                            print("Update for IP:", ip)
                        else:
                            print(
                                "IP",
                                ip,
                                "is already present in the table with the corresponding UUID:",
                                uuid,
                            )
                else:
                    notification = "Node ID - IP Mapping is failed"
                    notification_data = {
                        "requestor_id": requestor_id,
                        "request_id": request_id,
                        "message": notification,
                    }
                    notify_mobile_application(
                        uuid, notification, notification_data
                    )

            if topic_name == "SIFIS:Privacy_Aware_Speech_Recognition_Results":
                if "value" in json_message:
                    json_message = json_message["value"]
                    dictionary = json_message["Dictionary"]
                    requestor_id = json_message["requestor_id"]
                    request_id = json_message["request_id"]
                    dht_data = dht_monitor(
                        dictionary, requestor_id, request_id
                    )
                    print("PUBLISHING DHT INQUIRY ...")
                    publish_dht_data(dht_data)

            if topic_name == "SIFIS:Privacy_Aware_Device_DHT_monitor":
                # node_data = connect_to_node_manager()
                # publish_dht_data(node_data)
                if "value" in json_message:
                    json_message = json_message["value"]
                    dictionary = json_message["Dictionary"]
                    requestor_id = json_message["requestor_id"]
                    request_id = json_message["request_id"]
                    dht_data = dht_monitor(
                        dictionary, requestor_id, request_id
                    )
                    print("PUBLISHING DHT INQUIRY ...")
                    publish_dht_data(dht_data)

            if topic_name == "SIFIS:AUD_Manager_Results":
                print(" JSON message \n")
                if "value" in json_message:
                    json_message = json_message["value"]
                    # print(json_message)
                    # description = json_message["description"]
                    # requestor_id = json_message["requestor_id"]
                    # request_id = json_message["request_id"]
                    # print(description)
                    ip = json_message["subject_ip"]
                    ID = table[ip]
                    anomaly = json_message["anomaly"]
                    # print(anomaly)
                    # print("CATEGORY: ")
                    category = (
                        json_message["anomaly"]
                        .split("'category': ", 1)[1]
                        .split(", 'severity': ")[0]
                    )
                    print(
                        "[!] AUD Analytics Results have been arrived. System Protection Manager has received : "
                        + anomaly
                        + " --> "
                        + category
                    )
                    # print(category)
                    # node_data = connect_to_node_manager(ID) handling node manager settings
                    # publish_dht_data(node_data)  publishing node manager settings
                    data = {
                        "description": description,
                        "ID": ID,
                        "category": category,
                    }
                    notification = (
                        "Anomaly "
                        + anomaly
                        + " has been caught by AUD Analytic. The Node "
                        + str(ID)
                        + " has been kicked out"
                    )
                    notification_data = {
                        "requestor_id": requestor_id,
                        "request_id": request_id,
                        "notification": notification,
                    }
                    notify_mobile_application(
                        topic_uuid, notification, notification_data
                    )

            if (
                topic_name
                == "SIFIS:Privacy_Aware_Device_Anomaly_Detection_monitor"
            ):
                if "value" in json_message:
                    json_message = json_message["value"]
                    temperature = json_message["Temperatures"]
                    requestor_id = json_message["requestor_id"]
                    request_id = json_message["request_id"]

                    data = temperature_monitor(
                        temperature, requestor_id, request_id
                    )
                    publish_temperature(data)  # publish the data to the server

            if topic_name == "SIFIS:Privacy_Aware_Device_DHT_Results":
                print("[!!!] Results have arrived ...\n")
                requestor = json_message["value"]["requestor_id"]
                request = json_message["value"]["request_id"]
                response_dht = json_message["value"]["response"]
                response_data = {
                    "Response": response_dht,
                    "Requestor": requestor,
                    "Request": request,
                }
                print(response_data)
                if response_dht == "System Violation":
                    notification = {"message": "System Violation on the DHT"}

                    notify_mobile_application(
                        topic_uuid, response_data, notification
                    )

            if (
                topic_name
                == "SIFIS:Privacy_Aware_Device_Anomaly_Detection_Results"
            ):
                print("[!!!] Results have arrived ...\n")
                anomaly = json_message["value"]["anomaly"]
                requestor = json_message["value"]["requestor_id"]
                request = json_message["value"]["request_id"]
                with open("PROTECTION_MANAGER_LOG", "a") as f:
                    f.write("\n\nReceived: " + str(json_message))
                    f.write("ANOMALY: " + str(anomaly))
                    f.write("REQUESTOR: " + str(requestor))
                    anomaly_data = {
                        "Anomaly": anomaly,
                        "Requestor": requestor,
                        "Request": request,
                    }
                    print("ANOMALY_DATA: " + str(anomaly_data))
                    """
                    url = "http://localhost:7000/manager"
                    response = requests.post(url, json=anomaly_data)
                    """
        except Exception as e:
            print("[!!!] ERROR: " + str(e))


def connect_to_node_manager(node_id):
    data = {
        "RequestPostTopicUUID": {
            "topic_name": "SIFIS:node-manager-kick-vote-sugg",
            "topic_uuid": "72b880d0fdc9a9a00dde4180727e908feb60e07bd614db710f606ca02f209153:"
            + node_id,
            "value": {"kick": True, "time": 1234},
        }
    }
    return data


def publish_dht_data(dht_data):
    ws = websocket.WebSocketApp(
        "ws://localhost:3000/ws",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    ws.run_forever(dispatcher=rel)  # Set dispatcher to automatic reconnection
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    ws.send(json.dumps(dht_data))


def publish_temperature(data):
    ws = websocket.WebSocketApp(
        "ws://localhost:3000/ws",
        on_open=on_open,
        on_error=on_error,
        on_close=on_close,
    )
    ws.run_forever(dispatcher=rel)  # Set dispatcher to automatic reconnection
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    ws.send(json.dumps(data))


def dht_monitor(dictionary, requestor_id, request_id):
    data = {
        "RequestPostTopicUUID": {
            "topic_name": "SIFIS:Privacy_Aware_Device_DHT_inquiry",
            "topic_uuid": "DHT_inquiry",
            "value": {
                "description": "DHT inquiry",
                "requestor_id": str(requestor_id),
                "request_id": str(request_id),
                "requestor_type": "Pippo",
                "connected": True,
                "Data Type": "String",
                "Dictionary": str(dictionary),
            },
        }
    }

    return data


def temperature_monitor(temperature, requestor_id, request_id):
    temperature = [float(temp) for temp in temperature]
    data = {
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
        }
    }

    return data


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("### Connection closed ###")


def on_open(ws):
    print("### Connection established ###")


if __name__ == "__main__":
    ws = websocket.WebSocketApp(
        "ws://localhost:3000/ws",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )

    ws.run_forever()
