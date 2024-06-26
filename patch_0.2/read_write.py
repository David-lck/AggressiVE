import __main__
cdie = __main__.cdie if hasattr(__main__, 'cdie') else None
soc = __main__.soc if hasattr(__main__, 'soc') else None
cpu = __main__.pch if hasattr(__main__, 'cpu') else None
pch = __main__.pch if hasattr(__main__, 'pch') else None
itp = __main__.itp if hasattr(__main__, 'itp') else None
ioe = __main__.ioe if hasattr(__main__, 'ioe') else None
gcd = __main__.gcd if hasattr(__main__, 'gcd') else None
import time
import colorama
from colorama import Fore
from builtins import *
from builtins import str
from builtins import range
from builtins import object
import namednodes as _namednodes
from namednodes import sv as _sv
cpu = _sv.socket.get_all()[0]
import display_output as disp
import tracking as track
import user_input as user
import export_log_file as dump
import sys
try:
    from tqdm.tqdm import tqdm
except:
    from tqdm import tqdm
import pysvtools.fv_common.target as target
from meteorlake import debug


all_undefined_attrs = ['dc','ro/c/v','ro/p','ro/v','ro/v/p','rw/1c/p','rw/1c/v','rw/1c/v/p','rw/0c/v','rw/1s/v/p','rw/1s/v','rw/1s/v/l','rw/ac','rw/l/k','rw/o/p','rw/o/v/l','rw/p','rw/p/l','rw/s/l','rw/fuse','rw/strap','rw/v','rw/v/p','rw/v/l','rw/v/p/l','rw/v2']

class Conv:
    def convert_bin_to_hex(bin_value):
        dec_value = Conv.convert_bin_to_dec(bin_value)
        hex_value = Conv.convert_dec_to_hex(dec_value)
        return hex_value

    def convert_bin_to_dec(bin_value):
        dec_value = int(bin_value,2)
        dec_value = str(dec_value)
        return dec_value

    def convert_dec_to_hex(dec_value):
        hex_value = hex(int(dec_value))
        return hex_value

    def convert_hex_to_bin(hex_value):
        bin_value = bin(int(hex_value, 16))[2:]
        return bin_value
    
class Algorithm:
    def val_roc(numbit,val_stage,compare_value):
        wr = compare_value[0]
        rd1 = compare_value[1]
        rd2 = compare_value[2]
        pre_rd1 = compare_value[3]
        pre_rd2 = compare_value[4]
        if val_stage == 'pre_rd':
            if pre_rd2 == '0':
                return 'pass'
            else:
                return 'fail'
        elif val_stage == '1st_stage_rdwr':
            if rd1 == '0':
                return 'pass'
            else:
                return 'fail'

    def val_rwcr(numbit,val_stage,compare_value):
        wr = compare_value[0]
        rd1 = compare_value[1]
        rd2 = compare_value[2]
        pre_rd1 = compare_value[3]
        pre_rd2 = compare_value[4]
        if rd1 == wr and rd2 == '0':
            return 'pass'
        else:
            return 'fail'

    def val_wo1(numbit,val_stage,compare_value):
        wr = compare_value[0]
        rd1 = compare_value[1]
        pre_rd1 = compare_value[2]
        pre_rd2 = compare_value[3]
        if rd1 == '0':
            return 'pass'
        else:
            return 'fail'
    
    def val_woc(numbit,val_stage,compare_value):
        pass_fail = Algorithm.val_wo1(numbit,val_stage,compare_value)
        return pass_fail

    def val_na(numbit,val_stage,compare_value):
        wr = compare_value[0]
        rd1 = compare_value[1]
        pre_rd1 = compare_value[2]
        pre_rd2 = compare_value[3]
        if val_stage == 'pre_rd':
            if pre_rd1 == '0' and pre_rd2 == '0':
                return 'pass'
            else:
                return 'fail'
        if rd1 == '0':
            return 'pass'
        else:
            return 'fail'

    def val_rw0cfw(numbit,val_stage,compare_value):
        wr = compare_value[0]
        rd1 = compare_value[1]
        pre_rd1 = compare_value[2]
        pre_rd2 = compare_value[3]
        if rd1 == wr:
            return 'pass'
        else:
            return 'fail'
        
    def val_rw1cfw(numbit,val_stage,compare_value):
        pass_fail = Algorithm.val_rw0cfw(numbit,val_stage,compare_value)
        return pass_fail
    
    def val_db(numbit,val_stage,compare_value):
        pass_fail = Algorithm.val_rw0cfw(numbit,val_stage,compare_value)
        return pass_fail
    
    def val_rwhwc(numbit,val_stage,compare_value):
        pass_fail = Algorithm.val_rw0cfw(numbit,val_stage,compare_value)
        return pass_fail
    
    def val_r32wonly(numbit,val_stage,compare_value):
        pass_fail = Algorithm.val_rw0cfw(numbit,val_stage,compare_value)
        return pass_fail
    
    def val_rwfwo(numbit,val_stage,compare_value):
        pass_fail = Algorithm.val_rw0cfw(numbit,val_stage,compare_value)
        return pass_fail

    def val_roswc(numbit,val_stage,compare_value):#WIP due to not exist in system.
        all_one_value = '1'*numbit
        all_one_value = Conv.convert_bin_to_hex(all_one_value)
        wr=compare_value[0]
        rd1=compare_value[1]
        if val_stage == 'pre_rd':
            if wr == '0x0' and rd == all_one_value:
                return 'pass'
            else:
                return 'fail'
        elif val_stage in['1st_stage_rdwr','2nd_stage_rdwr','3rd_stage_rdwr']:
            rd2 = compare_value[2]
            if wr == rd1 and rd1 == rd2:
                return 'pass'
            return 'fail'

    def val_ro(numbit,compare_value):
        wr = compare_value[0]
        rd = compare_value[1]
        pre_rd = compare_value[2]
        if rd == pre_rd:
            return 'pass'
        else:
            return 'fail'
    
    def val_wo(numbit,compare_value):
        return Algorithm.val_ro(numbit,compare_value)
    
    def val_rw(numbit,compare_value):
        wr = compare_value[0]
        rd = compare_value[1]
        if rd == wr:
            return 'pass'
        else:
            return 'fail'
    
    def val_rws(numbit,val_stage,compare_value):
        wr = compare_value[0]
        rd = compare_value[1]
        pre_rd = compare_value[2]
        wr_in_bin = Conv.convert_hex_to_bin(wr)
        rd_in_bin = Conv.convert_hex_to_bin(rd)
        pre_rd_in_bin = Conv.convert_hex_to_bin(pre_rd)
        if len(wr_in_bin) > len(rd_in_bin):#add zero in front of rd due to rd bit lower than wr bit
            num_bit_dif = len(wr_in_bin) - len(rd_in_bit)
            rd_in_bin = ('0' * num_bit_dif) + rd_in_bin
        elif len(wr_in_bin) < len(rd_in_bin):#add zero in front of wd due to rd bit lower than rd bit
            num_bit_dif = len(rd_in_bin) - len(wr_in_bin)
            wr_in_bin = ('0' * num_bit_dif) + wr_in_bin
        if val_stage == '1st_stage_rdwr':
            (result_value1,result_value0) = Bit_Compare.compare_bit2bit(wr_in_bin,rd_in_bin)
            (result_value0) = Bit_Compare.compare_bit2bit_with_prerd(pre_rd_in_bin,wr_in_bin,rd_in_bin,'pre')
            if 'different' not in result_value1 and result_value0 in ['pre','no_zero']:
                return 'pass'
            elif result_value1 == [] or result_value0 == []:
                return Bit_Compare.single_bit_pass_fail(result_value0,result_value1,'different','same')
        elif val_stage == '2nd_stage_rdwr':
            (result_value1,result_value0) = Bit_Compare.compare_bit2bit(wr_in_bin,rd_in_bin)
            if 'same' not in result_value0 and 'different' not in result_value1:
                return 'pass'
            elif result_value1 == [] or result_value0 == []:
                return Bit_Compare.single_bit_pass_fail(result_value0,result_value1,'different','same')
        elif val_stage == '3rd_stage_rdwr':
            (result_value1,result_value0) = Bit_Compare.compare_bit2bit(wr_in_bin,rd_in_bin)
            if 'different' not in result_value1 and 'same' not in result_value0:
                return 'pass'
            elif result_value1 == [] or result_value0 == []:
                return Bit_Compare.single_bit_pass_fail(result_value0,result_value1,'different','same')
        return 'fail'
    
    def val_rwl(numbit,val_stage,compare_value):
        pass_fail = Algorithm.val_rws(numbit,val_stage,compare_value)
        return pass_fail
    
    def val_rwo(numbit,val_stage,compare_value):
        wr = compare_value[0]
        rd = compare_value[1]
        pre_rd = compare_value[2]
        wr_in_bin = Conv.convert_hex_to_bin(wr)
        rd_in_bin = Conv.convert_hex_to_bin(rd)
        pre_rd_in_bin = Conv.convert_hex_to_bin(pre_rd)
        if len(wr_in_bin) > len(rd_in_bin):
            num_bit_dif = len(wr_in_bin) - len(rd_in_bit)
            rd_in_bin = ('0' * num_bit_dif) + rd_in_bin
        elif len(wr_in_bin) < len(rd_in_bin):
            num_bit_dif = len(rd_in_bin) - len(wr_in_bin)
            wr_in_bin = ('0' * num_bit_dif) + wr_in_bin
        if val_stage in ['1st_stage_rdwr','3rd_stage_rdwr']:
            (result_value1,result_value0) = Bit_Compare.compare_bit2bit(wr_in_bin,rd_in_bin)
            if 'different' not in result_value0 and 'different' not in result_value1:
                return 'pass'
            elif result_value1 == [] or result_value0 == []:
                return Bit_Compare.single_bit_pass_fail(result_value0,result_value1,'same','same')
        elif val_stage == '2nd_stage_rdwr':
            (result_value1,result_value0) = Bit_Compare.compare_bit2bit(wr_in_bin,rd_in_bin)
            if 'same' not in result_value0 and 'same' not in result_value1:
                return 'pass'
            elif result_value1 == [] or result_value0 == []:
                return Bit_Compare.single_bit_pass_fail(result_value0,result_value1,'different','different')
        return 'fail'

    def val_rw1c(numbit,val_stage,compare_value):
        wr = compare_value[0]
        rd = compare_value[1]
        pre_rd = compare_value[2]
        wr_in_bin = Conv.convert_hex_to_bin(wr)
        rd_in_bin = Conv.convert_hex_to_bin(rd)
        pre_rd_in_bin = Conv.convert_hex_to_bin(pre_rd)
        if len(wr_in_bin) > len(rd_in_bin):
            num_bit_dif = len(wr_in_bin) - len(rd_in_bit)
            rd_in_bin = ('0' * num_bit_dif) + rd_in_bin
        elif len(wr_in_bin) < len(rd_in_bin):
            num_bit_dif = len(rd_in_bin) - len(wr_in_bin)
            wr_in_bin = ('0' * num_bit_dif) + wr_in_bin
        if val_stage == '1st_stage_rdwr':
            (result_value1,result_value0) = Bit_Compare.compare_bit2bit(wr_in_bin,rd_in_bin)
            (result_value0) = Bit_Compare.compare_bit2bit_with_prerd(pre_rd_in_bin,wr_in_bin,rd_in_bin,'pre')
            if 'same' not in result_value1 and result_value0 in ['pre','no_zero']:
                return 'pass'
            elif result_value1 == [] or result_value0 == []:
                return Bit_Compare.single_bit_pass_fail(result_value0,result_value1,['pre','no_zero'],'different')
        elif val_stage == '2nd_stage_rdwr':
            (result_value1,result_value0) = Bit_Compare.compare_bit2bit(wr_in_bin,rd_in_bin)
            if 'different' not in result_value0 and 'same' not in result_value1:
                return 'pass'
            elif result_value1 == [] or result_value0 == []:
                return Bit_Compare.single_bit_pass_fail(result_value0,result_value1,'same','different')
        elif val_stage == '3rd_stage_rdwr':
            (result_value1,result_value0) = Bit_Compare.compare_bit2bit(wr_in_bin,rd_in_bin)
            if 'different' not in result_value0 and 'same' not in result_value1:
                return 'pass'
            elif result_value1 == [] or result_value0 == []:
                return Bit_Compare.single_bit_pass_fail(result_value0,result_value1,'same','different')
        return 'fail'
    
    def val_rw1l(numbit,val_stage,compare_value):
        pass_fail = Algorithm.val_rwl(numbit,val_stage,compare_value)
        return pass_fail
    
    def val_rw1s(numbit,val_stage,compare_value):
        pass_fail = Algorithm.val_rws(numbit,val_stage,compare_value)
        return pass_fail
    
    def val_rwc(numbit,val_stage,compare_value):
        pass_fail = Algorithm.val_rw1c(numbit,val_stage,compare_value)
        return pass_fail
    
    def val_rsv(numbit,compare_value):
        wr = compare_value[0]
        rd = compare_value[1]
        pre_rd = compare_value[2]
        if rd == pre_rd:
            return 'pass'
        return 'fail'

class Bit_Compare:
    def single_bit_pass_fail(result_value0,result_value1,exp_val0,exp_val1):
        if exp_val0 == 'different':
            exp_val0 = 'same'
        elif exp_val0 == 'same':
            exp_val0 = 'different'
        if exp_val1 == 'different':
            exp_val1 = 'same'
        elif exp_val1 == 'same':
            exp_val1 = 'different'
        if exp_val0 not in ['different','same'] or exp_val1 not in ['different','same']:
            if result_value0 == []:
                if result_value1 in exp_val1:
                    return 'pass'
            elif result_value1 == []:
                if result_value0 in exp_val0:
                    return 'pass'
        else:
            if result_value0 == []:
                if exp_val1 not in result_value1:
                    return 'pass'
            elif result_value1 == []:
                if exp_val0 not in result_value0:
                    return 'pass'
        return 'fail'
    
    def compare_bit2bit_with_prerd(pre_rd,wr,rd,expect_value):
        i = 0
        result_value0 = result_value1 = ''
        for bit_wr in wr:
            if bit_wr == '0':
                if expect_value == 'pre' and pre_rd[i] == rd[i]:
                    result = 'pre'
                elif expect_value == 'pre' and pre_rd[i] != rd[i]:
                    result = 'not_pre'
                    break
                if expect_value == '0' and rd[i] == '0':
                    result = '0'
                elif expect_value == '0' and rd[i] != '0':
                    result = 'not_0'
                    break
            else:
                result = 'no_zero'
            i+=1
        return result
        
    def compare_bit2bit(value1,value2):#in binary
        i=0
        result_value1 = []
        result_value0 = []
        for bit_value in value1:
            if bit_value == '1' and bit_value == value2[i]:
                result_value1.append('same')
            elif bit_value == '1' and bit_value != value2[i]:
                result_value1.append('different')
            elif bit_value == '0' and bit_value == value2[i]:
                result_value0.append('same')
            elif bit_value == '0' and bit_value != value2[i]:
                result_value0.append('different')
            i+=1
        return result_value1,result_value0
        
def read(full_field_name):
    rd = str(eval(full_field_name))
    return rd

def write(full_field_name,write_value):
    eval(full_field_name+'.write('+write_value+')')

def compare(attr,full_field_name,wr,rd,pre_rd,numbit,val_stage):
    undefined_attrs = ['ro/c/v','ro/p','ro/v','rw/0c/v','rw/l/k','rw/p','rw/s/l','rw/v','rw/v2']
    undefined_rw_behav_attrs = ['rw/v/p','rw/v/l','rw/v/p/l']
    undefined_ro_behav_attrs = ['ro/v/p','rw/1c/p','rw/1c/v','rw/1c/v/p','rw/1s/v','rw/1s/v/l','rw/ac','rw/o/p','rw/o/v/l','rw/p/l','rw/fuse','rw/strap','dc']
    if attr in ['roswc','rw/cr'] or attr in undefined_attrs or attr in undefined_rw_behav_attrs or attr in undefined_ro_behav_attrs:
        compare_value = [wr,rd[0],rd[1],pre_rd[0],pre_rd[1]]
    elif attr in ['ro/c','wo/1','wo/c','na','rw0c_fw','rw1c_fw','double buffered','r/w hardware clear','read/32 bit write only','r/w firmware only']:
        compare_value = [wr,rd[0],pre_rd[0],pre_rd[1]]
    else:
        compare_value = [wr,rd,pre_rd[1]]
    if attr == 'ro':
        pass_fail = Algorithm.val_ro(numbit,compare_value)
    elif attr == 'wo':
        pass_fail = Algorithm.val_wo(numbit,compare_value)
    elif attr == 'rw':
        pass_fail = Algorithm.val_rw(numbit,compare_value)
    elif attr == 'rw/s':
        pass_fail = Algorithm.val_rws(numbit,val_stage,compare_value)
    elif attr == 'rw/l':
        pass_fail = Algorithm.val_rwl(numbit,val_stage,compare_value)
    elif attr == 'rw/o':
        pass_fail = Algorithm.val_rwo(numbit,val_stage,compare_value)
    elif attr == 'rw/1c':
        pass_fail = Algorithm.val_rw1c(numbit,val_stage,compare_value)
    elif attr == 'rw/1l':
        pass_fail = Algorithm.val_rw1l(numbit,val_stage,compare_value)
    elif attr == 'rw/1s':
        pass_fail = Algorithm.val_rw1s(numbit,val_stage,compare_value)
    elif attr == 'rw/c':
        pass_fail = Algorithm.val_rwc(numbit,val_stage,compare_value)
    elif attr == 'ro/swc':
        pass_fail = Algorithm.val_roswc(numbit,val_stage,compare_value)
    elif attr == 'rsv':
        pass_fail = Algorithm.val_rsv(numbit,compare_value)
    elif attr == 'ro/c':
        pass_fail = Algorithm.val_roc(numbit,val_stage,compare_value)
    elif attr == 'rw/cr':
        pass_fail = Algorithm.val_rwcr(numbit,val_stage,compare_value)
    elif attr == 'wo/1':
        pass_fail = Algorithm.val_wo1(numbit,val_stage,compare_value)
    elif attr == 'wo/c':
        pass_fail = Algorithm.val_woc(numbit,val_stage,compare_value)
    elif attr == 'na':
        pass_fail = Algorithm.val_na(numbit,val_stage,compare_value)
    elif attr == 'rw0c_fw':
        pass_fail = Algorithm.val_rw0cfw(numbit,val_stage,compare_value)
    elif attr == 'rw1c_fw':
        pass_fail = Algorithm.val_rw1cfw(numbit,val_stage,compare_value)
    elif attr == 'double buffered':
        pass_fail = Algorithm.val_db(numbit,val_stage,compare_value)
    elif attr == 'r/w hardware clear':
        pass_fail = Algorithm.val_rwhwc(numbit,val_stage,compare_value)
    elif attr == 'read/32 bit write only':
        pass_fail = Algorithm.val_r32wonly(numbit,val_stage,compare_value)
    elif attr == 'r/w firmware only':
        pass_fail = Algorithm.val_rwfwo(numbit,val_stage,compare_value)
    elif attr in undefined_ro_behav_attrs:
        pass_fail = Algorithm.val_ro(numbit,compare_value)
    elif attr in undefined_rw_behav_attrs:
        pass_fail = Algorithm.val_rw(numbit,compare_value)
    elif attr in undefined_attrs:
        pass_fail = 'NA'
    return pass_fail

def create_value_10_01(numbit,value):#value = '10'/'01'
    '''Method1: 
    1bit: 1/0
    2bit: 10/01
    odd_bit: multiply by the number of value-1
    even_bit: multiply by the number of value'''
    if numbit == 1:
        created_value = value[0]
    elif numbit == 2:
        created_value = value
    elif (numbit%2) == 0:
        created_value = value * (round(numbit/2))
    elif (numbit%2) == 1:
        created_value = (value * round((round((numbit - 1)) / 2))) + value[0]
    return created_value
    
def create_value(numbit, value):#value = 'A5'/'5A'
    '''Method2:'''
    stage = '5' if value == 'A5' else 'A' if value == '5A' else None
    created_value = ''
    numbit_remain = numbit
    if numbit > 4:
        while numbit_remain >= 4:
            add = '1010' if stage == 'A' else '0101' if stage == '5' else None
            created_value = add + created_value
            stage = 'A' if stage == '5' else '5'
            numbit_remain -= 4
        add = '1010' if stage == 'A' else '0101'
        created_value = add[-numbit_remain:]+created_value if numbit_remain != 0 else created_value
    else:
        add = '1010' if stage == 'A' else '0101'
        created_value = add[-numbit:]
    return created_value
    
    
class Val_stage:
    def pre_read(full_field_name):#It is mainly for attr = ro/swc
        pre_rd1 = str(eval(full_field_name))
        pre_rd2 = str(eval(full_field_name))
        pre_rd = [pre_rd1,pre_rd2]
        attr = eval(full_field_name+'.info["attribute"]')
        numbit = track.track_field_bits(full_field_name)
        if attr == 'ro/swc':
            pass_fail = Algorithm.val_roswc(numbit,'pre_rd',pre_rd)
            return pre_rd,pass_fail
        elif attr == 'ro/c':
            pass_fail = Algorithm.val_ros(numbit,'pre_rd',pre_rd)
            return pre_rd,pass_fail
        if attr == 'na':
            pass_fail = Algorithm.val_na(numbit,'pre_rd',pre_rd)
            return pre_rd,pass_fail
        return pre_rd,'pass'

    def first_stage_val(full_field_name,pre_rd,wr_in_list,rd_in_list,val_stage,wr_value):
        new_defined_attrs = ['ro/c','rw/cr','wo/1','wo/c','na','rw0c_fw','rw1c_fw','double buffered','r/w hardware clear','read/32 bit write only','r/w firmware only']
        numbit = track.track_field_bits(full_field_name)
        #identify attr of this field in universal attr name.
        attr = eval(full_field_name+'.info["attribute"]')
        attr = track.Pre_test.track_attr_cat(attr)
        if len(attr) == 0:
            attr = eval(full_field_name+'.info["attribute"]')
        else:
            attr = attr[0]
        #write 'A5'/'5A' to field with and without algorithm.
        if attr == 'ro/c' and val_stage in ['2nd_stage_rdwr','3rd_stage_rdwr']:
            wr = rd = 'NA'
        if attr in ['rw','rw/s','rw/l','rw/1c','rw/1l','rw/1s','rw/c','ro/swc','ro','wo','rsv','rw/o'] or attr in all_undefined_attrs or attr in new_defined_attrs:
            wr = create_value(numbit,wr_value)
            wr = Conv.convert_bin_to_dec(wr)
            write(full_field_name,wr)
            wr = Conv.convert_dec_to_hex(wr)#for table display purposes
        #No write, show 'NA' to field without algorithm.
        else:
            wr='NA'
        #read and compare to get result(pass/fail) for field with algorithm.
        if wr != 'NA':
            if attr in ['ro/v','rw/v']:
                time.sleep(10)
            rd = read(full_field_name)
            if attr in ['roswc','rw/cr'] or attr in all_undefined_attrs:#double read
                rd2 =read(full_field_name)
                two_read_value = [rd,rd2]
                pass_fail = compare(attr,full_field_name,wr,two_read_value,pre_rd,numbit,val_stage)
            else:
                pass_fail = compare(attr,full_field_name,wr,rd,pre_rd,numbit,val_stage)
        #no read, everything show 'NA' for field without algorithm.
        else:
            pass_fail = 'NA'
            rd = 'NA'
        #store write and read value in the 
        wr_in_list.append(wr)
        if attr in ['roswc','rw/cr'] or attr in all_undefined_attrs:
            rd_in_list.append(two_read_value[0])
            rd_in_list.append(two_read_value[1])
        else:
            rd_in_list.append(rd)
        if target.readPostcode() != 0x10AD:#only for UEFI.
            pass_fail = 'sys_rst'
        return wr_in_list,rd_in_list,pass_fail

    def second_stage_val(full_field_name,pre_rd,wr_in_list,rd_in_list,val_stage,wr_value):
        (wr_in_list,rd_in_list,pass_fail_1st_val) = Val_stage.first_stage_val(full_field_name,pre_rd,wr_in_list,rd_in_list,val_stage,wr_value)
        return wr_in_list,rd_in_list,pass_fail_1st_val

    def third_stage_val(full_field_name,pre_rd,wr_in_list,rd_in_list,val_stage,wr_value):
        (wr_in_list,rd_in_list,pass_fail_1st_val) = Val_stage.first_stage_val(full_field_name,pre_rd,wr_in_list,rd_in_list,val_stage,wr_value)
        return wr_in_list,rd_in_list,pass_fail_1st_val

def validate_1by1(full_field_name):#only on one chosen attr or all attrs.
    wr_in_list = []
    rd_in_list = []
    fail_reason = []
    (pre_rd,pass_fail_pre_rd) = Val_stage.pre_read(full_field_name)
    (wr_in_list,rd_in_list,pass_fail_1st_val) = Val_stage.first_stage_val(full_field_name,pre_rd,wr_in_list,rd_in_list,'1st_stage_rdwr','A5')
    (wr_in_list,rd_in_list,pass_fail_2nd_val) = Val_stage.second_stage_val(full_field_name,pre_rd,wr_in_list,rd_in_list,'2nd_stage_rdwr','5A')
    (wr_in_list,rd_in_list,pass_fail_3rd_val) = Val_stage.third_stage_val(full_field_name,pre_rd,wr_in_list,rd_in_list,'3rd_stage_rdwr','A5')
    if 'fail' in [pass_fail_pre_rd,pass_fail_1st_val,pass_fail_2nd_val,pass_fail_3rd_val]:
        pass_fail = 'fail'
        fail_reason = track.track_fail_reason(pass_fail_pre_rd,pass_fail_1st_val,pass_fail_2nd_val,pass_fail_3rd_val)
    elif 'NA' in [pass_fail_pre_rd,pass_fail_1st_val,pass_fail_2nd_val,pass_fail_3rd_val]:#for the fields with the non-prepared attr and ro/c.
        if 'pass' in [pass_fail_pre_rd,pass_fail_1st_val,pass_fail_2nd_val,pass_fail_3rd_val]:#for ro/c and ro/v
            pass_fail = 'pass'
        else:
            pass_fail = 'NA'
    else:
        pass_fail = 'pass'
    if itp.isrunning() == False:#If system has soft hang or cat error.
        itp.go()
        time.sleep(3)
        fail_reason.append('halt')
    if 'sys_rst' in [pass_fail_1st_val,pass_fail_2nd_val,pass_fail_3rd_val]:
        fail_reason.append('sys_rst')
        pass_fail = 'fail'
    return pre_rd,wr_in_list,rd_in_list,pass_fail,fail_reason
    
def hang_validate_1by1(full_field_name, confirm_hang_regs, hang_stages):
    wr_in_list = []
    rd_in_list = []
    fail_reason = []
    hang_state = [0,0,0,0]
    (pre_rd,pass_fail_pre_rd) = Val_stage.pre_read(full_field_name)
    hang_state = machine_check(hang_state, 0)
    (wr_in_list,rd_in_list,pass_fail_1st_val) = Val_stage.first_stage_val(full_field_name,pre_rd,wr_in_list,rd_in_list,'1st_stage_rdwr','A5')
    hang_state = machine_check(hang_state, 1)
    (wr_in_list,rd_in_list,pass_fail_2nd_val) = Val_stage.second_stage_val(full_field_name,pre_rd,wr_in_list,rd_in_list,'2nd_stage_rdwr','5A')
    hang_state = machine_check(hang_state, 2)
    (wr_in_list,rd_in_list,pass_fail_3rd_val) = Val_stage.third_stage_val(full_field_name,pre_rd,wr_in_list,rd_in_list,'3rd_stage_rdwr','A5')
    hang_state = machine_check(hang_state, 3)
    if 1 in hang_state:
        confirm_hang_regs.append(full_field_name)
        hang_stages.append(hang_state)
    return confirm_hang_regs, hang_stages

def validate(valid_fields,chosen_attr,dumpchoice,auto):
    num=1
    Pass=0
    Fail=0
    Unknown=0
    Error = 0
    num2print=0
    rowdictlist=[]
    fail_rowdl=[]
    x=[]
    fail_x=[]
    elg = ''
    elg = dump.export_error('open','NA',elg)
    alg = ''
    flg = ''
    error_info = {}
    fail_fields_name = []
    if dumpchoice == 0:
        (alg,flg) = dump.export('open','NA',alg,flg)
    #Exclude all the fields with non-chosen attr.
    chosen_attr_fields = track.track_chosen_attr_fields(valid_fields,chosen_attr)
    #validation.
    num_chosen_attr_fields = len(chosen_attr_fields)
    reserved_print_num=len(chosen_attr_fields)
    for full_field_name in chosen_attr_fields:
        #to ask user for the num of table display.
        if num2print == 0:                                                                                                              
            (num2print,reserved_print_num) = user.Exec.print_limit(num_chosen_attr_fields,reserved_print_num,auto)
            if num2print == 'end':
                break
            num_chosen_attr_fields-=num2print
            initial_time = time.time()
            reserved_num = 0
        reserved_num += 1
        time_taken = time.time() - initial_time
        (s,m,h) = disp.time(round(time_taken))
        disp.progress(reserved_num, reserved_print_num, prefix=f'Progress [{reserved_num}:{reserved_print_num}]:', infix1 = f'Time_Taken= {h}h{m}m{s}s', suffix=f'Reg: [{full_field_name}]')
        #validate
        try:
            (pre_rd,wr_in_list,rd_in_list,pass_fail,fail_reason) = validate_1by1(full_field_name)
        except:
            message = sys.exc_info()[1]
            fail_reason = str(message)
            if len(fail_reason) >= 30:
                fail_reason = fail_reason[:35-len(fail_reason)]+'...'
            fail_reason = [fail_reason]
            error_info[full_field_name]=str(message)
            pass_fail = 'error'
            pre_rd = wr_in_list = rd_in_list = []
            elg = dump.export_error('store',full_field_name,elg)
        #display and storing validation info in table form.
        attr = eval(full_field_name+'.info["attribute"]')
        (rowdictlist,x) = disp.store_content(rowdictlist,x,num,full_field_name,attr,pass_fail,pre_rd,wr_in_list,rd_in_list,fail_reason)
        (Pass,Fail,Unknown,Error) = track.track_num_pass_fail(pass_fail,Pass,Fail,Unknown,Error)
        #store fail fields validation info.
        if pass_fail == 'fail':
            (fail_rowdl,fail_x) = disp.store_fail_content(fail_rowdl,fail_x,num,full_field_name,attr,pass_fail,pre_rd,wr_in_list,rd_in_list,fail_reason)
            fail_fields_name.append(full_field_name)
        #print the table when reach number user want to print.
        num2print -= 1
        if int(repr(num2print)[-1]) == 0:
            print('')
            disp.disp_content(rowdictlist,x,dumpchoice,alg,flg)
            disp.disp_total_pass_fail(Pass,Fail,Unknown,Error)
            rowdictlist=[]
            x=[]
            machine_chk_error = debug.mca.analyze()
            if machine_chk_error != []:
                fail_reason.append('hang')
        num+=1
        if 'hang' in fail_reason:
            print('Validation will be stopped due to the present of machine check error')
            if dumpchoice == 0:
                (alg,flg) = dump.export('store','Validation will be stopped due to the present of machine check error',alg,flg)
                (alg,flg) = dump.export('store',str(machine_chk_error),alg,flg)
                (alg,flg) = dump.export('store_fail','Validation will be stopped due to the present of machine check error',alg,flg)
                (alg,flg) = dump.export('store_fail',str(machine_chk_error),alg,flg)
            break
    elg = dump.export_invalid('close','NA',elg)
    #second validation for hang regs if available
    hang_chk_choice = user.Post_test.disp_hang_choice(fail_reason,auto)
    if hang_chk_choice in ['yes','y']:
        sus_hang_regs = chosen_attr_fields[chosen_attr_fields.index(full_field_name)-9:chosen_attr_fields.index(full_field_name)+1]
        (alg, flg) = validate2_hang_regs(sus_hang_regs, alg, flg, dumpchoice)
    #display all or specific error registers.
    user.Post_test.disp_error_choice(Error,error_info,auto)
    if dumpchoice == 0 and Fail == 0:
        (alg,flg) = dump.export('close_all','NA',alg,flg)
        (alg,flg) = dump.export('close_fail','NA',alg,flg)
    return fail_x,Fail,alg,flg,fail_fields_name

def machine_check(hang_state, index):
    machine_chk_error = debug.mca.analyze()
    if machine_chk_error != []:
        hang_state[index] = 1
        target.powerCycle(waitOff=1,waitAfter=1)
        while True:
            if target.readPostcode() == 0x10AD:
                itp.unlock()
                break
    return hang_state

def validate2_hang_regs(sus_hang_regs, alg, flg, dumpchoice):
    confirm_hang_regs = []
    hang_stages = []
    hang_stage_reason = ['Pre-read','1st read-write','2nd read-write','3rd read-write']
    target.powerCycle(waitOff=1,waitAfter=1)
    while True:
        if target.readPostcode() == 0x10AD:
            itp.unlock()
            break
    for reg in sus_hang_regs:
        (confirm_hang_regs, hang_stages) = hang_validate_1by1(reg, confirm_hang_regs, hang_stages)
    final_hang_stages = []
    for hang_stage in hang_stages:
        temp = []
        for n in range(4):
            if hang_stage[n] == 1:
                temp.append(hang_stage_reason[n])
        final_hang_stages.append(temp)
    (alg, flg) = disp.disp_hang_regs(confirm_hang_regs, final_hang_stages, dumpchoice, alg, flg)
    target.powerCycle(waitOff=1,waitAfter=1)
    while True:
        if target.readPostcode() == 0x10AD:
            unlock()
            return alg, flg

def validate2_fail_regs(fail_fields_name,alg,flg,dumpchoice,Fail,auto):
    num2print=0
    num_chosen_attr_fields = len(fail_fields_name)
    reserved_print_num = num_chosen_attr_fields
    fail_rowdl = []
    fail_x = []
    Pass2 = 0
    Fail2 = 0
    Unknown2 = 0
    Error2 = 0
    num=1
    #2nd validation.
    reserved_print_num = len(fail_fields_name)
    for fail_field_name in fail_fields_name:
        #to ask user for the num of table display.
        if num2print == 0:                                                                                                              #to ask user for the num of table display.
            (num2print,reserved_print_num) = user.Exec.print_limit(num_chosen_attr_fields,reserved_print_num,auto)
            if num2print == 'end':
                return alg,flg
            num_chosen_attr_fields-=num2print
            initial_time = time.time()
            reserved_num = 0
        time_taken = time.time() - initial_time
        (s,m,h) = disp.time(round(time_taken))
        reserved_num += 1
        disp.progress(reserved_num, reserved_print_num, prefix=f'Progress [{reserved_num}:{reserved_print_num}]:', infix1 = f'Time_Taken= {h}h{m}m{s}s', suffix=f'Reg: [{fail_field_name}]')
        #validate
        (pre_rd,wr_in_list,rd_in_list,pass_fail,fail_reason) = validate_1by1(fail_field_name)
        attr = eval(fail_field_name+'.info["attribute"]')
        (fail_rowdl,fail_x) = disp.store_fail_content(fail_rowdl,fail_x,num,fail_field_name,attr,pass_fail,pre_rd,wr_in_list,rd_in_list,fail_reason)
        (Pass2,Fail2,Unknown2,Error2) = track.track_num_pass_fail(pass_fail,Pass2,Fail2,Unknown2,Error2)
        if 'hang' in fail_reason:
            num2print = 0
        num2print -= 1
        if int(repr(num2print)[-1]) == 0:
            disp.disp_fail_content(fail_x,dumpchoice,alg,flg)
            print(f'{Fail} fail(s) in 1st validation.')
            disp.disp_total_pass_fail(Pass2,Fail2,Unknown2,Error2)
            fail_rowdl=[]
            fail_x=[]
        num+=1
        if 'hang' in fail_reason:
            machine_chk_error = debug.mca.analyze()
            if machine_chk_error == []:
                hang_reason = 'System is not running!'
                print(hang_reason)
            else:
                hang_reason = 'Validation will be stopped due to the present of machine check error'
                print(hang_reason)
            if dumpchoice == 0:
                (alg,flg) = dump.export('store',hang_reason,alg,flg)
                (alg,flg) = dump.export('store',str(machine_chk_error),alg,flg)
                (alg,flg) = dump.export('store_fail',hang_reason,alg,flg)
                (alg,flg) = dump.export('store_fail',str(machine_chk_error),alg,flg)
            break
    #shows num of passed fields.
    if Fail2 == Fail:
        print('In second validation, no pass sub-register.')
    else:
        print(f"In second validation, there's {Pass2} pass registers.")
    return alg,flg
        