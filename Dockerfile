FROM python:3.8
RUN apt-get update && apt-get install -y \
    libusb-1.0-0-dev \
    && rm -rf /var/lib/apt/lists/*
RUN pip install pipenv
ENV PROJECT_DIR /secretary-nfc
COPY ./ ${PROJECT_DIR}
WORKDIR ${PROJECT_DIR}
RUN pipenv install
CMD ["pipenv", "run", "python", "./main.py", "-p", "config.yaml"]
