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

import os
import sys
import subprocess

def git(*cmd):
    return subprocess.check_output(['git', *cmd], universal_newlines=True)

def git_show(*args):
    return git('show', *args)

def git_log(*args):
    print(args)
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


def main():
    for line in sys.stdin:
        oldrev, newrev, ref = line.split()
        print(git_log('--oneline', '{}..{}'.format(oldrev, newrev)))
        for path, folders, files in walk(ref):
            print('path =', path)
            print('folders =', folders)
            print('files =', files)


if __name__ == '__main__':
    main()

