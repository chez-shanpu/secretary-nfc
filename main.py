import argparse
import binascii
import nfc
import logging
import yaml
import urllib.request
import os
import json

# logging
formatter = '%(levelname)s : %(asctime)s : %(message)s'
logging.basicConfig(level=logging.DEBUG, format=formatter)


class CardReader:
    def __init__(self, yaml_path):
        try:
            with open(yaml_path) as file:
                self.idm_dict = yaml.safe_load(file)
        except Exception as e:
            logging.error('exception occurred while loading YAML: %s', e)
            exit(1)

    def on_connect(self, tag):
        logging.info("Touched card %s", tag)
        self.idm = binascii.hexlify(tag._nfcid)
        idm_str = self.idm.decode('ascii')

        if idm_str in self.idm_dict:
            host = os.environ.get("SECRETARY_HOST")
            endpoint = os.environ.get("SECRETARY_ENDPOINT")
            url = "http://" + str(host) + "/" + str(endpoint)
            headers = {"Content-Type": "application/json"}
            body = {"name": self.idm_dict[idm_str]}
            json_data = json.dumps(body).encode("utf-8")
            request = urllib.request.Request(url, data=json_data, method="POST", headers=headers)
            with urllib.request.urlopen(request) as response:
                response_body = response.read().decode("utf-8")
                logging.info('response body: %s', response_body)
        else:
            logging.info('unknown IDm %s', self.idm)

        return True

    def read_id(self):
        clf = nfc.ContactlessFrontend('usb:054c:06c3')
        try:
            clf.connect(rdwr={
                'on-connect': self.on_connect
            })
        finally:
            clf.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--yaml', default="config.yaml", type=str, help="path to yaml config file")
    args = parser.parse_args()

    yaml_path = args.yaml
    cr = CardReader(yaml_path)
    while True:
        print("Please Touch")
        cr.read_id()
