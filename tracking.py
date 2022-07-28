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

    def track_error_regsname(input_reg):
        print(f'Getting information from {input_reg} ...')
        print('Detecting and storing all the error naming registers...')
        valid_fields = []
        error_regsname = []
        registers_1stsearch = eval(input_reg+".search('')")
        for register1 in tqdm(registers_1stsearch):
            try:
                registers_2ndsearch = eval(input_reg+"."+register1+".search('')")
                if registers_2ndsearch == []:
                    valid_fields.append(input_reg+"."+register1)
                else:
                    for register2 in registers_2ndsearch:
                        try:
                            registers_3rdsearch = eval(input_reg+"."+register1+"."+register2+".search('')")
                            if registers_3rdsearch == []:
                                valid_fields.append(input_reg+'.'+register1+'.'+register2)
                            else:
                                print(f'{input_reg+"."+register1+"."+register2} has more fields.')
                        except:
                            error_regsname.append(input_reg+"."+register1+"."+register2)
            except:
                error_regsname.append(input_reg+"."+register1)
        return error_regsname, valid_fields
		
def track_dif_errors(error_info):
    msg_sorted = []
    for msg in error_info.values():
        if msg not in msg_sorted:
            msg_sorted.append(msg)
    return msg_sorted
	
def track_val_time(num_to_print_regs, prev_est_t, current_reg_timetaken):
    if prev_est_t == 0:
        prev_est_t = 60
    estimated_t_perreg = round((current_reg_timetaken + prev_est_t)/2)#calculate average estimated time taken per register.
    estimated_t = estimated_t_perreg * num_to_print_regs
    return estimated_t_perreg,estimated_t,current_reg_timetaken
		
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
    