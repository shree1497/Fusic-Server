with open("data.txt") as f:
	dictionary = {}
	for line in f:
		dictionary[line.split(':')[0]]=int(line.split(':')[1].rstrip('\n'))
