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
import read_write as rw
import aggressive as ags
import export_log_file as dump
import sys
try:
    from tqdm.tqdm import tqdm
except:
    from tqdm import tqdm
import pysvtools.fv_common.target as target
from meteorlake import debug
from pysvtools.asciitable import AsciiTable as Table
import os


class Pre_test:
    def _main(input_regs, auto):
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
        #get attrs
        (avail_attrs,attr_badname_regs,no_last_list,last_level_list) = Pre_test._get_badname_attrs(badname_registers)
        print("Number of 'With Attribute Unacceptable Name' Registers: {len(attr_badname_regs)}")
        print("Number of 'Without Attribute Unacceptable Name' Registers: {len(badname_registers) - len(attr_badname_regs)}")
		(avail_attrs_list, avail_attrs_num) = Pre_test._chk_num_attrs_regs(avail_attrs,attr_badname_regs,no_last_list,last_level_list)
        #choose attr
        chosen_attr = user.Pre_test.attr_choice(avail_attrs_list,True,'')#choose the one for validation.('r/w' or '')
        (chosen_regs, filt_no_last_list, filt_last_level_list) = Pre_test._filter_fields(chosen_attr, avail_attrs,attr_badname_regs,no_last_list,last_level_list)
        #choose access method if available #dump
        Pre_test.access_method()#wip
        return chosen_regs, filt_no_last_list, filt_last_level_list
		
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
        (invf, vf) = dump.export_invalidate('open', '', '', '')
        print("Getting badname registers' attribute...")
        for badname_reg in tqdm(badname_registers):
            #Extract the last level out since unacceptable
            no_last_lvl_reg = ".".join(badname_reg.split('.')[:-1]) if badname_reg[-1] != '.' else ".".join(badname_reg.split('.')[:-2])
            last_lvl_reg = badname_reg.split('.')[-1] if badname_reg[-1] != '.' else badname_reg.split('.')[-2]
            try:
                avail_attrs.append(eval(no_last_lvl_reg+".getfielddefinition('"+last_lvl_reg+"').attribute"))
                attr_badname_regs.append(badname_reg)
                no_last_list.append(no_last_lvl_reg)
                last_level_list.append(last_lvl_reg)
                (invf, vf) = dump.export_invalidate('store_valid', badname_reg, invf, vf)
            except:
                (invf, vf) = dump.export_invalidate('store_invalid', badname_reg, invf, vf)
                pass
        (invf, vf) = dump.export_invalidate('close', '', invf, vf)
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
        (new_attrs,new_num_fields) = ags.Pre_test._comb_same_attr(attr_temp,num_avai_attr)
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
            table += [{'Num':i+1,'Attributes':new_attr ,'Num of fields':new_num_fields[i],'Algorithm':algo}]
            i+=1
        total_num_valid_fields = len(attr_badname_regs)
        table += [{'Num':'-','Attributes':'Total num of fields' ,'Num of fields':total_num_valid_fields,'Algorithm':'-'}]
        x = Table.fromDictList(table,headers)
        print(x.getTableText())
        print('Exporting table to attr_all.log...')
        aa = dump.export_attr_all('open','','')
        aa = dump.export_attr_all('store',x.getTableText(),aa)
        aa = dump.export_attr_all('close','',aa)
        return new_attrs, new_num_fields

    def access_method():#wip
        pass

    def _filter_fields(chosen_attr, avail_attrs,attr_badname_regs,no_last_list,last_level_list):
        chosen_regs, filt_no_last_list, filt_last_level_list = [],[],[]
        print('Filtering badname registes...')
        for attr in tqdm(avail_attrs):
            if chosen_attr != '' and attr != chosen_attr:
                continue
            chosen_regs.append(attr_badname_regs[avail_attrs.index(attr)])
            filt_no_last_list.append(no_last_list[avail_attrs.index(attr)])
            filt_last_level_list.append(last_level_list[avail_attrs.index(attr)])
        return chosen_regs, filt_no_last_list, filt_last_level_list

class Exec:
    def _main(chosen_regs, filt_no_last_list, filt_last_level_list, auto, is_targsim):#AggressiVE_badname.log #pass_regs.log #fail_regs.log #error_regs.log #sus_hang_regs.log #hang_regs.log
        #validation #dump
        Exec._validation_badname(chosen_regs, filt_no_last_list, filt_last_level_list, auto, is_targsim)
        #categorize regs with pass/fail/error/hang. #dump to each logs.

    def _validation_badname(chosen_regs, filt_no_last_list, filt_last_level_list, auto, is_targsim):
        num2print = 0
        Pass, Fail, Unknown, Error, Hang = 0, 0, 0, 0, 0
        table, x = [], []
        num=1
        num_chosen_attr_fields = len(chosen_regs)
        reserved_print_num = len(reserved_print_num)
        error_messages = {}
        for reg in chosen_regs:
            #to ask user for the num of table display
            if num2print == 0:
                (num2print,reserved_print_num) = user.Exec.print_limit(num_chosen_attr_fields,reserved_print_num,auto)
                if num2print == 'end':
                    break
                num_chosen_attr_fields-=num2print
                reserved_num = 0
            reserved_num += 1
            disp.progress(reserved_num, reserved_print_num, prefix=f'Progress [{reserved_num}:{reserved_print_num}]:', infix1 = f'StartTime= {time.ctime()}', suffix=f'Reg: [{reg}]')
            attr = eval(no_last_lvl_reg[chosen_regs.index(reg)]+".getfielddefinition('"+last_lvl_reg[chosen_regs.index(reg)]+"').attribute")
            #to validate
            try:
                (pre_rd,wr_in_list,rd_in_list,pass_fail,fail_reason) = Exec._validate1by1(reg,filt_no_last_list[chosen_regs.index(reg)], filt_last_level_list[chosen_regs.index(reg)],attr,is_targsim)
            except KeyboardInterrupt:
                print('\n' + Fore.RED + 'Validation forced to stopped!' + Fore.RESET)
                #display and storing validation info in table form.
                break
            except:
                message = sys.exc_info()[1]
                fail_reason = str(message)
                if len(fail_reason) >= 30:
                    fail_reason = fail_reason[:35-len(fail_reason)]+'...'
                fail_reason = [fail_reason]
                error_messages[reg]=str(message)
                pass_fail = 'error'
                pre_rd = wr_in_list = rd_in_list = []
            #display and storing validation info in table form.
            (table,x) = disp.store_content(table,x,num,reg,attr,pass_fail,pre_rd,wr_in_list,rd_in_list,fail_reason)
            (Pass,Fail,Unknown,Error) = track.track_num_pass_fail(pass_fail,Pass,Fail,Unknown,Error)
            #print the table when reach number user want to print.
            num2print -= 1
            if int(repr(num2print)[-1]) == 0:
                print('')
                if not is_targsim:
                    machine_chk_error = debug.mca.analyze()
                    if machine_chk_error != []:
                        pass_fail = 'hang'
                        Hang+=1
                print(x.getTableText())				
                disp.disp_total_pass_fail(Pass,Fail,Unknown,Error,Hang)
                table=[]
                x=[]
            num+=1
            #detect hang and stop.
            if 'hang' in pass_fail and not is_targsim:
                target.powerCycle(waitOff=1,waitAfter=1)
                while True:
                    if target.readPostcode() == 0x10AD:
                        itp.unlock()
                        break

    def _validate1by1(full_field_name, no_last_name, last_level_name, attr, is_targsim):
        wr_in_list = []
        rd_in_list = []
        fail_reason = []
        (pre_rd,pass_fail_pre_rd) = Val_stage.pre_read(no_last_name, last_level_name, attr)
        (wr_in_list,rd_in_list,pass_fail_1st_val) = Val_stage.first_stage_val(no_last_name, last_level_name, pre_rd,wr_in_list,rd_in_list,'1st_stage_rdwr','A5',is_targsim, attr)#wip
        (wr_in_list,rd_in_list,pass_fail_2nd_val) = Val_stage.second_stage_val(full_field_name,pre_rd,wr_in_list,rd_in_list,'2nd_stage_rdwr','5A',is_targsim)
        (wr_in_list,rd_in_list,pass_fail_3rd_val) = Val_stage.third_stage_val(full_field_name,pre_rd,wr_in_list,rd_in_list,'3rd_stage_rdwr','A5',is_targsim)
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

class Val_stage:
    def pre_read(no_last_name, last_level_name, no_last_name, last_level_name, attr):#It is mainly for attr = ro/swc
        pre_rd1 = str(eval(no_last_name + ".readfield('"+last_level_name+"')"))
        pre_rd2 = str(eval(no_last_name + ".readfield('"+last_level_name+"')"))
        pre_rd = [pre_rd1,pre_rd2]
        numbit = eval(no_last_name+".getfielddefinition('"+last_level_name+"').numbits")
        if attr == 'ro/swc':
            pass_fail = rw.Algorithm.val_roswc(numbit,'pre_rd',pre_rd)
            return pre_rd,pass_fail
        elif attr == 'ro/c':
            pass_fail = rw.Algorithm.val_ros(numbit,'pre_rd',pre_rd)
            return pre_rd,pass_fail
        if attr == 'na':
            pass_fail = rw.Algorithm.val_na(numbit,'pre_rd',pre_rd)
            return pre_rd,pass_fail
        return pre_rd,'pass'

    def first_stage_val(no_last_name, last_level_name, pre_rd,wr_in_list,rd_in_list,val_stage,wr_value,is_targsim, attr):
        numbit = eval(no_last_name+".getfielddefinition('"+last_level_name+"').numbits")
        #identify attr of this field in universal attr name.
        attr = track.Pre_test.track_attr_cat(attr)
        #write 'A5'/'5A' to field with and without algorithm.
        if attr == 'ro/c' and val_stage in ['2nd_stage_rdwr','3rd_stage_rdwr']:
            wr = rd = 'NA'
        if attr in ['rw','rw/s','rw/l','rw/1c','rw/1l','rw/1s','rw/c','ro/swc','ro','wo','rsv','rw/o'] or attr in rw.all_undefined_attrs or attr in rw.new_defined_attrs:
            wr = rw.create_value(numbit,wr_value)
            wr = rw.Conv.convert_bin_to_dec(wr)
            Val_stage.write(no_last_name, last_level_name,wr)
            wr = Conv.convert_dec_to_hex(wr)#for table display purposes
        #No write, show 'NA' to field without algorithm.
        else:
            wr='NA'
        #read and compare to get result(pass/fail) for field with algorithm.
        if wr != 'NA':
            rd = Val_stage.read(no_last_name, last_level_name)
            if attr in ['roswc','rw/cr'] or attr in rw.all_undefined_attrs:#double read
                rd2 = Val_stage.read(no_last_name, last_level_name)
                two_read_value = [rd,rd2]
                pass_fail = rw.compare(attr,wr,two_read_value,pre_rd,numbit,val_stage)
            else:
                pass_fail = rw.compare(attr,wr,rd,pre_rd,numbit,val_stage)
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
        if not is_targsim:
            if target.readPostcode() != 0x10AD:#only for UEFI.
                pass_fail = 'sys_rst'
        return wr_in_list,rd_in_list,pass_fail
		
    def write(no_last_name, last_level_name,write_value):
        eval(no_last_name + ".writefield('"+last_level_name+"',"+write_value+")"))
		
    def read(no_last_name, last_level_name):
        value = eval(no_last_name + ".readfield('"+last_level_name+"')")
        return value
