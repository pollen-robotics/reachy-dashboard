tee reachy_rap.service <<EOF
[Unit]
Description=Reachy Access Point service
[Service]
ExecStart=/usr/bin/python3.8 $PWD/dashboard/server.py
[Install]
WantedBy=default.target
EOF
