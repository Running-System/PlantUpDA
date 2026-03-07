---
description: An interactive reviewer that reads thesis sections, asks targeted questions to extract your personal thoughts, and rewrites the content to sound original and less AI-generated.
---

# Interactive Thesis Refiner Workflow

When I invoke this workflow (e.g., by saying "run the thesis refiner on state_of_the_art.tex"), follow these steps precisely:

1. **Analyze the Target Section:**
   - Use the `view_file` tool to read the contents of the requested LaTeX file (or chunk of the file).
   - Identify generic, repetitive, or overly formal "AI-sounding" paragraphs. Look for a lack of concrete examples, overused transition words (e.g., "Furthermore", "In conclusion"), and surface-level analysis.

2. **Formulate Targeted Questions:**
   - Do NOT edit the file yet.
   - Present a concise summary of the paragraph/section you are focusing on.
   - Ask 2-3 **highly specific** questions aimed at:
     - Drawing out the user's practical experience or original thoughts on the topic.
     - Asking *why* they structured the paragraph this way and how this specific topic relates to the rest of the thesis or the overall architectural goals.
   - *Example question:* "Why did you choose to structure the comparison of IoT models by starting with the 7-Layer model? How does understanding this model directly impact the latency challenges discussed later?"

3. **Check Sources and Research (Optional but Recommended):**
   - Use the `search_web` and `read_url_content` tools to verify claims or find academic sources (like IEEE papers) to back up assertions made in the text. Ask the user if they want to include a specific source you found.

4. **Wait for User Input:**
   - Stop and ask the user the questions using the chat. Wait for their response.

5. **Rewrite and Personalize (Using a Formal HTL Academic Style):**
   - Once the user provides their answers, rewrite the targeted text applying a formal but deeply personalized academic style:
     - **Objective but Grounded:** Keep the tone objective, structured, and analytical (usually third-person), but integrate the user's actual practical experiences and reasoning as the *methodological justification* for technical decisions.
     - **Structural Flow:** Ensure transitions explicitly connect back to the core research question or previous sections, based on the user's answers.
     - **HTL-Level Professionalism:** Avoid overly dramatic hooks, informal rhetorical questions (e.g., "Why spend months..."), or casual first-person narratives ("In my experience..."). Instead, use strict academic phrasing (e.g., "During the evaluation of...", "This limitation necessitated...").
   - Ensure the new text flows seamlessly within the existing LaTeX structure, maintaining academic rigor while demonstrating original thought.
   - Use the code editing tools (`replace_file_content` or `multi_replace_file_content`) to apply the edits to the file.

6. **Review and Iterate:**
   - Show a summary of the changes to the user.
   - Ask if they are satisfied with the new tone or if they want to move on to the next section or paragraph.
   - Repeat the process until the user is happy with the chapter.
