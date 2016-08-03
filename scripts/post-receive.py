#!/usr/bin/env python3
"""
This is an implementation of python's os.walk
function only using git-show, so it doesn't need
to check out a working copy.

Just put this in .git/hooks as `post-receive`,
push something, and watch as the contents of
your repsitory is printed out in the response
from the remote!
"""

import yaml
import os
import sys
import subprocess

def git(*cmd):
    return subprocess.check_output(['git', *cmd], universal_newlines=True)

def git_show(*args):
    return git('show', *args)

def git_log(*args):
    return git('log', *args)


def listdir(ref, path=''):
    path = path.strip('/')
    return git_show('{}:{}'.format(ref, path)).strip().split('\n')[2:]

def walk(ref, path=''):
    paths = listdir(ref, path)
    folders = [p for p in paths if p.endswith('/')]
    files = [p for p in paths if not p.endswith('/')]
    yield (path, folders, files)
    for d in folders:
        yield from walk(ref, os.path.join(path, d))

def exists(ref, path=''):
    listing = listdir(ref, path)
    if listing[0].startswith("fatal: Path '{}' does not exist".format(path)):
        return False
    return True

def get_messages_from_range(oldrev, newrev):
    """Messages are returned in reverse order, newest to oldest."""
    messages = git_log('--oneline', '{}..{}'.format(oldrev, newrev)).strip().split('\n')
    return [' '.join(msg.split(' ')[1:]) for msg in messages]

def get_commits_from_range(oldrev, newrev):
    """Messages are returned in reverse order, newest to oldest."""
    messages = git_log('--oneline', '{}..{}'.format(oldrev, newrev)).strip().split('\n')
    return [(msg.split(' ')[0], ' '.join(msg.split(' ')[1:])) for msg in messages]

import re

assignment_name_regex = re.compile(r'(hw|lab) ?(\d+)', re.IGNORECASE)
def parse_assignment_name(name):
    '''returns the kind and number from an assignment name'''
    matches = assignment_name_regex.match(name).groups()
    kind = matches[0]
    if kind == 'hw':
        kind = 'homework'
    elif kind == 'lab':
        kind = 'lab'
    num = int(matches[1])
    return kind, num


def process_file_into_dict(file_list):
    filename = file_list[0]
    commands = [f for f in file_list[1:] if type(f) is str]
    option_list = [opt for opt in file_list[1:] if type(opt) is dict]
    options = { k: v for opt in option_list for k, v in opt.items() }
    return {
        'filename': filename,
        'commands': commands,
        'options': options,
    }


def get_files(spec):
    '''returns the list of files from an assignment spec'''
    # `files` is an array of [file, ...options].
    # An `option` is either a string "command" to be run,
    # or an option to set.
    return [process_file_into_dict(f) for f in spec['files']]


def check_for_files_from_spec(ref, spec):
    print('check for files')
    assignment = spec['assignment']
    folder = spec.get('folder', assignment)
    kind, num = parse_assignment_name(assignment)
    results = {'number': num, 'kind': kind}

    if not exists(ref, folder):
        results['status'] = 'missing'
        return results

    files_that_do_exist = set(listdir(ref, folder))
    files_which_should_exist = set([f['filename'] for f in get_files(spec)])

    results['does have'] = files_that_do_exist
    results['should have'] = files_which_should_exist

    intersection_of = files_that_do_exist.intersection(files_which_should_exist)
    difference_of = files_which_should_exist.difference(files_that_do_exist)

    results['still needs'] = difference_of

    return results


def should_skip_commit(commit):
    return '[ci skip]' in commit[1] or '[skip ci]' in commit[1]


def find_assignment_tag(message):
    search = assignment_name_regex.search(message)
    if not search:
        return None
    matches = search.groups()
    return matches[0] + matches[1]


def load_spec(course, name):
    with open(os.path.join('..', 'specs', course, name + '.yaml'), 'r', encoding='utf-8') as infile:
        return yaml.safe_load(infile)


def load_specs(course, names):
    return [load_spec(course, name) for name in names]


def nicen(msg):
    print(msg)
    name = msg['kind'] + ' ' + str(msg['number'])
    if msg['still needs']:
        result = 'still needs: ' + ' '.join(msg['still needs'])
    elif msg['does have'] == msg['should have']:
        result = 'is complete!'
    return '{} {}'.format(name, result)

def main():
    for line in sys.stdin:
        oldrev, newrev, ref = line.split()
        print(oldrev, newrev, ref)

        # we need the latest commit ref for each assignment.
        # so we need all of the (commit, message) pairs…
        commits = get_commits_from_range(oldrev, newrev)
        print('commits =', commits)
        commits = [c for c in commits if not should_skip_commit(c)]

        assignments = [(c[0], find_assignment_tag(c[1])) for c in commits]
        touched_assignments = [c for c in assignments if c]
        print('assignments =', touched_assignments)

        # We have a list of (commit, assignment) pairs.
        # Now we need to only keep the latest ones.
        # The original list of commits was ordered newest-to-oldest.
        assignments = set()
        one_commit_per_assignment = []
        for c in touched_assignments:
            if c[1] in assignments:
                continue
            one_commit_per_assignment.append(c)
            assignments.add(c[1])
        print('uniq\'d assignments =', one_commit_per_assignment)

        specs = []
        for c in one_commit_per_assignment:
            specs.append((c[0], load_spec('cs251', c[1])))
        # specs = [hw12, lab2, etc]

        for rev, spec in specs:
            print(nicen(check_for_files_from_spec(rev, spec)))
        # print()
        # for path, folders, files in walk(ref):
        #     print('path =', path)
        #     print('folders =', folders)
        #     print('files =', files)
        # print()


if __name__ == '__main__':
    main()

