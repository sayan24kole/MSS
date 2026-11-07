# MSS Programming Language

A simple custom programming language with an ahead-of-time compiler written in Python. It compiles `.mss` source files into 64-bit x86 NASM assembly code, which can be assembled and run directly in SASM using `io64.inc`.

---

## How to Run

1. Make sure you have **Python 3** and **SASM** (configured for x64 NASM) installed.
2. Save your code in a file with the `.mss` extension (e.g. `test.mss`).
3. Run the compiler:
   ```bash
   python compiler.py
   ```
4. Enter your file name without the .mss extension when prompted (e.g. test).
5. Open the generated .asm file in SASM and press F9 (Build and Run).


# Important Rules
* File Declaration First: Every program must start with file <name> to define the output assembly file.
* Initialize Variables Early: Immediately after the file line, all variables (int and string) must be declared using create.
* The op Keyword: Every math operation and string concatenation must start with op.
* Spaces Between Tokens: Always include spaces between operators and variable names (e.g., op c = a + b, not c=a+b).
* Block Syntax: Every if, if-else, and while loop must start with * and close with }*.
* No Nesting (Yet): Blocks cannot be nested inside other blocks. They must be placed sequentially.
* Comments: Everything after a ? is treated as a comment and ignored.

# Syntax Reference

## 1. File Declaration
Creates the .asm file and includes io64.inc:
```
file my_program
```
## 2. Variable Creation
All variables must be defined on one line right after the file declaration:
```
create int a int b int c string s1 string s2
```
## 3. Assigning Values
```
int a = 10                  ? Assigns integer 10 to a
int b = 20                  ? Assigns integer 20 to b
string s1 = "Hello "        ? Assigns string literal to s1
string s2 = "World!"        ? Assigns string literal to s2
```
## 4. User Input
Reads a 64-bit integer from the console:
```
int a = input()
```
## 5. Arithmetic Operations
Supports addition (+), subtraction (-), multiplication (*), division (/), and modulus (%). You can use variables or literal numbers:
```
op c = a + b                ? Addition
op c = a - b                ? Subtraction
op c = a * b                ? Multiplication
op c = a / b                ? Division
op c = a % b                ? Modulus (remainder)
op a = a + 1                ? Incrementing a variable
```
## 6. String Operations (Concatenation)
Merges two string variables using +:
```
op s3 = s1 + s2
```
## 7. Printing Output
print(...): Prints on the same line.<br>
println(...): Prints and moves to a new line.<br>
Can print string literals, string variables, and integers separated by commas:
```
print("Hello ")
println("World")
println("The sum is: ", c)
println("Message: ", s3)
```
## 8. If & If-Else Branching
Must be wrapped inside *if ... }*:
```
? If-Else
*if ( a > b ) {
    println("a is greater than b")
} else {
    println("a is less than or equal to b")
}*

? Standalone If
*if ( a == 10 ) {
    println("a equals 10")
}*
```
## 9. While Loops
Must be wrapped inside *while ... }*:
```
*while ( a < 5 ) {
    println("Current count: ", a)
    op a = a + 1
}*
```
## Comparison Operators

Used inside `if` and `while` conditions:

| Operator | Meaning |
| :---: | :--- |
| `==` | Equal to |
| `!=` | Not equal to |
| `>` | Greater than |
| `<` | Less than |
| `>=` | Greater than or equal to |
| `<=` | Less than or equal to |
