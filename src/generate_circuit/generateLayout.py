from circuit_diagram import *
from colorTerminal import color as c

def infix2postfix(infix):
    weight = {"(": 0, "&": 1, "|": 1, "!": 2}
    stack = []
    postfix = ""
    temp = ""

    for i in infix:
        if i != " ":
            if (i not in weight) and (i != ")"):
                temp += i
            else:
                if i in "&|!":
                    while stack and weight[stack[-1]] >= weight[i]:
                        postfix += " " + stack.pop()
                    stack.append(i)
                elif i == "(":
                    stack.append(i)
                elif i == ")":
                    while stack[-1] != "(":
                        postfix += " " + stack.pop()
                    stack.pop()

        elif i == " " and temp != "":
            postfix += " " + temp
            temp = ""
        
    return (postfix + " " + temp + " " + " ".join(stack[::-1]))

def postfix2circuit(postfix: str, circuit: circuit_diagram):
    stack = []
    for i in postfix.split():
        if i == "&":
            B = stack.pop()
            A = stack.pop()
            ser = circuit.addNode('AND')
            circuit.addEdge(A, ser, 'AND-A')
            circuit.addEdge(B, ser, 'AND-B')
            stack.append(ser)
        elif i == "|":
            B = stack.pop()
            A = stack.pop()
            ser = circuit.addNode('OR')
            circuit.addEdge(A, ser, 'OR-A')
            circuit.addEdge(B, ser, 'OR-B')
            stack.append(ser)
        elif i == "!":
            A = stack.pop()
            ser = circuit.addNode('NOT')
            circuit.addEdge(A, ser, 'NOT')
            stack.append(ser)
        else:
            ser = circuit.getNodeSerNoByName(i)
            if (ser):
                stack.append(ser)
            else:
                ser = circuit.addNode('INPUT', i)
                stack.append(ser)
    
    return [circuit, stack.pop()]

print("Input description:")
print(f"The input step has three parts, namely {c('INPUT', 2)}, {c('OUTPUT', 3)} and {c('Boolean function', 6)}")
print(f"When entering, please separate different objects with spaces")
print(f"For example:\n{c('INPUT', 2)}: A B C\n{c('OUTPUT', 3)}: X Y\n{c('Boolean function', 6)}: A & B | C & ( ! A ) & ( ! B )")
print("")
IN = input(f"{c('INPUT', 2)}: ").split()
OUT = input(f"{c('OUTPUT', 3)}: ").split()
FUC = []
for i in OUT:
    ipt = input(f"{c('Boolean function', 6)} of {c(i, 6)}: ")
    f = infix2postfix(ipt)
    FUC.append(f)

print("")

circuit = circuit_diagram()
for i in range(len(OUT)):
    circuit, ser = postfix2circuit(FUC[i], circuit)
    outSer = circuit.addNode('OUTPUT', OUT[i])
    circuit.addEdge(ser, outSer, 'OUTPUT')
circuit.draw()

print("")

from draw import draw
draw(circuit, IN, OUT)
