# gro.py
For gro file of gromacs

## GroAtom class
### usage
    atom = GroAtom(res_num, res_name, atom_name, atom_num, position, velocity)
### variable
    res_num: int, residue number
    res_name: str, residue name
    atom_name: str, atom name
    atom_num: int, atom number
    position: list, [x, y, z]
    velocity: list, [vx, vy, yz]
### GroAtom.res_num()
    return residue number(int)
### GroAtom.res_name()
    return residue name(str)
### GroAtom.atom_name()
    return atom name(str)
### GroAtom.atom_num()
    return atom num(int)
### GroAtom.position()
    return position(list)
### GroAtom.velocity()
    return velocity
### GroAtom.change_res_num(num)
    num: int
    change residue number of atom to num
### GroAtom.change_atom_num(num)
    num: int
    change atom number of atom to num
### GroAtom.change_res_name(name)
    name: str
    change residue name of atom to "name"
### GroAtom.change_atom_name(name)
    name: str
    change atom name of atom to "name"
### GroAtom.get_str_gro_format()
    return atom parameters with gro format(str)
    gro_format = '{res_num:>5d}{res_name:<5s}{atom_name:>5s}{atom_num:>5d}' \
                     '{x:>8.3f}{y:>8.3f}{z:>8.3f}{vx:>8.4f}{vy:>8.4f}{vz:>8.4f}'

## GroRes class
GroRes is class for handling residue. This is collection of GroAtom.
### usage
    residue = GroRes(atoms)
### variable
    atoms: list of GroAtom obj, [atom1, atom2, ...]
### GroRes.name()
    if 1 residue number in residue, return number (int)
    else return residue numbers(list)
### GroRes.num()
    if 1 residue name in residue, return name (int)
    else return residue names(list)
### GroRes.atoms()
    return atoms in residue("list of GroAtom objects")
### GroRes.num_of_atoms()
    return number of atoms in residue(int)
### GroRes.change_res_nums(num) 
    num: int
    change residue number of atoms in residue to num
### GroRes.change_res_names(name)
    name: str
    change residue name of atoms in residue to name
### GroRes.change_atom_nums(num_i)
    change atom numbers
    set num_i(int) as the first number
    change with serial number  
     
    
## Gro class
parse gro file and read parameters
### usage
    gro_obj = Gro(path)
### variable
    path: paht of gro file(str)
### Gro.path()
    return gro file path
### Gro.title()
    return title section(str)
### Gro.num_of_atoms()
    return number of atoms(int) 
### Gro.box_vectors()
    return bo vectors section("list of float")
### Gro.residues()
    return list of residues("GroRes object")
### Gro.atoms()
    return list of atoms("GroAtom object")
### Gro.generate_gro()
    generate gro file
### Gro.residue_alignment()
    alignment residues by residue name 
    and renumbering the residue number from 1
    (example)
    0ResA    1ResA
    1ResB -> 2ResA
    2ResA    3ResB
### Gro.delete_residues_from_name(name)
    name: residue name (str)
    delete residues with residue name 'name'
### Gro.add_residues(residue_ojb_list)
    residue_ojb_list: list of GroRes obj(list)
    add resdidues
### Gro.res_nums()
    return list of residue numbers
### change_res_name(name, residue_nums)
    name: str
    residue_nums: list of residue numbers(int)
    change the name of residue matching the residue number to "name" 