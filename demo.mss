file demo
create int x int y int result int counter string first_name string greeting

? 1. Assign values
int x = 15
int y = 5

? 2. Math Operations
op result = x + y
println("15 + 5 = ", result)

op result = x / y
println("15 / 5 = ", result)

? 3. String Operations
string first_name = "User"
string greeting = "Welcome, "
op greeting = greeting + first_name
println(greeting)

? 4. Input & If-Else
println("Enter a number:")
int x = input()

*if ( x == 7 ) {
    println("Lucky number 7!")
} else {
    println("Not lucky today.")
}*

? 5. While Loop
int counter = 1
*while ( counter <= 3 ) {
    println("Loop count: ", counter)
    op counter = counter + 1
}*

println("Done!")
