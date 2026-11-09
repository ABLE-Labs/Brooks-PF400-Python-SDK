import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

# Make the example package resolvable from the SDK workspace root.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
