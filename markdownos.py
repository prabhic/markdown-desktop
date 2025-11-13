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

        if command == "--quiet":
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
        elif command == "--help":
            print("MarkdownOS Runtime")
            print()
            print("Usage: python3 markdownos.py [command]")
            print()
            print("Commands:")
            print("  (none)        - Boot the system")
            print("  --quiet       - Boot with minimal output (beginner-friendly)")
            print("  --verbose     - Boot with detailed debugging output")
            print("  --simulate    - Preview boot without making changes (safe mode)")
            print("  --explain     - List all explainable OS concepts")
            print("  --explain <topic> - Explain a specific OS concept (e.g. init, pid)")
            print("  --status      - Show system status")
            print("  --menu        - Show application menu")
            print("  --help        - Show this help")
            print()
            print("Output Modes:")
            print("  --quiet: Minimal output (best for beginners)")
            print("  (default): Normal output")
            print("  --verbose: Detailed debugging output (for troubleshooting)")
            print()
            print("Learning:")
            print("  Try '--explain' to see what you can learn!")
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
