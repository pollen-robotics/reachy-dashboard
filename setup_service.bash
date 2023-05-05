SCRIPT=$(realpath "$0")
SCRIPTPATH=$(dirname "$SCRIPT")

tee reachy_dashboard.service <<EOF
[Unit]
Description=Reachy Dashboard service
[Service]
SyslogIdentifier=reachy_dashboard
ExecStartPre=/bin/sleep 2
ExecStart=/usr/bin/bash $SCRIPTPATH/launch.bash
KillSignal=SIGKILL

[Install]
WantedBy=default.target
EOF

mkdir -p $HOME/.config/systemd/user

mv reachy_dashboard.service $HOME/.config/systemd/user

echo ""
echo "reachy_dashboard.service is now setup."
