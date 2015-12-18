# Copyright (c) 2013 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.


from sgtk.platform import Application

class StgkStarterApp(Application):
    """
    The app entry point. This class is responsible for intializing and tearing down
    the application, handle menu registration etc.
    """

    def init_app(self):
        """
        Called as the application is being initialized
        """
        # first, we use the special import_module command to access the app module
        # that resides inside the python folder in the app. This is where the actual UI
        # and business logic of the app is kept. By using the import_module command,
        # toolkit's code reload mechanism will work properly.
        app_payload = self.import_module("app")

        # now register a panel, this is to tell the engine about the our panel ui 
        # that the engine can automatically create the panel - this happens for
        # example when a saved window layout is restored in Nuke or at startup.
        self._unique_panel_id = self.engine.register_panel(self.create_panel)
        
        # keep track of the last dialog we have created
        # in order to support the DIALOG mode for the navigate() method
        self._current_dialog = None
        
        # also register a menu entry on the shotgun menu so that users
        # can launch the panel
        self.engine.register_command("Shotgun Chat...", 
                                     self.create_panel, 
                                     {"type": "panel", 
                                      "short_name": "shotgun_chat"})

    def create_dialog(self):
        """
        Shows the panel as a dialog.
        
        Contrary to the create_panel() method, multiple calls
        to this method will result in multiple windows appearing. 
        
        :returns: The widget associated with the dialog. 
        """
        app_payload = self.import_module("app")
        widget = self.engine.show_dialog("Chat", self, app_payload.AppDialog)
        self._current_dialog = widget
        return widget

    def create_panel(self):
        """
        Shows the UI as a panel. 
        Note that since panels are singletons by nature,
        calling this more than once will only result in one panel.
        
        :returns: The widget associated with the panel.
        """
        app_payload = self.import_module("app")
        
        # start the UI
        try:
            widget = self.engine.show_panel(self._unique_panel_id, "Chat", self, app_payload.AppDialog)
        except AttributeError, e:
            # just to gracefully handle older engines and older cores
            self.log_warning("Could not execute show_panel method - please upgrade "
                             "to latest core and engine! Falling back on show_dialog. "
                             "Error: %s" % e)
            widget = self.create_dialog()
            
        return widget
