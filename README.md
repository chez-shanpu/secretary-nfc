# Secretary nfc

## Environment
- python 3.8.x
- pipenv
- nfc reader device

## Usage
1. Setup environment
```shell
$ cd {secretary-nfc_root_dir}
$ pipenv install
```

2. Regrter device for without sudo
```shell
$ sudo vi /etc/udev/rules.d/nfcdev.rules
```

```
# you can check the "idVendor" and "idProduct" with `lsusb`
SUBSYSTEM=="usb", ACTION=="add", ATTRS{idVendor}=={{DEVICE_idVendor}}, ATTRS{idProduct}=={{DEVICE_idProduct}}, GROUP="plugdev"
```

Also you can get messages by `pipenv run python3 -m nfc`

3. Release device from kernel module
```shell
$ sudo sh -c 'echo blacklist port100 >> /etc/modprobe.d/blacklist-nfc.conf'
```

4. Reboot
```shell
$ sudo reboot
```

5. prepare config.yaml

```shell
$ cp config.sample.yaml config.yaml
```

```yaml
# config.yaml
{{ nfc-card id }}: {{ username }}
```

You can check your nfc-card id by running secretary-nfc, touching the card, and checking the log.

6. prepare .env
```shell
$ cp .env.sample .env
```

```
SECRETARY_ENDPOINT=http://localhost/event
```

- `SECRETARY_ENDPOINT`: this is the endpoint of [secretary-lab](https://github.com/chez-shanpu/secretary)


7. Build docker image
```shell
$ docker image build . -t secretary-nfc:latest
```

8. Run secretary-nfc
```shell
$ docker run \
  -v $PWD/config.yaml:/secretary-nfc/config.yaml \
  --device /dev/bus/usb/{{BUS_NUM}}/{DEV_NUM} \
  --env-file .env
  secretary-nfc
```