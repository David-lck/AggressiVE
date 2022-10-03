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
import read_write as rw
import export_log_file as dump
import aggressive as ags
from pysvtools.asciitable import AsciiTable as Table
import tracking as track
import os


class Pre_test:
    def _main(input_regs):
        #check for the input correction
        try:
            eval('__main__.'+input_regs)
        except:
            print('No such die exist in this project!')
            print('Please enter the correct one!')
            return 
        #detect the badname regs
        (badname_registers,attr_fields) = Pre_test.track_badname_regs(input_regs)
        #if yes, cont. if no, end with message.
        if badname_registers == []:
            return 'Bravo. There is no unacceptable name registers!'
        #get attrs #dump
        (avail_attrs,attr_badname_regs,no_last_list,last_level_list) = Pre_test._get_badname_attrs(badname_registers)
        print("Number of 'With Attribute Unacceptable Name' Registers: {len(attr_badname_regs)}")
        print("Number of 'Without Attribute Unacceptable Name' Registers: {len(badname_registers) - len(attr_badname_regs)}")
		Pre_test._chk_num_attrs_regs(avail_attrs,attr_badname_regs,no_last_list,last_level_list)
		
    def track_badname_regs(input_reg):
        print(f'Getting information from {input_reg} ...')
        print('Detecting and storing all the bad naming registers...')
        valid_fields = []
        bad_regsname = []
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
                            bad_regsname.append(input_reg+"."+register1+"."+register2)
            except:
                bad_regsname.append(input_reg+"."+register1)
        return bad_regsname, valid_fields

    def _get_badname_attrs(badname_registers):
        no_last_list = []
        last_level_list = []
        avail_attrs = []
        attr_badname_regs = []
        for badname_reg in badname_registers:
            #Extract the last level out since unacceptable
            no_last_lvl_reg = ".".join(badname_reg.split('.')[:-1]) if badname_reg[-1] != '.' else ".".join(badname_reg.split('.')[:-2])
            last_lvl_reg = badname_reg.split('.')[-1] if badname_reg[-1] != '.' else badname_reg.split('.')[-2]
            try:
                avail_attrs.append(eval(no_last_lvl_reg+".getfielddefinition('"+last_lvl_reg+"').attribute"))
                attr_badname_regs.append(badname_reg)
                no_last_list.append(no_last_lvl_reg)
                last_level_list.append(last_lvl_reg)
            except:
                pass
        return avail_attrs,attr_badname_regs,no_last_list,last_level_list

    def _chk_num_attrs_regs(avail_attrs,attr_badname_regs,no_last_list,last_level_list):
        print('Detecting and Categorizing attributes information...')
        avai_attrs = []
        num_avai_attr = []
        attr_temp = []
        for avail_attr in tqdm(avail_attrs):
            if avail_attr not in attr_temp:
                attr_temp.append(avail_attr)
                num_avai_attr.append(1)
            else:
                pointer = attr_temp.index(avail_attr)
                num_avai_attr[pointer] += 1
        (new_attrs,new_num) = ags.Pre_test._comb_same_attr(attr_temp,num_avai_attr)
        #display all the attrs and num of fields.
        i = 0
        table = []
        headers = ['Num','Attributes','Num of fields','Algorithm']
        for new_attr in new_attrs:
            if new_attr == 'rw':
                new_attr = 'r/w'
            elif new_attr == 'rw/c':
                new_attr = 'r/wc'
            if new_attr in ags.Algorithm.STATUS:
                algo = ags.Algorithm.STATUS[new_attr]
            else:
                algo = 'Undefined'
            table += [{'Num':i+1,'Attributes':new_attr ,'Num of fields':new_num[i],'Algorithm':algo}]
            i+=1
        total_num_valid_fields = len(attr_badname_regs)
        table += [{'Num':'-','Attributes':'Total num of fields' ,'Num of fields':total_num_valid_fields,'Algorithm':'-'}]
        x = Table.fromDictList(table,headers)
        print(x.getTableText())


class Exec:
    def _main:
        return




class Post_test:
    def _main:
	    return