import bench

def myZip(*seqs) :
	return (tuple(seq[i] for seq in seqs) for i in range(len(seqs)))
	
def myOtherZip(*seqs) :
	for i in range(len(seqs)) :
		out = []
		for seq in seqs :
			out.append(seq[i])
			
		yield tuple(out)
		
def myMap(func, *seqs) :
	for args in zip(*seqs) :
		yield func(*args)

if __name__ == "__main__" :
	seq = [(1, 2, 3), (4, 5, 6), (7, 8, 9), (1, 5, 2)]
	
	#bench.benchFunc(lambda: list(myZip(*seq)), comment="myZip: ", useOut=True)
	#bench.benchFunc(lambda: list(myOtherZip(*seq)), comment="myOtherZip: ", useOut=True)
	bench.benchFunc(lambda: list(zip(*seq)), comment="zip: ", useOut=True)
	bench.benchFunc(lambda: list(myMap(lambda x, y: x + y, [-2, -1, 0, 1, 2], [1, 2, -6, 2])), comment="zip: ", useOut=True)
