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
from pysvtools import asciitable
import export_log_file as dump
import time
import colorama
from colorama import Fore
try:
    from tqdm.tqdm import tqdm
except:
    from tqdm import tqdm


class Pre_test:
    def disp_invalidate(no_attr_ips,attr_ips,no_attr_fields,attr_fields):
        total_invalid = len(no_attr_ips)
        total_valid = len(attr_ips)
        total_invalid_f = len(no_attr_fields)
        total_valid_f = len(attr_fields)
        print(f'{Fore.LIGHTBLUE_EX}Number of invalid IPs: {total_invalid}')
        print(f'Number of valid IPs: {total_valid}')
        print(f'Number of invalid fields: {total_invalid_f}')
        print(f'Number of valid fields: {str(total_valid_f)+Fore.RESET}')
        total = [total_invalid,total_valid,total_invalid_f,total_valid_f]
        return total
        
def disp_avail_access(avail_access):
    headers=['Heads','Access_Methods']
    rowdictlist=[]
    x=[]
    for head in avail_access:
        rowdictlist += [{'Heads':head,'Access_Methods':str(avail_access[head])}]  
        x = asciitable.AsciiTable.fromDictList(rowdictlist,headers)
    print(x.getTableText())
    
def disp_avail_attr(avail_attrs):
    headers=['Num','Attributes in this IP']
    rowdictlist=[]
    x=[]
    i=0
    for avail_attr in avail_attrs:
        i+=1
        rowdictlist += [{'Num':i,'Attributes in this IP':str(avail_attr)}] 
        x = asciitable.AsciiTable.fromDictList(rowdictlist,headers)
    rowdictlist += [{'Num':'Enter','Attributes in this IP':' All'}] 
    x = asciitable.AsciiTable.fromDictList(rowdictlist,headers)
    print(x.getTableText())
    
def disp_hang_regs(confirm_hang_regs, final_hang_stages, alg, flg, hlg):
    headers=['Hang Registers','Stage that caused Hang']
    rowdictlist=[]
    x=[]
    for confirm_hang_reg in confirm_hang_regs:
        rowdictlist += [{'Hang Registers':confirm_hang_reg,'Stage that caused Hang':str(final_hang_stages[confirm_hang_regs.index(confirm_hang_reg)])}] 
        x = asciitable.AsciiTable.fromDictList(rowdictlist,headers)
    x = asciitable.AsciiTable.fromDictList(rowdictlist,headers)
    try:
        temp = x.getTableText()
    except:
        temp = 'Confirm Hang Registers = '+str(len(confirm_hang_regs))
        print(temp)
    (alg,flg) = dump.export('store',temp,alg,flg)
    hlg.write(temp)
    return alg, flg, hlg

def store_content(rowdictlist,x,num,full_field_name,attr,pass_fail,pre_rd,wr_in_list,rd_in_list,fail_reason):
    if pass_fail == 'pass':
        pass_fail = Fore.GREEN + 'pass' + Fore.RESET
    elif pass_fail == 'fail':
        pass_fail = Fore.RED + 'fail' + Fore.RESET
    undefined_attrs = ['dc','ro/c/v','ro/p','ro/v','ro/v/p','rw/1c/p','rw/1c/v','rw/1c/v/p','rw/0c/v','rw/1s/v/p','rw/1s/v','rw/1s/v/l','rw/ac','rw/l/k','rw/o/p','rw/o/v/l','rw/p','rw/p/l','rw/s/l','rw/fuse','rw/strap','rw/v','rw/v/p','rw/v/l','rw/v/p/l','rw/v2']
    headers=['Num','Field Name','Attr',Fore.LIGHTWHITE_EX+'Status'+Fore.RESET,'1st_Pre_RD','2nd_Pre_RD','1st_Val_WR','1st_Val_RD','2nd_Val_WR','2nd_Val_RD','3rd_Val_WR','3rd_Val_RD']
    if pre_rd == []:#for those that are not able to read and write.
        if attr in ['ro/swc','rw/cr'] or attr in undefined_attrs:
            rowdictlist += [{'Num':str(num),'Field Name':full_field_name,'Attr':attr,Fore.LIGHTWHITE_EX+'Status'+Fore.RESET: pass_fail+str(fail_reason),'1st_Pre_RD':'NA','2nd_Pre_RD':'NA','1st_Val_WR':'NA','1st_Val_RD':'1strd:NA;2ndrd:NA','2nd_Val_WR':'NA','2nd_Val_RD':'1strd:NA;2ndrd:NA','3rd_Val_WR':'NA','3rd_Val_RD':'1strd:NA;2ndrd:NA'}]
        else:
            rowdictlist += [{'Num':str(num),'Field Name':full_field_name,'Attr':attr,Fore.LIGHTWHITE_EX+'Status'+Fore.RESET:pass_fail+str(fail_reason),'1st_Pre_RD':'NA','2nd_Pre_RD':'NA','1st_Val_WR':'NA','1st_Val_RD':'NA','2nd_Val_WR':'NA','2nd_Val_RD':'NA','3rd_Val_WR':'NA','3rd_Val_RD':'NA'}]
    else:#normal one
        if attr in ['ro/swc','rw/cr'] or attr in undefined_attrs:
            rowdictlist += [{'Num':str(num),'Field Name':full_field_name,'Attr':attr,Fore.LIGHTWHITE_EX+'Status'+Fore.RESET: pass_fail+str(fail_reason),'1st_Pre_RD':pre_rd[0],'2nd_Pre_RD':pre_rd[1],'1st_Val_WR':wr_in_list[0],'1st_Val_RD':'1strd:'+rd_in_list[0]+';2ndrd:'+rd_in_list[1],'2nd_Val_WR':wr_in_list[1],'2nd_Val_RD':'1strd:'+rd_in_list[2]+';2ndrd:'+rd_in_list[3],'3rd_Val_WR':wr_in_list[2],'3rd_Val_RD':'1strd:'+rd_in_list[4]+';2ndrd:'+rd_in_list[5]}]
        else:
            Pre_RD1 = str(pre_rd[0])
            Pre_RD2 = str(pre_rd[1])
            WR1 = str(wr_in_list[0])
            RD1 = str(rd_in_list[0])
            WR2 = str(wr_in_list[1])
            RD2 = str(rd_in_list[1])
            WR3 = str(wr_in_list[2])
            RD3 = str(rd_in_list[2])
            rowdictlist += [{'Num':str(num),'Field Name':full_field_name,'Attr':attr,Fore.LIGHTWHITE_EX+'Status'+Fore.RESET:pass_fail+str(fail_reason),'1st_Pre_RD':Pre_RD1,'2nd_Pre_RD':Pre_RD2,'1st_Val_WR':WR1,'1st_Val_RD':RD1,'2nd_Val_WR':WR2,'2nd_Val_RD':RD2,'3rd_Val_WR':WR3,'3rd_Val_RD':RD3}]    
    x = asciitable.AsciiTable.fromDictList(rowdictlist,headers)
    return rowdictlist,x
    
def store_fail_content(fail_rowdl,fail_x,num,full_field_name,attr,pass_fail,pre_rd,wr_in_list,rd_in_list,fail_reason):
    if pass_fail == 'pass':
        pass_fail = Fore.GREEN + 'pass' + Fore.RESET
    elif pass_fail == 'fail':
        pass_fail = Fore.RED + 'fail' + Fore.RESET
    headers=['Num','Field Name','Attr',Fore.LIGHTWHITE_EX+'Status'+Fore.RESET,'1st_Pre_RD','2nd_Pre_RD','1st_Val_WR','1st_Val_RD','2nd_Val_WR','2nd_Val_RD','3rd_Val_WR','3rd_Val_RD']
    undefined_attrs = ['dc','ro/c/v','ro/p','ro/v','ro/v/p','rw/1c/p','rw/1c/v','rw/1c/v/p','rw/0c/v','rw/1s/v/p','rw/1s/v','rw/1s/v/l','rw/ac','rw/l/k','rw/o/p','rw/o/v/l','rw/p','rw/p/l','rw/s/l','rw/fuse','rw/strap','rw/v','rw/v/p','rw/v/l','rw/v/p/l','rw/v2']
    new_defined_attrs = ['ro/c','rw/cr','wo/1','wo/c','na','rw0c_fw','rw1c_fw','double buffered','r/w hardware clear','read/32 bit write only','r/w firmware only']
    if attr in ['ro/swc','rw/cr'] or attr in undefined_attrs:
        fail_rowdl += [{'Num':str(num),'Field Name':full_field_name,'Attr':attr,Fore.LIGHTWHITE_EX+'Status'+Fore.RESET: pass_fail+str(fail_reason),'1st_Pre_RD':pre_rd[0],'2nd_Pre_RD':pre_rd[1],'1st_Val_WR':wr_in_list[0],'1st_Val_RD':'1strd:'+rd_in_list[0]+';2ndrd:'+rd_in_list[1],'2nd_Val_WR':wr_in_list[1],'2nd_Val_RD':'1strd:'+rd_in_list[2]+';2ndrd:'+rd_in_list[3],'3rd_Val_WR':wr_in_list[2],'3rd_Val_RD':'1strd:'+rd_in_list[4]+';2ndrd:'+rd_in_list[5]}]
    else:
        Pre_RD1 = str(pre_rd[0])
        Pre_RD2 = str(pre_rd[1])
        WR1 = str(wr_in_list[0])
        RD1 = str(rd_in_list[0])
        WR2 = str(wr_in_list[1])
        RD2 = str(rd_in_list[1])
        WR3 = str(wr_in_list[2])
        RD3 = str(rd_in_list[2])
        fail_rowdl += [{'Num':str(num),'Field Name':full_field_name,'Attr':attr,Fore.LIGHTWHITE_EX+'Status'+Fore.RESET:pass_fail+str(fail_reason),'1st_Pre_RD':Pre_RD1,'2nd_Pre_RD':Pre_RD2,'1st_Val_WR':WR1,'1st_Val_RD':RD1,'2nd_Val_WR':WR2,'2nd_Val_RD':RD2,'3rd_Val_WR':WR3,'3rd_Val_RD':RD3}]
    fail_x = asciitable.AsciiTable.fromDictList(fail_rowdl,headers)
    return fail_rowdl,fail_x

def disp_content(rowdictlist,x,alg,flg):
    content_in_content = x.getTableText()
    print(content_in_content)
    (alg,flg) = dump.export('store',content_in_content,alg,flg)

def disp_fail_content(x,alg,flg):
    fail_content = x.getTableText()
    print(fail_content)
    (alg,flg) = dump.export('store',fail_content,alg,flg)
    (alg,flg) = dump.export('store_fail',fail_content,alg,flg)
    
def disp_total_pass_fail(Pass,Fail,Unknown,Error,Hang):
    print(Fore.LIGHTBLUE_EX+'Pass:'+str(Pass))
    print('Fail:'+str(Fail))
    print('Unknown:'+str(Unknown))
    print('Error:'+str(Error))
    print('Hang:'+str(Hang)+Fore.RESET)

def store(name,mode,content):
    if content == []:
        return f'No {mode}'
    headers=['Num',name]
    rowdictlist = []
    x = []
    i=1
    for c in tqdm(content):
        rowdictlist += [{'Num':mode+' '+str(i),name:c}]
        i+=1
    x = asciitable.AsciiTable.fromDictList(rowdictlist,headers)
    print(f'Done generating {mode}')
    return x.getTableText()

def loadbar(iteration, total, prefix='', infix ='', suffix='', decimals=1, length=100, fill='>'):
    percent = 0
    filledLength = 0
    percent = ('{0:.' + str(decimals) + 'f}').format(100 * (iteration/float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' *(length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% [{infix}] {suffix}', end='\r')
    if iteration == total:
        print()  
        
def progress(iteration, total, prefix='', infix1 ='', infix2 = '', suffix='', decimals=1):
    #percent = 0
    percent = ('{0:.' + str(decimals) + 'f}').format(100 * (iteration/float(total)))
    #print(f'\r{prefix}{Fore.LIGHTBLUE_EX + percent}%{Fore.RESET} [{infix}] {suffix}', end='\r')
    LINE_CLEAR = '\x1b[2K' # <-- ANSI sequence
    print(end=LINE_CLEAR)
    print(f'\r{prefix}{Fore.LIGHTBLUE_EX + percent}%{Fore.RESET} [{infix1}] {suffix}', end='')
    if iteration == total:
        print()

def error_table(msg_sorted):
    headers = ['Num', 'Error Message']
    rowdictlist = []
    x = []
    i=1
    for msg in msg_sorted:
        rowdictlist += [{'Num':str(i),'Error Message':msg}]
        i += 1
    x = asciitable.AsciiTable.fromDictList(rowdictlist,headers)
    print(x.getTableText())

def disp_all_errors(disp_choice,msg_sorted,error_info):
    headers = ['Num','Registers']
    rowdictlist = []
    x = []
    i = 1
    if disp_choice == '':
        for msg in msg_sorted:
            i = 1
            print(f'Error = {msg}')        
            for reg in error_info.keys():
                if msg == error_info[reg]:
                    rowdictlist += [{'Num':str(i),'Registers':reg}]
                    i += 1
    else:
        msg = msg_sorted[disp_choice-1]
        for reg in error_info.keys():
            if msg == error_info[reg]:
                rowdictlist += [{'Num':str(i),'Registers':reg}]
                i += 1
    x = asciitable.AsciiTable.fromDictList(rowdictlist,headers)
    print(x.getTableText())
    return x.getTableText()

def time(sec):
    min = 0
    hour = 0
    while sec >= 60:
        if sec >= 60:
            sec -= 60
            min += 1
    while min >= 60:
        if min == 60:
            min -= 60
            hour += 1
    return sec,min,hour
	