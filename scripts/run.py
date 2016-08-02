#!/usr/bin/env python3

import os
import subprocess

os.environ['FLASK_APP'] = 'referee.server.flask'
subprocess.run(['python', '-m', 'flask', 'run'])
