import datetime
from atomiceempire import AtomicEmpire

print('Start: ' + str(datetime.datetime.now()))
ae = AtomicEmpire()
ae.get_issue_info('Nightwing 76')
print('End: ' + str(datetime.datetime.now()))
