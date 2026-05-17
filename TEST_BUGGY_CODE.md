# Test Cases with ACTUAL Bugs

## Java Code with Bugs

```java
mport java.util.Scanner;  // BUG: Typo - should be "import"

public class Calculator {
    public static void main(String[] args) {

        Scanner input = new Scanner(System.in);

        double num1, num2;
        char op;

        System.out.print("Enter operator (+, -, *, /): ");
        op = input.next().charAt(0);

        System.out.print("Enter two numbers: ")  // BUG: Missing semicolon
        num1 = input.nextDouble();
        num2 = input.nextDouble();

        switch(op) {

            case '+':
                System.out.println("Result = " + (num1 + num2));
                break;

            case '-':
                System.out.println("Result = " + (num1 - num2))  // BUG: Missing semicolon
                break;

            case '*':
                System.out.println("Result = " + (num1 * num2));
                break;

            case '/':
                if(num2 != 0)
                    System.out.println("Result = " + (num1 /);  // BUG: Incomplete expression
                else
                    Sytem.out.println("Error! Division by zero.");  // BUG: Typo - "Sytem" should be "System"
                break;

            default:
                System.out.println("Invalid operator!");
        }

        input.close();
    }
}
```

**Expected Bugs to Find:**
1. Line 1: Typo `mport` → `import`
2. Line 13: Missing semicolon after print statement
3. Line 24: Missing semicolon after println
4. Line 31: Incomplete expression `num1 /` (missing num2)
5. Line 33: Typo `Sytem` → `System`

---

## JavaScript Code with Bugs

```javascript
// Simple Calculator

let num1 = parseFloat(prompt("Enter first number:"));
let op = prompt("Enter operator (+, -, *, /):")  // BUG: Missing semicolon (recommended in JS)
let num2 = parseFloat(prompt("Enter second number:"));

if (op === '+') {
    consol.log("Result =", num1 + num2);  // BUG: Typo - "consol" should be "console"
}

else if (op === '-') {
    console.log("Result =", num1 - num2)  // BUG: Missing semicolon
}

else if (op === '*') {
    console.log("Result =", num1 * num2);
}

else if (op === '/') {
    if (num2 !== 0) {
        console.log("Result =", num1 /);  // BUG: Incomplete expression
    } else {
        console.log("Error! Division by zero.");
    }
}

else {
    console.log("Invalid operator!")  // BUG: Missing semicolon
}
```

**Expected Bugs to Find:**
1. Line 4: Missing semicolon (JS best practice)
2. Line 8: Typo `consol` → `console`
3. Line 12: Missing semicolon
4. Line 20: Incomplete expression `num1 /` (missing num2)
5. Line 27: Missing semicolon

---

## C++ Code with Bugs

```cpp
#include <iostream>
using namespace std

int main() {
    char op;
    double num1, num2;

    cou << "Enter operator: ";  // BUG: Typo - "cou" should be "cout"
    cin >> op;

    cout << "Enter numbers: "  // BUG: Missing semicolon
    cin >> num1 >> num2;

    switch(op) {
        case '+':
            cout << "Result = " << num1 + num2;  // BUG: Missing semicolon
            break;

        case '-':
            cout << "Result = " << num1 - num2;
            break

        case '*':
            cout << "Result = " << (num1 * num2);
            break;

        case '/':
            if(num2 != 0)
                cout << "Result = " << num1 /;  // BUG: Incomplete expression
            else
                cout << "Error!";
            break;
    }
    return 0;
}
```

**Expected Bugs to Find:**
1. Line 2: Missing semicolon after `using namespace std`
2. Line 8: Typo `cou` → `cout`
3. Line 11: Missing semicolon
4. Line 16: Missing semicolon
5. Line 21: Missing semicolon after `break`
6. Line 29: Incomplete expression `num1 /` (missing num2)

---

## Python Code with Bugs

```python
import math

def calculator():
    num1 = float(input("Enter first number: "))
    op = input("Enter operator (+, -, *, /): ")
    num2 = float(input("Enter second number: "));  # BUG: Unnecessary semicolon in Python
    
    if op == '+':
        print("Result =", num1 + num2)
    elif op == '-':
        print("Result =", num1 - num2)
    elif op == '*':
        print("Result =", num1 * num2)
    elif op == '/':
        if num2 != 0:
            print("Result =", num1 /)  # BUG: Incomplete expression
        else:
            print("Error! Division by zero.")
    else:
        print("Invalid operator!")

calculator()
```

**Expected Bugs to Find:**
1. Line 6: Unnecessary semicolon (Python doesn't use semicolons)
2. Line 16: Incomplete expression `num1 /` (missing num2)

---

## How to Test

1. Copy each buggy code example above
2. Paste into BugFinderFixer at http://localhost:3000
3. Select the correct language (Java, JavaScript, C++, or Python)
4. Click "Analyze Code"
5. Verify the AI finds ALL the bugs listed

## Expected Behavior

- ✅ AI should find ALL bugs in each language
- ✅ AI should apply language-specific rules
- ✅ AI should NOT flag correct code as buggy
- ✅ AI should provide accurate fixes
- ✅ Fixed code should be syntactically correct

---

**Note:** The original code examples you provided were actually CORRECT and had no bugs. That's why the AI said they were fine!