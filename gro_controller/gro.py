import os

"""
Gromacs gro file controller
"""


class GroAtom(object):

    def __init__(self, res_num, res_name, atom_name, atom_num, position, velocity):
        """

        :param atom_name: str
        :param atom_num: int
        :param position: list
        :param velocity: list
        """
        self.__res_num = res_num
        self.__res_name = res_name
        self.__atom_name = atom_name
        self.__atom_num = atom_num
        self.__position = position
        self.__velocity = velocity

    def res_num(self):
        return self.__res_num

    def res_name(self):
        return self.__res_name

    def atom_name(self):
        return self.__atom_name

    def atom_num(self):
        return self.__atom_num

    def position(self):
        return self.__position

    def velocity(self):
        return self.__velocity

    def change_res_num(self, new_num):
        self.__res_num = new_num

    def change_atom_num(self, new_num):
        self.__atom_num = new_num

    def change_res_name(self, new_name):
        self.__res_name = new_name

    def change_atom_name(self, new_name):
        self.__atom_name = new_name

    def get_str_gro_format(self):
        gro_format = '{res_num:>5d}{res_name:<5s}{atom_name:>5s}{atom_num:>5d}' \
                     '{x:>8.3f}{y:>8.3f}{z:>8.3f}{vx:>8.4f}{vy:>8.4f}{vz:>8.4f}'
        x, y, z = self.position()
        vx, vy, vz = self.velocity()
        gro_str = gro_format.format(res_num=self.res_num(), res_name=self.res_name(),
                                    atom_name=self.atom_name(), atom_num=self.atom_num(),
                                    x=x, y=y, z=z, vx=vx, vy=vy, vz=vz)
        return gro_str


class GroRes(object):

    def __init__(self, atoms):
        """

        :param atoms: list
        """
        self.__atoms = atoms

    def num(self):
        nums = []
        for atom in self.__atoms:
            nums.append(atom.res_num())
        nums = set(nums)
        if len(nums) == 1:
            return list(nums)[0]
        else:
            return nums

    def name(self):
        names = []
        for atom in self.__atoms:
            names.append(atom.res_name())
        names = set(names)
        if len(names) == 1:
            return list(names)[0]
        else:
            return names

    def atoms(self):
        return self.__atoms

    def num_of_atoms(self):
        return len(self.__atoms)

    def change_res_nums(self, new_num):
        for atom in self.__atoms:
            atom.change_res_num(new_num)

    def change_res_names(self, new_name):
            for atom in self.__atoms:
                atom.change_res_name(new_name)

    def change_atom_nums(self, num_i):
        new_num = num_i
        for atom in self.__atoms:
            atom.change_atom_num(new_num)
            new_num += 1


class Gro(object):

    def __init__(self, gro_file_path):

        self.__path = gro_file_path
        if not os.path.exists(gro_file_path):
            print('{} is not exists.'.format(gro_file_path))

        self.__parse()

    def __parse(self):
        """
        read title(str), number of atoms(int), atoms, box vectors(list)
        :return:
        """

        path = self.__path
        with open(path, 'r') as gro:

            self.__residues = []
            res_num_before_addition = 0
            res_atoms_before_addition = []
            line_number = 0
            for line in gro:
                line_number += 1

                # title
                if line_number == 1:
                    self.__title = line.strip()

                # number of atoms
                elif line_number == 2:
                    self.__num_of_atoms = int(line.strip())

                # box vector(last line)
                elif line_number == self.__num_of_atoms + 3:
                    self.__box_vectors = [float(k) for k in line.strip().split()]

                    # add last residue
                    if res_atoms_before_addition:
                        self.__residues.append(GroRes(res_atoms_before_addition))

                # each atom
                else:
                    # parse atom
                    res_num = int(line[0:5].strip())
                    res_name = line[5:10].strip()

                    atom_name = line[10:15].strip()
                    atom_num = int(line[15:20].strip())

                    position = [float(k) for k in line[20:44].strip().split()]

                    if len(line) >= 68:
                        velocity = [float(k) for k in line[44:64].strip().split()]
                    else:
                        velocity = [0.0000, 0.0000, 0.0000]

                    atom = GroAtom(res_num, res_name, atom_name, atom_num, position, velocity)

                    if atom.res_num() != res_num_before_addition:
                        if res_atoms_before_addition:
                            self.__residues.append(GroRes(res_atoms_before_addition))
                            res_atoms_before_addition = []
                            res_num_before_addition = atom.res_num()

                    res_atoms_before_addition.append(atom)

    def __set_residues(self, new_residues):
        self.__residues = new_residues

    def __set_num_of_atoms(self):
        self.__num_of_atoms = len(self.atoms())

    def path(self):
        return self.__path

    def title(self):
        return self.__title

    def num_of_atoms(self):
        self.__set_num_of_atoms()
        return self.__num_of_atoms

    def box_vectors(self):
        return self.__box_vectors

    def residues(self):
        return self.__residues

    def atoms(self):
        atoms = []
        for residue in self.__residues:
            atoms.extend(residue.atoms())
        return atoms

    def generate_gro(self, new_gro_path):
        with open(new_gro_path, 'w') as new:
            new.write(self.__title + '\n')
            new.write(str(self.__num_of_atoms) + '\n')
            for atom in self.atoms():
                atom_str = atom.get_str_gro_format()
                new.write(atom_str + '\n')
            box_vectors_str = ['{:>10.5f}'.format(v) for v in self.__box_vectors]
            new.write(''.join(box_vectors_str) + '\n')

    def residue_alignment(self):
        residues_dict = {}
        for residue in self.__residues:
            name = residue.name()
            if name not in residues_dict.keys():
                residues_dict[name] = [residue]
            else:
                residues_dict[name].append(residue)

        new_residues = []
        res_num = 1
        atom_num = 1
        for residue_name in residues_dict.keys():
            residues = residues_dict[residue_name]

            for residue in residues:
                residue.change_res_nums(res_num)
                res_num += 1

                residue.change_atom_nums(atom_num)
                atom_num += residue.num_of_atoms()

                new_residues.append(residue)
        self.__set_residues(new_residues)

    def delete_residues_from_name(self, res_name):
        new_residues = [residue for residue in self.__residues if residue.name() != res_name]
        self.__set_residues(new_residues)
        self.__set_num_of_atoms()

    def add_residues(self, res_obj_list):
        new_residues = self.__residues + res_obj_list
        self.__set_residues(new_residues)
        self.__set_num_of_atoms()

    def res_nums(self):
        nums = []
        for res in self.__residues:
            nums.append(res.num())
        return nums

    def change_res_name(self, name, nums):
        res_num_list = self.res_nums()
        for num in nums:
            i = res_num_list.index(num)
            self.__residues[i].change_res_names(name)
