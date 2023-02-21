import pandas as pd 
import pandasgui as pdg
## reading the file to get the memory start,length and end

def sicFunc(path):

    f =  open(path,'r') 
    header = f.readline() 



    start_address = header[7:-7]
    end_address = hex(int(start_address,16) + int(header[-6:],16))[2:].zfill(6).upper()
    real_end = (end_address[:-1] + '0').zfill(6).upper()

    #Adding adresses to an empty list
    addresses = []
    start_int = int(start_address[:-1] + "0", 16) 
    end_int = int(real_end, 16)
    next_address = start_int

    while next_address < (end_int + 16):

        addresses.append(hex(next_address)[2:].zfill(6).upper())
        next_address = start_int + 16
        start_int = next_address
    
    #creating a dataframe for the memory graph

    df = pd.DataFrame()
    df = df.assign(**{'Addresses':addresses,'0': 'X', '1': 'X', '2': 'X','3':'X','4':'X','5':'X','6':'X','7':'X','8':'X','9':'X','A':'X','B':'X','C':'X','D':'X','E':'X','F':'X'})
    df = df.set_index('Addresses')

    #how to fill the rows

    T_rec = f.readlines()[0:-1]

    for record in T_rec:
        startT = record[1:7]
        col = startT[-1].upper()
        startT = startT[:-1] + '0'
        rest = record[9:]
        i = 0

        while i <  len(rest) - 1:

            df.at[startT, col] = (rest[i] + rest[i + 1])

            if int(col, 16) < 15:
                col = hex(int(col, 16) + 1)[2:].upper()

            else:
                col = "0"
                startT = hex(int(startT, 16) + 16)[2:].upper().zfill(6)

            i = i + 2

    pdg.show(df)



