"""Folder layout and direct IDE-style imports from an unrelated directory."""
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).parents[1]
EXAMPLES = ROOT / 'examples'


def test_examples_are_grouped_and_configuration_preserved():
    assert not list(EXAMPLES.glob('[0-9]*.py')), 'Runnable examples must be grouped by number'
    for prefix in range(1, 15):
        folders = list(EXAMPLES.glob(f'{prefix:02}_*'))
        assert len(folders) == 1 and folders[0].is_dir(), prefix
        assert list(folders[0].glob('*.py'))
    assert (EXAMPLES / 'common/initialization.py').is_file()
    assert (EXAMPLES / 'config/motion_profiles.json').is_file()
    assert (EXAMPLES / 'config/teaching_positions.json').is_file()


def test_grouped_scripts_import_without_test_path_setup(tmp_path):
    scripts = sorted(EXAMPLES.glob('[0-9]*/*.py'))
    assert len(scripts) == 30
    code = '''
import json,runpy,socket,sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
def forbidden(*args, **kwargs):
    raise AssertionError("Import must not connect")
socket.create_connection = forbidden
for script in json.loads(sys.argv[2]):
    data = runpy.run_path(script, run_name="layout_import")
    assert callable(data["main"]), script
'''
    result = subprocess.run(
        [sys.executable, '-I', '-B', '-c', code, str(ROOT / 'src'), json.dumps([str(p) for p in scripts])],
        cwd=tmp_path, capture_output=True, text=True, encoding='utf-8',
        env={**os.environ, 'PYTHONIOENCODING': 'utf-8'},
    )
    assert result.returncode == 0, result.stdout + result.stderr
