import sys
import os

Arguments = sys.argv[1:]
FileDirectory = Arguments[0]
OriginalFile = Arguments[1]
ModifiedFile = Arguments[2]
FileLength = os.path.getsize(OriginalFile)

if Arguments == []:
    print("Erorr: no files specified in argument")
    quit()

if os.path.exists("BinaryPatch.bp"):
    os.remove("BinaryPatch.bp")

OG = open(OriginalFile, 'rb')
Mod = open(ModifiedFile, 'rb')
PatchFile = open('BinaryPatch.bp', 'a')
OverOneByteList = []

PatchFile.write('{\n  "Version": 1,\n  "Patches": [\n') #Beginning of bp file

def OverOneBytePatch(Counter): #Function that checks if more than one bytes are different to the original file in a row
    OG.seek(i + Counter)  # Increments file pointer \ offset
    Mod.seek(i + Counter)
    if not OG.read(1) == Mod.read(1): #Checks if bytes are the same or not
        OverOneByteList.append(i + Counter) #Adds specific offset to exclusion list so duplicate patches aren't created
        Mod.seek(i + Counter) #It uses the next byte if I don't re-declare this for some reason, and I have no idea why
        PatchFile.write(f' {(Mod.read(1)).hex()}') #Writes patches
        OverOneBytePatch(Counter + 1)

for i in range(FileLength): #Goes through the entire file(s) byte by byte
    OG.seek(i) #Increments file pointer \ offset
    Mod.seek(i)
    if not OG.read(1) == Mod.read(1) and i not in OverOneByteList: #Checks if bytes are the same or not
        Mod.seek(i) #It uses the next byte if I don't re-declare this for some reason, and I have no idea why
        PatchFile.write(f'    {{\n      "file": "{FileDirectory}",\n      "offset": {i},\n      "data": "{(Mod.read(1)).hex()}') #Writes patches
        OverOneBytePatch(1)
        PatchFile.write(f'"\n    }},\n')

OG.close()
Mod.close()
PatchFile.close()

PatchFile = open('BinaryPatch.bp', 'rb+') #If I assign two different patch file variables from the start then the length returned from os.seek_end is incorrect for some reason, so I have to do it this way
PatchFile.seek(-3, os.SEEK_END) #Three places back so it catches the comma
PatchFile.truncate() #Deletes last comma

PatchFile.close()

PatchFile = open('BinaryPatch.bp', 'a')
PatchFile.write("\n  ]\n}") #End of bp file

PatchFile.close()
