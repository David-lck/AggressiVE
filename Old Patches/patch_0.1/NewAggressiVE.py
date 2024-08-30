from pysvtools import asciitable
try:
	import __main__
	soc = __main__.soc
except:
	from builtins import *
	from builtins import str
	from builtins import range
	from builtins import object
	import namednodes as _namednodes
	from namednodes import sv as _sv
	cpu = _sv.socket.get_all()[0]

#Stop at 451 row.
#Move to GUI.
print('''
          A
        /   \                                                              __              __   _________
       /  A  \                                                            (  \            /  ) |   ______|
      /  /_\  \                                                            \  \          /  /  |  |
     /  _____  \                                                        _   \  \        /  /   |  |______
    /  /     \  \                                                      |_|   \  \      /  /    |   ______|
   /  /	      \  \      _____   _____   ____   ____     ____    ____    _     \  \    /  /     |  |
  /  /         \  \    /  ___) /  ___) |  __| /  _  )  (    _) (    _) | |     \  \  /  /      |  |
 /  /           \  \  (  (__/|(  (__/| | |   (  (/ /   _\  \   _\  \   | |      \  \/  /       |  |______
(__/             \__)  \_____| \_____| |_|    \_____| (_____) (_____)  |_|       \____/        |_________|
<Aggress Register Spec iVE Tools>
Available Functions:
	- .check_attribute('IP_Name') = Check the num of reg w/ specific attr & display the name of reg(s).
	- .check_reg_width('IP_Name') = Check the num of reg w/ specific range of reg_width & display the name of reg(s).
	- .main('IP_Name') = Do the read/write.

Example: main('cpu.gfx.display')  
''')



class Val_Variables:
	def combine_order(self,combine_bit_order,combine_w1_order,combine_r1_1_order,combine_r1_2_order,combine_w2_order,combine_r2_1_order,combine_r2_2_order,combine_w3_order,combine_r3_order):
		self.combine_bit_order = combine_bit_order
		self.combine_w1_order = combine_w1_order
		self.combine_r1_1_order = combine_r1_1_order
		self.combine_r1_2_order = combine_r1_2_order
		self.combine_w2_order = combine_w2_order
		self.combine_r2_1_order = combine_r2_1_order
		self.combine_r2_2_order = combine_r2_2_order
		self.combine_w3_order = combine_w3_order
		self.combine_r3_order = combine_r3_order
	def rdwr_valueorder(self,bit_order,w1_order,r1_1_order,r1_2_order,w2_order,r2_1_order,r2_2_order,w3_order,r3_order):
		self.bit_order = bit_order
		self.w1_order = w1_order
		self.r1_1_order = r1_1_order
		self.r1_2_order = r1_2_order
		self.w2_order = w2_order
		self.r2_1_order = r2_1_order
		self.r2_2_order = r2_2_order
		self.w3_order = w3_order
		self.r3_order = r3_order
	def rdwr_value(self,w1,w2,r1_1,r1_2,r2_1,r2_2,w3,r3,rs1,rs2):
		self.w1 = w1
		self.w2 = w2
		self.r1_1 = r1_1
		self.r1_2 = r1_2
		self.r2_1 = r2_1
		self.r2_2 = r2_2
		self.w3 = w3
		self.r3 = r3
		self.rs1 = rs1
		self.rs2 = rs2
	def combine_all_list_components(input):
		output=[]
		for temp_one in input:
			for to in temp_one:
				output.append(to)
		return output



def test(full_ip):
	#my_list = ['foo', 'fob', 'faz', 'funk']
	#string = 'bar'
	#my_new_list = [x + string for x in my_list]
	#print (my_new_list)
    regs = eval(full_ip+".search('')")
    n = 0
    for reg in regs:
        try:
            full_name = full_ip + '.' + reg
            attr_status = eval(full_name+".info")
            for attr_status_1by1 in attr_status:
                if attr_status_1by1 == 'attribute':
                    info = 'Attribute'
                    break
            n+=1
        except:
            print(full_name)
    print(n)
	

def bin2hex(input):
	if input != '-':
		output = hex(int(str(input), 2))
	else:
		output = input
	return output

def bin2dec(input):
	if input != '-':
		output=int(input,2)
		output = (str(output))
	else:
		output=input
	return output

def hex2bin(input):
	input = str(input)
	if input != '-':
		scale = 16
		i=0
		str(input)
		output = bin(int(input, scale)).zfill(8)
		for op in output:
			i+=1
			if op=='b':
				output=output[i:]
				break
	else:
		output=input
	return output

def dec2bin(input):
	if input != '-':
		output=bin(int(input))
		i=0
		for op in output:
			i+=1
			if op== 'b':
				output=output[i:]
				break
	else:
		output = input
	return output

	
def num_display_user_input(total_num,left_num,displaying,previous_display_num,display_num,looped_num):
	if displaying == 0:
		displat_num = 'retype'
		while display_num == 'retype':
			if left_num == total_num:
				display_num = str(input('There are '+str(left_num)+' registers to be displayed, how many reg to display first?["end"=stop]: '))
			else:
				left_num=str(left_num)
				display_num = str(input('There are '+str(left_num)+' registers left, how many reg to display first?["end"=stop]: '))
			left_num=int(left_num)
			if display_num == '':
				display_num = previous_display_num
			elif display_num == 'end':
				break
			elif ord(display_num[0]) in range (49,57):
				display_num = int(display_num)
				previous_display_num = display_num
			if display_num == '0':
				display_num = 'retype'
			elif display_num > left_num:
				print('Please enter the value which is not higher than the number of registers left!')
				display_num = 'retype'
		displaying = 1
		looped_num = 0
	return left_num,displaying,previous_display_num,display_num,looped_num

def num_display_ending_part(x,total_num,displaying,display_num,Pass,Fail,Unknown,invalid_token,alg,flg):
	if looped_num == int(display_num) or current_num == total_num:
		print(x.getTableText())
		print('Pass: '+str(Pass)+'reg(s)')
		print('Fail: '+str(Fail)+'reg(s)')
		print('Unknown: '+str(Unknown)+'reg(s)')
		print('Invalid_token: '+str(invalid_token)+'reg(s)')
		(alg,flg) = export('store',x.getTableText(),alg,flg)
		displaying = 0
	return alg,flg,displaying

def stages_of_rdwr_val(full_reg_name,atjt_statusn,Pass,Fail,chosen_spec_attr):
	i = 0
	vv_combine_order = Val_Variables.combine_order([],[],[],[],[],[],[],[],[])
	#reg_fail = 0
	field_invalid_token = False
	'''read_store determination first'''
	defined_attr = [' ro ',' wo ',' r/w ',' rw/o ',' rsv ',' r/w set ',' rw/s ',' rw/l ',' rw/1c ',' rw/1l ',' rw/1s ',' r/wc ',' ro/swc ']
	for atjt_status in atjt_statusn:					#To loop all the available attributes.
		vv_rdwr_valueorder = Val_Variables.rdwr_valueorder([],[],[],[],[],[],[],[],[])
		i += 1
		'''determinate numbit then read write for a register'''
		#fail_attr = ''
		#Fail_attr = []
		if i == 1:
#for first attribute in that register only
			attr_bitranges_list = attr1_bit
		elif i == 2:
#for second attribute in that register only
			attr_bitranges_list = attr2_bit
		elif i == 3:
#for third attribute in that register only
			attr_bitranges_list = attr3_bit
		elif i == 4:
#for fourth attribute in that register only
			attr_bitranges_list = attr4_bit
		elif i == 5:
#for fifth attribute in that register only
			attr_bitranges_list = attr5_bit
		fields = eval(full_reg_name+'.search("")')
		for a_bitrange in attr_bitranges_list:#a_bitrange = a bit range in an attr. attr_bitranges_list=all bit range in one attr.
			lowerbit_det=0
			upperbit = ''
			lowerbit = ''
#determine upperbit, lowerbit, and numbit.
			for char in a_bitrange:#Eg: a_bitrange'31-22'
				if char == '-':
					lowerbit_det=1
				if lowerbit_det == 0:
					upperbit = str(upperbit)
					upperbit += str(char)
					upperbit = int(upperbit)
				else:
					lowerbit += str(char)
					lowerbit = lowerbit.replace('-','')	
				if lowerbit == '':
					numbit = 1
				elif lowerbit == '0' and upperbit == 0:
					numbit = 1
				else:
					numbit = upperbit - int(lowerbit)+1
#determine the field(s) with the current numbit to run the read/write command on the specific field(s).(sort out for this attr by determine the bit_ranges)
			chosen_fields =[]
			for field in fields:
				lb = eval(full_reg_name+'.'+field+'.info["lowerbit"]')
				nb = eval(full_reg_name+'.'+field+'.info["numbits"]')
				ub = int(lb) + int(nb) - 1
				if ub == int(upperbit):
					chosen_fields.append(field)
				elif lowerbit == '':
					break
				else:
					l = int(lowerbit)
					if int(lb) == int(lowerbit):
						chosen_fields.append(field)
					elif int(lb) > int(lowerbit):
						if int(lb) < int(upperbit):
							chosen_fields.append(field)
#Do read/write field(s) in a bit_range one by one & determine pass/fail/unknown. (For all the defined attributes)
			vv_rdwr_value = Val_Variables.rdwr_value('','','','','','','','','','')
			for chosen_field in chosen_fields:#From upperbit field to lowerbit field.
				#rs1 & rs2
				vv_rdwr_value.rs1 = eval(full_reg_name+'.'+chosen_field)
				vv_rdwr_value.rs2 = eval(full_reg_name+'.'+chosen_field)
				numbit = eval(full_reg_name+'.'+chosen_field+'.info["numbits"]')
				#w1
				if atjt_status in [' ro ',' wo ',' r/w ',' rw/o ',' rsv ']:
					#For w1=1
					vv_rdwr_value.w1 = '1' * numbit
					rw_compare_temp = bin2hex(vv_rdwr_value.w1)
					vv_rdwr_value.w1 = bin2dec(vv_rdwr_value.w1)
					eval(full_reg_name+'.'+chosen_field+'.write('+str(vv_rdwr_value.w1)+')')
				elif atjt_status in [' r/w set ',' rw/s ',' rw/l ',' rw/1c ',' rw/1l ',' rw/1s ',' r/wc ',' ro/swc ']:
					#For w1=0.
					vv_rdwr_value.w1 = 0
					eval(full_reg_name+'.'+chosen_field+'.write('+str(vv_rdwr_value.w1)+')')
				elif atjt_status not in defined_attr and chosen_at == 'Others':
					#For 'Others', w1=1
					vv_rdwr_value.w1 = '1' * numbit
					rw_compare_temp = bin2hex(vv_rdwr_value.w1)
					vv_rdwr_value.w1 = bin2dec(w1)
					eval(full_reg_name+'.'+chosen_field+'.write('+str(vv_rdwr_value.w1)+')')
				#r1_1 & r1_2
				vv_rdwr_value.r1_1 = eval(full_reg_name+'.'+chosen_field)
				vv_rdwr_value.r1_2 = eval(full_reg_name+'.'+chosen_field)
				if atjt_status == ' ro/swc ':
					if str(vv_rdwr_value.r1_1) == '0x0' and str(vv_rdwr_value.r1_2) == '0x0':
						PassFail = 'Pass'
					else:
						PassFail = 'Fail'
						fail_attr = 'ro/swc'
				elif atjt_status == ' r/w ':
					if str(vv_rdwr_value.r1_1) == str(rw_compare_temp):
						PassFail = 'Pass'
					else:
						PassFail = 'Fail'
						fail_attr = 'r/w'
				elif atjt_status in [' wo ',' r/wc ',' rsv ']:
					if str(vv_rdwr_value.r1_1) == '0x0':
						PassFail = 'Pass'
					else:
						PassFail = 'Fail'
						fail_attr = atjt_status[1:-1]
				elif atjt_status in [' ro ',' rw/s ',' r/w set ',' rw/l ',' rw/1c ',' rw/1l ',' rw/1s ']:
					if vv_rdwr_value.r1_1 == vv_rdwr_value.rs2:
						PassFail = 'Pass'
					else:
						PassFail = 'Fail'
						fail_attr = atjt_status[1:-1]
				#w2
				if atjt_status in [' rsv ',' rw/o ',' r/w ',' wo ',' ro ']:
					#For w2=0
					vv_rdwr_value.w2 = 0
					eval(full_reg_name+'.'+chosen_field+'.write('+str(vv_rdwr_value.w2)+')')
				elif atjt_status in [' rw/s ',' r/w set ',' rw/1c ',' rw/1l ',' rw/1s ',' r/wc ',' ro/swc ']:
					#For w2=1.
					vv_rdwr_value.w2 = '1' * numbit
					rw_compare_temp = bin2hex(vv_rdwr_value.w2)
					vv_rdwr_value.w2 = bin2dec(vv_rdwr_valuew2)
					eval(full_reg_name+'.'+chosen_field+'.write('+str(vv_rdwr_value.w2)+')')
				elif chosen_at == 'Others' and atjt_status not in defined_attr:
					#For Others,w2=0
					if atjt_status not in defined_attr:
						vv_rdwr_value.w2 = 0
						eval(full_reg_name+'.'+chosen_field+'.write('+str(vv_rdwr_value.w2)+')')
				#r2_1 & r2_2:
				vv_rdwr_value.r2_1 = eval(full_reg_name+'.'+chosen_field)
				vv_rdwr_value.r2_2 = eval(full_reg_name+'.'+chosen_field)
				if atjt_status == ' ro/swc ':
					if vv_rdwr_value.r2_1 == rw_compare_temp and vv_rdwr_value.r2_2 == rw_compare_temp:
						PassFail = 'Pass'
					else:
						PassFail = 'Fail'
						fail_attr = 'ro/swc'
				elif atjt_status ==  ' ro ':
					if vv_rdwr_value.r2_1 == vv_rdwr_value.rs2:
						PassFail = 'Pass'
					else:
						PassFail = 'Fail'
						fail_attr = 'ro'
				elif atjt_status in [' wo ',' r/w ',' rw/o ',' rw/1c ',' r/wc ',' rsv ']:
					if str(vv_rdwr_value.r2_1) == '0x0':
						PassFail == 'Pass'
					else:
						PassFail == 'Fail'
						fail_attr = atjt_status[1:-1]
				elif atjt_status in [' rw/s ',' r/w set ',' rw/1l ',' rw/1s ']:
					if vv_rdwr_value.r2_1 == rw_compare_temp:
						PassFail == 'Pass'
					else:
						PassFail == 'Fail'
						fail_attr = atjt_status[1:-1]
				#w3
				if atjt_status in [' ro ',' wo ',' r/w ',' rw/o ',' rsv ']:
					#For w3=1
					vv_rdwr_value.w3 = '1' * numbit
					vv_rdwr_value.w3 = bin2dec(vv_rdwr_value.w3)
					eval(full_reg_name+'.'+chosen_field+'.write('+str(vv_rdwr_value.w3)+')')
				elif atjt_status in [' rw/s ',' r/w set ',' rw/1c ',' rw/1l ',' rw/1s ',' r/wc ',' ro/swc ']:
					#For w3=0
					vv_rdwr_value.w3 = 0
					eval(full_reg_name+'.'+chosen_field+'.write('+str(vv_rdwr_value.w3)+')')
				elif atjt_status not in defined_attr and chosen_at == 'Others':
					#For 'Others', w1=1
					vv_rdwr_value.w3 = '1' * numbit
					vv_rdwr_value.w3 = bin2dec(w3)
					eval(full_reg_name+'.'+chosen_field+'.write('+str(vv_rdwr_value.w3)+')')
				#r3
				vv_rdwr_value.r3 = eval(full_reg_name+'.'+chosen_field)
				x='1' * numbit
				x = bin2hex(x)
				if atjt_status in [' ro ',' wo ',' rw/1c ',' r/wc ',' rsv ',' ro/swc ']:
					#r3=0
					if str(vv_rdwr_value.r3) == '0x0':
						PassFail = 'Pass'
					else:
						PassFail = 'Fail'
				elif atjt_status in [' r/w ',' rw/s ',' r/w set ',' rw/o ',' rw/1l ',' rw/1s ']:
					#r3=1
					if vv_rdwr_value.r3 == x:
						PassFail = 'Pass'
					else:
						PassFail = 'Fail'
						fail_attr = atjt_status[1:-1]
				#Extra determination for ro/swc.
				if atjt_status == ' ro/swc ':
					x='1' * numbit
					x = bin2hex(x)
					if str(vv_rdwr_value.rs1) == '0x0' and str(vv_rdwr_value.rs2) == x:
						PassFail == 'Pass'
					else:
						PassFail == 'Fail'
						fail_attr = 'ro/swc'
				
				if fail_attr != '':
					Fail_attr.append(fail_attr)
#Combine the current rw_val info in order list.
				vv_rdwr_value.rs1 = hex2bin(vv_rdwr_value.rs1)
				vv_rdwr_value.rs2 = hex2bin(vv_rdwr_value.rs2)
				vv_rdwr_value.w1=dec2bin(vv_rdwr_value.w1)
				vv_rdwr_value.w2=dec2bin(vv_rdwr_value.w2)
				vv_rdwr_value.w3=dec2bin(vv_rdwr_value.w3)
				vv_rdwr_value.r1_1=hex2bin(vv_rdwr_value.r1_1)
				vv_rdwr_value.r1_2=hex2bin(vv_rdwr_value.r1_2)
				vv_rdwr_value.r2_1=hex2bin(vv_rdwr_value.r2_1)
				vv_rdwr_value.r2_2=hex2bin(vv_rdwr_value.r2_2)
				vv_rdwr_value.r3=hex2bin(vv_rdwr_value.r3)
				if str(vv_rdwr_value.w1) == '0':
					vv_rdwr_value.w1 = '0' * numbit
				W1 += str(vv_rdwr_value.w1)
				if str(vv_rdwr_value.r1_1) == '0':
					vv_rdwr_value.r1_1 = '0' * numbit
				R1_1 += str(vv_rdwr_value.r1_1)
				if vv_rdwr_value.r1_2 != '-':
					if str(vv_rdwr_value.r1_2) == '0':
						vv_rdwr_value.r1_2 = '0' * numbit
					R1_2 += str(vv_rdwr_value.r1_2)
				else:
					R1_2 = str(vv_rdwr_value.r1_2)
				if str(vv_rdwr_value.w2) == '0':
					vv_rdwr_value.w2 = '0' * numbit
				W2 += str(vv_rdwr_value.w2)
				if str(vv_rdwr_value.r2_1) == '0':
					vv_rdwr_value.r2_1 = '0' * numbit
				R2_1 += str(vv_rdwr_value.r2_1)
				if vv_rdwr_value.r2_2 != '-':
					if str(vv_rdwr_value.r2_2) == '0':
						vv_rdwr_value.r2_2 = '0' * numbit
					R2_2 += str(vv_rdwr_value.r2_2)
				else:
					R2_2 = str(vv_rdwr_value.r2_2)
				if vv_rdwr_value.w3 != '-':
					W3 += str(vv_rdwr_value.w3)
				else:
					W3 = str(vv_rdwr_value.w3)
				if vv_rdwr_value.r3 != '-':
					if str(vv_rdwr_value.r3) == '0':
						vv_rdwr_value.r3 = '0' * numbit
					R3 += str(vv_rdwr_value.r3)
				else:
					R3 = str(vv_rdwr_value.r3)	
			if fail_attr != '':
				no_duplicate_fail_attr = list(set(Fail_attr))
				PassFail += '['
				for ndfa in no_duplicate_fail_attr:
					PassFail+=str(ndfa)
					if len(no_duplicate_fail_attr) != 1:
						PassFail+=','
				PassFail += ']'
			vv_rdwr_valueorder.bit_order.append(str(upperbit))
			vv_rdwr_valueorder.w1_order.append(str(W1))
			vv_rdwr_valueorder.r1_1_order.append(str(R1_1))
			vv_rdwr_valueorder.r1_2_order.append(str(R1_2))
			vv_rdwr_valueorder.w2_order.append(str(W2))
			vv_rdwr_valueorder.r2_1_order.append(str(R2_1))
			vv_rdwr_valueorder.r2_2_order.append(str(R2_2))
			vv_rdwr_valueorder.w3_order.append(str(W3))
			vv_rdwr_valueorder.r3_order.append(str(R3))
#combine all info (rw values for all fields which have different attr in one reg) into one for a register
		if chosen_at == 'Others' and PassFail == 'Pass':#NOt complete bcz have to include its behavior and add with the pass or fail.
			PassFail = '-'
		if PassFail != '-':
			combine_bit_order.append(bit_order)
			combine_w1_order.append(w1_order)
			combine_r1_1_order.append(r1_1_order)
			combine_r1_2_order.append(r1_2_order)
			combine_w2_order.append(w2_order)
			combine_r2_1_order.append(r2_1_order)
			combine_r2_2_order.append(r2_2_order)
			combine_w3_order.append(w3_order)
			combine_r3_order.append(r3_order)
			if PassFail == 'Fail' or PassFail == 'Fail (w/ invalid token)':
				reg_fail = 1
		if atjt_status not in defined_attr:
			if reg_fail != 2:
				Unknown+=1
				reg_fail = 2


				
				
	if str(combine_bit_order)[1] == '[':
		combine_bit_order=Val_Variables.combine_all_list_components(combine_bit_order)
		combine_w1_order=Val_Variables.combine_all_list_components(combine_w1_order)
		combine_r1_1_order=Val_Variables.combine_all_list_components(combine_r1_1_order)
		combine_r1_2_order=Val_Variables.combine_all_list_components(combine_r1_2_order)
		combine_w2_order=Val_Variables.combine_all_list_components(combine_w2_order)
		combine_r2_1_order=Val_Variables.combine_all_list_components(combine_r2_1_order)
		combine_r2_2_order=Val_Variables.combine_all_list_components(combine_r2_2_order)
		combine_w3_order=Val_Variables.combine_all_list_components(combine_w3_order)
		combine_r3_order=Val_Variables.combine_all_list_components(combine_r3_order)
	#Determine the bit of invalid token in current register!
	if field_invalid_token == True:
		fields = eval(full_reg_name+'.search("")')
		fw_loop = eval(full_reg_name+'.info')
		for temp_fw in fw_loop:
			if temp_fw == 'size':
				command_fw = 'size'
				break
			elif temp_fw =='FUSE_WIDTH':
				command_fw = 'FUSE_WIDTH'
				break
		valid_token_ub=''
		valid_token_lb=''
		invalid_token_breakpoint = 0
		for field in fields:
			try:
				valid_token_lb=eval(full_reg_name+'.'+field+'.info["lowerbit"]')
				valid_token_nb=eval(full_reg_name+'.'+field+'.info["numbits"]')
				valid_token_ub=str(int(valid_token_lb)+int(valid_token_nb)-1)
				if invalid_token_breakpoint == 1:
					invalid_token_breakpoint=2
			except:
				if invalid_token_breakpoint == 0:
					if valid_token_ub == '' or valid_token_lb == '':
						invalid_token_breakpoint_lb = eval(full_reg_name+'.info["'+command_fw+'"]')
						invalid_token_breakpoint_lb = str(int(invalid_token_breakpoint_lb) + 1)
					invalid_token_breakpoint_ub = valid_token_ub
					invalid_token_breakpoint_lb = valid_token_lb
					invalid_token_breakpoint = 1
			finally:
				if invalid_token_breakpoint==2:
					invalid_token_breakpoint=0
					itl = str(int(valid_token_lb)+1)
					itu = str(int(invalid_token_breakpoint_lb)-1)
					itn = str(int(itu)-int(itl)+1)
					combine_bit_order.append(itu)
					temp_none = '-'*int(itn)
					combine_w1_order += temp_none
					combine_r1_1_order += temp_none
					combine_r1_2_order += temp_none
					combine_w2_order += temp_none
					combine_r2_1_order += temp_none
					combine_r2_2_order += temp_none
					combine_w3_order += temp_none
					combine_r3_order += temp_none
	'''arrange combine value in bit order'''
	if PassFail != '-':
		order=[]
		in_order_bit=[]
		if str(combine_bit_order)[1] == '[':
			loop=0
			while loop < int(len(combine_bit_order)):
				temp_combine=sorted(combine_bit_order[loop])
				in_order_bit.append(temp_combine)
				loop+=1
		else:
			in_order_bit=sorted(combine_bit_order)
		in_order_bit.sort(reverse=True)
		for iob in in_order_bit:
			o=-1
			for cbo in combine_bit_order:
				o+=1
				if iob == cbo:
					order.append(o)
					break
		a=''
		for o in order:
			w1+=combine_w1_order[o]
			r1_1+=combine_r1_1_order[o]
			r1_2+=combine_r1_2_order[o]
			w2+=combine_w2_order[o]
			r2_1+=combine_r2_1_order[o]
			r2_2+=combine_r2_2_order[o]
			w3+=combine_w3_order[o]
			r3+=combine_r3_order[o]
		if field_invalid_token == False:
			w1=bin2hex(w1)
			r1_1=bin2hex(r1_1)
		hyphen=value=0
		for r12 in r1_2:
			if r12 == '-':
				hyphen=1
			elif r12 != '-':
				value=1
		if hyphen == 0 and value == 1:
			r1_2=bin2hex(r1_2)
		elif hyphen == 1 and value == 0:
			r1_2 = '-'
		elif hyphen == 1 and value == 1:
			r1_2=r1_2
		hyphen=value=0
		if field_invalid_token == False:
			w2=bin2hex(w2)
			r2_1=bin2hex(r2_1)	
		for r22 in r2_2:
			if r22 == '-':
				hyphen=1
			elif r22 != '-':
				value=1
		if hyphen == 0 and value == 1:
			r2_2=bin2hex(r2_2)
		elif hyphen == 1 and value == 0:
			r2_2 = '-'
		elif hyphen == 1 and value == 1:
			r2_2=r2_2
		hyphen=value=0
		for w33 in w3:
			if w33 == '-':
				hyphen=1
			elif w33 != '-':
				value=1
		if hyphen == 0 and value == 1:
			w3=bin2hex(w3)
		elif hyphen == 1 and value == 0:
			w3 = '-'
		elif hyphen == 1 and value == 1:
			w3=w3
		hyphen=value=0
		for r33 in r3:
			if r33 == '-':
				hyphen=1
			elif r33 != '-':
				value=1
		if hyphen == 0 and value == 1:
			r3=bin2hex(r3)
		elif hyphen == 1 and value == 0:
			r3 = '-'
		elif hyphen == 1 and value == 1:
			r3=r3
	else:
		PassFail = '-'
	'''store in table!'''
	temp_fw = eval(full_reg_name+'.info')
	for tfw in temp_fw:
		if tfw == 'size':
			FuseWidth=eval(full_reg_name+'.info["size"]')
			FuseWidth=str(FuseWidth)
			break
		elif tfw == 'FUSE_WIDTH':
			FuseWidth=eval(full_reg_name+'.info["FUSE_WIDTH"]')
			FuseWidth=str(FuseWidth)
			break
	if reg_fail == 1:
		Fail += 1
		if field_invalid_token == True:
			PassFail = 'Fail (w/ invalid_token)'
		else:
			PassFail = 'Fail'
		fail_number.append(current_number)
		fail_reg_name.append(full_reg_name)
		fail_attribute.append(atjt_statusn)
		fail_regwidth.append(FuseWidth)
		fail_rs1.append(rs1)
		fail_rs2.append(rs2)
		fail_w1.append(w1)
		fail_rr1_1.append(r1_1)
		fail_rr1_2.append(r1_2)
		fail_w2.append(w2)
		fail_rr2_1.append(r2_1)
		fail_rr2_2.append(r2_2)
		fail_w3.append(w3)
		fail_rr3.append(r3)
		RowDictList += [{'No.':current_number,'Reg_name':full_reg_name,'Attributes':atjt_statusn,'REG_WIDTH':FuseWidth,'Pass/Fail':PassFail,'Read_store_1':rs1,'Read_store_2':rs2,'Write_value1(10)':w1,'1stRead_value1':r1_1,'2ndRead_value1':r1_2,'Write_value2(01)':w2,'1stRead_value2':r2_1,'2ndRead_value2':r2_2,'Write_value3':w3,'Read_value3':r3}]				
		xx = asciitable.AsciiTable.fromDictList(RowDictList,headers)
	elif reg_fail == 0:
		Pass += 1
		if field_invalid_token == True:
			PassFail = 'Pass (w/ invalid token)'
		else:
			PassFail = 'Pass'
	rowDictList += [{'No.':current_number,'Reg_name':full_reg_name,'Attributes':atjt_statusn,'REG_WIDTH':FuseWidth,'Pass/Fail':PassFail,'Read_store_1':rs1,'Read_store_2':rs2,'Write_value1(10)':w1,'1stRead_value1':r1_1,'2ndRead_value1':r1_2,'Write_value2(01)':w2,'1stRead_value2':r2_1,'2ndRead_value2':r2_2,'Write_value3':w3,'Read_value3':r3}]
	x = asciitable.AsciiTable.fromDictList(rowDictList,headers)

	
def export(e_func,variable,alg,flg):#Write/store only
	if e_func == 'open':
		alg = open("AggressiVE.log", "a")
		flg = open("AggressiVE_fail.log", "a")
	elif e_func == 'close_all':
		alg.close()
	elif e_func == 'close_fail':
		flg.close()
	elif e_func == 'store':
		alg.write(variable)
	elif e_func == 'store_fail':
		flg.write(variable)
	return alg,flg
	
def access_method(full_ip):	#Done!
	headers = ['Access Method']
	rowDictList = []
	storage = []
	unit=''
	n = 1
	stop_func = False
	for temp in full_ip:
		if temp == '.':
			break
		unit+=temp
	available_access = eval(unit+'.getaccesschoices()')
	for temp in available_access:
		for temp2 in available_access[temp]:
			storage.append(temp2)
	storage = list(dict.fromkeys(storage))
	for all_avai_access in storage:
		rowDictList += [{'Access Method':all_avai_access}]
	x = asciitable.AsciiTable.fromDictList(rowDictList,headers)
	print( x.getTableText() )

	loop=1
	while loop == 1:
		user_choice = input('Choice: ')
		if user_choice not in storage:
			print('Please enter the listed available method!!!')
			loop=1
		elif user_choice in storage:
			loop=0

	eval(unit+'.setaccess("'+user_choice+'")')
	current_method = eval(unit+'.getaccess()')
	print('You have successfully changed the access method of '+unit+' into '+current_method)
	
	temp=''
	ip = full_ip[4:]
	ip+='.'
	ip_lv1 = ''
	ip_lv2 = ''
	for ip_temp in ip:
		if ip_temp == '.' and ip_lv1 == '':
			ip_lv1 = temp
			temp = ''
		elif ip_temp == '.' and ip_lv2 == '':
			ip_lv2 = temp
			break
		if ip_temp != '.':
			temp += ip_temp
	if ip_temp != '.':
		print('Your IP is incompleted, please re-enter!')
		stop_func = True
		return stop_func
	temp = ''
	for ips in eval(unit+".search('')"):
		for t in ips:
			if t == '.' and temp == ip_lv1:
				temp = ''
				now_method1 = eval(unit+'.'+ip_lv1+'.getaccess()')
			elif t == '.' and temp == ip_lv2:
				temp = ''
				now_method2 = eval(unit+'.'+ip_lv1+'.'+ip_lv2+'.getaccess()')
				break
			elif t != '.':
				temp+=t
			else:
				temp=''
				break
		if temp != '':
			print('There is no such IP!! Please re-enter!')
			stop_func = True
			return stop_func
	if now_method1 == current_method:
		print('You have successfully changed the read/write method of "'+ip_lv1+'" IP into '+now_method1)
	else:
		print("For '"+ip_lv1+"', it's not '"+current_method+"', but '" +now_method1+"'!")
		only_method = eval(unit+'.'+ip_lv1+'.getaccesschoices()')
		for om1 in only_method:
			print('The only available method is/are:')
			for om2 in only_method[om1]:
				print('- '+om2)
	if now_method2 == current_method:
		print('You have successfully changed the read/write method of "'+ip_lv2+'" IP into '+now_method2)
	else:
		print("For '"+ip_lv2+"', it's not '"+current_method+"', but '" +now_method2+"'!")
		only_method = eval(unit+'.'+ip_lv1+'.'+ip_lv2+'.getaccesschoices()')
		for om1 in only_method:
			print('The only available method is/are:')
			for om2 in only_method[om1]:
				print('- '+om2)
	return stop_func

def rdwr_val(full_ip,chosen_specific_attr,total_num,alg,flg):
	headers = ['No.','Reg_name', 'Attributes','REG_WIDTH','Result','Pre_rd1','Pre_rd2','WR1','RD1_1','RD1_2','WR2','RD2_1','RD2_2','WR3','RD3']
	rowdictlist = []
	x = []
	available_attr = [' ro ',' wo ',' r/w ',' rw/1c ',' rw/o ',' rw/s ',' rw/1s ',' r/w set ',' ro/swc ',' rsv ',' r/wc ',' others ']
	regs = eval(full_ip+'.search("")')
	left_num = total_num
	displaying = 0
	previous_display_num = '0'
	display_num = 'retype'
	current_num = 0
	Pass = Fail = Unknown = invalid_token = 0
	looped_num=0
	for reg in regs:
		full_reg_name = full_ip+'.'+reg
		(displaying,previous_display_num,display_num,looped_num) = num_display_user_input(total_num,left_num,displaying,previous_display_num,display_num,looped_num)
		if display_num == 'end':
			break
		(atjt_statusn,at_typen,attr1_bit,attr2_bit,attr3_bit,attr4_bit,attr5_bit) = Attribute_Jtag_Tracking(full_reg_name)#Received 'attributes list in a reg', 'AT/FIELD_ERROR', 'BITS under which attr'.
		if at_typen == 'FIELD_ERROR':
#Read/Write Start for invalid token(From the expectation of failure in determining the bit and attr of sub-reg.)
			bug=open("Invalid_Token.log","a")
			fields=eval(full_ip+'.'+reg+'.search("")')
			bug.write('---')
			for field in fields:
				bug.write('Invalid token: '+full_ip+'.'+reg+'.'+field+'\n')
			bug.close()
			FuseWidth = '-'
			PassFail = 'Invalid_Token'
			rs1 = rs2 = w1 = r1_1 = r1_2 = w2 = r2_1 = r2_2 = w3 = r3 = '-'
			if chosen_specific_attr == ' others ' or chosen_specific_attr == 'all_attr_disp':
				current_num += 1
				rowdictlist += [{'No.':current_num,'Reg_name':full_reg_name,'Attributes':atjt_statusn,'REG_WIDTH':FuseWidth,'Result':PassFail,'Pre_rd1':rs1,'Pre_rd2':rs2,'WR1':w1,'RD1_1':r1_1,'RD1_2':r1_2,'WR2':w2,'RD2_1':r2_1,'RD2_2':r2_2,'WR3':w3,'RD3':r3}]				
				x = asciitable.AsciiTable.fromDictList(rowdictlist,headers)
				invalid_token += 1
				looped_num += 1
				left_num -= 1
		elif chosen_spec_attr in available_attr and chosen_spec_attr in atjt_statusn:
#Read/Write Start for specific reg except invalid token.
			current_num += 1
			(Pass,Fail,Unknown,rs1,rs2,w1,r1_1,r1_2,w2,r2_1,r2_2,w3,r3) = stages_of_rdwr_val(full_reg_name,atjt_statusn,Pass,Fail,Unknown,chosen_spec_attr)
			rowdictlist += [{'No.':current_num,'Reg_name':full_reg_name,'Attributes':atjt_statusn,'REG_WIDTH':FuseWidth,'Result':PassFail,'Pre_rd1':rs1,'Pre_rd2':rs2,'WR1':w1,'RD1_1':r1_1,'RD1_2':r1_2,'WR2':w2,'RD2_1':r2_1,'RD2_2':r2_2,'WR3':w3,'RD3':r3}]
			x = asciitable.AsciiTable.fromDictList(rowdictlist,headers)
			looped_num += 1
			left_num -= 1
		elif chosen_spec_attr == 'all_attr_display':
#Read/Write Start for all except invalid token.
			current_num += 1
			(Pass,Fail,Unknown,rs1,rs2,w1,r1_1,r1_2,w2,r2_1,r2_2,w3,r3) = stages_of_rdwr_val(full_reg_name,atjt_statusn,Pass,Fail,Unknown,chosen_spec_attr)
			rowdictlist += [{'No.':current_num,'Reg_name':full_reg_name,'Attributes':atjt_statusn,'REG_WIDTH':FuseWidth,'Result':PassFail,'Pre_rd1':rs1,'Pre_rd2':rs2,'WR1':w1,'RD1_1':r1_1,'RD1_2':r1_2,'WR2':w2,'RD2_1':r2_1,'RD2_2':r2_2,'WR3':w3,'RD3':r3}]				
			x = asciitable.AsciiTable.fromDictList(rowdictlist,headers)
			looped_num += 1
			left_num -= 1
		(alg,flg)=num_display_ending_part(x,looped_num,total_num,displaying,display_num,Pass,Fail,Unknown,invalid_token,alg,flg)
	return alg,flg

def Attribute_Jtag_Tracking(full_reg_name):
#determine the register type of IP. Attribute/JTAG/SOmething Else.
	info = 'None'
	fields = eval(full_reg_name+".search('')")
	for field in fields:
		try:
			full_field = full_reg_name+'.'+field
			attr_status = eval(full_field+".info")
			if 'attribute' in attr_status:
				info = 'Attribute'
		except:
			info='FIELD_ERROR'
			num_none = '-'
			print('full_field:'+full_field)
			return info,info,num_none,num_none,num_none,num_none,num_none
		if info == 'Attribute':
			break
#-----------------------------------Attribute
	if info == 'Attribute':
		atjt_status = []
		attr1_bit = []
		attr2_bit = []
		attr3_bit = []
		attr4_bit = []
		attr5_bit = []
		temp_attribute1 = ''
		temp_attribute2 = ''
		temp_attribute3 = ''
		temp_attribute4 = ''
		temp_attribute5 = ''
		temp1_prev_lowerbit = temp2_prev_lowerbit = temp3_prev_lowerbit = temp4_prev_lowerbit = temp5_prev_lowerbit = 0
		temp1_prev_upperbit = temp2_prev_upperbit = temp3_prev_upperbit = temp4_prev_upperbit = temp5_prev_upperbit = 0
		fields = full_reg_name+".search('')"
		for field in eval(fields):
			key = 0
			try:
#determine lowerbit, numbits, attribute, upperbit, and bit_arrange of that fields from that register.
				attribute = eval(full_reg_name+'.'+field+'.info["attribute"]')
				lowerbit = eval(full_reg_name+'.'+field+'.info["lowerbit"]')
				numbits = eval(full_reg_name+'.'+field+'.info["numbits"]')
				if numbits != 1:
					upperbit = int(lowerbit)+int(numbits)-1
					bit_range = str(upperbit)+'-'+str(lowerbit)
				else:
					bit_range = str(int(lowerbit))
					upperbit = lowerbit
#Store every available attribute from that attribute in atjt_status(link).
				if attribute != temp_attribute1:
					temp_attribute1 = attribute
					atjt_status.append(attribute)
				elif attribute != temp_attribute2:
					temp_attribute2 = attribute
					atjt_status.append(attribute)
				elif attribute != temp_attribute3:
					temp_attribute3 = attribute
					atjt_status.append(attribute)
				elif attribute != temp_attribute4:
					temp_attribute4 = attribute
					atjt_status.append(attribute)
				elif attribute != temp_attribute5:
					temp_attribute5 = attribute
					atjt_status.append(attribute)
#Store the information (upperbit, lowerbit, and bit range) of the fields of registers with specific attr1.
				if attribute == temp_attribute1 and attr1_bit == []:
					attr1_bit.append(bit_range)
					temp1_prev_upperbit = int(upperbit)
					temp1_prev_lowerbit = int(lowerbit)
				elif attribute == temp_attribute1 and attr1_bit != []:
					if temp1_prev_lowerbit == (int(upperbit) + 1):
						bit_range = str(temp1_prev_upperbit)+'-'+str(lowerbit)
						attr1_bit.pop(-1)
					attr1_bit.append(bit_range)
					temp1_prev_upperbit = int(temp1_prev_upperbit)
					temp1_prev_lowerbit = int(lowerbit)
#Store...specific attr2.
				elif attribute == temp_attribute2 and attr2_bit == []:
					attr2_bit.append(bit_range)
					temp2_prev_upperbit = int(upperbit)
					temp2_prev_lowerbit = int(lowerbit)
				elif attribute == temp_attribute2 and attr2_bit != []:
					if temp2_prev_lowerbit == (int(upperbit) + 1):
						bit_range = str(temp2_prev_upperbit)+'-'+str(lowerbit)
						attr2_bit.pop(-1)
					attr2_bit.append(bit_range)
					temp2_prev_upperbit = int(temp2_prev_upperbit)
					temp2_prev_lowerbit = int(lowerbit)
#Store...specific attr3.
				elif attribute == temp_attribute3 and attr3_bit == []:
					attr3_bit.append(bit_range)
					temp3_prev_upperbit = int(upperbit)
					temp3_prev_lowerbit = int(lowerbit)
				elif attribute == temp_attribute3 and attr3_bit != []:
					if temp3_prev_lowerbit == (int(upperbit) + 1):
						bit_range = str(temp3_prev_upperbit)+'-'+str(lowerbit)
						attr3_bit.pop(-1)
					attr3_bit.append(bit_range)
					temp3_prev_upperbit = int(temp3_prev_upperbit)
					temp3_prev_lowerbit = int(lowerbit)
#Store...specific attr4.
				elif attribute == temp_attribute4 and attr4_bit == []:
					attr4_bit.append(bit_range)
					temp4_prev_upperbit = int(upperbit)
					temp4_prev_lowerbit = int(lowerbit)
				elif attribute == temp_attribute4 and attr4_bit != []:
					if temp4_prev_lowerbit == (int(upperbit) + 1):
						bit_range = str(temp4_prev_upperbit)+'-'+str(lowerbit)
						attr4_bit.pop(-1)
					attr4_bit.append(bit_range)
					temp4_prev_upperbit = int(temp4_prev_upperbit)
					temp4_prev_lowerbit = int(lowerbit)
#Store...specific attr5.
				elif attribute == temp_attribute5 and attr5_bit == []:
					attr5_bit.append(bit_range)
					temp5_prev_upperbit = int(upperbit)
					temp5_prev_lowerbit = int(lowerbit)
				elif attribute == temp_attribute5 and attr5_bit != []:
					if temp5_prev_lowerbit == (int(upperbit) + 1):
						bit_range = str(temp5_prev_upperbit)+'-'+str(lowerbit)
						attr5_bit.pop(-1)
					attr5_bit.append(bit_range)
					temp5_prev_upperbit = int(temp5_prev_upperbit)
					temp5_prev_lowerbit = int(lowerbit)
			except:
#If determination is not able to do, the only issue is coming from the name of field(s) of registers. So record the full name of fields and store in 
				bug=open("Invalid_Token.log","a")
				bug.write('---')
				for field in fields:
					bug.write('Invalid token: '+full_reg_name+'.'+field+'\n')
				bug.close()
		at_type = 'AT'
		return atjt_status,at_type,attr1_bit,attr2_bit,attr3_bit,attr4_bit,attr5_bit


def rdwr_val2_fail():
	Display = ''
	while Display == '':
		Display = input('Display FAIL registers? (y/n):')
		if Display != 'y' or Display != 'n':
			Display=''
	if Display == 'y':
		pass

def main(full_ip):
#Section 1: Choose access method.
	stop_func = access_method(full_ip)
	if stop_func == False:
		#Some Other Funcs.
#Section 2: Open log File?
		exp='nothing_yet'
		while len(exp) > 0:
			Exp = input('Dump Log File (y/n)?: ')
			exp = Exp.lower()
			if exp == 'y' or exp == 'yes':
				exp = 'y'
				print('''All the information will be dumped to:
For All information ==> C>Users>pgsvlab>Documents>PythonSv>ags_AggressiVE.log
For fail read/write information ==> C>Users>pgsvlab>Documents>PythonSv>ags_AggressiVE_fail.log''')
				alg = flg = variable = ''
				(alg,flg)=export('open',variable,alg,flg)
				break
			elif exp == 'n' or exp == 'no':
				alg = flg = variable = ''
				exp = 'n'
				break
			else:
				print('Please re-enter!!!')
#Section 3: First Read/Write Validation.
		specific_attr_disp = ''
		available_attr = [' ro ',' wo ',' r/w ',' rw/1c ',' rw/o ',' rw/s ',' rw/1s ',' r/w set ',' ro/swc ',' rsv ',' r/wc ',' others ']
		total_num = 0
		while specific_attr_disp == '':
			specific_attr_disp = input('Would you like to choose attribute(s) read/write? If no, read/write all attributes in current IP(y/n):')
			if specific_attr_disp != 'y':
				if specific_attr_disp != 'n':
					specific_attr_disp=''
		if specific_attr_disp == 'y':
			chosen_specific_attr=''
			while chosen_specific_attr == '':
				chosen_specific_attr = input('Which attribute(s)would you like to read/write?[ro,wo,r/w,rw/1c,rw/o,rw/s,rw/1s,r/w set,ro/swc,rsv,r/wc,others]:')
				chosen_specific_attr.lower()
				chosen_specific_attr = ' '+ chosen_specific_attr + ' '
				if chosen_specific_attr not in available_attr:
					chosen_specific_attr=''
			#Total Number calculation.
			regs = eval(full_ip+'.search("")')
			for reg in regs:
				fields = eval(full_ip+'.'+reg+'.search("")')
				for field in fields:
					attribute_detection = eval(full_ip+'.'+reg+'.'+field+'.info["attribute"]')
					if attribute_detection == chosen_specific_attr:
						total_num += 1
						break
			(alg,flg) = rdwr_val(full_ip,chosen_specific_attr,total_num,alg,flg)
		else:
			#all
			chosen_specific_attr='all_attr_disp'
			regs = eval(full_ip+'.search("")')
			for reg in regs:
				total_num += 1
			(alg,flg) = rdwr_val(full_ip,chosen_specific_attr,total_num,alg,flg)
#Section 4: Close 'all' log file.
		(alg,flg)=export('close_all',variable,alg,flg)
#Section 5: Second Read/Write Validation.
		rdwr_val2_fail()
#Section 6: Close 'fail' log file.
		(alg,flg)=export('close_fail',variable,alg,flg)
#The End!
