#!/bin/python3

server_root_path = "./webserver" # Replace this with your web server's root directory!!!

import socket
import os

def get_file_content(file_path):
    try:
        with open(file_path, 'rb') as file:
            return file.read()
    except FileNotFoundError:
        return None

def handle_request(client_socket):
    #request_data = client_socket.recv(1024)
    # This vvv prevents the slight chance of a buffer overflow in this ^^^ (I think)
    request_data = b""
    while True:
        chunk = client_socket.recv(1024)
        if not chunk:
            break
        request_data += chunk
        if b'\r\n\r\n' in request_data:
            break

    request_str = request_data.decode('utf-8')
    
    print(f"Client Request:\n{request_str}")

    # Extract the requested path from the request
    try:
        requested_path = request_str.split(' ')[1]
    except IndexError:
        requested_path = '/'

    # Set index.html as the default page if a directory is requested
    if requested_path.endswith('/'):
        requested_path += 'index.html'
    
    print(f"Adjusted Requested Path: \"{requested_path}\"")

    # Get the file content
    file_content = get_file_content(server_root_path + requested_path)

    if file_content is not None:
        # Respond with the file content
        response = f"HTTP/1.1 200 OK\nContent-Type: text/html\n\n{file_content.decode('utf-8')}"
    else:
        # Respond with a 404 error if a specific file is requested and it doesn't exist
        response = "HTTP/1.1 404 Not Found\nContent-Type: text/html\n\n<html><body><h1>404 Not Found</h1></body></html>"

    client_socket.sendall(response.encode('utf-8'))
    client_socket.close() # Closes the conenction so it can process next request

def run_server():
    host = '127.0.0.1'
    port = 8080

    # Opens socket and binds it to loopback address port 8080 then starts listening for requests
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Server listening on {host}:{port}")

    # Continously listen for incoming requests
    while True:
        client_socket, client_address = server_socket.accept() # Automatically accepts incoming requests
        print(f"Accepted connection from {client_address}")
        handle_request(client_socket)

if __name__ == "__main__":
    run_server()

