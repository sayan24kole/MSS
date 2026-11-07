#version 1.5 - All features (Input, Int Math, Strings, Print, If-Else, While)

""" Completion of compiler:- 
Completed task:-
1) File creation
2) Extension of .mss
3) generation of .data section
4) generation of .text section
5) Main section
6) Generation of variables of both int and string using create
7) Operations (op) :- int (add, sub, mul, div, mod) and string (concat +)
8) Comment addition via ?
9) print and println statements (supports int, string literals, and string variables)
10) If-Else condition
11) Loops (while loop)
12) String variable supported
"""

"""To be done:-
1) To implement stack ased syntax approach
2) To introduce for loops via while loops
3) To implement branching
4) Recursion to be done
5) Method implementation
"""


label_count = 0

def file_creation(a): #currently 64 bit
    if len(a) > 0 and a[0] == "file":
        fname = f"{a[1]}.asm"           
        with open(fname, "w") as f:    
            f.write('%include "io64.inc"\n')         
        return fname
    else:
        return None

def data_initialization(a): #currently 64 bit
    if len(a) > 0 and a[0] == "create":
        with open(file_name, "a") as f:
            f.write("section .data\n")
            for i in range(1, len(a), 2):
                if a[i] == "int":
                    f.write(f"{a[i+1]} dq 0 \n")
                    int_var_list.append(a[i+1])
                elif a[i] == "string":
                    # allocates 256 bytes buffer for string so it doesnt crash
                    f.write(f"{a[i+1]} times 256 db 0 \n")
                    string_var_list.append(a[i+1])
            f.write("section .text\n")      
            f.write("global main\n")
            f.write("main:\n")

def integer_define(a): #currently 64 bit
    line_str = " ".join(a)
    # only runs if not an input command
    if len(a) >= 4 and a[0] == "int" and "input" not in line_str:
        int_name = a[1]
        int_content = a[3]
        with open(file_name, "a") as f:
            f.write(f"mov qword [{int_name}], {int_content} \n")

def string_define(line): #currently 64 bit
    tokens = line.split()
    if len(tokens) >= 4 and tokens[0] == "string" and "=" in tokens:
        str_name = tokens[1]
        content = line.split("=", 1)[1].strip()
        
        global label_count
        label_count += 1
        lit_label = f"str_lit_{label_count}"
        
        # stores the text in data and copies it into the string variable
        with open(file_name, "a") as f:
            f.write(f"\nsection .data\n")
            f.write(f"{lit_label} db {content}, 0\n")
            f.write(f"section .text\n")
            f.write(f";Assign string literal to {str_name}\n")
            f.write("push rsi\npush rdi\npush rax\n")
            f.write(f"lea rsi, [{lit_label}]\n")
            f.write(f"lea rdi, [{str_name}]\n")
            f.write(f"L_assign_{label_count}:\n")
            f.write("mov al, byte [rsi]\n")
            f.write("mov byte [rdi], al\n")
            f.write("inc rsi\ninc rdi\n")
            f.write("cmp al, 0\n")
            f.write(f"jne L_assign_{label_count}\n")
            f.write("pop rax\npop rdi\npop rsi\n\n")

def get_user_input(a):
    line_str = " ".join(a)
    if len(a) >= 2 and a[0] == "int" and "input" in line_str:
        name = a[1]
        with open(file_name, "a") as f:
            f.write(f"\n;Input\n")
            f.write(f"push rax\n")
            f.write(f"GET_DEC 8, rax\n")
            f.write(f"mov [{name}], rax\n")
            f.write(f"pop rax\n\n")

def operations(a): #currently 64 bit
    if len(a) > 0 and a[0] == "op":
        global label_count
        # checks whether user wrote 'op int c = ...' or 'op c = ...'
        if a[1] == "int" or a[1] == "string":
            op_type = a[1]
            dest = a[2]
            op1 = a[4]
            operator = a[5]
            op2 = a[6]
        else:
            dest = a[1]
            op_type = "string" if dest in string_var_list else "int"
            op1 = a[3]
            operator = a[4]
            op2 = a[5]

        # --- STRING CONCATENATION ---
        if op_type == "string" and operator == "+":
            label_count += 1
            lbl1 = f"L_concat_1_{label_count}"
            lbl1_done = f"L_concat_1_done_{label_count}"
            lbl2 = f"L_concat_2_{label_count}"
            with open(file_name, "a") as f:
                f.write(f"\n;String Concatenation\n")
                f.write("push rsi\npush rdi\npush rax\n")
                f.write(f"lea rsi, [{op1}]\n")
                f.write(f"lea rdi, [{dest}]\n")
                f.write(f"{lbl1}:\n")
                f.write("mov al, byte [rsi]\n")
                f.write("cmp al, 0\n")
                f.write(f"je {lbl1_done}\n")
                f.write("mov byte [rdi], al\n")
                f.write("inc rsi\ninc rdi\n")
                f.write(f"jmp {lbl1}\n")
                f.write(f"{lbl1_done}:\n")
                f.write(f"lea rsi, [{op2}]\n")
                f.write(f"{lbl2}:\n")
                f.write("mov al, byte [rsi]\n")
                f.write("mov byte [rdi], al\n")
                f.write("inc rsi\ninc rdi\n")
                f.write("cmp al, 0\n")
                f.write(f"jne {lbl2}\n")
                f.write("pop rax\npop rdi\npop rsi\n\n")

        # --- INTEGER OPERATIONS ---
        elif op_type == "int":
            # safely loads either variable value [var] or raw literal number
            load_op1 = f"mov rax, [{op1}]\n" if op1 in int_var_list else f"mov rax, {op1}\n"
            load_op2 = f"mov rbx, [{op2}]\n" if op2 in int_var_list else f"mov rbx, {op2}\n"

            if operator == "+":
                with open(file_name, "a") as f:
                    f.write(f"\n;Addition\n")
                    f.write("push rax\npush rbx\n")
                    f.write(load_op1)
                    f.write(load_op2)
                    f.write(f"add rax, rbx\n")     
                    f.write(f"mov [{dest}], rax\n")
                    f.write("pop rbx\npop rax\n\n")
            elif operator == "-":
                with open(file_name, "a") as f:
                    f.write(f"\n;Difference\n")
                    f.write("push rax\npush rbx\n")
                    f.write(load_op1)
                    f.write(load_op2)
                    f.write(f"sub rax, rbx\n")      
                    f.write(f"mov [{dest}], rax\n")
                    f.write("pop rbx\npop rax\n\n")
            elif operator == "*":
                with open(file_name, "a") as f:
                    f.write(f"\n;Multiplication\n")
                    f.write("push rax\npush rbx\n")
                    f.write(load_op1)
                    f.write(load_op2)
                    f.write(f"mul rbx\n")
                    f.write(f"mov [{dest}], rax\n")
                    f.write("pop rbx\npop rax\n\n")
            elif operator == "/":
                with open(file_name, "a") as f:
                    f.write(f"\n;Division\n")
                    f.write("push rax\npush rbx\npush rdx\n")
                    f.write(load_op1)
                    f.write(load_op2)
                    f.write(f"cqo\nidiv rbx\n")
                    f.write(f"mov [{dest}], rax\n")
                    f.write("pop rdx\npop rbx\npop rax\n\n")
            elif operator == "%":
                with open(file_name, "a") as f:
                    f.write(f"\n;Modulus\n")
                    f.write("push rax\npush rbx\npush rdx\n")
                    f.write(load_op1)
                    f.write(load_op2)
                    f.write(f"cqo\nidiv rbx\n")
                    f.write(f"mov [{dest}], rdx\n")
                    f.write("pop rdx\npop rbx\npop rax\n\n")
                
def print_statement(line): # currently 64 bit using "io64.inc"
    if line.startswith("println") or line.startswith("print"):
        is_newline = line.startswith("println")
        prefix = "println" if is_newline else "print"
        operation = line[len(prefix):].strip()
        operation = operation.replace("(", "").replace(")", "")
        char_list = [token.strip() for token in operation.split(",") if token.strip()]
        with open(file_name, "a") as f:
            for i in char_list:
                # String Literal
                if len(i) > 0 and i[0] == '"' and i[-1] == '"':
                    f.write(f"\nPRINT_STRING {i}\n")
                # String Variable
                elif i in string_var_list:
                    f.write(f"\nPRINT_STRING {i}\n")
                # Integer Variable
                elif i in int_var_list:
                    f.write("push rax \n")
                    f.write(f"mov rax, [{i}]\n")
                    f.write("PRINT_DEC 8, rax\n")
                    f.write("pop rax\n")
            if is_newline:
                f.write("NEWLINE \n")

def run_command(line):
    tokens = line.split()
    if not tokens:
        return
    data_initialization(tokens)
    get_user_input(tokens)    
    print_statement(line)
    integer_define(tokens)
    string_define(line)
    operations(tokens)

def if_else_statement(block):
    global label_count
    label_count += 1
    else_label = f"L_else_{label_count}"
    end_label = f"L_endif_{label_count}"
    
    cond = block[0].replace("*if", "").replace("{", "").replace("(", "").replace(")", "").split()
    op1, rel, op2 = cond[0], cond[1], cond[2]
    
    has_else = False
    if_lines = []
    else_lines = []
    
    current_target = if_lines
    for line in block[1:]:
        clean = line.replace("}*", "").strip()
        if not clean:
            continue
        if "else" in clean:
            has_else = True
            current_target = else_lines
            continue
        if clean == "}":
            continue
        current_target.append(clean)
        
    with open(file_name, "a") as f:
        f.write(f"\n;If Condition\n")
        f.write("push rax\npush rbx\n")
        if op1 in int_var_list:
            f.write(f"mov rax, [{op1}]\n")
        else:
            f.write(f"mov rax, {op1}\n")
            
        if op2 in int_var_list:
            f.write(f"mov rbx, [{op2}]\n")
        else:
            f.write(f"mov rbx, {op2}\n")
            
        f.write("cmp rax, rbx\n")
        f.write("pop rbx\npop rax\n")
        
        jump_target = else_label if has_else else end_label
        if rel == "==": f.write(f"jne {jump_target}\n\n")
        elif rel == "!=": f.write(f"je {jump_target}\n\n")
        elif rel == ">": f.write(f"jle {jump_target}\n\n")
        elif rel == "<": f.write(f"jge {jump_target}\n\n")
        elif rel == ">=": f.write(f"jl {jump_target}\n\n")
        elif rel == "<=": f.write(f"jg {jump_target}\n\n")

    for cmd in if_lines:
        run_command(cmd)

    if has_else:
        with open(file_name, "a") as f:
            f.write(f"jmp {end_label}\n{else_label}:\n")
        for cmd in else_lines:
            run_command(cmd)
        with open(file_name, "a") as f:
            f.write(f"{end_label}:\n\n")
    else:
        with open(file_name, "a") as f:
            f.write(f"{end_label}:\n\n")

def while_loop_statement(block):
    global label_count
    label_count += 1
    start_label = f"L_loop_start_{label_count}"
    end_label = f"L_loop_end_{label_count}"
    
    cond = block[0].replace("*while", "").replace("{", "").replace("(", "").replace(")", "").split()
    op1, rel, op2 = cond[0], cond[1], cond[2]
    
    loop_lines = []
    for line in block[1:]:
        clean = line.replace("}*", "").strip()
        if not clean or clean == "}":
            continue
        loop_lines.append(clean)
        
    with open(file_name, "a") as f:
        f.write(f"\n;While Loop Start\n")
        f.write(f"{start_label}:\n")
        f.write("push rax\npush rbx\n")
        
        if op1 in int_var_list:
            f.write(f"mov rax, [{op1}]\n")
        else:
            f.write(f"mov rax, {op1}\n")
            
        if op2 in int_var_list:
            f.write(f"mov rbx, [{op2}]\n")
        else:
            f.write(f"mov rbx, {op2}\n")
            
        f.write("cmp rax, rbx\n")
        f.write("pop rbx\npop rax\n")
        
        if rel == "==": f.write(f"jne {end_label}\n\n")
        elif rel == "!=": f.write(f"je {end_label}\n\n")
        elif rel == ">": f.write(f"jle {end_label}\n\n")
        elif rel == "<": f.write(f"jge {end_label}\n\n")
        elif rel == ">=": f.write(f"jl {end_label}\n\n")
        elif rel == "<=": f.write(f"jg {end_label}\n\n")
            
    for cmd in loop_lines:
        run_command(cmd)
        
    with open(file_name, "a") as f:
        f.write(f"jmp {start_label}\n")
        f.write(f"{end_label}:\n\n")
        
code_line = []
fname = input("Enter your file name without extension 'mss' ")

with open(f"{fname}.mss", "r") as f:
    for line in f:
        line = line.strip()
        if line:
            result_line = line.split("?")[0].strip()
            if result_line:
                code_line.append(result_line)
            
file_name = None
int_var_list = []
string_var_list = []

idx = 0
while idx < len(code_line):
    i = code_line[idx]
    
    res = file_creation(i.split())
    if res:
        file_name = res
        idx += 1
        continue
    
    # if-else
    if i.startswith("*if"):
        if_else_string = []
        while idx < len(code_line):
            if_else_string.append(code_line[idx])
            if "}*" in code_line[idx]:
                break
            idx += 1
        if_else_statement(if_else_string)

    # while loop
    elif i.startswith("*while"):
        while_string = []
        while idx < len(code_line):
            while_string.append(code_line[idx])
            if "}*" in code_line[idx]:
                break
            idx += 1
        while_loop_statement(while_string)

    # normal lines
    else:
        run_command(i)
        
    idx += 1

with open(file_name, "a") as f:      
    f.write("xor rax, rax\n")    
    f.write("ret\n")

print("Compilation successful! Open and run the .asm file in SASM.")
