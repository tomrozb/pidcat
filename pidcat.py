#!/usr/bin/python

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
# Written by Jeff Sharkey, http://jsharkey.org/
# Piping detection and popen() added by other Android team members
# Package name restriction by Jake Wharton, http://jakewharton.com

import argparse
import os
import sys
import re
import fcntl
import termios
import struct
from regex import *


parser = argparse.ArgumentParser(description='Filter logcat by package name')
parser.add_argument('-p', nargs='+', metavar='package', dest='package', help='Application package name(s)')
parser.add_argument('--tag-width', metavar='N', dest='tag_width', type=int, default=22, help='Width of log tag')
parser.add_argument('--color-gc', dest='color_gc', action='store_true', help='Color garbage collection')
parser.add_argument('--no-gc', dest='no_gc', action="store_true", help='Show garbage collection info')
parser.add_argument('-t', nargs='+', metavar='tag', dest='debug_tags', type=str, help='Debug tag')
parser.add_argument('-s', '--serial', dest='device_serial', help='Device serial number (adb -s option)')

args = parser.parse_args()
serial=args.device_serial

header_size = args.tag_width + 1 + 3 + 1 # space, level, space

# unpack the current terminal width/height
data = fcntl.ioctl(sys.stdout.fileno(), termios.TIOCGWINSZ, '1234')
HEIGHT, WIDTH = struct.unpack('hh',data)

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

RESET = '\033[0m'

def  termcolor(fg=None, bg=None):
  codes = []
  if fg is not None: codes.append('3%d' % fg)
  if bg is not None: codes.append('10%d' % bg)
  return '\033[%sm' % ';'.join(codes) if codes else ''

def colorize(message, fg=None, bg=None):
  return termcolor(fg, bg) + message + RESET

def indent_wrap(message):
  wrap_area = WIDTH - header_size
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
  'Process': WHITE,
  'ActivityManager': WHITE,
  'ActivityThread': WHITE,
  'AndroidRuntime': CYAN,
  'JavaBinder' : CYAN,
  'jdwp': WHITE,
  'StrictMode': WHITE,
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


device = ''

if serial != None:
  device = "-s " + serial

input = os.popen('adb %s logcat -b events -b main -b system' % device)
pids = set()
last_tag = None
debug_tags = args.debug_tags

if debug_tags:
  debug_tags.append('AndroidRuntime')
  debug_tags.append('Process')
  debug_tags.append('ActivityManager')
  debug_tags.append('ActivityThread')
  debug_tags.append('jdwp')
  debug_tags.append('StrictMode')
  debug_tags.append('JavaBinder')

if not args.no_gc:
  debug_tags.append('dalvikvm')


def match_packages(token):
  index = token.find(':')
  return (token in args.package) if index == -1 else (token[:index] in args.package)

def dead(pid, package):
  if match_packages(package) and pid in pids:
    pids.remove(pid)
    linebuf  = '\n'
    linebuf += colorize(' ' * (header_size - 1), bg=RED)
    linebuf += ' Process %s ended' % pid
    linebuf += '\n'
    print(linebuf)
    last_tag = None # Ensure next log gets a tag printed
  return None

def print_log(level, tag, owner, message):
  global last_tag

  if owner not in pids:
    return last_tag

  linebuf = ''

  # right-align tag title and allocate color if needed
  tag = tag.strip()
  if tag != last_tag:
    last_tag = tag
    color = allocate_color(tag)
    tag = tag[-args.tag_width:].rjust(args.tag_width)
    linebuf += colorize(tag, fg=color)
  else:
    linebuf += ' ' * args.tag_width
  linebuf += ' '

  # write out level colored edge
  #if level not in TAGTYPES: break
  linebuf += TAGTYPES[level]
  linebuf += ' '

  # format tag message using rules
  for matcher in RULES:
    replace = RULES[matcher]
    message = matcher.sub(replace, message)

  linebuf += indent_wrap(message)
  print(linebuf)
  return last_tag

while True:
  try:
    line = input.readline()
  except KeyboardInterrupt:
    break
  if len(line) == 0:
    break

  bug_line = BUG_LINE.match(line)
  if bug_line is None:
    continue

  start_line = START_LINE.match(line)
  if not start_line is None:
    line_pid, line_uid, line_package, target = start_line.groups()

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
    dead_pid, dead_package = dead_line.groups()
    dead(dead_pid, dead_package)
    continue

  kill_line = KILL_LINE.match(line)
  if not kill_line is None:
    kill_pid, kill_package = kill_line.groups()
    dead(kill_pid, kill_package)
    continue

  log_line = LOG_LINE.match(line)
  if not log_line is None:
    level, tag, owner, message = log_line.groups()
    if debug_tags:
      if (tag.strip() in debug_tags):
        print_log(level, tag, owner, message)
    else:
      print_log(level, tag, owner, message)
