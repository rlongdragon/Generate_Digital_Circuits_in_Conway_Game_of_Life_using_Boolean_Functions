from circuit_diagram import *

def listInsertRow(list:list, col:int):
    # if len(list) > col: # insert mode
    #     list.insert(col, [0]*len(list[0]))

    #     return list

    while len(list) < col+1: # expand mode
        list.append([0]*len(list[0]))

    return list

def listInsertCol(list:list, row:int):
    if len(list[0]) > row: # insert mode
        for i in range(len(list)):
            list[i].insert(row, 0)

        return list

    while len(list[0]) < row+1: # expand mode
        for i in range(len(list)):
            list[i].append(0)

    return list

def listRemoveCol(list:list, row:int):
    for i in range(len(list)):
        list[i].pop(row)

    return list

def checkList(list:list, x:int, y:int):
    if x >= len(list[0]):
        list = listInsertCol(list, x)
    if y >= len(list):
        list = listInsertRow(list, y)
    
    return list

def addElement(list:list, x:int, y:int, element:int):
    list = checkList(list, x, y)
    list[y][x] = element
    return list

def verticalLink(list:list, x:int, highY:int, lowY:int):
    h = lowY - highY
    
    if h == 0:
        list = addElement(list, x, highY, 8)
        return list

    list = addElement(list, x, highY, 17)
    list = addElement(list, x, lowY, 12)

    for i in range(h-1):
        list = addElement(list, x, highY+i+1, 10)
    
    return list

def rateAndReverse(list:list):
    newList = []
    for i in range(len(list[0])):
        newList.append([0]*len(list))

    for i in range(len(list)):
        for j in range(len(list[0])):
            newList[-j-1][i] = list[i][j]
            if type(newList[-j-1][i]) != int:
                newList[-j-1][i] = 4
    
    return newList

def writeFile(list:list):
    f = open("./draw.txt", "w+")
    f.write(str(list))

def isInput(list:list, y:int):
    for i in range(len(list[0]), 0, -1):
        if type(list[y][i-1]) != int:
            return (True,  list[y][i-1], (i-1, y))
    return (False, 0, (0, 0))

def isNeedStagger(list:list, x:int, y:int):
    for i in range(x, len(list[0])):
        if list[y][i] == 4:
            return True
    return False

def shareInput(list:list, x:int, topY:int, downY:int, end:bool):
    print("shareInput")
    h = downY - topY
    for i in range(h-1):
        list = addElement(list, x, topY+i+1, 7)
    
    if end:
        list = addElement(list, x, downY, 13)
    else:
        list = addElement(list, x, downY, 21)

    return list

def linkPort(list:list[int], leftX:int, rightX:int, y:int):
    for i in range(leftX+1, rightX):
        list = addElement(list, i, y, 8)
    
    return list



scr = [[0]]
x = 0
y = 0
def draw(CD: circuit_diagram, input:list[str], output:list[str]):
    def DFS (CD: circuit_diagram, v:int, visited:list[int]):
        global scr, x, y
        visited[v] = True

        visitType = CD.getNodeBySerNo(v).type
        if visitType == 'INPUT':
            scr = addElement(scr, x, y, CD.getNodeBySerNo(v).name) # put INPUT
            y += 1
            return
        elif visitType == 'OUTPUT':
            scr = addElement(scr, x, y, 5) # put OUTPUT
            x += 1
            scr = addElement(scr, x, y, 8)
            x += 1

            DFS(CD, CD.getNodeBySerNo(v).A, visited)
            return
        elif visitType in ["AND", "OR"]:
            onX = x
            onY = y+1

            if visitType == "AND":
                scr = addElement(scr, x, y, 1)
            elif visitType == "OR":
                scr = addElement(scr, x, y, 2)
            scr = addElement(scr, x, y+1, 12)
            x += 1
            scr = addElement(scr, x, y, 8)
            scr = addElement(scr, x, y+1, 8)

            x += 1

            DFS(CD, CD.getNodeBySerNo(v).A, visited)

            
            if y > onY:
                scr = verticalLink(scr, onX+1, onY, y)
            else:
                scr = addElement(scr, onX+1, y, 8)

            x = onX + 2
            

            DFS(CD, CD.getNodeBySerNo(v).B, visited)

 
            x = onX
            return
        elif visitType == "NOT":
            onX = x

            scr = addElement(scr, x, y, 20)
            x += 1
            scr = addElement(scr, x, y, 8)
            x += 1

            DFS(CD, CD.getNodeBySerNo(v).A, visited)

            x = onX
            return
    
    def setInput(input:list[str]):
        global scr

        scr = listInsertCol(scr, len(scr[0])+2)

        for i in range(len(input)):
            print(input[i])
            waitForShare = []
            for j in range(len(scr)):
                ipt = input[i]
                check = isInput(scr, j)
                if ipt == check[1]:
                    waitForShare.append(check[2])
            if len(waitForShare) == 1:
                scr = addElement(scr, len(scr[0])-1, waitForShare[0][1], 4)
                scr = addElement(scr, len(scr[0])-2, waitForShare[0][1], 8)
                scr = addElement(scr, len(scr[0])-3, waitForShare[0][1], 8)
                continue
            for j in range(len(waitForShare)):
                if j == 0:
                    scr = addElement(scr, len(scr[0])-1, waitForShare[0][1], 4)
                    scr = addElement(scr, len(scr[0])-2, waitForShare[0][1], 8)
                    scr = addElement(scr, len(scr[0])-3, waitForShare[0][1], 6)
                else:
                    scr = shareInput(scr, len(scr[0])-3, waitForShare[j-1][1], waitForShare[j][1], j == len(waitForShare)-1)

            scr = listInsertCol(scr, len(scr[0])-2)

    def replaceStrToNum():
        global scr
        for i in range(len(scr)):
            check = isInput(scr, i)
            if check[0]:
                scr[i][check[2][0]] = 0
    
    def optimize():
        global scr

        for i in range(len(scr)):
            for j in range(len(scr[0])):
                if scr[i][j] != 17:
                    continue
                
                NW = False
                SE = False
                for x in range(j-1, -1, -1):
                    if scr[i][x] == 12:
                        NW = True
                        break
                if not NW:
                    continue
                for y in range(i+1, len(scr)):
                    if scr[y][j] == 12:
                        SE = True
                        break
                if not SE:
                    continue

                scr[i][j] = 0
                NWx = 0
                SEy = 0
                for x in range(j-1, -1, -1):
                    if scr[i][x] == 12:
                        scr[i][x] = 0
                        NWx = x
                        break
                for y in range(i+1, len(scr)):
                    if scr[y][j] == 12:
                        scr[y][j] = 0
                        SEy = y
                        break
                    scr[y][j] = 0

                scr[SEy][NWx] = 12
     
        i = 0
        while i < len(scr[0]):
            flag = True
            for j in range(len(scr)):
                if scr[j][i] not in [0, 8]:
                    flag = False
                    break
            if flag:
                scr = listRemoveCol(scr, i)
                i -= 1

            i += 1

    for i in range(len(output)):
        global x
        x = 0
        DFS(CD, CD.getNodeSerNoByName(output[i]), [False]*CD.nodeAmount())
    
    setInput(input)
    replaceStrToNum()
    optimize()
    writeFile(rateAndReverse(scr))