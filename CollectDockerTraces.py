##############################################################################
#
# CollectDockerTraces
# 
# A script to collect and merge pcap traces from multiple docker containers
#
# Author: Omar Rubio
#
##############################################################################
import os
import docker


##############################################################################
#
# Modify the following according to your setup:
# 
# The code below results in the following:
#
# TEMPORAL_DIRECTORY = '/home/omarhrc/temp'
# OUTPUT_DIRECTORY = '/home/omarhrc/outpcap'
#
# These directories MUST exist for the script to work
#
##############################################################################
BASE_DIRECTORY = '/home/omarhrc'
TEMPORAL_DIRECTORY = os.path.join(BASE_DIRECTORY, 'temp')
OUTPUT_DIRECTORY = os.path.join(BASE_DIRECTORY, 'omarhrc/outpcap')


##############################################################################
#
# remove_cnf_traces:
# Defines CNF traces are removed from the temporal directory:
# - True: Removes the files
# - False: Keep traces per CNF
#
##############################################################################
remove_cnf_traces = False


##############################################################################
#
# Start of script
#
##############################################################################
CONTAINER_NAMES = {'nr_gnb', 'amf', 'ausf', 'bsf', 'smf', 'udm', 'udr',
                   'nrf', 'nssf', 'pcf', 'upf', 'scp'}
merge_commands = ['mergecap -w mergedtrace.pcapng *.pcapng',
                  f'mv mergedtrace.pcapng {OUTPUT_DIRECTORY}'
                  ]
if remove_cnf_traces:
        merge_commands.append('rm *.pcapng')

client = docker.DockerClient(base_url='unix://var/run/docker.sock')

for container in CONTAINER_NAMES:
        client.containers.run('nicolaka/netshoot', name=f'tcpdump_{container}',
                          network=f'container:{container}',
                          command=f'tcpdump -i eth0 -w {container}.pcapng',
                          detach=True)

input('Press any key when ready to collect traces...')

os.chdir(f'{TEMPORAL_DIRECTORY}')
for container in CONTAINER_NAMES:
    print(f'Processing traces from {container}')
    container_object = client.containers.get(f'tcpdump_{container}')
    pathname = f'{TEMPORAL_DIRECTORY}/{container}.tar'
    f = open(pathname, 'wb')
    bits, stat = container_object.get_archive(f'/root/{container}.pcapng')
    for chunk in bits:
        f.write(chunk)
    f.close()
    os.system(f'tar -xvf {pathname}')
    os.remove(pathname)
    container_object.stop()
    container_object.remove()

for command in merge_commands:
    os.system(command)
print(f'Done!')
