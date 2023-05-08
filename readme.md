# ChatRoom

### About
This is a console chat server and client, utilizing TCP. Nicknames in chat are unique, chat can be protected by password (specified in config).

### Server
Server keeps a dictionary of users in format *{ nickname: (client,address) }*. Adding and deleting users done through locks. 
Password and port kept in json config of format *{"host": "localhost","port": 8888,"password": "pass"}*, by default run on *localhost:8888* without password.
Each client handled in different thread.

### Client 
Client expected to run with chat server address in command line adruments: first - host, second - port. Otherwise it connects on *localhost:8888*. 
One thread handles incoming messages, another one - sending messages to the server and another one handles user input. User input thread and message sender thread communicate through Queue.


### Sign-In Flow
Client starts interaction with sending message in format *'NIC<nickname>'*.
If nickname already in use server responds with *'NIC'* message, and client asked to choose another one until unique one is typed. 
Otherwise if password is requered server sends *'PWD'* message, and client asked to enter password until correct one is provided. 
If password is correct or no password requered, server responds with *'SUC'* message, and user joins the chat. Outgoing and incoming messages starts with *'MSG'* prefix.