import re

LOG_LINE = re.compile(r'^([A-Z])/([^\(]+)\( *(\d+)\): (.*)\r?$')
BUG_LINE = re.compile(r'.*nativeGetEnabledTags.*')
START_LINE = re.compile(r'^I/am_proc_start\( *\d+\): \[0?,?(\d+),(\d+),([a-zA-Z0-9._:]+),.*,(.*)\]\r?$')
DEATH_LINE = re.compile(r'^I/am_proc_died\( *\d+\): \[0?,?(\d+),([a-zA-Z0-9._:]+),?\d*\]\r?$')
KILL_LINE = re.compile(r'^I/am_kill ?\( *\d+\): \[0?,?(\d+),([a-zA-Z0-9._:]+),.*\]\r?$')
BACKTRACE_LINE = re.compile(r'^#(.*?)pc\s(.*?)$')

