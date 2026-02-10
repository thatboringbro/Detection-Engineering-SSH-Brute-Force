# Case Study: Adversary Emulation & SSH Brute-Force Detection

## 🎯 Executive Summary
This project demonstrates an end-to-end security engineering lifecycle: simulating a brute-force attack, engineering the necessary telemetry to witness it, and performing a forensic investigation within a SIEM. By bridging the gap between development and security, I validated a high-fidelity detection pipeline capable of identifying lateral movement and successful unauthorized access.

---

## 🛠️ Phase 1: Custom Adversary Emulation
Instead of using off-the-shelf tools, I developed a custom Python utility to simulate a realistic threat actor TTP (Tactics, Techniques, and Procedures).

* **Logic**: Utilized the `subprocess` module to automate rapid authentication attempts via `sshpass`.
* **Engineering Constraint**: The script was designed to run natively on the SIEM node using only the Python standard library. This minimized the performance footprint on the 16GB RAM host and avoided introducing third-party "noise" into the lab environment.
* **Execution**: Conducted a targeted attack against a monitored Ubuntu MATE endpoint to generate real-time security events.

> **File Path**: `/scripts/ssh-bruteforce-sim.py`

---

## 🛡️ Phase 2: Telemetry Engineering & Kernel Auditing
Standard logging often misses the "how" of an attack. I identified a visibility gap and hardened the Linux auditing subsystem to ensure 100% command-line transparency.

* **The Problem**: Default `auditd` configurations do not capture granular process execution (execve syscalls) by default.
* **The Solution**: Deployed a universal syscall monitor to track all process executions across all user contexts (including root and local users).
* **Implementation**: 
    `sudo auditctl -a always,exit -F arch=b64 -S execve -k user_commands`
* **Result**: Every command run by the adversary (e.g., `whoami`, `id`, `ls /etc/shadow`) is now captured and tagged with the `user_commands` key for instant retrieval.

---

## 🔍 Phase 3: SIEM Investigation & Attribution
With the telemetry pipeline active, I acted as a SOC Analyst to investigate the simulation.



* **Data Correlation**: Ingested `auth.log` and `audit.log` into Splunk via a Universal Forwarder.
* **Field Extraction**: Performed manual Regex field analysis to extract and map the attacker’s source IP (**10.10.10.10**).
* **Detection Success**: 
    * Successfully identified the brute-force cluster in the SIEM.
    * Captured and analyzed the critical `res=success` event, flagging exactly when the adversary gained shell access.
    * Validated host attribution by linking the `USER_LOGIN` event to the specific `auditd` session ID.

> **File Path**: `/screenshots/`

---

## 💡 Real-World Mitigation Recommendations
Based on the findings of this simulation, the following controls should be implemented to harden an enterprise environment:

1.  **Disable Password Authentication**: Enforce Public Key Authentication for all SSH connections to render brute-force attacks mathematically unfeasible.
2.  **Implementation of Fail2Ban**: Configure automated IP blocking after a threshold of failed login attempts.
3.  **MFA Ingress**: Require Multi-Factor Authentication for all remote access to prevent successful credential stuffing from leading to full system compromise.

---

### 🎓 Academic & Professional Alignment
This project applies core logic from my school courses to a cybersecurity context. It serves as a practical application of my **TryHackMe** SOC L1 modules and **Cisco's CyberOps Associate course on NetAcad** studies.
