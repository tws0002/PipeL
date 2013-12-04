import os
import shutil
import time

#TODO -->
#	check os... methods
#

class File(object):
	versInFolds = True #the versions are collected in a folder
	paddingNum  = 3
	threshold = 1.0

	def __init__(self, path):
		"""init file node with full path"""
		self._path = path

	def __repr__(self):
		"""return the path"""
		return self._path

	def __str__(self):
		"""return path"""
		return self._path

	@property
	def path(self):
		"""return full path of the file"""
		return self._path

	@property
	def exists(self):
		"""return if the file exists"""
		return os.path.exists( self.path )

	@property
	def date(self):
		"""return the modification date of the file"""
		return time.ctime(os.path.getmtime( self.path ))

	@property
	def dateNumber(self):
		"""return the modified date number"""
		return os.path.getmtime( self.path )

	@property
	def size(self):
		"""return the size of the file in bytes"""
		if not self.exists:
			return 0
		return os.path.getsize( self.path )#TODO check this method

	@property
	def basename(self):
		"""return the basename --> filename.ext"""
		return os.path.basename( self.path )

	@property
	def name(self):
		"""return file name without extension"""
		return os.path.splitext( self.basename )[0]#TODO check this method

	@property
	def fullName(self):
		"""return file name with extension"""
		return os.path.basename( self.path )

	@property
	def extension(self):
		"""return file extension without dot"""
		return os.path.splitext( self.basename )[1]#TODO check this method

	@property
	def dirPath(self):
		"""return directory path of the file"""
		return os.path.dirname( self.path ) + '/'

	@property
	def versionPath(self):
		"""return directory where the versions are"""
		if File.versInFolds:
			return self.dirPath + '/Versions/'
		else:
			return self.dirPath
	
	@property
	def version(self):
		"""return the number of version that the file is"""
		verPath = self.versionPath
		if not os.path.exists( verPath ):
			return 1
		verFils = [ a for a in os.listdir( verPath ) 
				if ( self.name in a
					and a.endswith( self.extension )
					and os.path.isfile( verPath + a ) 
				) ]
		return len( verFils ) + 1

	def create(self, path): #TODO
		"""method to create file if dosen't exists"""
		if not self.exists: 
			print 'creating file in path', path
			return True
		else:
			print 'this file allready exists in', path
			return False
	
	def copy(self, newPath):
		"""copy file to new path,
		   newPath could be a directory path or a complete path and it will rename the file"""
		if not os.path.exists( os.path.dirname( newPath ) ):
			os.makedirs( os.path.dirname( newPath ) )
		if os.path.isdir( newPath ):
			shutil.copy2( self.path, newPath + self.fullName )
		else:
			shutil.copy2( self.path, newPath )
	
	def rename(self, newName):
		"""rename filename newName"""
		os.rename( self.path, self.dirPath + newName )
		
	def newVersion(self):
		"""create a new Version of the file"""
		print self.versionPath + self.name + '_v' + str( self.version ).zfill( File.paddingNum ) + self.extension
		self.copy( self.versionPath + self.name + '_v' + str( self.version ).zfill( File.paddingNum ) + self.extension ) #TODO make correct padding for numbers

	def delete(self):
		"""delete file"""
		os.delete( self.path )

	def move(self, newPath):
		"""move file to newPath, same as copy but instead it will delete the original file"""
		self.copy( newPath )
		self.delete()

	def isOlderThan(self, fileToCompare):
		"""compare to File objects to see if the current one is older than"""
		return os.path.getmtime( fileToCompare.path ) - os.path.getmtime( self.path ) > File.threshold

	def isBiggerThan(self, fileToCompare):
		"""compare File object size with another File object"""
		return self.size > fileToCompare.size

	@property
	def isZero(self):
		"""return if the file is a zero kbytes file"""
		return os.path.getsize( self.path ) == 0

	@property
	def data(self):
		"""return the data if the file"""
		with open( self.path ) as f:
			file_str = f.read()
		return file_str

	@property
	def lines(self):
		"""return all the file in lines"""
		with open( self.path ) as f:
			file_str = f.readlines()
		return file_str