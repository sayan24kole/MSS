#version 1.3

""" Completion of compiler:- 
Completed task:-
1) File creation
2) Extension of .mss
3) generation of .data section
4) generation of .test section
5) Main section
6) Generation of variables of both int and string using create
7) Operations (op) :- add, sub, mul
8) Comment addition via ?
9) print and println statements

Improvement required:- 
1) requiement of space right after print and println should be removed
2) use of ? other than just commenting
3) nested operations

Future task:-
1) Add div
2) Add input
3) Add string functionality
4) DSA like array and stack
5) Syntax error generation
6) If else condition
7) Loops
8) Remove dependencies of io64.inc and use syscall

Future proofing task:-
1) Add functions
2) Add stl
3) try and catch statements
4) tokens instead of parser
"""

"""Key points:-
1) each variable needs space because parsing is used to seperate the var in op
2) It is mandatory to temporarily store spr value in r10 OR use push/pop whatever
is necessary. This is done to keep notice of the ongoing process. After the current 
process is over restore the spr value via r10.
3) Giving comments in .asm is required
4) Start of any block of code like for loop , if else condition requires it to be
inside of **. This means * your whole code block *. The code should be inside **
"""

def data_initialization(a): #currently 64 bit
    if(a[0] == "create"):
        with open(file_name, "a") as f:
            f.write(f"section .data\n")
            for i in range(1,len(a),2):
                if(a[i] == "int"):
                    f.write(f"{a[i+1]} dq 0 \n")
                    variable_name_list.append(a[i+1])
                elif(a[i] == "string"):
                    f.write(f"{a[i+1]} db 0 \n")
                    variable_name_list.append(a[i+1])
            f.write("section .text\n")      
            f.write("global main\n")
            f.write("main:\n")

def file_creation(a): #currently 64 bit
    if(a[0] == "file"):
        fname = f"{a[1]}.asm"           
        with open(fname, "w") as f:    
            f.write('%include "io64.inc"\n')         
        return fname
    else:
        return None

def integer_define(a): #currently 64 bit
    if(a[0] == "int" "input" not in a):
        int_name = a[1]
        int_content = a[3]
        with open(file_name, "a") as f:
            f.write(f"mov qword [{int_name}],{int_content} \n")

def operations(a): #currently 64 bit
    if(a[0] == "op"):
        int_name = a[2]
        op1 = a[4]
        op2 = a[6]
        if(a[5] == "+"):
            with open(file_name, "a") as f:
                f.write(f"\n;Addition\n")
                f.write(f"push rax\n")
                f.write(f"mov rax, [{op1}]\n")
                f.write(f"add rax, [{op2}]\n")     
                f.write(f"mov [{int_name}], rax\n")
                f.write(f"pop rax\n\n")
        elif(a[5] == "-"):
            with open(file_name, "a") as f:
                f.write(f"\n;Difference\n")
                f.write(f"push rax\n")
                f.write(f"mov rax, [{op1}]\n")    
                f.write(f"sub rax, [{op2}]\n")      
                f.write(f"mov [{int_name}], rax\n\n")
                f.write(f"pop rax\n\n")
        elif(a[5] == "*"):
            with open(file_name, "a") as f:
                f.write(f"\n;Multiplication\n")
                f.write(f"push rax\n")
                f.write(f"push rbx\n")
                f.write(f"mov rax, [{op1}]\n")    
                f.write(f"mov rbx, [{op2}]\n\n")      
                f.write(f"mul rbx\n\n")
                f.write(f"mov [{int_name}], rax\n")
                f.write(f"pop rax\n")
                f.write(f"pop rbx\n\n")
        elif(a[5] == "/"):
            with open(file_name, "a") as f:
                f.write(f"\n;Division\n")
                f.write(f"push rax\n")
                f.write(f"push rbx\n")
                f.write(f"push rdx\n\n")
                f.write(f"mov rax, [{op1}]\n")
                f.write(f"mov rbx, [{op2}]\n")
                f.write(f"\ncqo\n\n")
                f.write(f"idiv rbx\n")
                f.write(f"mov [{int_name}], rax\n\n")
                f.write(f"pop rax\n")
                f.write(f"pop rbx\n")
                f.write(f"pop rdx\n\n")
        elif(a[5] == "%"):
            with open(file_name, "a") as f:
                f.write(f"\n;Modulus\n")
                f.write(f"push rax\n")
                f.write(f"push rbx\n")
                f.write(f"push rdx\n\n")
                f.write(f"mov rax, [{op1}]\n")
                f.write(f"mov rbx, [{op2}]\n")
                f.write(f"\ncqo\n\n")
                f.write(f"idiv rbx\n")
                f.write(f"mov [{int_name}], rdx\n\n")
                f.write(f"pop rax\n")
                f.write(f"pop rbx\n")
                f.write(f"pop rdx\n\n")
                
def print_statement(a):  # currently 64 bit using "io64.inc"
    
    if a[0].startswith("println"):
        a = a[1:]
        a = [token.strip() for token in a if token.strip()]
        operation = " ".join(a)
        operation = operation.replace("(", "").replace(")", "")
        char_list = [token.strip() for token in operation.split(",") if token.strip()]
        with open(file_name, "a") as f:
            for i in char_list:
                if len(i) > 0 and i[0] == '"' and i[-1] == '"':
                    f.write("\n;Printing\n")
                    f.write(f"PRINT_STRING {i}\n")
                elif i in variable_name_list:
                    f.write("push rax \n")
                    f.write(f"mov rax, [{i}]\n")
                    f.write("PRINT_DEC 8, rax\n")
                    f.write("pop rax\n")
        with open(file_name, "a") as f:
            f.write("NEWLINE \n")
    elif a[0].startswith("print"):
        a = a[1:]
        a = [token.strip() for token in a if token.strip()]
        operation = " ".join(a)
        operation = operation.replace("(", "").replace(")", "")
        char_list = [token.strip() for token in operation.split(",") if token.strip()]
        with open(file_name, "a") as f:
            for i in char_list:
                if len(i) > 0 and i[0] == '"' and i[-1] == '"':
                    f.write("\n;Printing\n")
                    f.write(f"PRINT_STRING {i}\n")
                elif i in variable_name_list:
                    f.write("push rax \n")
                    f.write(f"mov rax, [{i}]\n")
                    f.write("PRINT_DEC 8, rax\n")
                    f.write("pop rax \n")
        
#def if_else_statement(a):
    
def get_user_input(a):
    if (a[0] == "int" and "input" in a):
        name = a[1]
        with open (file_name, "a") as f:
            f.write(f"\n;Input\n")
            f.write(f"push rax\n")
            f.write(f"GET_DEC 8,rax\n")
            f.write(f"mov [{name}], rax\n")
            f.write(f"pop rax\n\n")
        
code_line = []
fname = input("Enter your file name without extension 'mss' ")

#this contains the code of both comment and conversion of .mss file to python
with open(f"{fname}.mss", "r") as f:
    for line in f:
        line = line.strip()
        if line:
            result_line = line.split("?")[0].strip() #comment statement
            code_line.append(result_line)  #input of .mss file to python
            
#this is the implementation of all the functions created above.
file_name = None
variable_name_list = []
for i in code_line:
    res = file_creation(i.split())
    if res:
        file_name = res
    
    #below is if_else statement breakdown from actual .mss file
    if i[0] == "*" and i[1:3] == "if":
        if_else_string = []
        for j in range(code_line.index(i),len(code_line)):
            code_line[j] = code_line[j].strip()
            if_else_string.append(code_line[j])
            if "}*" in code_line[j] :
                break
        #if_else_statement(if_else_string)
        
    #normal initilization of different code block
    data_initialization(i.split())
    get_user_input(i.split())    
    print_statement(i.split())
    integer_define(i.split())
    operations(i.split())

#TEST
print(code_line)
#print(if_else_string)
#TEST

#essentials
with open(file_name, "a") as f:      
    f.write("xor rax, rax\n")    
    f.write("ret\n")