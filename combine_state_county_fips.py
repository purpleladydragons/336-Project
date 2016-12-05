import sys

assert len(sys.argv) == 2

# YOU HAVE TO MANUALLY EDIT HEADER LINE FROM COUNTY AND STATE FIPS INTO ONE FIPS
with open(sys.argv[1], 'r+') as f:
    new_f = []
    good = False
    for line in f:
        if not good:
            good = True
            new_f.append(line)
        else:
            fips_part = line[:6].replace(',','')
            new_f.append(fips_part + line[6:])

    f.seek(0)
    f.write(''.join(new_f))
    f.truncate()
