# Application-manager 
## 1. Running Manager
### Application Managare Side
- [x] ``` docker build -t application_manager . ```
- [x] ``` docker run --network host -it -p 5000:5000 application_manager ```
- [x] ``` python3 script.py ```
### Application Manager Host Side
- [x] ``` docker engine installation  ``` https://docs.docker.com/engine/install/ubuntu/
- [x] ``` python3 Support_Manager.py ``` 
## 2. Usage &rarr; DHT Emulator
### Run a Container:
```console
$curl -X POST -H "Content-Type: application/json" -d '{"image": "hello-world"}' http://localhost:5000/run
```
### List Running Containers:
```console
$curl -X POST http://localhost:5000/list
```
### Stop a Container:
```console
$curl -X POST -H "Content-Type: application/json" -d '{"container_id": "bda1903f326e"}' http://localhost:5000/stop
```
### Stop a Container:
```console
$curl -X POST -H "Content-Type: application/json" -d '{"container_id": "bda1903f326e"}' http://localhost:5000/remove
```
### Check Application Manager Log
```console
$curl -X POST http://localhost:5000/check
```
