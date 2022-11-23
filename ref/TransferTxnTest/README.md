1. Install Docker desktop and build a image
    - Ubuntu: 
    1.1 sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    1.2 sudo chmod +x /usr/local/bin/docker-compose
    1.3 sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
2. ./sandbox up
3. python3 -m venv venv
4. pip3 install -r requirements.txt
5. python3 server.py
