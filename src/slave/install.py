"""
This is the hub of slave activities. It contains software generic functions that are used by every part of the slave.
"""

import os, sys
import shutil
import json
import multiprocessing as mp
import importlib

CONFIG = {	'dirName'	: 'afarm-slave', #Read from a config file? In any case, standardized naming is never bad.
			'binDir'	: 'binaries',
			'dataDir'	: 'data',
			'extDir'	: 'extension',
			'scriptDir'	: 'scripts',
			'scrInts'	: ('net', 'api', 'admin') #0, 1, 2 of the Script Internals.
}

def setup(startDir = os.path.expanduser("~")) : #Home directory.
	rootDir = os.path.join(startDir, CONFIG['dirName'])
	if os.path.exists(rootDir): shutil.rmtree(rootDir) #Susceptible to symlink attack on some (older) systems.
	#For testing, the rootDir will be replaced each time setup() runs. Production use might offer additional functionality.
	
	os.mkdir(rootDir)
	
	#Setup the build dirs.
	os.mkdir(os.path.join(rootDir, CONFIG['binDir']))
	os.mkdir(os.path.join(rootDir, CONFIG['dataDir']))
	os.mkdir(os.path.join(rootDir, CONFIG['extDir']))
	
	scriptDir = os.path.join(rootDir, CONFIG['scriptDir'])
	os.mkdir(scriptDir)
	os.mkdir(os.path.join(scriptDir, CONFIG['scrInts'][0]))
	os.mkdir(os.path.join(scriptDir, CONFIG['scrInts'][1]))
	os.mkdir(os.path.join(scriptDir, CONFIG['scrInts'][2]))
	

def pathBinary(soft, version, name, rootDir = os.path.join(os.path.expanduser("~"), CONFIG['dirName'])) :
	"""
	Gets the path to a binary file.
	"""
	
	binDir = os.path.join(rootDir, CONFIG['binDir'])
	softDir = os.path.join(binDir, soft)
	verDir = os.path.join(softDir, version) #Because this as a one liner physically hurt to look at.
	
	return os.path.join(verDir, name)
	
	#Use the binary from the folder, of the version defined in the task. See specification
	#return './binary/2.76/blender'
	
def pathData(jobID, rootDir = os.path.join(os.path.expanduser("~"), CONFIG['dirName'])) :
	"""
	Gets the path to a given job's data, using its id.
	"""
	
	dataDir = os.path.join(rootDir, 'data')
	return os.path.join(dataDir, jobID) #The job's data is in a folder named by id.

def importApi(soft, rootDir = os.path.join(os.path.expanduser("~"), CONFIG['dirName'])) : #Essentially a software-based selective module import.
	scriptDir = os.path.join(rootDir, CONFIG['scriptDir'])
	apiDir = os.path.join(scriptDir, CONFIG['scrInts'][1])
	softDir = os.path.join(apiDir, soft)
		
	return importlib.machinery.SourceFileLoader('command', os.path.join(softDir, 'command.py').load_module()

def control(taskQ) : #We don't have great control over a queue's operation...
	"""
	Executes tasks in the taskQ. Strictly doesn't require its own process, but should have it - constantly checking.
	"""
	soft = importApi('blender')
	while True: #Not designed to end.
		task = taskQ.get()
		
		#These next parts are the "duck typing" part of the software api.
		soft.runTask(task)

class soft : #Simple static organization block. Modularize?
	def read(pathSoft, softLock = mp.Lock()) :
		"""
		Reads a software file.
		"""	
		with softLock : #Access sensitive.
			try:
				with open(pathSoft + "softBase.json", 'r') as dataFile :
					out = json.load(dataFile)
			except:
				out = False
		
		return out #Go learn better context management...
		
	def write(pathSoft, structSoft, softLock = mp.Lock()) :
		formerDir = os.getcwd()
		os.chdir(pathSoft) #Context manager where are you 
		
		with softLock : #Access sensitive.
			try:
				with open(pathSoft + "softBase.json", 'w') as dataFile :
					json.dump(structSoft, dataFile)
			except:
				print("Not a file!")
				
		os.chdir(formerDir)
			
	def info(software, pathAPI) :
		formerDir = os.getcwd()
		os.chdir(pathAPI + software)
		
		##Get binIDs and extensions from some kind of internal file in the api.
		
		os.chdir(formerDir)
		
		return {"binIDs" : binIDs, "extensionIDs" : extensions}
		
	def gen(pathAPI, soft = {}) :
		softwares = os.listdir(pathAPI)
		
		for software in softwares :
			soft[software] = info(software)
			
		return soft
		

