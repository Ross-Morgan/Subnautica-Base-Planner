import sys
from functools import partial

from PyQt6 import QtCore, QtGui, QtSvgWidgets, QtWidgets

from assets import Assets, Config, load_config
from subnautica import (Item, Material, base_pieces, interior_mods,
                        interior_pieces, power_sources)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, config: Config):
        super().__init__(parent=None,
                         flags=QtCore.Qt.WindowType.WindowStaysOnTopHint)

        self.setFixedSize(config.size)
        self.setWindowTitle(config.title)
        self.setWindowIcon(config.icon)

        QtGui.QFontDatabase.addApplicationFont(Assets.roboto)

        self.loaded_image = 0
        self.material_mappings: dict[QtWidgets.QWidget, Material] = {}
        self.current_materials: dict[Material, int] = {}

        self.setup_ui()
        self.connect_ui()
        self.apply_styles()

    def setup_ui(self):
        def spinbox() -> QtWidgets.QSpinBox:
            box = QtWidgets.QSpinBox()
            box.setMinimum(0)
            box.setFont(QtGui.QFont("Roboto", 20))
            box.setStyleSheet(Assets.Scripts.spinbox)

        class ui:  # noqa NOSONAR
            background = QtSvgWidgets.QSvgWidget(
                Assets.Images.backgrounds[self.loaded_image], self
            )
            background.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
            self.setCentralWidget(background)

            depth_slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Vertical,
                                             self)
            depth_slider.setGeometry(1780, 40, 100, 1000)
            depth_slider.setMinimum(-2000)
            depth_slider.setMaximum(0)

            depth_meter_label = QtWidgets.QLabel("Depth:", self)
            depth_meter_label.setGeometry(1540, 40, 220, 75)
            depth_meter_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            depth_meter = QtWidgets.QLabel("0m", self)
            depth_meter.setGeometry(1540, 135, 220, 75)
            depth_meter.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            #####

            materials_button = QtWidgets.QLabel("Materials", self)
            materials_button.setGeometry(1540, 1035, 220, 75)

            #####

            material_frame = QtWidgets.QFrame(self)
            material_frame.setGeometry(10, 10, 1200, 800)

            materials = QtWidgets.QHBoxLayout()

            class base_pieces:  # noqa NOSONAR
                buildings = QtWidgets.QFrame()

                group = QtWidgets.QGroupBox("Base Pieces", buildings)
                group.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)

                form = QtWidgets.QFormLayout()

                for room in base_pieces:
                    box = spinbox()
                    box.valueChanged.connect(partial(self.change_item_count,
                                                     base_pieces[room]))

                    self.material_mappings[box] = base_pieces[room]

                    form.addRow(room, box)

                group.setLayout(form)

            class power_pieces:  # noqa NOSONAR
                power = QtWidgets.QFrame()

                group = QtWidgets.QGroupBox("Power Sources", power)
                group.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)

                form = QtWidgets.QFormLayout()

                for source in power_sources:
                    box = spinbox()
                    box.valueChanged.connect(partial(self.change_item_count,
                                                     power_sources[source]))

                    self.material_mappings[box] = power_sources[source]

                    form.addRow(source, box)

                group.setLayout(form)

            class interior_pieces:
                interior = QtWidgets.QFrame()

                group = QtWidgets.QGroupBox("Interior Pieces", interior)
                group.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)

                form = QtWidgets.QFormLayout()

                for piece in interior_pieces:
                    box = spinbox()
                    box.valueChanged.connect(partial(self.change_item_count,
                                                     interior_pieces[piece]))

                    self.material_mappings[box] = interior_pieces[piece]

                    form.addRow(piece, box)

                group.setLayout(form)

            class interior_modules:
                modules = QtWidgets.QFrame()

                group = QtWidgets.QGroupBox("Interior Modules", modules)
                group.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)

                form = QtWidgets.QFormLayout()

                for module in interior_mods:
                    box = spinbox()
                    box.valueChanged.connect(partial(self.change_item_count,
                                                     interior_mods[module]))

            self.base_pieces = base_pieces()
            self.power_pieces = power_pieces()
            self.interior_pieces = interior_pieces()

            materials.addWidget(self.base_pieces.buildings)
            materials.addWidget(self.power_pieces.power)
            materials.addWidget(self.interior_pieces.interior)

            material_frame.setLayout(materials)

        self.ui = ui()

    def connect_ui(self):
        self.ui.depth_slider.valueChanged.connect(self.change_background)
        self.ui.depth_slider.valueChanged.connect(self.change_depth)

    def apply_styles(self):
        font = QtGui.QFont("Roboto", 48)

        self.setStyleSheet(Assets.Scripts.main_window)

        self.ui.depth_slider.setStyleSheet(Assets.Scripts.slider)
        self.ui.depth_meter_label.setStyleSheet(Assets.Scripts.depth)
        self.ui.depth_meter_label.setFont(font)

        self.ui.depth_meter.setStyleSheet(Assets.Scripts.depth)
        self.ui.depth_meter.setFont(font)

    def change_background(self, depth: int):
        depth = -depth

        if depth <= 0:
            img = 0  # sky
        elif 0 < depth < 300:
            img = 1  # light sand
        elif 300 <= depth <= 550:
            img = 2  # dark sand
        elif 550 < depth < 950:
            img = 3  # green
        elif 950 <= depth <= 1650:
            img = 4
        else:
            img = 5

        self.ui.background.load(Assets.Images.backgrounds[img])

    def change_depth(self, depth: int):
        self.ui.depth_meter.setText(f"{-depth}m")

    def change_item_count(self, item: Item, count: int):
        print(item, count, sep=" | ")


@load_config("../config/config.yaml")
def main(config: dict[str, str | QtCore.QSize | QtGui.QIcon]):
    app = QtWidgets.QApplication(sys.argv)

    window_config = Config(
        config.get("size"),
        config.get("title"),
        config.get("icon"),
    )

    window = MainWindow(window_config)
    window.show()

    app.exec()


if __name__ == "__main__":
    main()
