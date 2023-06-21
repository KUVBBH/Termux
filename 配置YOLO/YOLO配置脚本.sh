sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list

apt update

apt-get update

apt install python3 python3-pip

pip install ultralytics -i https://pypi.tuna.tsinghua.edu.cn/simple

sleep 3

apt install libgl1-mesa-glx

apt install libglib2.0-dev