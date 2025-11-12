# MarkdownOS Examples

This document provides practical examples of how to use and customize MarkdownOS.

## Example 1: Booting the System

### Step 1: Boot
```bash
cd /path/to/markdown-desktop
python3 markdownos.py
```

### Expected Output
You'll see:
1. Boot banner
2. Kernel loading messages
3. Filesystem initialization
4. Process startup sequence
5. Desktop environment startup
6. Welcome message

## Example 2: Adding a New Background Service

### Scenario
You want to add a log monitoring service to your system.

### Steps

1. Open `kernel.md`
2. Add a new process section:

```markdown
### Process: log-monitor
- **PID**: 10
- **Command**: `tail -f /var/log/system.log`
- **Working Directory**: `/var/log`
- **Auto Start**: true
- **Description**: Real-time log monitoring service
```

3. Save the file
4. Reboot the system: `python3 markdownos.py`
5. View status: `python3 markdownos.py --status`

### Result
Your new log monitoring service will appear in the process list!

## Example 3: Customizing the Desktop

### Scenario
You want to add a music player application to your desktop.

### Steps

1. Open `desktop.md`
2. Add a new application section:

```markdown
### Application: Music
- **Name**: Music Player
- **Command**: `mpg123`
- **Icon**: 🎵
- **Auto Start**: false
- **Category**: Media
```

3. Save the file
4. Restart desktop: `python3 markdownos.py`
5. View menu: `python3 markdownos.py --menu`

### Result
Music Player appears in your application menu!

## Example 4: Creating a Development Environment

### Scenario
Configure your system as a development environment.

### Modify kernel.md

Add development directories:
```markdown
### Directory: /workspace
- **Type**: directory
- **Permissions**: 0755
- **Owner**: user
- **Description**: Development workspace

### Directory: /workspace/projects
- **Type**: directory
- **Permissions**: 0755
- **Owner**: user
- **Description**: Project files
```

Add development processes:
```markdown
### Process: code-server
- **PID**: 20
- **Command**: `code-server --port 8080`
- **Working Directory**: `/workspace`
- **Auto Start**: true
- **Description**: VS Code server for remote development
```

### Modify desktop.md

Add development tools:
```markdown
### Application: IDE
- **Name**: Code Editor
- **Command**: `code`
- **Icon**: 💻
- **Auto Start**: false
- **Category**: Development

### Application: Git
- **Name**: Git Client
- **Command**: `git status`
- **Icon**: 🔀
- **Auto Start**: false
- **Category**: Development

### Application: Terminal
- **Name**: Developer Terminal
- **Command**: `bash`
- **Icon**: ⌨️
- **Auto Start**: true
- **Category**: Development
```

## Example 5: Minimal Server Configuration

### Scenario
Configure the system as a minimal web server.

### kernel.md Configuration

```markdown
### Process: nginx
- **PID**: 50
- **Command**: `nginx -g 'daemon off;'`
- **Working Directory**: `/var/www`
- **Auto Start**: true
- **Description**: Web server

### Directory: /var/www
- **Type**: directory
- **Permissions**: 0755
- **Owner**: www-data
- **Description**: Web root directory

### File: /var/www/index.html
- **Type**: file
- **Permissions**: 0644
- **Owner**: www-data
- **Content**: |
  ```
  <html>
    <body>
      <h1>MarkdownOS Web Server</h1>
      <p>Configured via markdown!</p>
    </body>
  </html>
  ```
- **Description**: Default web page
```

### desktop.md Configuration

Keep it minimal - remove auto-start applications:
```markdown
### Application: WebAdmin
- **Name**: Web Administration
- **Command**: `curl http://localhost`
- **Icon**: 🌐
- **Auto Start**: false
- **Category**: System
```

## Example 6: Checking System Status

### View Running Processes
```bash
python3 markdownos.py --status
```

Output shows:
- System name and version
- Number of running processes
- Filesystem entries
- Process list with PID and status

### View Available Applications
```bash
python3 markdownos.py --menu
```

Output shows:
- All available applications
- Their icons and categories
- Commands they execute

## Example 7: Version Controlling Your System

### Initialize Git Repository
```bash
git init
git add kernel.md desktop.md
git commit -m "Initial system configuration"
```

### Make Changes
Edit `kernel.md` to add a new process.

### Track Changes
```bash
git diff kernel.md
git commit -am "Added backup service"
```

### Rollback
```bash
git checkout HEAD~1 kernel.md
python3 markdownos.py  # System reverted!
```

## Example 8: Creating Multiple System Profiles

### Create Different Configurations

**Development Profile:**
```bash
cp kernel.md kernel-dev.md
cp desktop.md desktop-dev.md
# Edit these files for development setup
```

**Production Profile:**
```bash
cp kernel.md kernel-prod.md
cp desktop.md desktop-prod.md
# Edit these files for production setup
```

**Testing Profile:**
```bash
cp kernel.md kernel-test.md
cp desktop.md desktop-test.md
# Edit these files for testing setup
```

### Switch Profiles
```bash
# Switch to dev
cp kernel-dev.md kernel.md
cp desktop-dev.md desktop.md
python3 markdownos.py

# Switch to production
cp kernel-prod.md kernel.md
cp desktop-prod.md desktop.md
python3 markdownos.py
```

## Tips and Tricks

### Tip 1: Use Comments in Markdown
Add HTML comments for notes:
```markdown
<!-- TODO: Add database service -->
### Process: mysql
```

### Tip 2: Organize Processes by Purpose
Group related processes:
```markdown
## System Services
### Process: init
### Process: logger

## User Services
### Process: shell
### Process: desktop
```

### Tip 3: Document Dependencies
```markdown
### Process: app-server
- **PID**: 30
- **Command**: `./app`
- **Description**: Application server (requires database)
```

### Tip 4: Use Consistent Naming
- Process names: lowercase-with-hyphens
- Application names: Title Case
- Directories: /lowercase/paths

### Tip 5: Test Changes Incrementally
1. Add one process
2. Boot and verify
3. Add next process
4. Boot and verify

## Advanced Examples

### Custom System Calls
Edit kernel.md to define new system calls:
```markdown
## System Calls (Supported)

8. **custom_call** - My custom system call for XYZ
```

### Custom Desktop Themes
Edit desktop.md:
```markdown
### Custom Theme
- **Name**: MyTheme
- **Panel Background**: `#000000`
- **Panel Foreground**: `#00ff00`
```

### Dynamic Configurations
Use environment variables in commands:
```markdown
### Process: dynamic
- **Command**: `echo $USER is logged in`
```

## Troubleshooting

### System Won't Boot
- Check markdown syntax in kernel.md
- Ensure required sections exist
- Verify Python 3 is installed

### Process Not Starting
- Check **Auto Start** is set to `true`
- Verify command is valid
- Check working directory exists

### Application Not Appearing
- Verify application section syntax
- Check desktop.md formatting
- Ensure **Name** field is set

## Next Steps

1. Experiment with different configurations
2. Create your own custom system profiles
3. Share interesting configurations with others
4. Contribute improvements to the runtime
5. Dream up new features for iteration 1!

Remember: The system is as flexible as markdown allows. Be creative!
