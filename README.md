1. Start nats-server message broker \
cd nats-server.exe \
nats-server.exe --js  -c nats.conf
2. Start youtube comments publisher \
cd server \
"C:\Python39\python.exe" nats-youtube.py {nats_server_url} {stream_url}" \
ex.: \
"C:\Python39\python.exe" nats-youtube.py localhost "https://www.youtube.com/watch?v=IgE-DV-" 
3. Start the web subscriber \
cd server \
"C:\Python39\python.exe" nats-web-client.py  
Navigate to: http://127.0.0.1/chat?url={nats_server_url}, ex: http://127.0.0.1/chat?url=localhost 
4. Start nats printer subscriber \
*** Needs to be run in the Virtualbox environment *** \
Prerequirements: 
 - open ubuntu virual machine 
 - bind USB printer to the machine
 - pull this repo

cd client \
python3.9 nats-printer-client.py {nats_server_url} \
ex.: \
python3.9 nats-printer-client.py localhost

====== UPDATE 2022 ======== \
For web portal version: \
python3.9 nats-printer-client2.py localhost
