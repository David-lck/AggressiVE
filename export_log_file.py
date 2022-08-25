import tracking as track

def export(choice,content,alg,flg):#Write/store only
    dump_mode = "a" if choice == "open" else "w"
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
    
def export_badname(choice,content,ilg):
    if choice == 'open':
        ilg = open("bad_name_regs.log","w")
    elif choice == 'close':
        ilg.close()
    elif choice == 'store':
        ilg.write(content)
        ilg.write('\n')
    return ilg
	
def export_regs(pass_regs, fail_regs, error_regs, sus_hang_regs):
    prlg, frlg, erlg, shrlg = '', '', '', ''
    prlg = track.create_pass_regs_log(prlg)
    frlg = open("fail_regs.log","w")
    erlg = open("error_regs.log","w")
    shrlg = open("sus_hang_regs.log","w")
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
        shrlg.write(sus_hang_reg)
        shrlg.write('\n')
    print('All current list of pass registers have been saved to C>>Users>>pgsvlab>>PythonSv>>pass_regs.log')
    print('All current list of pass registers have been saved to C>>Users>>pgsvlab>>PythonSv>>fail_regs.log')
    print('All current list of error registers have been saved to C>>Users>>pgsvlab>>PythonSv>> error_regs.log')
    print('All current list of suspect hang registers have been saved to C>>Users>>pgsvlab>>PythonSv>>sus_hang_regs.log')
    prlg.close()
    frlg.close()
    erlg.close()
    shrlg.close()
    
def export_hang_regs(confirm_hang_regs):
    hrlg = ''
    hrlg = open("hang_regs.log","w")
    for reg in confirm_hang_regs:
        hrlg.write(reg)
        hrlg.write('\n')
    hrlg.close()
    print('All current list of confirmed hang registers have been saved to C>>Users>>pgsvlab>>PythonSv>>hang_regs.log')

def export_attr_all(choice,content,aa):
    if choice == 'open':
        aa = open("attr_all.log","w")
    elif choice == 'close':
        aa.close()
    elif choice == 'store':
        aa.write(content)
        aa.write('\n')
    return aa
    
def export_invalidate(choice,content,invf,vf):
    if choice == 'open':
        invf = open("no_attr_fields.log","w")
        vf = open("attr_fields.log","w")
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

def export_write_pass(plg,content):
    plg.write(content)
    plg.write('\n')
    return plg