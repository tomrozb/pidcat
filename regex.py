import re

LOG_LINE        = re.compile(r'^(?:[0-9-]* )?([0-9:.]* )?([A-Z])/([^\(]+)\( *(\d+)\): (.*)\r?$')
START_LINE      = re.compile(r'^(?:[0-9-]* )?([0-9:.]* )?I/am_proc_start\( *\d+\): \[0?,?(\d+),(\d+),([a-zA-Z0-9._:]+),.*,(.*)\]\r?$')
DEATH_LINE      = re.compile(r'^(?:[0-9-]* )?([0-9:.]* )?I/am_proc_died\( *\d+\): \[0?,?(\d+),([a-zA-Z0-9._:]+),?\d*\]\r?$')
KILL_LINE       = re.compile(r'^(?:[0-9-]* )?([0-9:.]* )?I/am_kill ?\( *\d+\): \[0?,?(\d+),([a-zA-Z0-9._:]+),.*\]\r?$')
BUG_LINE        = re.compile(r'.*nativeGetEnabledTags.*')

