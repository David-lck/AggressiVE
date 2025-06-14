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
socket = __main__.socket if hasattr(__main__, 'socket') else None
refresh = __main__.refresh if hasattr(__main__, 'refresh') else None

from pysvtools.asciitable import AsciiTable as Table
import time
import colorama
from colorama import Fore
import pandas as pd
from builtins import *
from builtins import str
from builtins import range
from builtins import object
import namednodes as _namednodes
from namednodes import sv
try:
    from tqdm.tqdm import tqdm
except:
    from tqdm import tqdm

#project = itp.threads.device.alias[0]
import sys
#itp.unlockerflush()
#itp.entercredentials()
#if 'TGL' in project:
#    import tigerlake.debug.domains.pm.pm_tools as pm
#    pm.ccx.cstate_limits(1,0)
#elif 'MTL' in project:
#    sys.path.append(r"C:\mtl_dev")
#    from meteorlake_dev.pysvtools.pmext.pm_mtl import pm_tools as pm
#    pm.pkg.ccx.cstate_limits(1,0)
#sys.path.append(r'C:\gitlab_project\GIT\aggressive')#sys.path.append(r'C:\pythonsv\alderlake\users\limchink\aggressive')
import os
sys.path.append(os.path.dirname(__file__))
import user_input as user
import read_write as rdwr
import display_output as disp
import tracking as track
import export_log_file as dump
import badname_subfunc as badfunc
'''
Current disabled/pending features:
1. itp unlock and credential. (initial_setting)
2. aggressive import
'''

try:
    itp.unlockerflush()
except:
    print('Failed to itp.unlockerflush()!')
try:
    itp.entercredentials()
except:
    print('Failed to enter credential!')

AVAIL_FUNCS = {
'theory' : 'To display the validation algorithms of AggressiVE in term of attributes.',
'badname_regs' :  'To display all the unacceptable name of Dies/IPs/Regs/Fields exist in input_reg.',
'invalidate' : 'To display all the fields which have the information of attribute.',
'attr_all' : 'To display the number of fields we have with the specific attributes.',
'aggressive' : 'Main function of AggressiVE. (Require the initial declaration from user if automatable.)',
'log' : 'To display logs that AgressiVE may generate.',
'set_access_method' : 'To set and check for the access method',
'reg_track' : 'To display the number of fields that is validatable in every IPs under input_reg.'
}
def list_all_cmd():
    headers = ['Available Functions','Description']
    table = []
    for func in AVAIL_FUNCS.keys():
        table+=[{'Available Functions':func,'Description':AVAIL_FUNCS[func]}]
    x = Table.fromDictList(table,headers)
    print(x.getTableText())
	
def log():
    headers = ['Logs Path','Descriptions','Delete for']
    table = []
    x = []    
    for title,path in Logs.PATH.items():
        table += [{'Logs Path':path,'Descriptions':Logs.DESC[title],'Delete for':Logs.AR[title]}]
    x = Table.fromDictList(table,headers)
    print(x.getTableText())

def my_test():
    temp = eval("hub.hub_fusehip.intel_hvm_idx_top_cfg_seq[100]")
    n = 0
    print(temp)
    for i in temp:
        print(f"{n}: {i}")
        n += 1

class Pre_test:
    def _rmv_validated_fields(chosen_attr_fields, validated_fields):
        for valed_field in validated_fields:
            chosen_attr_fields.remove(valed_field)
        return chosen_attr_fields

    def _detect_fid_subcomps(comp):
        nextstage_comps = []
        comps_with_fid = eval(comp)
        num_of_comps_w_fid = len(comps_with_fid)
        if num_of_comps_w_fid <= 1: # for those subcom without fid
            print(f"{comp} has no fid. Will skip it.")
            return []
        # for those subcom with fid
        add_num = 0
        for i in range(num_of_comps_w_fid):
            while True:
                try:
                    comps_with_fid = eval(f"{comp}['fid_{str(i+add_num)}']")
                    nextstage_comps.append(f"{comp}['fid_{str(i+add_num)}']")
                except LookupError:
                    try:
                        comps_with_fid = eval(f"{comp}[{str(i+add_num)}]")
                        nextstage_comps.append(f"{comp}[{str(i+add_num)}]")
                    except:
                        add_num += 1
                        continue
                except Exception:
                    comps_with_fid = eval(f"{comp}['fid_{str(i+add_num)}']")
                    nextstage_comps.append(f"{comp}['fid_{str(i+add_num)}']")
                    add_num += 1
                    if add_num >= 100:
                        print("Something is wrong due to Infinite Loop! Please Force to Stop!!!")
                    continue
                break
        return nextstage_comps
    
    def _show_subcomponents(firstlvl_comps, unfinalized_subcom):
        subcomps = []
        nextstage_comps = []
        for firstlvl_comp in firstlvl_comps:
            nextstage_comps = eval(f"{firstlvl_comp}.search('')")
            if nextstage_comps == []:
                nextstage_comps = Pre_test._detect_fid_subcomps(firstlvl_comp)
                unfinalized_subcom = []
            else:
                nextstage_comps = list(map(lambda item: firstlvl_comp + "." + item, nextstage_comps))
            subcomps += nextstage_comps
        return subcomps, unfinalized_subcom
        
    def _read_subcomponents(subcomponents):
        messages = []
        for subcomponent in tqdm(subcomponents):
            try:# for digit & still subcomponent
                message = str(eval(subcomponent))
            except Exception as e:# for not accessible
                error_message = str(e).split('(')[0]
                messages.append(error_message)
                continue
            #categorize the output message for digit and subcom.
            if message[:2] == "0x":
                messages.append("Accessible")
            else:
                messages.append("IsSubcomponent")
        return messages
            
    def _categorize_subcomponents(subcomponents, messages, final_data):
        [finalized_subcom, unfinalized_subcom, finalized_msgs] = final_data
        loop = 0
        for msg in messages:
            if msg != "IsSubcomponent":
                finalized_subcom.append(subcomponents[loop])
                finalized_msgs.append(msg)
                if subcomponents[loop] in unfinalized_subcom:
                    unfinalized_subcom.remove(subcomponents[loop])
            else:
                unfinalized_subcom.append(subcomponents[loop])
            loop += 1
        print(f"Detected {len(finalized_subcom)} finalized_subcom & {len(unfinalized_subcom)} unfinalized_subcom")
        return finalized_subcom, unfinalized_subcom, finalized_msgs

    def _get_and_read_subcomponents(dielet): # need to check. # didnt finish
        subcomponents = []
        finalized_subcom, unfinalized_subcom, finalized_msgs = [], [], []
        loop = 1
        while True:
            print(f"({loop})Executing Step1/3 [_show_subcomponents()]...")
            if subcomponents == []:
                (subcomponents, unfinalized_subcom) = Pre_test._show_subcomponents([dielet], unfinalized_subcom)
            else:
                (subcomponents, unfinalized_subcom) = Pre_test._show_subcomponents(unfinalized_subcom, unfinalized_subcom)
            print(f"({loop})Executing Step2/3 [_read_subcomponents()]...")
            messages = Pre_test._read_subcomponents(subcomponents)
            print(f"({loop})Executing Step3/3 [_categorize_subcomponents()]...")
            (finalized_subcom, unfinalized_subcom, finalized_msgs) = Pre_test._categorize_subcomponents(subcomponents, messages, [finalized_subcom, unfinalized_subcom, finalized_msgs])
            if unfinalized_subcom == []:
                return finalized_subcom, finalized_msgs
            loop += 1
        
    def _filter_subcomponent_data(subcomponents, messages_shown): # done!
        not_acc_subcoms, not_acc_messages_shown, acc_subcoms = [], [], []
        loop = 0
        for message in messages_shown:
            if isinstance(message, str):
                if message == "Accessible":
                    acc_subcoms.append(subcomponents[loop])
                elif any(char.isalpha() for char in message): # if the message is inaccessible
                    not_acc_subcoms.append(subcomponents[loop])
                    not_acc_messages_shown.append(message)
            else: # if it is digit value in int # this statement is bogus #have this here just in case.
                acc_subcoms.append(subcomponents[loop])
            loop += 1
        return acc_subcoms, not_acc_subcoms, not_acc_messages_shown
        
    def _convert_acc_subcoms_list2table(subcoms_in_list): # done!
        headers = ["Subcomponents"]
        table = []
        for subcom in subcoms_in_list:
            table += [{"Subcomponents": subcom}]
        x = Table.fromDictList(table,headers)
        return x.getTableText()
            
    def _manage_and_dump_accessibility_data(data): # done!
        sclg = dump.export_acessibility("open", "NA", "")
        for dielet, no_acc_info_in_dict in data.items():
            sclg = dump.export_acessibility("store", f"{dielet}:", sclg)
            if no_acc_info_in_dict == {}:
                sclg = dump.export_acessibility("store", f"No Inaccessible subcomponent.", sclg)
                continue
            for no_acc_msg, subcoms_in_list in no_acc_info_in_dict.items():
                sclg = dump.export_acessibility("store", f"Message: {no_acc_msg}", sclg)
                #convert subcoms name in list to table
                subcom_in_table = Pre_test._convert_acc_subcoms_list2table(subcoms_in_list)
                sclg = dump.export_acessibility("store", subcom_in_table, sclg)
        sclg = dump.export_acessibility("close", "NA", sclg)
    
    def _dump_badname_reg(badname_registers):
        blg = dump.export_badname_regs('open','','')
        print('Storing unacceptable name registers to bad_name_regs.log...')
        for badname_register in badname_registers:
            try:
                blg = dump.export_badname_regs('store',badname_register,blg)
            except:
                print(f'Special Symbols in the name which cannot be recorded in log file: {badname_register}')
        blg = dump.export_badname_regs('close','',blg)
    
    def convert_str2list(string):
        try:
            list = string.split(',')#make one input (str) into list.
        except:
            list = string
            pass
        return list

    def _generate_invalidate(attr_fields,no_attr_fields):
        print('Generating the attr IPs...')
        attr_ips = track.fields_2_ips(attr_fields)
        print('Generating the no attr IPs...')
        no_attr_ips = track.fields_2_ips(no_attr_fields)
        #Convert all info to table form.
        print('Generating a table of information...')
        table_invip = disp.store('Name of IPs','No_Attr_IP',no_attr_ips)
        table_vip = disp.store('Name of IPs','Attr_IP',attr_ips)
        table_invf = disp.store('Name of IPs','No_Attr_Field',no_attr_fields)
        table_vf = disp.store('Name of IPs','Attr_Field',attr_fields)
        return table_invip,table_vip,table_invf,table_vf,attr_ips,no_attr_ips
    
    def _dump_invalidate(total,table_invip,table_invf,table_vip,table_vf,invf,vf):
        (invf,vf) = dump.export_invalidate('store_invalid',f'Number of invalid IPs: {total[0]}',invf,vf)
        (invf,vf) = dump.export_invalidate('store_valid',f'Number of valid IPs: {total[1]}',invf,vf)
        (invf,vf) = dump.export_invalidate('store_invalid',f'Number of invalid fields: {total[2]}',invf,vf)
        (invf,vf) = dump.export_invalidate('store_valid',f'Number of invalid fields: {total[3]}',invf,vf)
        (invf,vf) = dump.export_invalidate('store_invalid',table_invip,invf,vf)
        (invf,vf) = dump.export_invalidate('store_invalid',table_invf,invf,vf)
        (invf,vf) = dump.export_invalidate('store_valid',table_vip,invf,vf)
        (invf,vf) = dump.export_invalidate('store_valid',table_vf,invf,vf)
        (invf,vf) = dump.export_invalidate('close','',invf,vf)
        
    def _get_fields(input_reg):
        print(f'Getting information from {input_reg} ...')
        print('Detecting and storing all the fields information...')
        fields = []
        registers_1stsearch = eval(input_reg+".search('')")
        for register1 in tqdm(registers_1stsearch):
            try:
                registers_2ndsearch = eval(input_reg+"."+register1+".search('')")
                if registers_2ndsearch == []:
                    fields.append(input_reg+'.'+register1)
                else:
                    for register2 in registers_2ndsearch:
                        try:
                            registers_3rdsearch = eval(input_reg+"."+register1+"."+register2+".search('')")
                            if registers_3rdsearch == []:
                                fields.append(input_reg+'.'+register1+'.'+register2)
                            else:
                                print(f'{input_reg+"."+register1+"."+register2} has more fields.')
                        except:
                            pass
            except:
                pass
        return fields
        
    def _get_valid_fields(fields):
        print('Detecting the with attr fields...')
        attr_fields = []
        for field in tqdm(fields):
            try:
                eval(field)
            except:
                pass
            try:
                eval(field+'.info["attribute"]')
                attr_fields.append(field)
            except:
                pass
        return attr_fields
    
    def _get_attr_num(fields):
        attr_fields = Pre_test._get_valid_fields(fields)
        print('Detecting and Categorizing attributes information...')
        avai_attrs = []
        num_avai_attr = []
        for attr_field in tqdm(attr_fields):
            attr = eval(attr_field+'.info["attribute"]')
            if attr not in avai_attrs:
                avai_attrs.append(attr)
                num_avai_attr.append(1)
            else:
                pointer = avai_attrs.index(attr)
                num_avai_attr[pointer] += 1
        return attr_fields,avai_attrs,num_avai_attr
     
    def _adjust_prerd_num(chosen_attr, detections):
        if chosen_attr in ['ro/swc','na','ro/c']:
            detections[-1] = 2
            print(f"Detected validation attribute contain {chosen_attr}. Proceed with 2 pre_rd.")
        return detections
        
    def _comb_same_attr(avai_attrs,num_avai_attr):
        new_attrs = [] 
        new_num = []
        i=0
        for an_attr in avai_attrs:
            group = track.Pre_test.track_attr_cat(an_attr)#ensure current attr need to combine.[]=cant combine.
            if group != [] and new_attrs != []:#can combine but not first detected attr.
                for new_attr in new_attrs:
                    if new_attr in group:
                        index2add = new_attrs.index(new_attr)
                        new_num[index2add] += num_avai_attr[i]
                        break
                    elif new_attrs.index(new_attr) == len(new_attrs)-1:
                        new_attrs.append(group[0])
                        new_num.append(num_avai_attr[i])
                        break
            else:
                if group != []:#can combine and first detected
                    new_attrs.append(group[0])
                    new_num.append(num_avai_attr[i])
                else:#cant combine (first and not first detected)
                    new_attrs.append(an_attr)
                    new_num.append(num_avai_attr[i])
            i += 1
        return new_attrs,new_num
        
    def fully_halt():
        itp.halt()
        print('It is halted!')
        cont = True
        while cont == True:
            try:
                itp.threads[15]
                cont = False
            except:
                print('Some of the threads are not awake!/nReconnect the pysv!')
                itp.reconnect()
                refresh()
                itp.unlock()
        print('All the threads are fully awake.')
        itp.halt()
        print('It is halted!')
        
    def initial_setting():
        refresh()
        itp.unlock()
        #time.sleep(20)
        #try:
        #    cdie.fuses.load_fuse_ram
        #    soc.south.fuses.load_fuse_ram
        #except:
        #    cpu.fuses.load_fuse_ram()
        #else:
        #    print('Not able to do load_fuse_ram!')
        #    pass
        #sv.socket0.target_info["tap2sb_timeout"]=5*60
        #sv.pch0.target_info["p2sb_timeout"]=5*60 #does not support pch0 in MTL project.
        #Pre_test.fully_halt()  		
        
    def export_pre_test_msg(log_store):
        alg,flg = '',''
        (alg,flg) = dump.export('pre_open','NA',alg,flg)
        for one_line_msg in log_store:
            (alg,flg) = dump.export('store',one_line_msg,alg,flg)
        (alg,flg) = dump.export('close_all','NA',alg,flg)
        (alg,flg) = dump.export('close_fail','NA',alg,flg)
		
    def find_lockreg(attr_fields,chosen_attr):
        lockbit_regs=[]
        lockattr_regs=[]
        for attr_field in attr_fields:
            attr = eval(f"{attr_field}.info['attribute']")
            if attr in ["rw/p/l", "rw/v/l", "rw/v/p/l", "rw/l"]:
                lockattr_regs.append(attr_field)
                try:
                    lockbit_name = eval(f"{attr_field}.info['LockKeyField'].lower()")
                except:
                    lockbit_name = None
                    lockbit_reg = None
                if lockbit_name != None:
                    temp_lockbit_reg = attr_field.split('.')
                    temp_lockbit_reg = temp_lockbit_reg[:-2]
                    temp_lockbit_reg = '.'.join(temp_lockbit_reg)
                    lockbit_reg = temp_lockbit_reg + '.' + lockbit_name
                lockbit_regs.append(lockbit_reg)
                lockattr_regs.append(attr_field)
        return lockbit_regs,lockattr_regs
                
    def feature_lock(attr_fields,chosen_attr):#wip
        lockbit_regs = []
        if isinstance(chosen_attr,list):
            (lockbit_regs,lockattr_regs) = Pre_test.find_lockreg(attr_fields,chosen_attr)
        elif isinstance(chosen_attr,str) and chosen_attr in ["rw/p/l", "rw/v/l", "rw/v/p/l", "rw/l"]:
            for field in attr_fields:
                try:
                    lockbit_name = eval(f"{field}.info['LockKeyField'].lower()")
                except:
                    lockbit_name = None
                    lockbit_reg = None
                if lockbit_name != None:
                    temp_lockbit_reg = field.split('.')
                    temp_lockbit_reg = temp_lockbit_reg[:-2]
                    temp_lockbit_reg = '.'.join(temp_lockbit_reg)
                    lockbit_reg = temp_lockbit_reg + '.' + lockbit_name
                lockbit_regs.append(lockbit_reg)
            lockattr_regs = attr_fields
        else:
            lockbit_regs=[]
            lockattr_regs=[]
        return lockbit_regs,lockattr_regs
        
    def _main(input_reg,auto_attr,auto_access):
        full_fields = badname_regs(input_reg,True)#detect for error regs and fields. Exclude them out from good regs and fields.
        (attr_fields,attr_ips) = invalidate(full_fields,True)#detect for invalid regs and fields without attribute info. Exclude them out.
        (log_store,chosen_access) = user.Pre_test.access_choice(input_reg,auto_access,True)#display available access method and choose access method.(only for ip)
        log_store = track.feedback_access_method(chosen_access,attr_ips,log_store)
        chosen_attr = user.Pre_test.attr_choice([],auto_attr)#choose the one for validation.('r/w' or '')
        Pre_test.export_pre_test_msg(log_store)#store access method info in 'AggressiVE.log'.
        (lockbit_regs,lockattr_regs) = Pre_test.feature_lock(attr_fields,chosen_attr)
        
        return attr_fields,chosen_attr,[lockbit_regs,lockattr_regs]

class Post_test:
    def _fail_main(fail_infos,alg,flg,detections,num_val_seq,locklists,auto):
        [Fail,fail_regs,fail_x] = fail_infos
        if Fail > 0 :
            chosen_fail_val = 1
            while chosen_fail_val == 1:
                chosen_fail_val = user.Post_test.fail_val_choice(auto)#choose the way to deal with fail fields.
                if chosen_fail_val == 2:
                    (alg,flg) = dump.export('store','Fail Registers Re-write is chosen!',alg,flg)
                    (alg,flg) = dump.export('store_fail','Fail Registers Re-write is chosen!',alg,flg)
                    (alg,flg) = rdwr.Post_test.validate2_fail_regs(fail_regs,alg,flg,Fail,auto,detections,num_val_seq,locklists)#2nd validation for fail fields(re-write)
                elif chosen_fail_val == 1:
                    disp.disp_fail_content(fail_x,alg,flg)#re-print fail fields
                    print('Fail:'+str(Fail))
        return alg,flg

class Algorithm:
    DESC = {
    'ro':'read-only',
    'wo':'write-only',
    'r/w':'read-write',
    'rw/s':'read-write set',
    'rw/l':'read-write lock',
    'rw/o':'read-write once',
    'rw/1c':'read-write (write 1 will clear)',
    'rw/1l':'read-write (write 1 will lock)',
    'rw/1s':'read-write (write 1 will set)',
    'r/wc':'read-write clear',
    'ro/swc':'read returns 0,subsequent reads return 1,write 1 clears, write 0 has no effect',
    'rsv':'reserved (rd and wr masks are disabled)',
    'ro/c':'read-only clear',
    'rw/cr':'read-write cleared by read',
    'wo/1':'write once without read',
    'wo/c':'write only, write will clear',
    'na':'no access. read and write masks are disabled',
    'rw0c_fw':'read-write 0 cleared by FW',
    'rw1c_fw':'read-write 1 cleared by FW',
    'double buffered':'-',
    'r/w hardware clear':'read-write cleared by HW',
    'read/32 bit write only':'read and can only write in 32bit',
    'r/w firmware only':'read-write by FW only',
    'rw/v/p':'Read-Write , Variant , HW loadable, Cleared with Power-good reset only',
    'rw/v/l':'Read-Write Variable Lock',
    'rw/v/p/l':'Read-Write variant with lock, sticky',
    'ro/v/p':'Read-Only, Variant, Sticky',
    'rw/1c/p':'Read-Write 1 to Clear Sticky (set by HW, cleared by FW)',
    'rw/1c/v':'Read-Write 1 to Clear with HW loadable',
    'rw/1c/v/p':'read, write 1 to clear, HW loadable, sticky',
    'rw/1s/v':'Read-Write 1 to Set wirh HW loadable',
    'rw/1s/v/l':'Read-Write 1 to Set with HW loadable, Lock',
    'rw/o/p':'Read-Write Once Sticky',
    'rw/o/v/l':'Read-Write Once Variant with Lock',
    'rw/v':'Read-Write , Variant , hardware loadable',
    'rw/v2':'Read-Write Variable Lock by software',
    'ro/c/v':'-',
    'ro/p':'Read only and Sticky , same as RO but will only reset on PowerGood reset.',
    'rw/p':'Read-Write Sticky. Functions as RW. Cleared with Power-good reset only.',
    'ro/v':'Read Only Variant. Variant refer to hardware updated registers and RAL will not predict and ignore checking for variant fields',
    'rw/0c/v':'Read-Write 0 to Clear, Variant',
    'rw/p/l':'Read-Write Sticky Lock',
    'rw/fuse':'Read-Write Fuse',
    'rw/strap':'Read-Write Strap',
    'rw/ac':'Read/Write Auto Clear.Field is RW,but HW may clear the field without intervention',
    'dc':'-',
    'rw/l/k':'-',
    'rw/s/l':'-'
    }

    STATUS = {
    'ro':'Ready',
    'wo':'Ready',
    'r/w':'Ready',
    'rw/s':'Ready',
    'rw/l':'Ready',
    'rw/o':'Ready',
    'rw/1c':'Ready',
    'rw/1l':'Ready',
    'rw/1s':'Ready',
    'r/wc':'Ready',
    'ro/swc':'Ready',
    'rsv':'Ready',
    'ro/c':'Ready',
    'rw/cr':'Ready',
    'wo/1':'Ready',
    'wo/c':'Ready',
    'na':'Ready',
    'rw0c_fw':'Ready',
    'rw1c_fw':'Ready',
    'double buffered':'Ready',
    'r/w hardware clear':'Ready',
    'read/32 bit write only':'Ready',
    'r/w firmware only':'Ready',
    'rw/v/p':'Ready',
    'rw/v/l':'Ready',
    'rw/v/p/l':'Ready',
    'ro/v/p':'Ready',
    'rw/1c/p':'Ready',
    'rw/1c/v':'Ready',
    'rw/1c/v/p':'Ready',
    'rw/1s/v':'Ready',
    'rw/1s/v/l':'Ready',
    'rw/ac':'Undefined',
    'rw/o/p':'Ready',
    'rw/o/v/l':'Ready',
    'rw/p/l':'Ready',
    'rw/fuse':'Undefined',
    'rw/strap':'Undefined',
    'dc':'Undefined',
    'ro/c/v':'Ready',
    'ro/p':'Ready',
    'ro/v':'Ready',
    'rw/0c/v':'Ready',
    'rw/l/k':'Undefined',
    'rw/p':'Ready',
    'rw/s/l':'Undefined',
    'rw/v':'Ready',
    'rw/v2':'Ready'
    }

    ALGORITHM = {
    'ro':['0/1','0/1','10','pre_rd','01','pre_rd','10','pre_rd'], # Done!
    'wo':['0/1','0/1','10','pre_rd','01','pre_rd','10','pre_rd'], # Done!
    'r/w':['0/1','0/1','10','10','01','01','10','10'], # Done!
    'rw/s':['0/1','0/1','10','1(pre_rd/non-zero)','01','11','10','11'], # Done!
    'rw/l':['0/1','0/1','10','1(pre_rd/non-zero)','01','11','10','11'], # Done!
    'rw/o':['0/1','0/1','10','10','01','10','10','10'], # Done!
    'rw/1c':['0/1','0/1','10','0(pre_rd/1)','01','00','10','00'], # Done!
    'rw/1l':['0/1','0/1','10','1(pre_rd/non-zero)','01','11','10','11'], # Done!
    'rw/1s':['0/1','0/1','10','1(pre_rd/non-zero)','01','11','10','11'], # Done!
    'r/wc':['0/1','0/1','10','0(pre_rd/1)','01','00','10','00'], # Done!
    'ro/swc':['0','1','10','1strd=10;2ndrd=10','01','1strd=01;2ndrd=01','10','1strd=10;2ndrd=10'], # Done!
    'rsv':['0/1','0/1','10','pre_rd','01','pre_rd','10','pre_rd'], # Done!
    'ro/c':['0','0','10','00','01','00','10','00'], # Done!
    'rw/cr':['1/0','1/0','10','1strd=10;2ndrd=00','01','1strd=01;2ndrd=00','10','1strd=10;2ndrd=00'], # Done!
    'wo/1':['1/0','1/0','10','00','01','00','10','00'], # Done!
    'wo/c':['1/0','1/0','10','00','01','00','10','00'], # Done!
    'na':['00','00','10','00','01','00','10','00'], # Done!
    'rw0c_fw':['1/0','1/0','10','10','01','01','10','10'], # Done!
    'rw1c_fw':['1/0','1/0','10','10','01','01','10','10'], # Done!
    'double buffered':['1/0','1/0','10','10','01','01','10','10'], # Done!
    'r/w hardware clear':['1/0','1/0','10','10','01','01','10','10'], # Done!
    'read/32 bit write only':['1/0','1/0','10','10','01','01','10','10'], # Done!
    'r/w firmware only':['1/0','1/0','10','10','01','01','10','10'], # Done!
    'rw/v/p':['1/0','1/0','10','10','01','01','10','10'], # Done!
    'rw/v/l':['0/1','0/1','10','1(pre_rd/non-zero)','01','11','10','11'], # Done!
    'rw/v/p/l':['0/1','0/1','10','1(pre_rd/non-zero)','01','11','10','11'], # Done!
    'ro/v/p':['0/1','0/1','10','pre_rd','01','pre_rd','10','pre_rd'], # Done!
    'rw/1c/p':['0/1','0/1','10','0(pre_rd/1)','01','00','10','00'], # Done!
    'rw/1c/v':['0/1','0/1','10','0(pre_rd/1)','01','00','10','00'], # Done!
    'rw/1c/v/p':['0/1','0/1','10','0(pre_rd/1)','01','00','10','00'], # Done!
    'rw/1s/v':['0/1','0/1','10','0(pre_rd/1)','01','00','10','00'], # Done!
    'rw/1s/v/l':['0/1','0/1','10','0(pre_rd/1)','01','00','10','00'], # Done!
    'rw/ac':['0/1','0/1','10','pre_rd','01','pre_rd','10','pre_rd'], # Done!
    'rw/o/p':['0/1','0/1','10','case1=10;case2=pre_rd','01','01','10','case1=10;case2=pre_rd'], # Done!
    'rw/o/v/l':['0/1','0/1','10','case1=10;case2=pre_rd','01','01','10','case1=10;case2=pre_rd'], # Done!
    'rw/p/l':['0/1','0/1','10','1(pre_rd/non-zero)','01','11','10','11'], # Done!
    'rw/fuse':['0/1','0/1','10','pre_rd','01','pre_rd','10','pre_rd'], # Done!
    'rw/strap':['0/1','0/1','10','pre_rd','01','pre_rd','10','pre_rd'], # Done!
    'dc':['0/1','0/1','10','pre_rd','01','pre_rd','10','pre_rd'], # Done!
    'ro/c/v':['0','0','10','00','01','00','10','00'], # Done!
    'ro/p':['0/1','0/1','10','pre_rd','01','pre_rd','10','pre_rd'], # Done!
    'ro/v':['0/1','0/1','10','pre_rd','01','pre_rd','10','pre_rd'], # Done!
    'rw/0c/v':['0/1','0/1','10','10','01','00','10','00'], # Done!
    'rw/l/k':['NA','NA','NA','NA','NA','NA','NA','NA'], # Done!
    'rw/p':['0/1','0/1','10','10','01','01','10','10'], # Done!
    'rw/s/l':['NA','NA','NA','NA','NA','NA','NA','NA'], # Done!
    'rw/v':['0/1','0/1','10','10','01','01','10','10'], # Done!
    'rw/v2':['0/1','0/1','10','10','01','01','10','10'] # Done!
    }

class Logs:
    PATH = {
    'wout_attr_fields' : 'C>>Users>>pgsvlab>>PythonSv>>Aggressive_logs>>no_attr_fields.log',
    'with_attr_fields' : 'C>>Users>>pgsvlab>>PythonSv>>Aggressive_logs>>attr_fields.log',
    'bad_name_regs' : 'C>>Users>>pgsvlab>>PythonSv>>Aggressive_logs>>bad_name_regs.log',
    'AggressiVE' : 'C>>Users>>pgsvlab>>PythonSv>>Aggressive_logs>>AggressiVE.log',
    'AggressiVE_fail' : 'C>>Users>>pgsvlab>>PythonSv>>Aggressive_logs>>AggressiVE_fail.log',
    'AggressiVE_error' : 'C>>Users>>pgsvlab>>PythonSv>>Aggressive_logs>>AggressiVE_error.log',
    'AggressiVE_hang' : 'C>>Users>>pgsvlab>>PythonSv>>Aggressive_logs>>AggressiVE_hang.log',
    'attr_all' : 'C>>Users>>pgsvlab>>PythonSv>>Aggressive_logs>>attr_all.log',
    'pass_regs' : 'C>>Users>>pgsvlab>>PythonSv>>Aggressive_logs>>pass_regs.log',
    'fail_regs' : 'C>>Users>>pgsvlab>>PythonSv>>Aggressive_logs>>fail_regs.log',
    'error_regs' : 'C>>Users>>pgsvlab>>PythonSv>>Aggressive_logs>>error_regs.log',
    'sus_hang_regs' : 'C>>Users>>pgsvlab>>PythonSv>>Aggressive_logs>>sus_hang_regs.log',
    'hang_regs' : 'C>>Users>>pgsvlab>>PythonSv>>Aggressive_logs>>hang_regs.log',
    'AggressiVE_badname' : 'C>>Users>>pgsvlab>>PythonSv>>Aggressive_logs>>AggressiVE_badname.log',
    'regtrack' : 'C>>Users>>pgsvlab>>PythonSv>>Aggressive_logs>>regtrack.log'
	}
    DESC = {
    'wout_attr_fields' : "Fields that don't have attribute information.",
    'with_attr_fields' : "Fields that have attribute information.",
    'bad_name_regs' : "Registers that have naming issue.",
    'AggressiVE' : "All the information when running aggressive().",
    'AggressiVE_fail' : "All the fail validation information when running aggressive().",
    'AggressiVE_error' : "All the error validation information when running aggressive().",
    'AggressiVE_hang' : 'All the hang validation information when running aggressive().',
    'attr_all' : "List of available attributes.",
    'pass_regs' : "List of passing registers.",
    'fail_regs' : "List of failing registers.",
    'error_regs' : 'List of registers that are not able to read and write and show error message.',
    'sus_hang_regs' : 'List of registers that might caused the system hang.',
    'hang_regs' : 'List of registers that caused the system hang.',
    'AggressiVE_badname' : 'All the information when validating unacceptable name regs by running aggressive_badname().',
    'regtrack' : 'List the number of validatable fields for every IPs under input_reg.'
	}
    AR = {
    'wout_attr_fields' : 'NA',
    'with_attr_fields' : 'NA',
    'bad_name_regs' : 'NA',
    'AggressiVE' : 'aggressive()',
    'AggressiVE_fail' : 'aggressive()',
    'AggressiVE_error' : 'aggressive()',
    'AggressiVE_hang' : 'aggressive()',
    'attr_all' : 'NA',
    'pass_regs' : 'NA',
    'fail_regs' : 'aggressive()',
    'error_regs' : 'aggressive()',
    'sus_hang_regs' : 'NA',
    'hang_regs' : 'aggressive()',
    'AggressiVE_badname' : 'NA',
    'regtrack' : 'reg_track()'
    }

class Exec:
    def check_attribute(badname_regs):#wip...#for aggressive_badname()
        for badname_reg in badname_regs:
            pass
        return attr_badname_regs, their_attr

def theory():
    '''
    Command:
        theory()

    Details:
        Displaying the algorithms that AggressiVE used for all the attributes (The value that it'll write and the expected value that it'll get).

    Inputs:
        None.

    Outputs:
        Table with the algorithms that AggressiVE used for all the attributes.

    EX:
        >>> theory()
    '''
    print('System will not be halted before/during/after all the validation!')
    headers = ['Attrs','Descriptions','Status','Pre_Rd1','Pre_Rd2','WR1','RD1','WR2','RD2','WR3','RD3']
    table = []
    x = []    
    for attr in Algorithm.DESC.keys():
        table += [{'Attrs':attr,'Descriptions':Algorithm.DESC[attr],'Status':Algorithm.STATUS[attr],'Pre_Rd1':Algorithm.ALGORITHM[attr][0],'Pre_Rd2':Algorithm.ALGORITHM[attr][1],'WR1':Algorithm.ALGORITHM[attr][2],'RD1':Algorithm.ALGORITHM[attr][3],'WR2':Algorithm.ALGORITHM[attr][4],'RD2':Algorithm.ALGORITHM[attr][5],'WR3':Algorithm.ALGORITHM[attr][6],'RD3':Algorithm.ALGORITHM[attr][7]}] 
    x = Table.fromDictList(table,headers)
    print(x.getTableText())
    print('''
Other Features:
Halt - Some registers will halt the system when read/write. It will still mark as 'pass' if the behavior is correct and continue validating.
System Reset - Some registers will restart the system when read/write. It will mark as 'fail' but it will still continue validating.
Hang - Some registers will make the system hang. It will mark as 'fail' and stop the validation. It will ask for doing 2nd validation for the last 10 registers and do machine check 1by1.
    ''')
    
def set_access_method(input_reg):
    '''
    Command:
        set_access_method()

    Details:
        Set new access method and read all the current access method of IPs using under the input_reg.

    Inputs:
        input_regs = Name of die/ Name of IP. [Not recommended since not able to re-set access method] Name of reg/ Name of field

    Outputs:
        Successfulness of setting access method to all IPs under input_reg.
        Log File: AggressiVE.log

    EX:
        >>> set_access_method('cdie')
        >>> set_access_method('soc')
        >>> set_access_method('gcd')
        >>> set_access_method('ioe')
        >>> set_access_method('cdie.taps')
        >>> set_access_method('cdie.taps.core2_corepma')
    '''
    (log_store,chosen_access) = user.Pre_test.access_choice(input_reg,'None',False)#display available access method and choose access method.(only for ip)
    full_fields = badname_regs(input_reg,True)#detect for error regs and fields. Exclude them out from good regs and fields.
    (attr_fields,attr_ips) = invalidate(full_fields,True)#detect for invalid regs and fields without attribute info. Exclude them out.
    log_store = track.feedback_access_method(chosen_access,attr_ips,log_store)
    
def badname_regs(input_reg,validate=False):#Completed(die,IP, and register)
    '''
    Command:
        badname_regs()

    Details:
        Displaying all the error Dies/IPs/Regs/Fields exist in input_reg.
        Error Die/IP/Reg = The Die/IP/Reg with the unacceptable name which contains unacceptable symbol and number.

    Inputs:
        input_regs = Name of die/ Name of IP/ Name of reg/ Name of field
        in_reg = To check in register level?
        in_field = To check in field level (deepest level)?

    Outputs:
        Name of error IPs/regs/fields.
        Log File: bad_name_regs.log

    EX:
        >>> badname_regs('cdie')
        >>> badname_regs('cdie',validate=True)
        >>> badname_regs('cdie.taps.core2_corepma')
    '''
    (badname_registers,attr_fields) = badfunc.Pre_test.track_badname_regs(input_reg)
    Pre_test._dump_badname_reg(badname_registers)
    print(f"{Fore.LIGHTBLUE_EX}There's {len(badname_registers)} unacceptable name registers.")
    print('All the error registers names have been saved to C>>Users>>pgsvlab>>Documents>>PythonSv>>bad_name_regs.py.'+Fore.RESET)
    if validate == True:
        return attr_fields

def invalidate(input_reg,validate=False):#Completed(die,ip,fields)
    '''
    Command:
        invalidate()

    Details:
        Displaying all the fields which have the information of 'attribute'.

    Inputs:
        input_regs = Name of die/ Name of IP/ Name of reg/ Name of field

    Outputs:
        All the name of valid and invalid fields/IPs.
        Log Files: 
            - no_attr_fields.log
            - attr_fields.log

    EX:
        >>> invalidate('cdie')
        >>> invalidate('cdie.taps.core2_corepma')
    '''
    if validate == False:#for die and ip (user input)
        full_fields = badname_regs(input_reg,True)
    elif validate == True:
        full_fields = input_reg
    full_ips = track.fields_2_ips(full_fields)#search for all the IPs
    #detect the attribute info for attr_fields and no_attr_fields.
    (attr_fields,no_attr_fields) = track.track_invalidate_fields(full_fields)
    (table_invip,table_vip,table_invf,table_vf,attr_ips,no_attr_ips) = Pre_test._generate_invalidate(attr_fields,no_attr_fields)#generate valid and invalid ips.
    #Display result.
    total = disp.Pre_test.disp_invalidate(no_attr_ips,attr_ips,no_attr_fields,attr_fields)
    #detect total num of fields and IPs.
    print('Calculating total number of fields and IPs...')
    total_num_fields = len(full_fields)
    (invf,vf) = dump.export_invalidate('open','','','')
    (invf,vf) = dump.export_invalidate('store_invalid',f'Total num of fields: {total_num_fields}',invf,vf)
    (invf,vf) = dump.export_invalidate('store_valid',f'Total num of fields: {total_num_fields}',invf,vf)
    Pre_test._dump_invalidate(total,table_invip,table_invf,table_vip,table_vf,invf,vf)
    print('All the with attr fields & non attr fields names have been saved to:')
    print(Fore.LIGHTBLUE_EX + 'C>>Users>>pgsvlab>>Documents>>PythonSv>>no_attr_fields.log.')
    print('C>>Users>>pgsvlab>>Documents>>PythonSv>>attr_fields.log.' + Fore.RESET)
    if validate == True:
        return attr_fields,attr_ips
		
def reg_track(input_reg,validate=True):
    '''
    Command:
        reg_track()

    Details:
        Displaying the number (per IPs) of all the registers available and 'validatable' under the input_reg.

    Inputs:
        input_regs = Name of die/ Name of IP

    Outputs:
        Table with the number of registers in every IPs under the input_regs.
        Log File: regtrack.log

    EX:
        >>> input_reg('soc')
        >>> input_reg('cdie')
        >>> input_reg('ioe')
        >>> input_reg('gcd')
    '''
    input_reg = badname_regs(input_reg,validate)
    (attr_fields,attr_ips) = invalidate(input_reg,validate)
    numlist = []
    rt = dump.export_regtrack('open','','')
    for attr_ip in attr_ips:
        for attr_field in attr_fields:
            if attr_ip in attr_field:
                try:
                    numlist[attr_ips.index(attr_ip)] += 1
                except IndexError:
                    numlist.append(1)
        print(f"{attr_ip}= {str(numlist[attr_ips.index(attr_ip)])}")
        rt = dump.export_regtrack("store",f"{attr_ip}= {str(numlist[attr_ips.index(attr_ip)])}",rt)
    rt = dump.export_regtrack("close",'',rt)
        
def attr_all(input_regs,validate=False):#for die, ip, register, and fields
    '''
    Command:
        attr_all()

    Details:
        Displaying all the available attributes in input_regs

    Inputs:
        input_regs = Name of die/ Name of IP/ Name of reg/ Name of fields

    Outputs:
        Table with the all the available attributes and the numbers of fields in all the specific attributes.
        Log File: attr_all.log

    EX:
        >>> attr_all('soc')
        >>> attr_all('soc.north')
        >>> attr_all('soc.north.punit')
        >>> attr_all('soc.north.punit.punit_gpsb')
        >>> attr_all('soc.north.punit.punit_gpsb.punit_fsms')
        >>> attr_all('soc.north.punit.punit_gpsb.punit_fsms.sa_perf_status_0_0_0_mchbar_pcu')
        >>> attr_all('soc.north.punit.punit_gpsb.punit_fsms.sa_perf_status_0_0_0_mchbar_pcu.sa_voltage')
    '''
    #make the one string to list.
    if ',' not in str(input_regs):
        input_regs = input_regs.split(',')
    if len(input_regs) >= 5:
        fields_input_mode = True
    else:
        fields_input_mode = False
    headers = ['Num','Attributes','Num of fields','Algorithm']
    table = []
    x = []
    total_num_valid_fields = 0
    if fields_input_mode:
        #detect the attribute info for valid_fields.
        (attr_fields,avai_attrs,num_avai_attr) = Pre_test._get_attr_num(input_regs)
        #combine the attributes with same category into one.
        (new_attrs,new_num) = Pre_test._comb_same_attr(avai_attrs,num_avai_attr)
        #display all the attrs and num of fields.
        i = 0
        for new_attr in new_attrs:
            if new_attr == 'rw':
                new_attr = 'r/w'
            elif new_attr == 'rw/c':
                new_attr = 'r/wc'
            if new_attr in Algorithm.STATUS:
                algo = Algorithm.STATUS[new_attr]
            else:
                algo = 'Undefined'
            table += [{'Num':i+1,'Attributes':new_attr ,'Num of fields':new_num[i],'Algorithm':algo}]
            i+=1
        total_num_valid_fields = len(attr_fields)
    else:
        for input_reg in input_regs:
            fields = Pre_test._get_fields(input_reg)#search for all the fields
            #detect the attribute info for valid_fields.
            (attr_fields,avai_attrs,num_avai_attr) = Pre_test._get_attr_num(fields)
            #combine the attributes with same category into one.
            (new_attrs,new_num) = Pre_test._comb_same_attr(avai_attrs,num_avai_attr)
            #display all the attrs and num of fields.
            i = 0
            for new_attr in new_attrs:
                if new_attr == 'rw':
                    new_attr = 'r/w'
                elif new_attr == 'rw/c':
                    new_attr = 'r/wc'
                if new_attr in Algorithm.STATUS:
                    algo = Algorithm.STATUS[new_attr]
                else:
                    algo = 'Undefined'
                table += [{'Num':i+1,'Attributes':new_attr ,'Num of fields':new_num[i],'Algorithm':algo}]
                i+=1
            total_num_valid_fields += len(attr_fields)
    table += [{'Num':'-','Attributes':'Total num of fields' ,'Num of fields':total_num_valid_fields,'Algorithm':'-'}]
    x = Table.fromDictList(table,headers)
    print(x.getTableText())
    aa = dump.export_attr_all('open','','')
    aa = dump.export_attr_all('store',x.getTableText(),aa)
    aa = dump.export_attr_all('close','',aa)
    if validate == True:
        return new_attrs

def check_accessibility(dielets=[]):
    #get all dielets
    if dielets == []:
        dielets = socket.show() # assume will get in the form of list.
    #get their final level of subcomponents per dielet
    not_acc_data = {}
    acc_data = {}
    print("Checking for subcomponents' accessibility...")
    for dielet in dielets:
        print(f"Currently checking for {dielet}...")
        (subcomponents, messages_shown) = Pre_test._get_and_read_subcomponents(dielet) # this is the only one need to be checked!
        (acc_subcoms, not_acc_subcoms, not_acc_messages_shown) = Pre_test._filter_subcomponent_data(subcomponents, messages_shown)
        #store data in dict which separated by dielet
        not_acc_data[dielet] = {}
        acc_data[dielet] = {}
        loop = 0
        for subcoms in acc_subcoms:
            acc_data[dielet]["Accessible"] = []
            acc_data[dielet]["Accessible"].append(str(len(acc_subcoms)))
        for message in not_acc_messages_shown:
            if message not in not_acc_data[dielet]:
                not_acc_data[dielet][message] = []
            not_acc_data[dielet][message].append(not_acc_subcoms[loop])
            loop += 1
    #display & dump data
    disp.Pre_test.disp_accessibility(acc_data)
    disp.Pre_test.disp_inaccessibility(not_acc_data)
    Pre_test._manage_and_dump_accessibility_data(not_acc_data)

def aggressive(file = r'C:\AggressiVE_GITHUB\AggressiVE\input_parameters.xlsx'):
    '''
    Command:
        aggressive()

    Details:
        Validate the fields of all the chosen regs.
        Dependencies = access method and attr

    Inputs:
        file = path of input parameter excel file

    Outputs:
        Table with the information of validation.
        Log Files:
            - no_attr_fields.log [override]
            - attr_fields.log [override]
            - badname_regs.log [override]
            - attr_all.log [override]
            - AggressiVE.log [override]
            - AggressiVE_fail.log [override]
            - AggressiVE_pass.log [override]
            - AggressiVE_error.log [override]
            - AggressiVE_hang.log [override]
            - pass_regs.log [generate new log]
            - fail_regs.log [override]
            - error_regs.log [override]
            - sus_hang_regs.log [override]
            - hang_regs.log [override]

    EX:
        >>> aggressive('cdie')
        >>> aggressive('cdie.taps.core2_corepma')
    '''
    df = pd.read_excel(file,'aggressive')
    input_regs = df['input_regs'].values.tolist()
    auto_attr = df['auto_attr'].values.tolist()[0:30]
    auto_access = df['access_method'].values.tolist()[0]
    halt_detection = df['halt_detection'].values.tolist()[0]
    reset_detection = df['reset_detection'].values.tolist()[0]
    hang_detection = df['hang_detection'].values.tolist()[0]
    auto = df['auto'].values.tolist()[0]
    mca_check = df['mca_check'].values.tolist()[0]
    num_val_seq = df['num_val_seq'].values.tolist()[0]
    random = df['random'].values.tolist()[0]
    dfd_en = df['dfd_en'].values.tolist()[0]
    post_val = df['post_val'].values.tolist()[0]
    pre_rd_num = df['pre_rd'].values.tolist()[0]
    dump.goto_default_path()
    dump.create_log_folder()
    dump.goto_latest_log_folder()
    dump.create_tbc_folder()
    if dfd_en == False:
        halt_detection = reset_detection = hang_detection = False
    if len(auto_attr) == 1:
        auto_attr = auto_attr[0]
    #input parameters naming correction
    if mca_check not in ['every_failreg','every_10val',False]:
        print('Input Parameter mca_check can only be either "every_failreg" or "every_10val" or "False". Please changed!')
        return
    #nan input to None.
    auto_attr = "None" if str(auto_attr) == "nan" and not isinstance(auto_attr, list) else auto_attr
    auto_access = "None" if str(auto_access) == "nan" and not isinstance(auto_access, list) else auto_access
    #detect die availability
    avail_die = 0
    filtered_input_regs = []
    for input_reg in input_regs:
        try:
            eval('__main__.'+input_reg)
            avail_die += 1
            filtered_input_regs.append(input_reg)
        except:
            print(f'No {str(input_reg)} die exist in this project!')
            print('Will continue without it.')
    if avail_die == 0:
        print('There is no correct die to be validated.')
        print('Please enter the correct one!')
        return 
    #detection mode changed
    detections = [halt_detection,reset_detection,hang_detection,mca_check,post_val,pre_rd_num]
    #AggressiVE_error.log & AggressiVE_hang.log & AggressiVE_pass.log?
    if dfd_en:
        Pre_test.initial_setting()
    dump.export_tobecont_input_regs(filtered_input_regs)
    print(f"filtered_input_regs:{filtered_input_regs}")
    for input_reg in filtered_input_regs:
        (attr_fields,chosen_attr,locklists) = Pre_test._main(input_reg,auto_attr,auto_access)#run all pretest features.
        detections = Pre_test._adjust_prerd_num(chosen_attr, detections)
        dump.export_tobecont_config(dfd_en, auto, detections, num_val_seq, locklists, random, auto_access, auto_attr)
        status = rdwr.Exec.validate(attr_fields,chosen_attr,auto,detections,num_val_seq,random,locklists)#validation.
        print(f"input_reg:{input_reg}")
        dump.rmv_input_reg_from_log(input_reg)
        if status == 1:
            break
    if status == 0:
        dump.rmv_tobecont_folder()
    dump.print_log_location()
    dump.goto_default_path()
    
def aggressive_log(path=None, logname=None):
    if logname is None or path is None:
        print("Please Enter The Path of Your Log File and Log File Name")
    input_regs = dump._get_logregs(path, logname)#full_path_fields
    auto_attr, auto_access = "None", "None"
    halt_detection, reset_detection, hang_detection = False, False, False
    auto = True
    mca_check, random, dfd_en = False, False, False
    num_val_seq = 3
    post_val = False
    pre_rd_num = 2
    dump.goto_default_path()
    dump.create_log_folder()
    dump.goto_latest_log_folder()
    dump.create_tbc_folder()

    #detection mode changed
    detections = [halt_detection,reset_detection,hang_detection,mca_check,post_val,pre_rd_num]
    #AggressiVE_error.log & AggressiVE_hang.log & AggressiVE_pass.log?
    if dfd_en:
        Pre_test.initial_setting()
    dump.export_tobecont_input_regs(input_regs)
    #(attr_fields,chosen_attr,locklists) = Pre_test._main(input_reg,auto_attr,auto_access)#run all pretest features.
    attr_fields = input_regs
    chosen_attr = "None"
    (lockbit_regs,lockattr_regs) = Pre_test.feature_lock(attr_fields,[])
    locklists = [lockattr_regs, lockattr_regs]
    detections = Pre_test._adjust_prerd_num(chosen_attr, detections)
    dump.export_tobecont_config(dfd_en, auto, detections, num_val_seq, locklists, random, auto_access, auto_attr)

    status = rdwr.Exec.validate(attr_fields,chosen_attr,auto,detections,num_val_seq,random,locklists)#validation.
    if status == 0:
        #dump.rmv_input_reg_from_log(input_regs)
        dump.rmv_tobecont_folder()
    dump.print_log_location()
    dump.goto_default_path()

def aggressive_cont(file=None):
    if file == None:
        return "Please input the path of log folder."
    (chosen_attr_fields, validated_fields, unfinish_input_regs, dfd_en, auto, detections, num_val_seq, locklists, random, auto_access, auto_attr) = dump._find_and_get_tobecont_logfile(file)
    if all(arg == 'NA' for arg in [chosen_attr_fields, validated_fields, dfd_en, auto, detections, num_val_seq, locklists, random, auto_access, auto_attr]):
        return 1
    if dfd_en:
        Pre_test.initial_setting()
    remain_fields = Pre_test._rmv_validated_fields(chosen_attr_fields, validated_fields)
    status = rdwr.Exec.validate_cont(remain_fields,auto,detections,num_val_seq,locklists)
    if status == 1:
        return 1
    for input_reg in unfinish_input_regs:
        (attr_fields,chosen_attr,locklists) = Pre_test._main(input_reg,auto_attr,auto_access)#run all pretest features.
        detections = Pre_test._adjust_prerd_num(chosen_attr, detections)
        dump.export_tobecont_config(dfd_en, auto, detections, num_val_seq, locklists, random, auto_access, auto_attr)
        status = rdwr.Exec.validate(attr_fields,chosen_attr,auto,detections,num_val_seq,random,locklists)#validation.
        dump.rmv_input_reg_from_log(input_reg)
        if status == 1:
            break
    if status == 0:
        dump.rmv_tobecont_folder()
    dump.goto_default_path()

def aggressive_badname(file = r'C:\AggressiVE_GITHUB\AggressiVE\input_parameters.xlsx'):
    '''
    Command:
        aggressive_badname()

    Details:
        Validate the fields of all the unacceptable name regs.
        Dependencies = access method and attr

    Inputs:
        input_regs = Name of die/ Name of IP/ Name of reg.

    Outputs:
        Table with the information of bad_name regs validation.
        Log File:
            - AggressiVE_badname.log
            - no_attr_fields.log [override]
            - attr_fields.log [override]
            - attr_all.log [override]
            - pass_regs.log [generate new log]
            - fail_regs.log [override]
            - error_regs.log [override]
            - sus_hang_regs.log [override]
            - hang_regs.log [override]

    EX:
        >>> aggressive_badname('cdie')
        >>> aggressive_badname('cdie.taps.core2_corepma')
    '''
    df = pd.read_excel(file,'aggressive_badname')
    input_regs = df['input_regs'].values.tolist()[0]
    auto_attr = df['auto_attr'].values.tolist()[0]
    halt_detection = df['halt_detection'].values.tolist()[0]
    reset_detection = df['reset_detection'].values.tolist()[0]
    hang_detection = df['hang_detection'].values.tolist()[0]
    auto = df['auto'].values.tolist()[0]
    mca_check = df['mca_check'].values.tolist()[0]
    detections = [halt_detection,reset_detection,hang_detection,mca_check]
    (chosen_regs, filt_no_last_list, filt_last_level_list) = badfunc.Pre_test._main(input_regs)
    badfunc.Exec._main(chosen_regs, filt_no_last_list, filt_last_level_list, auto, detections)
    #2nd pass/fail/error/hang regs validation if possible. #dump
    #close dump.
    return
	 