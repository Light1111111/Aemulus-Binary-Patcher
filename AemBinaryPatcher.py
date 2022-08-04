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
PatchFileA = open('BinaryPatch.bp', 'a') #Patchfile edited as a text file
PatchFileB = open('BinaryPatch.bp', 'rb+') #Patchfile edited as a binary file

PatchFileA.write('{\n  "Version": 1,\n  "Patches": [\n') #Beginning of bp file

for i in range(FileLength): #Goes through the entire file(s) byte by byte
    OG.seek(i) #Increments file pointer \ offset
    Mod.seek(i)
    if not OG.read(1) == Mod.read(1): #Checks if bytes are the same or not
        Mod.seek(i) #It uses the next byte if I don't re-declare this for some reason, and I have no idea why
        PatchFileA.write(f'    {{\n      "file": "{FileDirectory}",\n      "offset": {i},\n      "data": "{(Mod.read(1)).hex()}"\n    }},\n') #Writes patches

PatchFileB.seek(-3, os.SEEK_END) #goes three bytes from the end of the file to get to the last comma
PatchFileB.truncate() #Removes last comma
PatchFileA.write("\n  ]\n}") #End of bp file

OG.close()
Mod.close()
PatchFileA.close()
PatchFileB.close()
