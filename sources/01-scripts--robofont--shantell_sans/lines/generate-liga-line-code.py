"""
    A script to generate hyphen line ligature code.

    Replaces 3+ hyphens with a horizontal line, up to the width of 50 hyphens.

    Adds handling for emdashes, which macOS automatically turns two hyphens "--" into.

    Specific to repeated hyphens, but could be extended/adjusted for endash, arrows, etc.
"""

maxLine = 50

def subs(replace,max):
    lines = ""
    for i in range(max +1):
        if i <= 2:
            continue
        else:
            # baseName = f"{glyphName.replace('.','_')}.{i}"
            replaceThis = ' '.join([replace for x in range(i)])
            replaceWith = f"{replace}_line.{i}"
            lines += f"    sub {replaceThis} by {replaceWith};"
            lines += "\n"

        # if an even number of hyphens is typed...
        if i % 2 == 0:
            replaceThis = ' '.join(["emdash" for x in range(i) if x%2==0])
            replaceWith = f"{replace}_line.{i}"
            lines += f"    sub {replaceThis} by {replaceWith};"
            if i != max:
                lines += "\n"
        # if an odd number of hyphens is typed...
        elif i % 2 == 1:
            # "emdash emdash hyphen"
            replaceThis = ' '.join(["emdash" for x in range(i-1) if x%2==0]) + f' {replace}'
            replaceWith = f"{replace}_line.{i}"
            lines += f"    sub {replaceThis} by {replaceWith};"
            
            # "hyphen emdash emdash"
            replaceThis = f'{replace} ' + ' '.join(["emdash" for x in range(i-1) if x%2==0])
            replaceWith = f"{replace}_line.{i}"
            lines += f"    sub {replaceThis} by {replaceWith};"
            if i != max:
                lines += "\n"


    return lines

code = f"""\
feature liga {{
{subs('hyphen',50)}
}} liga;
"""

print(code)