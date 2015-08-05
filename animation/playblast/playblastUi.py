import os
import pipe.mayaFile.mayaFile as mfl
import pipe.file.file as fl
import general.ui.pySideHelper as uiH
import render.deadline.deadline as dl
reload( dl )
reload( uiH )
uiH.set_qt_bindings()
from Qt import QtGui,QtCore

PYFILEDIR = os.path.dirname(os.path.abspath(__file__))

uifile = PYFILEDIR + '/playblast.ui'
fom, base = uiH.loadUiType( uifile )

INMAYA = False
try:
	import animation.playblast.playblast as plb
	reload(plb)
	import maya.cmds as mc
	INMAYA = True
	import render.renderOcc.renderOcc as renOcc
	reload( renOcc )
except:
	pass
INHOU = False
try:
	import general.houdini.utils as hut
	reload( hut )
	import pipe.houdiniFile.houdiniFile as hfl
	reload( hfl )
	INHOU = True
except:
	pass

class PlayblastUi(base,fom):
	"""manager ui class"""
	def __init__(self, parent = None ):
		if INMAYA:
			if uiH.USEPYQT:
				super(base, self).__init__(uiH.getMayaWindow())
			else:
				super(PlayblastUi, self).__init__(uiH.getMayaWindow())
		else:
			if uiH.USEPYQT:
				super(base, self).__init__(parent)
			else:
				super(PlayblastUi, self).__init__(parent)
		self.setupUi(self)
		self._makeConnections()
		self.setObjectName( 'PlayblastUi' )
		dead = dl.Deadline()
		self.group_cmb.addItems( dead.groups )

	def _makeConnections(self):
		"""docstring for _makeConnections"""
		self.connect( self.playblast_btn , QtCore.SIGNAL("clicked()") , self.playblast )
		self.connect( self.renderOcc_btn , QtCore.SIGNAL("clicked()") , self.renderOcc )
		self.connect( self.publish_btn , QtCore.SIGNAL("clicked()") , self.publish )

	def renderOcc(self):
		"""render occ for current camera"""
		renOcc.renderOcc( self.motionBlur_chb.isChecked(), str( self.group_cmb.currentText() ) )

	def playblast(self):
		"""docstring for playblast"""
		if INMAYA:
			plb.playblastCurrentFile()
		elif INHOU:
			hut.playblastCurrentFile()

	def publish(self):
		"""docstring for publish"""
		if INMAYA:
			fil = mfl.currentFile()
			if not fil:
				print 'Please Save File To create Playblast'
				return
			movFil = fl.File( fil.versionPath + fil.name + '_v' + str( fil.version ).zfill( 3 ) + '.mov' )
		elif INHOU:
			fil = hfl.currentFile()
			if not fil:
				print 'Please Save File To create Playblast'
				return
			movFil = fl.File( fil.versionPath + fil.name + '_v' + str( fil.version ).zfill( 3 ) + '.mov' )
		if movFil.exists:
			movFil.copy( fil.dirPath + fil.name + '.mov' )

def main():
	try:
		if mc.window( 'PlayblastUi', q = 1, ex = 1 ):
			mc.deleteUI( 'PlayblastUi' )
	except:
		pass
	global PyForm
	PyForm=PlayblastUi(parent=QtGui.QApplication.activeWindow())
	PyForm.show()
