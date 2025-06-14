import __main__
cdie = __main__.cdie if hasattr(__main__, 'cdie') else None
soc = __main__.soc if hasattr(__main__, 'soc') else None
cpu = __main__.pch if hasattr(__main__, 'cpu') else None
pch = __main__.pch if hasattr(__main__, 'pch') else None
itp = __main__.itp if hasattr(__main__, 'itp') else None
ioe = __main__.ioe if hasattr(__main__, 'ioe') else None
gcd = __main__.gcd if hasattr(__main__, 'gcd') else None
hub = __main__.hub if hasattr(__main__, 'hub') else None
pcd = __main__.pcd if hasattr(__main__, 'pcd') else None
refresh = __main__.refresh if hasattr(__main__, 'refresh') else None
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
try:
    import pysvtools.fv_common.target as target
except:
    print("target script is failed to import")
import debug
#try:
#    from arrowlake import debug
#except:
#    try:
#        from meteorlake import debug
#    finally:
#        from pantherlake import debug
import random as dice

all_undefined_attrs = ['dc','rw/ac','rw/l/k','rw/s/l','rw/fuse','rw/strap']
partial_defined_attrs = ['ro/c/v','ro/p','ro/v','ro/v/p','rw/1c/p','rw/1c/v','rw/1c/v/p','rw/0c/v','rw/1s/v/p','rw/1s/v','rw/1s/v/l','rw/o/p','rw/o/v/l','rw/p','rw/p/l','rw/v','rw/v/p','rw/v/l','rw/v/p/l','rw/v2','ro/c','rw/cr','wo/1','wo/c','na','rw0c_fw','rw1c_fw','double buffered','r/w hardware clear','read/32 bit write only','r/w firmware only']

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
        if val_stage == 'pre_rd' and len(compare_value) == 2:
            pre_rd1 = compare_value[0]
            pre_rd2 = compare_value[1]
            if pre_rd2 in ['0x0','0'] and pre_rd1 in ['0x0','0']:
                return 'pass'
            else:
                return 'fail'
        elif val_stage == 'pre_rd' and len(compare_value) == 1:
            pre_rd = compare_value[0]
            if pre_rd in ['0x0','0']:
                return 'pass'
            else:
                return 'fail'
        elif val_stage == '1st_stage_rdwr':
            wr = compare_value[0]
            rd1 = compare_value[1]
            #rd2 = compare_value[2]
            pre_rd1 = compare_value[2]
            #pre_rd2 = compare_value[3]
            if rd1 in ['0x0','0']:
                return 'pass'
            else:
                return 'fail'
        elif val_stage in ['2nd_stage_rdwr','3rd_stage_rdwr']:
            wr = compare_value[0]
            rd1 = compare_value[1]
            #rd2 = compare_value[2]
            pre_rd1 = compare_value[2]
            #pre_rd2 = compare_value[3]
            if rd1 in ['0x0','0']:
                return 'pass'
            else:
                return 'fail'

    def val_rwv2(numbit,val_stage,compare_value):
        return 'NA'

    def val_rwcr(numbit,val_stage,compare_value):
        wr = compare_value[0]
        rd1 = compare_value[1]
        rd2 = compare_value[2]
        pre_rd1 = compare_value[3]
        #pre_rd2 = compare_value[4]
        if rd1 == wr and rd2 == '0':
            return 'pass'
        else:
            return 'fail'

    def val_wo1(numbit,val_stage,compare_value):
        wr = compare_value[0]
        rd1 = compare_value[1]
        pre_rd1 = compare_value[2]
        #pre_rd2 = compare_value[3]
        if rd1 == '0':
            return 'pass'
        else:
            return 'fail'
    
    def val_woc(numbit,val_stage,compare_value):
        pass_fail = Algorithm.val_wo1(numbit,val_stage,compare_value)
        return pass_fail

    def val_na(numbit,val_stage,compare_value):
        if val_stage == 'pre_rd' and len(compare_value) == 2:
            pre_rd1 = compare_value[0]
            pre_rd2 = compare_value[1]
            if pre_rd1 == '0' and pre_rd2 == '0':
                return 'pass'
            else:
                return 'fail'
        elif val_stage == 'pre_rd' and len(compare_value) == 1:
            pre_rd = compare_value[0]
            if pre_rd == '0':
                return 'pass'
            else:
                return 'fail'
        wr = compare_value[0]
        rd1 = compare_value[1]
        pre_rd1 = compare_value[2]
        #pre_rd2 = compare_value[3]
        if rd1 == '0':
            return 'pass'
        else:
            return 'fail'

    def val_rw0cfw(numbit,val_stage,compare_value):
        wr = compare_value[0]
        rd1 = compare_value[1]
        pre_rd1 = compare_value[2]
        #pre_rd2 = compare_value[3]
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
        if len(compare_value) == 1 and val_stage == 'pre_rd':
            if compare_value[0] == '0x0':
                return 'pass'
            else:
                return 'fail'
        elif len(compare_value) == 2 and val_stage == 'pre_rd':
            wr=compare_value[0]
            rd1=compare_value[1]
            if wr == '0x0' and rd1 == all_one_value:
                return 'pass'
            else:
                return 'fail'
        elif val_stage in['1st_stage_rdwr','2nd_stage_rdwr','3rd_stage_rdwr']:
            wr=compare_value[0]
            rd1=compare_value[1]
            rd2 = compare_value[2]
            if wr == rd1 and rd1 == rd2:
                return 'pass'
            return 'fail'

    def val_ro(numbit,val_stage,compare_value):
        wr = compare_value[0]
        rd = compare_value[1]
        pre_rd = compare_value[2]
        if rd == pre_rd:
            return 'pass'
        else:
            return 'fail'
    
    def val_wo(numbit,val_stage,compare_value):
        return Algorithm.val_ro(numbit,val_stage,compare_value)
    
    def val_rw(numbit,val_stage,compare_value):
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
            num_bit_dif = len(wr_in_bin) - len(rd_in_bin)
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
            num_bit_dif = len(wr_in_bin) - len(rd_in_bin)
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
        
    def val_rwop(numbit,val_stage,compare_value,rd_in_list):
        wr = compare_value[0]
        rd = compare_value[1]
        pre_rd = compare_value[2]
        wr_in_bin = Conv.convert_hex_to_bin(wr)
        rd_in_bin = Conv.convert_hex_to_bin(rd)
        pre_rd_in_bin = Conv.convert_hex_to_bin(pre_rd)
        if len(wr_in_bin) > len(rd_in_bin):
            num_bit_dif = len(wr_in_bin) - len(rd_in_bin)
            rd_in_bin = ('0' * num_bit_dif) + rd_in_bin
            num_bit_dif = len(wr_in_bin) - len(pre_rd_in_bin)
            pre_rd_in_bin = ('0' * num_bit_dif) + pre_rd_in_bin
        elif len(wr_in_bin) < len(rd_in_bin):
            num_bit_dif = len(rd_in_bin) - len(wr_in_bin)
            wr_in_bin = ('0' * num_bit_dif) + wr_in_bin
            num_bit_dif = len(rd_in_bin) - len(pre_rd_in_bin)
            pre_rd_in_bin = ('0' * num_bit_dif) + pre_rd_in_bin
        if val_stage in ['1st_stage_rdwr','3rd_stage_rdwr']:
            (result_value1,result_value0) = Bit_Compare.compare_bit2bit(wr_in_bin,rd_in_bin)
            if result_value0 in (['same'],[]) and result_value1 in (['same'],[]):
                return 'pass'
            elif result_value0 in (['different'],[]) or result_value1 in (['different'],[],['same','different']):
                if rd_in_bin == pre_rd_in_bin:
                    return 'pass'
                else:
                    return 'fail'
            elif len(set(result_value1)) == 2 or len(set(result_value0)) == 2:
                if rd_in_bin == pre_rd_in_bin:
                    return 'pass'
                else:
                    return 'fail'
            elif result_value1 == [] or result_value0 == []:
                return Bit_Compare.single_bit_pass_fail(result_value0,result_value1,'same','same')
        elif val_stage == '2nd_stage_rdwr':
            first_rd_in_bin = Conv.convert_hex_to_bin(rd_in_list[0])
            (result_value1,result_value0) = Bit_Compare.compare_bit2bit(first_rd_in_bin,rd_in_bin)
            if result_value0 in (['same'],[]) and result_value1 in (['same'],[]):
                return 'pass'
            elif result_value1 == [] or result_value0 == []:
                return Bit_Compare.single_bit_pass_fail(result_value0,result_value1,'different','different')
        return 'fail'

    def val_rw0cv(numbit,val_stage,compare_value):
        wr = compare_value[0]
        rd = compare_value[1]
        pre_rd = compare_value[2]
        wr_in_bin = Conv.convert_hex_to_bin(wr)
        rd_in_bin = Conv.convert_hex_to_bin(rd)
        pre_rd_in_bin = Conv.convert_hex_to_bin(pre_rd)
        if len(wr_in_bin) > len(rd_in_bin):
            num_bit_dif = len(wr_in_bin) - len(rd_in_bin)
            rd_in_bin = ('0' * num_bit_dif) + rd_in_bin
        elif len(wr_in_bin) < len(rd_in_bin):
            num_bit_dif = len(rd_in_bin) - len(wr_in_bin)
            wr_in_bin = ('0' * num_bit_dif) + wr_in_bin
        if val_stage == '1st_stage_rdwr':
            (result_value1,result_value0) = Bit_Compare.compare_bit2bit(wr_in_bin,rd_in_bin)
            (result_value1) = Bit_Compare.compare_bit2bit_with_prerd_and_val1(pre_rd_in_bin,wr_in_bin,rd_in_bin,'pre')
            if result_value1 == 'pre' and result_value0 in [[],['same']]:
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

    def val_rw1c(numbit,val_stage,compare_value):
        wr = compare_value[0]
        rd = compare_value[1]
        pre_rd = compare_value[2]
        wr_in_bin = Conv.convert_hex_to_bin(wr)
        rd_in_bin = Conv.convert_hex_to_bin(rd)
        pre_rd_in_bin = Conv.convert_hex_to_bin(pre_rd)
        if len(wr_in_bin) > len(rd_in_bin):
            num_bit_dif = len(wr_in_bin) - len(rd_in_bin)
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
        pass_fail = Algorithm.val_rws(numbit,val_stage,compare_value)
        return pass_fail
    
    def val_rw1s(numbit,val_stage,compare_value):
        pass_fail = Algorithm.val_rws(numbit,val_stage,compare_value)
        return pass_fail
    
    def val_rwc(numbit,val_stage,compare_value):
        pass_fail = Algorithm.val_rw1c(numbit,val_stage,compare_value)
        return pass_fail
    
    def val_rsv(numbit,val_stage,compare_value):
        wr = compare_value[0]
        rd = compare_value[1]
        pre_rd = compare_value[2]
        if rd == pre_rd:
            return 'pass'
        return 'fail'

    def val_dunno(numbit,val_stage,compare_value):
        return 'NA'
    
    
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
    def compare_bit2bit_with_prerd_and_val1(pre_rd,wr,rd,expect_value):
        i = 0
        result_value0 = result_value1 = ''
        if pre_rd == '0':
            pre_rd = '0' * len(wr)
        elif pre_rd != '0' and len(pre_rd) < len(wr):
            pre_rd = ('0' * (len(wr)-len(pre_rd))) + pre_rd
        for bit_wr in wr:
            if bit_wr == '1':
                if expect_value == 'pre' and pre_rd[i] == rd[i]:
                    result = 'pre'
                elif expect_value == 'pre' and pre_rd[i] != rd[i]:
                    result = 'not_pre'
                    break
            else:
                result = 'no_one'
            i+=1
        return result
 
    def compare_bit2bit_with_prerd(pre_rd,wr,rd,expect_value):
        i = 0
        result_value0 = result_value1 = ''
        if pre_rd == '0':
            pre_rd = '0' * len(wr)
        elif pre_rd != '0' and len(pre_rd) < len(wr):
            pre_rd = ('0' * (len(wr)-len(pre_rd))) + pre_rd
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
        result_value1,result_value0 = Bit_Compare.clean_compare_results(result_value1,result_value0)
        return result_value1,result_value0
        
    def clean_compare_results(result_value1,result_value0):
        if result_value1 == []:
            pass
        elif all(element == result_value1[0] for element in result_value1):
            result_value1 = [result_value1[0]]
        elif len(set(result_value1)) == 2:
            result_value1 = ['different','same']
        if result_value0 == []:
            pass
        elif all(element == result_value0[0] for element in result_value0):
            result_value0 = [result_value0[0]]
        elif len(set(result_value0)) == 2:
            result_value0 = ['different','same']
        return result_value1,result_value0
        
def read(full_field_name):
    rd = str(eval(full_field_name))
    return rd

def write(full_field_name,write_value):
    eval(full_field_name+'.write('+write_value+')')

def arr_compare_value(attr,wr,rd,pre_rd):
    undefined_attrs = ['rw/l/k','rw/s/l']
    undefined_ro_behav_attrs = ['rw/ac','rw/fuse','rw/strap','dc']
    if attr in ['roswc','rw/cr'] or attr in undefined_attrs or attr in undefined_ro_behav_attrs:
        if len(pre_rd) == 2:
            return [wr,rd[0],rd[1],pre_rd[0],pre_rd[1]]
        elif len(pre_rd) == 1:
            return [wr,rd[0],rd[1],pre_rd[0]]
    elif attr in ['ro/c','wo/1','wo/c','na','rw0c_fw','rw1c_fw','double buffered','r/w hardware clear','read/32 bit write only','r/w firmware only','rw/0c/v','ro/c/v']:
        if len(pre_rd) == 2:
           return [wr,rd[0],pre_rd[0],pre_rd[1]]
        elif len(pre_rd) == 1:
           return [wr,rd[0],pre_rd[0]]
    else:
        if len(pre_rd) == 2:
            return [wr,rd,pre_rd[1]]
        elif len(pre_rd) == 1:
            return [wr,rd,pre_rd[0]]

compare = {
'ro':Algorithm.val_ro, 'ro/p':Algorithm.val_ro, 'ro/v':Algorithm.val_ro, 'ro/v/p':Algorithm.val_ro,
'wo':Algorithm.val_wo,
'rw':Algorithm.val_rw, 'rw/v':Algorithm.val_rw, 'rw/v/p':Algorithm.val_rw, 'rw/p':Algorithm.val_rw, 'rw/v2':Algorithm.val_rwv2, 
'rw/s':Algorithm.val_rws,
'rw/l':Algorithm.val_rw, 'rw/p/l':Algorithm.val_rw, 'rw/v/l':Algorithm.val_rw, 'rw/v/p/l':Algorithm.val_rw,
'rw/o':Algorithm.val_rwo, 'rw/o/p':Algorithm.val_rwop, 'rw/o/v/l':Algorithm.val_rwop,
'rw/1c':Algorithm.val_rw1c, 'rw/1c/p':Algorithm.val_rw1c, 'rw/1c/v':Algorithm.val_rw1c, 'rw/1c/v/p':Algorithm.val_rw1c, 
'rw/1l':Algorithm.val_rw1l, 
'rw/1s':Algorithm.val_rw1s, 'rw/1s/v/p':Algorithm.val_rw1s, 'rw/1s/v':Algorithm.val_rw1s, 'rw/1s/v/l':Algorithm.val_rw1s, 
'rw/c':Algorithm.val_rwc, 
'ro/swc':Algorithm.val_roswc, 
'rsv':Algorithm.val_rsv, 
'ro/c':Algorithm.val_roc, 
'rw/cr':Algorithm.val_rwcr, 
'wo/1':Algorithm.val_wo1, 
'wo/c':Algorithm.val_woc, 
'na':Algorithm.val_na, 
'rw0c_fw':Algorithm.val_rw0cfw,
'rw/0c/v':Algorithm.val_rw0cv, 
'rw1c_fw':Algorithm.val_rw1cfw, 
'double buffered':Algorithm.val_db, 
'r/w hardware clear':Algorithm.val_rwhwc, 
'read/32 bit write only':Algorithm.val_r32wonly, 
'r/w firmware only':Algorithm.val_rwfwo, 
'ro/c/v':Algorithm.val_roc, 
'rw/ac':Algorithm.val_ro,'rw/fuse':Algorithm.val_ro,'rw/strap':Algorithm.val_ro,'dc':Algorithm.val_ro,
'rw/l/k':Algorithm.val_dunno,'rw/s/l':Algorithm.val_dunno
}

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
    
def create_value(numbit, value):#value = 'A5'/'5A'/'FF'
    '''Method2:'''
    stage = '5' if value == 'A5' else 'A' if value == '5A' else 'F' if value == 'FF' else None
    created_value = ''
    numbit_remain = numbit
    if numbit > 4:
        while numbit_remain >= 4:
            add = '1010' if stage == 'A' else '0101' if stage == '5' else '1111' if stage == 'F' else None
            created_value = add + created_value
            stage = 'A' if stage == '5' else '5' if stage == 'A' else 'F'
            numbit_remain -= 4
        add = '1010' if stage == 'A' else '0101' if stage == '5' else '1111'
        created_value = add[-numbit_remain:]+created_value if numbit_remain != 0 else created_value
    else:
        add = '1010' if stage == 'A' else '0101' if stage == '5' else '1111'
        created_value = add[-numbit:]
    return created_value

class Val_stage:
    def pre_read(full_field_name,pre_rd_num,prefered_list):#It is mainly for attr = ro/swc
        [prefered_attr, prefered_reason] = prefered_list
        pre_rd1 = str(eval(full_field_name))
        if str(pre_rd_num) in ['2','2.0']:
            pre_rd2 = str(eval(full_field_name))
            pre_rd = [pre_rd1,pre_rd2]
        elif str(pre_rd_num) in ['1','1.0']:
            pre_rd = [pre_rd1]
        attr = eval(full_field_name+'.info["attribute"]')
        numbit = track.track_field_bits(full_field_name)
        if prefered_attr != None:
            pass
        else:
            if attr == 'ro/swc':
                pass_fail = Algorithm.val_roswc(numbit,'pre_rd',pre_rd)
                return pre_rd,pass_fail
            elif attr == 'ro/c':
                pass_fail = Algorithm.val_roc(numbit,'pre_rd',pre_rd)
                return pre_rd,pass_fail
            if attr == 'na':
                pass_fail = Algorithm.val_na(numbit,'pre_rd',pre_rd)
                return pre_rd,pass_fail
        if attr == 'rw/v2':
            return pre_rd, 'NA'
        else:
            return pre_rd,'pass'

    def first_stage_val(full_field_name,pre_rd,wr_in_list,rd_in_list,val_stage,wr_value,reset_detection,prefered_list):
        [prefered_attr, prefered_reason] = prefered_list
        numbit = track.track_field_bits(full_field_name)
        #identify attr of this field in universal attr name.
        if prefered_attr == None:
            attr = eval(full_field_name+'.info["attribute"]')
        else:
            attr = prefered_attr
        attr = track.Pre_test.track_attr_cat(attr)
        if len(attr) == 0:
            attr = eval(full_field_name+'.info["attribute"]')
        else:
            attr = attr[0]
        #write 'A5'/'5A' to field with and without algorithm.
        if attr == 'ro/c' and val_stage in ['2nd_stage_rdwr','3rd_stage_rdwr']:
            wr = rd = 'NA'
        if attr in ['rw','rw/s','rw/l','rw/1c','rw/1l','rw/1s','rw/c','ro/swc','ro','wo','rsv','rw/o'] or attr in all_undefined_attrs or attr in partial_defined_attrs:
            wr = create_value(numbit,wr_value)
            wr = Conv.convert_bin_to_dec(wr)
            write(full_field_name,wr)
            wr = Conv.convert_dec_to_hex(wr)#for table display purposes
        #No write, show 'NA' to field without algorithm.
        else:
            wr='NA'
        #read and compare to get result(pass/fail) for field with algorithm.
        if wr != 'NA':
            #//if attr in ['ro/v','rw/v']:
            #//    time.sleep(1)#regs of this attr needs time to update value...
            rd = read(full_field_name)
            if attr in ['roswc','rw/cr'] or attr in all_undefined_attrs:#double read
                rd2 =read(full_field_name)
                two_read_value = [rd,rd2]
                ##pass_fail = compare(attr,wr,two_read_value,pre_rd,numbit,val_stage)
                pass_fail = compare[attr](numbit,val_stage,arr_compare_value(attr,wr,two_read_value,pre_rd))
            elif attr in ["rw/o/p","rw/o/v/l"]:
                pass_fail = compare[attr](numbit,val_stage,arr_compare_value(attr,wr,rd,pre_rd),rd_in_list)
            else:
                ##pass_fail = compare(attr,wr,rd,pre_rd,numbit,val_stage)
                pass_fail = compare[attr](numbit,val_stage,arr_compare_value(attr,wr,rd,pre_rd))
        #no read, everything show 'NA' for field without algorithm.
        else:
            pass_fail = 'NA'
            rd = 'NA'
        #store write and read value in the 
        wr_in_list.append(wr)
        if attr in ['roswc','rw/cr'] or attr in all_undefined_attrs:#store double read
            rd_in_list.append(two_read_value[0])
            rd_in_list.append(two_read_value[1])
        else:
            rd_in_list.append(rd)
        if reset_detection:
            if target.readPostcode() != 0x10AD:#only for UEFI.
                pass_fail = 'sys_rst'
        return wr_in_list,rd_in_list,pass_fail

    def second_stage_val(full_field_name,pre_rd,wr_in_list,rd_in_list,val_stage,wr_value,reset_detection,prefered_list):
        (wr_in_list,rd_in_list,pass_fail_1st_val) = Val_stage.first_stage_val(full_field_name,pre_rd,wr_in_list,rd_in_list,val_stage,wr_value,reset_detection,prefered_list)
        return wr_in_list,rd_in_list,pass_fail_1st_val

    def third_stage_val(full_field_name,pre_rd,wr_in_list,rd_in_list,val_stage,wr_value,reset_detection,prefered_list):
        (wr_in_list,rd_in_list,pass_fail_1st_val) = Val_stage.first_stage_val(full_field_name,pre_rd,wr_in_list,rd_in_list,val_stage,wr_value,reset_detection,prefered_list)
        return wr_in_list,rd_in_list,pass_fail_1st_val

class Exec:
    def categorize_regs(pass_fail, full_field_name, chosen_attr_fields, cath_regs):
        [pass_regs, fail_regs, error_regs, sus_hang_regs, nocheck_regs] = cath_regs
        if pass_fail == 'pass':
            pass_regs.append(full_field_name)
        elif pass_fail == 'fail':
            fail_regs.append(full_field_name)
        elif pass_fail == 'error':
            error_regs.append(full_field_name)
        elif pass_fail == 'hang':
            sus_hang_regs.append(chosen_attr_fields[chosen_attr_fields.index(full_field_name)-9:chosen_attr_fields.index(full_field_name)+1])
        elif pass_fail == 'NA':
            nocheck_regs.append(full_field_name)
        return pass_regs, fail_regs, error_regs, sus_hang_regs, nocheck_regs

    def attr_preference(full_field_name, locklists):
        [lockbit_regs,lockattr_regs] = locklists
        if full_field_name in lockattr_regs:
            if lockbit_regs[lockattr_regs.index(full_field_name)] == None:
                lockbit_val = None
            else:
                lockbit_val = str(eval(lockbit_regs[lockattr_regs.index(full_field_name)]))
            if lockbit_val == '0x0':
                prefered_attr = "r/w"
                prefered_reason = 'Lockbit=0'
            elif lockbit_val == '0x1':
                prefered_attr = "ro"
                prefered_reason = 'Lockbit=1'
            else:
                prefered_attr = "r/w"
                prefered_reason = f'Lockbit={lockbit_val}'
        else:
            prefered_attr = None
            prefered_reason = None
        return prefered_attr, prefered_reason

    def validate_1by1(full_field_name,reset_detection,halt_detection,num_val_seq,pre_rd_num,locklists):#only on one chosen attr or all attrs.
        wr_in_list = []
        rd_in_list = []
        fail_reason = []
        [lockbit_regs,lockattr_regs] = locklists
        (prefered_attr, prefered_reason) = Exec.attr_preference(full_field_name, locklists)
        prefered_list = [prefered_attr, prefered_reason]
        if prefered_reason == None:
            pass
        else:
            fail_reason.append(prefered_reason)
        (pre_rd,pass_fail_pre_rd) = Val_stage.pre_read(full_field_name,pre_rd_num,prefered_list)
        if str(int(float(num_val_seq))) == "1":
            firststage_wr_value = 'FF'
        else:
            firststage_wr_value = 'A5'
        (wr_in_list,rd_in_list,pass_fail_1st_val) = Val_stage.first_stage_val(full_field_name,pre_rd,wr_in_list,rd_in_list,'1st_stage_rdwr',firststage_wr_value,reset_detection,prefered_list)
        if str(int(float(num_val_seq))) == "3":
            (wr_in_list,rd_in_list,pass_fail_2nd_val) = Val_stage.second_stage_val(full_field_name,pre_rd,wr_in_list,rd_in_list,'2nd_stage_rdwr','5A',reset_detection,prefered_list)
            (wr_in_list,rd_in_list,pass_fail_3rd_val) = Val_stage.third_stage_val(full_field_name,pre_rd,wr_in_list,rd_in_list,'3rd_stage_rdwr','A5',reset_detection,prefered_list)
        elif str(int(float(num_val_seq))) == "2":
            (wr_in_list,rd_in_list,pass_fail_2nd_val) = Val_stage.second_stage_val(full_field_name,pre_rd,wr_in_list,rd_in_list,'2nd_stage_rdwr','5A',reset_detection,prefered_list)
            wr_in_list.append('NA')
            rd_in_list.append('NA')
            pass_fail_3rd_val = 'NA'
        elif str(int(float(num_val_seq))) == "1":
            wr_in_list.append('NA')
            wr_in_list.append('NA')
            rd_in_list.append('NA')
            rd_in_list.append('NA')
            #if attr in ['roswc','rw/cr'] or attr in all_undefined_attrs:#store double read
            #    rd_in_list.append('NA')
            #    rd_in_list.append('NA')
            pass_fail_2nd_val = 'NA'
            pass_fail_3rd_val = 'NA'
        if 'fail' in [pass_fail_pre_rd,pass_fail_1st_val,pass_fail_2nd_val,pass_fail_3rd_val]:
            pass_fail = 'fail'
            fail_reason = track.track_fail_reason(pass_fail_pre_rd,pass_fail_1st_val,pass_fail_2nd_val,pass_fail_3rd_val,fail_reason)
        elif 'NA' in [pass_fail_pre_rd,pass_fail_1st_val,pass_fail_2nd_val,pass_fail_3rd_val]:#for the fields with the non-prepared attr and 1 num_val_seq case.
            if 'fail' in [pass_fail_pre_rd,pass_fail_1st_val,pass_fail_2nd_val,pass_fail_3rd_val]:#for ro/c and ro/v
                pass_fail = 'fail'
            elif 'pass' in [pass_fail_pre_rd,pass_fail_1st_val,pass_fail_2nd_val,pass_fail_3rd_val]:
                pass_fail = 'pass'
            else:
                pass_fail = 'NA'
        else:
            pass_fail = 'pass'
        if halt_detection and itp.isrunning() == False:#If system has soft hang or cat error.
            itp.go()
            time.sleep(3)
            fail_reason.append('halt')
        if 'sys_rst' in [pass_fail_1st_val,pass_fail_2nd_val,pass_fail_3rd_val]:
            fail_reason.append('sys_rst')
            pass_fail = 'fail'
            itp.resettarget()
            print("AggressiVE Forced reset!!!")
        return pre_rd,wr_in_list,rd_in_list,pass_fail,fail_reason
        
    def _reboot(pass_fail, hang_detection, full_field_name, cont_fail_cnt):
        if 'hang' in pass_fail and hang_detection:
            print('\n' + Fore.RED + "AggressiVE Forced Reboot due to hang!" + Fore.RESET)
            print(f'Reg: {full_field_name}')
            target.powerCycle(waitOff=1,waitAfter=1)
            while True:
                if target.readPostcode() == 0x10AD:
                    itp.unlock()
                    refresh()
                    break
        elif cont_fail_cnt == 10:
            print('\n' + Fore.RED + "AggressiVE Forced Reboot due to continuous reg fail(suspect hang)!" + Fore.RESET)
            target.powerCycle(waitOff=1,waitAfter=1)
            while True:
                if target.readPostcode() == 0x10AD:
                    itp.unlock()
                    refresh()
                    break
                    
    def _post_val_stage(num_status, alg, flg, status_infos, detections, auto, num_val_seq, locklists):
        [Pass, Fail, Error, Hang] = num_status
        [[pass_regs],[Fail,fail_regs,fail_x],[sus_hang_regs],[error_messages]] = status_infos
        post_val = detections[4]
        if post_val:
            reset_detection = detections[1]
            if reset_detection:
                print("Reboot for post validation in case it is hang!")
                target.powerCycle(waitOff=1,waitAfter=1)
                while True:
                    if target.readPostcode() == 0x10AD:
                        itp.unlock()
                        refresh()
                        break
            (alg, flg) = user.Post_test.choose_post_test([Pass, Fail, Error, Hang],alg,flg,[[pass_regs],[Fail,fail_regs,fail_x],[sus_hang_regs],[error_messages]],detections,auto,num_val_seq,locklists)
        return alg, flg
        
    def _store(pass_fail, detections, full_field_name, attr, fail_reason, tables_params, num_list):
        [rowdictlist, x, pass_rowdl,pass_x, fail_rowdl, fail_x,nochk_rowdictlist,nochk_x] = tables_params
        [Hang, cont_fail_cnt, num, nochk_cnt, num_val_seq, pre_rd, wr_in_list, rd_in_list] = num_list
        hang_detection, mca_check = detections[2], detections[3]
        if pass_fail == 'fail':
            if hang_detection and mca_check == 'every_failreg': # will do the machine check every fial reg detected.
                machine_chk_error = debug.mca.analyze()
                print(machine_chk_error)
                if machine_chk_error != []:
                    pass_fail = 'hang'
                    Hang+=1
                else:
                    cont_fail_cnt += 1
            (fail_rowdl,fail_x) = disp.store_fail_content(fail_rowdl,fail_x,num,full_field_name,attr,pass_fail,pre_rd,wr_in_list,rd_in_list,fail_reason,num_val_seq)
        elif pass_fail =='pass':#this statement is for continuous fail due to undetected hang
            cont_fail_cnt = 0 #reset it back due to not continuous fail.
            (pass_rowdl,pass_x) = disp.store_content(pass_rowdl,pass_x,num,full_field_name,attr,pass_fail,pre_rd,wr_in_list,rd_in_list,fail_reason,num_val_seq)
        elif pass_fail == 'NA':
            nochk_cnt += 1
            (nochk_rowdictlist,nochk_x) = disp.store_nocheck_content(nochk_rowdictlist,nochk_x,nochk_cnt,full_field_name,attr,pass_fail,pre_rd,wr_in_list,rd_in_list,num_val_seq)
        # storing validation info in table form.
        (rowdictlist,x) = disp.store_content(rowdictlist,x,num,full_field_name,attr,pass_fail,pre_rd,wr_in_list,rd_in_list,fail_reason,num_val_seq)
        return Hang, pass_fail, cont_fail_cnt, fail_rowdl, fail_x, pass_rowdl,pass_x, nochk_rowdictlist,nochk_x, rowdictlist,x
        
    def _print_data_in_condition(pass_fail, table_info, dump_info, num_info, detections):
        [rowdictlist, x, pass_rowdl, pass_x, fail_rowdl, fail_x, error_rowdl, error_x, nochk_rowdictlist, nochk_x] = table_info
        [alg, flg, plg, elg, nclg] = dump_info
        [num, num2print, Pass, Fail, Unknown, Error, Hang] = num_info
        hang_detection, mca_check = detections[2], detections[3]
    
        num2print -= 1
        if int(repr(num2print)[-1]) == 0:
            print('')
            if hang_detection and mca_check == 'every_10val':#will do the machine check every 10 validation.
                machine_chk_error = debug.mca.analyze()
                if machine_chk_error != []:
                    pass_fail = 'hang'
                    Hang+=1
            disp.disp_content(rowdictlist,x,alg,flg)
            if fail_rowdl != []:
                (alg, flg) = dump.export("store_fail", fail_x.getTableText(), alg, flg)
            if pass_rowdl != []:
                plg = dump.export_write_pass(plg, pass_x.getTableText())
            if error_rowdl != []:
                elg = dump.export_write_error(elg, error_x.getTableText())
            disp.disp_total_pass_fail(Pass,Fail,Unknown,Error,Hang)
            rowdictlist = []
            pass_rowdl = []
            fail_rowdl = []
            error_rowdl = []
            x = []
            if nochk_rowdictlist != []:
                nclg = dump.export_nocheck('store',nochk_x.getTableText(),nclg)
        num+=1
        return num2print, pass_fail, Hang, alg, flg, plg, elg, Pass, Fail, Unknown, Error, rowdictlist, pass_rowdl, fail_rowdl, error_rowdl, x, nclg, num
        
    def validate(valid_fields,chosen_attr,auto,detections,num_val_seq,random,locklists):
        # initialization
        [halt_detection,reset_detection,hang_detection,mca_check,post_val,pre_rd_num] = detections
        Pass, Fail, Unknown, Error, Hang, num2print, cont_fail_cnt, nochk_cnt, num = 0, 0, 0, 0, 0, 0, 0, 0, 1
        rowdictlist, pass_rowdl, fail_rowdl, error_rowdl, nochk_rowdictlist = [], [], [], [], []
        x, pass_x, fail_x, error_x, nochk_x = [], [], [], [], []
        validated_fields, pass_regs, fail_regs, error_regs, sus_hang_regs, nocheck_regs = [], [], [], [], [], []
        error_messages = {}
        # Exclude all the fields with non-chosen attr.
        chosen_attr_fields_all = track.track_chosen_attr_fields(valid_fields,chosen_attr)
        print(f"\nTotal Num Available= {str(len(chosen_attr_fields_all))}")
        if random != False: #re-suffle the arrangement of registers
            chosen_attr_fields = dice.sample(chosen_attr_fields_all, random)
            print(f"Total Random Num Available= {str(len(chosen_attr_fields))}")
        else:
            chosen_attr_fields = chosen_attr_fields_all
        # open dump log
        (alg,flg) = dump.export('open','NA','','')
        (nclg) = dump.export_nocheck('open','NA','')
        plg = open("AggressiVE_pass.log","a")
        elg = open("AggressiVE_error.log","a")
        #keep data into tobecont log folder
        dump.export_tobecont_allfields(chosen_attr_fields)

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
                reserved_num = 0
            reserved_num += 1
            disp.progress(reserved_num, reserved_print_num, prefix=f'Progress [{reserved_num}:{reserved_print_num}]:', infix1 = f'StartTime= {time.ctime()}', suffix=f'Reg: [{full_field_name}]')
            #validate
            attr = eval(full_field_name+'.info["attribute"]')
            try:
                (pre_rd,wr_in_list,rd_in_list,pass_fail,fail_reason) = Exec.validate_1by1(full_field_name,reset_detection,halt_detection,num_val_seq,pre_rd_num,locklists)
            except KeyboardInterrupt:
                print('\n' + Fore.RED + 'Validation forced to stopped!' + Fore.RESET)
                disp.disp_content(rowdictlist,x,alg,flg)
                disp.disp_total_pass_fail(Pass,Fail,Unknown,Error,Hang)
                dump.export_regs(pass_regs, fail_regs, error_regs, sus_hang_regs, nocheck_regs)
                dump.export_tobecont_final(validated_fields)
                return 1
            except:
                message = sys.exc_info()[1]
                fail_reason = str(message)
                if len(fail_reason) >= 30:
                    fail_reason = fail_reason[:35-len(fail_reason)]+'...'
                fail_reason = [fail_reason]
                error_messages[full_field_name]=str(message)
                pass_fail = 'error'
                pre_rd = wr_in_list = rd_in_list = []
                (error_rowdl,error_x) = disp.store_content(error_rowdl,error_x,num,full_field_name,attr,pass_fail,pre_rd,wr_in_list,rd_in_list,fail_reason,num_val_seq)
                if "'Python SV time-out reached (0.1 se..." in fail_reason and reset_detection:
                    print('\n' + Fore.RED + "AggressiVE Forced Reboot due to error message!" + Fore.RESET)
                    print(f"Reg: {full_field_name}")
                    target.powerCycle(waitOff=1,waitAfter=1)
                    while True:
                        if target.readPostcode() == 0x10AD:
                            itp.unlock()
                            refresh()
                            break
            try:
                #store pass, fail, & no_chk fields validation info separately.
                tables_params = [rowdictlist, x, pass_rowdl,pass_x, fail_rowdl, fail_x,nochk_rowdictlist,nochk_x]
                num_list = [Hang, cont_fail_cnt, num, nochk_cnt, num_val_seq, pre_rd, wr_in_list, rd_in_list]
                (Hang, pass_fail, cont_fail_cnt, fail_rowdl, fail_x, pass_rowdl,pass_x, nochk_rowdictlist,nochk_x,rowdictlist,x) = Exec._store(pass_fail, detections, full_field_name, attr, fail_reason, tables_params, num_list)
                #update num of pass/fail/etc regs.
                (Pass,Fail,Unknown,Error) = track.track_num_pass_fail(pass_fail,Pass,Fail,Unknown,Error)
                #print the table when reach number user want to print.
                (num2print, pass_fail, Hang, alg, flg, plg, elg, Pass, Fail, Unknown, Error, rowdictlist, pass_rowdl, fail_rowdl, error_rowdl, x, nclg, num) = Exec._print_data_in_condition(pass_fail, [rowdictlist, x, pass_rowdl, pass_x, fail_rowdl, fail_x, error_rowdl, error_x, nochk_rowdictlist, nochk_x], [alg, flg, plg, elg, nclg], [num, num2print, Pass, Fail, Unknown, Error, Hang], detections)
                #categorize registers in different logs.
                (pass_regs, fail_regs, error_regs, sus_hang_regs, nocheck_regs) = Exec.categorize_regs(pass_fail, full_field_name, chosen_attr_fields, [pass_regs, fail_regs, error_regs, sus_hang_regs, nocheck_regs])
                #detect hang and stop.
                Exec._reboot(pass_fail, hang_detection, full_field_name, cont_fail_cnt)
                #store validated fields as backup for ToBeCont.
                validated_fields.append(full_field_name)
            except KeyboardInterrupt:
                print('\n' + Fore.RED + 'Validation forced to stopped!' + Fore.RESET)
                print("After")
                disp.disp_content(rowdictlist,x,alg,flg)
                disp.disp_total_pass_fail(Pass,Fail,Unknown,Error,Hang)
                dump.export_regs(pass_regs, fail_regs, error_regs, sus_hang_regs, nocheck_regs)
                dump.export_tobecont_final(validated_fields)
                return 1
        # dump different categorized regs.
        dump.export_regs(pass_regs, fail_regs, error_regs, sus_hang_regs, nocheck_regs)
        #Post Validation
        (alg, flg) = Exec._post_val_stage([Pass, Fail, Error, Hang],alg,flg,[[pass_regs],[Fail,fail_regs,fail_x],[sus_hang_regs],[error_messages]],detections,auto,num_val_seq,locklists)
        # close dump log
        (alg,flg) = dump.export('close_all','NA',alg,flg)
        (alg,flg) = dump.export('close_fail','NA',alg,flg)
        nclg = dump.export_nocheck('close','NA',nclg)
        plg.close()
        elg.close()
        return 0
        
    def validate_cont(remain_fields,auto,detections,num_val_seq,locklists):
        # initialization
        [halt_detection,reset_detection,hang_detection,mca_check,post_val,pre_rd_num] = detections
        Pass, Fail, Unknown, Error, Hang, num2print, cont_fail_cnt, nochk_cnt, num = 0, 0, 0, 0, 0, 0, 0, 0, 1
        validated_fields, pass_regs, fail_regs, error_regs, sus_hang_regs, nocheck_regs = [], [], [], [], [], []
        rowdictlist, pass_rowdl, fail_rowdl, error_rowdl, nochk_rowdictlist = [], [], [], [], []
        x, pass_x, fail_x, error_x, nochk_x = [], [], [], [], []
        alg, flg, nclg = '', '', ''
        error_messages = {}
        #open dump log
        (alg,flg) = dump.export('open','NA',alg,flg)
        (nclg) = dump.export_nocheck('open','NA',nclg)
        plg = open("AggressiVE_pass.log","a")
        elg = open("AggressiVE_error.log","a")
        #keep data into tobecont log folder
        dump.export_tobecont_allfields(remain_fields)
        
        #validation.
        print(f"\nTotal Num Available= {str(len(remain_fields))}")
        num_chosen_attr_fields = len(remain_fields)
        reserved_print_num=len(remain_fields)
        for full_field_name in remain_fields:
            #to ask user for the num of table display.
            if num2print == 0:                                                                                                              
                (num2print,reserved_print_num) = user.Exec.print_limit(num_chosen_attr_fields,reserved_print_num,auto)
                if num2print == 'end':
                    break
                num_chosen_attr_fields-=num2print
                reserved_num = 0
            reserved_num += 1
            disp.progress(reserved_num, reserved_print_num, prefix=f'Progress [{reserved_num}:{reserved_print_num}]:', infix1 = f'StartTime= {time.ctime()}', suffix=f'Reg: [{full_field_name}]')
            #validate
            attr = eval(full_field_name+'.info["attribute"]')
            try:
                (pre_rd,wr_in_list,rd_in_list,pass_fail,fail_reason) = Exec.validate_1by1(full_field_name,reset_detection,halt_detection,num_val_seq,pre_rd_num,locklists)
            except KeyboardInterrupt:
                print('\n' + Fore.RED + 'Validation forced to stopped again!' + Fore.RESET)
                disp.disp_content(rowdictlist,x,alg,flg)
                disp.disp_total_pass_fail(Pass,Fail,Unknown,Error,Hang)
                #close all log files
                (alg,flg) = dump.export('close_all','NA',alg,flg)
                (alg,flg) = dump.export('close_fail','NA',alg,flg)
                nclg = dump.export_nocheck('close','NA',nclg)
                plg.close()
                elg.close()
                dump.export_regs(pass_regs, fail_regs, error_regs, sus_hang_regs, nocheck_regs)
                dump.export_tobecont_final(validated_fields) # dump validated_fields for cont next time.
                return 1
            except:
                message = sys.exc_info()[1]
                fail_reason = str(message)
                if len(fail_reason) >= 30:
                    fail_reason = fail_reason[:35-len(fail_reason)]+'...'
                fail_reason = [fail_reason]
                error_messages[full_field_name]=str(message)
                pass_fail = 'error'
                pre_rd = wr_in_list = rd_in_list = []
                (error_rowdl,error_x) = disp.store_content(error_rowdl,error_x,num,full_field_name,attr,pass_fail,pre_rd,wr_in_list,rd_in_list,fail_reason,num_val_seq)
                if "'Python SV time-out reached (0.1 se..." in fail_reason and reset_detection:
                    print('\n' + Fore.RED + "AggressiVE Forced Reboot due to error message!" + Fore.RESET)
                    print(f"Reg: {full_field_name}")
                    target.powerCycle(waitOff=1,waitAfter=1)
                    while True:
                        if target.readPostcode() == 0x10AD:
                            itp.unlock()
                            refresh()
                            break

            #store validated fields as backup for ToBeCont.
            validated_fields.append(full_field_name)
            #store pass, fail, & no_chk fields validation info separately.
            tables_params = [rowdictlist, x, pass_rowdl,pass_x, fail_rowdl, fail_x,nochk_rowdictlist,nochk_x]
            num_list = [Hang, cont_fail_cnt, num, nochk_cnt, num_val_seq, pre_rd, wr_in_list, rd_in_list]
            (Hang, pass_fail, cont_fail_cnt, fail_rowdl, fail_x, pass_rowdl,pass_x, nochk_rowdictlist,nochk_x,rowdictlist,x) = Exec._store(pass_fail, detections, full_field_name, attr, fail_reason, tables_params, num_list)
            #update num of pass/fail/etc regs.
            (Pass,Fail,Unknown,Error) = track.track_num_pass_fail(pass_fail,Pass,Fail,Unknown,Error)
            #print the table when reach number user want to print.
            (num2print, pass_fail, Hang, alg, flg, plg, elg, Pass, Fail, Unknown, Error, rowdictlist, pass_rowdl, fail_rowdl, error_rowdl, x, nclg, num) = Exec._print_data_in_condition(pass_fail, [rowdictlist, x, pass_rowdl, pass_x, fail_rowdl, fail_x, error_rowdl, error_x, nochk_rowdictlist, nochk_x], [alg, flg, plg, elg, nclg], [num, num2print, Pass, Fail, Unknown, Error, Hang], detections)
            #categorize registers in different logs.
            (pass_regs, fail_regs, error_regs, sus_hang_regs, nocheck_regs) = Exec.categorize_regs(pass_fail, full_field_name, remain_fields, [pass_regs, fail_regs, error_regs, sus_hang_regs, nocheck_regs])
            #detect hang and stop.
            Exec._reboot(pass_fail, hang_detection, full_field_name, cont_fail_cnt)
        # dump different categorized regs.
        dump.export_regs(pass_regs, fail_regs, error_regs, sus_hang_regs, nocheck_regs)
        # Post Validation
        (alg, flg) = Exec._post_val_stage([Pass, Fail, Error, Hang],alg,flg,[[pass_regs],[Fail,fail_regs,fail_x],[sus_hang_regs],[error_messages]],detections,auto,num_val_seq,locklists)
        # close dump log
        (alg,flg) = dump.export('close_all','NA',alg,flg)
        (alg,flg) = dump.export('close_fail','NA',alg,flg)
        nclg = dump.export_nocheck('close','NA',nclg)
        plg.close()
        elg.close()
        return 0
        
class Post_test:
    def simplify_error_msg(full_err_msg):
        simplified_msr = []
        if isinstance(full_err_msg,list):
            pass
        else:
            full_err_msg = [full_err_msg]
        for msg in full_err_msg:
            if "SOCKET" in msg:
                index = msg.find("SOCKET")
                simplified_msr.append(msg[index:])
            else:
                simplified_msr.append(msg)
        return simplified_msr
    
    def machine_check(hang_state, mca_err, index):
        machine_chk_error = debug.mca.analyze()
        if machine_chk_error != []:
            machine_chk_error = Post_test.simplify_error_msg(machine_chk_error)
            mca_err += machine_chk_error
            hang_state[index] = 1
            target.powerCycle(waitOff=1,waitAfter=1)
            while True:
                if target.readPostcode() == 0x10AD:
                    itp.unlock()
                    break
        return hang_state,mca_err

    def hang_validate_1by1(full_field_name, confirm_hang_regs, hang_stages, regs_mca_errs):
        wr_in_list = []
        rd_in_list = []
        fail_reason = []
        hang_state = [0,0,0,0]
        mca_err = []
        (pre_rd,pass_fail_pre_rd) = Val_stage.pre_read(full_field_name)
        (hang_state,mca_err) = Post_test.machine_check(hang_state, mca_err, 0)
        (wr_in_list,rd_in_list,pass_fail_1st_val) = Val_stage.first_stage_val(full_field_name,pre_rd,wr_in_list,rd_in_list,'1st_stage_rdwr','A5',False)
        (hang_state,mca_err) = Post_test.machine_check(hang_state, mca_err, 1)
        (wr_in_list,rd_in_list,pass_fail_2nd_val) = Val_stage.second_stage_val(full_field_name,pre_rd,wr_in_list,rd_in_list,'2nd_stage_rdwr','5A',False)
        (hang_state,mca_err) = Post_test.machine_check(hang_state, mca_err, 2)
        (wr_in_list,rd_in_list,pass_fail_3rd_val) = Val_stage.third_stage_val(full_field_name,pre_rd,wr_in_list,rd_in_list,'3rd_stage_rdwr','A5',False)
        (hang_state,mca_err) = Post_test.machine_check(hang_state, mca_err, 3)
        if 1 in hang_state:
            confirm_hang_regs.append(full_field_name)
            hang_stages.append(hang_state)
            regs_mca_errs.append(mca_err)
        return confirm_hang_regs, hang_stages, regs_mca_errs

    def validate2_hang_regs(sus_hang_regs, alg, flg):
        confirm_hang_regs = []
        hang_stages = []
        regs_mca_errs = []
        hang_stage_reason = ['Pre-read','1st read-write','2nd read-write','3rd read-write']
        final_hang_stages = []
        hlg = open("AggressiVE_hang.log","a")
        #Do a reboot before validation to prevent hang at the beginning.
        target.powerCycle(waitOff=1,waitAfter=1)
        while True:
            if target.readPostcode() == 0x10AD:
                itp.unlock()
                refresh()
                break
        #validate the suspect hang registers once and for all. Do machine check in every validation stages.
        try:
            for sus_regs in sus_hang_regs:
                for reg in sus_regs:
                    print('\n' + Fore.BLUE + f'REG{str(sus_regs.index(reg))}/{str(len(sus_regs))} in List{str(len(sus_hang_regs))}/{str(len(sus_regs))}' + Fore.BLUE)
                    (confirm_hang_regs, hang_stages, regs_mca_errs) = Post_test.hang_validate_1by1(reg, confirm_hang_regs, hang_stages, regs_mca_errs)
        except KeyboardInterrupt:
            print('\n' + Fore.RED + 'Hang 2nd Validation forced to stopped!' + Fore.RESET)
            (alg, flg, hlg) = disp.disp_hang_regs(confirm_hang_regs, final_hang_stages, regs_mca_errs, alg, flg, hlg)
            hlg.close()
            dump.export_hang_regs(confirm_hang_regs)
            return alg, flg
        except:
            print('\n' + Fore.RED + 'Hang 2nd Validation detected error message!' + Fore.RESET)
            (alg, flg, hlg) = disp.disp_hang_regs(confirm_hang_regs, final_hang_stages, regs_mca_errs, alg, flg, hlg)
            hlg.close()
            dump.export_hang_regs(confirm_hang_regs)
            return alg, flg
        ##for reg_hang_stages in hang_stages:
        for hang_stage in hang_stages:
            temp = []
            for n in range(4):
                if hang_stage[n] == 1:
                    temp.append(hang_stage_reason[n])
            final_hang_stages.append(temp)
        (alg, flg, hlg) = disp.disp_hang_regs(confirm_hang_regs, final_hang_stages, regs_mca_errs, alg, flg, hlg)
        hlg.close()
        dump.export_hang_regs(confirm_hang_regs)
        target.powerCycle(waitOff=1,waitAfter=1)
        while True:
            if target.readPostcode() == 0x10AD:
                itp.unlock()
                return alg, flg

    def validate2_fail_regs(fail_regs,alg,flg,Fail,auto,detections,num_val_seq,locklists):
        num2print=0
        num_chosen_attr_fields = len(fail_regs)
        reserved_print_num = num_chosen_attr_fields
        fail_rowdl = []
        fail_x = []
        Pass2 = 0
        Fail2 = 0
        Unknown2 = 0
        Error2 = 0
        num=1
        error_messages = {}
        reserved_print_num = len(fail_regs)
        for fail_field_name in fail_regs:
            #to ask user for the num of table display.
            if num2print == 0:#to ask user for the num of table display.
                (num2print,reserved_print_num) = user.Exec.print_limit(num_chosen_attr_fields,reserved_print_num,auto)
                if num2print == 'end':
                    return alg,flg
                num_chosen_attr_fields-=num2print
                reserved_num = 0
            reserved_num += 1
            disp.progress(reserved_num, reserved_print_num, prefix=f'Progress [{reserved_num}:{reserved_print_num}]:', infix1 = f'StartTime= {time.ctime()}', suffix=f'Reg: [{fail_field_name}]')
            #validate
            try:
                (pre_rd,wr_in_list,rd_in_list,pass_fail,fail_reason) = Exec.validate_1by1(fail_field_name,detections[1],detections[0],num_val_seq,detections[5],locklists)
            except KeyboardInterrupt:
                print('\n' + Fore.RED + 'Fail 2nd Validation forced to stopped!' + Fore.RESET)
                disp.disp_fail_content(fail_x,alg,flg)
                disp.disp_total_pass_fail(Pass2,Fail2,Unknown2,Error2,0)
                break
            except:
                message = sys.exc_info()[1]
                fail_reason = str(message)
                if len(fail_reason) >= 30:
                    fail_reason = fail_reason[:35-len(fail_reason)]+'...'
                fail_reason = [fail_reason]
                error_messages[fail_field_name]=str(message)
                pass_fail = 'error'
                pre_rd = wr_in_list = rd_in_list = ['NA','NA','NA']
            attr = eval(fail_field_name+'.info["attribute"]')
            (fail_rowdl,fail_x) = disp.store_fail_content(fail_rowdl,fail_x,num,fail_field_name,attr,pass_fail,pre_rd,wr_in_list,rd_in_list,fail_reason,num_val_seq)
            (Pass2,Fail2,Unknown2,Error2) = track.track_num_pass_fail(pass_fail,Pass2,Fail2,Unknown2,Error2)
            if 'hang' in fail_reason:
                num2print = 0
            num2print -= 1
            if int(repr(num2print)[-1]) == 0:
                print('')
                disp.disp_fail_content(fail_x,alg,flg)
                print(f'{Fail} fail(s) in 1st validation.')
                disp.disp_total_pass_fail(Pass2,Fail2,Unknown2,Error2,0)
                (alg,flg) = dump.export('store_fail',fail_x.getTableText(),alg,flg)
                (alg,flg) = dump.export('store_fail',f'Pass:{Pass2}',alg,flg)
                (alg,flg) = dump.export('store_fail',f'Fail:{Fail2}',alg,flg)
                (alg,flg) = dump.export('store_fail',f'Unknown:{Unknown2}',alg,flg)
                (alg,flg) = dump.export('store_fail',f'Error:{Error2}',alg,flg)
                #(alg,flg) = dump.export('store_fail',f'Hang:{Hang2}',alg,flg)
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
                #break
                while True:
                    if target.readPostcode() == 0x10AD:
                        itp.unlock()
                        break
                (alg,flg) = dump.export('store',hang_reason,alg,flg)
                (alg,flg) = dump.export('store',str(machine_chk_error),alg,flg)
                (alg,flg) = dump.export('store_fail',hang_reason,alg,flg)
                (alg,flg) = dump.export('store_fail',str(machine_chk_error),alg,flg)
                    
        #shows num of passed fields.
        if Fail2 == Fail:
            print('In second validation, no pass sub-register.')
        else:
            print(f"In second validation, there's {Pass2} pass registers.")
        return alg,flg

    def validate_pass(pass_infos,Pass,alg,flg,detections,auto,num_val_seq,locklists):
        num = 1
        plg = []
        #pass_regs_sets = []
        pass_regs_sets = pass_infos
        while num > 0:
            try:
                plg = open("pass_regs_"+str(num)+".log",'r')
                pass_regs_sets.append(plg.readlines())
                plg.close()
                print('Detected pass_regs_'+str(num)+'.log')
            except:
                break
            num+=1
        #comparing
        final_list_regs = []
        for pass_regs_set in pass_regs_sets:
            pass_regs_set = [pass_reg.replace('\n','') for pass_reg in pass_regs_set]
            if final_list_regs == []:
                final_list_regs = pass_regs_set
            else:
                final_list_regs = list(set(final_list_regs) | set(pass_regs_set))	      
        plg = open("AggressiVE_pass.log","a")
        num=1
        num2print=0
        rowdictlist,x = [],[]
        error_messages = {}
        #validation.
        num_chosen_attr_fields = len(final_list_regs)
        reserved_print_num=len(final_list_regs)
        Pass,Fail,Unknown,Error,Hang = 0,0,0,0,0
        print('Post-validation: Pass Registers Re-write is chosen!')
        (alg,flg) = dump.export('store','Post-validation: Pass Registers Re-write is chosen!',alg,flg)
        plg = dump.export_write_pass(plg,'Post-validation: Pass Registers Re-write is chosen!')
        for reg in final_list_regs:
            #to ask user for the num of table display.
            if num2print == 0:                                                                                                              
                (num2print,reserved_print_num) = user.Exec.print_limit(num_chosen_attr_fields,reserved_print_num,auto)
                if num2print == 'end':
                    break
                num_chosen_attr_fields-=num2print
                ##initial_time = time.time()
                reserved_num = 0
            reserved_num += 1
            disp.progress(reserved_num, reserved_print_num, prefix=f'Progress [{reserved_num}:{reserved_print_num}]:', infix1 = f'StartTime= {time.ctime()}', suffix=f'Reg: [{reg}]')
            #validate
            try:
                (pre_rd,wr_in_list,rd_in_list,pass_fail,fail_reason) = Exec.validate_1by1(reg,detections[1],detections[0],num_val_seq,detections[5],locklists)
            except KeyboardInterrupt:
                print('\n' + Fore.RED + 'Pass 2nd Validation forced to stopped!' + Fore.RESET)
                disp.disp_content(rowdictlist,x,alg,flg)
                disp.disp_total_pass_fail(Pass,Fail,Unknown,Error,Hang)
                break
            except:
                message = sys.exc_info()[1]
                fail_reason = str(message)
                if len(fail_reason) >= 30:
                    fail_reason = fail_reason[:35-len(fail_reason)]+'...'
                fail_reason = [fail_reason]
                error_messages[reg]=str(message)
                pass_fail = 'error'
                pre_rd = wr_in_list = rd_in_list = ['NA','NA','NA']
            #display and storing validation info in table form.
            attr = eval(reg+'.info["attribute"]')
            (rowdictlist,x) = disp.store_content(rowdictlist,x,num,reg,attr,pass_fail,pre_rd,wr_in_list,rd_in_list,fail_reason,num_val_seq)
            (Pass,Fail,Unknown,Error) = track.track_num_pass_fail(pass_fail,Pass,Fail,Unknown,Error)
            #print the table when reach number user want to print.
            if pass_fail == 'fail':
                if detections[2] and detections[3] == 'every_failreg':
                    machine_chk_error = debug.mca.analyze()
                    if machine_chk_error != []:
                        pass_fail = 'hang'
                        Hang += 1
            num2print -= 1
            if int(repr(num2print)[-1]) == 0:
                print('')
                if detections[2] and detections[3] == 'every_10val':
                    machine_chk_error = debug.mca.analyze()
                    if machine_chk_error != []:
                        pass_fail = 'hang'
                        Hang += 1
                disp.disp_content(rowdictlist,x,alg,flg)
                disp.disp_total_pass_fail(Pass,Fail,Unknown,Error,Hang)
                plg = dump.export_write_pass(plg,x.getTableText())
                plg = dump.export_write_pass(plg,f'Pass:{Pass}')
                plg = dump.export_write_pass(plg,f'Fail:{Fail}')
                plg = dump.export_write_pass(plg,f'Unknown:{Unknown}')
                plg = dump.export_write_pass(plg,f'Error:{Error}')
                plg = dump.export_write_pass(plg,f'Hang:{Hang}')
                rowdictlist=[]
                x=[]
            num+=1
            #detect hang and stop.
            if 'hang' in pass_fail:
                print('Validation will be stopped due to the present of machine check error')
                (alg,flg) = dump.export('store','Validation will be stopped due to the present of machine check error',alg,flg)
                (alg,flg) = dump.export('store',str(machine_chk_error),alg,flg)
                (alg,flg) = dump.export('store_fail','Validation will be stopped due to the present of machine check error',alg,flg)
                (alg,flg) = dump.export('store_fail',str(machine_chk_error),alg,flg)
                plg = dump.export_write_pass(plg,'Validation will be stopped due to the present of machine check error')
                plg = dump.export_write_pass(plg,str(machine_chk_error))
                target.powerCycle(waitOff=1,waitAfter=1)
                while True:
                    if target.readPostcode() == 0x10AD:
                        itp.unlock()
                        break
                break
        plg.close()
        return alg, flg

        