# A class for expressing schematic designs
# The data structure used to store the circuit diagram
# Modified from the graph data structure

class circuit_input:
    def __init__(self, serial_number, name=None):
        self.type = 'INPUT'
        self.O = []
        self.serial_number = serial_number
        self.name = name

class circuit_output:
    def __init__(self, serial_number, name=None):
        self.type = 'OUTPUT'
        self.A = None
        self.serial_number = serial_number
        self.name = name

class AND:
    def __init__(self, serial_number):
        self.type = 'AND'
        self.B = None
        self.A = None
        self.O = []        
        self.serial_number = serial_number

class OR:
    def __init__(self, serial_number):
        self.type = 'OR'
        self.A = None
        self.B = None
        self.O = []
        self.serial_number = serial_number

class NOT:
    def __init__(self, serial_number):
        self.type = 'NOT'
        self.A = None
        self.O = []
        self.serial_number = serial_number

class circuit_diagram:
    def __init__(self, edges=[], n=0, elements=[]):
        # edges: (outputFrom, inputTo, port)
        self.nodes = []
        
        for i in range(n):
            if elements[i] == 'INPUT':
                self.nodes.append(circuit_input(i))
            elif elements[i] == 'OUTPUT':
                self.nodes.append(circuit_output(i))
            elif elements[i] == 'AND':
                self.nodes.append(AND(i))
            elif elements[i] == 'OR':
                self.nodes.append(OR(i))
            elif elements[i] == 'NOT':
                self.nodes.append(NOT(i))
            else:
                print('error: unknown element type')
                print("at self > __init__ > for i in range(n):", elements[i])
                exit(1)
        
        for (outputFrom, inputTo, port) in edges:
            # port: AND-A, AND-B, OR-A, OR-B, NOT, INPUT, OUTPUT
            if port == 'AND-A':
                self.nodes[inputTo].A = outputFrom
            elif port == 'AND-B':
                self.nodes[inputTo].B = outputFrom
            elif port == 'OR-A':
                self.nodes[inputTo].A = outputFrom
            elif port == 'OR-B':
                self.nodes[inputTo].B = outputFrom
            elif port == 'NOT':
                self.nodes[inputTo].A = outputFrom
            elif port == 'INPUT':
                self.nodes[inputTo].O.append(outputFrom)
            elif port == 'OUTPUT':
                self.nodes[inputTo].A = outputFrom
            else:
                print('error: unknown port type')
                print("at self > __init__ > for (outputFrom, inputTo, port) in edges:", port)
                exit(1)
            
            self.nodes[outputFrom].O.append(inputTo)

    def addNode(self, type, name=""):
        if type == 'INPUT':
            self.nodes.append(circuit_input(len(self.nodes), name))
        elif type == 'OUTPUT':
            self.nodes.append(circuit_output(len(self.nodes), name))
        elif type == 'AND':
            self.nodes.append(AND(len(self.nodes)))
        elif type == 'OR':
            self.nodes.append(OR(len(self.nodes)))
        elif type == 'NOT':
            self.nodes.append(NOT(len(self.nodes)))
        else:
            print('error: unknown element type')
            print("at self > addNode:", type)
            exit(1)

        return len(self.nodes) - 1
    
    def addEdge(self, outputFrom, inputTo, port):
        # port: AND-A, AND-B, OR-A, OR-B, NOT, INPUT, OUTPUT
        if port == 'AND-A':
            self.nodes[inputTo].A = outputFrom
        elif port == 'AND-B':
            self.nodes[inputTo].B = outputFrom
        elif port == 'OR-A':
            self.nodes[inputTo].A = outputFrom
        elif port == 'OR-B':
            self.nodes[inputTo].B = outputFrom
        elif port == 'NOT':
            self.nodes[inputTo].A = outputFrom
        elif port == 'INPUT':
            self.nodes[inputTo].O.append(outputFrom)
        elif port == 'OUTPUT':
            self.nodes[inputTo].A = outputFrom
        else:
            print('error: unknown port type')
            print("at self > addEdge:", port)
            exit(1)
        
        self.nodes[outputFrom].O.append(inputTo)
    
    def getNodeSerNoByName(self, name):
        # Only INPUT and OUTPUT have "name" label
        for node in self.nodes:
            if node.type in ["INPUT", "OUTPUT"] and node.name == name:
                return node.serial_number
        return None
    
    def getNodeBySerNo(self, serNo):
        for i in self.nodes:
            if i.serial_number == serNo:
                return i

    def draw(self):
        # [1, INPUT] -> [2, AND-A]
        # [2, AND] -> [3, OUTPUT]
        # [nodeSerialNumber, nodeType] -> [nodeSerialNumber, nodeType]

        for outputFrom in self.nodes:
            if (outputFrom.type != "OUTPUT"):
                for inputTo in outputFrom.O:
                    outputFromPort = ""
                    inputToPort = ""
                    inputToNode = self.getNodeBySerNo(inputTo)

                    if outputFrom.type == "INPUT":
                        outputFromPort = outputFrom.name
                    else:
                        outputFromPort = outputFrom.type

                    if inputToNode.type in ["AND", "OR"]:
                        if outputFrom.serial_number == inputToNode.A:
                            inputToPort = inputToNode.type + "-A"
                        elif outputFrom.serial_number == inputToNode.B:
                            inputToPort = inputToNode.type + "-B"
                    elif inputToNode.type == "NOT":
                        inputToPort = inputToNode.type
                    elif inputToNode.type == "OUTPUT":
                        inputToPort = inputToNode.name
                    
                    print('[%d, %s] -> [%d, %s]' % (outputFrom.serial_number, outputFromPort, inputToNode.serial_number, inputToPort))

                    
            else:
                print('[%d, %s]' % (outputFrom.serial_number, outputFrom.type))
    
    def nodeAmount(self):
        return len(self.nodes)
    

# circuit_diagram([edges], n, [elements])
# circuit_diagram.draw() -> print the circuit diagram
# circuit_diagram.addNode(nodeType, *nodeName) -> add a node to the circuit diagram
# circuit_diagram.addEdge(outputFrom, inputTo, port) -> add an edge to the circuit diagram
# circuit_diagram.getNodeSerNoByName(name) -> get the serial number of the node by its name
# circuit_diagram.getNodeBySerNo(serNo) -> get the node by its serial number
# circuit_diagram.nodeAmount() -> get the amount of nodes in the circuit diagram