import re

LOG_LINE = re.compile(r'^([A-Z])/([^\(]+)\( *(\d+)\): (.*)\r?$')
BUG_LINE = re.compile(r'^(?!.*(nativeGetEnabledTags)).*$')
START_LINE = re.compile(r'^I/am_proc_start\( *\d+\): \[\d*,?(\d+),(\d+),([a-zA-Z0-9._:]+),.*,(.*)\]\r?$')
DEATH_LINE = re.compile(r'^I/am_proc_died\( *\d+\): \[\d*,?(\d+),([a-zA-Z0-9._:]+),?\d*\]\r?$')
KILL_LINE = re.compile(r'^I/am_kill ?\( *\d+\): \[\d*,?(\d+),([a-zA-Z0-9._:]+),.*\]\r?$')
