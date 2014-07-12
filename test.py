import unittest
from regex import *

am_create_activity = {}
am_proc_start = {}
am_proc_bound = {}
am_restart_activity = {}
am_resume_activity = {}
am_on_resume_called = {}
am_activity_launch_time = {}
am_pause_activity = {}
am_on_paused_called = {}
am_destroy_activity = {}
am_kill = {}
am_proc_died = {}
am_finish_activity = {}

# TEMPLATE # 15 lines
# Samsung Galaxy []
#model = ''
#am_create_activity[model] = ''
#am_proc_start[model] = ''
#am_proc_bound[model] = ''
#am_restart_activity[model] = ''
#am_resume_activity[model] = ''
#am_on_resume_called[model] = ''
#am_activity_launch_time[model] = ''
#am_pause_activity[model] = ''
#am_on_paused_called[model] = ''
#am_destroy_activity[model] = ''
#am_kill[model] = ''
#am_proc_died[model] = ''
#am_finish_activity[model] = ''

# Samsung Galaxy S4 [4.2.2]
model = 'Samsung Galaxy S4 [4.2.2]'
am_create_activity[model] = ''
am_proc_start[model] = 'I/am_proc_start(  782): [0,1448,10222,com.pkg,activity,com.pkg/.Activity]'
am_proc_bound[model] = ''
am_restart_activity[model] = ''
am_resume_activity[model] = ''
am_on_resume_called[model] = ''
am_activity_launch_time[model] = ''
am_pause_activity[model] = ''
am_on_paused_called[model] = ''
am_destroy_activity[model] = ''
am_kill[model] = 'I/am_kill (  782): [0,9547,com.pkg,15,old background process]'
am_proc_died[model] = 'I/am_proc_died(  782): [0,11610,com.pkg,0]'
am_finish_activity[model] = ''

# Samsung Galaxy Nexus [4.2.2]
model = 'Samsung Galaxy Nexus [4.2.2]'
am_create_activity[model] = ''
am_proc_start[model] = 'I/am_proc_start(  389): [0,8937,10070,com.pkg,activity,com.pkg/.Activity]'
am_proc_bound[model] = ''
am_restart_activity[model] = ''
am_resume_activity[model] = ''
am_on_resume_called[model] = ''
am_activity_launch_time[model] = ''
am_pause_activity[model] = ''
am_on_paused_called[model] = ''
am_destroy_activity[model] = ''
am_kill[model] = 'I/am_kill (  389): [0,9771,com.pkg:Service,15,old background process]'
am_proc_died[model] = 'I/am_proc_died(  389): [0,8445,com.pkg]'
am_finish_activity[model] = ''

# Samsung Galaxy Note 10.1 [4.2.1]
model = 'Samsung Galaxy Note 10.1 [4.2.1]'
am_create_activity[model] = ''
am_proc_start[model] = 'I/am_proc_start( 2352): [9767,10149,com.pkg,activity,com.pkg/.Activity]'
am_proc_bound[model] = ''
am_restart_activity[model] = ''
am_resume_activity[model] = ''
am_on_resume_called[model] = ''
am_activity_launch_time[model] = ''
am_pause_activity[model] = ''
am_on_paused_called[model] = ''
am_destroy_activity[model] = ''
am_kill[model] = 'I/am_kill ( 2352): [5440,com.pkg_text,14,too many background]'
am_proc_died[model] = 'I/am_proc_died( 2352): [3402,com.pkg:Service,14]'
am_finish_activity[model] = ''

# Samsung Galaxy S+ [2.3.6]
model = 'Samsung Galaxy S+ [2.3.6]'
am_create_activity[model] = ''
am_proc_start[model] = 'I/am_proc_start(  185): [1785,10081,com.pkg,activity,com.pkg/.Activity]'
am_proc_bound[model] = ''
am_restart_activity[model] = ''
am_resume_activity[model] = ''
am_on_resume_called[model] = ''
am_activity_launch_time[model] = ''
am_pause_activity[model] = ''
am_on_paused_called[model] = ''
am_destroy_activity[model] = ''
am_kill[model] = 'I/am_kill (  185): [17575,com.pkg,12,too many background]'
am_proc_died[model] = 'I/am_proc_died(  185): [17858,com.pkg]'
am_finish_activity[model] = ''

# Samsung Galaxy S3 [4.2.2]
model = 'Samsung Galaxy S3 [4.2.2]'
am_create_activity[model] = 'I/am_create_activity( 2342): [0,1109076088,18,com.pkg/.Activity,android.intent.action.MAIN,NULL,NULL,268435456,2000]'
am_proc_start[model] = 'I/am_proc_start( 2342): [0,17762,10150,com.pkg,activity,com.pkg/.Activity]'
am_proc_bound[model] = 'I/am_proc_bound( 2342): [0,17762,com.pkg]'
am_restart_activity[model] = 'I/am_restart_activity( 2342): [0,1109076088,18,com.pkg/.Activity]'
am_resume_activity[model] = ''
am_on_resume_called[model] = 'I/am_on_resume_called(17762): [0,com.pkg.Activity]'
am_activity_launch_time[model] = 'I/am_activity_launch_time( 2342): [0,1109076088,com.pkg/.Activity,309,309]'
am_pause_activity[model] = 'I/am_pause_activity( 2342): [0,1109076088,com.pkg/.Activity]'
am_on_paused_called[model] = 'I/am_on_paused_called(17762): [0,com.pkg.Activity]'
am_destroy_activity[model] = 'I/am_destroy_activity( 2342): [0,1109076088,18,com.pkg/.Activity,always-finish]'
am_kill[model] = 'I/am_kill ( 2342): [0,17762,com.pkg,15,too many background]'
am_proc_died[model] = 'I/am_proc_died( 2342): [0,17762,com.pkg,15]'
am_finish_activity[model] = 'I/am_finish_activity( 2342): [0,1109076088,18,com.pkg/.Activity,proc died without state saved]'

# Samsung Galaxy Note 2 [4.1.2]
model = 'Samsung Galaxy Note 2 [4.1.2]'
am_create_activity[model] = 'I/am_create_activity( 2263): [1137291104,5,com.pkg/.Activity,android.intent.action.MAIN,NULL,NULL,268435456]'
am_proc_start[model] = 'I/am_proc_start( 2263): [9910,10151,com.pkg,activity,com.pkg/.Activity]'
am_proc_bound[model] = 'I/am_proc_bound( 2263): [9910,com.pkg]'
am_restart_activity[model] = 'I/am_restart_activity( 2263): [1137291104,5,com.pkg/.Activity]'
am_resume_activity[model] = 'I/am_resume_activity( 2263): [1137291104,5,com.pkg/.Activity]'
am_on_resume_called[model] = 'I/am_on_resume_called( 9910): com.pkg.Activity'
am_activity_launch_time[model] = 'I/activity_launch_time( 2263): [1137291104,com.pkg/.Activity,244,96004]'
am_pause_activity[model] = 'I/am_pause_activity( 2263): [1137291104,com.pkg/.Activity]'
am_on_paused_called[model] = 'I/am_on_paused_called( 9910): com.pkg.Activity'
am_destroy_activity[model] = ''
am_kill[model] = 'I/am_kill ( 2263): [15437,com.pkg,10,too many background]'
am_proc_died[model] = 'I/am_proc_died( 2263): [9910,com.pkg,7]'
am_finish_activity[model] = ''

# Samsung Galaxy Camera [4.1.2]
model = 'Samsung Galaxy Camera [4.1.2]'
am_create_activity[model] = 'I/am_create_activity( 2131): [1119376232,13,com.pkg/.Activity,NULL,NULL,NULL,268435456]'
am_proc_start[model] = 'I/am_proc_start( 2131): [15700,10132,com.pkg,activity,com.pkg/.Activity]'
am_proc_bound[model] = 'I/am_proc_bound( 2131): [15700,com.pkg]'
am_restart_activity[model] = 'I/am_restart_activity( 2131): [1119376232,13,com.pkg/.Activity]'
am_resume_activity[model] = ''
am_on_resume_called[model] = 'I/am_on_resume_called(15700): com.pkg.Activity'
am_activity_launch_time[model] = 'I/activity_launch_time( 2131): [1119376232,com.pkg/.Activity,304,304]'
am_pause_activity[model] = 'I/am_pause_activity( 2131): [1119376232,com.pkg/.Activity]'
am_on_paused_called[model] = 'I/am_on_paused_called(15700): com.pkg.Activity'
am_destroy_activity[model] = 'I/am_destroy_activity( 2131): [1119376232,13,com.pkg/.Activity,always-finish]'
am_kill[model] = 'I/am_kill ( 2131): [15700,com.pkg,10,too many background]'
am_proc_died[model] = 'I/am_proc_died( 2131): [15700,com.pkg,10]'
am_finish_activity[model] = 'I/am_finish_activity( 2131): [1121464424,12,com.pkg/.Activity,proc died without state saved]'


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
