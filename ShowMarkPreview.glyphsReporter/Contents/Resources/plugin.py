# encoding: utf-8
from __future__ import division, print_function, unicode_literals

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

import objc
from GlyphsApp import *
from GlyphsApp.plugins import *
from math import radians, tan

class ShowMarkPreview(ReporterPlugin):
	categoriesOnWhichToDrawAccents = ("Letter","Number","Punctuation")
	specialGlyphsOnWhichToDrawAccents = ("dottedCircle")
	
	@objc.python_method
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
			skewStruct.m21 = tan(radians(skew))
			skewTransform = NSAffineTransform.transform()
			skewTransform.setTransformStruct_(skewStruct)
			myTransform.appendTransform_(skewTransform)
		return myTransform

	@objc.python_method
	def settings(self):
		self.menuName = Glyphs.localize({
			'en': u'Mark Preview',
			'de': u'Akzent-Vorschau',
			'es': u'previsualización de diacríticos',
			'fr': u'aperçu des accents',
		})
		Glyphs.registerDefault("com.mekkablue.ShowMarkPreview.extension", "")
		self.extension = Glyphs.defaults["com.mekkablue.ShowMarkPreview.extension"]

	@objc.python_method
	def drawMarksOnLayer(self, layer, lineOfLayers, offset=NSPoint(0,0)):
		# draw only in letters:
		if not lineOfLayers:
			return
		glyph = layer.glyph()
		if glyph.category not in self.categoriesOnWhichToDrawAccents and glyph.name not in self.specialGlyphsOnWhichToDrawAccents:
			return
		anchorDict = {}
		anchors = layer.anchorsTraversingComponents()
		if not anchors:
			return 
		for thisAnchor in anchors:
			anchorDict[thisAnchor.name] = thisAnchor.position

		# continue if there are any anchors in the layer:
		if not anchorDict:
			return

		marks = []
		for thisLayer in lineOfLayers:
			if thisLayer.glyph() and thisLayer.glyph().category == "Mark":
				marks.append(thisLayer)

		# continue if there are any marks in the Edit tab:
		if not marks:
			return
		
		for thisMark in marks:
			attachingAnchorNames = sorted([a for a in thisMark.anchorNamesTraversingComponents() if a.startswith("_")], key = lambda anchorName: len(anchorName))
			stackingAnchorNames = sorted([a for a in thisMark.anchorNamesTraversingComponents() if not a.startswith("_")], key = lambda anchorName: len(anchorName))
			
			# sort names with extension to the front:
			if self.extension:
				attachingAnchorNames = sorted(attachingAnchorNames, key = lambda anchorName: -(self.extension in anchorName))
				stackingAnchorNames = sorted(stackingAnchorNames, key = lambda anchorName: -(self.extension in anchorName))
			
			if attachingAnchorNames:
				for attachingAnchorName in attachingAnchorNames:
					attachingAnchor = thisMark.anchorForName_traverseComponents_(attachingAnchorName,True)
					relatedStackingAnchorName = attachingAnchor.name[1:]
					try:
						letterAnchor = anchorDict[relatedStackingAnchorName]
					except KeyError:
						letterAnchor = None
					if letterAnchor:
						break

				if not letterAnchor:
					continue 
					
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
						anchorDict[stackingAnchorName] = NSPoint(nextAnchorX, nextAnchorY)

	@objc.python_method
	def defineColors(self, RGBA, parameterValue):
		if parameterValue:
			# read out custom parameter:
			parameterValues = [item.strip() for item in parameterValue.strip().split(",")]
		
			# add the values to the RGBA list of colors:
			numValues = min(4,len(parameterValues))
			for i in range(numValues):
				try:
					value = float(parameterValues[i])
					RGBA[i] = min(value,1.0)
				except:
					# fail gracefully and continue if invalid
					pass
		return RGBA
	
	@objc.python_method
	def foreground(self, layer):
		self.extension = Glyphs.defaults["com.mekkablue.ShowMarkPreview.extension"]
		
		# go through tab content
		glyph = layer.glyph()
		font = layer.font()
		if not font: # sometimes font is empty, don't know why
			return

		editView = self.controller.graphicView()
		try:
			darkMode = editView.drawDark()
		except:
			# Glyphs 2
			darkMode = NSUserDefaults.standardUserDefaults().stringForKey_('AppleInterfaceStyle') == "Dark" and Glyphs.defaults["GSEditViewDarkMode"]
			
		if darkMode:
			# default dark mode colors:
			colorDefaultsActive = [0.8, 0.0, 1.0, 0.5]
			colorDefaultsInactive = [0.45, 0.15, 0.6, 0.6]
		else:
			# default light mode colors:
			colorDefaultsActive = [0.3, 0.0, 0.6, 0.4]
			colorDefaultsInactive = [0.15, 0.05, 0.3, 0.5]

		# define drawing colors (user set or defaults)
		RGBA = self.defineColors(
			colorDefaultsActive,                       # default active color
			font.customParameters["MarkPreviewColor"], # user-defined color
		)
		RGBAinactive = self.defineColors(
			colorDefaultsInactive,                             # default inactive color
			font.customParameters["MarkPreviewColorInactive"], # user-defined color
		)

		windowController = self.controller.view().window().windowController()
		if windowController and windowController.SpaceKey():
			activeColor = NSColor.textColor()
			inactiveColor = NSColor.textColor()
		else:
			activeColor = NSColor.colorWithRed_green_blue_alpha_(*RGBA) # * splits into separate items of list
			inactiveColor = NSColor.colorWithRed_green_blue_alpha_(*RGBAinactive)

		layerCount = editView.cachedLayerCount()
		lineOfLayers = []
		lineOfOffsets = []
		activePosition = editView.activePosition()
		# collect layers in the same line (to only draw the marks we need)
		for i, thisLayer in enumerate(editView.layoutManager().cachedLayers()):
			# collect layers and their offsets except newlines
			if not isinstance(thisLayer, GSControlLayer):
				lineOfLayers.append(thisLayer)
				lineOfOffsets.append(editView.cachedPositionAtIndex_(i))

			if not (isinstance(thisLayer, GSControlLayer) or i == layerCount - 1):
				continue

			# if we reach end of line or end of text, draw with collected layers:
			# step through all layers of the line:
			for j, thisLayerInLine in enumerate(lineOfLayers):
				# draw accents on them if they are Letter/Number/Punctuation
				if thisLayerInLine.parent.category in self.categoriesOnWhichToDrawAccents or thisLayerInLine.parent.name in self.specialGlyphsOnWhichToDrawAccents:
					thisLayerInLinePosition = lineOfOffsets[j]
					offset = subtractPoints(thisLayerInLinePosition, activePosition)
					if offset == NSPoint(0, 0):
						activeColor.set()
						self.drawMarksOnLayer(thisLayerInLine, lineOfLayers)
					else:
						inactiveColor.set()
						self.drawMarksOnLayer(thisLayerInLine, lineOfLayers, offset)

			# reset layer collection
			lineOfLayers = []
			lineOfOffsets = []

	def shouldDrawAccentCloudForLayer_(self, layer):
		return False

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
