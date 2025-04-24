# KPS_Final
## 1.Create Venv
```
sudo apt update
python -m venv venv
```
## 2. Install Library
```
sudo apt install libcamera-dev # rpi-libcamera
sudo apt install -y libkms++-dev libfmt-dev libdrm-dev # rpi-kms
pip install -r requirements.txt

```

3.Config Pi
```
sudo raspi-config
```
Interface Options -> I2C -> Enabled
