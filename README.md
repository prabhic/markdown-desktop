# MarkdownOS - Markdown-Based Linux System

An experimental Linux-like system where **all behavior is defined in markdown files**.

## What is this?

This is a proof-of-concept that demonstrates how an operating system kernel and desktop environment can be configured entirely through human-readable markdown files. Instead of writing C code or complex configuration files, you simply edit markdown documents to define system behavior.

## Core Concept

- **kernel.md** - Defines the kernel: processes, file system, system calls
- **desktop.md** - Defines the desktop environment: applications, window manager, panels
- **markdownos.py** - Runtime interpreter that reads markdown and simulates the system

When you want to change the system, you just edit the markdown files!

## Iteration 0: Bare Minimum

This implementation focuses on the two essential features that make Linux "Linux":

1. **Process Management** - The ability to run and manage programs
2. **File System** - The ability to organize and access data

These are defined declaratively in markdown and interpreted by the runtime.

## Quick Start

### Boot the System

```bash
python3 markdownos.py
```

This will:
1. Parse kernel.md and desktop.md
2. Display the boot sequence
3. Show initialized processes and filesystem
4. Start the desktop environment

### View System Status

```bash
python3 markdownos.py --status
```

Shows running processes and system information.

### View Application Menu

```bash
python3 markdownos.py --menu
```

Lists all available desktop applications.

## Making Changes

### Example 1: Add a New Process

Edit `kernel.md` and add:

```markdown
### Process: my-service
- **PID**: 4
- **Command**: `echo "My custom service"`
- **Working Directory**: `/tmp`
- **Auto Start**: true
- **Description**: My custom background service
```

Reboot the system to see your new process!

### Example 2: Add a New Desktop Application

Edit `desktop.md` and add:

```markdown
### Application: Calculator
- **Name**: Calculator App
- **Command**: `bc`
- **Icon**: 🔢
- **Auto Start**: false
- **Category**: Utilities
```

Check the menu to see your new application!

### Example 3: Add a New File

Edit `kernel.md` and add:

```markdown
### File: /etc/myconfig
- **Type**: file
- **Permissions**: 0644
- **Owner**: root
- **Content**: `my custom configuration`
- **Description**: My configuration file
```

## Architecture

```
User edits markdown → Runtime parses markdown → System behavior changes
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed architecture explanation.

## File Structure

```
markdown-desktop/
├── README.md           # This file
├── ARCHITECTURE.md     # Detailed architecture explanation
├── kernel.md          # Kernel configuration (processes, filesystem)
├── desktop.md         # Desktop environment configuration
├── markdownos.py      # Runtime interpreter
└── EXAMPLES.md        # Usage examples
```

## Why This Matters

This project demonstrates:

1. **Declarative System Configuration** - Describe what you want, not how to do it
2. **Documentation as Code** - Configuration files are self-documenting
3. **Accessibility** - Anyone who can edit markdown can configure the system
4. **Version Control** - Track system changes with git
5. **Simplicity** - No complex syntax or programming required

## Limitations (Iteration 0)

This is a proof-of-concept that:
- Simulates an OS on top of a real OS (doesn't replace the Linux kernel)
- Displays behavior rather than executing actual processes
- Is intentionally minimal to demonstrate the core concept

Future iterations could:
- Actually execute the defined processes
- Implement a real virtual filesystem
- Add networking, user management, etc.
- Create a proper GUI desktop environment

## Philosophy

> "The best interface is no interface. The second best is markdown."

By using markdown:
- System configuration is human-readable documentation
- No special tools required (any text editor works)
- Easy to understand, easy to modify
- Self-documenting by design

## Example Output

```
╔══════════════════════════════════════════════════════════╗
║              MARKDOWN-BASED LINUX SYSTEM                 ║
║                    Iteration 0                           ║
╚══════════════════════════════════════════════════════════╝

============================================================
Booting MarkdownOS v0.1.0...
============================================================

[KERNEL] Loading kernel configuration from kernel.md...
[KERNEL] Found 3 processes
[KERNEL] Found 8 filesystem entries

[FS] Initializing virtual file system...
[FS] Creating directory: Directory: /home
[FS] Creating file: File: /etc/hostname

[INIT] Starting system processes...
[INIT] Starting init (PID 1): The init process
[INIT] Starting shell (PID 2): Interactive shell for user
[INIT] Starting logger (PID 3): System logging service

[KERNEL] Boot complete!
============================================================
```

## Contributing

This is an experimental project. Ideas for improvement:

1. Add more system calls to kernel.md
2. Implement actual process execution
3. Create a real virtual filesystem layer
4. Add networking configuration
5. Implement user management
6. Create a graphical desktop version
7. Add package management via markdown

## License

Experimental project - feel free to use and modify!

## Inspiration

Inspired by the idea that complex systems can be made simple and accessible through good abstractions. What if we could configure an entire OS as easily as writing documentation?

---

*Experiment inspired by Claude's imagination*
