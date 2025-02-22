FROM python:3.13

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    ffmpeg

WORKDIR /src
COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY src/* .

USER 1000

ENTRYPOINT ["python3", "main.py"]
