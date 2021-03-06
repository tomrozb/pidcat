#!/usr/bin/python -u

'''
Copyright 2009, The Android Open Source Project

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

# Script to highlight adb logcat output for console
# Originally written by Jeff Sharkey, http://jsharkey.org/
# Piping detection and popen() added by other Android team members
# Package filtering and output improvements by Jake Wharton, http://jakewharton.com

import argparse
import sys
import re
import subprocess
from subprocess import PIPE
from regex import *

__version__ = '2.0.0'

LOG_LEVELS = 'VDIWEF'
LOG_LEVELS_MAP = dict([(LOG_LEVELS[i], i) for i in range(len(LOG_LEVELS))])
parser = argparse.ArgumentParser(description='Filter logcat by package name')
parser.add_argument('-p', '--package', nargs='*', metavar='package', dest='package', help='Application package name(s)')
parser.add_argument('-w', '--tag-width', metavar='N', dest='tag_width', type=int, default=22, help='Width of log tag')
parser.add_argument('-l', '--min-level', dest='min_level', type=str, choices=LOG_LEVELS+LOG_LEVELS.lower(), default='V', help='Minimum level to be displayed')
parser.add_argument('-cgc', '--color-gc', dest='color_gc', action='store_true', help='Color garbage collection')
parser.add_argument('--always-display-tags', dest='always_tags', action='store_true',help='Always display the tag name')
parser.add_argument('-ngc', '--no-gc', dest='no_gc', action="store_true", help='Do not show garbage collection info')
parser.add_argument('-nsm', '--no-strict-mode', dest='no_strict_mode', action="store_true", help='Do not show StrictMode info')
parser.add_argument('--lifecycle', dest='lifecycle', action="store_true", help='Show Activity lifecycle info (for tests with Espresso)')
parser.add_argument('-r', '--tag-prefix', nargs='+', metavar='tag_prefix', dest='debug_tag_prefix', type=str, help='Debug tag prefix')
parser.add_argument('-s', '--serial', dest='device_serial', help='Device serial number (adb -s option)')
parser.add_argument('-d', '--device', dest='use_device', action='store_true', help='Use first device for log input (adb -d option)')
parser.add_argument('-e', '--emulator', dest='use_emulator', action='store_true', help='Use first emulator for log input (adb -e option)')
parser.add_argument('-c', '--clear', dest='clear_logcat', action='store_true', help='Clear the entire log before running')
parser.add_argument('-t', '--tag', nargs='+', metavar='tag', dest='debug_tags', type=str, help='Filter output by specified tag(s)')
parser.add_argument('-i', '--ignore-tag', dest='ignored_tag', action='append', help='Filter output by ignoring specified tag(s)')
parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__, help='Print the version number and exit')
parser.add_argument('-ts', '--timestamp', dest='timestamp', action='store_true', help='Show timestamp')

args = parser.parse_args()
min_level = LOG_LEVELS_MAP[args.min_level.upper()]

if args.package:
  # Store the names of packages for which to match all processes.
  catchall_package = filter(lambda package: package.find(":") == -1, args.package)
  # Store the name of processes to match exactly.
  named_processes = filter(lambda package: package.find(":") != -1, args.package)
  # Convert default process names from <package>: (cli notation) to <package> (android notation) in the exact names match group.
  named_processes = map(lambda package: package if package.find(":") != len(package) - 1 else package[:-1], named_processes)

header_size = args.tag_width + 1 + 3 + 1 # space, level, space
if args.timestamp:
  header_size += 13 # '16:06:30.222 '

width = -1
try:
  # Get the current terminal width
  import fcntl, termios, struct
  h, width = struct.unpack('hh', fcntl.ioctl(0, termios.TIOCGWINSZ, struct.pack('hh', 0, 0)))
except:
  pass

wrap_area = width - header_size

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

RESET = '\033[0m'

def termcolor(fg=None, bg=None):
  codes = []
  if fg is not None: codes.append('3%d' % fg)
  if bg is not None: codes.append('10%d' % bg)
  return '\033[%sm' % ';'.join(codes) if codes else ''

def colorize(message, fg=None, bg=None):
  return termcolor(fg, bg) + message + RESET

def indent_wrap(message):
  if width == -1:
    return message
  message = message.replace('\t', '    ')
  wrap_area = width - header_size
  messagebuf = ''
  current = 0
  while current < len(message):
    next = min(current + wrap_area, len(message))
    messagebuf += message[current:next]
    if next < len(message):
      messagebuf += '\n'
      messagebuf += ' ' * header_size
    current = next
  return messagebuf


LAST_USED = [RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN]
KNOWN_TAGS = {
  'dalvikvm': WHITE,
  'dalvikvm-heap': YELLOW,
  'Process': WHITE,
  'ActivityManager': WHITE,
  'ActivityThread': WHITE,
  'jdwp': WHITE,
  'StrictMode': WHITE,
  'LifecycleMonitor': WHITE,
  'AndroidRuntime': YELLOW,
  'JavaBinder' : YELLOW,
  'DEBUG': YELLOW,
  'LeakCanary': YELLOW,
  'SQLiteDatabase': YELLOW,
  'TestRunner' : GREEN
}

def allocate_color(tag):
  # this will allocate a unique format for the given tag
  # since we dont have very many colors, we always keep track of the LRU
  if tag not in KNOWN_TAGS:
    KNOWN_TAGS[tag] = LAST_USED[0]
  color = KNOWN_TAGS[tag]
  if color in LAST_USED:
    LAST_USED.remove(color)
    LAST_USED.append(color)
  return color


RULES = {
  # StrictMode policy violation; ~duration=319 ms: android.os.StrictMode$StrictModeDiskWriteViolation: policy=31 violation=1
  re.compile(r'^(StrictMode policy violation)(; ~duration=)(\d+ ms)')
    : r'%s\1%s\2%s\3%s' % (termcolor(RED), RESET, termcolor(YELLOW), RESET),
}

# Only enable GC coloring if the user opted-in
if args.color_gc:
  # GC_CONCURRENT freed 3617K, 29% free 20525K/28648K, paused 4ms+5ms, total 85ms
  key = re.compile(r'^(GC_(?:CONCURRENT|FOR_M?ALLOC|EXTERNAL_ALLOC|EXPLICIT) )(freed <?\d+.)(, \d+\% free \d+./\d+., )(paused \d+ms(?:\+\d+ms)?)')
  val = r'\1%s\2%s\3%s\4%s' % (termcolor(GREEN), RESET, termcolor(YELLOW), RESET)
  RULES[key] = val

  # TODO add sample for this entry 
  key = re.compile(r'^()((FATAL EXCEPTION: .*))')
  val = r'\1%s\2%s' % (termcolor(RED), RESET)
  RULES[key] = val

  # *** Uncaught remote exception!  (Exceptions are not yet supported across processes.)
  key = re.compile(r'^()((\*\*\* Uncaught remote exception!  .*))')
  val = r'\1%s\2%s' % (termcolor(RED), RESET)
  RULES[key] = val

TAGTYPES = {
  'V': colorize(' V ', fg=WHITE, bg=BLACK),
  'D': colorize(' D ', fg=BLACK, bg=BLUE),
  'I': colorize(' I ', fg=BLACK, bg=GREEN),
  'W': colorize(' W ', fg=BLACK, bg=YELLOW),
  'E': colorize(' E ', fg=BLACK, bg=RED),
  'F': colorize(' F ', fg=WHITE, bg=RED),
}

adb_command = ['adb']
if args.device_serial:
  adb_command.extend(['-s', args.device_serial])
if args.use_device:
  adb_command.append('-d')
if args.use_emulator:
  adb_command.append('-e')
adb_command.append('logcat')
if args.timestamp:
  adb_command.extend(['-v', 'time'])
else:
  adb_command.extend(['-v', 'brief'])
adb_command.extend(['-b', 'events', '-b', 'main', '-b', 'system', '-b', 'crash'])

# Clear log before starting logcat
if args.clear_logcat:
  adb_clear_command = list(adb_command)
  adb_clear_command.append('-c')
  adb_clear = subprocess.Popen(adb_clear_command)

  while adb_clear.poll() is None:
    pass

# This is a ducktype of the subprocess.Popen object
class FakeStdinProcess():
  def __init__(self):
    self.stdout = sys.stdin
  def poll(self):
    return None

if sys.stdin.isatty():
  adb = subprocess.Popen(adb_command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
  first_line = adb.stdout.readline().decode('utf-8', 'replace').strip()
  if (first_line == "Unable to open log device '/dev/log/crash': No such file or directory") or (first_line == "Unable to open log device 'crash'"):
    adb.stdin.close()
    adb = subprocess.Popen(adb_command[:-2], stdin=PIPE, stdout=PIPE, stderr=PIPE)
else:
  adb = FakeStdinProcess()
pids = set()
last_tag = None
debug_tags = args.debug_tags
debug_tag_prefixes = args.debug_tag_prefix

# Initialize empty array
if debug_tags or debug_tag_prefixes:
  if not debug_tags:
    debug_tags = []
  debug_tags.append('Process')
  debug_tags.append('ActivityManager')
  debug_tags.append('ActivityThread')
  debug_tags.append('jdwp')
  if not args.no_strict_mode:
    debug_tags.append('StrictMode')
  debug_tags.append('LifecycleMonitor')
  debug_tags.append('AndroidRuntime')
  debug_tags.append('JavaBinder')
  debug_tags.append('DEBUG')
  debug_tags.append('SQLiteDatabase')
  debug_tags.append('LeakCanary')
  debug_tags.append('TestRunner')
  if not args.no_gc:
    debug_tags.append('dalvikvm-heap')
    debug_tags.append('dalvikvm')

# TODO Lifecycle causes problem with displaying all logs
# (when no tag or tag prefix is provided)
if args.lifecycle:
  if not debug_tags:
    debug_tags = []
  debug_tags.append('LifecycleMonitor')


def match_packages(token):
  if not args.package or len(args.package) == 0:
    return True
  if token in named_processes:
    return True
  index = token.find(':')
  return (token in catchall_package) if index == -1 else (token[:index] in catchall_package)

def dead(dead_pid, dead_package):
  if match_packages(dead_package) and dead_pid in pids:
    pids.remove(dead_pid)
    linebuf  = '\n'
    linebuf += colorize(' ' * (header_size - 1), bg=RED)
    linebuf += ' Process %s (PID: %s) ended' % (dead_package, dead_pid)
    linebuf += '\n'
    print(linebuf)
    last_tag = None # Ensure next log gets a tag printed
  return None

def print_log(timestamp, level, tag, owner, message, custom_bg):
  global last_tag

  if owner not in pids:
    return last_tag
  if args.ignored_tag and tag.strip() in args.ignored_tag:
    return last_tag

  linebuf = ''

  # right-align tag title and allocate color if needed
  tag = tag.strip()
  if tag != last_tag or args.always_tags:
    last_tag = tag
    color = allocate_color(tag)
    tag = tag[-args.tag_width:].rjust(args.tag_width)
    linebuf += colorize(tag, fg=color)
  else:
    linebuf += ' ' * args.tag_width
  linebuf += ' '

  # write out level colored edge
  if level in TAGTYPES:
    linebuf += TAGTYPES[level]
  else:
    linebuf += ' ' + level + ' '
  linebuf += ' '

  # format tag message using rules
  for matcher in RULES:
    replace = RULES[matcher]
    message = matcher.sub(replace, message)

  message = indent_wrap(message)
  if custom_bg:
    message = '\033[0;40m' + message + ' ' * (wrap_area - len(message) % wrap_area) + RESET
  linebuf += message

  # prepend timestamp
  if args.timestamp:
    linebuf = timestamp + linebuf

  print(linebuf.encode('utf-8'))
  return last_tag

while adb.poll() is None:
  try:
    line = adb.stdout.readline().decode('utf-8', 'replace').strip()
  except KeyboardInterrupt:
    break
  if len(line) == 0:
    break

  bug_line = BUG_LINE.match(line)
  if bug_line is not None:
    continue

  start_line = START_LINE.match(line)
  if not start_line is None:
    timestamp, line_pid, line_uid, line_package, target = start_line.groups()

    if match_packages(line_package):
      pids.add(line_pid)
      linebuf  = '\n'
      linebuf += colorize(' ' * (header_size - 1), bg=WHITE)
      linebuf += indent_wrap(' Process created for %s\n' % target)
      linebuf += colorize(' ' * (header_size - 1), bg=WHITE)
      linebuf += ' PID: %s   UID: %s' % (line_pid, line_uid)
      linebuf += '\n'
      print(linebuf)
      last_tag = None # Ensure next log gets a tag printed
      continue

  dead_line = DEATH_LINE.match(line)
  if not dead_line is None:
    timestamp, dead_pid, dead_package = dead_line.groups()
    dead(dead_pid, dead_package)
    continue

  kill_line = KILL_LINE.match(line)
  if not kill_line is None:
    timestamp, kill_pid, kill_package = kill_line.groups()
    dead(kill_pid, kill_package)
    continue

  log_line = LOG_LINE.match(line)
  if not log_line is None:
    timestamp, level, tag, owner, message = log_line.groups()
    handled = False
    if level in LOG_LEVELS_MAP and LOG_LEVELS_MAP[level] < min_level and tag.strip() != 'DEBUG':
        continue
    if debug_tag_prefixes:
      stripped = tag.strip()
      for tag_prefix in debug_tag_prefixes:
        if stripped.startswith(tag_prefix):
          handled = True
          print_log(timestamp, level, tag, owner, message, True)
    if not handled:
      if debug_tags:
        if (tag.strip() in debug_tags):
          print_log(timestamp, level, tag, owner, message, False)
      elif not debug_tag_prefixes:
        print_log(timestamp, level, tag, owner, message, False)
