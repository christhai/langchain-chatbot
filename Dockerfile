FROM python:3.9-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends python3-dev
# Install all python requirements from repository
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

COPY . ./app/

EXPOSE 7860

WORKDIR /app
ENTRYPOINT ["python3","./app.py"]