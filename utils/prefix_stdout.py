import sys
from contextlib import contextmanager

class PrefixStdout:
    def __init__(self, prefix):
        self.prefix = prefix
        self._stdout = sys.stdout

    def write(self, text):
        if text.strip():
            for line in text.splitlines(keepends=True):
                if line.strip():
                    self._stdout.write(f"{self.prefix}{line}")
                else:
                    self._stdout.write(line)
        else:
            self._stdout.write(text)

    def flush(self):
        self._stdout.flush()

@contextmanager
def prefix_stdout(prefix):
    original_stdout = sys.stdout
    sys.stdout = PrefixStdout(prefix)
    try:
        yield
    finally:
        sys.stdout = original_stdout

# Usage:
# with prefix_stdout("[PLUGIN] "):
#     print("Hello, world!")
#     print("Another line")
# print("Back to normal")