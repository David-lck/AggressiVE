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
import display_output as disp
import tracking as track
import read_write as rw
import aggressive as ags
from pysvtools.asciitable import AsciiTable as Table
import colorama
from colorama import Fore

class Pre_test:
    def _get_access_method(input_reg):
        #try:
        avail_access = eval(input_reg+'.getaccesschoices()')
        unit = input_reg.split('.')
        #except:
        #    unit = input_reg.split('.')
        #    input_reg = (input_reg.split('.'))[:-1]
        #    d_i_r = ''
        #    for temp in input_reg:
        #        if input_reg.index(temp)==3:
        #            break
        #        d_i_r+=temp+'.'
        #    d_i_r = d_i_r[:-1]
        #    avail_access = eval(d_i_r+'.getaccesschoices()')
        return avail_access,unit

    def _access_choice_input(avail_access):
        loop = 0
        while loop == 0:
            chosen_access = input('Access Method: ')
            if chosen_access in avail_access['default'] or chosen_access == '':
                loop = 1
        return chosen_access
        
    def access_choice(input_reg):
        log_store = []
        if len(input_reg.split('.')) != 1:#for input_reg = ip/reg only
            (avail_access,unit) = Pre_test._get_access_method(input_reg)
            disp.disp_avail_access(avail_access)
            chosen_access = Pre_test._access_choice_input(avail_access)
        else:#for die level
            chosen_access = ''
        if chosen_access != '':#not default
            eval(unit[0]+".setaccess('"+chosen_access+"')")
            temp = ''
            input_reg = input_reg.split('.')
            for n_level in input_reg:
                if temp=='':
                    temp+=n_level
                else:
                    temp+='.'+n_level
                if eval(temp+'.getaccess()') == chosen_access:
                    print(f'{Fore.LIGHTBLUE_EX + chosen_access} has successfully been set in {temp + Fore.RESET}')
                    log_store.append(f'{chosen_access} has successfully been set in {temp}')
                else:
                    print(f'{Fore.LIGHTBLUE_EX+chosen_access} has unsuccessfully been set in {temp+Fore.RESET}')
                    log_store.append(f'{chosen_access} has unsuccessfully been set in {temp}')
        else:#default
            print(f'{Fore.LIGHTBLUE_EX}User has chosen default access for {input_reg}.')
            log_store.append(f'User has chosen default access for {input_reg}.')
            default_access = eval(input_reg+'.getaccess()')
            print(f'Default access for {input_reg} is {default_access}.{Fore.RESET}')
            log_store.append(f'Default access for {input_reg} is {default_access}.')
        return log_store

    def attr_choice(avai_attrs,auto,auto_attr):
        if auto == True:
            choice = auto_attr
        elif auto == False:
            choice = input('Attribute (Enter for All): ')
        if choice.isdigit() and choice != '':
            choice = avai_attrs[int(choice)-1]
        elif choice != '' and choice.isdigit() == False:
            choice = choice.lower()
            #choice = track.Pre_test.track_attr_typo(avai_attrs,choice)
        return choice
        
    def invalidate_choice(auto):
        if auto == False:
            result_form = ''
        elif auto == True:
            result_form = '3'
        while result_form not in ['1','2','3']:
            result_form = input('Display result in 1)IP form or 2)field form 3)Skip?')
            if result_form == '':
                result_form = '3'
        return result_form

    def disp_badname_reg_choice(badname_registers,auto):
        if auto == True:
            choice = 'n'
        elif auto == False:
            choice = input('Display error regs?(y/n)')
        if choice == 'y' or choice == '':
            print('-'*100)
            for badname_register in badname_registers:
                print(badname_register)
            print('-'*100)
        print(f"{Fore.LIGHTBLUE_EX}There's {len(badname_registers)} unacceptable name registers.")
        print('All the error registers names have been saved to C>>Users>>pgsvlab>>Documents>>PythonSv>>bad_name_regs.py.'+Fore.RESET)
   
class Exec:
    def print_limit(total_field2print,reserved_print_limit,auto):
        loop=0
        while loop == 0:
            if auto == True:
                num2print = total_field2print
            elif auto == False:
                print('')
                num2print = input(f'Display_Number[Left:{total_field2print}]["end"=stop]: ')
            if num2print == '':
                num2print = reserved_print_limit
            if num2print != 'end':
                num2print = int(num2print)
            loop = 1
            if num2print != 'end' and num2print > int(total_field2print):
                print(f'Please insert a value less than or equal to {total_field2print}!')
                loop=0
            if num2print == 0:
                loop = 0
        reserved_print_limit = num2print
        return num2print,reserved_print_limit
        
class Post_test:
    def disp_error_choice(Error, error_messages, auto, is_cont):
        msg_sorted = track.track_dif_errors(error_messages)
        disp_choice = 0
        disp.error_table(msg_sorted)
        if is_cont:
            elg = open("AggressiVE_cont_error.log","a")
        else:
            elg = open("AggressiVE_error.log","a")
        while disp_choice != 'end':
            if auto:
                disp_choice == ''
            else:
                disp_choice = input('Which error of registers to display?(Enter=All;"end"=stop):')
            if disp_choice != "end":
                printed_error_msg = disp.disp_all_errors(disp_choice,msg_sorted,error_messages)
                elg.write(printed_error_msg)
                elg.write('\n')
        elg.close()
        if is_cont:
            print('All the printed error infos have been saved in C>>Users>>pgsvlab>>PythonSv>>AggressiVE_error.log')
        else:
            print('All the printed error infos have been saved in C>>Users>>pgsvlab>>PythonSv>>AggressiVE_cont_error.log')

    def choose_post_test(Pass,Fail,Error,Hang,alg,flg,fail_infos,sus_hang_infos,error_infos,is_cont):
        avail_choice = []
        print('Second Validation!')
        if Pass != 0:
            avail_choice.append('Pass Registers.')
        if Fail != 0:
            avail_choice.append('Fail Registers.')
        if Hang != 0:
            avail_choice.append('Hang Registers.')		
        if Error != 0:
            avail_choice.append('Errors Check.')
        while True:
            for choice in avail_choice:
                print(f'{str(avail_choice.index(choice)+1)}. {choice}')

            while True:
                val_choice = input('Choice["end" to exit]: ')
                if val_choice in ['1','2','3','4','end']:
                    break
                print('Please enter properly!')

            if val_choice == 'end':
                break
            elif 'Pass' in avail_choice[int(val_choice)-1]:
                (alg, flg) = rw.Post_test.validate_pass(alg, flg,is_cont)
                avail_choice.remove('Pass Registers.')
            elif 'Fail' in avail_choice[int(val_choice)-1]:
                (alg, flg) = ags.Post_test._fail_main(fail_infos, alg, flg,is_cont)#run post feature (Validate or display fail fields only).
                avail_choice.remove('Fail Registers.')
            elif 'Hang' in avail_choice[int(val_choice)-1]:
                [sus_hang_regs] = sus_hang_infos
                (alg, flg) = rw.Post_test.validate2_hang_regs(sus_hang_regs, alg, flg, is_cont)
                avail_choice.remove('Hang Registers.')
            elif 'Error' in avail_choice[int(val_choice)-1]:
                [error_messages] = error_infos
                Post_test.disp_error_choice(Error,error_messages,auto,is_cont)
                avail_choice.remove('Errors Check.')
        return alg, flg
            
        
    def fail_val_choice(auto):
        if auto == True:
            return 2
        loop = 0
        while loop == 0:
            print('''There are Fail registers/fields
1. Re-print
2. Re-write
3. Exit''')
            chosen_fail_val = input('Choice: ')
            if int(chosen_fail_val) in [1,2,3]:
                loop = 1
            else:
                print('Please enter properly!')
        return int(chosen_fail_val)


