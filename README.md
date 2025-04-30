# KPS_Final
## Setup env
### 1.Create Venv
```
sudo apt update
python -m venv venv
```
### 2. Install Library
```
sudo apt update
sudo apt install libcamera-dev # rpi-libcamera
sudo apt install -y libkms++-dev libfmt-dev libdrm-dev # rpi-kms
pip install -r requirements.txt

```

### 3.Pi Config 
```
sudo raspi-config
```
```
Interface Options -> I2C -> Enabled
```
```
sudo reboot
```
<p><strong>⚠️ If you have a problem with the OLED or LED, please unplug the OLED or LED and plug it back in.</strong></p>

## File 
### 1. collect_data.py
use to collect the new data
### 2. main.py
this file is use the model only
### 3. cv_main.py
this file is use the model+cv (can use multiple seed)
### 4. cv_led_oled_main.py
this file is use the model+cv and connect to led and oled (can use only 1 seed)
