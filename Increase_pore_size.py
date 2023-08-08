# this script can increase the pore size of quartz by modify the lammps data
# writen by eastsheng, 2023/7/22
#!/usr/bin/python
import numpy as np
import os
import pdb2xyz
def read_index(datafile):
	with open(datafile,"r") as f:
		for index, line in enumerate(f,1):
			if "atoms" in line:
				print(line)
				atom_number = int(line.split()[0])
			if "bonds" in line:
				print(line)	
				bonds_number = int(line.split()[0])
			if "Bonds" in line:
				print(line)	
				Bonds_index = index+1
			if "angles" in line:
				print(line)	
				angles_number = int(line.split()[0])
			if "Angles" in line:
				print(line)	
				Angles_index = index+1
			if "Atoms" in line:
				data_full_index = index+1
	return atom_number,data_full_index,bonds_number, Bonds_index, angles_number, Angles_index

def header_info(datafile,data_full_index,increment=10):
	with open(datafile,"r") as f, open("header_info.data","w") as w:
		for index, line in enumerate(f,1):
			if index<data_full_index-2:
				if "zlo zhi" in line:
					zline = line.strip().split()
					zline[0] = float(zline[0])
					zline[1] = float(zline[1])+increment
					w.write("\t "+str(zline[0]-zline[0])+"\t"+str(zline[1]-zline[0])+" zlo zhi\n")
				else:
					w.write(line)

	return


def modify_data_full(datafile,new_line,data_full_index,atom_number,increment=10):
	data_full = np.loadtxt(datafile,skiprows=data_full_index,max_rows=atom_number)
	m,n = data_full.shape
	# print(m,n)
	# count = 0
	for i in range(m):
		z = new_line[i][3]
		data_full[i,6] = z
		if data_full[i,6] > 30:
			# count += 1
			data_full[i,6] += increment # increment/angstrom
	# print(count)
	np.savetxt("data_full.data",data_full,fmt="%d %d %d %f %f %f %f %d %d %d")	
	return data_full

def modify_Bonds(datafile,Bonds_index,bonds_number):
	Bonds = np.loadtxt(datafile,skiprows=Bonds_index,max_rows=bonds_number)
	np.savetxt("data_Bonds.data",Bonds,fmt="%d %d %d %d")	
	return

def modify_Angles(datafile,Angles_index,angles_number):
	Angles = np.loadtxt(datafile,skiprows=Angles_index,max_rows=angles_number)
	np.savetxt("data_Angles.data",Angles,fmt="%d %d %d %d %d")			
	return


def rewrite_data(new_data):
	element_data = ["header_info.data","data_full.data","data_Bonds.data","data_Angles.data"]
	label = ["","Atoms  # full","Bonds","Angles"]
	with open(new_data,"w") as f:
		for i in range(len(element_data)):
			if i == 0:
				pass
			else:
				f.write(label[i])
				f.write("\n\n")
			for line in open(element_data[i]):
				f.writelines(line)
			f.write("\n")	
	for i in range(len(element_data)):
		os.remove(element_data[i])
	return

if __name__ == '__main__':
	incrementnm = 5 # nm
	incrementang = incrementnm*10 # nm to angstrom
	data = "quartz_pore_clayff_5nm.data"
	new_data = "quartz_pore_clayff_5+"+str(incrementnm)+"nm.data"

	atom_number, data_full_index, \
	bonds_number, Bonds_index, \
	angles_number, Angles_index,  = read_index(data)
	new_line = pdb2xyz.pdb2xyz("quartz_pore.pdb","quartz_pore.xyz")

	header_info(data,data_full_index,incrementang)
	modify_data_full(data,new_line,data_full_index,atom_number,incrementang) 
	modify_Bonds(data,Bonds_index,bonds_number)
	modify_Angles(data,Angles_index,angles_number) 
	
	rewrite_data(new_data)
	