mbm3000
=======

Intel IoTLab 2014 prototype

Install on Server
-----------------

clone this repo to somewhere on an internet-connected server.

create a new virtualenv or just install everything in requirements.txt into the
global package dirs:

pip install -r requirements.txt

Install redis on the server (apt-get install redis).

Install on Edison
-----------------

Copy everything in this repository's edison/ subdir to the edison. Make .sh-files executable if necessary.
Copy mbm3000.service to /etc/systemd/system. The run systemctl enable mbm3000.

Connect servo to pin D3.
