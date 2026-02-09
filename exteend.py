#!/usr/bin/env python3

import subprocess
import os
import re
import sys
import time
import shutil

def check_adb_status():
   print("[*] Checking ADB device status and permissions...")
   output = subprocess.check_output("adb devices", shell=True).decode('utf-8').strip().split('\n')
   time.sleep(1)
   
   devices = output[1:]
   
   if not devices or devices[0].strip() == "":
      print("[!] Fatal: No device connected via USB.")
      sys.exit(1)
         
   device_info = devices[0].split()
   device_id = device_info[0]
   status = device_info[1]

   if status == "unauthorized":
      print(f"[!] Warning: Device {device_id} is Unauthorized.")
      sys.exit(1)
   elif status == "device":
      print(f"[+] Device {device_id} is connected and Debugging is Active.")
      return True
   else:
      print(f"[!] Unknown status: {status}")
      sys.exit(1)

def check_connectivity():
   print(f"[*] Checking Wifi Status...")
   output_wifi = subprocess.check_output("adb shell settings get global wifi_on", shell=True).decode('utf-8').strip()
   time.sleep(0.5)
   if output_wifi == '1':
      print(f"[-] Turning Off Wifi...")
      os.system("adb shell svc wifi disable")
      time.sleep(0.5)
      
   print(f"[*] Checking Mobile Data Status...")
   output_data = output_wifi = subprocess.check_output("adb shell settings get global mobile_data", shell=True).decode('utf-8').strip()
   time.sleep(0.5)
   if output_data == '1':
      print(f"[-] Turning Off Mobile Data...")
      os.system("adb shell svc data disable")
      time.sleep(0.5)

def check_connected_hdmi():
   cmd = "xrandr | grep 'HDMI' | grep ' connected' | awk '{print $1}'"
   connected_hdmi = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
   time.sleep(0.5)
   
   if connected_hdmi:
      print(f"[*] {connected_hdmi} Connected")
   else:
      print(f"[!] Disconnected. Check your HDMI port")
      sys.exit(1)

def get_usb_tethering_ipv4():
   print(f"[*] Activating USB Tethering...")
   os.system("adb shell svc usb setFunctions rndis")
   time.sleep(5)
   
   cmd = "ip -4 addr show | grep -E 'enx|usb' | grep 'inet ' | awk '{print $2}' | cut -d/ -f1"
   print("[*] Getting IPv4 USB Tethering...")
   ipv4 = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
   time.sleep(0.5)
   
   if ipv4:
      print(f"[*] IPv4 USB Tethering: {ipv4}")
      return ipv4
   
   print(f"[!] IPv4 Not Found")
   sys.exit(1)

def main():
   try:
      check_adb_status()
      check_connectivity()
      check_connected_hdmi()
      
      ipv4 = get_usb_tethering_ipv4()
      raw_url = ''
      
      if shutil.which("xclip"):
         input(f"\nPress enter when URL has copied...").strip()
         raw_url = subprocess.check_output("xclip -selection clipboard -o", shell=True).decode('utf-8').strip()
         time.sleep(0.5)
      else:
         raw_url = input(f"[?] Paste URL from Deskreen: ")
      
      
      match = re.search(r'/(\d{6})', raw_url)
      if not match:
         print(f"[!] Code not found in link. Check your URL again")
         return 0
      
      code = match.group(1)
      final_url = f"http://{ipv4}:3131/{code}"
      package_name = "de.ozerov.fully"
      
      print(f"[*] Re-routed URL: {final_url}")
      time.sleep(0.5)
      print(f"[*] Launching Fully Kiosk Browser...")
      time.sleep(0.5)
      os.system(f"adb shell am start -a android.intent.action.VIEW -d '{final_url}' {package_name}")
      time.sleep(0.5)
      
      input(f"[+] Script Finished, Return to Deskreen App...")
      os.system('clear')
   except KeyboardInterrupt:
      print(f"\n[-] Script Stopped")
      
   except Exception as e:
      print(f"[!] Error: {e}")
      
if __name__ == "__main__":
   main()