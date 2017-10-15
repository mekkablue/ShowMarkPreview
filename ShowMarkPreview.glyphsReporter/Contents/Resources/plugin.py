# encoding: utf-8

###########################################################################################################
#
#
#	Reporter Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Reporter
#
#
###########################################################################################################


from GlyphsApp.plugins import *
import math
	
class ShowMarkPreview(ReporterPlugin):
	
	def transform(self, shiftX=0.0, shiftY=0.0, rotate=0.0, skew=0.0, scale=1.0):
		"""
		Returns an NSAffineTransform object for transforming layers.
		Apply an NSAffineTransform t object like this:
			Layer.transform_checkForSelection_doComponents_(t,False,True)
		Access its transformation matrix like this:
			tMatrix = t.transformStruct() # returns the 6-float tuple
		Apply the matrix tuple like this:
			Layer.applyTransform(tMatrix)
			Component.applyTransform(tMatrix)
			Path.applyTransform(tMatrix)
		Chain multiple NSAffineTransform objects t1, t2 like this:
			t1.appendTransform_(t2)
		"""
		myTransform = NSAffineTransform.transform()
		if rotate:
			myTransform.rotateByDegrees_(rotate)
		if scale != 1.0:
			myTransform.scaleBy_(scale)
		if not (shiftX == 0.0 and shiftY == 0.0):
			myTransform.translateXBy_yBy_(shiftX,shiftY)
		if skew:
			skewStruct = NSAffineTransformStruct()
			skewStruct.m11 = 1.0
			skewStruct.m22 = 1.0
			skewStruct.m21 = math.tan(math.radians(skew))
			skewTransform = NSAffineTransform.transform()
			skewTransform.setTransformStruct_(skewStruct)
			myTransform.appendTransform_(skewTransform)
		return myTransform
	
	
	def settings(self):
		self.menuName = Glyphs.localize({
			'en': u'Mark Preview',
			'de': u'Akzent-Vorschau'
		})
	
	def drawMarksOnLayer(self, layer):
		# draw only in letters:
		if layer.glyph().category == "Letter":
			anchorDict = {}
			for thisAnchor in layer.anchors:
				anchorDict[thisAnchor.name] = thisAnchor.position
			
			# continue if there are any anchors in the layer:
			if anchorDict:
				font = layer.font()
				tab = font.currentTab
				
				# continue if there is an Edit tab open:
				if tab:
					marks = []
					for thisLayer in tab.layers:
						if thisLayer.glyph().category == "Mark":
							marks.append( thisLayer )
							
					# continue if there are any marks in the Edit tab:
					if marks:
						for thisMark in marks:
							attachingAnchors = [a for a in thisMark.anchors if a.name.startswith("_")]
							if attachingAnchors:
								attachingAnchor = attachingAnchors[0]
								stackingAnchorName = attachingAnchor.name[1:]
								stackingAnchor = thisMark.anchors[stackingAnchorName]
								letterAnchor = anchorDict[stackingAnchorName]

								if letterAnchor:
									# shift and draw bezier path:
									shiftX = letterAnchor.x - attachingAnchor.x
									shiftY = letterAnchor.y - attachingAnchor.y
									displayShift = self.transform(shiftX=shiftX, shiftY=shiftY)
									displayMark = thisMark.completeBezierPath.copy()
									displayMark.transformUsingAffineTransform_(displayShift)
									displayMark.fill()
									
									# shift and store next anchor position (if exists)
									if stackingAnchor:
										nextAnchorX = stackingAnchor.x + shiftX
										nextAnchorY = stackingAnchor.y + shiftY
										anchorDict[stackingAnchorName] = NSPoint( nextAnchorX, nextAnchorY )
	
	def foreground(self, layer):
		color = NSColor.colorWithRed_green_blue_alpha_(0.3, 0.0, 0.6, 0.4)
		color.set()
		self.drawMarksOnLayer(layer)

	def inactiveLayers(self, layer):
		self.shouldDrawAccentCloudForLayer_(layer)
		color = NSColor.colorWithRed_green_blue_alpha_(0.15, 0.05, 0.3, 0.5)
		color.set()
		self.drawMarksOnLayer(layer)
	
	def needsExtraMainOutlineDrawingForInactiveLayer_(self, layer):
		return True
			
	def shouldDrawAccentCloudForLayer_(self, layer):
		return False
	