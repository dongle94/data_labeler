# data_labeler
Create data annotation tool for servering


## Installation
- Python 3.10.14
- MariaDB 10.11
  - https://mariadb.org/download/?t=repo-config
- PySide6(PyQt6) 6.7.0
- Image Server
  - seaweedfs (https://github.com/seaweedfs/seaweedfs)


### Python packages
qt-plugin is require
```bash
sudo apt install libxcb-cursor-dev
```

```bash
$ conda create -n label python==3.10.14
$ conda activate label
$ pip install -r ./requirements.txt
```