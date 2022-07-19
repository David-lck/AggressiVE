import __main__
cdie = __main__.cdie if hasattr(__main__, 'cdie') else None
soc = __main__.soc if hasattr(__main__, 'soc') else None
cpu = __main__.pch if hasattr(__main__, 'cpu') else None
pch = __main__.pch if hasattr(__main__, 'pch') else None
itp = __main__.itp if hasattr(__main__, 'itp') else None
ioe = __main__.ioe if hasattr(__main__, 'ioe') else None
gcd = __main__.gcd if hasattr(__main__, 'gcd') else None
from builtins import *
from builtins import str
from builtins import range
from builtins import object
import namednodes as _namednodes
from namednodes import sv as _sv
cpu = _sv.socket.get_all()[0]
try:
    from tqdm.tqdm import tqdm
except:
    from tqdm import tqdm

class Pre_test:
    def track_attr_cat(attr):
        rw = ['rw',' rw ',' r/w ','r/w',' write/read status ']
        wo = ['wo',' wo ']
        ro = ['ro',' ro ']
        na = ['na',' ']
        rov = ['ro/v','ro_v',' ro variant ']
        rwv = ['rw/v','rw_v']
        rws = ['rw/s',' r/w set ','rws']
        rw1s = ['rw/1s','rw1s']
        rsv = ['rsv',' rsv ']
        rwl = ['rw/l','rw_l',' r/w lock ']
        rwc = ['rw/c',' r/wc ']
        rw1c = ['rw/1c','rw1c']
        if attr in rw:
            return rw
        elif attr in wo:
            return wo
        elif attr in ro:
            return ro
        elif attr in na:
            return na
        elif attr in rov:
            return rov
        elif attr in rwv:
            return rwv
        elif attr in rws:
            return rws
        elif attr in rw1s:
            return rw1s
        elif attr in rsv:
            return rsv
        elif attr in rwl:
            return rwl
        elif attr in rwc:
            return rwc
        elif attr in rw1c:
            return rw1c
        return []
    
    def track_attr_typo(attrs,input_attr):
        for attr in attrs:
            if input_attr in attr:
                return attr
		
    def track_level(input_reg):
        detected_or_userinput_reg = 'detected'
        unknown_level = eval(input_reg+".search('')")
        if unknown_level == []:
            registers = []
            registers.append(input_reg)
            detected_or_userinput_reg = 'userinput'
            return registers,detected_or_userinput_reg
        present_absent_field = eval(input_reg+"."+unknown_level[0]+".search('')")
        if present_absent_field == []:
            #means unknown level is field level (lowest level).
            registers = []
            registers.append(input_reg)
            detected_or_userinput_reg = 'userinput'
        else:
            #means unknown level is register level (not lowest level)
            registers = unknown_level
        return registers,detected_or_userinput_reg

    def track_error_regs(input_reg,in_reg,registers,detected_or_userinput_reg):
        full_registers = []
        error_registers = []
        if in_reg == True:
            print('Detecting error regs...')
            for register in tqdm(registers):
                try:
                    if detected_or_userinput_reg == 'userinput':
                        eval(register)
                        full_registers.append(register)
                    else:
                        eval(input_reg+'.'+register)
                        full_registers.append(input_reg+'.'+register)
                except:
                    error_registers.append(input_reg+'.'+register)
        return full_registers,error_registers
		
    def track_error_fields(in_field,full_registers):
        error_fields = []
        full_fields = []
        if in_field == True:
            print('Detecting error fields...')
            for full_reg in tqdm(full_registers):
                fields = eval(full_reg+".search('')")
                if fields == []:
                    full_fields.append(full_reg)
                else:
                    for field in fields:
                        try:
                            eval(full_reg+'.'+field)
                            full_fields.append(full_reg+'.'+field)
                        except:
                            error_fields.append(full_reg+'.'+field)
        return full_fields,error_fields
		
def fields_2_ips(full_fields):
    print('Detecting all the IPs information...')
    full_ips = []
    for field in full_fields:
        ip = ''
        dot = 0
        for alphabet in field:
            if alphabet == '.':
                dot+=1
            if dot != 3:
                ip+=alphabet
            else:
                break
        if ip not in full_ips:
            full_ips.append(ip)
    return full_ips

def track_invalidate_fields(full_fields):
    print('Detecting the valid and invalid fields...')
    valid_fields = []
    invalid_fields = []
    for field in tqdm(full_fields):
        try:
            eval(field+'.info["attribute"]')
            valid_fields.append(field)
        except:
            invalid_fields.append(field)
    return valid_fields,invalid_fields
	
def track_field_bits(full_field_name):
    numbit = eval(full_field_name+'.info["numbits"]')
    #lowerbit = eval(full_field_name+'.info["lowerbit"]')
    return numbit

def track_num_pass_fail(pass_fail,Pass,Fail,Unknown,Error):
    if pass_fail == 'pass':
        Pass+=1
    elif pass_fail == 'fail':
        Fail+=1
    elif pass_fail == 'NA':
        Unknown+=1
    elif pass_fail == 'error':
        Error+=1
    return Pass,Fail,Unknown,Error
    
def track_chosen_attr_fields(valid_fields,chosen_attr):
    num_chosen_attr_fields = 0
    chosen_attr_fields = []
    for valid_field in valid_fields:
        attr = eval(valid_field+'.info["attribute"]')
        attr = Pre_test.track_attr_cat(attr)
        if attr != []:
            attr = attr[0]
        elif attr == []:
            attr = eval(valid_field+'.info["attribute"]')
        if attr == chosen_attr or chosen_attr == '':
            chosen_attr_fields.append(valid_field)
    return chosen_attr_fields
    
def track_fail_reason(pass_fail_pre_rd,pass_fail_1st_val,pass_fail_2nd_val,pass_fail_3rd_val):
    fail_reason = []
    if pass_fail_pre_rd == 'fail':
        fail_reason.append('Pre_rd')
    if pass_fail_1st_val == 'fail':
        fail_reason.append('1st_val')
    if pass_fail_2nd_val == 'fail':
        fail_reason.append('2nd_val')
    if pass_fail_3rd_val == 'fail':
        fail_reason.append('3rd_val')
    return fail_reason
    