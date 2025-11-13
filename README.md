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

### Quiet Mode (Beginner-Friendly)

Boot the system with minimal, clean output - perfect for beginners!

```bash
python3 markdownos.py --quiet
```

This will:
1. Boot the system silently
2. Show a clean success message
3. Display key system stats (processes, files, apps)
4. Suggest helpful next commands

**Use quiet mode when:**
- You want a cleaner, less overwhelming experience
- You're new to MarkdownOS
- You don't need detailed boot logs
- You want quick confirmation the system works

### Simulation Mode (Safe Experimentation)

Preview system behavior without making any changes - perfect for learning!

```bash
python3 markdownos.py --simulate
```

This will:
1. Parse kernel.md and desktop.md
2. Show what WOULD happen during boot
3. Display all processes, filesystem changes, and apps that would start
4. Exit without making any actual changes

**Use simulation mode to:**
- Learn how the system works safely
- Preview configuration changes before applying
- Build confidence in understanding system behavior

### Learning Mode (Understanding OS Concepts)

Get instant explanations of operating system concepts in plain English!

```bash
# List all available topics
python3 markdownos.py --explain

# Explain a specific concept
python3 markdownos.py --explain init
python3 markdownos.py --explain pid
python3 markdownos.py --explain filesystem
```

**Available topics**: init, pid, process, filesystem, directory, autostart, command, permissions

**Use learning mode to:**
- Understand OS concepts without searching documentation
- Learn what each configuration option means
- Build foundational knowledge of system internals
- Get context-specific examples from the codebase

### Playground Mode (Learn Kernel Internals)

Learn by breaking things! The playground provides a **persistent interactive shell** where you can experiment with kernel concepts through hands-on challenges.

```bash
# Enter the interactive playground shell
python3 markdownos.py --playground

# Once in the shell, you get a persistent session:
playground> help              # Show all commands
playground> list              # List all challenges
playground> challenge 1       # Start challenge 1
playground> edit              # Edit playground-kernel.md (opens in nano/vim)
playground> boot              # Boot and see results immediately
playground> reset             # Reset to start fresh
playground> hint              # Get hints when stuck
playground> status            # Show system status
playground> exit              # Exit when done
```

**Why Interactive Shell?**
- **Persistent session** - Stay in playground, no need to retype long commands
- **Rapid feedback loop** - Edit → Boot → Observe → Repeat in seconds
- **Built-in editor** - Type "edit" to modify files, returns to shell when done
- **Low overhead** - Short commands (e.g., "boot" not "python3 markdownos.py --playground boot")
- **Exploration-friendly** - Try challenges quickly without context switching
- **Like kernel debugging** - Similar to GDB, kdb, or QEMU console experience

**Quick Example Session:**
```
$ python3 markdownos.py --playground
playground> list
[Shows 5 challenges]
playground> challenge 1
[Shows "Remove init process" task]
playground> edit
[Opens nano with playground-kernel.md, remove init process, save]
playground> boot
[Error: PID 1 required! - Learning achieved!]
playground> reset
[Resets to working state]
playground> exit
```

**5 Challenges Available:**
1. **The Missing Init Mystery** - Learn why PID 1 is essential
2. **PID Collision Course** - Understand PID uniqueness
3. **Permission Puzzle** - Master Unix file permissions
4. **Process Overload** - See how the kernel manages many processes
5. **The Auto-Start Experiment** - Learn process lifecycle control

**How it works:**
- Creates isolated `playground-kernel.md` and `playground-desktop.md` files
- Safe to break - doesn't affect your main system configuration
- Each challenge teaches a kernel concept through intentional failure
- Errors become learning opportunities
- Reset anytime to start fresh
- Interactive shell keeps you in flow state

**One-shot commands** (for scripts/automation):
```bash
python3 markdownos.py --playground list
python3 markdownos.py --playground challenge 1
python3 markdownos.py --playground boot
```

**Use playground mode to:**
- Learn kernel internals by experimenting
- Understand what happens when things go wrong
- Build confidence through hands-on practice
- Master OS concepts through breaking and fixing
- Rapid iteration without leaving your flow

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
├── README.md              # This file
├── VISION.md              # North Star goals and guiding principles
├── ARCHITECTURE.md        # Detailed architecture explanation
├── IMPLEMENTATION_PLAN.md # Detailed roadmap with micro-phases
├── REVIEWERS.md           # Expert review framework
├── kernel.md              # Kernel configuration (processes, filesystem)
├── desktop.md             # Desktop environment configuration
├── markdownos.py          # Runtime interpreter
├── EXAMPLES.md            # Usage examples
└── reviews/               # Review archive for each phase
    ├── README.md
    └── REVIEW_TEMPLATE.md
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

## Development Roadmap

MarkdownOS is actively being developed with a clear vision and roadmap:

### North Star Goal
> "The killer feature isn't markdown itself—it's removing fear from systems programming."

See [VISION.md](VISION.md) for our guiding principles and three pillars:
1. **Learning Platform** - Teach OS concepts safely (Jessie Frazelle perspective)
2. **AI-Native System** - Self-explaining, LLM-friendly (Simon Willison perspective)
3. **Collaboration Tool** - GitOps and team workflows (Kelsey Hightower perspective)

### Current Development

**Phase 1: Foundation - Safe Experimentation** (In Planning)
- Simulation mode for safe testing
- Interactive tutorials for beginners
- Validation and helpful error messages
- Undo functionality
- Progressive disclosure (quiet/verbose modes)

See [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) for detailed micro-phase breakdown.

### Review Process

Every feature is reviewed from three expert perspectives:
- **Kelsey Hightower** - Infrastructure & GitOps
- **Simon Willison** - AI-First Tooling
- **Jessie Frazelle** - Systems Accessibility

See [REVIEWERS.md](REVIEWERS.md) for review framework.

## Contributing

We welcome contributions! Before contributing:

1. Read [VISION.md](VISION.md) to understand our goals
2. Check [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) for current work
3. Follow the review process in [REVIEWERS.md](REVIEWERS.md)

Key principle: Every change should **remove fear from systems programming**.

## License

Experimental project - feel free to use and modify!

## Inspiration

Inspired by the idea that complex systems can be made simple and accessible through good abstractions. What if we could configure an entire OS as easily as writing documentation?

---

*Experiment inspired by Claude's imagination*
