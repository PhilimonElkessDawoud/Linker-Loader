import Sic
import SicXE

print("Welcome to Linker Loader \n")

path = input("Please add file path: ")
print("\n")

while(True):

    x = input("For SIC press: 1 / For SIC/XE press: 2 \n")

    if(x == "1"):
        Sic.sicFunc(path)
        break

    elif(x == "2"):
        LOC = input("Please Enter Start Address: ")

        try:
            SicXE.sicxeFunc(path, LOC.upper())
            break
        except:
            print("Invalid Address!")

    else:
        print("Invalid Input!\n")

