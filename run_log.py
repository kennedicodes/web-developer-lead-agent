import sys
import traceback
from datetime import datetime

LOG_FILE = "run_log.txt"


class _Tee:
    """Writes everything printed to both the terminal and the log file."""

    def __init__(self, stream, log):
        self.stream, self.log = stream, log

    def write(self, text):
        self.stream.write(text)
        self.log.write(text)
        self.log.flush()

    def flush(self):
        self.stream.flush()
        self.log.flush()


def start():
    """Send this run's output (and any crash traceback) to run_log.txt, replacing the previous run's log."""
    log = open(LOG_FILE, "w", encoding="utf-8")
    log.write(f"Run started {datetime.now():%Y-%m-%d %H:%M:%S}\n\n")
    sys.stdout = _Tee(sys.__stdout__, log)
    sys.stderr = _Tee(sys.__stderr__, log)

    def _on_crash(exc_type, exc, tb):
        if issubclass(exc_type, KeyboardInterrupt):
            print("\nStopped with Ctrl+C.")
        else:
            print("\nCRASHED:")
            traceback.print_exception(exc_type, exc, tb)
        print(f"Run ended {datetime.now():%Y-%m-%d %H:%M:%S}")

    sys.excepthook = _on_crash
