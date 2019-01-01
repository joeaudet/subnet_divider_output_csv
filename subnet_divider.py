# Tool to create list of smaller subnets from a larger subnets
# Written for Python 3
# Author: Joe Audet
# v1 - Print output only
# v2 - Added exporting list to CSV as an entity with each item on a new line
# v3 - Added input verification for base_subnet / base_cidr / desired subnet_size variables

import ipaddress
import csv
import re

output_file = "subnet_list.csv"

def base_subnet_validation(prompt):
    while True:
        try:
            value = input(prompt)
        except ValueError:
            print("Sorry, I didnt understand that input")
            continue
        if validate_ipv4(value):
            print("You entered: " + value)
            break
        else:
            print("Please enter a valid subnet. The following wasn't valid: " + value)
            continue
    return value

def base_cidr_validation(prompt):
    while True:
        try:
            value = input(prompt)
        except ValueError:
            print("Sorry, I didnt understand that input")
            continue
        if validate_cidr(value):
            print("You entered: " + value)
            break
        else:
            print("Please enter a valid CIDR (1-32). The following wasn't valid: " + value)
            continue
    return value

def desired_subnet_size_validation(prompt):
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Sorry, I didnt understand that input")
            continue
        if validate_cidr(str(value)) and validate_desired_subnet_size(value):
            print("You entered for desired subnet size: " + str(value))
            break
        else:
            if validate_cidr(str(value)):
                print("Please enter a CIDR value larger than the subnet you want to divide, which is: " + base_cidr)
            else:
                print("Please enter a valid CIDR (1-32). The following wasn't valid: " + value)
            continue
    return value

def validate_ipv4(ip):
    if re.search('^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', ip):
       return True
    else:
       return False

def validate_cidr(cidr):
    if re.search('^(([1-9])|([1-2][0-9])|(3[0-2]))$', cidr):
        return True
    else:
        return False

def validate_desired_subnet_size(cidr):
    if (int(cidr) > int(base_cidr)):
        return True
    else:
        return False

base_subnet = base_subnet_validation("What is the base subnet you would like to divide? (Do not include mask) ")
base_cidr = base_cidr_validation("What is the base subnet mask in CIDR notation? (Do not include the / - digits only) ")
desired_subnet_size = desired_subnet_size_validation("What size subnets do you want returned, in CIDR notation? (Do not include the / - digits only) ")
output = []

def divide_subnet(base_subnet, base_cidr, desired_subnet_size):
        print("The following base subnet was calculated: " + str(ipaddress.ip_network(base_subnet + "/" + base_cidr, strict=False)))
        output = list(ipaddress.ip_network(base_subnet + "/" + base_cidr, strict=False).subnets(new_prefix=desired_subnet_size))
        with open(output_file, 'w', newline='') as file:
            writer = csv.writer(file, delimiter = '\n')
            writer.writerow(output)
        print("Your output results were stored in the following file: " + output_file)

divide_subnet(base_subnet, base_cidr, desired_subnet_size)
