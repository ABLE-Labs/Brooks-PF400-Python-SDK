"""Explicit package imports are statically resolvable from the SDK workspace."""
import ast
from pathlib import Path

EXAMPLES = Path(__file__).parents[1] / 'examples'


def test_common_imports_use_explicit_package_names():
    assert (EXAMPLES / '__init__.py').exists()
    assert (EXAMPLES / 'common/__init__.py').exists()
    for path in EXAMPLES.glob('[0-9]*/*.py'):
        tree = ast.parse(path.read_text(encoding='utf-8'))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                assert node.module not in ('initialization', 'motion_profiles', 'teaching_positions'), path
