import tracking as track
import os
import time

def export(choice,content,alg,flg):#Write/store only
    #dump_mode = "w"
    dump_mode = "a"
    if choice == 'close_all':
        alg.close()
    elif choice == 'close_fail':
        flg.close()
    elif choice == 'store':
        alg.write(content)
        alg.write('\n')
    elif choice == 'store_fail':
        flg.write(content)
        flg.write('\n')
    else:
        alg = open("AggressiVE.log", dump_mode)
        flg = open("AggressiVE_fail.log", dump_mode)
    return alg,flg
    
def export_nocheck(choice,content,nclg):
    dump_mode = "a"
    if choice == 'close':
        nclg.close()
    elif choice == 'store':
        nclg.write(content)
        nclg.write('\n')
    else:
        nclg = open("Printout_nocheck.log", dump_mode)
    return nclg

def export_badname(choice,content,blg):
    current_time = str(time.ctime().replace(" ","_").replace(":",""))
    if choice == 'open':
        blg = open("AggressiVE_badname"+str(current_time)+'.log',"w")
    elif choice == 'close':
        blg.close()
    elif choice == 'store':
        blg.write(content)
        blg.write('\n')
    return blg
	
def export_badname_regs(choice,content,ilg):
    current_time = str(time.ctime().replace(" ","_").replace(":",""))
    if choice == 'open':
        ilg = open("bad_name_regs"+str(current_time)+'.log',"w")
    elif choice == 'close':
        ilg.close()
    elif choice == 'store':
        ilg.write(content)
        ilg.write('\n')
    return ilg
	
def export_regs(pass_regs, fail_regs, error_regs, sus_hang_regs, nocheck_regs):
    prlg, frlg, erlg, shrlg, nclg = '', '', '', '', ''
    prlg = open("pass_regs.log","w")
    frlg = open("fail_regs.log","w")
    erlg = open("error_regs.log","w")
    shrlg = open("sus_hang_regs.log","w")
    nclg = open("nocheck_regs.log","w")
    for pass_reg in pass_regs:
        prlg.write(pass_reg)
        prlg.write('\n')
    for fail_reg in fail_regs:
        frlg.write(fail_reg)
        frlg.write('\n')
    for error_reg in error_regs:
        erlg.write(error_reg)
        erlg.write('\n')
    for sus_hang_reg in sus_hang_regs:
        for one_sus_reg in sus_hang_reg:
            shrlg.write(one_sus_reg)
            shrlg.write('\n')
    for nocheck_reg in nocheck_regs:
        nclg.write(nocheck_reg)
        nclg.write('\n')
    print('All current list of pass registers have been saved to C>>Users>>pgsvlab>>PythonSv>>Aggressive_logs>>pass_regs.log')
    print('All current list of pass registers have been saved to C>>Users>>pgsvlab>>PythonSv>>Aggressive_logs>>fail_regs.log')
    print('All current list of error registers have been saved to C>>Users>>pgsvlab>>PythonSv>>Aggressive_logs>>error_regs.log')
    print('All current list of suspect hang registers have been saved to C>>Users>>pgsvlab>>PythonSv>>Aggressive_logs>>sus_hang_regs.log')
    print('All current list of error registers have been saved to C>>Users>>pgsvlab>>PythonSv>>Aggressive_logs>>nocheck_regs.log')
    prlg.close()
    frlg.close()
    erlg.close()
    shrlg.close()
    nclg.close()
    
def export_hang_regs(confirm_hang_regs):
    hrlg = ''
    hrlg = open("hang_regs.log","w")
    for reg in confirm_hang_regs:
        hrlg.write(reg)
        hrlg.write('\n')
    hrlg.close()
    print('All current list of confirmed hang registers have been saved to C>>Users>>pgsvlab>>PythonSv>>Aggressive_logs>>hang_regs.log')

def export_attr_all(choice,content,aa):
    current_time = str(time.ctime().replace(" ","_").replace(":",""))
    if choice == 'open':
        aa = open('attr_all_'+str(current_time)+'.log',"w")
    elif choice == 'close':
        aa.close()
    elif choice == 'store':
        aa.write(content)
        aa.write('\n')
    return aa
	
def export_invalidate(choice,content,invf,vf):
    current_time = str(time.ctime().replace(" ","_").replace(":",""))
    if choice == 'open':
        invf = open("no_attr_fields_"+str(current_time)+'.log',"w")
        vf = open("attr_fields_"+str(current_time)+'.log',"w")
    elif choice == 'close':
        invf.close()
        vf.close()
    elif choice == 'store_invalid':
        invf.write(content)
        invf.write('\n')
    elif choice == 'store_valid':
        vf.write(content)
        vf.write('\n')
    return invf,vf
	
def export_regtrack(choice,content,rt):
    if choice == 'open':
        rt = open("regtrack.log","w")
    elif choice == 'close':
        rt.close()
    elif choice == 'store':
        rt.write(content)
        rt.write('\n')
    return rt

def export_write_pass(plg,content):
    #For AggressiVE_pass.log
    plg.write(content)
    plg.write('\n')
    return plg
    
def export_write_error(elg,content):
    #For AggressiVE_error.log
    elg.write(content)
    elg.write('\n')
    return elg

def create_log_folder():
    log_num=1
    while True:
        try:
            os.makedirs('Aggressive_logs'+str(log_num))
        except:
            log_num += 1
            continue
        break
	
def goto_latest_log_folder():#Assume C:\Users\pgsvlab\PythonSv is the default log file for all systems.
    log_num=1
    while True:
        try:
            os.chdir(r'C:\Users\pgsvlab\PythonSv\Aggressive_logs'+str(log_num))
        except:
            break
        log_num+=1

def goto_default_path():#Assume C:\Users\pgsvlab\PythonSv is the default log file for all systems.
    os.chdir(r'C:\Users\pgsvlab\PythonSv')