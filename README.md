# UbuCon2026
HARDWARE-AWARE RUNTIME SECURITY FOR UBUNTU SYSTEMS
1. Workshop goals
Prepare an Ubuntu environment and use basic terminal commands.
Install and verify Linux perf.
Discover hardware performance events supported by the machine.
Measure simple, compression-heavy and computation-heavy workloads.
Understand process scheduling and virtual-machine measurement limitations.
Learn how performance measurements become features for an ML-based ransomware detector.
2. Set up Ubuntu
2.1 Choose an Ubuntu environment
Use Ubuntu 22.04 LTS or 24.04 LTS where possible. Ubuntu can run directly on a computer or inside a virtual machine. Use the workshop machine or VM provided by the instructor if available.
For a physical installation, download the Ubuntu Desktop LTS ISO from the official Ubuntu website.
Create a bootable USB using a trusted imaging tool.
Boot from the USB and select Install Ubuntu. Follow the installer prompts.
Create a user account, complete installation and restart.
Sign in and open Terminal, usually with Ctrl + Alt + T.
Virtual machine note  A hypervisor may hide or restrict physical CPU performance counters from the guest OS. A perf command may work on bare metal but fail or show fewer events inside a VM. Do not change hypervisor or system security settings without administrator approval.


2.2 Update Ubuntu
sudo apt update
sudo apt upgrade -y
apt update refreshes the package lists. apt upgrade installs available updates. The -y option automatically confirms installation prompts.
2.3 Check Ubuntu, kernel and CPU
lsb_release -a
uname -r
lscpu
lsb_release -a shows the Ubuntu release; uname -r shows the running kernel; lscpu displays CPU architecture, model, logical CPUs and core information. Record these details because event availability depends on the hardware and kernel.


2.4 Basic terminal commands
Command
Purpose
pwd
Show the current directory.
ls -lh
List files and readable sizes.
cd folder
Move into a directory.
mkdir folder
Create a directory.
whoami
Show the current username.
man command
Open a command's manual; press q to exit.

3. Install and verify Linux perf
perf is a Linux performance-analysis tool. It can count selected events, record sampled execution profiles and inspect performance behaviour. Available events depend on the CPU, kernel, permissions and virtualisation environment.
3.1 Install perf tools
sudo apt update
sudo apt install linux-tools-common linux-tools-generic
linux-tools-common provides common perf support. linux-tools-generic is suitable for many Ubuntu generic-kernel installations.
If Ubuntu reports that matching kernel tools are missing, try:
sudo apt install linux-tools-$(uname -r)
This requests the tools package matching the currently running kernel. Package names can vary with Ubuntu release and kernel flavour.
3.2 Verify the installation
perf --version
perf stat -- sleep 1
The first command prints the installed perf version. The second measures a one-second sleep. It confirms that perf can start, but does not guarantee that every hardware event is accessible.
3.3 Check perf permissions
cat /proc/sys/kernel/perf_event_paranoid
This value is part of the kernel's perf access policy. Permission errors can also come from container restrictions or hypervisor settings.
Do not change this blindly  Do not lower perf_event_paranoid or change global security settings on a shared, university-managed or production machine. First try a basic user-space measurement and ask the administrator before any policy change.

