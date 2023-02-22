FROM ubuntu:latest

# Installare Python e Flask
RUN apt-get update && apt-get install -y python3-pip
RUN pip3 install flask
RUN pip3 install requests
RUN apt install nano
RUN apt-get update
RUN apt-get install -y iproute2

# Creare una cartella per il nostro script
RUN mkdir -p /app
WORKDIR /app

# Copiare il nostro script nella cartella appena creata
COPY script.py /app/script.py
COPY manager.log /app/manager.log

# Impostare la porta su cui Flask ascolterà
ENV FLASK_APP=script.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Avviare lo script quando l'immagine viene eseguita
#CMD ["python3", "/app/script.py"]

# TO RUN THE IMAGE
# docker run --network host -it -p 5000:5000 application_manager
