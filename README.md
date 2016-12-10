#What is it?

afarm is a package, currently in development, which makes it easy to allow multiple computers to participate in generalized distributed computing, with a focus on distributed 3D rendering with Blender 3D. Design goals are:
- Stability and Security: It is written in Python 3, and uses standard, open source tools like ssh, rsync, and ffmpeg. On the master and any Debian running slaves, Debian system management is used to restrict access to the system more than absolutely neccessary (It is still very possible to run between distributions, or even operating systems; see Portability).

- Ease of Use: The master merely listens for tasks on a port and serves data back on another; however you decide to submit and get data is up to you. Design goals for this include a CLI and a web interface.

- Algorithmic Viability: The algorithm, which will be based around a multidimentional sort, is designed to be able to take n number of properties, as the combination relates to each individual slave, into account when allocating tasks out. This includes, for example, taking electricity usage into account when sorting to optimize performance vs. cost.

- Portability: The design focuses on four individual modules: Core, Application, Client, and Slave. The last three can be interchanged at-will, and can even used at the same time ("Plug and Play") due to the standard way that Core communicates with each.

- Open Source and Extensible: All code is licensed under MIT Licence. Adding an Application or a Slave will be no harder than creating a few config files, according to the documentation.

- Feature-Rich: There are lots of features that should make their way into the final release. Here are a few:
  
  - Consistent Versioning: Because each slave has its own user, binaries can be transferred by the master to the entire farm for use in executing tasks. The Master is able to manage all versions of software and libraries; this is all defined in the Application definition.

  - Slave Setup: A simple package can be installed on the slave, which will setup everything correctly and allow the Master to automatically detect it. Alternatively, everything can be manually set up. Once connected, the Master runs all necessary tests, after which the Slave can begin working immediately.

  - Slave Definitions: Within the design goals are slave definitions (see Portability) for 
  
##Why Debian?
There are some very compelling reasons to write animal-farm primarily for Debian:
- Package Management: Debian can take care of all the dependencies and versioning, in a way that is guaranteed to work.
- System Structure and Policies: Debian is built very consistently, which not only makes it stable and secure, but which also makes it easy to work with. Also, policies exist for the usage of system services like Wake on LAN and user/group management.

##Related Work
Similar pieces of software exist, specifically for Blender:
- Loki Render (http://blenderartists.org/forum/showthread.php?353911-Loki-Render-0-7-0-released!). It is built in Java, and has many similar features to blenderfarm. It is optimized to use Amazon Web Services, and is currently in development.
- Yadra (https://sites.google.com/site/blendoli/yadra). Yet another Java utility. This one is based around a web interface, and for the moment has a very limited scope.
- NetRender (http://wiki.blender.org/index.php/Doc:2.6/Manual/Render/Performance/Netrender), which is an extension for Blender. Traditionally this is the way to create a render farm using Blender, however it is currently very out of date.
- Flamenco (previously known as brender). It will be the solution that the Blender Foundation uses to 


##Who is the Audience?
For now, the audience is primarily Blender users, which includes hobbyists, independent professionals, and small studios. That will work, however, in a way so that anyone who needs a general distributed computing solution can easily set one up.

##What's with the name?
Animal Farm (http://en.wikipedia.org/wiki/Animal_Farm) is a book by George Orwell, in which farm animals take over the farm, driving out the humans, and establish their (meaning the pig's) own rules. One of these rules is that "All animals are equal."

Of course, this quickly turns into "All animals are equal, but some are more equal than others." Kind of like the slaves in the package...

#Contribute!
- If you think afarm could be helpful to you, and you have knowledge of Python, then shoot me an email!
- If you test out a release (whenever that comes around) and find a bug, submit it!
