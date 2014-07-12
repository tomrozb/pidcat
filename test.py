import unittest
from regex import *

am_proc_start = {}
am_proc_died = {}
am_kill = {}

# Samsung Galaxy S4 [4.2.2]
model = 'Samsung Galaxy S4 [4.2.2]'
am_proc_start[model] = 'I/am_proc_start(  782): [0,1448,10222,com.package,activity,com.package/.Activity]'
am_proc_died[model] = 'I/am_proc_died(  782): [0,11610,com.package,0]'
am_kill[model] = 'I/am_kill (  782): [0,9547,com.package,15,old background process]'

# Samsung Galaxy Nexus [4.2.2]
model = 'Samsung Galaxy Nexus [4.2.2]'
am_proc_start[model] = 'I/am_proc_start(  389): [0,8937,10070,com.package,activity,com.package/.Activity]'
am_proc_died[model] = 'I/am_proc_died(  389): [0,8445,com.package]'
am_kill[model] = 'I/am_kill (  389): [0,9771,com.package:Service,15,old background process]'

# Samsung Galaxy Note 10.1 [4.2.1]
model = 'Samsung Galaxy Note 10.1 [4.2.1]'
am_proc_start[model] = 'I/am_proc_start( 2352): [9767,10149,com.package,activity,com.package/.Activity]'
am_proc_died[model] = 'I/am_proc_died( 2352): [3402,com.package:Service,14]'
am_kill[model] = 'I/am_kill ( 2352): [5440,com.package_text,14,too many background]'

# Samsung Galaxy S+ [2.3.6]
model = 'Samsung Galaxy S+ [2.3.6]'
am_proc_start[model] = 'I/am_proc_start(  185): [1785,10081,com.package,activity,com.package/.Activity]'
am_proc_died[model] = 'I/am_proc_died(  185): [17858,com.package]'
am_kill[model] = 'I/am_kill (  185): [17575,com.package,12,too many background]'


def matchRegex(self, regex, **dict):
    for (key, value) in dict.items():
        self.assertIsNotNone(regex.match(value), '[%s] %s' % (key, value))


class TestRegex(unittest.TestCase):
    def test_am_proc_start(self):
        matchRegex(self, START_LINE, **am_proc_start)

    def test_am_proc_died(self):
        matchRegex(self, DEATH_LINE, **am_proc_died)

    def test_am_kill(self):
        matchRegex(self, KILL_LINE, **am_kill)

if __name__ == "__main__":
    unittest.main()
