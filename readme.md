
while ! ping -c1 google.com &>/dev/null; do echo "Ping Fail"; done ; echo "Host Found" ; python3 ~/Desktop/ennea-LED/main.py &