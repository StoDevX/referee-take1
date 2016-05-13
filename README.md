# Referee

> What is it?

The first phase of world domination, of course!

> No, really.

You're no fun, are you? Fine. If you must know, it's part of a new feedback system for CS courses at St. Olaf.

## Outline

Goal: Provide more immidiate feedback to students about their homework submissions.
Un-goal: Remove human graders from the feedback loop.

- Student submits homework: `git commit -m "submit hw13 complete"` and `git push origin master`
- Stogit sees a new commit and notifies a webhook: `http://rns202-3.cs.stolaf.edu:15715/stogit.py`
- `referee` now has control of the process!
  - It checks to see if the commit came from a stogit group that we care about
  - Then it loads the appropriate course definitions
  - It checks the commit message against something, to see if it needs to care about it: something like `(hw|lab).*complete$`
  - If the commit makes it here, we send the student an email confirming that they sucessfully submitted homework
  - Now we load a spec file for the appropriate course:
    - Check to see if folder exists
    - For each file that we expect, check to see if it's there
    - Also check for common misspellings and case-sensetivity
    - Also check for the filename in other folders? Might provide too many false positives
    - Lint each file, with custom syntax-checker, cpplint/cppcheck, and a style checker?
    - Try to compile each file
    - Test files as appropriate
- Done! Send student an email with feedback from each sucessful step and the failed step. Stop processing as soon as an error occurs.

