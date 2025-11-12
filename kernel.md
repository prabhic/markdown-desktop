# Kernel Configuration

This file defines the core kernel behavior for the markdown-based Linux system.

## System Information

- **Name**: MarkdownOS
- **Version**: 0.1.0
- **Architecture**: markdown-based
- **Boot Mode**: interpreted

## Process Management

Define processes that should run on the system. Each process is declared in markdown.

### Process: init
- **PID**: 1
- **Command**: `echo "MarkdownOS Init System Starting..."`
- **Working Directory**: `/`
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
- **Command**: `echo "Logger service ready" > /tmp/system.log`
- **Working Directory**: `/var/log`
- **Auto Start**: true
- **Description**: System logging service

## File System Layout

Define the virtual file system structure.

### Root Directory: /
- **Type**: directory
- **Permissions**: 0755
- **Owner**: root

### Directory: /home
- **Type**: directory
- **Permissions**: 0755
- **Owner**: root
- **Description**: User home directories

### Directory: /home/user
- **Type**: directory
- **Permissions**: 0755
- **Owner**: user
- **Description**: Default user home directory

### Directory: /tmp
- **Type**: directory
- **Permissions**: 0777
- **Owner**: root
- **Description**: Temporary files

### Directory: /var/log
- **Type**: directory
- **Permissions**: 0755
- **Owner**: root
- **Description**: System log files

### File: /etc/hostname
- **Type**: file
- **Permissions**: 0644
- **Owner**: root
- **Content**: `markdown-os`
- **Description**: System hostname

### File: /etc/motd
- **Type**: file
- **Permissions**: 0644
- **Owner**: root
- **Content**: |
  ```
  Welcome to MarkdownOS v0.1.0
  A Linux system configured entirely through markdown files!
  
  To change system behavior, edit kernel.md
  ```
- **Description**: Message of the day

## Memory Management

### Total Memory
- **Size**: 512MB (virtual)
- **Mode**: managed by host

### Swap
- **Enabled**: false

## Scheduling

### Scheduler Type
- **Algorithm**: simple-round-robin
- **Time Slice**: 100ms

## System Calls (Supported)

The following system calls are supported in this minimal kernel:

1. **fork** - Create new process
2. **exec** - Execute program
3. **exit** - Terminate process
4. **read** - Read from file
5. **write** - Write to file
6. **open** - Open file
7. **close** - Close file

## Boot Sequence

1. Parse this kernel.md file
2. Create virtual file system structure
3. Start init process (PID 1)
4. Start auto-start processes in order
5. System ready

## Notes

- Edit this file to add/remove processes
- Changes take effect on next "boot"
- This is a declarative specification - the runtime interprets it
