#!/usr/bin/env python
import sys
import os
import re
import os.path
#Janus code path
#Set JanusPATH and parser PATH to the root directory of janus and cinnamon respectively 
JanusPATH = "/janus"
parserPATH= "/cinnamon"
def usage():
	print "compileToJanus.py <program.dsl>"
if len(sys.argv) != 2:
	usage()
	sys.exit(0)

#Step 1: Invoke DSL parser and generator
dslFile = sys.argv[1]
fileName = os.path.splitext(dslFile)[0]

os.system(parserPATH + '/bdc ' + dslFile)  
#os.system("gdb --args " + parserPATH + '/bdc ' + dslFile)


#Step 2: Call clang compiler to generate assembly code for actions
os.system('clang++ -fno-stack-protector -fomit-frame-pointer -fno-asynchronous-unwind-tables -S '+ fileName + '.cpp -o ' + fileName + '.s')

#Step 3: Parse assembly code to take useful ones, and transform them into DynamoRio functions
print "Start parsing assembly code, output file to" + fileName + ".instr"
os.system(parserPATH + '/parse-assembly/assem.o ' + fileName)
print "End parsing assembly code\n"

#Step 4 Insert DynamoRio Macros into correct places
print "Start inserting DynamoRio Macros into .dyn file"
os.system(parserPATH + '/parse-assembly/wrtodyn.o ' + fileName)
print "End inserting DynamoRio Macros into .dyn file\n"

#exit()

#Step 5: Start moving code to Janus
with open(fileName+".stat", 'r') as static_file:
	code = static_file.read();
	code = '/*--- Static RuleGen Start ---*/\n'+code+'\n/*--- Static RuleGen Finish ---*/'
	with open(JanusPATH+"/static/schedgen/dsl/StaticGenCode.cpp", "r") as dest_file:
		content = dest_file.read();
		content_new = re.sub(r'/\*--- Static RuleGen Start ---\*/.*?/\*--- Static RuleGen Finish ---\*/', code, content, flags=re.DOTALL)
		with open(JanusPATH+"/static/schedgen/dsl/StaticGenCode.cpp", "w") as replace_file:
			replace_file.write(content_new)
			print "static rule generation code:"
			# print content_new

with open(fileName+".stath", 'r') as static_h_file:
	code = static_h_file.read();
	code = '/*--- Global Var Decl Start ---*/\n'+code+'\n/*--- Global Var Decl End ---*/'
	with open(JanusPATH+"/static/schedgen/dsl/StaticGenCode.cpp", "r") as dest_file:
		content = dest_file.read();
		content_new = re.sub(r'/\*--- Global Var Decl Start ---\*/.*?/\*--- Global Var Decl End ---\*/', code, content, flags=re.DOTALL)
		with open(JanusPATH+"/static/schedgen/dsl/StaticGenCode.cpp", "w") as replace_file:
			replace_file.write(content_new)
			print "global var decl - static part"
			# print content_new

with open(fileName+".dyn", 'r') as dynamic_file:
	code = dynamic_file.read();
	code = '/*--- Dynamic Handlers Start ---*/\n'+code+'\n/*--- Dynamic Handlers Finish ---*/'
	with open(JanusPATH+"/dynamic/dsl/dsl_handler.cpp", "r") as dest_file:
		content = dest_file.read();
		content_new = re.sub(r'/\*--- Dynamic Handlers Start ---\*/.*?/\*--- Dynamic Handlers Finish ---\*/', code, content, flags=re.DOTALL)
		with open(JanusPATH+"/dynamic/dsl/dsl_handler.cpp", "w") as replace_file:
			replace_file.write(content_new)
			print "dynamic handler code:"
			# print content_new
with open(fileName+".dynh", 'r') as dynamic_h_file:
	code = dynamic_h_file.read();
	code = '/*--- Global Var Decl Start ---*/\n'+code+'\n/*--- Global Var Decl End ---*/'
	with open(JanusPATH+"/dynamic/dsl/func.cpp", "r") as dest_file:
		content = dest_file.read();
		content_new = re.sub(r'/\*--- Global Var Decl Start ---\*/.*?/\*--- Global Var Decl End ---\*/', code, content, flags=re.DOTALL)
		with open(JanusPATH+"/dynamic/dsl/func.cpp", "w") as replace_file:
			replace_file.write(content_new)
			print "global declarations - dyn part"
			# print content_new

with open(fileName+".func", 'r') as func_file:
	code = func_file.read();
	code = '/*--- DSL Function Start ---*/\n'+code+'\n/*--- DSL Function Finish ---*/'
	with open(JanusPATH+"/dynamic/dsl/func.cpp", "r") as dest_file:
		content = dest_file.read();
		content_new = re.sub(r'/\*--- DSL Function Start ---\*/.*?/\*--- DSL Function Finish ---\*/', code, content, flags=re.DOTALL)
		with open(JanusPATH+"/dynamic/dsl/func.cpp", "w") as replace_file:
			replace_file.write(content_new)
			print "function code:"
			# print content_new

with open(fileName+".funch", 'r') as header_file:
	code = header_file.read();
	code = '/*--- Function Global Declaration Start ---*/\n'+code+'\n/*--- Function Global Declaration Finish ---*/'
	with open(JanusPATH+"/dynamic/dsl/func.h", "r") as dest_file:
		content = dest_file.read();
		content_new = re.sub(r'/\*--- Function Global Declaration Start ---\*/.*?/\*--- Function Global Declaration Finish ---\*/', code, content, flags=re.DOTALL)
		with open(JanusPATH+"/dynamic/dsl/func.h", "w") as replace_file:
			replace_file.write(content_new)
			print "function header code:"
			# print content_new
with open(fileName+".exit", 'r') as exit_file:
	code = exit_file.read();
	code = '/*--- Termination Start ---*/\n'+code+'\n/*--- Termination End ---*/'
	with open(JanusPATH+"/dynamic/dsl/func.cpp", "r") as dest_file:
		content = dest_file.read();
		content_new = re.sub(r'/\*--- Termination Start ---\*/.*?/\*--- Termination End ---\*/', code, content, flags=re.DOTALL)
		with open(JanusPATH+"/dynamic/dsl/func.cpp", "w") as replace_file:
			replace_file.write(content_new)
			print "thread exit code:"
			# print content_new
with open(fileName+".init", 'r') as init_file:
	code = init_file.read();
	code = '/*--- Init Start ---*/\n'+code+'\n/*--- Init End ---*/'
	with open(JanusPATH+"/dynamic/dsl/func.cpp", "r") as dest_file:
		content = dest_file.read();
		content_new = re.sub(r'/\*--- Init Start ---\*/.*?/\*--- Init End ---\*/', code, content, flags=re.DOTALL)
		with open(JanusPATH+"/dynamic/dsl/func.cpp", "w") as replace_file:
			replace_file.write(content_new)
			print "thread entry code:"
			# print content_new
with open(fileName+".thread_init", 'r') as thread_init_file:
	code = thread_init_file.read();
	code = '/*--- Janus Thread Init Start ---*/\n'+code+'\n/*--- Janus Thread Init Finish ---*/'
	with open(JanusPATH+"/dynamic/dsl/dsl_core.cpp", "r") as dest_file:
		content = dest_file.read();
		content_new = re.sub(r'/\*--- Janus Thread Init Start ---\*/.*?/\*--- Janus Thread Init Finish ---\*/', code, content, flags=re.DOTALL)
		with open(JanusPATH+"/dynamic/dsl/dsl_core.cpp", "w") as replace_file:
			replace_file.write(content_new)
			print "Janus thread init code:"
			# print content_new

with open(fileName+".thread_manager_h", 'r') as thread_manager_h:
	code = thread_manager_h.read();
	code = '/*--- Thread Manager Declarations Start ---*/\n\n'+code+'\n/*--- Thread Manager Declarations Finish ---*/'
	with open(JanusPATH+"/dynamic/dsl/dsl_thread_manager.h", "r") as dest_file:
		content = dest_file.read();
		content_new = re.sub(r'/\*--- Thread Manager Declarations Start ---\*/.*?/\*--- Thread Manager Declarations Finish ---\*/', code, content, flags=re.DOTALL)
		with open(JanusPATH+"/dynamic/dsl/dsl_thread_manager.h", "w") as replace_file:
			replace_file.write(content_new)
			print "Janus thread manager h code:"
			# print content_new

with open(fileName+".thread_manager_cpp", 'r') as thread_manager_cpp:
	code = thread_manager_cpp.read();
	code = '/*--- Thread Manager Declarations Start ---*/\n\n'+code+'\n/*--- Thread Manager Declarations Finish ---*/'
	with open(JanusPATH+"/dynamic/dsl/dsl_thread_manager.cpp", "r") as dest_file:
		content = dest_file.read();
		content_new = re.sub(r'/\*--- Thread Manager Declarations Start ---\*/.*?/\*--- Thread Manager Declarations Finish ---\*/', code, content, flags=re.DOTALL)
		with open(JanusPATH+"/dynamic/dsl/dsl_thread_manager.cpp", "w") as replace_file:
			replace_file.write(content_new)
			print "Janus thread manager cpp code:"
			# print content_new

with open(fileName+".ipc_h", 'r') as ipc_h:
	code = ipc_h.read();
	code = '/*--- IPC Declarations Start ---*/\n\n'+code+'\n/*--- IPC Declarations Finish ---*/'
	with open(JanusPATH+"/dynamic/dsl/dsl_ipc.h", "r") as dest_file:
		content = dest_file.read();
		content_new = re.sub(r'/\*--- IPC Declarations Start ---\*/.*?/\*--- IPC Declarations Finish ---\*/', code, content, flags=re.DOTALL)
		with open(JanusPATH+"/dynamic/dsl/dsl_ipc.h", "w") as replace_file:
			replace_file.write(content_new)
			print "Janus IPC h code:"
			# print content_new

with open(fileName+".ipc_cpp", 'r') as ipc_cpp:
	code = ipc_cpp.read();
	code = '/*--- IPC Declarations Start ---*/\n\n'+code+'\n/*--- IPC Declarations Finish ---*/'
	with open(JanusPATH+"/dynamic/dsl/dsl_ipc.cpp", "r") as dest_file:
		content = dest_file.read();
		content_new = re.sub(r'/\*--- IPC Declarations Start ---\*/.*?/\*--- IPC Declarations Finish ---\*/', code, content, flags=re.DOTALL)
		with open(JanusPATH+"/dynamic/dsl/dsl_ipc.cpp", "w") as replace_file:
			replace_file.write(content_new)
			print "Janus IPC cpp code:"
			# print content_new
