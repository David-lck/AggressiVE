
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
    
def export_invalid(choice,content,ilg):
    if choice == 'open':
        ilg = open("error_reg.log","w")
    elif choice == 'close':
        ilg.close()
    elif choice == 'store':
        ilg.write(content)
        ilg.write('\n')
    return ilg
    
def export_error(choice,content,elg):
    if choice == 'open':
        elg = open("error.log","w")
    elif choice == 'close':
        elg.close()
    elif choice == 'store':
        elg.write(content+' \n')
    return elg
    
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
        invf = open("invalid_fields.log","w")
        vf = open("valid_fields.log","w")
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

def test():
    alg = open("aaa.log", "w")
    alg.write("test")
    alg.write('\n')
    alg.close()
