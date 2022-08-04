# Aemulus-Binary-Patcher
Python script that automates creating binary patches for [Aemulus Package Manager.](https://github.com/TekkaGB/AemulusModManager)

Tested and made with Python 3.10

Usage:

py AemBinaryPatcher.py (File directory of the file inside of the games data archive, ex: facility\\\\cmbroot\\\\ps_model.bin) (File directory of the original, unchanged file) (File directory of the modified file)

Example argument:

py AemBinaryPatcher.py facility\\\\cmbroot\\\\ps_model.bin "Original\ps_model.bin" "Modified\ps_model.bin"

A binary patch will be generated in the same directory of the python file.
