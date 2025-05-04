# KPS_Final

## 🛠️ How to Run

### 1. Create Virtual Environment
```bash
sudo apt update
python -m venv venv
```

### 2. Install Dependencies
```bash
source venv/bin/activate
sudo apt update
sudo apt install libcamera-dev            # For rpi-libcamera
sudo apt install -y libkms++-dev \
                   libfmt-dev \
                   libdrm-dev             # For rpi-kms
pip install -r requirements.txt

```

### 3.Raspberry Pi Configuration
```bash
sudo raspi-config
```
Navigate to:
``` rust
Interface Options -> I2C -> Enabled
```
Then reboot:
```
sudo reboot
```
<strong>⚠️ If you have a problem with the OLED or LED, please unplug the OLED or LED and plug it back in.</strong>

### 4.Run the Project
``` bash
cd KPS_Final
source venv/bin/activate
python <file_name>.py
```
## File Descriptions
### `collect_data.py`
Use this file to collect new data. You can change the output directory by editing:
```python
output_dir = os.path.expanduser('path/to/save')
```
### `main.py`
Run the model only (no CV or external device interaction).
### `cv_main.py`
Run the model with computer vision (CV) support.
✅ Supports multiple seeds.
### `cv_led_oled_main.py`
Run the model with CV and hardware (LED + OLED) integration.
⚠️ Supports only 1 seed.
