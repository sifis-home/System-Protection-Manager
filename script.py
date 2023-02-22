from flask import Flask, request
import requests
import logging
import json
import os
from datetime import datetime

def log_to_json():
   # Apri il file di log in modalità di lettura
    with open('manager.log', 'r') as f:
        # Inizializza una lista vuota dove verranno salvate le informazioni estratte
        log_entries = []
        # Itera ogni riga del file di log
        for line in f:
            # Suddividi la riga in una lista di elementi utilizzando il carattere di spazio come separatore
            log_entry = set_log_components(line)
            # Aggiungi il dizionario alla lista
            log_entries.append(log_entry)

    # Converte la lista di dizionari in un oggetto JSON
    log_json = json.dumps(log_entries)
    return log_json

def set_log_components(line):
   elements = line.split(' ')
    elements = [s for s in elements if s != '-']
            # Estrai le informazioni rilevanti dalla lista di elementi
    date = elements[0]
    time = elements[1]
    ip = elements[2]
    method = elements[5]
    route = elements[6]
    status = elements[7]
            # Crea un dizionario che rappresenta una singola voce di log
    log_entry = {
                'date': date,
                'time': time,
                'ip': ip,
                'method': method,
                'route': route,
                'status': status
            }

    return log_entry



def recover_address():
    try:
        os_result = os.system("ip route show | grep -Eo 'src[[:space:]]+([[:digit:]]{1,3}\.){3}[[:digit:]]{1,3}' | grep -Eo '([[:digit:]]{1,3}\.){3}[[:digit:]]{1,3}' | head -n 1 > HOST_IP")
        if os_result == 0:
            ip_list = open('HOST_IP', 'r').readlines()
            for ip in ip_list:
              address = ip.replace('\n', '')
        return address
    except Exception as e:
        log(e)

app = Flask(__name__)

headers = {
    'Content-Type': 'application/json',
}

def log(response):
    logging.basicConfig(filename='manager.log', filemode='w', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    logging.info(response)
    return

@app.route('/run', methods=['POST'])
def run():
    ip = str(recover_address())
    try:
      image = request.json['image']
      if 'port' in request.json:
        port = request.json['port']
      else:
        port = 0
      json_data = {
        'image': image,
        'port': port,
      }
      response = requests.post('http://' + ip + ':8080/run', headers=headers, json=json_data)
      log(response.content.decode())
      return response.content.decode()
    except Exception as e:
      log(response.content.decode())
      return f'ERRORE: {e}\n'

@app.route('/stop', methods=['POST'])
def stop():
    ip = str(recover_address())
    try:
      container_id = request.json['container_id']
      json_data = {
        'container_id': container_id
      }
      response = requests.post('http://' + ip + ':8080/stop', headers=headers, json=json_data)
      log(response.content.decode())
      return response.content.decode()
    except Exception as e:
      log(response.content.decode())
      return f'ERRORE: {e}\n'

@app.route('/remove', methods=['POST'])
def remove():
    ip = str(recover_address())
     try:
      container_id = request.json['container_id']
      json_data = {
        'container_id': container_id
      }
      response = requests.post('http://' + ip + ':8080/remove', headers=headers, json=json_data)
      log(response.content.decode())
      return response.content.decode()
    except Exception as e:
      log(response.content.decode())
      return f'ERRORE: {e}\n'

@app.route('/start', methods=['POST'])
def start():
  try:
    data = request.data
    print(data)
  except Exception as e:
    return f'ERRORE: {e}\n'


@app.route('/check', methods=['POST'])
def check():
    try:
      ip = '127.0.0.1'
      client_ip = request.remote_addr
      # Controllo dell'indirizzo IP del client
      if client_ip == ip or client_ip == str(recover_address()):
          file = log_to_json()
           url = 'http://' + str(recover_address()) + ':8080/log'
          response = requests.post(url, headers=headers, json=file)
          response.raise_for_status()
          return f'Access Authorized! The log file has been sent to the host\n'
      else:
          return 'Access Denied!\n'
    except Exception as e:
      print('File could be empty')
      return f'ERRORE: {e}\n'

@app.route('/list', methods=['POST'])
def list_running_container():
  try:
    # Filtra la lista dei container in esecuzione per l'immagine che ti interessa
    url = 'http://' + str(recover_address()) + ':8080/list'
    response = requests.post(url, headers=headers)
    return response.content.decode()
  except Exception as e:
    return f'ERRORE: {e}\n'

if __name__ == '__main__':
    print('APPLICATION MANAGER CONTAINER')
    app.run(host='0.0.0.0')
