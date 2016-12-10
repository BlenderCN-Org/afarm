#!/usr/bin/python3

import time

def benchFunc(f, comment='BENCH:', useOut=False):
	start = time.time()
	out = f()
	elapsed = time.time() - start
	
	print(comment, "Completed in {} seconds.".format(elapsed))
	if useOut: print("OUTPUT:", out)
	
	return out
