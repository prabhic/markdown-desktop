#!/usr/bin/env python3
"""
MarkdownOS Runtime - A minimal Linux-like system interpreter that reads markdown files.

This runtime parses kernel.md and desktop.md to simulate a Linux kernel and desktop
environment. All system behavior is defined declaratively in markdown files.
"""

import re
import os
import sys
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple


# Educational explanations for OS concepts
EXPLANATIONS = {
    "init": """
The 'init' process is the first program that starts when your system boots.

Think of it like the manager of a company:
- It starts up first (always PID 1)
- It's responsible for starting all other processes
- If init stops, everything else must stop too

In MarkdownOS, init is defined in kernel.md.
Look for "Process: init" with PID 1.

Example: kernel.md lines 16-21
    """,
    "pid": """
PID stands for Process ID - a unique number for each running program.

Like a name tag at a conference:
- Every process gets a number when it starts
- No two processes can have the same PID
- PID 1 is always the init process (it starts first)
- The kernel assigns PIDs in order

In MarkdownOS, you assign PIDs manually in kernel.md.
Each process definition has a "PID" field.

Example: kernel.md - look for "**PID**: 1"
    """,
    "process": """
A process is a running program on your computer.

Think of it like a task on your to-do list:
- Each process does one job
- It has its own memory space
- It can be started, paused, or stopped
- Multiple processes can run at the same time

In MarkdownOS, processes are defined in kernel.md.
Each "Process:" section creates one process.

Example: kernel.md - sections starting with "### Process:"
    """,
    "filesystem": """
A filesystem is how your computer organizes files and directories.

Like a filing cabinet:
- Files contain data (documents, photos, programs)
- Directories are folders that organize files
- Everything has a path (like /home/user/photo.jpg)
- Permissions control who can read/write files

In MarkdownOS, the filesystem is defined in kernel.md.
Look for "Directory:" and "File:" sections.

Example: kernel.md - sections starting with "### Directory:" or "### File:"
    """,
    "directory": """
A directory (also called a folder) is a container for files and other directories.

Like a folder in a filing cabinet:
- Holds files and other directories
- Has a path (like /home or /tmp)
- Can have permissions (who can access it)
- Creates organization in your filesystem

In MarkdownOS, directories are defined in kernel.md.
Each "Directory:" section creates one directory.

Example: kernel.md - look for "### Directory: /home"
    """,
    "autostart": """
Auto-start controls whether a process or application launches automatically at boot.

Like programs that open when you turn on your computer:
- "Auto Start: true" means it starts automatically
- "Auto Start: false" means you start it manually
- Useful for background services (like loggers)
- Not needed for on-demand apps (like calculators)

In MarkdownOS, autostart is defined in both kernel.md and desktop.md.
Look for "**Auto Start**: true" or "**Auto Start**: false"
    """,
    "command": """
A command is the actual program that runs when a process starts.

Like instructions to execute:
- It's usually the name of a program (like "bash" or "nginx")
- Can include arguments (like "echo 'Hello'")
- Tells the system what to do
- Must be a valid executable

In MarkdownOS, commands are defined in kernel.md and desktop.md.
Look for "**Command**:" fields in process/app definitions.

Example: "**Command**: `bash`"
    """,
    "permissions": """
Permissions control who can read, write, or execute files.

Like access levels on a document:
- Read (r): Can view the file
- Write (w): Can modify the file
- Execute (x): Can run the file as a program
- Format: 0644 means owner can write, everyone can read

In MarkdownOS, permissions are defined in kernel.md.
Look for "**Permissions**: 0644" in file definitions.

Example: kernel.md - "**Permissions**: 0644"
    """,
}


class MarkdownParser:
    """Parse markdown files to extract system configuration."""
    
    @staticmethod
    def parse_key_value(text: str, key: str) -> str:
        """Extract value for a key from markdown text."""
        pattern = rf'\*\*{key}\*\*:\s*`?([^`\n]+)`?'
        match = re.search(pattern, text)
        return match.group(1).strip() if match else ""
    
    @staticmethod
    def parse_sections(content: str) -> Dict[str, str]:
        """Parse markdown content into sections by headers."""
        sections = {}
        current_section = "header"
        current_content = []
        
        for line in content.split('\n'):
            if line.startswith('###'):
                if current_content:
                    sections[current_section] = '\n'.join(current_content)
                current_section = line.strip('#').strip()
                current_content = []
            else:
                current_content.append(line)
        
        if current_content:
            sections[current_section] = '\n'.join(current_content)
        
        return sections


class Process:
    """Represents a process defined in kernel.md."""
    
    def __init__(self, name: str, config: str):
        self.name = name
        parser = MarkdownParser()
        self.pid = parser.parse_key_value(config, "PID")
        self.command = parser.parse_key_value(config, "Command")
        self.workdir = parser.parse_key_value(config, "Working Directory")
        self.autostart = parser.parse_key_value(config, "Auto Start").lower() == "true"
        self.description = parser.parse_key_value(config, "Description")
    
    def __repr__(self):
        return f"Process(name={self.name}, pid={self.pid}, cmd={self.command})"


class FileSystemEntry:
    """Represents a file or directory defined in kernel.md."""
    
    def __init__(self, name: str, config: str):
        self.name = name
        parser = MarkdownParser()
        self.type = parser.parse_key_value(config, "Type")
        self.permissions = parser.parse_key_value(config, "Permissions")
        self.owner = parser.parse_key_value(config, "Owner")
        self.description = parser.parse_key_value(config, "Description")
        
        # Extract content for files
        content_match = re.search(r'\*\*Content\*\*:\s*\|?\s*\n\s*```?\n(.*?)\n\s*```', 
                                 config, re.DOTALL)
        if content_match:
            self.content = content_match.group(1).strip()
        else:
            content_match = re.search(r'\*\*Content\*\*:\s*`([^`]+)`', config)
            self.content = content_match.group(1) if content_match else ""
    
    def __repr__(self):
        return f"FSEntry(name={self.name}, type={self.type})"


class Application:
    """Represents an application defined in desktop.md."""
    
    def __init__(self, name: str, config: str):
        self.name = name
        parser = MarkdownParser()
        self.display_name = parser.parse_key_value(config, "Name")
        self.command = parser.parse_key_value(config, "Command")
        self.icon = parser.parse_key_value(config, "Icon")
        self.autostart = parser.parse_key_value(config, "Auto Start").lower() == "true"
        self.category = parser.parse_key_value(config, "Category")
    
    def __repr__(self):
        return f"App(name={self.display_name}, cmd={self.command})"


class MarkdownKernel:
    """The kernel component - manages processes and file system."""

    def __init__(self, kernel_md_path: str):
        self.kernel_md_path = kernel_md_path
        self.processes: List[Process] = []
        self.filesystem: List[FileSystemEntry] = []
        self.system_info = {}

    def validate(self):
        """Validate kernel configuration for common errors."""
        errors = []
        warnings = []

        # Check: No duplicate PIDs
        pids = [int(p.pid) for p in self.processes if p.pid.isdigit()]
        if len(pids) != len(set(pids)):
            pid_counts = {}
            for pid in pids:
                pid_counts[pid] = pid_counts.get(pid, 0) + 1
            duplicates = [pid for pid, count in pid_counts.items() if count > 1]
            errors.append(f"Duplicate PIDs found: {duplicates}")

        # Check: PID 1 must exist
        if 1 not in pids:
            errors.append("PID 1 (init process) is required but not found!")

        # Warning: Large PIDs
        if any(pid > 1000 for pid in pids):
            large_pids = [pid for pid in pids if pid > 1000]
            warnings.append(f"PIDs over 1000 detected: {large_pids}. Consider using smaller numbers.")

        # Check: Processes have required fields
        for proc in self.processes:
            if not proc.pid:
                errors.append(f"Process '{proc.name}' missing PID")
            if not proc.command:
                warnings.append(f"Process '{proc.name}' has no command")

        # Check: Filesystem permissions are valid (basic check)
        for entry in self.filesystem:
            if entry.type == "file" and entry.permissions:
                try:
                    perm_val = int(entry.permissions, 8)  # Octal
                    if perm_val > 0o777:
                        warnings.append(f"File '{entry.name}' has unusual permissions: {entry.permissions}")
                except ValueError:
                    errors.append(f"File '{entry.name}' has invalid permissions: {entry.permissions}")

        return errors, warnings

    def load(self):
        """Load and parse kernel.md."""
        with open(self.kernel_md_path, 'r') as f:
            content = f.read()

        sections = MarkdownParser.parse_sections(content)

        # Parse system information
        if "System Information" in content:
            parser = MarkdownParser()
            self.system_info = {
                'name': parser.parse_key_value(content, "Name"),
                'version': parser.parse_key_value(content, "Version"),
            }

        # Parse processes
        for section_name, section_content in sections.items():
            if section_name.startswith("Process:"):
                process_name = section_name.replace("Process:", "").strip()
                process = Process(process_name, section_content)
                self.processes.append(process)
            elif section_name.startswith("Directory:") or section_name.startswith("File:"):
                entry = FileSystemEntry(section_name, section_content)
                self.filesystem.append(entry)

        # Validate after loading
        errors, warnings = self.validate()
        if errors:
            print("\n⚠️  Configuration Errors Found:")
            for error in errors:
                print(f"  ❌ {error}")
            print()
            sys.exit(1)
        if warnings:
            print("\n⚠️  Configuration Warnings:")
            for warning in warnings:
                print(f"  ⚠️  {warning}")
            print()

        return self
    
    def boot(self):
        """Boot the system - display boot sequence."""
        print("=" * 60)
        print(f"Booting {self.system_info.get('name', 'MarkdownOS')} "
              f"v{self.system_info.get('version', '0.1.0')}...")
        print("=" * 60)
        print()
        
        print("[KERNEL] Loading kernel configuration from kernel.md...")
        print(f"[KERNEL] Found {len(self.processes)} processes")
        print(f"[KERNEL] Found {len(self.filesystem)} filesystem entries")
        print()
        
        # Initialize filesystem
        print("[FS] Initializing virtual file system...")
        for entry in self.filesystem:
            if entry.type == "directory":
                print(f"[FS] Creating directory: {entry.name}")
            elif entry.type == "file":
                print(f"[FS] Creating file: {entry.name}")
        print()
        
        # Start processes
        print("[INIT] Starting system processes...")
        for process in sorted(self.processes, key=lambda p: int(p.pid or "999")):
            if process.autostart:
                print(f"[INIT] Starting {process.name} (PID {process.pid}): {process.description}")
        print()
        
        print("[KERNEL] Boot complete!")
        print("=" * 60)
        print()
    
    def show_status(self):
        """Display system status."""
        print("\n" + "=" * 60)
        print("SYSTEM STATUS")
        print("=" * 60)
        print(f"Name: {self.system_info.get('name', 'Unknown')}")
        print(f"Version: {self.system_info.get('version', 'Unknown')}")
        print(f"\nRunning Processes: {len([p for p in self.processes if p.autostart])}")
        print(f"Filesystem Entries: {len(self.filesystem)}")
        print("\nProcesses:")
        for process in self.processes:
            status = "RUNNING" if process.autostart else "STOPPED"
            print(f"  [{status}] PID {process.pid}: {process.name}")
        print("=" * 60 + "\n")


class MarkdownDesktop:
    """The desktop environment component."""
    
    def __init__(self, desktop_md_path: str):
        self.desktop_md_path = desktop_md_path
        self.applications: List[Application] = []
        self.desktop_info = {}
    
    def load(self):
        """Load and parse desktop.md."""
        with open(self.desktop_md_path, 'r') as f:
            content = f.read()
        
        sections = MarkdownParser.parse_sections(content)
        
        # Parse desktop information
        parser = MarkdownParser()
        self.desktop_info = {
            'name': parser.parse_key_value(content, "Name"),
            'version': parser.parse_key_value(content, "Version"),
        }
        
        # Parse applications
        for section_name, section_content in sections.items():
            if section_name.startswith("Application:"):
                app_id = section_name.replace("Application:", "").strip()
                app = Application(app_id, section_content)
                self.applications.append(app)
        
        # Extract welcome message
        welcome_match = re.search(r'```\n(╔.*?╚[^`]*?)```', content, re.DOTALL)
        if welcome_match:
            self.welcome_message = welcome_match.group(1)
        else:
            self.welcome_message = None
        
        return self
    
    def start(self):
        """Start the desktop environment."""
        print()
        print("=" * 60)
        print(f"Starting {self.desktop_info.get('name', 'MarkdownDE')} "
              f"v{self.desktop_info.get('version', '0.1.0')}...")
        print("=" * 60)
        print()
        
        if self.welcome_message:
            print(self.welcome_message)
            print()
        
        print("[DE] Loading desktop configuration from desktop.md...")
        print(f"[DE] Found {len(self.applications)} applications")
        print()
        
        print("[WM] Initializing window manager...")
        print("[PANEL] Creating top panel...")
        print()
        
        print("[DE] Starting auto-start applications...")
        for app in self.applications:
            if app.autostart:
                print(f"[DE] Starting {app.display_name}: {app.command}")
        print()
        
        print("[DE] Desktop ready!")
        print("=" * 60)
        print()
    
    def show_menu(self):
        """Display application menu."""
        print("\n" + "=" * 60)
        print("APPLICATION MENU")
        print("=" * 60)
        for i, app in enumerate(self.applications, 1):
            print(f"{i}. {app.icon} {app.display_name} [{app.category}]")
            print(f"   Command: {app.command}")
        print("=" * 60 + "\n")


class MarkdownOS:
    """Main system controller."""

    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.kernel = MarkdownKernel(str(self.base_path / "kernel.md"))
        self.desktop = MarkdownDesktop(str(self.base_path / "desktop.md"))

    def simulate_boot(self):
        """Simulate boot without making any changes - preview mode."""
        print("\n")
        print("╔══════════════════════════════════════════════════════════╗")
        print("║              🔍 SIMULATION MODE                          ║")
        print("║         No actual changes will be made                   ║")
        print("╚══════════════════════════════════════════════════════════╝")
        print()

        print("=" * 60)
        print("Simulating System Boot...")
        print("=" * 60)
        print()

        # Load configurations
        print("[SIM] Loading kernel.md...")
        self.kernel.load()
        print(f"[SIM] ✓ Parsed {len(self.kernel.processes)} process definitions")
        print(f"[SIM] ✓ Parsed {len(self.kernel.filesystem)} filesystem entries")
        print()

        print("[SIM] Loading desktop.md...")
        self.desktop.load()
        print(f"[SIM] ✓ Parsed {len(self.desktop.applications)} application definitions")
        print()

        # Show what would happen
        print("[SIM] The following would occur during boot:")
        print()

        print("  Filesystem Initialization:")
        for entry in self.kernel.filesystem:
            action = "Create directory" if entry.type == "directory" else "Create file"
            print(f"    → {action}: {entry.name}")
        print()

        print("  Process Startup:")
        autostart_procs = [p for p in self.kernel.processes if p.autostart]
        for process in sorted(autostart_procs, key=lambda p: int(p.pid or "999")):
            print(f"    → Start {process.name} (PID {process.pid}): {process.command}")
        print()

        print("  Desktop Environment:")
        autostart_apps = [a for a in self.desktop.applications if a.autostart]
        for app in autostart_apps:
            print(f"    → Launch {app.display_name}: {app.command}")
        print()

        print("=" * 60)
        print("✓ Simulation Complete - No changes were made")
        print("=" * 60)
        print()
        print("To actually boot the system, run: python3 markdownos.py")
        print("To see more options, run: python3 markdownos.py --help")
        print()

    def quiet_boot(self):
        """Boot with minimal, beginner-friendly output."""
        # Load configurations silently
        self.kernel.load()
        self.desktop.load()

        # Count what's running
        num_processes = len([p for p in self.kernel.processes if p.autostart])
        num_files = len(self.kernel.filesystem)
        num_apps = len(self.desktop.applications)

        # Show minimal, encouraging output
        print()
        print("╔══════════════════════════════════════════╗")
        print("║      MarkdownOS v0.1.0                   ║")
        print("╚══════════════════════════════════════════╝")
        print()
        print("✓ System booted successfully!")
        print(f"✓ {num_processes} processes running")
        print(f"✓ {num_files} filesystem entries ready")
        print(f"✓ {num_apps} applications available")
        print()
        print("What's next?")
        print("  • Try: markdownos.py --status")
        print("  • Learn: markdownos.py --explain init")
        print()

    def verbose_boot(self):
        """Boot with detailed debugging output."""
        print("\n")
        print("╔══════════════════════════════════════════════════════════╗")
        print("║              🔍 VERBOSE MODE - DETAILED OUTPUT           ║")
        print("╚══════════════════════════════════════════════════════════╝")
        print()

        # Load kernel with detailed output
        print("[VERBOSE] Starting kernel configuration load...")
        print(f"[VERBOSE] Reading file: {self.kernel.kernel_md_path}")
        self.kernel.load()
        print(f"[VERBOSE] ✓ Kernel load complete")
        print(f"[VERBOSE]   - Processes found: {len(self.kernel.processes)}")
        for proc in self.kernel.processes:
            print(f"[VERBOSE]     • {proc.name} (PID {proc.pid}): autostart={proc.autostart}")
        print(f"[VERBOSE]   - Filesystem entries: {len(self.kernel.filesystem)}")
        for entry in self.kernel.filesystem:
            print(f"[VERBOSE]     • {entry.name} (type: {entry.type})")
        print()

        # Load desktop with detailed output
        print("[VERBOSE] Starting desktop configuration load...")
        print(f"[VERBOSE] Reading file: {self.desktop.desktop_md_path}")
        self.desktop.load()
        print(f"[VERBOSE] ✓ Desktop load complete")
        print(f"[VERBOSE]   - Applications found: {len(self.desktop.applications)}")
        for app in self.desktop.applications:
            print(f"[VERBOSE]     • {app.display_name}: autostart={app.autostart}")
        print()

        # Boot kernel with verbose output
        print("[VERBOSE] Starting kernel boot sequence...")
        self.kernel.boot()

        # Start desktop with verbose output
        print("[VERBOSE] Starting desktop environment...")
        self.desktop.start()

        # Detailed summary
        print("[VERBOSE] Boot complete - System summary:")
        print(f"[VERBOSE]   - Total processes: {len(self.kernel.processes)}")
        print(f"[VERBOSE]   - Running processes: {len([p for p in self.kernel.processes if p.autostart])}")
        print(f"[VERBOSE]   - Filesystem entries: {len(self.kernel.filesystem)}")
        print(f"[VERBOSE]   - Desktop apps: {len(self.desktop.applications)}")
        print(f"[VERBOSE]   - Auto-start apps: {len([a for a in self.desktop.applications if a.autostart])}")
        print()

    def boot(self):
        """Boot the complete system."""
        print("\n")
        print("╔══════════════════════════════════════════════════════════╗")
        print("║              MARKDOWN-BASED LINUX SYSTEM                 ║")
        print("║                    Iteration 0                           ║")
        print("╚══════════════════════════════════════════════════════════╝")
        print()

        # Load configurations
        self.kernel.load()
        self.desktop.load()

        # Boot kernel
        self.kernel.boot()

        # Start desktop
        self.desktop.start()

        # Show info
        print("System is ready! Here's what you can do:")
        print()
        print("  • View system status with: --status")
        print("  • View application menu with: --menu")
        print("  • Edit kernel.md to change kernel behavior")
        print("  • Edit desktop.md to change desktop environment")
        print()
        print("This demonstrates how markdown files define system behavior!")
        print()


def run_tutorial():
    """Interactive tutorial for first-time users."""
    import time

    print("\n")
    print("╔════════════════════════════════════════════════════════╗")
    print("║        Welcome to MarkdownOS Tutorial!                ║")
    print("╚════════════════════════════════════════════════════════╝")
    print()
    print("This tutorial will teach you to:")
    print("  1. Understand how MarkdownOS works")
    print("  2. Make your first configuration change")
    print("  3. Boot the system with your changes")
    print()
    print("This is a safe, hands-on learning experience!")
    print("Duration: ~5 minutes")
    print()

    try:
        input("Press Enter to start the tutorial (or Ctrl+C to exit)...")
    except KeyboardInterrupt:
        print("\n\nTutorial cancelled. Come back anytime!")
        return

    # Step 1: Understanding the System
    print("\n" + "=" * 60)
    print("STEP 1/5: Understanding MarkdownOS")
    print("=" * 60)
    print()
    print("MarkdownOS is configured entirely through markdown files.")
    print("There are two main files:")
    print()
    print("  • kernel.md   - Defines processes and filesystem")
    print("  • desktop.md  - Defines desktop applications")
    print()
    print("Everything you see when the system boots is defined in")
    print("these files. No code required - just markdown!")
    print()

    try:
        input("Press Enter to continue...")
    except KeyboardInterrupt:
        print("\n\nTutorial cancelled. Your system is unchanged.")
        return

    # Step 2: Looking at an Existing Process
    print("\n" + "=" * 60)
    print("STEP 2/5: Exploring a Process Definition")
    print("=" * 60)
    print()
    print("Let's look at how a process is defined in kernel.md.")
    print("Here's the 'logger' process:")
    print()
    print("┌─────────────────────────────────────────────┐")
    print("│ ### Process: logger                         │")
    print("│ - **PID**: 3                                │")
    print("│ - **Command**: `echo 'Logger ready'`        │")
    print("│ - **Working Directory**: `/tmp`             │")
    print("│ - **Auto Start**: true                      │")
    print("│ - **Description**: System logging service   │")
    print("└─────────────────────────────────────────────┘")
    print()
    print("Each process has:")
    print("  • A unique PID (Process ID)")
    print("  • A command to run")
    print("  • Auto Start (true = starts on boot)")
    print("  • A description")
    print()

    try:
        input("Press Enter to continue...")
    except KeyboardInterrupt:
        print("\n\nTutorial cancelled. Your system is unchanged.")
        return

    # Step 3: Your First Change
    print("\n" + "=" * 60)
    print("STEP 3/5: Making Your First Change")
    print("=" * 60)
    print()
    print("Now YOU'LL add a new process!")
    print()
    print("We're going to add a 'welcome' process that displays")
    print("a message when the system boots.")
    print()
    print("The process will look like this:")
    print()
    print("┌─────────────────────────────────────────────┐")
    print("│ ### Process: welcome                        │")
    print("│ - **PID**: 10                               │")
    print("│ - **Command**: `echo 'Welcome!'`            │")
    print("│ - **Working Directory**: `/tmp`             │")
    print("│ - **Auto Start**: true                      │")
    print("│ - **Description**: Welcome message          │")
    print("└─────────────────────────────────────────────┘")
    print()
    print("This will be added to your kernel.md file.")
    print()

    try:
        response = input("Ready to add this process? (yes/no): ").strip().lower()
        if response not in ['yes', 'y']:
            print("\nTutorial cancelled. Your system is unchanged.")
            return
    except KeyboardInterrupt:
        print("\n\nTutorial cancelled. Your system is unchanged.")
        return

    # Actually add the process
    print("\nAdding process to kernel.md...")
    time.sleep(0.5)

    kernel_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kernel.md")

    # Read current content
    with open(kernel_path, 'r') as f:
        content = f.read()

    # Check if welcome process already exists
    if "Process: welcome" in content:
        print("✓ The 'welcome' process already exists!")
        print("  (You may have run this tutorial before)")
    else:
        # Add the new process
        new_process = """

### Process: welcome
- **PID**: 10
- **Command**: `echo "Welcome to MarkdownOS!"`
- **Working Directory**: `/tmp`
- **Auto Start**: true
- **Description**: Welcome message for new users
"""

        # Append to file
        with open(kernel_path, 'a') as f:
            f.write(new_process)

        print("✓ Process added successfully!")

    print()

    try:
        input("Press Enter to continue...")
    except KeyboardInterrupt:
        print("\n\nNote: The change has been made to kernel.md")
        print("The system will use this process on next boot.")
        return

    # Step 4: Validating Your Change
    print("\n" + "=" * 60)
    print("STEP 4/5: Validating Your Configuration")
    print("=" * 60)
    print()
    print("Before booting, let's validate the configuration.")
    print("MarkdownOS checks for common errors like:")
    print("  • Duplicate PIDs")
    print("  • Missing required processes (PID 1)")
    print("  • Invalid permissions")
    print()
    print("Running validation...")
    time.sleep(0.5)

    # Load and validate
    base_path = os.path.dirname(os.path.abspath(__file__))
    try:
        os_instance = MarkdownOS(base_path)
        os_instance.kernel.load()
        print("✓ Configuration is valid!")
        print(f"✓ Found {len(os_instance.kernel.processes)} processes")
        print("✓ Your 'welcome' process is ready to boot!")
    except SystemExit:
        print("\n❌ Validation found errors!")
        print("The tutorial will help you fix them.")
        print("Check the error messages above.")
        return

    print()

    try:
        input("Press Enter to continue...")
    except KeyboardInterrupt:
        print("\n\nYour change is saved and validated!")
        return

    # Step 5: Boot and See Your Change
    print("\n" + "=" * 60)
    print("STEP 5/5: Booting Your System")
    print("=" * 60)
    print()
    print("Now let's boot MarkdownOS and see your process in action!")
    print()

    try:
        input("Press Enter to boot the system...")
    except KeyboardInterrupt:
        print("\n\nYou can boot manually later with: python3 markdownos.py")
        return

    print()
    print("Booting in quiet mode to see your process clearly...")
    print()
    time.sleep(1)

    # Boot in quiet mode
    os_instance.quiet_boot()

    # Show completion
    print()
    print("=" * 60)
    print("🎉 TUTORIAL COMPLETE!")
    print("=" * 60)
    print()
    print("Congratulations! You've successfully:")
    print("  ✓ Learned how MarkdownOS works")
    print("  ✓ Added a new process to kernel.md")
    print("  ✓ Validated your configuration")
    print("  ✓ Booted the system with your changes")
    print()
    print("What's next?")
    print("  • Try adding more processes to kernel.md")
    print("  • Explore desktop.md to add applications")
    print("  • Use '--explain' to learn more concepts")
    print("  • Use '--simulate' to preview changes safely")
    print()
    print("You're now a MarkdownOS user! 🚀")
    print()


# Playground challenges
PLAYGROUND_CHALLENGES = {
    1: {
        "title": "The Missing Init Mystery",
        "description": "The init process (PID 1) is missing! Try to boot and see what happens.",
        "task": "Remove the init process from playground-kernel.md and try to boot.",
        "learning": "Why every OS needs an init process (PID 1)",
        "hint": "The init process is the first process that starts. Without it, no other processes can start!",
        "validation": "missing_init",
    },
    2: {
        "title": "PID Collision Course",
        "description": "What happens when two processes fight for the same PID?",
        "task": "Add a new process with PID 2 (same as shell) and try to boot.",
        "learning": "Why PIDs must be unique",
        "hint": "Each process needs its own unique identifier, like people need unique ID numbers.",
        "validation": "duplicate_pid",
    },
    3: {
        "title": "Permission Puzzle",
        "description": "Explore how file permissions work.",
        "task": "Create a file with permission 0000 (no access) and one with 0777 (full access).",
        "learning": "How Unix permissions control file access",
        "hint": "Permissions format: owner-group-others. Each digit: read(4) + write(2) + execute(1).",
        "validation": "permissions",
    },
    4: {
        "title": "Process Overload",
        "description": "Add 10 new processes and watch the system handle them.",
        "task": "Add 10 processes with PIDs 20-29, all with autostart=true.",
        "learning": "How the kernel manages multiple processes",
        "hint": "Copy the existing process template and change PIDs, names, and commands.",
        "validation": "many_processes",
    },
    5: {
        "title": "The Auto-Start Experiment",
        "description": "Understand the difference between autostart and manual start.",
        "task": "Set all processes to autostart=false except init. What happens?",
        "learning": "How autostart controls process lifecycle",
        "hint": "Only processes with autostart=true will run on boot.",
        "validation": "autostart",
    },
}


def print_playground_help():
    """Print help for playground shell commands."""
    print()
    print("Playground Shell Commands:")
    print("  list              - List all challenges")
    print("  challenge <N>     - Start challenge N (1-5)")
    print("  boot              - Boot the playground system")
    print("  reset             - Reset playground to initial state")
    print("  hint [N]          - Show hint (optionally for challenge N)")
    print("  edit [target]     - Edit playground files")
    print("                      'kernel' or 'k' - Edit playground-kernel.md")
    print("                      'desktop' or 'd' - Edit playground-desktop.md")
    print("                      (default: kernel)")
    print("  status            - Show playground system status")
    print("  help              - Show this help")
    print("  exit / quit       - Exit playground shell")
    print()


def run_playground_shell():
    """Interactive playground shell - persistent session."""
    import shutil
    import time

    base_path = os.path.dirname(os.path.abspath(__file__))
    playground_kernel = os.path.join(base_path, "playground-kernel.md")
    playground_desktop = os.path.join(base_path, "playground-desktop.md")

    print("\n")
    print("╔════════════════════════════════════════════════════════╗")
    print("║        🎮 MarkdownOS Playground Shell                 ║")
    print("║        Learn by Breaking Things Safely!               ║")
    print("╚════════════════════════════════════════════════════════╝")
    print()

    # Check if playground files exist
    if not os.path.exists(playground_kernel):
        print("🎉 First time in playground! Creating playground files...")
        create_playground_files()
        print("✓ Playground files created!")
        print()

    print("Welcome to the interactive playground shell!")
    print("Type 'help' for commands, 'exit' to quit.")
    print()
    print("Quick start:")
    print("  • Type 'list' to see all challenges")
    print("  • Type 'challenge 1' to start first challenge")
    print("  • Type 'edit' to modify playground-kernel.md")
    print("  • Type 'boot' to test your changes")
    print()

    # Interactive shell loop
    while True:
        try:
            command_line = input("playground> ").strip()

            if not command_line:
                continue

            parts = command_line.split()
            command = parts[0].lower()
            args = parts[1:] if len(parts) > 1 else []

            if command in ["exit", "quit", "q"]:
                print("\nExiting playground. Happy learning! 🚀\n")
                break

            elif command == "help" or command == "h":
                print_playground_help()

            elif command == "list" or command == "ls":
                playground_list()

            elif command == "challenge" or command == "c":
                if args:
                    try:
                        challenge_num = int(args[0])
                        playground_challenge(challenge_num)
                    except ValueError:
                        print("❌ Challenge number must be an integer (1-5)")
                else:
                    print("❌ Please specify a challenge number")
                    print("Usage: challenge <N>")
                    print("Example: challenge 1")

            elif command == "boot" or command == "b":
                playground_boot()

            elif command == "reset" or command == "r":
                playground_reset()

            elif command == "hint":
                if args:
                    try:
                        challenge_num = int(args[0])
                        playground_hint(challenge_num)
                    except ValueError:
                        playground_hint()
                else:
                    playground_hint()

            elif command == "edit" or command == "e":
                # Determine which file to edit
                target = args[0].lower() if args else "kernel"

                if target in ["kernel", "k"]:
                    editor = os.environ.get('EDITOR', 'nano')
                    print(f"\nOpening playground-kernel.md with {editor}...")
                    print("(Edit the file, save, and return here to continue)\n")
                    subprocess.run([editor, playground_kernel])
                    print("\n✓ Back in playground shell")
                elif target in ["desktop", "d"]:
                    editor = os.environ.get('EDITOR', 'nano')
                    print(f"\nOpening playground-desktop.md with {editor}...")
                    print("(Edit the file, save, and return here to continue)\n")
                    subprocess.run([editor, playground_desktop])
                    print("\n✓ Back in playground shell")
                else:
                    print(f"❌ Unknown target: {target}")
                    print("Valid targets: kernel, desktop")

            elif command == "status" or command == "s":
                # Load and show playground system status
                if os.path.exists(playground_kernel):
                    try:
                        class PlaygroundOS(MarkdownOS):
                            def __init__(self, base_path):
                                self.base_path = Path(base_path)
                                self.kernel = MarkdownKernel(playground_kernel)
                                self.desktop = MarkdownDesktop(playground_desktop)

                        os_instance = PlaygroundOS(base_path)
                        os_instance.kernel.load()
                        os_instance.kernel.show_status()
                    except SystemExit:
                        print("❌ Validation errors found. Fix them and try again.")
                else:
                    print("❌ Playground not initialized. Run 'reset' first.")

            else:
                print(f"❌ Unknown command: {command}")
                print("Type 'help' for available commands")

        except KeyboardInterrupt:
            print("\n\n(Use 'exit' to quit the playground shell)")
            continue
        except EOFError:
            print("\n\nExiting playground. Happy learning! 🚀\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Type 'help' for available commands\n")


def run_playground():
    """Entry point for playground - launches interactive shell."""
    run_playground_shell()


def create_playground_files():
    """Create initial playground configuration files."""
    base_path = os.path.dirname(os.path.abspath(__file__))

    # Create playground-kernel.md
    playground_kernel = os.path.join(base_path, "playground-kernel.md")
    kernel_content = """# MarkdownOS Playground Kernel Configuration

**This is your playground! Break things, experiment, and learn.**

## System Information
- **Name**: MarkdownOS Playground
- **Version**: 0.1.0

---

## Processes

### Process: init
- **PID**: 1
- **Command**: `echo "Playground Init Starting..."`
- **Working Directory**: `/tmp`
- **Auto Start**: true
- **Description**: The init process - first process that starts

### Process: shell
- **PID**: 2
- **Command**: `bash`
- **Working Directory**: `/home/user`
- **Auto Start**: true
- **Description**: Interactive shell for user commands

### Process: logger
- **PID**: 3
- **Command**: `echo "Logger ready" > /tmp/playground.log`
- **Working Directory**: `/tmp`
- **Auto Start**: true
- **Description**: System logging service

---

## Filesystem

### Directory: /home
- **Type**: directory
- **Permissions**: 0755
- **Owner**: root
- **Description**: User home directories

### Directory: /tmp
- **Type**: directory
- **Permissions**: 0777
- **Owner**: root
- **Description**: Temporary files

### File: /etc/hostname
- **Type**: file
- **Permissions**: 0644
- **Owner**: root
- **Content**: `playground`
- **Description**: System hostname

### File: /etc/motd
- **Type**: file
- **Permissions**: 0644
- **Owner**: root
- **Content**: |
  ```
  Welcome to MarkdownOS Playground!
  This is a safe space to experiment.
  ```
- **Description**: Message of the day
"""

    with open(playground_kernel, 'w') as f:
        f.write(kernel_content)

    # Create playground-desktop.md
    playground_desktop = os.path.join(base_path, "playground-desktop.md")
    desktop_content = """# MarkdownOS Playground Desktop Configuration

## Desktop Environment

- **Name**: MarkdownDE Playground
- **Version**: 0.1.0

## Applications

### Application: terminal
- **Name**: Terminal Emulator
- **Command**: `bash`
- **Icon**: 💻
- **Auto Start**: true
- **Category**: System

### Application: editor
- **Name**: Nano Editor
- **Command**: `nano`
- **Icon**: 📝
- **Auto Start**: false
- **Category**: Accessories
"""

    with open(playground_desktop, 'w') as f:
        f.write(desktop_content)


def playground_boot():
    """Boot the playground system."""
    base_path = os.path.dirname(os.path.abspath(__file__))
    playground_kernel = os.path.join(base_path, "playground-kernel.md")
    playground_desktop = os.path.join(base_path, "playground-desktop.md")

    if not os.path.exists(playground_kernel):
        print("❌ Playground not initialized!")
        print("Run: python3 markdownos.py --playground")
        return

    print("\n🎮 Booting Playground System...")
    print()

    # Create temporary MarkdownOS instance with playground files
    class PlaygroundOS(MarkdownOS):
        def __init__(self, base_path):
            self.base_path = Path(base_path)
            self.kernel = MarkdownKernel(playground_kernel)
            self.desktop = MarkdownDesktop(playground_desktop)

    try:
        os_instance = PlaygroundOS(base_path)
        os_instance.quiet_boot()
        print("✓ Playground boot successful!")
        print()
    except SystemExit as e:
        print("\n💥 Playground boot failed!")
        print("This is expected if you're experimenting.")
        print("Check the errors above to learn what went wrong.")
        print()
        print("To reset: python3 markdownos.py --playground reset")
        print()


def playground_reset():
    """Reset playground to initial state."""
    base_path = os.path.dirname(os.path.abspath(__file__))
    playground_kernel = os.path.join(base_path, "playground-kernel.md")
    playground_desktop = os.path.join(base_path, "playground-desktop.md")

    print("\n🔄 Resetting playground...")

    # Remove existing files
    if os.path.exists(playground_kernel):
        os.remove(playground_kernel)
    if os.path.exists(playground_desktop):
        os.remove(playground_desktop)

    # Recreate
    create_playground_files()

    print("✓ Playground reset to initial state!")
    print()
    print("Files restored:")
    print("  • playground-kernel.md")
    print("  • playground-desktop.md")
    print()


def playground_challenge(challenge_num):
    """Start a specific playground challenge."""
    if challenge_num not in PLAYGROUND_CHALLENGES:
        print(f"\n❌ Challenge {challenge_num} not found!")
        print(f"Available challenges: 1-{len(PLAYGROUND_CHALLENGES)}")
        return

    challenge = PLAYGROUND_CHALLENGES[challenge_num]

    print("\n")
    print("=" * 60)
    print(f"CHALLENGE {challenge_num}: {challenge['title']}")
    print("=" * 60)
    print()
    print(f"📚 What you'll learn: {challenge['learning']}")
    print()
    print(f"📋 Your task:")
    print(f"   {challenge['task']}")
    print()
    print("=" * 60)
    print()
    print("Instructions:")
    print("  1. Edit playground-kernel.md as described")
    print("  2. Run: python3 markdownos.py --playground boot")
    print("  3. Observe what happens (errors are learning!)")
    print("  4. Run: python3 markdownos.py --playground hint - if stuck")
    print()
    print("When done, reset with: python3 markdownos.py --playground reset")
    print()


def playground_hint(challenge_num=None):
    """Show hint for current or specified challenge."""
    if challenge_num and challenge_num in PLAYGROUND_CHALLENGES:
        challenge = PLAYGROUND_CHALLENGES[challenge_num]
        print("\n💡 HINT:")
        print(f"   {challenge['hint']}")
        print()
    else:
        print("\n💡 General hints:")
        print("  • Use --playground challenge <N> to start a challenge")
        print("  • Edit playground-kernel.md to make changes")
        print("  • Use --playground boot to test your changes")
        print("  • Errors are your teachers - read them carefully!")
        print("  • Use --playground reset to start fresh")
        print()


def playground_list():
    """List all available challenges."""
    print("\n" + "=" * 60)
    print("PLAYGROUND CHALLENGES")
    print("=" * 60)
    print()

    for num, challenge in PLAYGROUND_CHALLENGES.items():
        print(f"Challenge {num}: {challenge['title']}")
        print(f"  📚 Learn: {challenge['learning']}")
        print(f"  📋 Task: {challenge['task']}")
        print()

    print("Start with: python3 markdownos.py --playground challenge 1")
    print()


def explain_concept(topic: str = None):
    """Explain OS concepts in plain language."""
    if topic is None:
        # List all available topics
        print("\n" + "=" * 60)
        print("MARKDOWNOS LEARNING MODE")
        print("=" * 60)
        print()
        print("Get instant explanations of operating system concepts!")
        print()
        print("Available topics:")
        print()
        for topic_name in sorted(EXPLANATIONS.keys()):
            print(f"  • {topic_name}")
        print()
        print("Usage: python3 markdownos.py --explain <topic>")
        print("Example: python3 markdownos.py --explain init")
        print()
        print("=" * 60 + "\n")
    elif topic.lower() in EXPLANATIONS:
        # Show explanation for specific topic
        topic_lower = topic.lower()
        print("\n" + "=" * 60)
        print(f"EXPLAINING: {topic_lower.upper()}")
        print("=" * 60)
        print(EXPLANATIONS[topic_lower].strip())
        print()
        print("=" * 60)
        print(f"💡 Learn more: Try '--explain' to see all topics")
        print("=" * 60 + "\n")
    else:
        # Unknown topic
        print(f"\n❌ No explanation available for '{topic}'")
        print()
        print("Available topics:")
        for topic_name in sorted(EXPLANATIONS.keys()):
            print(f"  • {topic_name}")
        print()
        print("Usage: python3 markdownos.py --explain <topic>")
        print()


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        command = sys.argv[1]
        base_path = os.path.dirname(os.path.abspath(__file__))

        if command == "--tutorial":
            run_tutorial()
        elif command == "--quiet":
            os_instance = MarkdownOS(base_path)
            os_instance.quiet_boot()
        elif command == "--verbose":
            os_instance = MarkdownOS(base_path)
            os_instance.verbose_boot()
        elif command == "--simulate":
            os_instance = MarkdownOS(base_path)
            os_instance.simulate_boot()
        elif command == "--explain":
            # Get topic if provided
            topic = sys.argv[2] if len(sys.argv) > 2 else None
            explain_concept(topic)
        elif command == "--status":
            os_instance = MarkdownOS(base_path)
            os_instance.kernel.load()
            os_instance.kernel.show_status()
        elif command == "--menu":
            os_instance = MarkdownOS(base_path)
            os_instance.desktop.load()
            os_instance.desktop.show_menu()
        elif command == "--playground":
            # Playground subcommands
            if len(sys.argv) > 2:
                subcommand = sys.argv[2]
                if subcommand == "boot":
                    playground_boot()
                elif subcommand == "reset":
                    playground_reset()
                elif subcommand == "list":
                    playground_list()
                elif subcommand == "challenge":
                    if len(sys.argv) > 3:
                        try:
                            challenge_num = int(sys.argv[3])
                            playground_challenge(challenge_num)
                        except ValueError:
                            print("❌ Challenge number must be an integer")
                    else:
                        print("❌ Please specify a challenge number")
                        print("Usage: python3 markdownos.py --playground challenge <N>")
                elif subcommand == "hint":
                    if len(sys.argv) > 3:
                        try:
                            challenge_num = int(sys.argv[3])
                            playground_hint(challenge_num)
                        except ValueError:
                            playground_hint()
                    else:
                        playground_hint()
                else:
                    print(f"Unknown playground command: {subcommand}")
                    print("Try: python3 markdownos.py --playground")
            else:
                # Main playground entry point
                run_playground()
        elif command == "--help":
            print("MarkdownOS Runtime")
            print()
            print("Usage: python3 markdownos.py [command]")
            print()
            print("Commands:")
            print("  (none)        - Boot the system")
            print("  --tutorial    - Interactive tutorial for first-time users (recommended!)")
            print("  --playground  - Enter playground mode (learn by breaking things!)")
            print("  --quiet       - Boot with minimal output (beginner-friendly)")
            print("  --verbose     - Boot with detailed debugging output")
            print("  --simulate    - Preview boot without making changes (safe mode)")
            print("  --explain     - List all explainable OS concepts")
            print("  --explain <topic> - Explain a specific OS concept (e.g. init, pid)")
            print("  --status      - Show system status")
            print("  --menu        - Show application menu")
            print("  --help        - Show this help")
            print()
            print("Playground Mode (Interactive Shell):")
            print("  --playground           - Enter interactive playground shell")
            print()
            print("  Once in the shell, use these commands:")
            print("    list              - List all challenges")
            print("    challenge <N>     - Start challenge N")
            print("    edit [kernel|desktop] - Edit playground files")
            print("    boot              - Boot playground system")
            print("    reset             - Reset to initial state")
            print("    hint [N]          - Get hints")
            print("    status            - Show system status")
            print("    help              - Show help")
            print("    exit              - Exit playground shell")
            print()
            print("  One-shot commands (for scripts/automation):")
            print("    --playground list      - List all challenges")
            print("    --playground challenge <N> - Start challenge N")
            print("    --playground boot      - Boot playground system")
            print("    --playground reset     - Reset playground to initial state")
            print("    --playground hint [N]  - Get hint for challenge N")
            print()
            print("Output Modes:")
            print("  --quiet: Minimal output (best for beginners)")
            print("  (default): Normal output")
            print("  --verbose: Detailed debugging output (for troubleshooting)")
            print()
            print("Learning:")
            print("  🎓 New to MarkdownOS? Try '--tutorial' for a guided experience!")
            print("  🎮 Learn kernel internals? Try '--playground' to experiment!")
            print("  📚 Learn concepts: '--explain' to see all topics")
            print("  Example: python3 markdownos.py --explain init")
            print()
        else:
            print(f"Unknown command: {command}")
            print("Use --help for usage information")
    else:
        # Default: boot the system
        base_path = os.path.dirname(os.path.abspath(__file__))
        os_instance = MarkdownOS(base_path)
        os_instance.boot()


if __name__ == "__main__":
    main()
