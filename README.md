# GhostLogger_X
Project Name: GhostLogger X

Description (Simple + Editable):

GhostLogger X is a stealth surveillance utility designed for educational and ethical penetration testing. Once deployed, it performs the following tasks silently in the background:

1. Keylogging:
   Captures all keystrokes typed by the user and logs them with timestamps to a hidden file.

2. Screenshot Logging:
   Takes a full screenshot every 2 seconds and stores them in an invisible system folder.

3. Startup Persistence:
   Automatically runs at every system boot by adding itself to the Windows startup registry.

4. USB Exfil Trigger:
   When a specific USB (with serial F6CF-BE46) is plugged in:
   - All keylogs and screenshots are compressed into a password-protected ZIP file.
   - The archive is dumped to the USB.
   - All traces (logs, screenshots, folders) are wiped clean from the user's computer.

5. Password Protection:
   The ZIP file is locked with a password (backgroundcharacter101) ensuring data confidentiality even during transit or storage.

GhostLogger X is a ghost. You won’t know it was ever there.

Steps to Convert Python Script to EXE:
---------------
1. Install PyInstaller:
   Run the following command in your terminal or command prompt:
   pip install pyinstaller

2. Convert Python Script to EXE:
   Navigate to the folder where your Python file (e.g., logger.py) is located.
   Run this command:
   pyinstaller --onefile --noconsole logger.py

3. Find your EXE:
   After the command runs, go to the "dist" folder in your project directory.
   You'll find your EXE file there.
   
Project Credits:  
- Created by BackgroundCharacter101.
