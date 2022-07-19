from pysvtools import asciitable
try:
	import __main__
	soc = __main__.soc
except:
	from builtins import *
	from builtins import str
	from builtins import range
	from builtins import object
	import namednodes as _namednodes
	from namednodes import sv as _sv
	cpu = _sv.socket.get_all()[0]

def seperate_pkg_and_ip(ip):
	seperated_ip = ip.split('.')
	return seperated_ip[0],seperate_ip[0],seperate_ip[2]
	
def access_method_section(ip):
	value_setaccess = input('Register Access Method:')
	(pkg,ip,sub_ip) = seperate_pkg_and_ip(ip)
	ip.setaccess(value_setaccess)


def main(ip):
	access_metod_section(ip)
	