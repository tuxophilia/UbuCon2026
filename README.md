# Hardware-Aware Runtime Security on Ubuntu

## Workshop Guide: Getting Started with Linux `perf`

This hands-on workshop introduces hardware-aware performance monitoring on Ubuntu. Participants will use Linux `perf` to explore how different workloads affect processor behaviour and how performance measurements can be converted into features for an ML-based ransomware detection system.

> [!NOTE]
> All exercises use benign workloads. You do not need to execute ransomware or other malware to complete this workshop.

## 1. Workshop Goals

By the end of this workshop, you should be able to:

- Set up an Ubuntu environment and navigate it using basic terminal commands.
- Install Linux `perf` and verify that it works.
- Discover the performance events supported by your CPU and operating system.
- Measure and compare simple, compression-intensive, and compute-intensive workloads.
- Recognize the effects of process scheduling, permissions, and virtualization on measurements.
- Understand how performance counter measurements can serve as features in an ML-based ransomware detector.

## 2. Set Up Ubuntu

### 2.1 Choose an Ubuntu Environment

Ubuntu **22.04 LTS** or **24.04 LTS** is recommended. You can use:

- **A physical machine (bare metal):** Typically provides the most direct access to hardware performance counters.
- **A virtual machine (VM):** Convenient for the workshop, although access to physical CPU counters may be limited.
- **An instructor-provided system:** Use this option if one is available.

If you need to install Ubuntu on a physical machine:

1. Download the Ubuntu Desktop LTS ISO from the [official Ubuntu website](https://ubuntu.com/download/desktop).
2. Create a bootable USB drive using a trusted imaging tool.
3. Boot from the USB drive, select **Install Ubuntu**, and follow the prompts.
4. Create your user account, complete the installation, and restart.
5. Sign in and open a terminal using **Ctrl + Alt + T**.

> [!IMPORTANT]
> **Virtual-machine limitation:** A hypervisor may hide or restrict access to the host CPU's performance monitoring unit (PMU). A `perf` command that works on bare metal may fail or expose fewer events inside a VM. Do not alter hypervisor settings or system security policies without administrator approval.

### 2.2 Update Ubuntu

Open a terminal and run:

```bash
sudo apt update
sudo apt upgrade -y
```

- `apt update` refreshes the list of available packages.
- `apt upgrade` installs available updates for installed packages.
- `-y` automatically answers **yes** to confirmation prompts. Review the planned changes first if you are on a managed machine.

### 2.3 Check Your Ubuntu Version, Kernel, and CPU

```bash
lsb_release -a
uname -r
lscpu
```

| Command | What it shows |
| --- | --- |
| `lsb_release -a` | Ubuntu distribution and release information. |
| `uname -r` | The version of the currently running Linux kernel. |
| `lscpu` | CPU architecture, model, logical CPUs, cores, and other processor details. |

**Record these details.** The events available to `perf` depend on the CPU, kernel, permissions, and execution environment.

### 2.4 Practice Basic Terminal Commands

| Command | Purpose |
| --- | --- |
| `pwd` | Print the current working directory. |
| `ls -lh` | List files with human-readable sizes. |
| `cd folder` | Move into a directory named `folder`. |
| `mkdir folder` | Create a directory named `folder`. |
| `whoami` | Display the current username. |
| `man command` | Open the manual for a command; press **q** to exit. |

**Quick exercise:** Create a directory for workshop files, enter it, and confirm your location:

```bash
mkdir -p ~/perf-workshop
cd ~/perf-workshop
pwd
```

## 3. Install and Verify Linux `perf`

Linux `perf` is a performance-analysis tool that can **count events**, **sample execution**, and **profile workloads**. Depending on the system, it can report hardware events (such as CPU cycles, instructions, and cache misses) and software events (such as context switches and page faults).

> [!NOTE]
> Not every event is supported on every machine. Event availability and access depend on the processor, kernel, permissions, and virtualization setup.

### 3.1 Install the Tools

On Ubuntu systems using a generic kernel, start with:

```bash
sudo apt update
sudo apt install linux-tools-common linux-tools-generic
```

- `linux-tools-common` provides common support files for Linux performance tools.
- `linux-tools-generic` is a metapackage for tools associated with Ubuntu's generic kernel.

If `perf` reports that tools matching your **running kernel** are missing, try:

```bash
sudo apt install "linux-tools-$(uname -r)"
```

The exact package names and availability may vary by Ubuntu version, kernel flavour, and configured repositories. If the package cannot be found, ask the workshop instructor or system administrator rather than changing repositories or kernel settings without guidance.

### 3.2 Verify the Installation

Check the installed version:

```bash
perf --version
```

Run a simple measurement:

```bash
perf stat -- sleep 1
```

The `sleep 1` program waits for approximately one second. `perf stat` attempts to collect performance statistics while that command runs. This is an initial check that `perf` can execute; **it does not prove that every hardware counter is accessible**.

Next, list the events that `perf` recognizes:

```bash
perf list
```

The list may contain hardware, software, and kernel-provided event descriptions. An event appearing in `perf list` does not always mean it can be measured successfully in your current environment.

### 3.3 Check `perf` Permissions

Inspect the kernel's performance-monitoring access policy:

```bash
cat /proc/sys/kernel/perf_event_paranoid
```

The returned integer is one part of the kernel's policy for unprivileged `perf` access. Restrictions may also arise from Linux capabilities, containers, or VM/hypervisor settings.

If a measurement fails with a permission or unsupported-event error:

1. Record the full error message.
2. Check whether you are on a physical machine or in a VM.
3. Try the basic `perf stat -- sleep 1` check before requesting access to more specialized hardware events.
4. Ask the instructor or administrator if the exercise requires additional permissions or PMU access.

> [!CAUTION]
> **Do not weaken system security settings just to make an exercise run.** In particular, do not lower `kernel.perf_event_paranoid` or change global security or hypervisor settings on a shared, university-managed, or production machine without administrator approval.

---

**Checkpoint:** Before continuing, make sure you can identify your Ubuntu release and CPU, run `perf --version`, and determine whether a basic `perf stat` command succeeds. If hardware events are unavailable, document the limitation; it is itself an important observation for the workshop.
