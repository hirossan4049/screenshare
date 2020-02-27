import socket

PORT = 50001
# BUFFER_SIZE = 1500000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('127.0.0.1', PORT))
    s.listen()
    (connection, client) = s.accept()
    all_data = bytes()
    while True:
        try:
            data = connection.recv(1024)
            all_data += data
            if not data:
                print("end data.")
                break
            if len(data) < 1024:
                print("cut data")
            # connection.send(data.upper())
        except:
            print("ERROR")