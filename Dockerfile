FROM python:3.8-slim-buster

RUN pip install websocket-client
RUN pip install requests
RUN pip install rel

COPY system_protection_manager.py /app/

WORKDIR /app

CMD ["python", "system_protection_manager.py"]
