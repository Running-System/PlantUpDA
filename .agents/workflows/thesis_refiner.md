---
description: An interactive reviewer that reads thesis sections, processes supervisor feedback, asks targeted questions to extract missing information, and rewrites the content.
---

# Interactive Thesis Refiner Workflow

When I invoke this workflow (e.g., by saying "run the thesis refiner on state_of_the_art.tex" or providing a supervisor review), follow these steps precisely:

1. **Analyze the Target Section & Supervisor Feedback:**
   - Use the `view_file` tool to read the contents of the requested LaTeX file (or chunk of the file).
   - If the user provides **Supervisor Feedback**, carefully read the verdict. 
   - Determine the scope of the required changes (e.g., Minor Tweaks, Cohesion Fixes, or a **Major Rewrite**).
   - *Alternative:* If no feedback is provided, identify generic, repetitive, or overly formal "AI-sounding" paragraphs. Look for a lack of concrete examples, overused transition words, and surface-level analysis.

2. **Formulate Targeted Questions (CONDITIONAL):**
   - Do NOT edit the file yet.
   - Present a concise summary of the paragraph/section or the supervisor's core critique.
   - **If a MAJOR REWRITE is required:** Analyze if you have enough context to execute the rewrite.
   - **ONLY ask questions if critical technical details, methodological justifications, or personal reasoning are MISSING.** If you already know the architecture (e.g., from previous chapters) or the user provided enough context, skip to Step 5.
   - If information *is* missing, ask 1-2 **highly specific** questions.
   - *Example question:* "The supervisor noted we need to explain the communication protocol here. Does the Gamification Engine communicate via REST APIs or database triggers?"

3. **Check Sources and Research (Optional but Recommended):**
   - Use the `search_web` and `read_url_content` tools to verify claims or find academic sources (like IEEE papers) to back up assertions made in the text. Ask the user if they want to include a specific source you found.

4. **Wait for User Input (If Questions Were Asked):**
   - If you asked questions in Step 2, stop and wait for the user's response.
   - If you did NOT ask questions, proceed immediately to Step 5.

5. **Rewrite and Personalize (Using a Formal HTL Academic Style):**
   - Once the user provides their answers, rewrite the targeted text applying a formal but deeply personalized academic style:
     - **Objective but Grounded:** Keep the tone objective, structured, and analytical (usually third-person), but integrate the user's actual practical experiences and reasoning as the *methodological justification* for technical decisions.
     - **Address Feedback Explicitly:** Ensure all points from the supervisor's critique have been systematically resolved.
     - **HTL-Level Professionalism:** Avoid overly dramatic hooks, informal rhetorical questions (e.g., "Why spend months..."), or casual first-person narratives ("In my experience..."). Instead, use strict academic phrasing (e.g., "During the evaluation of...", "This limitation necessitated...").
   - Ensure the new text flows seamlessly within the existing LaTeX structure, maintaining academic rigor while demonstrating original thought.
   - Use the code editing tools (`replace_file_content` or `multi_replace_file_content`) to apply the edits to the file.

6. **Review and Iterate:**
   - Show a summary of the changes to the user.
   - Ask if they are satisfied with the new tone or if they want to move on to the next section or paragraph.
   - Repeat the process until the user is happy with the chapter.
