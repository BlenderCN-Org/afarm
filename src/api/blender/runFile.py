import bpy

def readSettings(path) : 
	'''
	Read a settings object from the path.
	:param str path: The string path to the pickled settings file. Usually .tmp/settings.
	:return: A settings object with all the data needed to execute the render.
	'''
	with open(path, 'rb') as data: return pickle.load(data)

def blendSet(settings) : #settings contains render engine specific data in its 'renderengine' index.
	"""
	Sets the settings in the .blend file of the data_path.
	:param dict task: The task dictionary. Focused on what the task is.
	:param dict settings: The settings dictionary. Describes how the blend should look before rendering.
	:return: A boolean indicating success.
	"""
	
	#Base access paths.
	scene = bpy.data.scene[bpy.context.scene] #Assume current scene for now. Scene management is a larger task.
	render = scene.render
	image = render.image_settings
	
	#Resolution
	render.resolution_x = settings['x_res']
	render.resolution_y = settings['y_res']
	render.resolution_percentage = settings['percent_res']
	
	#Frame
	scene.frame_start = settings['start_frame']
	scene.frame_end = settings['end_frame']
	scene.frame_step = settings['step_frame']
	
	if settings['isSingle'] :
		scene.frame_set(settings['single_frame']) #Set the frame to render if only rendering a single.
		
	#Engine Specific
	if render.engine == 'CYCLES' :
		cycles = scene.cycles
		
		cycles.progressive = settings['cycles']['path_trace'] #Path tracing or branched path tracing.
		cycles.samples = settings['cycles']['samples']
		cycles.max_bounces = settings['cycles']['bounces_max']
		cycles.min_bounces = settings['cycles']['bounces_min']
		cycles.glossy_bounces = settings['cycles']['bounces_glossy']
		cycles.transmission_bounces = settings['cycles']['bounces_transmission']
		cycles.volume_bounces = settings['cycles']['bounces_volume']
		cycles.transparent_max_bounces = settings['cycles']['bounces_trans-max']
		cycles.transparent_min_bounces = settings['cycles']['bounces_trans-min']
		cycles.use_progressive_refine = False #We'll never be using progressive refine, ever.
		
		if settings['isGPU'] :
			#Use slave settings to determine which GPU combination to activate now. Pull these initially from Blender Prefs on slave setup.
			render.tile_x = 256
			render.tile_y = 256
		else :
			#Make sure to activate CPU as compute device.
			render.tile_x = 16
			render.tile_y = 16
	
	#Image Settings - Make sure there are mechanisms to use format based on disk space; the only thing that matters is the final output.
	image.file_format = settings['file_format'] #Client must verify this, and entire settings dict, against whether it works or not.
	image.color_mode = settings['color_mode']
	
	#Format specific settings. Don't wanna do this now .-.
	
	#Dynamically Set
	render.filepath = settings['dynamic']['outputPath'] #This part of the settings dictionary is set on the slave, dynamically.
	render.use_overwrite = settings['dynamic']['overwrite']
	
def render(animation=False, scene="") :
	'''
	Execute the render. Must execute after settings are set.
	:param bool animation
	'''
	bpy.ops.render.render(animation=animation, scene=scene, write_still=True)

if __name__ == '__main__' :
	settings = readSettings(os.path.join('.tmp', 'settings')) #Depends on existance of "settings" file in .tmp.
	
	blendSet(settings)
	render(animation=settings['isMultiFrame')
