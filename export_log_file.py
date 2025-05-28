import tracking as track
import os
import time
import math
import shutil
from pathlib import Path
current_directory = Path(__file__).parent
script_path = current_directory / "log_path.txt"

log_file_path1 = r'C:\Users\limchink\PythonSv'
log_file_path2 = r'C:\Users\pgsvlab\PythonSv'
log_file_path3 = r'C:\Users\pgsvlab\PythonSv'


def _convert_strnan_2_floatnan(list_with_nan):
    newlist = []
    for item in list_with_nan:
        if item == "nan":
            newlist.append(math.nan)
        else:
            newlist.append(item)
    return newlist

def _convert_strlist2list(strlist):
    strlist = strlist[1:-1]
    if strlist[0] == "[":
        strlist = strlist.replace(" ", "")
        strlist = strlist.split("],")
        output = []
        for string in strlist:
            #for empty list
            if string in ["[","[]"]:
                output.append([])
            else:
                string = string.replace("[","")#1,1 or 1
                string = string.replace("]","")
                string = string.replace("'","")
                string = string.replace('"','')
                string = string.split(",")#[1,1] ir [1]
                output.append(string)
    else:
        strlist = strlist.replace("[","")
        strlist = strlist.replace("]","")
        strlist = strlist.replace("'","")
        strlist = strlist.replace('"','')
        strlist = strlist.replace(' ','')
        output = strlist.split(",")
    if "nan" in output:
        output = _convert_strnan_2_floatnan(output)
    return output

def process_var(varx):
    # Split the string at the '=' character
    key, value = varx.split('=', 1)
    
    if value[0] == "[":
        evaluated_value = _convert_strlist2list(value) # if the data is list or nested list in string, convert to list or nested list back.
    else:
        evaluated_value = value # when it is string, not list.
    return evaluated_value

def _get_logregs(path, logname):
    os.chdir(path)
    #read the fail_regs.log
    with open(os.path.join(path, logname),'r') as file:
        full_fields = file.readlines()
        full_fields = [line.strip() for line in full_fields]

    return full_fields

def _find_and_get_tobecont_logfile(path):
    os.chdir(path) # goto Unfinish logfile folder    
    #find tbc
    tbc_path = os.path.join(path, 'ToBeCont')
    if os.path.exists(tbc_path) and os.path.isdir(tbc_path):
        os.chdir(tbc_path) # goto ToBeCont folder
        #read the input_regs.log
        with open(os.path.join(tbc_path,'input_regs.log'),'r') as file:
            unfinish_input_regs = file.readlines()
            unfinish_input_regs = [line.strip() for line in unfinish_input_regs]
        #read the all_tobeval_fields.log
        with open(os.path.join(tbc_path,'all_tobeval_fields.log'),'r') as file:
            chosen_attr_fields = file.readlines()
            chosen_attr_fields = [line.strip() for line in chosen_attr_fields]
        #read the validated_fields.log
        with open(os.path.join(tbc_path,'validated_fields.log'),'r') as file:
            validated_fields = file.readlines()
            validated_fields = [line.strip() for line in validated_fields]
        #read the config data
        with open(os.path.join(tbc_path,'configurations.log'),'r') as file:
            log_lines = file.readlines()
            log_lines = [line.strip() for line in log_lines]
        for config_line in log_lines:
            if "dfd_en" in config_line:
                dfd_en = process_var(config_line)
            elif "auto_access" in config_line:
                auto_access = process_var(config_line)
            elif "auto_attr" in config_line:
                auto_attr = process_var(config_line)
            elif "auto" in config_line:
                auto = process_var(config_line)
            elif "detections" in config_line:
                detections = process_var(config_line)
            elif "num_val_seq" in config_line:
                num_val_seq = process_var(config_line)
                num_val_seq = int(float(num_val_seq))
            elif "locklists" in config_line:
                locklists = process_var(config_line)
            elif "random" in config_line:
                random = process_var(config_line)
    else:
        print("Not able to find ToBeCont. Will Stop!")
        os.chdir(path) # go out from ToBeCont folder
        return "NA","NA","NA","NA","NA","NA","NA","NA","NA","NA"
    os.chdir(path) # go out from ToBeCont folder
    #convert all the 1/0/"True"/"False" back to boolean
    dfd_en = dfd_en == "True"
    auto = auto == "True"
    random = random == "True"
    detections = [item == "True" if item in ["True", "False"] else item for item in detections]
    return chosen_attr_fields, validated_fields, unfinish_input_regs, dfd_en, auto,detections,num_val_seq,locklists, random, auto_access, auto_attr

def export(choice,content,alg,flg):#Write/store only
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
        alg = open("AggressiVE.log", "a")
        flg = open("AggressiVE_fail.log", "a")
    return alg,flg

def create_tbc_folder():
    os.makedirs("ToBeCont") # create ToBeCont folder

def export_tobecont_input_regs(filtered_input_regs):
    cur_path = os.getcwd() # get current path
    tbc_dir = os.path.join(cur_path, 'ToBeCont')
    os.chdir(tbc_dir) # goto ToBeCont folder
    bulg = open("input_regs.log", "w")
    for reg in filtered_input_regs:
        bulg.write(reg)
        bulg.write('\n')
    bulg.close()
    os.chdir(cur_path) # go out from ToBeCont folder

def rmv_input_reg_from_log(input_reg):
    cur_path = os.getcwd() # get current path
    if 'ToBeCont' not in cur_path:
        tbc_path = os.path.join(cur_path, 'ToBeCont')
    else:
        tbc_path = cur_path
    os.chdir(tbc_path) # goto ToBeCont folder
    #read the data in list
    with open(f"{tbc_path}/input_regs.log","r") as file:
        log_lines = file.readlines()
        log_lines = [line.strip() for line in log_lines]
    #remove the input_reg from list
    log_lines.remove(input_reg)
    #rewrite the log file with this new input_reg
    bulg = open("input_regs.log", "w")
    for reg in log_lines:
        bulg.write(reg)
        bulg.write('\n')
    bulg.close()
    os.chdir(cur_path) # go out from ToBeCont folder

def export_tobecont_allfields(chosen_attr_fields):
    cur_path = os.getcwd() # get current path
    tbc_path = os.path.join(cur_path, 'ToBeCont')
    os.chdir(tbc_path) # goto ToBeCont folder
    bulg = open("all_tobeval_fields.log", "w")
    for field in chosen_attr_fields:
        bulg.write(field)
        bulg.write('\n')
    bulg.close()
    os.chdir(cur_path) # go out from ToBeCont folder
    
def _ensure_detections_in_boolean(detections):
    new_detections = []
    loop = 0
    for detection in detections:
        if loop == (len(detections)-1):
            new_detections.append(str(int(float(detection))))
        elif str(detection) in ["False", "0", "0.0"]:
            new_detections.append(False)
        elif str(detection) in ["True", "1", "1.0"]:
            new_detections.append(True)
        loop += 1
    return new_detections
    
def export_tobecont_config(dfd_en, auto, detections, num_val_seq, locklists, random, auto_access, auto_attr):
    cur_path = os.getcwd() # get current path
    tbc_path = os.path.join(cur_path, 'ToBeCont')
    os.chdir(tbc_path) # goto ToBeCont folder
    bulg = open("configurations.log", "w")
    if dfd_en == 0:
        bulg.write(f"dfd_en={False}")
    else:
        bulg.write(f"dfd_en={True}")
    bulg.write('\n')
    if auto == 0:
        bulg.write(f"auto={False}")
    else:
        bulg.write(f"auto={True}")
    bulg.write('\n')
    detections = _ensure_detections_in_boolean(detections)
    bulg.write(f"detections={detections}")
    bulg.write('\n')
    bulg.write(f"num_val_seq={str(num_val_seq)}")
    bulg.write('\n')
    bulg.write(f"locklists={str(locklists)}")
    bulg.write('\n')
    if random == 0:
        bulg.write(f"random={False}")
    else:
        bulg.write(f"random={True}")
    bulg.write('\n')
    bulg.write(f"auto_access={str(auto_access)}")
    bulg.write('\n')
    bulg.write(f"auto_attr={str(auto_attr)}")
    bulg.close()
    os.chdir(cur_path) # go out from ToBeCont folder
    
def export_tobecont_final(validated_fields):
    cur_path = os.getcwd() # get current path
    tbc_path = os.path.join(cur_path, 'ToBeCont')
    os.chdir(tbc_path) # goto ToBeCont folder
    bulg = open("validated_fields.log", "w")
    for field in validated_fields:
        bulg.write(field)
        bulg.write('\n')
    bulg.close()
    
def rmv_tobecont_folder():
    cur_path = os.getcwd() # Get the current working directory
    tbc_path = os.path.join(cur_path, 'ToBeCont')# Construct the path to the "ToBeCont" folder
    # Check if the "tbc" folder exists
    if os.path.exists(tbc_path) and os.path.isdir(tbc_path):
        # Remove the "tbc" folder and all its contents
        shutil.rmtree(tbc_path)
        print(f"The folder '{tbc_path}' and all its contents have been removed due to validation has successfully finished.")
    else:
        print(f"The folder '{tbc_path}' does not exist.")
    
def export_acessibility(choice, content, sclg):
    if choice == 'close':
        sclg.close()
    elif choice == 'store':
        sclg.write(content)
        sclg.write('\n')
    else:
        sclg = open("accessibility.log", "w")
    return sclg
    
def export_nocheck(choice,content,nclg):
    if choice == 'close':
        nclg.close()
    elif choice == 'store':
        nclg.write(content)
        nclg.write('\n')
    else:
        nclg = open("Printout_nocheck.log", "a")
    return nclg

def export_badname(choice,content,blg):
    if choice == 'open':
        blg = open("AggressiVE_badname.log","a")
    elif choice == 'close':
        blg.close()
    elif choice == 'store':
        blg.write(content)
        blg.write('\n')
    return blg
	
def export_badname_regs(choice,content,ilg):
    if choice == 'open':
        ilg = open("bad_name_regs.log","a")
    elif choice == 'close':
        ilg.close()
    elif choice == 'store':
        ilg.write(content)
        ilg.write('\n')
    return ilg
	
def export_regs(pass_regs, fail_regs, error_regs, sus_hang_regs, nocheck_regs):
    prlg, frlg, erlg, shrlg, nclg = '', '', '', '', ''
    prlg = open("pass_regs.log","a")
    frlg = open("fail_regs.log","a")
    erlg = open("error_regs.log","a")
    shrlg = open("sus_hang_regs.log","a")
    nclg = open("nocheck_regs.log","a")
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
    hrlg = open("hang_regs.log","a")
    for reg in confirm_hang_regs:
        hrlg.write(reg)
        hrlg.write('\n')
    hrlg.close()
    print('All current list of confirmed hang registers have been saved to C>>Users>>pgsvlab>>PythonSv>>Aggressive_logs>>hang_regs.log')

def export_attr_all(choice,content,aa):
    if choice == 'open':
        aa = open("attr_all.log","a")
    elif choice == 'close':
        aa.close()
    elif choice == 'store':
        aa.write(content)
        aa.write('\n')
    return aa
	
def export_invalidate(choice,content,invf,vf):
    if choice == 'open':
        invf = open("no_attr_fields.log","a")
        vf = open("attr_fields.log","a")
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
    with open(script_path, "r") as file:
        recommend_logpath = file.read()
    while True:
        try:
            new_directory = os.path.join(recommend_logpath, 'Aggressive_logs')
            os.chdir(new_directory+str(log_num))
        except:
            break
        log_num+=1

def goto_default_path():#Assume C:\Users\pgsvlab\PythonSv is the default log file for all systems.
    with open(script_path, "r") as file:
        recommend_logpath = file.read()
    os.chdir(recommend_logpath)
