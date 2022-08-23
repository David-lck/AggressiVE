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
'badname_regs' :  'To display all the unacceptable name of Dies/IPs/Regs/Fields exist in input_reg.',
'invalidate' : 'To display all the fields which have the information of attribute.',
'attr_all' : 'To display the number of fields we have with the specific attributes.',
'aggressive' : 'Main function of AggressiVE. (Require the initial declaration from user if automatable.)',
'log':'To display logs that AgressiVE may generate.'
}
def list_all_cmd():
    headers = ['Available Functions','Description']
    table = []
    for func in AVAIL_FUNCS.keys():
        table+=[{'Available Functions':func,'Description':AVAIL_FUNCS[func]}]
    x = Table.fromDictList(table,headers)
    print(x.getTableText())
	
def log():
    headers = ['Logs Path','Descriptions']
    table = []
    x = []    
    for title,path in Logs.PATH.items():
        table += [{'Logs Path':path,'Descriptions':Logs.DESC[title]}]
    x = Table.fromDictList(table,headers)
    print(x.getTableText())

class Pre_test:
    def _dump_error_reg(badname_registers):
        blg = dump.export_badname('open','','')
        print('Storing unacceptable name registers to bad_name_regs.log...')
        for badname_register in badname_registers:
            try:
                blg = dump.export_badname('store',badname_register,blg)
            except:
                print(f'Special Symbols in the name which cannot be recorded in log file: {badname_register}')
        blg = dump.export_badname('close','',blg)
    
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
        
    def _main(input_reg,auto_attr,auto):
        full_fields = badname_regs(input_reg,auto,True)#detect for error regs and fields. Exclude them out from good regs and fields.
        attr_fields = invalidate(full_fields,auto,True)#detect for invalid regs and fields without attribute info. Exclude them out.
        #try:
        eval(input_reg+'.getaccess()')
        log_store = user.Pre_test.access_choice(input_reg)#display available access method and choose access method.(only for ip, how about die? how to choose?)
        #except Exception as e:
        #    log_store = ['']
        #    print(e)
        avai_attrs = attr_all(input_reg,True)#display available attributes
        chosen_attr = user.Pre_test.attr_choice(avai_attrs,auto,auto_attr)#choose the one for validation.('r/w' or '')
        Pre_test.export_pre_test_msg(log_store)#store access method info in 'AggressiVE.log'.
        return attr_fields,chosen_attr
    
class Post_test:
    def _fail_main(fail_infos,alg,flg):
        [Fail,fail_regs,fail_x,auto] = fail_infos
        if Fail > 0 :
            chosen_fail_val = 1
            while chosen_fail_val == 1:
                chosen_fail_val = user.Post_test.fail_val_choice(auto)#choose the way to deal with fail fields.
                if chosen_fail_val == 2:
                    (alg,flg) = rdwr.Post_test.validate2_fail_regs(fail_regs,alg,flg,Fail,auto)#2nd validation for fail fields(re-write)
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

class Logs:
    PATH = {
    'wout_attr_fields' : 'C>>Users>>pgsvlab>>PythonSv>>no_attr_fields.log',
    'with_attr_fields' : 'C>>Users>>pgsvlab>>PythonSv>>attr_fields.log',
    'bad_name_regs' : 'C>>Users>>pgsvlab>>PythonSv>>bad_name_regs.log',
    'AggressiVE' : 'C>>Users>>pgsvlab>>PythonSv>>AggressiVE.log',
    'AggressiVE_fail' : 'C>>Users>>pgsvlab>>PythonSv>>AggressiVE_fail.log',
    'AggressiVE_error' : 'C>>Users>>pgsvlab>>PythonSv>>AggressiVE_error.log',
    'AggressiVE_hang' : 'C>>Users>>pgsvlab>>PythonSv>>AggressiVE_hang.log',
    'attr_all' : 'C>>Users>>pgsvlab>>PythonSv>>attr_all.log',
    'pass_regs' : 'C>>Users>>pgsvlab>>PythonSv>>pass_regs.log',
    'fail_regs' : 'C>>Users>>pgsvlab>>PythonSv>>fail_regs.log',
    'error_regs' : 'C>>Users>>pgsvlab>>PythonSv>>error_regs.log',
    'hang_regs' : 'C>>Users>>pgsvlab>>PythonSv>>hang_regs.log',
	}
    DESC = {
    'wout_attr_fields' : "Fields that don't have attribute information.",
    'with_attr_fields' : "Fields that have attribute information.",
    'bad_name_regs' : "Registers that have naming issue.",
    'AggressiVE' : "All the information when running aggressive().",
    'AggressiVE_fail' : "All the fail validation information when running aggressive().",
    'attr_all' : "List of available attributes.",
    'pass_regs' : "List of passing registers.",
    'fail_regs' : "List of failing registers.",
    'error_regs' : 'List of registers that are not able to read and write and show error message.',
    'hang_regs' : 'List of registers that caused the system hang.',
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
    
def badname_regs(input_reg,auto,validate=False):#Completed(die,IP, and register)
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

    EX:
        >>> badname_regs('cpu')
        >>> badname_regs('cpu',auto=True)
        >>> badname_regs('cpu',validate=True)
        >>> badname_regs('cpu.gfx.display')
        >>> badname_regs('cpu.gfx.display.vga_control')
    '''
    (badname_registers,attr_fields) = track.Pre_test.track_badname_regs(input_reg)
    Pre_test._dump_error_reg(badname_registers)
    user.Pre_test.disp_badname_reg_choice(badname_registers,auto)
    if validate == True:
        return attr_fields
    
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
        full_fields = badname_regs(input_reg,auto,True)
    elif validate == True:
        full_fields = input_reg
    full_ips = track.fields_2_ips(full_fields)#search for all the IPs
    #detect the attribute info for attr_fields and no_attr_fields.
    (attr_fields,no_attr_fields) = track.track_invalidate_fields(full_fields)
    (table_invip,table_vip,table_invf,table_vf,attr_ips,no_attr_ips) = Pre_test._generate_invalidate(attr_fields,no_attr_fields)#generate valid and invalid ips.
    #Display result.
    total = disp.Pre_test.disp_invalidate(no_attr_ips,attr_ips,no_attr_fields,attr_fields)
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
    print('All the with attr fields & non attr fields names have been saved to:')
    print(Fore.LIGHTBLUE_EX + 'C>>Users>>pgsvlab>>Documents>>PythonSv>>no_attr_fields.py.')
    print('C>>Users>>pgsvlab>>Documents>>PythonSv>>attr_fields.py.' + Fore.RESET)
    if validate == True:
        return attr_fields
        
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

def aggressive(input_regs, auto=True, auto_attr=''):#WIP (register level)
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
        >>> aggressive('cpu.gfx.display',auto=False)
        >>> aggressive('cpu.gfx.display',auto_attr='rw')
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
        (attr_fields,chosen_attr) = Pre_test._main(input_reg,auto_attr,auto)#run all pretest features.
        Exec.rdwr.validate(attr_fields,chosen_attr,auto)#validation.



 