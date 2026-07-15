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

from krita import DockWidgetFactory, DockWidgetFactoryBase, Krita
from .simple_hsv_sliders import HCLSliders

DOCKER_ID = 'pykrita_simple_hsv_sliders'

instance = Krita.instance()
dock_widget_factory = DockWidgetFactory(DOCKER_ID,
                                        DockWidgetFactoryBase.DockPosition.DockRight,
                                        HCLSliders)

instance.addDockWidgetFactory(dock_widget_factory)
