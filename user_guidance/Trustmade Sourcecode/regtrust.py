###############################################################################
# INTEL CONFIDENTIAL
# Copyright 2019 Intel Corporation All Rights Reserved.
#
# The source code contained or described herein and all documents related to
# the source code ("Material") are owned by Intel Corporation or its suppliers
# or licensors. Title to the Material remains with Intel Corporation or its
# suppliers and licensors. The Material may contain trade secrets and
# proprietary and confidential information of Intel Corporation and its
# suppliers and licensors, and is protected by worldwide copyright and trade
# secret laws and treaty provisions. No part of the Material may be used,
# copied, reproduced, modified, published, uploaded, posted, transmitted,
# distributed, or disclosed in any way without Intel's prior express written
# permission.
#
# No license under any patent, copyright, trade secret or other intellectual
# property right is granted to or conferred upon you by disclosure or delivery
# of the Materials, either expressly, by implication, inducement, estoppel or
# otherwise. Any license under such intellectual property rights must be
# express and approved by Intel in writing.
###############################################################################
# Standard
import re
import os
# Third
# Local
import __main__
from namednodes import sv
from pysvtools.trustmate.libs.logheader import Log
from pysvtools.trustmate.libs.testresults import TestResults
from pysvtools.trustmate.libs.componentmanager import get_component


SUPPORTED_COMPONENT = ['cpu', 'socket', 'pch', 'spch0', 'pch0', 'gfxcard0']


class RegTrust:

    def __init__(self, type_component, root, directory=None,sub_comp=None):
        self.root = root
        self.type_component = type_component
        if sub_comp:
            self.reg_list = []
            temp_reg_list = sub_comp.search('')
            for item in temp_reg_list:
                self.reg_list.append(sub_comp.get_by_path(item))
        else:
            self.reg_list = []
            temp_reg_list = root.search('')
            for item in temp_reg_list:
                self.reg_list.append(root.get_by_path(item))
        self.directory = directory
        self.reg_name_statistics = {}
        self.reg_name_sorted = ''
        self.total_len = 0
        self.__get_component()
        self.current_list = []

    def __get_header_lines(self):
        self.__get_component()
        lines = ''
        if self.type_component in SUPPORTED_COMPONENT:
            lines = 'import __main__\n'
            if self.type_component == 'cpu':
                return lines + 'cpu = __main__.cpu\n'
            elif self.type_component == 'pch':
                return lines + 'pch = __main__.pch\n'
            elif self.type_component == 'pch0':
                lines = 'from namednodes import sv\n'
                return lines + 'pch0 = sv.pch0\n\n'
            elif self.type_component == 'gfxcard0':
                lines = 'from namednodes import sv\n'
                return lines + 'gfxcard0 = sv.gfxcard0\n\n'
            elif self.type_component == 'spch0':
                lines = 'from namednodes import sv\n'
                return lines + 'spch0 = sv.pch.get_all()[0]\n\n'
            elif self.type_component == 'socket':
                return lines + 'socket = __main__.socket\n'
        elif self.type_component.startswith('socket') and self.__is_socket_num():
            lines = 'from namednodes import sv\n'
            num = int(self.type_component.replace('socket',''))
            lines = lines + 'socket_list = sv.socket.get_all()\n'
            return lines + 'socket{0} = socket_list[{0}]\n\n'.format(num)
        return ''

    def __get_component(self):
        if self.type_component in SUPPORTED_COMPONENT:
            if self.type_component == 'cpu':
                global cpu
                cpu = __main__.cpu
            elif self.type_component == 'pch':
                global pch
                pch = __main__.pch
            elif self.type_component == 'socket':
                global socket
                socket = __main__.socket
            elif self.type_component == 'pch0':
                global pch0
                pch0 = sv.pch0
            elif self.type_component == 'gfxcard0':
                global gfxcard0
                gfxcard0 = sv.gfxcard0
            elif self.type_component == 'spch0':
                global spch0
                spch0 = sv.pch.get_all()[0]
        elif self.type_component.startswith('socket') and self.__is_socket_num():
            socket_list = sv.socket.get_all()
            num_sockets = len(socket_list)
            if self.type_component.endswith('0'):
                global socket0
                socket0 = socket_list[0]
            elif self.type_component.endswith('1'):
                global socket1
                socket1 = socket_list[1]
            elif self.type_component.endswith('2'):
                global socket2
                socket2 = socket_list[2]
            elif self.type_component.endswith('3'):
                global socket3
                socket3 = socket_list[3]

    def __intersection(self, lst1, lst2):
        lst3 = [value for value in lst1 if value in lst2]
        return lst3

    def __diference(self, lst1, lst2):
        lst3 = [value for value in lst1 if value not in lst2]
        return lst3

    def __is_socket_num(self):
        m = re.match(r"socket(\d)", self.type_component)
        if m is not None:
            return True
        return False

    def current_list_string(self):
        for item in self.current_list:
            print(item.path)

    def get_syntax_errors(self,reg_list_to_search=None, max_regs=0):
        count = 0
        header_lines = self.__get_header_lines()
        test_results = TestResults()
        if reg_list_to_search:
            register_list = reg_list_to_search
        else:
            register_list = self.reg_list

        log = Log('syntax_errors', 'py', self.directory)
        log.msg(header_lines)
        log.msg('reg_list = [')
        for item in register_list:

            reg_name = item.path

            try:
                value = eval(reg_name)
            except SyntaxError:
                log.msg('    {},'.format(reg_name))
                test_results.add_pass_reg()
            except AttributeError:
                log.msg('    {},'.format(reg_name))
                test_results.add_pass_reg()

            if max_regs != 0:
                count += 1
                if count == max_regs:
                    break

        log.msg(']')
        log.close_file()

        if max_regs != 0:
            total_len = max_regs
        else:
            total_len = len(self.reg_list)

        print("Total Registers: {}".format(total_len))
        print("Total Registers passed: {}".format(test_results.get_pass_reg()))
        log.close_file()

    def send_current_list_to_file(self):
        header_lines = self.__get_header_lines()
        log = Log('reglist', 'py', self.directory)
        log.msg(header_lines)
        log.msg('reg_list = [')
        for item in self.current_list:
            log.msg('    {},'.format(item.path))
        log.msg(']')
        log.close_file()

    def reg_sanity(self, max_regs=0):
        log_reg = Log('reg_trust', self.directory)
        log_reg.init_table_3('Field Name', 'Total Appearances', 'Total Percentage')

        count = 0
        for item in self.reg_list:

            reg_name = self.type_component + '.' + item
            try:
                reg_name_dic = eval(reg_name + ".info")
            except (SyntaxError, AttributeError):
                print('Problem with reg: {}'.format(reg_name))
                continue

            for item in reg_name_dic:
                try:
                    self.reg_name_statistics[item]['total_appearences'] += 1
                except KeyError:
                    self.reg_name_statistics[item] = {
                        'total_appearences': 1,
                        'percentage_in_all': 0
                    }

            if max_regs != 0:
                count += 1
                if count == max_regs:
                    break
        if max_regs != 0:
            total_len = max_regs
        else:
            total_len = len(self.reg_list)
        for item in self.reg_name_statistics:
            reg_total = self.reg_name_statistics[item]['total_appearences']
            percentage_total = (reg_total / total_len) * 100
            percentage_total = round(percentage_total, 2)
            self.reg_name_statistics[item]['percentage_in_all'] = percentage_total

        self.total_len = total_len
        self.reg_name_sorted = sorted(self.reg_name_statistics.items(), key=lambda x: x[1]['total_appearences'],
                                      reverse=True)

        for item in self.reg_name_sorted:
            log_reg.add_to_table_3(item[0], item[1]['total_appearences'], item[1]['percentage_in_all'])

        log_reg.table_show()
        log_reg.msg("Total Registers: {}".format(self.total_len))
        log_reg.msg("Total Field Name Types: {}".format(len(self.reg_name_statistics)))
        log_reg.close_file()

    def check_for_fields(self, fields_searched,strict_mode=True, reg_list_to_search=None, max_regs=0):
        fields_searched.sort()
        test_results = TestResults()
        self.current_list = []

        if reg_list_to_search:
            register_list = reg_list_to_search
        else:
            register_list = self.reg_list

        log_reg = Log('check_for_fields', self.directory)
        log_reg.init_table_3('Register', 'Status', 'Values')

        count = 0
        for item in register_list:

            reg_name = item.path

            try:
                reg_name_dic = eval(reg_name + ".info")
            except SyntaxError:
                print('Syntax Error: {}'.format(reg_name))
                continue
            except AttributeError:
                print('Attribute Error: {}'.format(reg_name))
                continue

            if strict_mode:
                lst3 = self.__intersection(reg_name_dic, fields_searched)

                lst3.sort()

                if lst3 == fields_searched:
                    values = {}
                    for i in fields_searched:
                        values[i] = eval(reg_name + ".info['{}']".format(i))

                    log_reg.add_to_table_3(reg_name, 'Passed', values)
                    test_results.add_pass_reg()
                    self.current_list.append(eval(reg_name))
            else:
                lst3 = self.__intersection(reg_name_dic, fields_searched)

                lst3.sort()

                if lst3.__len__() > 0:
                    values = {}

                    for i in lst3:
                        values[i] = eval(reg_name + ".info['{}']".format(i))

                    log_reg.add_to_table_3(reg_name, 'Passed', values)
                    test_results.add_pass_reg()
                    self.current_list.append(eval(reg_name))

            if max_regs != 0:
                count += 1
                if count == max_regs:
                    break

        if max_regs != 0:
            total_len = max_regs
        else:
            total_len = len(register_list)

        self.total_len = total_len

        log_reg.table_show()
        log_reg.msg("Total Registers Searched: {}".format(self.total_len))
        log_reg.msg("Total Registers Passed: {}".format(test_results.get_pass_reg()))
        log_reg.close_file()

        if len(self.current_list) > 0:
            print("You will have the list with the registers in the variable current_list of your object")
            print("You can pass this list as an argument to narrow the search")
        else:
            print("Registers with this fields were not found")

    def check_for_fields_negative(self, fields_searched,strict_mode=True, reg_list_to_search=None, max_regs=0):
        fields_searched.sort()
        self.current_list = []
        test_results = TestResults()
        if reg_list_to_search:
            register_list = reg_list_to_search
        else:
            register_list = self.reg_list

        log_reg = Log('check_for_fields_negative', self.directory)
        log_reg.init_table_3('Register', 'Fields', 'Missing')

        count = 0
        for item in register_list:

            reg_name = item.path

            try:
                reg_name_dic = eval(reg_name + ".info")
            except SyntaxError:
                print('Syntax Error: {}'.format(reg_name))
                continue
            except AttributeError:
                print('Attribute Error: {}'.format(reg_name))
                continue

            if strict_mode:
                lst3 = self.__diference(fields_searched, reg_name_dic)

                lst3.sort()

                if lst3 == fields_searched:
                    log_reg.add_to_table_3(reg_name, fields_searched, fields_searched)
                    self.current_list.append(eval(reg_name))
                    test_results.add_pass_reg()
            else:
                lst3 = self.__diference(fields_searched, reg_name_dic)

                lst3.sort()

                if lst3.__len__() > 0:

                    log_reg.add_to_table_3(reg_name, fields_searched, lst3)
                    self.current_list.append(eval(reg_name))
                    test_results.add_pass_reg()

            if max_regs != 0:
                count += 1
                if count == max_regs:
                    break

        if max_regs != 0:
            total_len = max_regs
        else:
            total_len = len(register_list)

        self.total_len = total_len

        log_reg.table_show()
        log_reg.msg("Total Registers Searched: {}".format(self.total_len))
        log_reg.msg("Total Registers Passed: {}".format(test_results.get_pass_reg()))
        log_reg.close_file()

        if len(self.current_list) > 0:
            print("You will have the list with the registers in the variable current_list of your object")
            print("You can pass this list as an argument to narrow the search")
        else:
            print("Registers with this fields were not found")

    def value_in_fields(self, values_searched,strict_mode=True, verbose=1, reg_list_to_search=None, max_regs=0):
        self.current_list = []

        keys_values = values_searched.keys()
        test_results = TestResults()
        if reg_list_to_search:
            register_list = reg_list_to_search
        else:
            register_list = self.reg_list

        if verbose:
            log_reg = Log('value_in_fields', self.directory)
            log_reg.init_table_3('Register', 'Status', 'Values')

        count = 0
        for item in register_list:
            reg_name = item.path

            values = {}

            for key in keys_values:

                try:
                    value = eval(reg_name + ".info['" + key + "']")

                    if value in values_searched[key]:
                        values[key] = value
                except KeyError:
                        values[key] = False
                except SyntaxError:
                    print('Syntax Error: {}'.format(reg_name))
                    break
                except AttributeError:
                    break

            if values:
                if strict_mode:
                    if values.__len__() == values_searched.__len__():
                        gotten_key_values = values.keys()
                        found = False
                        for key in gotten_key_values:
                            if values[key] in values_searched[key]:
                                found = True
                            else:
                                found = False
                                break
                        if found:
                            if verbose:
                                log_reg.add_to_table_3(reg_name,'Passed', values)
                            self.current_list.append(eval(reg_name))
                            test_results.add_pass_reg()
                else:
                    last_dict = {}
                    at_least_one = False

                    gotten_key_values = values.keys()
                    for key in gotten_key_values:
                        if values[key] in values_searched[key]:
                            at_least_one = True
                            last_dict[key] = values[key]

                    if at_least_one:
                        if verbose:
                            log_reg.add_to_table_3(reg_name, 'Passed', last_dict)
                        self.current_list.append(eval(reg_name))
                        test_results.add_pass_reg()

            if max_regs != 0:
                count += 1
                if count == max_regs:
                    break

        if max_regs != 0:
            total_len = max_regs
        else:
            total_len = len(register_list)

        self.total_len = total_len

        if verbose:
            log_reg.table_show()
            log_reg.msg("Total Registers: {}".format(self.total_len))
            log_reg.msg("Total Registers Passed: {}".format(test_results.get_pass_reg()))
            log_reg.close_file()

        if len(self.current_list) > 0 and verbose:
            print("You will have the list with the registers in the variable current_list of your object")
            print("You can pass this list as an argument to narrow the search")

    def no_info_registers(self,reg_list_to_search=None, max_regs=0):
        count = 0
        header_lines = self.__get_header_lines()
        test_results = TestResults()

        if reg_list_to_search:
            register_list = reg_list_to_search
        else:
            register_list = self.reg_list

        log = Log('no_info', 'py', self.directory)
        log.msg(header_lines)
        log.msg('reg_list = [')
        for item in register_list:

            reg_name = item.path

            try:
                reg_name_dic_quantity = eval(reg_name + ".info.__len__()")
                if reg_name_dic_quantity == 0:
                    log.msg('    {},'.format(reg_name))
                    test_results.add_pass_reg()
            except SyntaxError:
                print('Syntax Error: {}'.format(reg_name))
                continue
            except AttributeError:
                print('Attribute Error: {}'.format(reg_name))
                continue

            if max_regs != 0:
                count += 1
                if count == max_regs:
                    break

        log.msg(']')
        log.close_file()

        if max_regs != 0:
            total_len = max_regs
        else:
            total_len = len(self.reg_list)

        print("Total Registers: {}".format(total_len))
        log.msg("Total Registers Passed: {}".format(test_results.get_pass_reg()))
        log.close_file()

    # def registers_no_value(self,reg_list_to_search=None, max_regs=0):
    #     count = 0
    #     header_lines = self.__get_header_lines()
    #
    #     if reg_list_to_search:
    #         register_list = reg_list_to_search
    #     else:
    #         register_list = self.reg_list
    #
    #     log = Log('registers_no_value', 'py', self.directory)
    #     log.msg(header_lines)
    #     log.msg('reg_list = [')
    #     for item in register_list:
    #
    #         if not reg_list_to_search:
    #             reg_name = self.type_component + '.' + item
    #         else:
    #             reg_name = self._get_full_name(item)
    #
    #         try:
    #             value = eval('{}.{}'.format(reg_name,'read()'))
    #         except SyntaxError:
    #             print('Syntax Error: {}'.format(reg_name))
    #             continue
    #         except AttributeError:
    #             print('Attribute Error: {}'.format(reg_name))
    #             continue
    #         except:
    #             log.msg('    {},'.format(reg_name))
    #
    #         if max_regs != 0:
    #             count += 1
    #             if count == max_regs:
    #                 break
    #
    #     log.msg(']')
    #     log.close_file()
    #
    #     if max_regs != 0:
    #         total_len = max_regs
    #     else:
    #         total_len = len(self.reg_list)
    #
    #     print("Total Registers: {}".format(total_len))
    #     log.close_file()