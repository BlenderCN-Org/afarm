"""
Blender-specific tools to run tasks.
"""
import pickle
import multiprocessing as mp
import subprocess
import sys
import time

from fractions import Fraction

sys.path.append('/home/sofus/subhome/src/afarm/src/slave/unix/admin') #Slave operations.

import framework

sys.path.append('/home/sofus/subhome/src/afarm/src/lib') #AFarm Global Library.

import col

def runTask(task) :
	"""
	Assembles and runs a command in the current process from a path to a data structure file, as per the standard.
	:param str task: The task dictionary.
	:return: The Process object, used to monitor.
	"""
	isSet = writeSettings(task['settings']); #Pass in the task settings to the runFile, for dynamic load at rendertime.
	pathBlend = os.path.join(pathData(task['job_id']) #Task has all of its associated job data built into it.
	#pathBlend = 'bench.blend'
	
	if isSet : #task['binary_info'] must be a tuple of soft, version, name. task[<software>] has software specific info.
		args = [framework.pathBinary(*task['binary_info']), '-b', task['blender']['init_blend'], '-P', 'runFile.py'] #Runfile uses settings file.
		
		process = subprocess.Popen(args, stdout=subprocess.PIPE)
		
		for raw in iter(process.stdout.readline, b'') : #iter(callable, stopReturnValue). Kinda weird, so just clarifying ;).
			line = raw.decode('utf-8').rstrip()
			
			col.printDbg('run', line)
			
			if line[:4] == "Fra:": col.printDbg('info', parseRender(line))

def writeSettings(settings) :
	try:
		with open(os.path.join('.tmp', 'settings'), 'wb') as data :
			pickle.dump(settings, data)
		
		return True
	except:
		return False

class Matcher:
	def matchRange(text, start, end, fromI=0) :
		"""
		Returns a string equal to the text between start and end, stripped of all but . and : .
		:param fromI: The spot to start the search from.
		:return str: A string between start and end.
		"""
		index = text.find(start, fromI)
		partFloat = lambda schar: schar.isdecimal() or schar == '.' or schar == ':' or schar == '/'
		
		return ''.join(c for c in text[index + len(start) : text.find(end, index + len(start))] if partFloat(c))
	
	def matchTime(text, start, end, fromI=0) :
		"""
		Parses the text between start and end in text into a dictionary containing 'sec', 'hr', and 'min'.
		"""
		strTime = Matcher.matchRange(text, start, end, fromI)
		
		entries = strTime.count(':') + 1 #Determine how many places based on # of :'s.
		options = ['hr', 'min', 'sec']
		keys = [options[::-1][i] for i in range(entries)][::-1] #Flip options to index from reverse, flipping the list back again.
		vals = ['' for x in range(entries)]
		#End result is a keys list sorted by hours first, filled with seconds first, with vals being filled hours first.
		
		i=0 #Which offset to use. Fill up hr before min before sec, etc. .
		for c in strTime :
			if c == ':' :
				i += 1
			elif c.isdecimal(): vals[i] += c #Assemble vals little by little.
		
		newVals = map(lambda c: c if c else 0, vals) #map expression making c 0 if it's currently ''. Relies on '' == False.
		return dict(zip(keys, map(int, newVals))) #Combine keys and filtered out vals in a dictionary.
		
	def matchEnd(text, start) :
		return text[text.find(start) + len(start):]
		
	def matchFrac(text, start, end='', fromI=0) :
		strFrac = Matcher.matchRange(text, start, end, fromI) if end else Matcher.matchEnd(text, start)
		
		return int(100 * float(Fraction(strFrac)))
		
def parseRender(line) :
	mch = Matcher #static rename.
	
	#Parameters to start with.
	frame = int(mch.matchRange(line, 'Fra:', ' '))
	elapsed = mch.matchTime(line, 'Time:', '.')
	
	#Initial Values for all advanced parameters.
	remaining = -1
	memLeft = float(mch.matchRange(line, 'Mem:', 'M'))
	memPeak = float(mch.matchRange(line, 'Peak ', 'M'))
	
	tileTotal = -1
	tileDone = -1
	
	#Stages: PRE, REN, POST. Status: SYNC, BUILD, PATH_TRACE, COMP. Progress: In %. Object: String name of object being handled.
	status = {'stage':'', 'status':'', 'progress':0, 'object':''}
	
	if 'Remaining:' in line: #This indicates that the proper rendering has begun. More advanced data is now recorded.
		remaining = mch.matchTime(line, 'Remaining:', '.')
		memLeft = float(mch.matchRange(line, 'Mem:', 'M', fromI=line.find('Remaining:'))) #Read more accurate memory stats.
		memPeak = float(mch.matchRange(line, 'Peak ', 'M', fromI=line.find('Remaining:')))
		
	if 'Synchronizing object' in line:
		tmpStr = 'Synchronizing object | '
		
		status['stage'] = 'PRE'
		status['object'] = mch.matchEnd(line, tmpStr)
		status['status'] = 'SYNC'
		status['progress'] = -1
	elif 'Updating Mesh BVH ' in line:
		tmpStr = 'Updating Mesh BVH '
		
		status['stage'] = 'PRE'
		status['object'] = mch.matchRange(line, tmpStr, ' ')
		status['status'] = 'BUILD'
		status['progress'] = mch.matchFrac(line, status['object'], end=' ')
	elif 'Path Tracing Tile ' in line:
		tmpStr = 'Path Tracing Tile '
		
		status['stage'] = 'REN'
		status['object'] = ''
		status['status'] = 'PATH_TRACE'
		status['progress'] = mch.matchFrac(line, status['object'])
		
	
	return status

if __name__ == '__main__' :
	runTask()
