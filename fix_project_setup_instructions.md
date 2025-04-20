# Fix Project Setup and Run Instructions for AI-CyberDefender-Genius

To fix the current errors and run the project and tests successfully, follow these steps:

1. **Rename Project Directory**

   Ensure the project directory uses underscores instead of hyphens for Python package compatibility:

   ```bash
   mv ai-cyberdefender-genius ai_cyberdefender_genius
   ```

2. **Add `__init__.py` Files**

   Add empty `__init__.py` files in all subdirectories to mark them as Python packages:

   ```bash
   touch ai_cyberdefender_genius/__init__.py
   touch ai_cyberdefender_genius/core/__init__.py
   touch ai_cyberdefender_genius/tests/__init__.py
   ```

3. **Set PYTHONPATH Environment Variable**

   When running the application or tests, set the `PYTHONPATH` to the project root directory:

   ```bash
   export PYTHONPATH=$(pwd)
   ```

4. **Run Tests**

   Run tests using unittest discovery:

   ```bash
   python3 -m unittest discover -s ai_cyberdefender_genius/tests -p "*.py"
   ```

5. **Run Application**

   Run the main application entry point (adjust if your main script is different):

   ```bash
   python3 main.py
   ```

6. **Fix File Saving Issues**

   If you encounter file saving errors in your editor (e.g., VSCode):

   - Restart the editor.
   - Disable conflicting extensions temporarily.
   - Check file system permissions.
   - Save files manually if needed.

7. **Verify and Fix Code Errors**

   After the above steps, review any remaining errors or missing dependencies and fix them incrementally.

---

Following these steps will resolve import errors, enable proper test discovery, and ensure your project runs smoothly.

If you want, I can help automate these steps or provide scripts to simplify the process.
