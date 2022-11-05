# Naive search for unticked files. Has no semantic knowledge, just a lexical
# search for #include directives against existing file paths.
#
# Usage:
#  python unticked_files.py C:\Path\To\Paradise\
#
# Returns 0 if all existing files are considered ticked, 1 otherwise.

from pathlib import Path
import argparse
import sys

INCLUDER_FILES = [
    'paradise.dme',
    'code/modules/tgs/includes.dm',
    'code/modules/unit_tests/_unit_tests.dm',
]

IGNORE_FILES = {
    # Included directly in the function /datum/tgs_api/v5#ApiVersion
    'code/modules/tgs/v5/interop_version.dm'
}

def get_unticked_files(root:Path):
    ticked_files = set()
    for includer in INCLUDER_FILES:
        with open(root / includer, 'r') as f:
            lines = [line for line in f.readlines() if line.startswith('#include')]
            included = [line.replace('#include ', '').rstrip('\r\n').strip('"') for line in lines]
            print(f'Found {len(included)} includes in {root / includer}')
            ticked_files.update([root / Path(includer).parent / i for i in included])

    all_dm_files = {f for f in root.glob('**/*.dm')}
    return all_dm_files - ticked_files - {root / f for f in IGNORE_FILES}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("root", help="paracode root directory")
    args = parser.parse_args()

    # Windows quoting behavior for directories adds trailing double-quote
    unticked_files = get_unticked_files(Path(args.root.strip('"')))
    if unticked_files:
        print(f'Found {len(unticked_files)} unticked files:')
        print('\n'.join(str(x) for x in sorted(unticked_files)))
        sys.exit(1)
    else:
        print(f'Found no unticked files')
