#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2007-2008 One Laptop Per Child
# Copyright 2007 Gerard J. Cerchio <www.circlesoft.com>
# Copyright 2008 Andrés Ambrois <andresambrois@gmail.com>
# Copyright 2010 Marcos Orfila <www.marcosorfila.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

from gi.repository import Gtk
from gi.repository import Pango
import os
import commands
import platform

from sugar3.activity import activity
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.activity.widgets import ActivityButton
from sugar3.activity.widgets import TitleEntry
from sugar3.activity.widgets import StopButton

from gettext import gettext as _


class JreActivity(activity.Activity):

    def __init__(self, handle):
        activity.Activity.__init__(self, handle)
        self.max_participants = 1

        self.folder_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
        if platform.machine().startswith('arm'):
            self.jre_folder = None
            machine = "arm"
        else:
            if platform.architecture()[0] == '64bit':
                self.jre_folder = os.path.join(self.folder_path, "jre_64")
            else:
                self.jre_folder = None
                machine = "32"
        self.ceibaljam_icon_path = os.path.join(self.folder_path, "images/ceibaljam.png")

        self.build_toolbar()
        if self.jre_folder is not None:
            self.build_canvas()
        else:
            if machine == '32':
                label = Gtk.Label('<b>Please download the 32 bits version of Java activity</b>\nhttp://activities.sugarlabs.org/en-US/sugar/addon/4779/')
            if machine == 'arm':
                label = Gtk.Label('<b>Please download the ARM version of Java activity</b>\nhttp://activities.sugarlabs.org/en-US/sugar/addon/4780/')
            self.set_canvas(label)
        self.show_all()

    def build_toolbar(self):

        toolbox = ToolbarBox()

        activity_button = ActivityButton(self)
        toolbox.toolbar.insert(activity_button, -1)
        activity_button.show()

        separator = Gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbox.toolbar.insert(separator, -1)

        stop_button = StopButton(self)
        stop_button.props.accelerator = _('<Ctrl>Q')
        toolbox.toolbar.insert(stop_button, -1)
        stop_button.show()

        self.set_toolbar_box(toolbox)

    def build_canvas(self):

        box_canvas = Gtk.VBox(False, 0)

        # Title

        box_title = Gtk.VBox(False, 0)
        label_title = Gtk.Label(_("Java Runtime Environment"))
        label_title.set_justify(Gtk.Justification.CENTER)
        label_title.modify_font(Pango.FontDescription("Arial 18"))
        label_copyright1 = Gtk.Label(_("Copyright © 2010 Sun Microsystems, Inc., 4150 Network Circle, Santa Clara,"))
        label_copyright2 = Gtk.Label(_("California 95054, U.S.A.  All rights reserved."))
        label_copyright1.set_justify(Gtk.Justification.CENTER)
        label_copyright2.set_justify(Gtk.Justification.CENTER)

        box_title.add(Gtk.Label(""))
        box_title.add(Gtk.Label(""))
        box_title.add(label_title)
        box_title.add(Gtk.Label(""))
        box_title.add(Gtk.Label(""))
        box_title.add(label_copyright1)
        box_title.add(label_copyright2)
        box_title.add(Gtk.Label(""))

        # Version

        box_version = Gtk.VBox(False, 0)
        version_information = commands.getoutput(self.jre_folder + "/bin/java -version")
        label_version_info = Gtk.Label(version_information)
        label_version_info.set_justify(Gtk.Justification.CENTER)

        box_version.add(Gtk.Label(""))
        box_version.add(label_version_info)
        box_version.add(Gtk.Label(""))

        # Usage explanation

        box_usage = Gtk.VBox(False, 0)
        label_usage1 = Gtk.Label(_("To use this JRE in your activity, add the following line to your script:"))
        label_usage2 = Gtk.Label('<b>PATH=' + self.jre_folder + '/bin:$PATH</b>')
        label_usage2.set_use_markup(True)
        label_usage1.set_justify(Gtk.Justification.CENTER)
        label_usage2.set_justify(Gtk.Justification.CENTER)
        box_usage.add(Gtk.Label(""))
        box_usage.add(label_usage1)
        box_usage.add(label_usage2)
        box_usage.add(Gtk.Label(""))

        # Credits

        box_credits = Gtk.VBox(False, 0)
        box_credits.add(Gtk.Label(""))
        box_credits.add(Gtk.Label(_('Sugarized by %(THE_AUTHOR)s') % { 'THE_AUTHOR': 'Marcos Orfila' }))
        label_my_website = Gtk.Label('<b>http://www.marcosorfila.com</b>')
        label_my_website.set_use_markup(True)
        box_credits.add(label_my_website)
        box_credits.add(Gtk.Label(""))

        # Footer box (Activities on CeibalJAM! website)

        box_footer = Gtk.VBox(False, 0)
        box_footer.add(Gtk.Label(""))
        box_footer.add(Gtk.Label(_('Find more activities on %(CEIBALJAM)s website:') % { 'CEIBALJAM': 'CeibalJAM!'}))
        label_ceibaljam_website = Gtk.Label('<b>http://activities.ceibaljam.org</b>')
        label_ceibaljam_website.set_use_markup(True)
        box_footer.add(label_ceibaljam_website)
        box_footer.add(Gtk.Label(""))

        # CeibalJAM! image

        box_ceibaljam_image = Gtk.VBox(False, 0)
        image_ceibaljam = Gtk.Image()
        image_ceibaljam.set_from_file(self.ceibaljam_icon_path)
        box_ceibaljam_image.pack_end(image_ceibaljam, False, False, 0)

        # Get all the boxes together

        box_canvas.pack_start(box_title, False, False, 0)
        box_canvas.pack_start(box_version, False, False, 0)
        box_canvas.pack_start(box_usage, False, False, 0)
        box_canvas.pack_end(box_footer, False, False, 0)
        box_canvas.pack_end(box_ceibaljam_image, False, False, 0)
        box_canvas.pack_end(box_credits, False, False, 0)

        self.set_canvas(box_canvas)

