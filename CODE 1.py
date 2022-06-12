from yamale import YamaleError
import yamale
from pathlib import Path
import ruamel.yaml
import sys
import yaml


"""
Validation function validates the input conditions with schema as the reference.
"""
def validation():
    #Create a schema object
    schema = yamale.make_schema(r'C:\Users\User\OneDrive\Documents\HPE\Task 1\schema.yml', parser='ruamel')
    # Create a Data object
    try:
        data = yamale.make_data(r'C:\Users\User\OneDrive\Documents\HPE\Task 1\tools-main\tools-main\config\fam_memoryserver_config.yaml', parser='ruamel')
        #print (data)
    except Exception as s: #This line shows an exception if two memory_server_ids are same.
        print('The error is\n%s' % str(s))
    #To validate
    try:
        yamale.validate(schema, data)
        print('Validation success! 👍')
    except ValueError as e:
        print('Validation failed!\n%s' % str(e))
"""
Compare block checks the conditions
"""
def compare():
    host_port = {}
    fam_path_list = {}
    libabric_port_list ={}
    file_in = Path(r'C:\Users\User\OneDrive\Documents\HPE\Task 1\tools-main\tools-main\config\fam_memoryserver_config.yaml')

    yaml = ruamel.yaml.YAML(typ='safe')  # faster than using yaml.safe_load()
    data = yaml.load(file_in)
    for machine_nr, config in data.items():
        if 'rpc_interface' not in config: 
            print(f'machine {machine_nr} has no "rpc_interface"');
            sys.exit(1)
        else:
            host_port.setdefault(config['rpc_interface'], set()).add(machine_nr)
            fam_path_list.setdefault(config['fam_path'], set()).add(machine_nr)
            libabric_port_list.setdefault(config['libfabric_port'], set()).add(machine_nr)
    # now check if host_port has any values that have more than one machine_nr
    for hp, machine_nrs in host_port.items():
        if len(machine_nrs) == 1:
            continue
        j=[str(x) for x in machine_nrs]
        print(f'Found {hp} in machines: {", ".join(j)}')
   
    for hp, machine_nrs in fam_path_list.items():
        if len(machine_nrs) == 1:
            continue
        k=[str(x) for x in machine_nrs]
        print(f'Found {hp} in machines: {", ".join(k)}')

    for hp, machine_nrs in libabric_port_list.items():
        if len(machine_nrs) == 1:
           continue
        l=[str(x) for x in machine_nrs]
        print(f'Found {hp} in machines: {", ".join([str(x) for x in machine_nrs])}')

    def removeElements(j, k):
        return ', '.join(map(str, j)) in ', '.join(map(str, k))

    if (removeElements(j, k)==True) :
        print('The machines from the same system have the same fam_path, hence Validation failed!')
    else:
        print('Only the rpc_interface of the machines are same, hence Validation failed!')
 

    def removeElements(j, l):
        return ', '.join(map(str, j)) in ', '.join(map(str, l))

    if (removeElements(j, l)==True) :
        print('The machines from the same system have the same libfabric_port, hence Validation failed!')
    else:
        print('Only the rpc_interface of the machines are same, hence Validation failed!')

validation()
compare()