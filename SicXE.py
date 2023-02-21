import pandas as pd 
import pandasgui as pdg
from tabulate import tabulate

## reading the file to get the memory start,length and end
def sicxeFunc(path, LOC):

    f =  open(path,'r') 
    xSYMTAB = {}
    xSYMTAB2 = [["CSEC", "VAR", "ADDRESS", "LENGTH"]]
    # First Pass SIC/XE

    # LOC = "004C2B" 
    oldLOC = LOC

    for line in f:

        if line[0] == "H":
            progName = line[1:7].translate({ord(letter): None for letter in "0"})
            xSYMTAB[progName] = [LOC.upper(), line[-7:-1]]
            xSYMTAB2 += [[progName, "", LOC.upper(), line[-7:-1]]]
            LOC = hex(int(LOC, 16) + int(line[-7:-1], 16))[2:].zfill(6)

        elif line[0] == "D":
            
            subLine = line[1:-1]
            i = 0
            
            # 6 bytes name + 6 bytes location = 12
            # (subLine[12 * 0 : 12 * 0 + 6] = subLine[0:6]) = (subLine[12 * 0 + 6 : 12 * 0 + 12] = subLine[6:12])
            while i < int(len(subLine) / 12):
                varName = subLine[12 * i: 12 * i + 6].translate({ord(letter): None for letter in "0"})
                varAddress = hex(int(subLine[12 * i + 6: 12 * i + 12], 16) + int(oldLOC, 16))[2:].zfill(6).upper()
                xSYMTAB[varName] = [varAddress]
                xSYMTAB2 += [["", varName, varAddress, ""]]
                i = i + 1

            oldLOC = LOC

    f.close()

    EXTSYMWRITE = open("Ext_sym_Table.txt", "w")
    EXTSYMWRITE.writelines(tabulate(xSYMTAB2, headers="firstrow", tablefmt="grid"))
    EXTSYMWRITE.close()

    # Second Pass SIC/XE


    addresses = []
    start_int = list(xSYMTAB.values())[0][0]       #First Address indictionary
    start_int = int(start_int[:-1] + "0", 16)  
    end_int = int(LOC, 16)
    next_address = start_int

    while next_address < (end_int + 16):

        addresses.append(hex(next_address)[2:].zfill(6).upper())
        next_address = start_int + 16
        start_int = next_address
    

    #creating a dataframe for the memory graph

    df = pd.DataFrame()
    df = df.assign(**{'Addresses':addresses,'0': 'X', '1': 'X', '2': 'X','3':'X','4':'X','5':'X','6':'X','7':'X','8':'X','9':'X','A':'X','B':'X','C':'X','D':'X','E':'X','F':'X'})
    df = df.set_index('Addresses')

    # print(df)

    f =  open(path,'r') 

    progStart = ""
    
    for line in f:

        if line[0] == "H":
            progStart = xSYMTAB[line[1:7].translate({ord(letter): None for letter in "0"})][0]
            # print(progStart)

        if line[0] == "T":
            startT = hex(int(line[1:7], 16) + int(progStart, 16))[2:].zfill(6).upper()
            col = startT[-1].upper()
            startT = startT[:-1] + '0'

            modified = line[9:]
            i = 0

            while i <  len(modified) - 1:

                df.at[startT, col] = (modified[i] + modified[i + 1])

                if int(col, 16) < 15:
                    col = hex(int(col, 16) + 1)[2:].upper()

                else:
                    col = "0"
                    startT = hex(int(startT, 16) + 16)[2:].upper().zfill(6)

                i = i + 2

        if line[0] == "M":

            startT = hex(int(line[1:7], 16) + int(progStart, 16))[2:].zfill(6).upper()
            col = startT[-1].upper()
            startT = startT[:-1] + '0'

            colCopy = col
            startTCopy = startT

            modified = df.loc[startT, col]
            i = 0

            while i < 2:
                if int(col, 16) < 15:
                    col = hex(int(col, 16) + 1)[2:].upper()
                    modified += df.loc[startT, col]

                else:
                    col = "0"
                    startT = hex(int(startT, 16) + 16)[2:].upper().zfill(6)
                    modified += df.loc[startT, col]

                i = i + 1

            if line[8] == "5":
                firstChar = modified[0]

                if line[9] == "+":
                    modified = hex(int(modified[1:], 16) + int(xSYMTAB[line[10:-1]][0], 16))[2:].zfill(5).upper()

                else:
                    modified = hex((int(modified[1:], 16) - int(xSYMTAB[line[10:-1]][0], 16)) & (2**24-1))[2:].zfill(5).upper()

                modified = firstChar + modified

            else:
                
                if line[9] == "+":

                    modified = hex(int(modified, 16) + int(xSYMTAB[line[10:-1]][0], 16))[2:].zfill(6).upper()
                    modified = modified[-6:]


                else:

                    modified = hex((int(modified, 16) - int(xSYMTAB[line[10:-1]][0], 16)) & (2**24-1))[2:].zfill(6).upper()
                    modified = modified[-6:]

            i = 0
            while i < 5:

                df.at[startTCopy, colCopy] = (modified[i] + modified[i + 1])

                if int(colCopy, 16) < 15:
                    colCopy = hex(int(colCopy, 16) + 1)[2:].upper()

                else:
                    colCopy = "0"
                    startTCopy = hex(int(startTCopy, 16) + 16)[2:].upper().zfill(6)

                i = i + 2

    pdg.show(df)