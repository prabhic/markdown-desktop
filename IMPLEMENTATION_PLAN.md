# MarkdownOS Implementation Plan

**North Star**: Remove fear from systems programming
**Reviewers**: See REVIEWERS.md for expert perspectives

---

## Plan Structure

Each micro-phase follows this pattern:

```
Micro-Phase X.Y: [Name]
├── Deliverable: What gets built
├── User Value: Why this matters now
├── Test Criteria: How we verify it works
├── Time Box: Maximum time to spend
├── Review Checkpoint: Expert feedback session
└── Ship Criteria: What "done" looks like
```

**Key Principle**: Every micro-phase must be **shippable and usable** at completion.

---

# Phase 1: Foundation - Safe Experimentation
**Goal**: Users can try things without fear of breaking anything
**Duration**: 2 weeks (10 micro-phases)

---

## Micro-Phase 1.1: Add Simulate Flag

**Deliverable**: `--simulate` flag that previews changes without applying them

**Implementation**:
```python
# In markdownos.py
def simulate_changes(kernel_path, desktop_path):
    """Parse configs and show what WOULD happen without executing"""
    print("🔍 SIMULATION MODE - No actual changes will be made")
    # Parse markdown
    # Show what would happen
    # Exit without executing
```

**User Value**:
- See what a config change would do before applying
- Build confidence in understanding the system
- Learn cause-and-effect safely

**Test Criteria**:
```bash
# Test 1: Basic simulation
python3 markdownos.py --simulate
# Should show boot sequence without actually creating processes

# Test 2: Works with existing configs
python3 markdownos.py --simulate
# Should parse kernel.md and desktop.md successfully

# Test 3: Clear messaging
# Output must say "SIMULATION MODE" prominently
# Output must say "No changes were made"
```

**Acceptance Tests**:
- [ ] Flag is recognized and documented in `--help`
- [ ] Simulation runs without errors
- [ ] Output clearly states this is a simulation
- [ ] No actual system state is modified
- [ ] Exit code is 0 on success

**Time Box**: 4 hours

**Documentation Update**:
```markdown
# Add to README.md
## Simulation Mode

Preview system behavior without making changes:

\`\`\`bash
python3 markdownos.py --simulate
\`\`\`

Perfect for learning and testing configurations safely!
```

**Review Checkpoint**: `reviews/phase-1-1-simulate-flag-review.md`

**Ship Criteria**:
- ✅ All tests pass
- ✅ Documentation updated
- ✅ Reviewed by all 3 expert perspectives
- ✅ User can run and understand the output

---

## Micro-Phase 1.2: Basic Explain Mode

**Deliverable**: `--explain [topic]` command that explains OS concepts in plain language

**Implementation**:
```python
# In markdownos.py
EXPLANATIONS = {
    "init": """
    The 'init' process is the first program that starts when your system boots.

    Think of it like the manager of a company:
    - It starts up first (PID 1)
    - It's responsible for starting all other processes
    - If init stops, everything else must stop too

    In MarkdownOS, init is defined in kernel.md lines 16-21.
    """,
    "pid": """
    PID stands for Process ID - a unique number for each running program.

    Like a name tag at a conference:
    - Every process gets a number when it starts
    - No two processes can have the same PID
    - PID 1 is always the init process (it starts first)

    In MarkdownOS, you assign PIDs in kernel.md.
    """,
    # Add more explanations
}

def explain_concept(topic):
    if topic in EXPLANATIONS:
        print(EXPLANATIONS[topic])
    else:
        print(f"No explanation for '{topic}' yet. Try: init, pid, filesystem")
```

**User Value**:
- Beginners get instant help without searching docs
- Learn OS concepts in plain English
- Build understanding while exploring

**Test Criteria**:
```bash
# Test 1: Explain init
python3 markdownos.py --explain init
# Should output clear explanation of init process

# Test 2: Explain PID
python3 markdownos.py --explain pid
# Should explain what PIDs are

# Test 3: Unknown topic
python3 markdownos.py --explain foobar
# Should gracefully handle unknown topics

# Test 4: List available topics
python3 markdownos.py --explain
# Should list all available explanation topics
```

**Acceptance Tests**:
- [ ] At least 5 core concepts explained (init, pid, filesystem, process, directory)
- [ ] Explanations are under 100 words each
- [ ] No jargon without explanation
- [ ] Each explanation references where to find it in markdown files
- [ ] Help text lists available topics

**Time Box**: 3 hours

**Documentation Update**:
```markdown
# Add to README.md
## Learning Mode

Get instant explanations of OS concepts:

\`\`\`bash
python3 markdownos.py --explain init
python3 markdownos.py --explain pid
python3 markdownos.py --explain filesystem
\`\`\`

Perfect for beginners learning how operating systems work!
```

**Review Checkpoint**: `reviews/phase-1-2-explain-mode-review.md`

**Ship Criteria**:
- ✅ All tests pass
- ✅ At least 5 concepts explained
- ✅ Explanations are beginner-friendly (tested on non-technical person)
- ✅ Documentation updated

---

## Micro-Phase 1.3: Progressive Disclosure - Quiet Mode

**Deliverable**: `--quiet` flag for minimal output (beginner-friendly default)

**Implementation**:
```python
# In markdownos.py
def boot_system(verbosity="normal"):
    if verbosity == "quiet":
        print("╔══════════════════════════════════════╗")
        print("║      MarkdownOS v0.1.0               ║")
        print("╚══════════════════════════════════════╝")
        print()
        print(f"✓ System booted successfully")
        print(f"✓ {num_processes} processes running")
        print(f"✓ {num_files} files ready")
        print()
        print("Try: markdownos.py --status")
        print("     markdownos.py --explain init")
    elif verbosity == "normal":
        # Current output
        pass
    elif verbosity == "verbose":
        # Will add in next phase
        pass
```

**User Value**:
- Beginners aren't overwhelmed with technical details
- Success is clear and encouraging
- Next steps are suggested

**Test Criteria**:
```bash
# Test 1: Quiet boot
python3 markdownos.py --quiet
# Should show minimal, friendly output

# Test 2: Default behavior unchanged
python3 markdownos.py
# Should show normal output (backward compatible)

# Test 3: Clear success message
python3 markdownos.py --quiet
# Should clearly indicate success
# Should suggest next actions
```

**Acceptance Tests**:
- [ ] Quiet mode output fits in 10 lines or less
- [ ] Success is visually clear (checkmarks, positive language)
- [ ] Suggests next steps to user
- [ ] No confusing technical jargon
- [ ] Default behavior is unchanged

**Time Box**: 2 hours

**Review Checkpoint**: `reviews/phase-1-3-quiet-mode-review.md`

**Ship Criteria**:
- ✅ Output tested with non-technical person (they understand it)
- ✅ Backward compatible
- ✅ Documented

---

## Micro-Phase 1.4: Progressive Disclosure - Verbose Mode

**Deliverable**: `--verbose` flag for detailed debugging output

**Implementation**:
```python
def boot_system(verbosity="normal"):
    # ... quiet mode from 1.3 ...
    elif verbosity == "verbose":
        print("[PARSER] Reading kernel.md...")
        print(f"[PARSER] Line 16: Found process definition: init")
        print(f"[VALIDATOR] Checking PID 1 uniqueness... ✓")
        print(f"[RUNTIME] Creating process struct for init")
        # etc.
```

**User Value**:
- Advanced users can debug issues
- Learning users can see what's happening under the hood
- Transparency builds trust

**Test Criteria**:
```bash
# Test 1: Verbose output
python3 markdownos.py --verbose
# Should show detailed step-by-step process

# Test 2: Shows file parsing
# Output should reference specific markdown files and line numbers

# Test 3: Shows validation steps
# Output should show what checks are being performed
```

**Acceptance Tests**:
- [ ] Shows file being parsed
- [ ] Shows line numbers being processed
- [ ] Shows validation steps
- [ ] Shows what's being created/initialized
- [ ] Still completes successfully

**Time Box**: 3 hours

**Review Checkpoint**: `reviews/phase-1-4-verbose-mode-review.md`

**Ship Criteria**:
- ✅ Helps debug issues
- ✅ References specific line numbers in markdown
- ✅ Documented with examples

---

## Micro-Phase 1.5: Validation Framework

**Deliverable**: Pre-flight validation that catches common mistakes

**Implementation**:
```python
def validate_kernel_config(config):
    """Check for common configuration errors"""
    errors = []
    warnings = []

    # Check: No duplicate PIDs
    pids = [p['pid'] for p in config['processes']]
    if len(pids) != len(set(pids)):
        errors.append("Duplicate PIDs found!")

    # Check: PID 1 must exist
    if 1 not in pids:
        errors.append("PID 1 (init) is required but not found!")

    # Warning: Large PIDs
    if any(pid > 1000 for pid in pids):
        warnings.append("PIDs over 1000 detected. Consider using smaller numbers.")

    return errors, warnings
```

**User Value**:
- Catch mistakes before they cause confusion
- Learn what makes a valid configuration
- Helpful error messages teach best practices

**Test Criteria**:
```bash
# Test 1: Duplicate PID detection
# Edit kernel.md to have duplicate PIDs
python3 markdownos.py
# Should show clear error message

# Test 2: Missing PID 1
# Remove init process from kernel.md
python3 markdownos.py
# Should explain why PID 1 is required

# Test 3: Valid config passes
python3 markdownos.py
# Should boot normally with no errors
```

**Acceptance Tests**:
- [ ] Detects duplicate PIDs
- [ ] Requires PID 1 to exist
- [ ] Checks for invalid permissions (e.g., 0999)
- [ ] Checks for missing required fields
- [ ] Error messages explain how to fix the issue
- [ ] Warnings don't block boot

**Time Box**: 4 hours

**Review Checkpoint**: `reviews/phase-1-5-validation-review.md`

**Ship Criteria**:
- ✅ Catches at least 5 common errors
- ✅ Error messages are helpful (not just "invalid config")
- ✅ Valid configs still work
- ✅ Tests added for each validation rule

---

## Micro-Phase 1.6: Helpful Error Messages

**Deliverable**: Educational error messages that teach users

**Implementation**:
```python
def format_error(error_type, context):
    """Format errors to be helpful and educational"""

    if error_type == "duplicate_pid":
        return f"""
╔════════════════════════════════════════════════════════╗
║  Configuration Error: Duplicate PID                    ║
╚════════════════════════════════════════════════════════╝

Problem: PID {context['pid']} is used by multiple processes:
  • {context['process1']} (line {context['line1']})
  • {context['process2']} (line {context['line2']})

What this means:
  Every process needs a unique Process ID (PID).
  It's like two people having the same ID number - the system
  wouldn't know which is which!

How to fix:
  1. Open kernel.md
  2. Change one of the PIDs to an unused number
  3. Try booting again

Example:
  ### Process: {context['process2']}
  - **PID**: {context['pid'] + 1}  ← Change this to a different number

Learn more: markdownos.py --explain pid
        """
```

**User Value**:
- Errors become learning opportunities
- Users know exactly how to fix problems
- Reduces frustration and confusion

**Test Criteria**:
```bash
# Test 1: Error includes explanation
# Trigger any error
# Should explain WHAT went wrong, WHY it's wrong, HOW to fix it

# Test 2: Error includes line numbers
# Should reference specific lines in markdown files

# Test 3: Error suggests next steps
# Should offer concrete actions to take
```

**Acceptance Tests**:
- [ ] Every error has WHAT/WHY/HOW sections
- [ ] References specific file and line number
- [ ] Includes example of correct syntax
- [ ] Suggests relevant `--explain` topic if available
- [ ] Error is formatted for readability (not a stack trace)

**Time Box**: 4 hours

**Review Checkpoint**: `reviews/phase-1-6-helpful-errors-review.md`

**Ship Criteria**:
- ✅ All validation errors use new format
- ✅ Non-technical person can understand and fix errors
- ✅ Includes examples of fixes

---

## Micro-Phase 1.7: Configuration Diff Tool

**Deliverable**: `--diff` command to show what changed between boots

**Implementation**:
```python
# In markdownos.py
def show_config_diff():
    """Show what changed in config since last boot"""
    # Read .markdownos_state.json (saved on last boot)
    # Compare with current kernel.md and desktop.md
    # Show differences in user-friendly format

    print("📊 Configuration Changes Since Last Boot")
    print()
    print("Added:")
    print("  + Process 'nginx' (PID 10)")
    print()
    print("Modified:")
    print("  ~ Process 'logger' - command changed")
    print()
    print("Removed:")
    print("  (none)")
```

**User Value**:
- See exactly what you changed
- Understand impact before booting
- Build confidence in config management

**Test Criteria**:
```bash
# Test 1: First boot (no previous state)
python3 markdownos.py --diff
# Should say "No previous boot found"

# Test 2: After adding process
# Boot once, add process to kernel.md, run diff
python3 markdownos.py --diff
# Should show "Added: Process 'name'"

# Test 3: After modifying
# Change a process command, run diff
# Should show "Modified: Process 'name' - command changed"
```

**Acceptance Tests**:
- [ ] Detects added processes
- [ ] Detects modified processes
- [ ] Detects removed processes
- [ ] Detects filesystem changes
- [ ] Saves state after successful boot
- [ ] Handles first boot gracefully

**Time Box**: 5 hours

**Review Checkpoint**: `reviews/phase-1-7-diff-tool-review.md`

**Ship Criteria**:
- ✅ Diff is accurate
- ✅ Output is clear
- ✅ State persists between boots
- ✅ Documented with examples

---

## Micro-Phase 1.8: Undo Last Change

**Deliverable**: `--undo` command to revert last configuration change

**Implementation**:
```python
# In markdownos.py
def undo_last_change():
    """Restore previous version of config from backup"""
    # Check if .markdownos_backup/ exists
    # Restore kernel.md and desktop.md from backup
    # Show what was reverted

    print("⏪ Reverting to Previous Configuration")
    print()
    print("Restored:")
    print("  ✓ kernel.md")
    print("  ✓ desktop.md")
    print()
    print("Changes undone:")
    print("  - Removed process 'nginx'")
    print()
    print("Boot with: python3 markdownos.py")
```

**User Value**:
- Mistakes can be undone instantly
- Experimentation becomes truly safe
- Removes fear of breaking things

**Test Criteria**:
```bash
# Test 1: Undo after change
# Boot, modify kernel.md, run undo
python3 markdownos.py --undo
# Should restore previous version

# Test 2: Files actually restored
# Verify kernel.md contents match previous version

# Test 3: No backup available
python3 markdownos.py --undo
# Should handle gracefully with helpful message
```

**Acceptance Tests**:
- [ ] Backs up config on every successful boot
- [ ] Undo restores previous config files
- [ ] Shows what was changed
- [ ] Handles "no backup available" case
- [ ] Keeps last 3 backups (not just 1)
- [ ] Works with both kernel.md and desktop.md

**Time Box**: 4 hours

**Review Checkpoint**: `reviews/phase-1-8-undo-review.md`

**Ship Criteria**:
- ✅ Undo actually works
- ✅ Doesn't lose data
- ✅ Clear about what's being reverted
- ✅ Tested with real config changes

---

## Micro-Phase 1.9: Interactive Tutorial

**Deliverable**: `--tutorial` command that guides users through first config change

**Implementation**:
```python
def run_tutorial():
    """Interactive tutorial for first-time users"""
    print("""
╔════════════════════════════════════════════════════════╗
║        Welcome to MarkdownOS Tutorial!                 ║
╚════════════════════════════════════════════════════════╝

This tutorial will teach you to:
1. Understand the system
2. Make your first change
3. Boot with your changes

Ready? Let's go!

Step 1/5: Understanding Processes
----------------------------------
A process is a running program. In MarkdownOS, processes are
defined in kernel.md.

Let's look at the 'logger' process:
    """)

    # Show logger process from kernel.md
    # Explain each field
    # Ask user to press Enter to continue

    # Step 2: Edit config
    # Step 3: Validate
    # Step 4: Boot
    # Step 5: Verify
```

**User Value**:
- Guided learning for absolute beginners
- Hands-on experience in safe environment
- Builds confidence step-by-step

**Test Criteria**:
```bash
# Test 1: Tutorial runs to completion
python3 markdownos.py --tutorial
# Should complete all steps without errors

# Test 2: Tutorial makes actual changes
# Should modify a config file and boot the system

# Test 3: Tutorial is interruptible
# Ctrl+C should exit cleanly
```

**Acceptance Tests**:
- [ ] Tutorial has 5 clear steps
- [ ] Each step explains what and why
- [ ] User makes an actual config change
- [ ] User boots with their change
- [ ] User sees their change working
- [ ] Tutorial takes <5 minutes
- [ ] Can exit anytime safely

**Time Box**: 6 hours

**Review Checkpoint**: `reviews/phase-1-9-tutorial-review.md`

**Ship Criteria**:
- ✅ Tested with someone who's never used MarkdownOS
- ✅ Beginner completes tutorial successfully
- ✅ Beginner can explain what they learned
- ✅ Tutorial is engaging, not boring

---

## Micro-Phase 1.10: Phase 1 Integration Testing

**Deliverable**: Comprehensive test suite for Phase 1 features

**Implementation**:
```bash
#!/bin/bash
# tests/phase1_integration_test.sh

echo "Running Phase 1 Integration Tests..."

# Test 1: Simulate flag
echo "[1/10] Testing --simulate..."
python3 markdownos.py --simulate > /dev/null || exit 1

# Test 2: Explain mode
echo "[2/10] Testing --explain..."
python3 markdownos.py --explain init > /dev/null || exit 1

# Test 3: Quiet mode
echo "[3/10] Testing --quiet..."
python3 markdownos.py --quiet > /dev/null || exit 1

# Test 4: Verbose mode
echo "[4/10] Testing --verbose..."
python3 markdownos.py --verbose > /dev/null || exit 1

# Test 5: Validation
echo "[5/10] Testing validation..."
# Create invalid config, expect error
# Restore valid config

# Test 6: Error messages
echo "[6/10] Testing error messages..."
# Trigger error, verify format

# Test 7: Diff
echo "[7/10] Testing --diff..."
python3 markdownos.py --diff > /dev/null || exit 1

# Test 8: Undo
echo "[8/10] Testing --undo..."
# Make change, undo, verify restored

# Test 9: Tutorial
echo "[9/10] Testing --tutorial..."
# Run tutorial in non-interactive mode

# Test 10: All features together
echo "[10/10] Testing full workflow..."
python3 markdownos.py --simulate
python3 markdownos.py --quiet
python3 markdownos.py --diff
echo "✓ All Phase 1 features working!"
```

**User Value**:
- Confidence that all features work together
- Regression prevention
- Quality assurance

**Test Criteria**:
- All 10 micro-phases pass their individual tests
- Features work in combination
- No conflicts between flags
- Documentation is complete

**Acceptance Tests**:
- [ ] All individual feature tests pass
- [ ] Combined usage tests pass
- [ ] README has examples of all features
- [ ] EXAMPLES.md is updated
- [ ] No broken functionality from Iteration 0

**Time Box**: 4 hours

**Review Checkpoint**: `reviews/phase-1-10-integration-review.md`

**Ship Criteria**:
- ✅ All tests pass
- ✅ All features documented
- ✅ All 3 reviewers approve Phase 1
- ✅ Ready to announce "Phase 1 Complete"

---

## Phase 1 Review Gate

**Before proceeding to Phase 2**, conduct comprehensive review:

### Review Document: `reviews/phase-1-final-review.md`

```markdown
# Phase 1 Complete Review

## Deliverables Checklist
- [ ] --simulate flag working
- [ ] --explain mode with 5+ concepts
- [ ] --quiet and --verbose modes
- [ ] Validation framework with 5+ rules
- [ ] Helpful error messages
- [ ] --diff tool
- [ ] --undo functionality
- [ ] Interactive tutorial
- [ ] Integration test suite
- [ ] All documentation updated

## Kelsey Hightower Perspective
**Can users safely experiment?**
**Can changes be tracked and reverted?**
**Is this ready for team collaboration?**

Rating: 🟢 / 🟡 / 🔴
Feedback: [detailed feedback]

## Simon Willison Perspective
**Is documentation clear for AI to understand?**
**Can an LLM explain these features?**
**Is the developer experience smooth?**

Rating: 🟢 / 🟡 / 🔴
Feedback: [detailed feedback]

## Jessie Frazelle Perspective
**Can a beginner use this without fear?**
**Are errors educational?**
**Is complexity manageable?**

Rating: 🟢 / 🟡 / 🔴
Feedback: [detailed feedback]

## User Validation
- [ ] Non-technical person completed tutorial
- [ ] Someone broke the config and recovered using --undo
- [ ] Someone learned something new from --explain
- [ ] Errors helped someone fix their mistake

## Go/No-Go Decision
**Proceed to Phase 2**: YES / NO / WITH CHANGES

**Required Actions Before Phase 2**:
1. [Any blocking issues]
2. [Documentation gaps]
3. [Bug fixes]
```

---

# Phase 2: AI Integration (Preview)
**Goal**: AI can explain, generate, and validate configs
**Duration**: 2 weeks (8-10 micro-phases)

*Detailed breakdown coming after Phase 1 approval*

**Micro-phases will include**:
- 2.1: Markdown-to-JSON schema export (for LLM consumption)
- 2.2: AI explain integration (local LLM)
- 2.3: Natural language config generator
- 2.4: AI validation assistant
- 2.5: RAG integration for documentation
- etc.

---

# Phase 3: Collaboration Tools (Preview)
**Goal**: Teams can collaborate on configs via git
**Duration**: 2 weeks (8-10 micro-phases)

**Micro-phases will include**:
- 3.1: Git integration checks
- 3.2: PR template generator
- 3.3: Automated policy validation in CI
- 3.4: Change impact analysis
- 3.5: Collaborative review workflows
- etc.

---

## Success Metrics Dashboard

Track these metrics after each phase:

```markdown
## Phase 1 Metrics

**Democratization**:
- Time to first config change: ____ minutes (target: <10)
- Tutorial completion rate: ___% (target: >80%)
- Undo usage rate: ___% (target: >50% try it)

**Fearless Experimentation**:
- Simulate mode usage: ___% (target: >60%)
- Errors encountered and fixed: ____ (higher is good!)
- Undo successful recovery rate: ___% (target: 100%)

**Transparency**:
- Explanation requests: ____ (target: >5 per user)
- Time to understand error: ____ seconds (target: <30)
- Diff usage before boot: ___% (target: >40%)
```

---

## Review Process Flow

```
Micro-Phase Complete
        ↓
   Run Tests
        ↓
   Update Docs
        ↓
 Create Review Doc (using template from REVIEWERS.md)
        ↓
 Apply 3 Expert Perspectives
        ↓
 All Perspectives Pass? ──NO──→ Fix Issues → Retest
        ↓ YES
 Commit & Mark Complete
        ↓
 Update Metrics Dashboard
        ↓
 Next Micro-Phase
```

---

## Emergency Procedures

**If a micro-phase is blocked:**

1. **Time box exceeded**:
   - Document what's blocking
   - Get reviewer input on simplifying scope
   - Split into smaller micro-phase if needed

2. **Tests won't pass**:
   - Don't proceed to next phase
   - Create issue document
   - Get reviewer perspective on approach

3. **Reviewer gives 🔴 on critical criteria**:
   - Stop and address feedback
   - Rework before proceeding
   - Re-review after changes

**Never proceed with broken functionality. Every micro-phase must work.**

---

*Last Updated: 2025-11-12*
*Current Phase: Planning Complete, Ready to Start Phase 1.1*
