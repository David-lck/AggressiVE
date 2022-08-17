import __main__
cdie = __main__.cdie if hasattr(__main__, 'cdie') else None
soc = __main__.soc if hasattr(__main__, 'soc') else None
cpu = __main__.pch if hasattr(__main__, 'cpu') else None
pch = __main__.pch if hasattr(__main__, 'pch') else None
itp = __main__.itp if hasattr(__main__, 'itp') else None
ioe = __main__.ioe if hasattr(__main__, 'ioe') else None
gcd = __main__.gcd if hasattr(__main__, 'gcd') else None
socket = __main__.socket if hasattr(__main__, 'socket') else None
refresh = __main__.refresh if hasattr(__main__, 'refresh') else None

from pysvtools.asciitable import AsciiTable as Table
import time
import colorama
from colorama import Fore
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

project = itp.threads.device.alias[0]
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
'''
Current disabled/pending features:
1. itp unlock and credential. (initial_setting)
2. aggressive import
'''

itp.unlockerflush()
itp.entercredentials()

AVAIL_FUNCS = {
'theory' : 'To display the validation algorithms of AggressiVE in term of attributes.',
'error_regs' :  'To display all the error Dies/IPs/Regs/Fields exist in input_reg which have the unacceptable name.',
'invalidate' : 'To display all the fields which have the information of attribute.',
'attr_all' : 'To display the number of fields we have with the specific attributes.',
'aggressive' : 'Main function of AggressiVE. (Require the initial declaration from user if automatable.)',
}
def list_all_cmd():
    headers = ['Available Functions','Description']
    table = []
    for func in AVAIL_FUNCS.keys():
        table+=[{'Available Functions':func,'Description':AVAIL_FUNCS[func]}]
    x = Table.fromDictList(table,headers)
    print(x.getTableText())

class Pre_test:
    def _dump_error_reg(error_registers):
        ilg = dump.export_invalid('open','','')
        #dump error regs to error_reg.log
        print('Storing error registers names to error_reg.log...')
        for error_register in error_registers:
            try:
                ilg = dump.export_invalid('store',error_register,ilg)
            except:
                print(f'Special Symbols in the name which cannot be recorded in log file: {error_register}')
        ilg = dump.export_invalid('close','',ilg)
    
    def convert_str2list(string):
        try:
            list = string.split(',')#make one input (str) into list.
        except:
            list = string
            pass
        return list

    def _generate_invalidate(valid_fields,invalid_fields):
        print('Generating the valid IPs...')
        valid_ips = track.fields_2_ips(valid_fields)
        print('Generating the invalid IPs...')
        invalid_ips = track.fields_2_ips(invalid_fields)
        #Convert all info to table form.
        print('Generating a table of information...')
        table_invip = disp.store('Name of IPs','Invalid_IP',invalid_ips)
        table_vip = disp.store('Name of IPs','Valid_IP',valid_ips)
        table_invf = disp.store('Name of IPs','Invalid_Field',invalid_fields)
        table_vf = disp.store('Name of IPs','Valid_Field',valid_fields)
        return table_invip,table_vip,table_invf,table_vf,valid_ips,invalid_ips
    
    def _dump_invalidate_ver3(total,table_invip,table_invf,table_vip,table_vf,invf,vf):
        (invf,vf) = dump.export_invalidate('store_invalid',f'Number of invalid IPs: {total[0]}',invf,vf)
        (invf,vf) = dump.export_invalidate('store_valid',f'Number of valid IPs: {total[1]}',invf,vf)
        (invf,vf) = dump.export_invalidate('store_invalid',f'Number of invalid fields: {total[2]}',invf,vf)
        (invf,vf) = dump.export_invalidate('store_valid',f'Number of invalid fields: {total[3]}',invf,vf)
        (invf,vf) = dump.export_invalidate('store_invalid',table_invip,invf,vf)
        (invf,vf) = dump.export_invalidate('store_invalid',table_invf,invf,vf)
        (invf,vf) = dump.export_invalidate('store_valid',table_vip,invf,vf)
        (invf,vf) = dump.export_invalidate('store_valid',table_vf,invf,vf)
        (invf,vf) = dump.export_invalidate('close','',invf,vf)
    
    def _dump_invalidate_ver2(total,table_invf,table_vf,invf,vf):
        (invf,vf) = dump.export_invalidate('store_invalid',f'Number of invalid fields: {total[2]}',invf,vf)
        (invf,vf) = dump.export_invalidate('store_valid',f'Number of valid fields: {total[3]}',invf,vf)
        if int(total[2]) >= 1000:
            print('Due to too many invalid fields, pls refer to the log below.')
            print(table_invf)
        if int(total[3]) >= 1000:
            print('Due to too many valid fields, pls refer to the log below.')
            print(table_vf)
        (invf,vf) = dump.export_invalidate('store_invalid',table_invf,invf,vf)
        (invf,vf) = dump.export_invalidate('store_valid',table_vf,invf,vf)
        (invf,vf) = dump.export_invalidate('close','',invf,vf)
    
    def _dump_invalidate_ver1(total,table_invip,table_vip,invf,vf):
        (invf,vf) = dump.export_invalidate('store_invalid',f'Number of invalid IPs: {total[0]}',invf,vf)
        (invf,vf) = dump.export_invalidate('store_valid',f'Number of valid IPs: {total[1]}',invf,vf)
        (invf,vf) = dump.export_invalidate('store_invalid',table_invip,invf,vf)
        (invf,vf) = dump.export_invalidate('store_valid',table_vip,invf,vf)
        print(table_invip)
        print(table_vip)
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
        print('Detecting the valid fields...')
        valid_fields = []
        for field in tqdm(fields):
            try:
                eval(field)
            except:
                pass
            try:
                eval(field+'.info["attribute"]')
                valid_fields.append(field)
            except:
                pass
        return valid_fields
    
    def _get_attr_num(fields):
        valid_fields = Pre_test._get_valid_fields(fields)
        print('Detecting and Categorizing attributes information...')
        avai_attrs = []
        num_avai_attr = []
        for valid_field in tqdm(valid_fields):
            attr = eval(valid_field+'.info["attribute"]')
            if attr not in avai_attrs:
                avai_attrs.append(attr)
                num_avai_attr.append(1)
            else:
                pointer = avai_attrs.index(attr)
                num_avai_attr[pointer] += 1
        return valid_fields,avai_attrs,num_avai_attr
        
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
        
    def export_pre_test_msg(dumpchoice,log_store):
        alg,flg = '',''
        if dumpchoice == 0:
            (alg,flg) = dump.export('pre_open','NA',alg,flg)
            for one_line_msg in log_store:
                (alg,flg) = dump.export('store',one_line_msg,alg,flg)
            (alg,flg) = dump.export('close_all','NA',alg,flg)
            (alg,flg) = dump.export('close_fail','NA',alg,flg)
        
    def _main(input_reg,auto_attr,auto):
        full_fields = error_regs(input_reg,auto,True)#detect for error regs and fields. Exclude them out from good regs and fields.
        valid_fields = invalidate(full_fields,auto,True)#detect for invalid regs and fields without attribute info. Exclude them out.
        #try:
        eval(input_reg+'.getaccess()')
        log_store = user.Pre_test.access_choice(input_reg)#display available access method and choose access method.(only for ip, how about die? how to choose?)
        #except Exception as e:
        #    log_store = ['']
        #    print(e)
        avai_attrs = attr_all(input_reg,True)#display available attributes
        chosen_attr = user.Pre_test.attr_choice(avai_attrs,auto,auto_attr)#choose the one for validation.('r/w' or '')
        dumpchoice = user.Pre_test.dump_choice(auto)#dump validation information to AggressiVE.log and AggressiVE_fail.log?(0/1)
        Pre_test.export_pre_test_msg(dumpchoice,log_store)#store access method info in 'AggressiVE.log'.
        return valid_fields,chosen_attr,dumpchoice
    
class Post_test:
    def _fail_main(Fail,fail_fields_name,alg,flg,dumpchoice,fail_x,auto):
        if Fail > 0 :
            chosen_fail_val = 1
            while chosen_fail_val == 1:
                chosen_fail_val = user.Post_test.fail_val_choice(auto)#choose the way to deal with fail fields.
                if chosen_fail_val == 2:
                    (alg,flg) = rdwr.validate2_fail_regs(fail_fields_name,alg,flg,dumpchoice,Fail,auto)#2nd validation for fail fields(re-write)
                elif chosen_fail_val == 1:
                    disp.disp_fail_content(fail_x,dumpchoice,alg,flg)#re-print fail fields
                    print('Fail:'+str(Fail))
            if dumpchoice == 0:#close the log file if opened.
                (alg,flg) = dump.export('close_all','NA',alg,flg)
                (alg,flg) = dump.export('close_fail','NA',alg,flg)
    
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
'rw/ac':'Read/Write Auto Clear.Field is RW,but HW may clear the field without intervention',
'rw/o/p':'Read-Write Once Sticky',
'rw/o/v/l':'Read-Write Once Variant with Lock',
'rw/p/l':'Read-Write Sticky Lock',
'rw/fuse':'Read-Write Fuse',
'rw/strap':'Read-Write Strap',
'dc':'-',
'ro/c/v':'-',
'ro/p':'-',
'ro/v':'-',
'rw/0c/v':'-',
'rw/l/k':'-',
'rw/p':'-',
'rw/s/l':'-',
'rw/v':'-',
'rw/v2':'-'
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
'ro/c':'New',
'rw/cr':'New',
'wo/1':'New',
'wo/c':'New',
'na':'New',
'rw0c_fw':'New',
'rw1c_fw':'New',
'double buffered':'New',
'r/w hardware clear':'New',
'read/32 bit write only':'New',
'r/w firmware only':'New',
'rw/v/p':'Undefined',
'rw/v/l':'Undefined',
'rw/v/p/l':'Undefined',
'ro/v/p':'Undefined',
'rw/1c/p':'Undefined',
'rw/1c/v':'Undefined',
'rw/1c/v/p':'Undefined',
'rw/1s/v':'Undefined',
'rw/1s/v/l':'Undefined',
'rw/ac':'Undefined',
'rw/o/p':'Undefined',
'rw/o/v/l':'Undefined',
'rw/p/l':'Undefined',
'rw/fuse':'Undefined',
'rw/strap':'Undefined',
'dc':'Undefined',
'ro/c/v':'Undefined',
'ro/p':'Undefined',
'ro/v':'Undefined',
'rw/0c/v':'Undefined',
'rw/l/k':'Undefined',
'rw/p':'Undefined',
'rw/s/l':'Undefined',
'rw/v':'Undefined',
'rw/v2':'Undefined'
}

ALGORITHM = {
'ro':['0/1','0/1','10','pre_rd','01','pre_rd','10','pre_rd'],
'wo':['0/1','0/1','10','pre_rd','01','pre_rd','10','pre_rd'],
'r/w':['0/1','0/1','10','10','01','01','10','10'],
'rw/s':['0/1','0/1','10','1(pre_rd)','01','11','10','11'],
'rw/l':['0/1','0/1','10','1(pre_rd)','01','11','10','11'],
'rw/o':['0/1','0/1','10','10','01','10','10','10'],
'rw/1c':['0/1','0/1','10','0(pre_rd)','01','00','10','00'],
'rw/1l':['0/1','0/1','10','1(pre_rd)','01','11','10','11'],
'rw/1s':['0/1','0/1','10','1(pre_rd)','01','11','10','11'],
'r/wc':['0/1','0/1','10','0(pre_rd)','01','00','10','00'],
'ro/swc':['0','1','10','1strd=0;2ndrd=0','01','1strd=1;2ndrd=1','10','1strd=0;2ndrd=0'],
'rsv':['0/1','0/1','10','pre_rd','01','Pre_rd','10','Pre_rd'],
'ro/c':['?','0','10','0','NA','NA','NA','NA'],
'rw/cr':['1/0','1/0','10','1strd=10;2ndrd=0','01','1strd=01;2ndrd=0','NA','NA'],
'wo/1':['1/0','1/0','10','0','01','0','10','0'],
'wo/c':['1/0','1/0','10','0','01','0','10','0'],
'na':['0','0','10','0','01','0','10','0'],
'rw0c_fw':['1/0','1/0','10','10','01','01','10','10'],
'rw1c_fw':['1/0','1/0','10','10','01','01','10','10'],
'double buffered':['1/0','1/0','10','10','01','01','10','10'],
'r/w hardware clear':['1/0','1/0','10','10','01','01','10','10'],
'read/32 bit write only':['1/0','1/0','10','10','01','01','10','10'],
'r/w firmware only':['1/0','1/0','10','10','01','01','10','10'],
'rw/v/p':['r/w','r/w','r/w','r/w','r/w','r/w','r/w','r/w'],
'rw/v/l':['r/w','r/w','r/w','r/w','r/w','r/w','r/w','r/w'],
'rw/v/p/l':['r/w','r/w','r/w','r/w','r/w','r/w','r/w','r/w'],
'ro/v/p':['ro','ro','ro','ro','ro','ro','ro','ro'],
'rw/1c/p':['ro','ro','ro','ro','ro','ro','ro','ro'],
'rw/1c/v':['ro','ro','ro','ro','ro','ro','ro','ro'],
'rw/1c/v/p':['ro','ro','ro','ro','ro','ro','ro','ro'],
'rw/1s/v':['ro','ro','ro','ro','ro','ro','ro','ro'],
'rw/1s/v/l':['ro','ro','ro','ro','ro','ro','ro','ro'],
'rw/ac':['ro','ro','ro','ro','ro','ro','ro','ro'],
'rw/o/p':['ro','ro','ro','ro','ro','ro','ro','ro'],
'rw/o/v/l':['ro','ro','ro','ro','ro','ro','ro','ro'],
'rw/p/l':['ro','ro','ro','ro','ro','ro','ro','ro'],
'rw/fuse':['ro','ro','ro','ro','ro','ro','ro','ro'],
'rw/strap':['ro','ro','ro','ro','ro','ro','ro','ro'],
'dc':['ro','ro','ro','ro','ro','ro','ro','ro'],
'ro/c/v':['r/w','r/w','?','?','?','?','?','?'],
'ro/p':['r/w','r/w','?','?','?','?','?','?'],
'ro/v':['r/w','r/w','?','?','?','?','?','?'],
'rw/0c/v':['ro','ro','?','?','?','?','?','?'],
'rw/l/k':['ro','ro','?','?','?','?','?','?'],
'rw/p':['ro','ro','?','?','?','?','?','?'],
'rw/s/l':['ro','ro','?','?','?','?','?','?'],
'rw/v':['ro','ro','?','?','?','?','?','?'],
'rw/v2':['ro','ro','?','?','?','?','?','?']
}
        
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
    for attr in DESC.keys():
        table += [{'Attrs':attr,'Descriptions':DESC[attr],'Status':STATUS[attr],'Pre_Rd1':ALGORITHM[attr][0],'Pre_Rd2':ALGORITHM[attr][1],'WR1':ALGORITHM[attr][2],'RD1':ALGORITHM[attr][3],'WR2':ALGORITHM[attr][4],'RD2':ALGORITHM[attr][5],'WR3':ALGORITHM[attr][6],'RD3':ALGORITHM[attr][7]}] 
    x = Table.fromDictList(table,headers)
    print(x.getTableText())
    print('''
Other Features:
Halt - Some registers will halt the system when read/write. It will still mark as 'pass' if the behavior is correct and continue validating.
System Reset - Some registers will restart the system when read/write. It will mark as 'fail' but it will still continue validating.
Hang - Some registers will make the system hang. It will mark as 'fail' and stop the validation. It will ask for doing 2nd validation for the last 10 registers and do machine check 1by1.
    ''')
    
def error_regs(input_reg,auto,validate=False):#Completed(die,IP, and register)
    '''
    Command:
        error_regs()

    Details:
        Displaying all the error Dies/IPs/Regs/Fields exist in input_reg.
        Error Die/IP/Reg = The Die/IP/Reg with the unacceptable name which contains unacceptable symbol and number.

    Inputs:
        input_regs = Name of die/ Name of IP/ Name of reg/ Name of field
        in_reg = To check in register level?
        in_field = To check in field level (deepest level)?

    Outputs:
        Name of error IPs/regs/fields.

    EX:
        >>> error_regs('cpu')
        >>> error_regs('cpu',auto=True)
        >>> error_regs('cpu',validate=True)
        >>> error_regs('cpu.gfx.display')
        >>> error_regs('cpu.gfx.display.vga_control')
    '''
    (error_regsname,valid_fields) = track.Pre_test.track_error_regsname(input_reg)
    Pre_test._dump_error_reg(error_regsname)#dump error regs and fields to error_regs.log
    user.Pre_test.disp_error_reg_choice(error_regsname,auto)#display all error regs and fields.
    if validate == True:
        return valid_fields
    
def invalidate(input_reg,auto,validate=False):#Completed(die,ip,fields)
    '''
    Command:
        invalidate()

    Details:
        Displaying all the fields which have the information of 'attribute'.

    Inputs:
        input_regs = Name of die/ Name of IP/ Name of reg/ Name of field

    Outputs:
        All the name of valid and invalid fields/IPs.

    EX:
        >>> invalidate('cpu')
        >>> invalidate('cpu.gfx.display')
        >>> invalidate('cpu.gfx.display.vga_control')
        >>> invalidate('cpu.gfx.display.vga_control',auto=False)
        >>> invalidate('cpu.gfx.display.vga_control',auto=False,validate=True)
    '''
    if validate == False:#for die and ip (user input)
        full_fields = error_regs(input_reg,auto,True)
    elif validate == True:
        full_fields = input_reg
    full_ips = track.fields_2_ips(full_fields)#search for all the IPs
    #detect the attribute info for valid_fields and invalid_fields.
    (valid_fields,invalid_fields) = track.track_invalidate_fields(full_fields)
    (table_invip,table_vip,table_invf,table_vf,valid_ips,invalid_ips) = Pre_test._generate_invalidate(valid_fields,invalid_fields)#generate valid and invalid ips.
    #Display result.
    total = disp.Pre_test.disp_invalidate(invalid_ips,valid_ips,invalid_fields,valid_fields)
    result_form = user.Pre_test.invalidate_choice(auto)
    #detect total num of fields and IPs.
    print('Calculating total number of fields and IPs...')
    total_num_fields = len(full_fields)
    (invf,vf) = dump.export_invalidate('open','','','')
    (invf,vf) = dump.export_invalidate('store_invalid',f'Total num of fields: {total_num_fields}',invf,vf)
    (invf,vf) = dump.export_invalidate('store_valid',f'Total num of fields: {total_num_fields}',invf,vf)
    if int(result_form) == 3:
        Pre_test._dump_invalidate_ver3(total,table_invip,table_invf,table_vip,table_vf,invf,vf)
    elif int(result_form) == 2:
        Pre_test._dump_invalidate_ver2(total,table_invf,table_vf,invf,vf)
    elif int(result_form) == 1:
        Pre_test._dump_invalidate_ver1(total,table_invip,table_vip,invf,vf)
    print('All the error fields names have been saved to:')
    print(Fore.LIGHTBLUE_EX + 'C>>Users>>pgsvlab>>Documents>>PythonSv>>invalid_fields.py.')
    print('C>>Users>>pgsvlab>>Documents>>PythonSv>>valid_fields.py.' + Fore.RESET)
    if validate == True:
        return valid_fields
        
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
    headers = ['Num','Attributes','Num of fields','Algorithm']
    table = []
    x = []
    total_num_valid_fields = 0
    for input_reg in input_regs:
        fields = Pre_test._get_fields(input_reg)#search for all the fields
        #detect the attribute info for valid_fields.
        (valid_fields,avai_attrs,num_avai_attr) = Pre_test._get_attr_num(fields)
        #combine the attributes with same category into one.
        (new_attrs,new_num) = Pre_test._comb_same_attr(avai_attrs,num_avai_attr)
        #display all the attrs and num of fields.
        i = 0
        for new_attr in new_attrs:
            if new_attr == 'rw':
                new_attr = 'r/w'
            elif new_attr == 'rw/c':
                new_attr = 'r/wc'
            if new_attr in STATUS:
                algo = STATUS[new_attr]
            else:
                algo = 'Undefined'
            table += [{'Num':i+1,'Attributes':new_attr ,'Num of fields':new_num[i],'Algorithm':algo}]
            i+=1
        total_num_valid_fields += len(valid_fields)
    table += [{'Num':'-','Attributes':'Total num of fields' ,'Num of fields':total_num_valid_fields,'Algorithm':'-'}]
    x = Table.fromDictList(table,headers)
    print(x.getTableText())
    aa = dump.export_attr_all('open','','')
    aa = dump.export_attr_all('store',x.getTableText(),aa)
    aa = dump.export_attr_all('close','',aa)
    if validate == True:
        return new_attrs

def aggressive(input_regs, auto=False, auto_attr=''):#WIP (register level)
    '''
    Command:
        aggressive()

    Details:
        Validate the fields of all the chosen regs.
        Dependencies = access method and attr
        If auto=True, it's a function without user input.

    Inputs:
        input_regs = Name of die/ Name of IP/ Name of reg
        auto = (False in default) Automate this features
        auto_attr = Attribute(s) of the registers that would like to validate

    Outputs:
        Table with the information of validation.

    EX:
        >>> aggressive('cpu')
        >>> aggressive('cpu.gfx.display')
        >>> aggressive('cpu.gfx.display.vga_control')
        >>> aggressive('cpu.gfx.display',auto=True)
        >>> aggressive('cpu.gfx.display',auto=True,auto_attr='rw')
    '''
    try:
        eval('__main__.'+input_regs)
    except:
        print('No such die exist in this project!')
        print('Please enter the correct one!')
        return 
    Pre_test.initial_setting()
    input_regs = Pre_test.convert_str2list(input_regs)
    for input_reg in input_regs:
        (valid_fields,chosen_attr,dumpchoice) = Pre_test._main(input_reg,auto_attr,auto)#run all pretest features.
        (fail_x,Fail,alg,flg,fail_fields_name) = rdwr.validate(valid_fields,chosen_attr,dumpchoice,auto)#validation.
        Post_test._fail_main(Fail,fail_fields_name,alg,flg,dumpchoice,fail_x,auto)#run post feature (Validate or display fail fields only).
    #itp.go()

def test():
    itp.halt()
    temp1 = 'cpu.cpu.core1.iq_cr_fit_hwa_error.fit_assertions'
    temp2 = 'cpu.cpu.core1.dcu_cr_mc2_addr.enh_mca_avail'
    temp3 = 'cpu.cpu.core1.dcu_cr_mc2_misc.enh_mca_avail'
    temp4 = 'cpu.cpu.core1.dcu_cr_fb_confiscate.enable'
    print(eval(temp2))
    eval(temp2+'.write('+'0xaaaaaaaaaaaaaaaa'+')')
    print(eval(temp2))
    eval(temp2+'.write('+'0x5555555555555555'+')')
    print(eval(temp2))
    eval(temp2+'.write('+'0xaaaaaaaaaaaaaaaa'+')')
    print(eval(temp2))
    
def debug():
    Pre_test.initial_setting()
    valid_fields = ['cpu.gfx.display.vga_control.vga_display_disable']
    (fail_x,Fail,alg,flg,fail_fields_name) = rdwr.validate(valid_fields,'rw',0,auto=False)#validation.

def test2():
    return 0

def test3():
    print(Fore.RED + 'This text is red in color')
    print(Fore.BLACK + 'This text is red in color')
    print(Fore.BLUE + 'This text is red in color')
    print(Fore.CYAN + 'This text is red in color')
    print(Fore.GREEN + 'This text is red in color')
    print(Fore.LIGHTBLACK_EX + 'This text is red in color')
    print(Fore.LIGHTBLUE_EX + 'This text is red in color')
    print(Fore.LIGHTCYAN_EX + 'This text is red in color')
    print(Fore.LIGHTGREEN_EX + 'This text is red in color')
    print(Fore.LIGHTMAGENTA_EX + 'This text is red in color')
    print(Fore.LIGHTRED_EX + 'This text is red in color')
    print(Fore.LIGHTWHITE_EX + 'This text is red in color')
    print(Fore.LIGHTYELLOW_EX + 'This text is red in color')
    print(Fore.MAGENTA + 'This text is red in color')
    print(Fore.RED + 'This text is red in color')
    print(Fore.WHITE + 'This text is red in color')
    print(Fore.YELLOW + 'This text is red in color')
    print(Fore.RESET + 'This text is red in color')
    print(Fore.YELLOW + 'This text is red in color. '+Fore.RED + 'sss')
    print(Fore.RESET + 'This text is red in color')
    temp1 = 32
    temp2 = 'jjk'
    print(f'{Fore.GREEN + str(temp1)} testing {Fore.YELLOW + temp2+Fore.RESET} hohoho')
    print('last')

 