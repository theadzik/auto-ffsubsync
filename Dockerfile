FROM python:3.13

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    ffmpeg

WORKDIR /src
COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY src/main.py main.py

USER 10005

ENTRYPOINT ["python3", "main.py"]
