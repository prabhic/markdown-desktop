# Quick Start Guide

## Welcome to MarkdownOS!

This is a minimal Linux-like system configured entirely through markdown files. Here's how to get started:

## Step 1: Boot Your System

```bash
python3 markdownos.py
```

You'll see:
- The system booting up
- Kernel initialization
- File system creation
- Process startup
- Desktop environment launch

## Step 2: Explore What's Running

### Check System Status
```bash
python3 markdownos.py --status
```

This shows:
- System name and version
- Running processes (init, shell, logger)
- File system entries

### View Available Applications
```bash
python3 markdownos.py --menu
```

This shows:
- Terminal Emulator
- File Browser
- Text Editor
- System Monitor

## Step 3: Make Your First Change

Let's add a new process to the system!

### Edit kernel.md

Open `kernel.md` and add this new section anywhere after the existing processes:

```markdown
### Process: hello-world
- **PID**: 4
- **Command**: `echo "Hello from MarkdownOS!"`
- **Working Directory**: `/tmp`
- **Auto Start**: true
- **Description**: A friendly hello world service
```

### Reboot and See the Change

```bash
python3 markdownos.py
```

Look for your new process in the startup sequence! You'll see:
```
[INIT] Starting hello-world (PID 4): A friendly hello world service
```

### Verify It's Running

```bash
python3 markdownos.py --status
```

You should see 4 running processes now!

## Step 4: Add a Desktop Application

Let's add a calculator app to the desktop.

### Edit desktop.md

Open `desktop.md` and add this new section:

```markdown
### Application: Calculator
- **Name**: Calculator
- **Command**: `bc -l`
- **Icon**: 🔢
- **Auto Start**: false
- **Category**: Utilities
```

### Check the Menu

```bash
python3 markdownos.py --menu
```

Your calculator should now appear in the menu!

## Understanding the System

### Two Essential Linux Features

This system implements the bare minimum that makes Linux "Linux":

1. **Process Management** (kernel.md)
   - Define what programs run
   - Control when they start
   - Manage their execution

2. **File System** (kernel.md)
   - Define directory structure
   - Create files and directories
   - Set permissions

### How It Works

```
┌──────────────┐
│ Edit MD file │
└──────┬───────┘
       │
       ↓
┌──────────────┐
│ Run runtime  │
└──────┬───────┘
       │
       ↓
┌──────────────┐
│ See changes  │
└──────────────┘
```

The `markdownos.py` runtime:
1. Parses the markdown files
2. Interprets the configuration
3. Simulates the system behavior

## More Examples

### Add a New Directory

In `kernel.md`:

```markdown
### Directory: /workspace
- **Type**: directory
- **Permissions**: 0755
- **Owner**: user
- **Description**: Development workspace
```

### Add a New File

In `kernel.md`:

```markdown
### File: /etc/version
- **Type**: file
- **Permissions**: 0644
- **Owner**: root
- **Content**: `MarkdownOS 0.1.0`
- **Description**: System version file
```

### Add a Development Tool

In `desktop.md`:

```markdown
### Application: Git
- **Name**: Git Version Control
- **Command**: `git --version`
- **Icon**: 🔀
- **Auto Start**: false
- **Category**: Development
```

## Tips

1. **Always reboot** after changing kernel.md
2. **Use meaningful names** for processes and applications
3. **Set Auto Start** to true only for essential services
4. **Add descriptions** to document your changes
5. **Use version control** - git track your system changes!

## Next Steps

1. Read [ARCHITECTURE.md](ARCHITECTURE.md) to understand the design
2. Check [EXAMPLES.md](EXAMPLES.md) for more scenarios
3. Experiment with different configurations
4. Create your own custom system!

## Philosophy

> "Configuration should be documentation. Documentation should be configuration."

With MarkdownOS:
- Your system config IS the documentation
- Anyone can read and understand it
- Anyone can modify it (just edit markdown!)
- Changes are tracked (use git!)

## Have Fun!

This is iteration 0 - the bare minimum. It demonstrates the concept. Future iterations could:
- Actually execute processes
- Implement a real virtual filesystem
- Add networking
- Create a GUI desktop
- Support plugins
- And more!

The goal: Make system configuration as simple as writing documentation.

---

**Experiment, learn, and enjoy!** 🚀
