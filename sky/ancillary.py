#!/usr/bin/env python3

#tresholds for packets
class trsh:
    HIGH = 50
    MEDIUM = 10
    LOW = 5

#colors
class bcolors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'



def replace_tab(s, tabstop = 4):
  result = str()
  for c in s:
    if c == '\t':
      while (len(result) % tabstop != 0):
        result += ' ';
    else:
      result += c    
  return result
