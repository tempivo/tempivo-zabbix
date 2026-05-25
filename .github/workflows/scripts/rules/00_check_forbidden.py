#!/usr/bin/env python

import json

forbidden_names = [
    '.git/',
    '.gitignore',
    'docs/',
    'LICENSE',
    '.venv/'
]

# CI lives under .github/workflows/; block other .github paths (e.g. outputs).
allowed_github_prefix = '.github/workflows/'


def run_check(skip: bool = False) -> dict:
    """ 
    Check for forbidden folders.
    """

    skip = False

    step_name = 'Check forbidden folders'

    if skip:
        return {
            'step': step_name,
            'status': 'skip',
            'message': ''
        }

    with open('.github/outputs/all_changed_files.json', 'r', encoding='utf-8') as file_list:
        changed_files = json.load(file_list)

    for file in changed_files:
        if file.startswith('.github/') and not file.startswith(allowed_github_prefix):
            return {
                'step': step_name,
                'status': 'fail',
                'message': f'Changing path "{file}" is forbidden (only {allowed_github_prefix}* is allowed under .github/).'
            }
        for name in forbidden_names:
            if file.startswith(name):
                return {
                    'step': step_name,
                    'status': 'fail',
                    'message': f'Changing directory "{file}" is forbidden.'
                }

    return {
        'step': step_name,
        'status': 'success',
        'message': ''
    }
