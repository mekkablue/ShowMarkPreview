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


from GlyphsApp import GSControlLayer, subtractPoints
from GlyphsApp.plugins import *
import math

class ShowMarkPreview(ReporterPlugin):
	categoriesOnWhichToDrawAccents = ("Letter","Number","Punctuation")

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
			'de': u'Akzent-Vorschau',
			'es': u'previsualización de acentos',
		})

	def drawMarksOnLayer(self, layer, lineOfLayers, offset=NSPoint(0,0)):
		# draw only in letters:
		if layer.glyph().category in self.categoriesOnWhichToDrawAccents:
			anchorDict = {}
			for thisAnchor in layer.anchorsTraversingComponents():
				anchorDict[thisAnchor.name] = thisAnchor.position

			# continue if there are any anchors in the layer:
			if anchorDict:

				# continue if there is an Edit tab open:
				if lineOfLayers:
					marks = []
					for thisLayer in lineOfLayers:
						if thisLayer.glyph() and thisLayer.glyph().category == "Mark":
							marks.append( thisLayer )

					# continue if there are any marks in the Edit tab:
					if marks:
						for thisMark in marks:
							attachingAnchorNames = [a for a in thisMark.anchorNamesTraversingComponents() if a.startswith("_")]
							stackingAnchorNames = [a for a in thisMark.anchorNamesTraversingComponents() if not a.startswith("_")]
							if attachingAnchorNames:
								attachingAnchor = thisMark.anchorForName_traverseComponents_(attachingAnchorNames[0],True)
								relatedStackingAnchorName = attachingAnchor.name[1:]
								try:
									letterAnchor = anchorDict[relatedStackingAnchorName]
								except KeyError:
									letterAnchor = None

								if letterAnchor:
									# shift and draw bezier path:
									scale = self.getScale()
									shiftX = letterAnchor.x - attachingAnchor.x + offset.x / scale
									shiftY = letterAnchor.y - attachingAnchor.y + offset.y / scale
									displayShift = self.transform(shiftX=shiftX, shiftY=shiftY)
									displayMark = thisMark.completeBezierPath.copy()
									displayMark.transformUsingAffineTransform_(displayShift)
									displayMark.fill()

									# shift and store next anchor position (if exists)
									for stackingAnchorName in stackingAnchorNames:
										stackingAnchor = thisMark.anchorForName_traverseComponents_(stackingAnchorName,True)
										if stackingAnchor:
											nextAnchorX = stackingAnchor.x + shiftX - offset.x / scale
											nextAnchorY = stackingAnchor.y + shiftY - offset.y / scale
											anchorDict[stackingAnchorName] = NSPoint( nextAnchorX, nextAnchorY )

	def foreground(self, layer):

		# define drawing colors
		activeColor = NSColor.colorWithRed_green_blue_alpha_(0.3, 0.0, 0.6, 0.4)
		inactiveColor = NSColor.colorWithRed_green_blue_alpha_(0.15, 0.05, 0.3, 0.5)

		currentController = self.controller.view().window().windowController()
		if currentController:
			if currentController.SpaceKey():
				activeColor = NSColor.colorWithRed_green_blue_alpha_(0.0, 0.0, 0.0, 1.0)
				inactiveColor = NSColor.colorWithRed_green_blue_alpha_(0.0, 0.0, 0.0, 1.0)


		# go through tab content
		glyph = layer.glyph()
		font = layer.font()
		if font: # sometimes font is empty, don't know why
			tabView = font.currentTab.graphicView()
			layerCount = tabView.cachedLayerCount()
			lineOfLayers = []
			lineOfOffsets = []

			# collect layers in the same line (to only draw the marks we need)
			for i in range(layerCount):
				thisLayer = tabView.cachedGlyphAtIndex_(i)

				# collect layers and their offsets except newlines
				if type(thisLayer) != GSControlLayer:
					lineOfLayers.append( thisLayer )
					lineOfOffsets.append( tabView.cachedPositionAtIndex_(i) )

				# if we reach end of line or end of text, draw with collected layers:
				if type(thisLayer) == GSControlLayer or i==layerCount-1:

					# step through all layers of the line:
					for j, thisLayerInLine in enumerate(lineOfLayers):

						# draw accents on them if they are Letter/Number/Punctuation
						if thisLayerInLine.parent.category in self.categoriesOnWhichToDrawAccents:
							activePosition = tabView.activePosition()
							lastLayerInLinePosition = tabView.cachedPositionAtIndex_(i)
							thisLayerInLinePosition = lineOfOffsets[j]
							offset = subtractPoints(thisLayerInLinePosition, activePosition)
							if offset == NSPoint(0,0):
								activeColor.set()
								self.drawMarksOnLayer(thisLayerInLine, lineOfLayers)
							else:
								inactiveColor.set()
								self.drawMarksOnLayer(thisLayerInLine, lineOfLayers, offset)

					# reset layer collection
					lineOfLayers = []
					lineOfOffsets = []

	def needsExtraMainOutlineDrawingForInactiveLayer_(self, layer):
		return True

	def shouldDrawAccentCloudForLayer_(self, layer):
		return False
