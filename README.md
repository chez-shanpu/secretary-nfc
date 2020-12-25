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

3. Release device from kernel module
```shell
$ sudo sh -c 'echo blacklist port100 >> /etc/modprobe.d/blacklist-nfc.conf'
```

4. Reboot
```shell
$ sudo reboot
```