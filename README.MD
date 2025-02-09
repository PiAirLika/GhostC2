
#  👻 GhostC2

  

##  🔍 Overview

  

GhostC2 is an advanced, stealthy multi-client remote management system. Built with Python, it provides seamless, invisible remote access and management capabilities.

  

##  🚀 Features

  

- 🥷 **Invisible Remote Management**

- Minimal system footprint

- No visible console

- Self-cleanup mechanism

  

- 🌐 **Multi-Client**

- Centralized server control

- Simultaneous client management

- Dynamic client connection handling


- 💻 **Flexible Operations**

- Remote command execution

- Directory navigation

- System information retrieval

  

##  🛠️ Technical Architecture

  

###  Components

-  `ghostserver.py`: Central management server

-  `ghostclient.py`: Lightweight remote client agent

-  `delete.py`: Automated cleanup and self-destruction module

-  `compiler.py`: Executable compilation utility

  

###  Technologies

-  **Language**: Python 3.8+

-  **Communication**: Custom TCP Socket Protocol

-  **Platform**: Windows

-  **Compilation**: PyInstaller

  

##  📦 Prerequisites

- Python 3.8 or higher
- PyInstaller
 
##  🔧 Installation & Setup

  

1. Clone the repository

```bash

git clone https://github.com/piairlika/GhostC2.git

cd GhostC2

```
 

2. Configure Server

- Edit `ghostclient.py` to set your server IP

```python

server_ip =  'XX.XX.XX.XX'  # Your server's IP

server_port =  12345

```  

3. Compile Executables

```bash

python compiler.py

```
### ⚠️ Warning :   
If you want to rename the client, change the `delete.py` code for optimal deletion.
  

##  🚀 Usage

  

###  Server

```bash

python  ghostserver.py

```
  
###  Client Deployment

1. Compile client executable using `compiler.py`

2. Deploy to target machines

3. Clients will automatically connect to the server

https://github.com/user-attachments/assets/a93a497b-523a-4d51-bcb4-dd1f5c9ccc1e

##  ⚠️ Legal Disclaimer

  

This tool is strictly for educational purposes. Unauthorized access or use is a violation of computer crime laws. The developer assumes no liability for misuse.

  

##  🌟 Author

  

- piairlika

  

---
