# Markdown-Based Linux System Architecture

## Vision
A minimalist Linux-like system where **all behavior is defined in markdown files**. When you want to change the system, you simply edit markdown files.

## Core Philosophy
- **Declarative over Imperative**: Describe what you want, not how to do it
- **Readable Configuration**: System behavior readable as documentation
- **Iteration 0**: Bare minimum features that make Linux "Linux"

## Essential Linux Features (Iteration 0)

### 1. Process Management
The ability to run and manage programs - this is the heart of any OS.

### 2. File System
The ability to organize and access data - fundamental to Unix philosophy.

## How It Works

### Architecture Layers

```
┌─────────────────────────────────┐
│   Markdown Configuration Files  │  ← User edits these
│   (kernel.md, desktop.md, etc)  │
└────────────┬────────────────────┘
             │
             ↓
┌─────────────────────────────────┐
│   Markdown Interpreter/Parser   │  ← Reads & validates markdown
└────────────┬────────────────────┘
             │
             ↓
┌─────────────────────────────────┐
│   Runtime Executor               │  ← Executes defined behavior
│   (Python/Shell based)           │
└────────────┬────────────────────┘
             │
             ↓
┌─────────────────────────────────┐
│   Host Operating System          │  ← Actual Linux kernel
└─────────────────────────────────┘
```

### Key Insight
This is a **specification-driven OS simulator**. The markdown files are not code - they are specifications that a simple runtime interprets to provide OS-like functionality on top of a real OS.

## Example Flow

1. User edits `kernel.md` to define a new process
2. Interpreter parses the markdown file
3. Runtime creates a corresponding process using host OS primitives
4. Changes to markdown immediately affect system behavior

## Why Markdown?

- **Human-readable**: System configuration doubles as documentation
- **Version-controllable**: Use git to track system changes
- **Simple syntax**: Easy to parse and validate
- **Universal**: Works anywhere, no special tools needed

## Iteration 0 Scope

Keep it minimal:
- Define processes in markdown
- Define file system structure in markdown
- Simple CLI to "boot" the system by reading markdown
- Demonstrate that editing markdown changes behavior

Future iterations could add:
- Network configuration
- User management
- Desktop environment
- Package management
- etc.
