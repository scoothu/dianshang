import sys
import os

project_root = os.path.dirname(os.path.abspath(__file__))
lib_path = os.path.join(project_root, 'lib')
output_file = os.path.join(project_root, 'test_output.txt')

if project_root not in sys.path:
    sys.path.insert(0, project_root)
if lib_path not in sys.path:
    sys.path.insert(0, lib_path)

orig_stdout = sys.stdout
orig_stderr = sys.stderr

with open(output_file, 'w', encoding='utf-8') as f:
    sys.stdout = f
    sys.stderr = f
    try:
        import pytest
        exit_code = pytest.main(sys.argv[1:])
        f.write(f'\n\n=== PYTEST EXIT CODE: {exit_code} ===\n')
    except Exception as e:
        f.write(f'\n\n=== EXCEPTION: {type(e).__name__}: {e} ===\n')
        import traceback
        traceback.print_exc(file=f)
        exit_code = 99
    finally:
        sys.stdout = orig_stdout
        sys.stderr = orig_stderr

sys.exit(exit_code)
