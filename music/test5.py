from os import walk
var='surprise'
f = []
for (dirpath, dirnames, filenames) in walk(var):
	f.extend(filenames)
	
print(len(f))