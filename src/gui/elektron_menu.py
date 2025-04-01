from PyQt5.QtWidgets import QMenuBar, QAction

class ElektronMenu(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._create_menus()

    def _create_menus(self):
        self.file_menu = self.addMenu("File")
        self.edit_menu = self.addMenu("Edit")
        self.view_menu = self.addMenu("View")
        self.help_menu = self.addMenu("Help")

        self._add_file_menu_actions()
        self._add_edit_menu_actions()
        self._add_view_menu_actions()
        self._add_help_menu_actions()

    def _add_file_menu_actions(self):
        new_action = QAction("New", self)
        open_action = QAction("Open", self)
        save_action = QAction("Save", self)
        exit_action = QAction("Exit", self)

        self.file_menu.addAction(new_action)
        self.file_menu.addAction(open_action)
        self.file_menu.addAction(save_action)
        self.file_menu.addAction(exit_action)

        new_action.triggered.connect(self.parent().new_file)
        open_action.triggered.connect(self.parent().open_file)
        save_action.triggered.connect(self.parent().save_file)
        exit_action.triggered.connect(self.parent().exit_app)

    def _add_edit_menu_actions(self):
        undo_action = QAction("Undo", self)
        redo_action = QAction("Redo", self)
        cut_action = QAction("Cut", self)
        copy_action = QAction("Copy", self)
        paste_action = QAction("Paste", self)

        self.edit_menu.addAction(undo_action)
        self.edit_menu.addAction(redo_action)
        self.edit_menu.addAction(cut_action)
        self.edit_menu.addAction(copy_action)
        self.edit_menu.addAction(paste_action)

        undo_action.triggered.connect(self.parent().undo)
        redo_action.triggered.connect(self.parent().redo)
        cut_action.triggered.connect(self.parent().cut)
        copy_action.triggered.connect(self.parent().copy)
        paste_action.triggered.connect(self.parent().paste)

    def _add_view_menu_actions(self):
        zoom_in_action = QAction("Zoom In", self)
        zoom_out_action = QAction("Zoom Out", self)
        full_screen_action = QAction("Full Screen", self)

        self.view_menu.addAction(zoom_in_action)
        self.view_menu.addAction(zoom_out_action)
        self.view_menu.addAction(full_screen_action)

        zoom_in_action.triggered.connect(self.parent().zoom_in)
        zoom_out_action.triggered.connect(self.parent().zoom_out)
        full_screen_action.triggered.connect(self.parent().toggle_full_screen)

    def _add_help_menu_actions(self):
        about_action = QAction("About", self)
        help_action = QAction("Help", self)

        self.help_menu.addAction(about_action)
        self.help_menu.addAction(help_action)

        about_action.triggered.connect(self.parent().show_about)
        help_action.triggered.connect(self.parent().show_help)
