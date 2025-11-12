# Live Demo: Customizing Your System

This document shows a real example of customizing MarkdownOS by editing markdown files.

## Scenario: Create a Development Environment

Let's transform the base system into a development environment by adding:
1. A code server process
2. Development directories
3. Developer tools in the desktop

## Step 1: Before Changes

Run the system to see the baseline:

```bash
python3 markdownos.py --status
```

Output:
```
Running Processes: 3
  [RUNNING] PID 1: init
  [RUNNING] PID 2: shell
  [RUNNING] PID 3: logger
```

## Step 2: Edit kernel.md

Add development infrastructure to `kernel.md`:

### Add Development Directories

Add these sections to kernel.md:

```markdown
### Directory: /workspace
- **Type**: directory
- **Permissions**: 0755
- **Owner**: user
- **Description**: Development workspace for projects

### Directory: /workspace/code
- **Type**: directory
- **Permissions**: 0755
- **Owner**: user
- **Description**: Source code directory

### File: /workspace/README.md
- **Type**: file
- **Permissions**: 0644
- **Owner**: user
- **Content**: `# Welcome to your workspace!`
- **Description**: Workspace readme
```

### Add Development Processes

Add these process sections:

```markdown
### Process: git-daemon
- **PID**: 10
- **Command**: `git daemon --base-path=/workspace --export-all`
- **Working Directory**: `/workspace`
- **Auto Start**: true
- **Description**: Git server for version control

### Process: dev-server
- **PID**: 11
- **Command**: `python3 -m http.server 8000`
- **Working Directory**: `/workspace/code`
- **Auto Start**: true
- **Description**: Development HTTP server
```

## Step 3: Edit desktop.md

Add development tools to the desktop menu.

Add these application sections to `desktop.md`:

```markdown
### Application: VSCode
- **Name**: Visual Studio Code
- **Command**: `code .`
- **Icon**: 💻
- **Auto Start**: false
- **Category**: Development

### Application: Git
- **Name**: Git Status
- **Command**: `git status`
- **Icon**: 🔀
- **Auto Start**: false
- **Category**: Development

### Application: PythonREPL
- **Name**: Python Interactive
- **Command**: `python3`
- **Icon**: 🐍
- **Auto Start**: false
- **Category**: Development

### Application: NodeREPL
- **Name**: Node.js Interactive
- **Command**: `node`
- **Icon**: 📦
- **Auto Start**: false
- **Category**: Development
```

## Step 4: See the Changes

### Boot the System

```bash
python3 markdownos.py
```

You'll now see:
```
[FS] Creating directory: Directory: /workspace
[FS] Creating directory: Directory: /workspace/code
[FS] Creating file: File: /workspace/README.md

[INIT] Starting git-daemon (PID 10): Git server for version control
[INIT] Starting dev-server (PID 11): Development HTTP server
```

### Check System Status

```bash
python3 markdownos.py --status
```

Output:
```
Running Processes: 5
  [RUNNING] PID 1: init
  [RUNNING] PID 2: shell
  [RUNNING] PID 3: logger
  [RUNNING] PID 10: git-daemon
  [RUNNING] PID 11: dev-server
```

### View Application Menu

```bash
python3 markdownos.py --menu
```

Output now includes:
```
5. 💻 Visual Studio Code [Development]
6. 🔀 Git Status [Development]
7. 🐍 Python Interactive [Development]
8. 📦 Node.js Interactive [Development]
```

## Result

Just by editing two markdown files:
- ✅ Added 3 new directories
- ✅ Created 1 new file
- ✅ Started 2 new services
- ✅ Added 4 new applications

**No programming required. No complex configuration. Just markdown.**

## What This Demonstrates

1. **Declarative Configuration**: Describe what you want, not how to do it
2. **Self-Documenting**: The configuration IS the documentation
3. **Accessible**: Anyone who can edit text can configure the system
4. **Verifiable**: See exactly what changed by comparing markdown
5. **Reversible**: Use git to rollback changes

## Try It Yourself!

Copy the sections above into your kernel.md and desktop.md files, then:

```bash
# See before
python3 markdownos.py --status

# Make the changes (edit the .md files)

# See after
python3 markdownos.py --status
```

## Version Control Your Changes

```bash
# Save this configuration
git add kernel.md desktop.md
git commit -m "Configure development environment"

# Later, revert to base system
git checkout HEAD~1 kernel.md desktop.md
python3 markdownos.py  # Back to base configuration!
```

## What's Next?

Other configurations you could create:
- **Web Server**: Add nginx, database processes
- **Monitoring System**: Add prometheus, grafana
- **Media Server**: Add plex, transmission
- **Home Automation**: Add home-assistant, mqtt
- **Whatever you imagine**: Just edit markdown!

---

This is the power of markdown-based system configuration. The system becomes as flexible and readable as a document.
