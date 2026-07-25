# SPDX-License-Identifier: GPL-3.0-or-later
#
# Simple HSV Sliders is a Krita plugin for color selection.
# Copyright (C) 2024  Lucifer <krita-artists.org/u/Lucifer>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# This file incorporates work covered by the following copyright and  
# permission notice:
#
#   Pigment.O is a Krita plugin and it is a Color Picker and Color Mixer.
#   Copyright ( C ) 2020  Ricardo Jeremias.
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   ( at your option ) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from krita import DockWidget, ManagedColor
from .qt_compat import *

from .colorconversion import Convert
from .settings import *


class ColorDisplay(QWidget):
    
    def __init__(self, parent):
        super().__init__(parent)

        self.hcl = parent
        self.current = None
        self.recent = None
        self.foreground = None
        self.background = None
        self.temp = None
        self.bgMode = False
        self.displayBoth = False
        self.flip = False
        self.switchToolTip()

    def setCurrentColor(self, color=None):
        self.current = color
        self.update()

    def setForeGroundColor(self, color=None):
        self.foreground = color
        self.update()

    def setBackGroundColor(self, color=None):
        self.background = color
        self.update()

    def setTempColor(self, color=None):
        self.temp = color
        self.update()

    def resetColors(self):
        self.current = None
        self.recent = None
        self.foreground = None
        self.background = None
        self.temp = None
        self.update()

    def isChanged(self):
        if self.current is None:
            return True
        if self.bgMode:
            if self.current.components() != self.background.components():
                return True
            if self.current.colorModel() != self.background.colorModel():
                return True
            if self.current.colorDepth() != self.background.colorDepth():
                return True
            if self.current.colorProfile() != self.background.colorProfile():
                return True
        else:
            if self.current.components() != self.foreground.components():
                return True
            if self.current.colorModel() != self.foreground.colorModel():
                return True
            if self.current.colorDepth() != self.foreground.colorDepth():
                return True
            if self.current.colorProfile() != self.foreground.colorProfile():
                return True
        return False
    
    def isChanging(self):
        if self.recent is None:
            return False
        if self.recent.components() != self.current.components():
            return True
        if self.recent.colorModel() != self.current.colorModel():
            return True
        if self.recent.colorDepth() != self.current.colorDepth():
            return True
        if self.recent.colorProfile() != self.current.colorProfile():
            return True
        return False
    
    def switchToolTip(self):
        if self.displayBoth:
            if self.flip:
                self.setToolTip("Foreground Color | Background Color")
            else:
                self.setToolTip("Background Color | Foreground Color")
        else:
            if self.bgMode:
                self.setToolTip("Background Color")
            else:
                self.setToolTip("Foreground Color")
    
    def switchMode(self):
        self.bgMode = not self.bgMode
        self.switchToolTip()
        self.update()
    
    def mousePressEvent(self, event):
        self.setFocus()
        self.switchMode()

    def displayBothColors(self, check: bool):
        self.displayBoth = check
        self.switchToolTip()
        self.update()

    def flipDisplay(self, check: bool):
        self.flip = check
        self.switchToolTip()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(PenStyle_NoPen)
        width = self.width()
        height = self.height()
        foreground = self.foreground.colorForCanvas(self.hcl.canvas()) if self.foreground else QColor(0, 0, 0)
        background = self.background.colorForCanvas(self.hcl.canvas()) if self.background else QColor(0, 0, 0)
        flipped = (self.bgMode and not self.flip) or (not self.bgMode and self.flip)
        if self.displayBoth:
            thirdwidth = round(width / 3.0)
            # foreground and background color from krita
            if flipped:
                painter.setBrush(QBrush(background if self.bgMode else foreground))
                painter.drawRect(0, 0, width - thirdwidth, height)
                painter.setBrush(QBrush(foreground if self.bgMode else background))
                painter.drawRect(width - thirdwidth, 0, thirdwidth, height)
            else:
                painter.setBrush(QBrush(foreground if self.bgMode else background))
                painter.drawRect(0, 0, thirdwidth, height)
                painter.setBrush(QBrush(background if self.bgMode else foreground))
                painter.drawRect(thirdwidth, 0, width - thirdwidth, height)
            if self.current:
                painter.setBrush(QBrush(self.current.colorForCanvas(self.hcl.canvas())))
                painter.drawRect(thirdwidth, 0, width - 2 * thirdwidth, height)
            if self.temp:
                painter.setBrush(QBrush(self.temp.colorForCanvas(self.hcl.canvas())))
                painter.drawRect(thirdwidth, 0, width - 2 * thirdwidth, height)
        else:
            halfwidth = round(width / 2.0)
            # foreground/background color from krita
            painter.setBrush(QBrush(background if self.bgMode else foreground)) 
            painter.drawRect(0, 0, width, height)
            # current color from sliders
            if self.current:
                painter.setBrush(QBrush(self.current.colorForCanvas(self.hcl.canvas())))
                if flipped:
                    painter.drawRect(halfwidth, 0, width - halfwidth, height)
                else:
                    painter.drawRect(0, 0, halfwidth, height)
            # indicator for picking past color in other mode
            if self.temp:
                painter.setBrush(QBrush(self.temp.colorForCanvas(self.hcl.canvas())))
                if flipped:
                    painter.drawRect(0, 0, halfwidth, height)
                else:
                    painter.drawRect(halfwidth, 0, width - halfwidth, height)


class ColorHistory(QListWidget):

    def __init__(self, hcl, parent=None):
        super().__init__(parent)
        # should not pass in hcl as parent if it can be hidden
        self.hcl = hcl
        self.index = -1
        self.modifier = None
        self.start = 0
        self.position = 0
        self.setFlow(QListWidget.Flow.LeftToRight)
        self.setFixedHeight(HISTORY_HEIGHT)
        self.setViewportMargins(-2, 0, 0, 0)
        # grid width + 2 to make gaps between swatches
        self.setGridSize(QSize(HISTORY_HEIGHT + 2, HISTORY_HEIGHT))
        self.setUniformItemSizes(True)
        self.setVerticalScrollBarPolicy(ScrollBarPolicy_ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(ScrollBarPolicy_ScrollBarAlwaysOff)
        self.setHorizontalScrollMode(QListWidget.ScrollMode.ScrollPerPixel)
        self.setSelectionMode(QListWidget.SelectionMode.NoSelection)

    def startScrollShift(self, event):
        self.start = self.horizontalScrollBar().value()
        self.position = int(event.position().x())
    
    def keyPressEvent(self, event):
        # disable keyboard interactions
        pass

    def mousePressEvent(self, event):
        self.hcl.setPressed(True)
        item = self.itemAt(event.position().toPoint())
        index = self.row(item)

        if index != -1:
            if (event.buttons() == MouseButton_LeftButton and 
                event.modifiers() == KeyboardModifier_NoModifier):
                color = self.hcl.makeManagedColor(*self.hcl.pastColors[index])
                if color:
                    if self.hcl.color.bgMode:
                        self.hcl.color.setTempColor(color)
                    else:
                        self.hcl.color.setCurrentColor(color)
                    self.index = index
                self.modifier = KeyboardModifier_NoModifier
            elif (event.buttons() == MouseButton_LeftButton and 
                event.modifiers() == KeyboardModifier_ControlModifier):
                color = self.hcl.makeManagedColor(*self.hcl.pastColors[index])
                if color:
                    if self.hcl.color.bgMode:
                        self.hcl.color.setCurrentColor(color)
                    else:
                        self.hcl.color.setTempColor(color)
                    self.index = index
                self.modifier = KeyboardModifier_ControlModifier
            elif (event.buttons() == MouseButton_LeftButton and 
                event.modifiers() == KeyboardModifier_AltModifier):
                self.index = index
                self.modifier = KeyboardModifier_AltModifier
        self.startScrollShift(event)

    def mouseMoveEvent(self, event):
        if (event.buttons() == MouseButton_LeftButton and 
            event.modifiers() == KeyboardModifier_ShiftModifier):
            position = 0
            bar = self.horizontalScrollBar()
            if bar.maximum():
                # speed of grid width squared seems good
                speed = (HISTORY_HEIGHT + 2) ** 2
                # move bar at constant speed
                shift = float(self.position - int(event.position().x())) / self.width()
                position = round(self.start + shift * speed)
            bar.setValue(position)
        else:
            self.startScrollShift(event)

    def mouseReleaseEvent(self, event):
        item = self.itemAt(event.position().toPoint())
        index = self.row(item)

        if index == self.index and index != -1:
            if (event.modifiers() == KeyboardModifier_NoModifier and 
                self.modifier == KeyboardModifier_NoModifier):
                self.hcl.setPastColor(index)
            elif (event.modifiers() == KeyboardModifier_ControlModifier and 
                  self.modifier == KeyboardModifier_ControlModifier):
                self.hcl.setPastColor(index, False)
        
        if (event.modifiers() == KeyboardModifier_AltModifier and 
            self.modifier == KeyboardModifier_AltModifier):
            if self.index != -1 and index != -1 :
                start = index
                stop = self.index
                if self.index > index:
                    start = self.index
                    stop = index
                for i in range(start, stop - 1, -1):
                    self.takeItem(i)
                    self.hcl.pastColors.pop(i)

        if self.modifier == KeyboardModifier_NoModifier and self.index != -1:
            if self.hcl.color.bgMode:
                self.hcl.color.setTempColor()
            else:
                # prevent setHistory when krita fg color not changed
                self.hcl.color.current = self.hcl.color.foreground
        elif self.modifier == KeyboardModifier_ControlModifier and self.index != -1:
            if self.hcl.color.bgMode:
                # prevent setHistory when krita bg color not changed
                self.hcl.color.current = self.hcl.color.background
            else:
                self.hcl.color.setTempColor()
        
        self.modifier = None
        self.index = -1
        self.hcl.setPressed(False)


class ChannelSlider(QWidget):

    valueChanged = pyqtSignal(float)
    mousePressed = pyqtSignal(bool)

    def __init__(self, limit: float, parent=None):
        super().__init__(parent)

        self.value = 0.0
        self.limit = limit
        self.interval = 0.1
        self.displacement = 0
        self.start = 0.0
        self.position = 0
        self.shift = 0.1
        self.colors = []

    def setGradientColors(self, colors: list):
        if self.colors:
            self.colors = []
        for rgb in colors:
            # using rgbF as is may result in black as colors are out of gamut
            color = QColor(*rgb)
            self.colors.append(color)
        self.update()

    def setValue(self, value: float):
        self.value = value
        self.update()

    def setLimit(self, value: float):
        self.limit = value
        self.update()

    def setInterval(self, interval: float):
        limit = 100.0 if self.limit < 360 else 360.0
        if interval < 0.1:
            interval = 0.1
        elif interval > limit:
            interval = limit
        self.interval = interval

    def setDisplacement(self, displacement: float):
        limit = 99.9 if self.limit < 360 else 359.9
        if displacement < 0:
            displacement = 0
        elif displacement > limit:
            displacement = limit
        self.displacement = displacement

    def emitValueChanged(self, event):
        position = int(event.position().x())
        width = self.width()
        if position > width:
            position = width
        elif position < 0:
            position = 0.0
        self.value = round((position / width) * self.limit, 4)
        self.valueChanged.emit(self.value)
        self.mousePressed.emit(True)

    def emitValueSnapped(self, event):
        position = int(event.position().x())
        width = self.width()
        if position > width:
            position = width
        elif position < 0:
            position = 0.0
        value = round((position / width) * self.limit, 4)

        if value != 0 and value != self.limit:
            interval = self.interval if self.interval != 0 else self.limit
            if self.limit < 100:
                interval = (self.interval / 100) * self.limit
            displacement = (value - self.displacement) % interval
            if displacement < interval / 2:
                value -= displacement
            else:
                value += interval - displacement
            if value > self.limit:
                value = self.limit
            elif value < 0:
                value = 0.0
        
        self.value = value
        self.valueChanged.emit(self.value)
        self.mousePressed.emit(True)
    
    def startValueShift(self, event):
        self.start = self.value
        self.position = int(event.position().x())
    
    def emitValueShifted(self, event):
        position = int(event.position().x())
        vector = position - self.position
        if self.limit < 100:
            self.shift /= 100 / self.limit
        value = self.start + (vector * self.shift)

        if value < 0:
            if self.limit == 360:
                value += self.limit
            else:
                value = 0
        elif value > self.limit:
            if self.limit == 360:
                value -= self.limit
            else:
                value = self.limit
          
        self.value = value
        self.valueChanged.emit(self.value)
        self.mousePressed.emit(True)

    def mousePressEvent(self, event):
        if (event.buttons() == MouseButton_LeftButton and 
            event.modifiers() == KeyboardModifier_NoModifier):
            self.emitValueChanged(event)
        elif (event.buttons() == MouseButton_LeftButton and 
              event.modifiers() == KeyboardModifier_ControlModifier):
            self.emitValueSnapped(event)
        self.startValueShift(event)
        self.update()

    def mouseMoveEvent(self, event):
        if (event.buttons() == MouseButton_LeftButton and 
            event.modifiers() == KeyboardModifier_NoModifier):
            self.emitValueChanged(event)
            self.startValueShift(event)
        elif (event.buttons() == MouseButton_LeftButton and 
              event.modifiers() == KeyboardModifier_ControlModifier):
            self.emitValueSnapped(event)
            self.startValueShift(event)
        elif (event.buttons() == MouseButton_LeftButton and 
              event.modifiers() == KeyboardModifier_ShiftModifier):
            self.shift = 0.1
            self.emitValueShifted(event)
        elif (event.buttons() == MouseButton_LeftButton and 
              event.modifiers() == KeyboardModifier_AltModifier):
            self.shift = 0.01
            self.emitValueShifted(event)
        self.update()

    def mouseReleaseEvent(self, event):
        self.mousePressed.emit(False)

    def paintEvent(self, event):
        painter = QPainter(self)
        width = self.width()
        height = self.height()
        # background
        painter.setPen(PenStyle_NoPen)
        painter.setBrush( QBrush(QColor(0, 0, 0, 50)))
        painter.drawRect(0, 1, width, height - 2)
        # gradient
        gradient = QLinearGradient(0, 0, width, 0)
        if self.colors:
            for index, color in enumerate(self.colors):
                gradient.setColorAt(index / (len(self.colors) - 1), color)
        painter.setBrush(QBrush(gradient))
        painter.drawRect(1, 2, width - 2, height - 4)
        # cursor
        if self.limit:
            position = round((self.value / self.limit) * (width - 2))
            painter.setBrush( QBrush(QColor(0, 0, 0, 100)))
            painter.drawRect(position - 2, 0, 6, height)
            painter.setBrush(QBrush(QColor(255, 255, 255, 200)))
            painter.drawRect(position, 1, 2, height - 2)


class ColorChannel:

    channelList = None

    def __init__(self, name: str, parent):
        self.name = name
        self.update = parent.updateChannels
        self.refresh = parent.updateChannelGradients
        wrap = False
        interval = 10.0
        displacement = 0.0
        self.scale = True
        self.clip = 0.0
        self.colorful = False
        self.luma = False
        self.limit = 100.0
        if self.name[-3:] == "Hue":
            wrap = True
            interval = 30.0
            if self.name[:2] == "ok":
                interval = 40.0
                displacement = 25.0
            self.limit = 360.0
        elif self.name[-6:] == "Chroma":
            self.limit = 0.0
        self.layout = QHBoxLayout()
        self.layout.setSpacing(2)

        if self.name[:2] == "ok":
            tip = f"{self.name[:5].upper()} {self.name[5:]}"
            letter = self.name[5:6]
        else:
            tip = f"{self.name[:3].upper()} {self.name[3:]}"
            if self.name[-4:] == "Luma":
                letter = "Y"
            else:
                letter = self.name[3:4]
        self.label = QLabel(letter)
        self.label.setFixedHeight(CHANNEL_HEIGHT - 1)
        self.label.setFixedWidth(LABEL_WIDTH)
        self.label.setAlignment(AlignmentFlag_AlignCenter)
        self.label.setToolTip(tip)

        self.slider = ChannelSlider(self.limit)
        self.slider.setFixedHeight(CHANNEL_HEIGHT)
        self.slider.setMinimumWidth(100)
        self.slider.setInterval(interval)
        self.slider.setDisplacement(displacement)
        self.slider.mousePressed.connect(parent.setPressed)

        self.spinBox = QDoubleSpinBox()
        if self.name[-6:] == "Chroma":
            if self.name[:5] == "oklch":
                self.spinBox.setDecimals(4)
            else:    
                self.spinBox.setDecimals(3)
        self.spinBox.setMaximum(self.limit)
        self.spinBox.setWrapping(wrap)
        self.spinBox.setFixedHeight(CHANNEL_HEIGHT)
        self.spinBox.setFixedWidth(VALUES_WIDTH)
        self.spinBox.editingFinished.connect(parent.finishEditing)

        self.slider.valueChanged.connect(self.updateSpinBox)
        self.spinBox.valueChanged.connect(self.updateSlider)
        ColorChannel.updateList(name)

    def value(self):
        return self.spinBox.value()
    
    def setValue(self, value: float):
        if self.name[-6:] == "Chroma" and self.limit >= 10:
            value = round(value, 2)
        self.slider.setValue(value)
        self.spinBox.setValue(value)

    def setLimit(self, value: float):
        if self.name == "oklchChroma":
            self.limit = value
        else:
            decimal = 2 if value >= 10 else 3
            self.spinBox.setDecimals(decimal)
            self.limit = round(value, decimal)
        self.slider.setLimit(self.limit)
        self.spinBox.setMaximum(self.limit)
        self.spinBox.setSingleStep(self.limit / 100)

    def clipChroma(self, clip: bool):
        # do not set chroma channel itself to clip as the clip value will not be updated when adjusting
        self.scale = not clip
        self.refresh()

    def colorfulHue(self, colorful: bool):
        self.colorful = colorful
        self.refresh()

    def updateSlider(self, value: float):
        self.update(value, self.name, "slider")

    def updateSpinBox(self, value: float):
        self.update(value, self.name, "spinBox")
    
    def updateGradientColors(self, firstConst: float, lastConst: float, trc: str, ChromaLimit: float=-1):
        colors = []
        if self.name[-3:] == "Hue":
            if self.name[:2] == "ok":
                # oklab hue needs more points for qcolor to blend more accurately
                # range of 0 to 25 - 345 in 15deg increments to 360
                points = 26
                increment = self.limit / (points - 2)
                displacement = increment - 25

                if self.colorful:
                    for number in range(points):
                        hue = (number - 1) * increment - displacement
                        if hue < 0:
                            hue = 0
                        elif hue > self.limit:
                            hue = self.limit
                        rgb = Convert.okhsvToRgbF(hue, 100.0, 100.0, trc)
                        colors.append(Convert.rgbFToInt8(*rgb, trc))
                elif self.name[:5] == "okhcl":
                    for number in range(points):
                        hue = (number - 1) * increment - displacement
                        if hue < 0:
                            hue = 0
                        elif hue > self.limit:
                            hue = self.limit
                        rgb = Convert.okhclToRgbF(hue, firstConst, lastConst, ChromaLimit, trc)
                        colors.append(Convert.rgbFToInt8(*rgb, trc))
                elif self.name[:5] == "okhsv":
                    for number in range(points):
                        hue = (number - 1) * increment - displacement
                        if hue < 0:
                            hue = 0
                        elif hue > self.limit:
                            hue = self.limit
                        rgb = Convert.okhsvToRgbF(hue, firstConst, lastConst, trc)
                        colors.append(Convert.rgbFToInt8(*rgb, trc))
                elif self.name[:5] == "okhsl":
                    for number in range(points):
                        hue = (number - 1) * increment - displacement
                        if hue < 0:
                            hue = 0
                        elif hue > self.limit:
                            hue = self.limit
                        rgb = Convert.okhslToRgbF(hue, firstConst, lastConst, trc)
                        colors.append(Convert.rgbFToInt8(*rgb, trc))
                elif self.name[:5] == "oklch":
                    for number in range(points):
                        hue = (number - 1) * increment - displacement
                        if hue < 0:
                            hue = 0
                        elif hue > self.limit:
                            hue = self.limit
                        rgb = Convert.oklchToRgbF(firstConst, lastConst, hue, ChromaLimit, trc)
                        colors.append(Convert.rgbFToInt8(*rgb, trc))
            else:
                # range of 0 to 360deg incrementing by 30deg
                points = 13
                increment = self.limit / (points - 1)

                if self.colorful:
                    if self.name[:3] != "hcy":
                        for number in range(points):
                            rgb = Convert.hsvToRgbF(number * increment, 100.0, 100.0, trc)
                            colors.append(Convert.rgbFToInt8(*rgb, trc))
                    else:
                        for number in range(points):
                            rgb = Convert.hcyToRgbF(number * increment, 100.0, -1, -1, trc, self.luma)
                            colors.append(Convert.rgbFToInt8(*rgb, trc))
                elif self.name[:3] == "hsv":
                    for number in range(points):
                        rgb = Convert.hsvToRgbF(number * increment, firstConst, lastConst, trc)
                        colors.append(Convert.rgbFToInt8(*rgb, trc))
                elif self.name[:3] == "hsl":
                    for number in range(points):
                        rgb = Convert.hslToRgbF(number * increment, firstConst, lastConst, trc)
                        colors.append(Convert.rgbFToInt8(*rgb, trc))
                elif self.name[:3] == "hcy":
                    for number in range(points):
                        rgb = Convert.hcyToRgbF(number * increment, firstConst, lastConst, 
                                                ChromaLimit, trc, self.luma)
                        colors.append(Convert.rgbFToInt8(*rgb, trc))
        else:
            # range of 0 to 100% incrementing by 10%
            points = 11
            increment = self.limit / (points - 1)

            if self.name[:3] == "hsv":
                if self.name[3:] == "Saturation":
                    for number in range(points):
                        rgb = Convert.hsvToRgbF(firstConst, number * increment, lastConst, trc)
                        colors.append(Convert.rgbFToInt8(*rgb, trc))
                elif self.name[3:] == "Value":
                    for number in range(points):
                        rgb = Convert.hsvToRgbF(firstConst, lastConst, number * increment, trc)
                        colors.append(Convert.rgbFToInt8(*rgb, trc))
            elif self.name[:3] == "hsl":
                if self.name[3:] == "Saturation":
                    for number in range(points):
                        rgb = Convert.hslToRgbF(firstConst, number * increment, lastConst, trc)
                        colors.append(Convert.rgbFToInt8(*rgb, trc))
                elif self.name[3:] == "Lightness":
                    for number in range(points):
                        rgb = Convert.hslToRgbF(firstConst, lastConst, number * increment, trc)
                        colors.append(Convert.rgbFToInt8(*rgb, trc))
            elif self.name[:3] == "hcy":
                if self.name[3:] == "Chroma":
                    for number in range(points):
                        rgb = Convert.hcyToRgbF(firstConst, number * increment, lastConst, 
                                                ChromaLimit, trc, self.luma)
                        colors.append(Convert.rgbFToInt8(*rgb, trc))
                elif self.name[3:] == "Luma":
                    for number in range(points):
                        rgb = Convert.hcyToRgbF(firstConst, lastConst, number * increment, 
                                                ChromaLimit, trc, self.luma)
                        colors.append(Convert.rgbFToInt8(*rgb, trc))
            elif self.name[:5] == "okhcl":
                if self.name[5:] == "Chroma":
                    for number in range(points):
                        rgb = Convert.okhclToRgbF(firstConst, number * increment, lastConst, 
                                                  ChromaLimit, trc)
                        colors.append(Convert.rgbFToInt8(*rgb, trc))
                elif self.name[5:] == "Lightness":
                    for number in range(points):
                        rgb = Convert.okhclToRgbF(firstConst, lastConst, number * increment, 
                                                  ChromaLimit, trc)
                        colors.append(Convert.rgbFToInt8(*rgb, trc))
            elif self.name[:5] == "okhsv":
                if self.name[5:] == "Saturation":
                    for number in range(points):
                        rgb = Convert.okhsvToRgbF(firstConst, number * increment, lastConst, trc)
                        colors.append(Convert.rgbFToInt8(*rgb, trc))
                elif self.name[5:] == "Value":
                    for number in range(points):
                        rgb = Convert.okhsvToRgbF(firstConst, lastConst, number * increment, trc)
                        colors.append(Convert.rgbFToInt8(*rgb, trc))
            elif self.name[:5] == "okhsl":
                if self.name[5:] == "Saturation":
                    for number in range(points):
                        rgb = Convert.okhslToRgbF(firstConst, number * increment, lastConst, trc)
                        colors.append(Convert.rgbFToInt8(*rgb, trc))
                elif self.name[5:] == "Lightness":
                    for number in range(points):
                        rgb = Convert.okhslToRgbF(firstConst, lastConst, number * increment, trc)
                        colors.append(Convert.rgbFToInt8(*rgb, trc))
            elif self.name[:5] == "oklch":
                if self.name[5:] == "Chroma":
                    for number in range(points):
                        rgb = Convert.oklchToRgbF(firstConst, number * increment, lastConst, 
                                                  ChromaLimit, trc)
                        colors.append(Convert.rgbFToInt8(*rgb, trc))
                elif self.name[5:] == "Lightness":
                    for number in range(points):
                        rgb = Convert.oklchToRgbF(number * increment, firstConst, lastConst, 
                                                  ChromaLimit, trc)
                        colors.append(Convert.rgbFToInt8(*rgb, trc))

        self.slider.setGradientColors(colors)

    def blockSignals(self, block: bool):
        self.slider.blockSignals(block)
        self.spinBox.blockSignals(block)

    @classmethod
    def updateList(cls, name: str):
        if cls.channelList is None:
            cls.channelList = []
        if name not in cls.channelList:
            cls.channelList.append(name)

    @classmethod
    def getList(cls):
        return cls.channelList.copy()
        

class HCLSliders(DockWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle(DOCKER_NAME)
        mainWidget = QWidget(self)
        mainWidget.setContentsMargins(2, 1, 2, 1)
        self.setWidget(mainWidget)
        self.mainLayout = QVBoxLayout(mainWidget)
        self.mainLayout.setSpacing(2)
        self.document = None
        self.memory = 30
        self.trc = "sRGB"
        self.pressed = False
        self.editing = False
        self._deferGradientChannels = set()
        self.pastColors = []
        self.displayOrder = []
        self.loadChannels()
        self.history = ColorHistory(self)
        self._loadHexInput()
        self.readSettings()
        self.displayChannels()

    def colorDisplay(self):
        # load into channel layout to prevent alignment issue when channels empty
        layout = QHBoxLayout()
        layout.setSpacing(2)

        self.color = ColorDisplay(self)
        self.color.setFixedHeight(DISPLAY_HEIGHT)
        layout.addWidget(self.color)


        self.timer = QTimer()
        self.timer.timeout.connect(self.getKritaColors)
        self.singleShot = QTimer()
        self.singleShot.setSingleShot(True)
        self.singleShot.timeout.connect(self.setHistory)
        self.gradientTimer = QTimer()
        self.gradientTimer.setSingleShot(True)
        self.gradientTimer.timeout.connect(self._computeDeferredGradients)
        return layout
    
    def loadChannels(self):
        self.channelLayout = QVBoxLayout()
        self.channelLayout.setAlignment(AlignmentFlag_AlignTop)
        self.channelLayout.setSpacing(2)
        self.channelLayout.addLayout(self.colorDisplay())
        self.channelLayout.addSpacing(1)

        self.hsvHue = ColorChannel("hsvHue", self)
        self.hsvSaturation = ColorChannel("hsvSaturation", self)
        self.hsvValue = ColorChannel("hsvValue", self)

        self.mainLayout.addLayout(self.channelLayout)

    def _loadHexInput(self):
        self.hexLayout = QHBoxLayout()
        self.hexLayout.setSpacing(2)
        hexLabel = QLabel("#")
        hexLabel.setFixedHeight(CHANNEL_HEIGHT - 1)
        hexLabel.setFixedWidth(LABEL_WIDTH)
        hexLabel.setAlignment(AlignmentFlag_AlignCenter)
        self.hexLayout.addWidget(hexLabel)
        self.hexInput = QLineEdit()
        self.hexInput.setFixedHeight(CHANNEL_HEIGHT - 1)
        self.hexInput.setMaxLength(7)
        self.hexInput.setPlaceholderText("RRGGBB")
        self.hexInput.setAlignment(AlignmentFlag_AlignCenter)
        self.hexInput.editingFinished.connect(self._parseHex)
        self.hexLayout.addWidget(self.hexInput)
        self.mainLayout.addSpacing(1)
        self.mainLayout.addLayout(self.hexLayout)

    def readSettings(self):
        channels = ColorChannel.getList()
        self.displayOrder = list(channels)

        for name in channels:
            settings: list = Application.readSetting(DOCKER_NAME, name, "").split(",")
            if len(settings) > 1:
                channel: ColorChannel = getattr(self, name)
                try:
                    channel.slider.setInterval(float(settings[0]))
                except ValueError:
                    pass
                try:
                    channel.slider.setDisplacement(float(settings[1]))
                except ValueError:
                    pass

        history = Application.readSetting(DOCKER_NAME, "history", "").split(",")
        if len(history) == 2:
            self.history.setEnabled(history[0] != "False")
            try:
                memory = int(history[1])
                if 0 <= memory <= 999:
                    self.memory = memory
            except ValueError:
                pass

    def writeSettings(self):
        for name in ColorChannel.getList():
            settings = []
            channel: ColorChannel = getattr(self, name)
            settings.append(str(channel.slider.interval))
            settings.append(str(channel.slider.displacement))
            Application.writeSetting(DOCKER_NAME, name, ",".join(settings))

        history = [str(self.history.isEnabled()), str(self.memory)]
        Application.writeSetting(DOCKER_NAME, "history", ",".join(history))

    def displayChannels(self):
        prev = ""
        for name in self.displayOrder:
            if MODEL_SPACING:
                model = name[:5] if name[:2] == "ok" else name[:3]
                if prev and prev != model:
                    self.channelLayout.addSpacing(MODEL_SPACING)
                prev = model
            channel = getattr(self, name)
            channel.layout.addWidget(channel.label)
            channel.layout.addWidget(channel.slider)
            channel.layout.addWidget(channel.spinBox)
            self.channelLayout.addLayout(channel.layout)

    def clearChannels(self):
        # first 2 items in channelLayout is color display and spacing
        for i in reversed(range(self.channelLayout.count() - 2)):
            item = self.channelLayout.itemAt(i + 2)
            layout = item.layout()
            if layout:
                for index in reversed(range(layout.count())):
                    widget = layout.itemAt(index).widget()
                    layout.removeWidget(widget)
                    widget.setParent(None)
            self.channelLayout.removeItem(item)

    def displayOthers(self):
        pass

    def clearOthers(self):
        pass

    def openConfig(self):
        pass

    def profileTRC(self, profile: str):
        if profile in SRGB:
            return "sRGB"
        elif profile in LINEAR:
            return "linear"
        return self.trc
    
    def setMemory(self, memory: int):
        self.memory = memory

    def setPressed(self, pressed: bool):
        self.pressed = pressed

    def finishEditing(self):
        self.editing = False

    def getKritaColors(self):
        view = Application.activeWindow().activeView()
        if not view.visible():
            return

        if not self.pressed and not self.editing:
            if self.color.isChanged() and self.color.current:
                self.setHistory()

            foreground = view.foregroundColor()
            self.color.setForeGroundColor(foreground)
            background = view.backgroundColor()
            self.color.setBackGroundColor(background)

            if self.color.isChanged():
                if self.color.bgMode:
                    self.color.setCurrentColor(background)
                else:
                    self.color.setCurrentColor(foreground)

                current = self.color.current
                rgb = tuple(current.componentsOrdered()[:3])
                if current.colorModel() != "RGBA":
                    if current.colorModel() in ("A", "GRAYA"):
                        rgb = (rgb[0], rgb[0], rgb[0])
                    else:
                        return
                
                trc = self.profileTRC(current.colorProfile())
                self._updateHex(rgb, trc)
                if trc != self.trc:
                    rgb = Convert.rgbToTRC(rgb, self.trc)
                self.updateChannels(rgb)
                if not self.singleShot.isActive():
                    self.color.recent = current
                    self.singleShot.start(DELAY)

    def blockChannels(self, block: bool):
        self.hsvHue.blockSignals(block)
        self.hsvSaturation.blockSignals(block)
        self.hsvValue.blockSignals(block)

    def updateChannels(self, values: tuple|float, name: str=None, widget: str=None):
        self.timer.stop()
        self.blockChannels(True)
        
        if type(values) is tuple:
            self.setChannelValues("hsv", values)
        else:
            channel: ColorChannel = getattr(self, name)
            channelWidget = getattr(channel, widget)
            channelWidget.setValue(values)
            if widget == "slider":
                self.editing = True
            hue = self.hsvHue.value()
            rgb = Convert.hsvToRgbF(hue, self.hsvSaturation.value(), 
                                    self.hsvValue.value(), self.trc)
            self.setKritaColor(rgb)
        
        self.blockChannels(False)
        if TIME:
            self.timer.start(TIME)
        if self.pressed:
            if name:
                self._deferGradientChannels.add(name)
            else:
                self._deferGradientChannels.update(("hsvHue", "hsvSaturation", "hsvValue"))
            if not self.gradientTimer.isActive():
                self.gradientTimer.start(16)
        else:
            self.updateChannelGradients()

    def _computeDeferredGradients(self):
        names = self._deferGradientChannels
        self._deferGradientChannels = set()
        if not names:
            return
        hue = self.hsvHue.value()
        sat = self.hsvSaturation.value()
        val = self.hsvValue.value()
        if any(n in ("hsvSaturation", "hsvValue") for n in names):
            self.hsvHue.updateGradientColors(sat, val, self.trc)
        if any(n in ("hsvHue", "hsvValue") for n in names):
            self.hsvSaturation.updateGradientColors(hue, val, self.trc)
        if any(n in ("hsvHue", "hsvSaturation") for n in names):
            self.hsvValue.updateGradientColors(hue, sat, self.trc)

    def updateChannelGradients(self, channels: str=None):
        self.hsvHue.updateGradientColors(self.hsvSaturation.value(), self.hsvValue.value(), 
                                         self.trc)
        self.hsvSaturation.updateGradientColors(self.hsvHue.value(), self.hsvValue.value(), 
                                                self.trc)
        self.hsvValue.updateGradientColors(self.hsvHue.value(), self.hsvSaturation.value(), 
                                           self.trc)

    def setChannelValues(self, channels: str, rgb: tuple, hue: float=-1):
        if channels == "hsv":
            hsv = Convert.rgbFToHsv(*rgb, self.trc)
            if hue != -1:
                self.hsvHue.setValue(hue)
            elif hsv[1] > 0:
                self.hsvHue.setValue(hsv[0])
            if hsv[2] > 0:
                self.hsvSaturation.setValue(hsv[1])
            self.hsvValue.setValue(hsv[2])

    def makeManagedColor(self, rgb: tuple, profile: str=None):
        model = "RGBA"
        depth = self.document.colorDepth()
        if not profile:
                if self.trc == "sRGB":
                    profile = SRGB[0]
                else:
                    profile = LINEAR[0]
        elif profile not in Application.profiles(model, depth):
            models = filter(lambda cm: cm != "RGBA", Application.colorModels())
            for cm in models:
                if profile in Application.profiles(cm, depth):
                    model = cm
                    break

        color = ManagedColor(model, depth, profile)
        components = color.components()
        if model == "RGBA":
            if depth[0] == "U":
                components[0] = rgb[2]
                components[1] = rgb[1]
                components[2] = rgb[0]
            else:
                components[0] = rgb[0]
                components[1] = rgb[1]
                components[2] = rgb[2]
            components[3] = 1.0
            color.setComponents(components)
            return color
        elif model in ("A", "GRAYA"):
            components[0] = rgb[0]
            components[1] = 1.0
            color.setComponents(components)
            return color

    def setKritaColor(self, rgb: tuple):
        view = Application.activeWindow().activeView()
        if not view.visible():
            return
        
        color = self.makeManagedColor(rgb)
        if color:
            self.color.setCurrentColor(color)
            self._updateHex(rgb, self.trc)
            if self.color.bgMode:
                view.setBackGroundColor(color)
            else:
                view.setForeGroundColor(color)
            self.color.recent = color

    def setHistory(self):
        if self.color.isChanging():
            self.color.current = None
            return
        
        current = self.color.current
        rgb = tuple(current.componentsOrdered()[:3])
        if current.colorModel() in ("A", "GRAYA"):
            rgb = (rgb[0], rgb[0], rgb[0])
        profile = current.colorProfile()
        color = (rgb, profile)
        if color in self.pastColors:
            index = self.pastColors.index(color)
            if index:
                self.pastColors.pop(index)
                self.pastColors.insert(0, color)
                item = self.history.takeItem(index)
                self.history.insertItem(0, item)
        else:
            self.pastColors.insert(0, color)
            pixmap = QPixmap(HISTORY_HEIGHT, HISTORY_HEIGHT)
            pixmap.fill(QColor(*Convert.rgbFToInt8(*rgb, self.profileTRC(profile))))
            item = QListWidgetItem()
            item.setIcon(QIcon(pixmap))
            self.history.insertItem(0, item)
            if self.memory:
                for i in reversed(range(self.history.count())):
                    if i > self.memory - 1:
                        self.history.takeItem(i)
                        self.pastColors.pop()
                    else:
                        break
        self.history.horizontalScrollBar().setValue(0)

    def setPastColor(self, index: int, fg=True):
        view = Application.activeWindow().activeView()
        if not view.visible():
            return
        
        if (self.color.bgMode and not fg) or (fg and not self.color.bgMode):
            self.history.takeItem(index)
            color = self.pastColors.pop(index)
            rgb = color[0]
            trc = self.profileTRC(color[1])
            self._updateHex(rgb, trc)
            if trc != self.trc:
                rgb = Convert.rgbToTRC(rgb, self.trc)
            self.updateChannels(rgb)

            current = self.color.current
            if fg:
                view.setForeGroundColor(current)
                self.color.setForeGroundColor(current)
            else:
                view.setBackGroundColor(current)
                self.color.setBackGroundColor(current)
            self.color.recent = current
            self.setHistory()
        else:
            temp = self.color.temp
            if fg:
                view.setForeGroundColor(temp)
                self.color.setForeGroundColor(temp)
            else:
                view.setBackGroundColor(temp)
                self.color.setBackGroundColor(temp)

    def clearHistory(self):
        self.history.clear()
        self.pastColors = []

    def _updateHex(self, rgb: tuple, trc: str):
        self.hexInput.blockSignals(True)
        self.hexInput.setText(Convert.rgbFToHexS(*rgb, trc))
        self.hexInput.blockSignals(False)

    def _parseHex(self):
        view = Application.activeWindow().activeView()
        if not view.visible():
            return
        text = self.hexInput.text().strip()
        if not text.startswith("#"):
            text = "#" + text
        result = Convert.parseAnything(text, self.trc, "HEX")
        if result is None:
            return
        rgb, _ = result
        if rgb:
            self.setKritaColor(rgb)
            self.updateChannels(rgb)

    def showEvent(self, event):
        if TIME:
            self.timer.start(TIME)

    def closeEvent(self, event):
        self.timer.stop()
        self.gradientTimer.stop()

    def canvasChanged(self, canvas):
        if self.document != Application.activeDocument():
            self.color.resetColors()
            self.hexInput.clear()
            self.document = Application.activeDocument()
            if self.document:
                self.trc = self.profileTRC(self.document.colorProfile())    
                self.getKritaColors()

