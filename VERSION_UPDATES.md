# AggressiVE
#Current Patch: 0.3

#Used for register validation with feedback system.
#It helps you to detect the naming issue of registers, check for nunmber of registers with specific attribute(s), and check for the false behavior of the 
registers by doing read_write validation. It will also check for the current state of the system which include the 'system restart' and 'Hang state with 
the present of Machine Check Error'.
#It will feedback to users which register and which part of it are false and unexpected.
#AggressiVE are expecting to be executed in UEFI Shell and require Machine Check Error script. Recommend to run it in the host instead of laptop because 
laptop doesn't has Machine Check Error Script.
#Validation Time Taken: 3 seconds per every 10 registers full validation.

#Patch 0.1 = Basic Features. BETA Mode. With Main and most used Attribute only.

#Patch 0.2 = With better feedback system. Added all the available attributes but not all the behaviors are ready. With some useful functions such as 
algorithm, get attribute, check for naming issue registers and so on.

#Patch 0.3 [Current] = Added features such as tracking hang registers and registers that caused system reset. Do Machine Check when system is hang. Added 2 more 
functions called as aggressive_cont() and aggressive_badname(). Due to the process of validation takes very long time, this is why aggressive_cont() is 
generated to let user continue to validate without restarting everything. Other than that, we also found that the registers with an unacceptable name can be 
read-write and read info but in different way. This is why we created aggressive_badname() with new subfunctions to validate it to manage the complexity and 
nidiness of the scripts. For access method, this patch will only support to get and set the access in 'default' group.

#Patch 1.0 = Officially tested on Pre-silicon Emulation Model and Transactor as well.