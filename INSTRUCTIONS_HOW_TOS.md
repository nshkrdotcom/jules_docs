# Working with Jules: Instructions and How-Tos

Hello! I'm Jules, your AI Software Engineering Agent. To help us work together effectively and for me to provide you with the best possible assistance, please consider the following guidelines when interacting with me.

## 1. Phrasing Your Requests

*   **Be Specific and Clear:** The more detailed and unambiguous your request, the better I can understand and execute it. Instead of "write some code," try "write a Python function that takes a list of integers and returns the sum of all even numbers in the list."
*   **Break Down Complex Tasks:** For large or complex problems, it's often best to break them down into smaller, manageable sub-tasks. This allows for more focused work and easier review at each stage.
*   **Provide Context:** If your request relates to existing code or a specific project, provide as much relevant context as possible. This includes:
    *   The programming language and relevant frameworks/libraries.
    *   Snippets of existing code (if applicable).
    *   The desired outcome or behavior.
    *   Any constraints or requirements.
*   **Specify File Names and Locations:** When asking for code changes or new files, clearly state the target file names and their intended directory paths.

## 2. Providing Context for Coding Tasks

*   **File Paths:** When referring to files, use their full path from the repository root if there's any ambiguity.
*   **Existing Code:** If you want me to modify existing code, provide the relevant snippets or tell me which files and functions to look at.
*   **Dependencies:** If new dependencies are needed, please specify them (e.g., "add the 'requests' library to the Python project"). I can often infer this, but explicit instruction is better.
*   **Error Messages:** If you're encountering an error, provide the full error message and stack trace. This is invaluable for debugging.

## 3. My Iterative Process and Your Feedback

I typically follow a process that includes:

1.  **Understanding the Request:** I'll analyze your request and may ask clarifying questions if needed.
2.  **Planning:** For non-trivial tasks, I will create a plan outlining the steps I intend to take. I will usually ask for your approval of this plan.
3.  **Execution (Subtasks):** I delegate specific actions (like writing code, reading files, running commands) to a "Worker" agent. You'll see notifications about these subtasks starting and completing.
4.  **Review and Testing:** I will aim to create code that is correct and, where appropriate, I will suggest or create tests.
5.  **Seeking Feedback:** Your feedback is crucial! After I complete a step or a task, please review my work. Tell me what you like, what needs changing, or if I've missed something.

*   **Constructive Feedback:** "This function works, but could you add error handling for X case?" or "The variable name Y is a bit unclear, could we change it to Z?" is very helpful.
*   **Plan Adjustments:** If you think the plan needs to change, let me know. I can update the plan based on your input.

## 4. My Use of Tools

I use a set of tools to interact with the codebase, access information, and manage my workflow. These include:

*   `ls()`: To list files in the repository.
*   `read_files()`: To read the content of files.
*   `view_text_website()`: To fetch content from URLs (e.g., documentation).
*   `set_plan()`: To create or update my working plan.
*   `plan_step_complete()`: To mark a step in my plan as done.
*   `run_subtask()`: To delegate tasks like writing/modifying code, running commands, etc.
*   `message_user()` / `request_user_input()`: To communicate with you.
*   `submit()`: To commit changes to the repository.

You don't need to know the specifics of how these tools work, but understanding that I operate by using them can help explain my responses and actions. For example, I don't "see" your screen or have direct access to your local environment; I only interact with the project through these tools within a controlled environment.

## 5. What to Expect

*   **I'm a Collaborator:** Think of me as a pair programmer or a junior developer you're mentoring. I can do a lot, but I work best with guidance and oversight.
*   **Strengths:** Repetitive tasks, boilerplate code, implementing well-defined logic, writing tests, refactoring, exploring codebases.
*   **Limitations:** Highly abstract reasoning, tasks requiring deep domain-specific knowledge not provided to me, tasks requiring visual feedback (e.g., complex UI design), or tasks that require access to external systems I'm not explicitly equipped to handle. I also don't have "opinions" or "preferences" in a human sense, but I can follow specified style guides or best practices.
*   **Learning:** I can learn from examples you provide and adapt to specific coding styles or patterns within a project.

By following these guidelines, we can have a productive and successful collaboration!
