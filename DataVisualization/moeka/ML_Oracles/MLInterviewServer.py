#!/usr/bin/env python3
import socket
import sys
import pickle
import numpy as np

def main():

    print("PASSED IN FILE", sys.argv[2])

    port = int(sys.argv[1])

    # Do this:
    loaded_data = pickle.load(open(sys.argv[2], 'rb'))
    if isinstance(loaded_data, dict) and 'model' in loaded_data:
        model = loaded_data['model']
    else:
        model = loaded_data

    # Create a TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        
        # set up our socket. make it reusable so that we don't have to wait for timeouts. 
        try:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind(('localhost', port))
        except socket.error as e:
            print(f"Failed to bind socket on port {port}: {e}")
            sys.exit(1)

        # Listen for incoming connections
        server_socket.listen(1)
        print(f"Server listening on port {port}...")

        # Wait for a connection
        conn, addr = server_socket.accept()
        with conn:
            print(f"Connected by {addr}")
            
            while True:
                # Receive data (up to 1024 bytes)
                data = conn.recv(1024)
                if not data:
                    print("Client closed the connection.")
                    break

                # Check if the received message is the shutdown flag
                decoded_data = data.decode().strip()
                if decoded_data.lower() == "exit":
                    print("Shutdown flag received. Ending communication.")
                    break

                try:
                    # Assume the client sends a whitespace-separated list of integers
                    numbers = list(map(int, decoded_data.split()))
                    print(f"Received numbers: {numbers}")
                except Exception as e:
                    error_message = f"Error parsing numbers: {e}"
                    print(error_message)
                    conn.sendall(error_message.encode())
                    continue  # Wait for the next message

                # Process the numbers using the model's prediction
                # cast as a 2d array even though it's a 1d array.
                # import numpy as np
                numbers_array = np.array(numbers).reshape(1, -1)
                prediction = int(model.predict(numbers_array)[0])
                print(f"Processed result: {prediction}")

                # Send the result back to the client
                conn.sendall(str(prediction).encode())

            print("Closing connection.")

if __name__ == "__main__":
    main()