# CollectDockerTraces
A script to collect and merge tcpdump traces from multiple running Docker containers 

Please adjust temporal and output directories at the beginning of the script according to your own configuration


## Python and other dependencies installation on Ubuntu 20.04

Python install:
```
sudo apt update
sudo apt -y upgrade
python3 -V
```

Python package manager install:
```
sudo apt install -y python3-pip
```

Python library for the Docker Engine API:
```
pip3 install docker
```

