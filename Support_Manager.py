import docker
from flask import Flask, request
import subprocess
import logging
import datetime
import os

class DockerManager:
  def __init__(self):
    self.client = docker.DockerClient(base_url='unix://var/run/docker.sock')

  def run_container(self, image, port):
    image_list = self.client.images.list()
    image_string = []
    for im in image_list:
      stringa = str(im).split("<Image: '", 1)[1].split(':')[0]
      image_string.append(stringa)
    if image not in image_string:
      output = self.client.images.pull(image, stream=True, decode=True)
      return f"{image} was not present. The Image {image} has been built\n"
    else:
      if port:
        process = subprocess.run(['docker', 'run', '-p', port + ':' + port, image], stdout=subprocess.PIPE)
      elif port == 0:
        process = subprocess.run(['docker', 'run', image], stdout=subprocess.PIPE)
      output = process.stdout
      return f"The container with {image} is active...\n\n{output.decode()}\n"


  def stop_container(self, container_id):
   container = self.client.containers.get(container_id)
    container.stop()

  def remove_container(self, container_id):
    container = self.client.containers.get(container_id)
    container.remove()

  def list_container(self):
    try:
      # Filtra la lista dei container in esecuzione per l'immagine che ti interessa
      containers = self.client.containers.list(filters={"status": "running"})
      # Prendi solo il primo container della lista (se esiste)
      # Crea il dizionario di output
      output = {}
      for container in containers:
        output[container.id] = container.image.tags[0]
      return output
    except Exception as e:
      return f"ERRORE: {e}\n"


app = Flask(__name__)
manager = DockerManager()

def log(response):
    logging.basicConfig(filename='support.log', filemode='w', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    logging.info(response)
    return

def get_open_ports():
    # Esegue il comando 'netstat' per visualizzare le porte aperte
    proc = subprocess.run(['netstat', '-tulpn'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Splitta l'output del comando in linee separate
    lines = proc.stdout.decode('utf-8').split('\n')
    # Inizializza una lista vuota per le porte
    ports = []
    # Per ogni linea dell'output...
    for line in lines:
        # ...se la linea contiene informazioni su una porta aperta...
        if ':*' in line:
            port = filter_ports(line)
            ports.append(port)
    # Restituisci la lista delle porte
    return ports

def filter_ports(line):
    words = line.split()
    port = words[3]
    port = port[1:]
    port = port.split(':', 1)[1]
    if ':' in port:
        port = port.split(':', 1)[1]
    return port

@app.route('/run', methods=['POST'])
def run():
    try:
      image = request.json['image']
      port = request.json['port']
            ports = get_open_ports()
      if port in ports:
        return f'ERRORE: la porta è gia occupata\n'
      container_id = manager.run_container(image, port)
      #process = subprocess.Popen(["doc", "-l"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      #output, errors = process.communicate()
      return f'Container activated: {container_id}'
    except Exception as e:
      return f'ERRORE: {e}\n'

@app.route('/stop', methods=['POST'])
def stop():
    try:
      container_id = request.json['container_id']
      manager.stop_container(container_id)
      return f'Container stopped: {container_id}\n'
    except Exception as e:
      print('errore e qui')
      return f'ERRORE: {e}\n'
      '''
      try:
        log(container_id + ' STOP')
      except:
        print(container_id + ' STOP: it has been impossible to log the event')
      '''
@app.route('/remove', methods=['POST'])
def remove():
    try:
      container_id = request.json['container_id']
      manager.remove_container(container_id)
      log(container_id + ' REMOVED')
      return f'Container removed: {container_id}'
    except Exception as e:
      return f'ERRORE: {e}\n'

@app.route('/log', methods=['POST'])
def log():
    try:
      file = request.json
      current_time = datetime.datetime.now()
      with open('manager_log_' + str(current_time) + '.log', 'w') as f:
        f.write(file)
      return f'Manager Log Has Been Received'
    except Exception as e:
      return f'ERRORE: {e}\n'

@app.route('/list', methods=['POST'])
def list_running_container():
  return manager.list_container()


if __name__ == '__main__':
    print('\n\nAPPLICATION MANAGER HOST\n\n')
    app.run(host='0.0.0.0', port=8080)
  
