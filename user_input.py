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

    def dump_choice(auto):
        if auto == False:
            choice = input('Dump Log File?[y/n]: ')
        elif auto == True:
            choice = 'y'
        if choice in ['y','yes','']:
            return 0
        elif choice in ['n','no']:
            return 1

    def disp_error_reg_choice(error_names,auto):
        if auto == True:
            choice = 'n'
        elif auto == False:
            choice = input('Display error regs?(y/n)')
        if choice == 'y' or choice == '':
            print('-'*100)
            for error_name in error_names:
                print(error_name)
            print('-'*100)
        print(f"{Fore.LIGHTBLUE_EX}There's {len(error_names)} error registers.")
        print('All the error registers names have been saved to C>>Users>>pgsvlab>>Documents>>PythonSv>>error_reg.py.'+Fore.RESET)
   
class Exec:
    def _auto_generate_print_limit(total_field2print):
        if total_field2print < 10:
            return total_field2print
        else:
            return 10

    def print_limit(total_field2print,reserved_print_limit,auto):
        loop=0
        while loop == 0:
            if auto == True:
                num2print = Exec._auto_generate_print_limit(total_field2print)
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
    def disp_error_choice(Error, error_info, auto):
        if Error > 0:
            if auto:
                chk_choice = 'y'
            else:
                chk_choice = input('Check Errors?(y/n): ')
        else:
            chk_choice = 'n'
        if chk_choice.lower() in ['y','yes','']:
            msg_sorted = track.track_dif_errors(error_info)
            disp_choice = 0
            disp.error_table(msg_sorted)
            while disp_choice != 'end':
                if auto:
                    disp_choice == ''
                else:
                    disp_choice = input('Which error of registers to display?(Enter=All;"end"=stop):')
                if disp_choice != "end":
                    disp.disp_all_errors(disp_choice,msg_sorted,error_info)
                
    def disp_hang_choice(fail_reason,auto):
        if 'hang' in fail_reason:
            if auto:
                chk_choice = 'y'
            else:
                while True:
                    chk_choice = input('Check Hang registers?(y/n): ')
                    if chk_choice.lower() in ['yes','y']:
                        break
                    elif chk_choice.lower() in ['no','n']:
                        break
                    print('Pls enter properly!')
        else:
            chk_choice = 'n'
        return chk_choice.lower()
        
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

