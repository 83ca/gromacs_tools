import re


class AtomName(object):
    def __init__(self, name):
        # 原子名: {元素}{番号}
        self.__element, self.__number = re.findall(r'(\d+|\D)', name)

    def name(self):
        return self.element() + self.number_str()

    def element(self):
        return self.__element

    def number_str(self):
        return self.__number

    def number_int(self):
        return int(self.__number)

    def change_element(self, new_element):
        self.__element = new_element
        return self.__element

    def change_number(self, new_num):
        self.__number = new_num
        return self.__number


def pdb_name_format(name):
    return "{name:<4}".format(name=name)


def decimal_convert_to_hex(num):
    num_hex = hex(num)
    return num_hex[2:]


def convert_hex_atomname(atomname):
    atom = AtomName(atomname)
    hex_number = decimal_convert_to_hex(atom.number_int())
    print('{name} change number: {old} -> {new}'.format(name=atom.name(), old=atom.number_str(), new=hex_number))
    atom.change_number(hex_number)
    return atom.name()


def main():
    atoms = './atoms.txt'
    with open(atoms, 'r') as old_atoms:
        with open('atoms_new.txt', 'w') as new_atoms:
            for line in old_atoms:
                atom = line.strip()
                new_atoms.write(pdb_name_format(convert_hex_atomname(atom))+'\n')


if __name__ == '__main__':
    main()

