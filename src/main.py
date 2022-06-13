import os
import sys
from functools import partial

from PyQt6 import QtCore, QtGui, QtSvgWidgets, QtWidgets

from assets import Assets, Config, load_assets, load_config
from subnautica import (Item, Material, base_pieces, depths, interior_modules,
                        interior_pieces, power_sources)


os.chdir(os.path.normpath(f"{__file__}/../"))


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
        self.selected_materials: dict[Material, int] = {}

        self._prev_image = -1

        self.setup_ui()
        self.connect_ui()
        self.apply_styles()

    def setup_ui(self):
        def spinbox() -> QtWidgets.QSpinBox:
            box = QtWidgets.QSpinBox()
            box.setMinimum(0)
            box.setFont(QtGui.QFont("Roboto", 18))
            box.setStyleSheet(Assets.Scripts.spinbox)

            return box

        def material_section(name: str, source: list[str]) -> QtWidgets.QFrame:
            frame = QtWidgets.QFrame()

            group = QtWidgets.QGroupBox(name, frame)
            group.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)

            form = QtWidgets.QFormLayout()

            for data in source:
                box = spinbox()
                box.valueChanged.connect(partial(self.change_item_count,
                                                 source[data]))

                self.material_mappings[box] = source[data]

                form.addRow(data, box)

            group.setLayout(form)

            return frame

        class ui:  # noqa NOSONAR
            background = QtSvgWidgets.QSvgWidget(
                Assets.Images.backgrounds[self.loaded_image], self
            )
            background.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
            self.setCentralWidget(background)

            depth_slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Vertical,
                                             self)
            depth_slider.setGeometry(1780, 40, 100, 1000)
            depth_slider.setMinimum(-2000)
            depth_slider.setMaximum(0)

            depth_meter_label = QtWidgets.QLabel("Depth:", self)
            depth_meter_label.setGeometry(1520, 40, 240, 80)
            depth_meter_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            depth_meter = QtWidgets.QLabel("0m", self)
            depth_meter.setGeometry(1520, 140, 240, 80)
            depth_meter.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            struct_int_label = QtWidgets.QLabel("Integrity:", self)
            struct_int_label.setGeometry(1480, 240, 280, 80)
            struct_int_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            struct_int = QtWidgets.QLabel("0m", self)
            struct_int.setGeometry(1520, 140, 240, 80)
            struct_int.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            #####

            materials_button = QtWidgets.QLabel("Materials", self)
            materials_button.setGeometry(1540, 1035, 220, 75)

            #####

            material_frame = QtWidgets.QFrame(self)
            material_frame.setGeometry(50, 50, 800, 800)
            # material_frame.setStyleSheet()

            materials = QtWidgets.QHBoxLayout()

            vbox_frame = QtWidgets.QFrame()
            vbox = QtWidgets.QVBoxLayout(vbox_frame)

            spacer = QtWidgets.QLabel() 

            widgets = []

            vbox.addWidget(material_section("Power Pieces",
                                            source=power_sources))
            vbox.addWidget(material_section("Interior Pieces",
                                            source=interior_pieces))
            vbox.addWidget(spacer)

            widgets.append(material_section("Base Pieces",
                                            source=base_pieces))
            widgets.append(vbox_frame)
            widgets.append(material_section("Interior Modules",
                                            source=interior_modules))

            for widget in widgets:
                materials.addWidget(widget)

            material_frame.setLayout(materials)

        self.ui = ui()

    def connect_ui(self):
        self.ui.depth_slider.valueChanged.connect(self.change_background)
        self.ui.depth_slider.valueChanged.connect(self.change_depth)
        self.ui.depth_slider.valueChanged.connect(self.change_struct_integrity)

    def apply_styles(self):
        font = QtGui.QFont("Roboto", 48)

        self.setStyleSheet(Assets.Scripts.main_window)

        self.ui.depth_slider.setStyleSheet(Assets.Scripts.slider)

        self.ui.depth_meter_label.setStyleSheet(Assets.Scripts.depth)
        self.ui.depth_meter_label.setFont(font)

        self.ui.struct_int_label.setFont(font)
        self.ui.struct_int_label.setStyleSheet(Assets.Scripts.depth)

        self.ui.depth_meter.setStyleSheet(Assets.Scripts.depth)
        self.ui.depth_meter.setFont(font)

    def change_background(self, depth: int):
        depth = abs(depth)

        img = depths[list(filter(lambda d: depth in d, list(depths)))[0]]

        if self._prev_image == img:
            return

        self._prev_image = img

        self.ui.background.load(Assets.Images.backgrounds[img])

    def change_depth(self, depth: int):
        self.ui.depth_meter.setText(f"{-depth}m")

    def change_struct_integrity(self, depth: int):
        depth = -depth

    def change_item_count(self, item: Item, count: int):
        self.selected_materials[item] = count


@load_config("../config/config.yaml")
def main(config: dict[str, str | QtCore.QSize | QtGui.QIcon]) -> None:
    load_assets()

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
