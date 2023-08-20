#!/usr/bin/env python3.8

# soft version 0.1 of the script
# need to make bespoke variants for each text bin file or confirm a pattern functions.
# all 900+ of the files.
# why were psp games like this

# Current completion rate: 12/934 (0.1%)

import binascii, json, os

targetstrings = [
["FFFFFFFFFFFFFFFFFFFFFF5B","00FFFFFFFFFFFFFF"]
]

def convert_bin_to_json(file, targetfile, fstring, lstring):
    with open(file, 'rb') as f:
        hexdata = binascii.hexlify(f.read())
    decodeHEX = hexdata.decode('utf-8')

    startstr = fstring
    endstr = lstring
    
    ind1 = decodeHEX.find(startstr.lower()) + (len(startstr)-2)
    ind2 = decodeHEX.rfind(endstr.lower()) -4

    trimHEX = decodeHEX[ind1:ind2]
    
    hexBLOCKS = [trimHEX[i:i+2] for i in range(0,len(trimHEX), 2)]
    oLine = 0
    nLine = 0
    key = 1
    json_block = {}
    for hex in hexBLOCKS:
        nLine += 1
        if hex.lower() == "2f":
            data = {
                "data" : binascii.unhexlify("".join(hexBLOCKS[oLine:nLine-1]).strip()).decode("cp932"),
                "translated": ""
            }
            json_block[f"key{key:04d}"] = data
            key+=1
            oLine = nLine + 1
    
    data = {
        "data" : binascii.unhexlify("".join(hexBLOCKS[oLine:nLine]).strip()).decode("cp932"),
        "translated": ""
    }
    json_block[f"key{key:04d}"] = data        

    json_object = json.dumps(json_block, indent=4, ensure_ascii=False).replace(r'\u0000', r'\n').replace(r'\\n', r'\n')#.encode('shift_jis')

    with open(targetfile, 'w', encoding="cp932") as f:
            f.write(json_object)

textPath = r'X:\python\psp\ex\cmn\txt\jp'
files = []
for (dir_path, dir_names, file_names) in os.walk(textPath):
    attemptStrings = targetstrings
    attempts = 0
    for file in file_names:
        currentPath = fr"{dir_path}\{file}"
        newPath = currentPath.replace(r"\jp", r"\en").replace(".bin", ".json")
        print(f"Converting {currentPath}")
        try:
            os.makedirs("\\".join(newPath.split("\\")[:-1]))
        except Exception as e:
            pass
        while attemptStrings:
            try:
                fstr, estr = attemptStrings.pop(0)
                convert_bin_to_json(currentPath, newPath, fstr, estr)
            except Exception as e:
                print(f"Failed on {file} with hexindex {attempts}")
            attempts+=1