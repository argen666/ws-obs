1. Start nats-server message broker \
cd nats-server.exe \
nats-server.exe --js
2. Start youtube comments publisher \
cd server \
"C:\Python39\python.exe" nats-youtube.py {nats_server_url} {stream_url}" \
ex.: \
"C:\Python39\python.exe" nats-youtube.py localhost "https://www.youtube.com/watch?v=IgE-DV-"
3. Start nats printer subscriber \
*** Needs to be run in the Virtualbox environment *** \
Prerequirements: 
 - open ubuntu virual machine 
 - bind USB printer to the machine
 - pull this repo

cd client \
python3.9 nats-printer-client.py {nats_server_url} \
ex.: \
python3.9 nats-printer-client.py localhost