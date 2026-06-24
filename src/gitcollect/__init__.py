"""gitcollect: a lightweight Git repository hygiene scanner."""

__version__ = "0.1.0"

from gitcollect.scanner import Finding, scan_lines, scan_text

__all__ = ["Finding", "scan_lines", "scan_text", "__version__"]
