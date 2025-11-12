# Micro-Phase Review Template

**Copy this template for each micro-phase review**

---

## Micro-Phase Review: [PHASE-X-Y-NAME]

**Deliverable**: [What was built]
**Date**: [YYYY-MM-DD]
**Reviewer**: [Your name]
**Implementation Time**: [Actual hours spent vs time box]

---

## Feature Checklist

**Acceptance Criteria:**
- [ ] All tests pass
- [ ] Documentation updated
- [ ] User value is clear
- [ ] Code is committed
- [ ] Examples provided

---

## Review: Kelsey Hightower Perspective (Infrastructure)

### Evaluation Criteria

**Version Control & GitOps:**
- Can this be tracked in git effectively? 🟢 / 🟡 / 🔴
- _Rationale:_ [Why this rating?]

**Reversibility:**
- Can mistakes be rolled back safely? 🟢 / 🟡 / 🔴
- _Rationale:_ [Why this rating?]

**Team Collaboration:**
- Can multiple people work on this? 🟢 / 🟡 / 🔴
- _Rationale:_ [Why this rating?]

**Configuration Drift:**
- Does this prevent or detect drift? 🟢 / 🟡 / 🔴
- _Rationale:_ [Why this rating?]

**Audit Trail:**
- Can we track who changed what and why? 🟢 / 🟡 / 🔴
- _Rationale:_ [Why this rating?]

### Overall Infrastructure Rating
🟢 Pass / 🟡 Conditional Pass / 🔴 Needs Rework

### Feedback
**What works well:**
- [List strengths from infrastructure perspective]

**What needs improvement:**
- [List concerns or suggestions]

**Blocking issues:**
- [Any critical problems that must be fixed]

---

## Review: Simon Willison Perspective (AI-First)

### Evaluation Criteria

**LLM Readable:**
- Can an LLM understand and use this? 🟢 / 🟡 / 🔴
- _Rationale:_ [Why this rating?]

**Documentation Quality:**
- Is documentation clear and complete? 🟢 / 🟡 / 🔴
- _Rationale:_ [Why this rating?]

**AI Assistance Enabled:**
- Does this enable AI-assisted workflows? 🟢 / 🟡 / 🔴
- _Rationale:_ [Why this rating?]

**Developer Experience:**
- Is the developer UX smooth? 🟢 / 🟡 / 🔴
- _Rationale:_ [Why this rating?]

**RAG Compatibility:**
- Can this work in RAG/embedding systems? 🟢 / 🟡 / 🔴
- _Rationale:_ [Why this rating?]

### Overall AI-First Rating
🟢 Pass / 🟡 Conditional Pass / 🔴 Needs Rework

### Feedback
**What works well:**
- [List strengths from AI perspective]

**What needs improvement:**
- [List concerns or suggestions]

**Blocking issues:**
- [Any critical problems that must be fixed]

---

## Review: Jessie Frazelle Perspective (Accessibility)

### Evaluation Criteria

**Beginner Friendly:**
- Can a beginner understand this? 🟢 / 🟡 / 🔴
- _Rationale:_ [Why this rating?]

**Safe to Experiment:**
- Is it safe to try without fear? 🟢 / 🟡 / 🔴
- _Rationale:_ [Why this rating?]

**Helpful Errors:**
- Do errors teach users? 🟢 / 🟡 / 🔴
- _Rationale:_ [Why this rating?]

**Removes Fear:**
- Does this reduce anxiety about systems? 🟢 / 🟡 / 🔴
- _Rationale:_ [Why this rating?]

**Appropriate Complexity:**
- Is complexity proportional to task? 🟢 / 🟡 / 🔴
- _Rationale:_ [Why this rating?]

### Overall Accessibility Rating
🟢 Pass / 🟡 Conditional Pass / 🔴 Needs Rework

### Feedback
**What works well:**
- [List strengths from accessibility perspective]

**What needs improvement:**
- [List concerns or suggestions]

**Blocking issues:**
- [Any critical problems that must be fixed]

---

## User Testing Results

**Test 1: Non-technical user**
- Could they complete the task? YES / NO
- Time taken: ___ minutes
- Confusion points: [What was unclear?]
- Success indicators: [What worked well?]

**Test 2: Technical user**
- Feedback on UX: [What did they say?]
- Feature requests: [What did they want?]
- Bugs found: [Any issues?]

**Test 3: [Specific scenario]**
- [Describe test and results]

---

## Metrics

**From IMPLEMENTATION_PLAN.md success metrics:**

**Democratization:**
- Time to first config change: ___ minutes (target: <10)
- [Other relevant metrics]

**Fearless Experimentation:**
- Simulate/test mode usage: ___%
- [Other relevant metrics]

**Transparency:**
- Error comprehension time: ___ seconds (target: <30)
- [Other relevant metrics]

---

## Final Decision

### Summary
[Brief summary of review outcomes]

### Rating Distribution
- Hightower (Infrastructure): 🟢 / 🟡 / 🔴
- Willison (AI-First): 🟢 / 🟡 / 🔴
- Frazelle (Accessibility): 🟢 / 🟡 / 🔴

### Ship Decision
✅ **Ship It** - All criteria met, ready to proceed
⚠️ **Ship with Notes** - Ship but track improvements
🚫 **Rework Required** - Must address blocking issues

### Action Items Before Next Phase
1. [Required fixes if any]
2. [Improvements to track]
3. [Documentation updates needed]
4. [Next micro-phase preparations]

---

## Reviewer Notes

[Any additional context, learnings, or observations]

---

**Review Completed**: [Date]
**Next Micro-Phase**: [Phase X.Y+1]
**Status**: APPROVED / CONDITIONAL / BLOCKED
