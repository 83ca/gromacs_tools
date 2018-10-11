from gro import Gro


path = 'molecules.gro'
gro_obj = Gro(path)
change_res_id = list(range(1, 50, 6))
gro_obj.change_res_name('MOL2', change_res_id)
gro_obj.delete_residues_from_name('MOL1')
gro_obj.residue_alignment()
gro_obj.generate_gro('new.gro')



