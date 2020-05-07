# lmp2cfg.py v.1.0
# convert lammps dump file to atomeye cfg file.
# lammps: https://lammps.sandia.gov/
# atomeye: http://li.mit.edu/Archive/Graphics/A/
import sys

args = sys.argv
if len(args) == 1:
    print("\x1b[31m error:\x1b[39m no input file.")
    print("python lmp2cfg.py <dumpfile>")
    sys.exit(1)

inputfilename = args[1]
outputfilename = inputfilename.split(".")[0] + ".cfg"

numberOfAtoms = 0
types = []
cellSize = [0, 0, 0]
atoms = []

try:
    with open(inputfilename) as inputfile:

        print("Now reading {}".format(inputfilename))
        flag = ""
        xyzcol = [0, 0, 0]
        typecol = None
        coodinatetype = ""

        for line in [s.strip() for s in inputfile.readlines()]:

            # get values
            if flag == "number":
                numberOfAtoms = int(line)
                flag = ""

            elif flag == "box-x":
                cellSize[0] = float(line.split()[1]) - float(line.split()[0])
                flag = "box-y"

            elif flag == "box-y":
                cellSize[1] = float(line.split()[1]) - float(line.split()[0])
                flag = "box-z"

            elif flag == "box-z":
                cellSize[2] = float(line.split()[1]) - float(line.split()[0])
                flag = ""

            elif flag == "atoms":
                cols = line.split()
                if coodinatetype == "unscaled":
                    x = float(cols[xyzcol[0]]) / cellSize[0]
                    y = float(cols[xyzcol[1]]) / cellSize[1]
                    z = float(cols[xyzcol[2]]) / cellSize[2]
                elif coodinatetype == "scaled":
                    x = float(cols[xyzcol[0]])
                    y = float(cols[xyzcol[1]])
                    z = float(cols[xyzcol[2]])

                if typecol == None:
                    atoms.append([0, x, y, z])
                else:
                    atoms.append([int(cols[typecol]), x, y, z])

                    if not int(cols[typecol]) in types:
                        types.append(int(cols[typecol]))

            # set flag
            if line == "ITEM: NUMBER OF ATOMS":
                flag = "number"
            elif line[0:16] == "ITEM: BOX BOUNDS":
                flag = "box-x"
            elif line[0:11] == "ITEM: ATOMS":
                flag = "atoms"
                cols = line.split()
                if "x" in cols and "y" in cols and "z" in cols:
                    xyzcol[0] = cols.index("x") - 2
                    xyzcol[1] = cols.index("y") - 2
                    xyzcol[2] = cols.index("z") - 2
                    coodinatetype = "unscaled"
                elif "xs" in cols and "ys" in cols and "zs" in cols:
                    xyzcol[0] = cols.index("xs") - 2
                    xyzcol[1] = cols.index("ys") - 2
                    xyzcol[2] = cols.index("zs") - 2
                    coodinatetype = "scaled"
                else:
                    print("Error: lmt2cfg.py requires coordinate (x y z or xs ys zs) args in dump file.")
                    sys.exit(1)

                if "type" in cols:
                    typecol = cols.index("type") - 2

except Exception as e:
    print(e)
    sys.exit(1)

# ask atom mass and element for each atom type
types.sort()
masses = {}
elements = {}
if len(types) >= 1:
    print("{} atom types are found. Input mass and element for each atom type.".format(len(types)))
    for atomtype in types:
        print("For #{}".format(atomtype))
        print(" mass: ", end='')
        masses[atomtype] = input()
        print(" element: ", end='')
        elements[atomtype] = input()

else:
    print("No type argument in dump file. All atoms are considered to be the same.")
    print(" mass: ", end='')
    masses[0] = input()
    print(" element: ", end='')
    elements[0] = input()

# output cfg file
try:
    with open(outputfilename, "w") as out:
        out.write("Number of particles = {}\n".format(numberOfAtoms))
        out.write("A = 1 Angstrom (basic length-scale)\n")
        out.write("H0(1,1) = {} A\n".format(cellSize[0]))
        out.write("H0(1,2) = 0 A\n")
        out.write("H0(1,3) = 0 A\n")
        out.write("H0(2,1) = 0 A\n")
        out.write("H0(2,2) = {} A\n".format(cellSize[1]))
        out.write("H0(2,3) = 0 A\n")
        out.write("H0(3,1) = 0 A\n")
        out.write("H0(3,2) = 0 A\n")
        out.write("H0(3,3) = {} A\n".format(cellSize[2]))
        for atom in atoms:
            out.write("{} {} {} {} {} 0 0 0\n".format(masses[atom[0]], elements[atom[0]], atom[1], atom[2], atom[3]))

except Exception as e:
    print(e)
    sys.exit(1)