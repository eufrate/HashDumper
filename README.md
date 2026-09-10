# HashDumper

A Python script to extract Windows password hashes, LSA secrets, and OS version information from an offline Windows partition. It is intended to be used on a (preferably) Kali live USB.

## Overview

HashDumper automates the following steps:

1. Verifies required dependencies (`impacket-secretsdump`, `hivexget`).
2. Prompts for the Windows partition device (e.g., `/dev/nvme0n1p3`).
3. Detects the filesystem type (NTFS, VFAT, exFAT) and mounts it read-only to `/mnt/windows`.
4. Copies the registry hive files (`SYSTEM`, `SAM`, `SECURITY`, `SOFTWARE`) to `/tmp/dump/` to avoid permission and hibernation issues.
5. Extracts the boot key from the `SYSTEM` hive using `impacket-secretsdump`.
6. Dumps local SAM hashes and LSA secrets from the copied hives.
7. Extracts Windows version details (`ProductName`, `CurrentVersion`, `CurrentBuild`) from the `SOFTWARE` hive using `hivexget`.
8. Saves all output to `dump.txt`.
9. Unmounts the partition safely.
10. Checks if the Administrator hash (RID 500) was successfully extracted.

## Requirements

- Python 3
- `impacket-scripts` (provides `impacket-secretsdump`)
- `libhivex-bin` (provides `hivexget`)
- `ntfs-3g` (for mounting NTFS partitions)
- Root privileges (the script uses `sudo` for mounting and copying)
- Debian environment (tested on Kali Linux)

## Installation

Install the required packages:

```bash
sudo apt update
sudo apt install -y impacket-scripts libhivex-bin ntfs-3g
```

Clone or download the script:

```bash
git clone <repository-url>
cd HashDumper
```

## Usage

Run the script with root privileges:

```bash
sudo python3 hashdumper.py
```

The script will guide you through the process:

1. It checks for missing dependencies and offers to install them.
2. It creates `/mnt/windows` and `/tmp/dump` if they do not exist.
3. It lists available disks with `fdisk -l`.
4. You are prompted to enter the partition device name (e.g., `nvme0n1p3` or `sda2`).
5. The script mounts the partition read-only, copies the registry hives, and performs the extraction.
6. After completion, it unmounts the partition and reports success or failure.

## Output

The extracted data is written to `dump.txt` in the current working directory. The file contains:

- `SAM` – local user hashes (NTLM/LM)
- `SECURITY` – LSA secrets (cached domain credentials, service passwords, etc.)
- `ProductName` – Windows edition (e.g., `Windows 10 Pro`)
- `CurrentVersion` – kernel version (e.g., `6.3`)
- `CurrentBuild` – build number (e.g., `19045`)

Example output format:

```
SAM = Administrator:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::

SECURITY = $MACHINE.ACC: ...
...

ProductName = Windows 10 Pro

CurrentVersion = 6.3

CurrentBuild = 19045
```

## Notes

- The script mounts the Windows partition read-only (`-o ro`), so it is safe to use even if Windows is hibernated or has Fast Startup enabled.
- Administrator privileges are required for mounting and copying files.
- The boot key is extracted from the `SYSTEM` hive and truncated to 32 hexadecimal characters (the `0x` prefix is removed).
- If `impacket-secretsdump` or `hivexget` are not found, the script offers to install them automatically.
- The script supports NTFS, VFAT, and exFAT filesystems.

## Troubleshooting

- **`Command not found: impacket-secretsdump`**  
  Ensure `impacket-scripts` is installed. The script attempts to install it if missing.

- **`Command not found: hivexget`**  
  Ensure `libhivex-bin` is installed. The script attempts to install this too if it doesn't detect it.

- **`mount: unknown filesystem type 'ntfs-3g'`**  
  Install `ntfs-3g` (`sudo apt install ntfs-3g`).

- **`No such file or directory` when accessing registry hives**  
  Verify that the partition is mounted correctly and that the path `/mnt/windows/Windows/System32/config/` exists. Use `ls` to check.

- **Empty or missing output in `dump.txt`**  
  Check the error messages in the file. Common causes: missing boot key, corrupted hives, or insufficient permissions.

## Legal Disclaimer

This tool is intended for authorized security testing and forensic analysis only. Use it only on systems you own or have explicit written permission to examine. Unauthorized access to computer systems is illegal.
