"""
    A script to generate line recipes 
    for RoboFont Glyph Construction.
"""

def lines(glyphName, max):
    for i in range(max +1):
        if i <= 2:
            continue
        else:
            baseName = f"{glyphName.replace('.','_')}.{i}"
            recipe = ' & '.join([glyphName for x in range(i)])
            print(baseName + " = " + recipe)
        
lines("hyphen.line", 50)