# Extendroid for Linux
Zero-latency Linux screen extension via Android USB Tethering and Deskreen. Requires an HDMI Dummy Plug for optimal rendering performance. Includes an automation script to simplify the entire setup process.

In Display Settings on linux, You can using second screen as vertical or horizontal, choose resolution and fps. Thanks to HDMI Dummy Plug which tricks the OS into detecting a second screen and creates a canvas as if we were using a monitor. However, the canvas is not yet visible because there is no device to display it. But it exists in the system. This is where Deskreen comes in. By directing the capture to HDMI, we can see the screen display.

## Requirements
- HDMI Dummy Plug
- ADB (Android Debug Bridge)
- XClip (Optional but Recommended)
- USB Cable that support transfer data
- Fully Kiosk Browser App (Download in [PlayStore](https://play.google.com/store/apps/details?id=de.ozerov.fully))
- Deskreen Community Edition Desktop ([link](https://deskreen.com/download/))

## Environtment Test
- Linux Mint Zara 22.3 x86_64 with AMD Ryzen 5 6600H with AMD ATI Radeon 660M Integreted GPU
- HyperOS 2.0 with Android 15 Tab

## Step:
**1.)** Download and install requirement package and app
```bash
sudo apt install adb android-tools-adb android-tools-fastboot xclip
```

**2.)** Activate USB Debug in settings depend your devices. On my device on `About Phone` and click 7x `OS Version`. Open `Additional Settings` -> `Developer Option` -> turn on USB debugging.
  
**3.)** Download Automation Script
```bash
curl -L https://raw.githubusercontent.com/oujisan/extendroid-linux/main/extendroid.py
```

**4.)** Give execution permission
```
sudo chmod +x extendroid.py
```

**5.)** Put script globally. choose one between `~/.bashrc` or `/usr/local/bin`
- Using `~/.bashrc` 
`Open `.bashrc` with text editor and add this line in bottom

```bash
alias extendroid='python3 [PATH TO YOUR FILE]/extendroid.py'
```

  reload configuration
```bash
source ~/.bashrc
```

- Using `/usr/local/bin`
	Move `extendroid.py` to `/usr/local/bin/` and delete `.py` extension at filename

```bash
sudo mv [PATH TO YOUR FILE]/extendroid.py /usr/local/bin/extendroid
```

  reload configuration
```bash
hash -r
```

**6.)** Connect Android and Desktop with USB cable and open Deskreen app

**7.)** Run script to auto-setup
```bash
extendroid
```

```bash
oujisan@fumori:~$ extendroid
[*] Checking ADB device status and permissions...
[+] Device of9tvc7t4pge95xw is connected and Debugging is Active.
[*] Checking Wifi Status...
[*] Checking Mobile Data Status...
[*] HDMI-A-0 Connected
[*] Activating USB Tethering...
setCurrentFunctions opId:1
[*] Getting IPv4 USB Tethering...
[*] IPv4 USB Tethering: 10.80.58.77

Press enter when URL has copied...
```

**8.)** Open Deskreen, click the blue box below to copy the URL.
<img width="940" height="672" alt="image" src="https://github.com/user-attachments/assets/f3bfcfbb-bb6a-4513-b94d-812cf5a0f07f" />

Return to script, press enter to continue. make sure lastet clipboard is copied the url.
 
```bash
Press enter when URL has copied...
[*] Re-routed URL: http://10.80.58.77:3131/104279
[*] Launching Fully Kiosk Browser...
Starting: Intent { act=android.intent.action.VIEW dat=http://10.80.58.77:3131/... pkg=de.ozerov.fully }
[+] Script Finished, Press Enter and Return to Deskreen App...
```

Script is finished, Your android device will automaticly open fully kiosk browser with that url. Check your android and clik "Allow" to continue

**9.)** in Deskreen Desktop, clik Allow to give permission connection with your android device.
<img width="940" height="672" alt="image" src="https://github.com/user-attachments/assets/45b635db-8a0d-4cd8-85e0-cb4623eaafd1" />

**10.)** Choose Entire Screen -> Screen 2. Now in your android device will displayed the screen, click fullscreen icon for best experience. Enjoy your screen

## NB:
- To disconnect, just plug off your usb cable, use the script when you wanna conenct again.
- I recomended choose fit resolution to your tablet, in this case my tab have same resolution with my laptop (1920x1200 60fps).

## IMPORTANT
**THE SCRIPT ONLY WORK WELL WITH ALL DEPEDENCY ABOVE** (Because i only prepare for that), feel free to modified the script to suit your needs.
If you dont wanna use the script, do it yourself manually from turn on USB Tethering, turn off wifi and mobile data, note IP from tethering, copy 6 code number from deskreen and open it on your browser every time you wanna connect.

## What Script Do?
- Check the ADB status and permission
- Check the HDMI status
- Check the status of Wi-Fi and mobile data connectivity; if enabled, it will be disabled
- Enable USB Tethering and obtain its IPv4 address
- If you already have the `xclip` package, you can directly copy the URL to the clipboard and the script will read from the clipboard. If not, you need to paste it manually into the terminal.
- Assembling the appropriate URL
- Automatically open the `Fully Kiosk Browser` application via ADB with the assembled URL above

## Why You Need Script?
- Every time you disconnect, the 6-digit code from Deskreen changes. You must manually enter it each time.
- The IP address from USB Tethering also changes every time it disconnects from the desktop.
- USB Tethering mode will not turn on automatically when the USB is connected to the tablet.
- Open browser everytime wanna connected, write IP and code that change every disconnected.
