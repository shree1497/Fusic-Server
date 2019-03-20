from os import walk

def create_dict(folder):
	f, dict_here = [], []
	for (dirpath, dirnames, filenames) in walk(folder):
		f.extend(filenames)
		break
	for i in range(len(f)):
		dictl='music/{}/{}'.format(folder,f[i])
		dict_here.append(dictl)

	with open("{}.txt".format(folder),"w") as f:
		for i in range(0,len(dict_here)):
			f.writelines("{}|music/songbg.jpg\n".format(dict_here[i]))
	return dict_here


print(create_dict('disgust'))