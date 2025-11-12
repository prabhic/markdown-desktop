# Desktop Environment Configuration

This file defines the desktop environment for the markdown-based Linux system.

## Desktop Information

- **Name**: MarkdownDE (Markdown Desktop Environment)
- **Version**: 0.1.0
- **Type**: minimal-text-based
- **Window Manager**: tmux-based

## Display Configuration

### Screen
- **Resolution**: Terminal size (auto-detect)
- **Color Depth**: 256 colors
- **Type**: Text-based (character mode)

## Window Manager

### Type: TilingWM
- **Layout**: tiling
- **Border**: single-line
- **Focus Mode**: click-to-focus

### Keyboard Shortcuts
- **Open Terminal**: `Ctrl+Alt+T`
- **Switch Window**: `Alt+Tab`
- **Close Window**: `Alt+F4`
- **Quit Desktop**: `Ctrl+Alt+Q`

## Applications

### Application: Terminal
- **Name**: Terminal Emulator
- **Command**: `bash`
- **Icon**: `>`
- **Auto Start**: true
- **Category**: System

### Application: File Manager
- **Name**: File Browser
- **Command**: `ls -la`
- **Icon**: `📁`
- **Auto Start**: false
- **Category**: Utilities

### Application: Text Editor
- **Name**: Nano Editor
- **Command**: `nano`
- **Icon**: `📝`
- **Auto Start**: false
- **Category**: Accessories

### Application: System Monitor
- **Name**: Process Viewer
- **Command**: `ps aux`
- **Icon**: `📊`
- **Auto Start**: false
- **Category**: System

## Panel Configuration

### Top Panel
- **Position**: top
- **Height**: 1 line
- **Background**: blue
- **Widgets**:
  - Clock (right)
  - System Info (left)
  - Active Windows (center)

### Clock Widget
- **Format**: `%Y-%m-%d %H:%M:%S`
- **Update Interval**: 1 second

### System Info Widget
- **Show**: hostname, load average
- **Update Interval**: 5 seconds

## Menu

### Application Menu
- **Trigger**: Click on hostname
- **Layout**: list
- **Items**:
  1. Terminal
  2. File Manager
  3. Text Editor
  4. System Monitor
  5. ---
  6. Logout

## Desktop Behavior

### Startup Sequence
1. Initialize display
2. Start window manager
3. Draw top panel
4. Launch auto-start applications
5. Show welcome message

### Session Management
- **Save Session**: on exit
- **Restore Session**: on startup
- **Session File**: `/tmp/.desktop-session.md`

## Themes

### Default Theme
- **Name**: MarkdownDark
- **Panel Background**: `#1e1e1e`
- **Panel Foreground**: `#ffffff`
- **Window Border**: `#444444`
- **Focused Border**: `#0066cc`

## Welcome Message

```
╔═══════════════════════════════════════════════════════════╗
║                    MarkdownDE v0.1.0                      ║
║         Markdown-Configured Desktop Environment           ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  Your desktop is configured via desktop.md                ║
║  Edit the file to customize your environment              ║
║                                                           ║
║  Quick Start:                                             ║
║  - Terminal opens automatically                           ║
║  - Click hostname for application menu                    ║
║  - Edit desktop.md to add more apps                       ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

## Notes

- This is a text-based desktop environment
- Perfect for servers or minimal systems
- Edit this file to customize the desktop
- Changes apply on next login
- Applications are just shell commands
- Add new apps by adding markdown sections
