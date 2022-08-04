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

PatchFile.write('{\n  "Version": 1,\n  "Patches": [\n') #Beginning of bp file


def OverOneBytePatch(OffSet): #Function that checks if more than one bytes are different to the original file in a row
    OffSet = OffSet + 1 # Increments file offset \ pointer
    OG.seek(OffSet)
    Mod.seek(OffSet)
    if not OG.read(1) == Mod.read(1): #Checks if bytes are the same or not
        Mod.seek(OffSet) #It uses the wrong byte if I don't re-declare this for some reason
        PatchFile.write(f' {(Mod.read(1)).hex()}') #Writes patches
        OffSet = OverOneBytePatch(OffSet)
    return OffSet


while OffSet < FileLength:
    OG.seek(OffSet)
    Mod.seek(OffSet)
    if not OG.read(1) == Mod.read(1):
        Mod.seek(OffSet)
        PatchFile.write(f'    {{\n      "file": "{FileDirectory}",\n      "offset": {OffSet},\n      "data": "{(Mod.read(1)).hex()}')  # Writes patches
        OffSet = OverOneBytePatch(OffSet)
        PatchFile.write(f'"\n    }},\n')
    OffSet = OffSet + 1


OG.close()
Mod.close()
PatchFile.close()

PatchFile = open('BinaryPatch.bp', 'rb+')
PatchFile.seek(-3, os.SEEK_END) #Three places back so it catches the comma
PatchFile.truncate() #Deletes last comma

PatchFile.close()

PatchFile = open('BinaryPatch.bp', 'a')
PatchFile.write("\n  ]\n}") #End of bp file

PatchFile.close()
