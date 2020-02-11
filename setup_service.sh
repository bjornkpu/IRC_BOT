# Moving service file
sudo cp mentionbot.service /etc/systemd/system/
sudo chown root:root /etc/systemd/system/mentionbot.service
sudo chmod 644 /etc/systemd/system/mentionbot.service

# Setting premissions on script
sudo chmod 644 bot.py

# Reload the changes
sudo systemctl daemon-reload