#!/bin/bash
set -e

# Install python-evdev
sudo pacman -S --noconfirm python-evdev

# Install udev rule
sudo cp 99-footpedal.rules /etc/udev/rules.d/
sudo udevadm control --reload
sudo udevadm trigger

# Install systemd service
sudo cp footpedal.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now footpedal.service

# Create restart script for GNOME shortcut
sudo bash -c 'echo "#!/bin/sh" > /usr/local/bin/restart-footpedal'
sudo bash -c 'echo "sudo systemctl restart footpedal.service" >> /usr/local/bin/restart-footpedal'
sudo chmod +x /usr/local/bin/restart-footpedal

# Allow passwordless restart of this service
sudo bash -c 'echo "alex ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart footpedal.service" > /etc/sudoers.d/footpedal'
sudo chmod 440 /etc/sudoers.d/footpedal

echo "Done. Super+Shift+P will restart the foot pedal service."
