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

# Samsung Galaxy S3 [4.2.2]
I/am_create_activity( 2342): [0,1109076088,18,com.packag/.MyActivity,android.intent.action.MAIN,NULL,NULL,268435456,2000]
I/am_proc_start( 2342): [0,17762,10150,com.packag,activity,com.packag/.MyActivity]
I/am_proc_bound( 2342): [0,17762,com.packag]
I/am_restart_activity( 2342): [0,1109076088,18,com.packag/.MyActivity]
I/am_on_resume_called(17762): [0,com.packag.MyActivity]
I/am_activity_launch_time( 2342): [0,1109076088,com.packag/.MyActivity,309,309]
I/am_pause_activity( 2342): [0,1109076088,com.packag/.MyActivity]
I/am_on_paused_called(17762): [0,com.packag.MyActivity]
I/am_destroy_activity( 2342): [0,1109076088,18,com.packag/.MyActivity,always-finish]
I/am_kill ( 2342): [0,17762,com.packag,15,too many background]
I/am_proc_died( 2342): [0,17762,com.packag,15]
I/am_proc_start( 2342): [0,18442,10150,com.packag,activity,com.packag/.MyActivity]
I/am_proc_bound( 2342): [0,18442,com.packag]
I/am_restart_activity( 2342): [0,1109076088,18,com.packag/.MyActivity]
I/am_on_resume_called(18442): [0,com.packag.MyActivity]
I/am_activity_launch_time( 2342): [0,1109076088,com.packag/.MyActivity,287,287]
I/am_proc_died( 2342): [0,18442,com.packag,0]
I/am_finish_activity( 2342): [0,1109076088,18,com.packag/.MyActivity,proc died without state saved]

# Samsung Galaxy Note 2 [4.1.2]
I/am_create_service( 2263): [1138765776,com.google.android.gms/.icing.impl.IndexService,act=android.intent.action.PACKAGE_REMOVED dat=package:com.packag,7825]
I/notification_cancel_all( 2263): [com.packag,0,0]
I/am_create_service( 2263): [1138076392,com.android.keychain/.KeyChainService,act=android.intent.action.PACKAGE_REMOVED dat=package:com.packag,9328]
I/am_create_service( 2263): [1137171248,com.google.android.apps.plus/.service.PackagesMediaMonitor$AsyncService,act=android.intent.action.PACKAGE_REMOVED dat=package:com.packag,4464]
I/am_create_service( 2263): [1139738960,com.google.android.partnersetup/.RlzPingIntentService,act=android.intent.action.PACKAGE_ADDED dat=package:com.packag,6813]
I/am_create_service( 2263): [1139674104,com.google.android.partnersetup/.AppInstalledService,dat=package:com.packag,6813]
I/am_create_service( 2263): [1139597312,com.google.android.apps.plus/.service.PackagesMediaMonitor$AsyncService,act=android.intent.action.PACKAGE_ADDED dat=package:com.packag,4464]
I/am_create_activity( 2263): [1137291104,5,com.packag/.MyActivity,android.intent.action.MAIN,NULL,NULL,268435456]
I/am_proc_start( 2263): [9910,10151,com.packag,activity,com.packag/.MyActivity]
I/am_proc_bound( 2263): [9910,com.packag]
I/am_restart_activity( 2263): [1137291104,5,com.packag/.MyActivity]
I/am_pause_activity( 2263): [1137291104,com.packag/.MyActivity]
I/am_on_resume_called( 9910): com.packag.MyActivity
I/am_on_paused_called( 9910): com.packag.MyActivity
I/activity_launch_time( 2263): [1137291104,com.packag/.MyActivity,244,96004]
I/am_resume_activity( 2263): [1137291104,5,com.packag/.MyActivity]
I/am_on_resume_called( 9910): com.packag.MyActivity
I/am_pause_activity( 2263): [1137291104,com.packag/.MyActivity]
I/am_on_paused_called( 9910): com.packag.MyActivity
I/am_proc_died( 2263): [9910,com.packag,7]




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
