import sys
import os

Arguments = sys.argv[1:]
FileDirectory = Arguments[0]
OriginalFile = Arguments[1]
ModifiedFile = Arguments[2]
FileLength = os.path.getsize(OriginalFile)

if os.path.exists("BinaryPatch.bp"):
    os.remove("BinaryPatch.bp")

OG = open(OriginalFile, 'rb')
Mod = open(ModifiedFile, 'rb')
PatchFile = open('BinaryPatch.bp', 'a')
OffSet = 0
PatchesStr = f""

PatchFile.write('{\n  "Version": 1,\n  "Patches": [\n') #Beginning of bp file


def OverOneBytePatch(OffSet, PatchesStr): #Function that checks if more than one bytes are different to the original file in a row
    OffSet = OffSet + 1 # Increments file offset \ pointer
    OG.seek(OffSet)
    Mod.seek(OffSet)
    if not OG.read(1) == Mod.read(1): #Checks if bytes are the same or not
        Mod.seek(OffSet) #It uses the wrong byte if I don't re-declare this for some reason
        PatchesStr = PatchesStr + f' {(Mod.read(1)).hex()}' #Adding extra byte to patch statement
        Return = OverOneBytePatch(OffSet, PatchesStr)
        OffSet = Return[0]
        PatchesStr = Return[1]
    return OffSet, PatchesStr


while OffSet < FileLength: #Note: should change this to adding to a string that is later added to the file, meaning I dont have to use truncate
    OG.seek(OffSet)
    Mod.seek(OffSet)
    if not OG.read(1) == Mod.read(1):
        Mod.seek(OffSet)
        PatchesStr = PatchesStr + f'    {{\n      "file": "{FileDirectory}",\n      "offset": {OffSet},\n      "data": "{(Mod.read(1)).hex()}' #Writing patch to string
        Return = OverOneBytePatch(OffSet, PatchesStr)
        OffSet = Return[0]
        PatchesStr = Return[1]
        PatchesStr = PatchesStr + f'"\n    }},\n' #Finishing individual patch
    OffSet = OffSet + 1


OG.close()
Mod.close()

PatchesStr = PatchesStr[:-2] #Removes last comma
PatchFile.write(PatchesStr) #Writing all patches to file
PatchFile.write("\n  ]\n}") #End of bp file

PatchFile.close()
