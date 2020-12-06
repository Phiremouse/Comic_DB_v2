import datetime
from atomicempire import AtomicEmpire

print('Start: ' + str(datetime.datetime.now()))

ae = AtomicEmpire()
ae.get_issue_info('The Flash 1')
print(ae.creators)
print(ae.issue_description)
# ae.show_image()
print('End: ' + str(datetime.datetime.now()))
