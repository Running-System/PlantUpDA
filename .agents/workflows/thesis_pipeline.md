---
description: An automated pipeline that goes through each section of the thesis sequentially, automatically running the text_checker for rigorous critique and then invoking the thesis_refiner to ask questions and rewrite the text.
---

# Thesis Pipeline Workflow

When invoked (e.g., "start the thesis pipeline" or `@[/thesis_pipeline]`), follow this exact process to review and refine the entire thesis section by section.

## Prerequisites
1. Identify the list of LaTeX files or logical sections to be reviewed. You can ask the user which file/chapter to start with, or analyze the workspace to deduce the order.

## Section Processing Loop
For **each section** (or manageable chunk of text/LaTeX code), perform the following steps sequentially:

### Step 1: Automated Text Checker
- Read the content of the current section using `view_file` if not already loaded.
- Execute the role and instructions from **`/text_checker`** internally.
- Generate and display the full supervisor critique specifically for this section:
  - A. Overall verdict
  - B. Detailed findings
  - C. Cohesion check
  - D. Style check
  - E. Priority fixes
  - Supervisor verdict
- *Do not wait for the user to reply to this critique; move immediately to the next step.*

### Step 2: Handoff to Thesis Refiner
- Seamlessly transition into the role of **`/thesis_refiner`**.
- Using the critique you just generated in Step 1, identify what information is missing to properly rewrite and fix the section.
- **Ask the user targeted questions** (1-3 questions maximum) to extract missing facts, technical details, or specific thoughts needed to address the text checker's feedback. 
- *Crucially: Do not ask the user to rewrite the text. Just ask for the raw answers/facts so you can rewrite it for them.*

### Step 3: Wait for User Input
- Stop and wait for the user to answer the questions.

### Step 4: Rewrite, Humanize, and Propose Draft
- Once the user answers, rewrite the section in a formal HTL academic style as defined in the `/thesis_refiner`.
- Ensure all points from the text checker's critique are fully resolved using the user's answers.
- **CRITICAL - Apply `/humanizer` Rules:** Before proposing the text, rigorously review and modify your own draft using the `/humanizer` guidelines:
  - Remove all common AI buzzwords and overly dramatic phrases (e.g., "delve", "crucial", "testament", "tapestry").
  - Vary sentence structures so it doesn't sound robotic.
  - Simplify overly complex sentence constructions; keep it easy to understand while maintaining academic rigor.
  - Ensure the writing retains a natural, human tone that isn't completely stripped of personality.
- **Present the final humanized draft to the user in the chat.**
- Ask the user to proofread the draft and explicitly request their approval before applying it. Do NOT modify the LaTeX file yet.

### Step 5: Wait for Proofreading Approval
- Stop and wait for the user to read the new draft.
- The user may request further tweaks to the drafted text. If so, iterate on the draft until they are completely satisfied.

### Step 6: Apply Changes and Proceed to Next Section
- ONLY once the user approves the draft (e.g., "looks good", "apply it"), use `replace_file_content` (or `multi_replace_file_content`) to update the file with the finalized text.
- After successfully saving the changes, target the next logical section in the document (or the next file) and completely restart from **Step 1**.
