import socket

def server_program():
    host = '127.0.0.1'  # 로컬호스트
    port = 9000         # 포트 번호

    # 소켓 생성
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))  # 서버 주소와 포트 바인딩
    server_socket.listen(1)           # 하나의 클라이언트 연결 대기

    print("Server is waiting for a connection...")
    conn, address = server_socket.accept()  # 클라이언트 연결 수락
    print(f"Connection from {address} has been established.")

    while True:
        data = conn.recv(1024).decode()  # 클라이언트로부터 데이터 수신
        if not data:
            break
        print(f"Received from client: {data}")
        conn.send("Acknowledged".encode())  # 클라이언트로 응답 송신

    conn.close()  # 연결 종료
    
    
def client_program():
    host = '127.0.0.1'  # 서버 주소 (로컬호스트)
    port = 9000         # 서버 포트 번호

    # 소켓 생성
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))  # 서버에 연결

    message = input("Enter message to send: ")

    while message.lower().strip() != 'exit':
        client_socket.send(message.encode())  # 메시지 송신
        data = client_socket.recv(1024).decode()  # 서버로부터 응답 수신
        print(f"Server response: {data}")

        message = input("Enter message to send: ")

    client_socket.close()  # 연결 종료

import sys    
if __name__ == '__main__':
    if sys.argv[1].lower() == 's':
        server_program()
    else:
        client_program()