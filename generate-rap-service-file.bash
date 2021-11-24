tee rap.service <<EOF
[Unit]
Description=Reachy Access Point service
Wants=network-online.target
After=network.target network-online.target
[Service]
PIDFile=/var/run/rap.pid
ExecStart=/usr/bin/python3.8 $PWD/dashboard/server.py
User=$(whoami)
Group=$(whoami)
Type=simple
[Install]
WantedBy=multi-user.target
EOF
