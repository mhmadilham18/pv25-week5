from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QRadioButton, QComboBox, QGroupBox,
    QMessageBox, QGridLayout, QTextEdit, QShortcut
)
from PyQt5.QtGui import QIcon, QPixmap, QIntValidator, QRegExpValidator, QKeySequence
from PyQt5.QtCore import QRegExp
import sys
import re


class RegistrationForm(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Initialize main UI window
        self.setWindowTitle("Form")
        self.setGeometry(800, 200, 600, 750)
        self.setWindowIcon(QIcon("asset/icon-app.svg"))  # set icon

        # Define color scheme
        self.primary_color = "#bca47f"
        self.secondary_color = "#56021F"
        self.accent_color = "#A9B5DF"

        # Create shortcut to close app with Q key
        self.close_shortcut = QShortcut(QKeySequence('Q'), self)
        self.close_shortcut.activated.connect(self.close)

        # Create main layout
        main_layout = QVBoxLayout()

        # Add identity section
        info_label = QLabel("Identitas Pribadi")
        info_label.setStyleSheet(
            f"font-weight: bold; margin-bottom: 16px; font-size: 28px; color: {self.secondary_color};")
        main_layout.addWidget(info_label)
        main_layout.addWidget(self.create_identity_section())

        # Add navigation section
        nav_label = QLabel("Navigasi")
        nav_label.setStyleSheet(
            f"font-weight: bold; margin-top:16px; margin-bottom: 16px; font-size: 28px; color: {self.secondary_color};")
        main_layout.addWidget(nav_label)
        main_layout.addLayout(self.create_navigation_bar())

        # Add registration form section
        regis_label = QLabel("Form Registrasi")
        regis_label.setStyleSheet(
            f"font-weight: bold; margin-top:16px; margin-bottom: 16px; font-size: 28px; color: {self.secondary_color};")
        main_layout.addWidget(regis_label)
        main_layout.addWidget(self.create_registration_form())

        # Add action buttons
        main_layout.addLayout(self.create_action_buttons())

        # Set main layout
        self.setLayout(main_layout)

    def create_identity_section(self):
        # Create identity group box
        identity_group = QGroupBox(" ")
        layout = QGridLayout()

        # Set background style
        identity_group.setStyleSheet(f"""
                QGroupBox {{
                    background-color: white;
                    border: 1px solid {self.primary_color}; 
                    border-radius: 5px;
                    padding: 16px;
                }}
            """)

        # Data identitas
        icons = [
            "asset/user-name.svg",
            "asset/key-identifier.svg",
            "asset/class-home.svg",
            "asset/state-current.svg"
        ]
        values = [
            "M. Ilham Abdul Shaleh",
            "F1D022061",
            "Kelas D",
            "Semester 6"
        ]

        # Add each identity row with icon and text
        for i, (icon_path, value) in enumerate(zip(icons, values)):
            icon_label = QLabel()
            icon_pixmap = QPixmap(icon_path).scaled(28, 28, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            icon_label.setPixmap(icon_pixmap)

            text_label = QLabel(f":  {value}")
            text_label.setAlignment(Qt.AlignLeft)
            text_label.setStyleSheet("font-size: 20px;")

            row_layout = QHBoxLayout()
            row_layout.addWidget(icon_label)
            row_layout.addWidget(text_label)
            row_layout.addStretch()

            layout.addLayout(row_layout, i, 0)

        identity_group.setLayout(layout)
        return identity_group

    def create_navigation_bar(self):
        # Create navigation layout
        nav_layout = QHBoxLayout()

        # Create Home button with outline to indicate current page
        home_button = QPushButton("Home")
        home_button.setStyleSheet(f"""
            QPushButton {{
                border: 2px solid {self.accent_color};
                border-radius: 5px;
                padding: 12px;
                background-color: #f0f8ff;
                font-size: 20px;
                color: {self.primary_color};
            }}
        """)

        # Create other navigation buttons
        profile_button = QPushButton("Profile")
        profile_button.setStyleSheet(f"font-size: 20px; padding: 12px; color: {self.primary_color};")
        profile_button.clicked.connect(lambda: self.show_under_development_message("Profile"))

        settings_button = QPushButton("Settings")
        settings_button.setStyleSheet(f"font-size: 20px; padding: 12px; color: {self.primary_color};")
        settings_button.clicked.connect(lambda: self.show_under_development_message("Settings"))

        # Add buttons to navigation layout
        nav_layout.addWidget(home_button)
        nav_layout.addWidget(profile_button)
        nav_layout.addWidget(settings_button)

        return nav_layout

    def show_under_development_message(self, feature_name):
        # Show message for features under development
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Dalam Pengembangan")
        msg_box.setText(f"Fitur {feature_name} sedang dalam pengembangan.")
        msg_box.setWindowIcon(QIcon("asset/alert-pop-up.svg"))
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

    def create_registration_form(self):
        # Create form group box
        form_group = QGroupBox(" ")
        layout = QVBoxLayout()

        # Set form group style
        form_group.setStyleSheet(f"""
                QGroupBox {{
                    background-color: white;
                    border: 1px solid {self.primary_color}; 
                    border-radius: 5px;
                    padding: 16px;
                    margin-bottom: 24px;
                }}
            """)

        # Define input style with larger font size and custom colors
        input_style = f"""
            QLineEdit, QComboBox, QTextEdit {{
                border: 1px solid {self.primary_color};
                border-radius: 5px;
                padding: 12px;
                font-size: 20px;
                font-family: Arial;
                min-width: 300px;
                color: {self.secondary_color};
            }}

            QLineEdit:focus, QComboBox:focus, QTextEdit:focus {{
                border: 2px solid {self.accent_color};
            }}

            QComboBox::drop-down {{
                border: 0px;
            }}

            QComboBox::down-arrow {{
                width: 18px;
                height: 18px;
            }}
        """

        # Create text label with input field
        def create_labeled_input(label_text, placeholder):
            container = QHBoxLayout()
            container.setSpacing(16)

            # Create label
            text_label = QLabel(label_text)
            text_label.setStyleSheet(f"font-size: 18px; min-width: 150px; color: {self.secondary_color};")

            # Create input field
            input_field = QLineEdit()
            input_field.setPlaceholderText(placeholder)
            input_field.setStyleSheet(input_style)

            container.addWidget(text_label)
            container.addWidget(input_field)

            return container, input_field

        # Name field
        name_layout, self.input_full_name = create_labeled_input("Nama:", "Masukkan nama lengkap Anda")

        # Email field with validation
        email_layout, self.input_email = create_labeled_input("Email:", "Masukkan email Anda")

        # Age field with numeric validation
        age_layout, self.input_age = create_labeled_input("Umur:", "Masukkan umur Anda")
        self.input_age.setValidator(QIntValidator(1, 120))

        # Phone number with input mask
        phone_layout, self.input_phone = create_labeled_input("Telepon:", "+62 ___ ____ ____")
        self.input_phone.setInputMask("+62 999 9999 9999;_")


        # Address field (TextEdit for multiline)
        address_container = QHBoxLayout()
        address_label = QLabel("Alamat:")
        address_label.setStyleSheet(f"font-size: 20px; min-width: 150px; color: {self.secondary_color};")

        self.input_address = QTextEdit()
        self.input_address.setPlaceholderText("Masukkan alamat lengkap Anda")
        self.input_address.setStyleSheet(input_style)
        self.input_address.setMaximumHeight(220)

        address_container.addWidget(address_label)
        address_container.addWidget(self.input_address)

               # Gender and Education in one row
        gender_edu_container = QHBoxLayout()

        # Gender section
        gender_box = QVBoxLayout()
        gender_label = QLabel("Jenis Kelamin:")
        gender_label.setStyleSheet(f"font-size: 20px; color: {self.secondary_color};")

        self.dropdown_gender = QComboBox()
        self.dropdown_gender.setStyleSheet(input_style)
        gender_options = ["Pilih Gender", "Laki-laki", "Perempuan"]
        self.dropdown_gender.addItems(gender_options)

        gender_box.addWidget(gender_label)
        gender_box.addWidget(self.dropdown_gender)

        # Education section
        education_box = QVBoxLayout()
        education_label = QLabel("Pendidikan:")
        education_label.setStyleSheet(f"font-size: 20px; color: {self.secondary_color};")

        self.dropdown_education = QComboBox()
        self.dropdown_education.setStyleSheet(input_style)
        education_options = ["Pilih Pendidikan", "SD", "SMP", "SMA/SMK", "D3", "S1", "S2", "S3"]
        self.dropdown_education.addItems(education_options)

        education_box.addWidget(education_label)
        education_box.addWidget(self.dropdown_education)

        # Add both to the container
        gender_edu_container.addLayout(gender_box)
        gender_edu_container.addLayout(education_box)

        # Add spacers between sections
        layout.addLayout(name_layout)
        layout.addSpacing(16)
        layout.addLayout(email_layout)
        layout.addSpacing(16)
        layout.addLayout(age_layout)
        layout.addSpacing(16)
        layout.addLayout(phone_layout)
        layout.addSpacing(16)
        layout.addLayout(address_container)
        layout.addSpacing(16)
        layout.addLayout(gender_edu_container)

        form_group.setLayout(layout)
        return form_group

    def create_action_buttons(self):
        # Create layout for action buttons
        button_layout = QHBoxLayout()

        # Create save button
        self.btn_submit = QPushButton("Simpan Data")
        self.btn_submit.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.primary_color};
                color: white;
                border-radius: 5px;
                padding: 18px 24px;
                font-size: 20px;
            }}
            QPushButton:hover {{
                background-color: #a89060;
            }}
        """)

        # Create clear button
        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.secondary_color};
                color: white;
                border-radius: 5px;
                padding: 18px 24px;
                font-size: 20px;
            }}
            QPushButton:hover {{
                background-color: #450219;
            }}
        """)

        # Connect button signals to handler functions
        self.btn_submit.clicked.connect(self.handle_submit)
        self.btn_cancel.clicked.connect(self.handle_clear_form)

        # Add spacer to push buttons to the right
        button_layout.addStretch()

        # Add buttons to layout
        button_layout.addWidget(self.btn_submit)
        button_layout.addWidget(self.btn_cancel)

        return button_layout

    def validate_email(self, email):
        # Validate email format using regex
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def validate_phone(self, phone):
        # Validate phone number format
        pattern = r'^\+62 \d{3} \d{4} \d{4}$'
        return re.match(pattern, phone) is not None

    def handle_submit(self):
        # Get all form values
        name = self.input_full_name.text()
        email = self.input_email.text()
        age = self.input_age.text()
        phone = self.input_phone.text()
        address = self.input_address.toPlainText()
        gender = self.dropdown_gender.currentText()
        education = self.dropdown_education.currentText()


        # Validation errors list
        errors = []

        # Validate required fields
        if not name:
            errors.append("⚠ Nama tidak boleh kosong")
        elif len(name) < 3:
            errors.append("⚠ Nama harus terdiri dari minimal 3 karakter")

        if not self.validate_email(email):
            errors.append("⚠ Format email tidak valid")

        if age and not age.isdigit():
            errors.append("⚠ Umur harus berupa angka")

        if not self.validate_phone(phone):
            errors.append("⚠ Nomor telepon harus sesuai format +62 XXX XXXX XXXX")

        if not address:
            errors.append("⚠ Alamat tidak boleh kosong")

        if gender == "Pilih Gender":
            errors.append("⚠ Jenis kelamin harus dipilih")

        if education == "Pilih Pendidikan":
            errors.append("⚠ Pendidikan harus dipilih")

        # Show error message if any validation fails
        if errors:
            msg_box = QMessageBox()
            msg_box.setWindowIcon(QIcon("asset/alert-pop-up.svg"))
            msg_box.setWindowTitle("Validasi Gagal")
            msg_box.setText("Mohon perbaiki error berikut:")
            msg_box.setInformativeText("\n".join(errors))
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.exec_()
            return

        # If validation passes, show success message
        msg_box = QMessageBox()
        msg_box.setWindowIcon(QIcon("asset/info.svg"))
        msg_box.setWindowTitle("Pendaftaran Berhasil")
        msg_box.setText(
            f"Data {name} berhasil disimpan"
        )
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

        # Clear all fields on success
        self.clear_all_fields()

    def clear_all_fields(self):
        # Clear all input fields
        self.input_full_name.clear()
        self.input_email.clear()
        self.input_age.clear()
        self.input_phone.setText("+62 ")
        self.input_address.clear()
        self.dropdown_gender.setCurrentIndex(0)
        self.dropdown_education.setCurrentIndex(0)


    def handle_clear_form(self):
        # Ask for confirmation before clearing
        msg_box = QMessageBox()
        msg_box.setWindowIcon(QIcon("asset/ask.svg"))
        msg_box.setWindowTitle("Batalkan Pengisian")
        msg_box.setText("Apakah Anda yakin ingin membersihkan semua isian formulir?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)

        if msg_box.exec_() == QMessageBox.Yes:
            self.clear_all_fields()


if __name__ == "__main__":
    # Create and run application
    app = QApplication(sys.argv)
    window = RegistrationForm()
    window.show()
    sys.exit(app.exec_())