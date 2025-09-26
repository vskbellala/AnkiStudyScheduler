# -*- coding: utf-8 -*-
# Filename: __init__.py
# Version: 1.0

"""
Anki Study Scheduler Addon
Calculates a study plan and can optionally apply the new card limit to a selected deck.
"""

from datetime import date, datetime, timedelta
import math
import traceback

# Anki and PyQt6 imports
from aqt import mw
from aqt.qt import (
    QAction,
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QGroupBox,
    QLabel,
    QRadioButton,
    QSpinBox,
    QDateEdit,
    QCheckBox,
    QPushButton,
    QTextEdit,
    QFrame,
    QDate,
    QComboBox,
    QMessageBox,
    Qt,
)
from aqt.utils import showInfo, showWarning, tooltip, openLink
from anki.hooks import addHook
from aqt.gui_hooks import deck_browser_will_show_options_menu, state_did_change

class SchedulerDialog(QDialog):
    """The main dialog window for the addon."""

    # Modified __init__ to accept a pre-selected deck_id
    def __init__(self, parent=None, deck_id=None):
        super().__init__(parent)
        self.preselected_deck_id = deck_id # Store the deck_id
        
        self.setWindowTitle("Anki Study Scheduler")
        self.setMinimumWidth(550)
        self.setup_ui()
        self.populate_deck_list()
        self.connect_signals()
        self.change_mode_callback()

        # If a deck was passed in, try to select it
        if self.preselected_deck_id:
            index = self.deck_selector.findData(self.preselected_deck_id)
            if index != -1:
                self.deck_selector.setCurrentIndex(index)


    def setup_ui(self):
        """Create and arrange all the UI widgets."""
        
        layout = QVBoxLayout(self)
        header_label = QLabel("Anki Study Scheduler")
        header_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #3c78c8;")
        sub_header_label = QLabel("Plan your study sessions and apply settings directly to your decks.")
        layout.addWidget(header_label)
        layout.addWidget(sub_header_label)

        line1 = QFrame()
        line1.setFrameShape(QFrame.Shape.HLine)
        line1.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line1)
        
        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        # ... (rest of the UI is the same as before) ...
        self.mode_group = QGroupBox()
        mode_layout = QHBoxLayout()
        self.radio_rate = QRadioButton("Calculate Daily Rate")
        self.radio_date = QRadioButton("Calculate End Date")
        self.radio_rate.setChecked(True)
        mode_layout.addWidget(self.radio_rate)
        mode_layout.addWidget(self.radio_date)
        self.mode_group.setLayout(mode_layout)
        form_layout.addRow("Calculation Mode:", self.mode_group)
        self.total_cards_input = QSpinBox()
        self.total_cards_input.setRange(1, 999999)
        self.total_cards_input.setValue(1000)
        form_layout.addRow("Total Cards to Study:", self.total_cards_input)
        self.duration_input = QSpinBox()
        self.duration_input.setRange(1, 9999)
        self.duration_input.setValue(30)
        self.duration_label = QLabel("Target Duration (days):")
        form_layout.addRow(self.duration_label, self.duration_input)
        self.rate_input = QSpinBox()
        self.rate_input.setRange(1, 9999)
        self.rate_input.setValue(20)
        self.rate_label = QLabel("Cards per Day:")
        form_layout.addRow(self.rate_label, self.rate_input)
        self.start_date_input = QDateEdit()
        self.start_date_input.setCalendarPopup(True)
        self.start_date_input.setDate(QDate.currentDate())
        self.start_date_input.setDisplayFormat("yyyy-MM-dd")
        form_layout.addRow("Start Date:", self.start_date_input)
        layout.addLayout(form_layout)
        line2 = QFrame()
        line2.setFrameShape(QFrame.Shape.HLine)
        line2.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line2)
        options_group_layout = QFormLayout()
        self.deck_selector = QComboBox()
        self.deck_selector_label = QLabel("Target Deck:")
        options_group_layout.addRow(self.deck_selector_label, self.deck_selector)
        self.apply_to_deck_checkbox = QCheckBox("Apply calculated rate to selected deck's 'New cards/day' limit")
        options_group_layout.addRow("", self.apply_to_deck_checkbox)
        self.weekends_checkbox = QCheckBox("Study on Weekends")
        self.weekends_checkbox.setChecked(True)
        options_group_layout.addRow("Schedule Options:", self.weekends_checkbox)
        self.verbose_checkbox = QCheckBox("Show Daily Schedule")
        options_group_layout.addRow("", self.verbose_checkbox)
        layout.addLayout(options_group_layout)
        layout.addSpacing(15)
        self.generate_button = QPushButton("Generate My Schedule")
        self.generate_button.setMinimumHeight(40)
        self.generate_button.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.generate_button)
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setPlaceholderText("Your custom schedule will appear here...")
        layout.addWidget(self.output_text)
        
        # --- NEW: Footer section ---
        footer_line = QFrame()
        footer_line.setFrameShape(QFrame.Shape.HLine)
        footer_line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(footer_line)
        
        footer_label = QLabel()
        
        # !!! IMPORTANT: REPLACE THIS URL WITH YOUR ACTUAL GITHUB REPO LINK !!!
        github_url = "https://github.com/vskbellala/AnkiStudyScheduler" # Example URL
        
        footer_text = f'Made by vskbellala with Gemini — <a href="{github_url}">View on GitHub</a>'
        footer_label.setText(footer_text)
        footer_label.setTextFormat(Qt.TextFormat.RichText)
        footer_label.setOpenExternalLinks(True) # Makes the link clickable
        footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(footer_label)

    # ... (the rest of the class methods are the same) ...

    def populate_deck_list(self):
        self.deck_selector.clear()
        try:
            decks = mw.col.decks.get_tree()
            def add_deck_node_to_selector(deck_node, level):
                prefix = "    " * level
                self.deck_selector.addItem(prefix + deck_node.name, deck_node.deck_id)
                for child in deck_node.children:
                    add_deck_node_to_selector(child, level + 1)
            for deck_node in decks.children:
                add_deck_node_to_selector(deck_node, 0)
        except AttributeError:
            names_and_ids = mw.col.decks.all_names_and_ids()
            for d in sorted(names_and_ids, key=lambda x: x.name.lower()):
                self.deck_selector.addItem(d.name, d.id)

    def connect_signals(self):
        self.radio_rate.toggled.connect(self.change_mode_callback)
        self.generate_button.clicked.connect(self.run_full_process)

    def change_mode_callback(self):
        is_rate_mode = self.radio_rate.isChecked()
        self.duration_label.setVisible(is_rate_mode)
        self.duration_input.setVisible(is_rate_mode)
        self.rate_label.setVisible(not is_rate_mode)
        self.rate_input.setVisible(not is_rate_mode)
        self.deck_selector_label.setVisible(is_rate_mode)
        self.deck_selector.setVisible(is_rate_mode)
        self.apply_to_deck_checkbox.setVisible(is_rate_mode)
        if not is_rate_mode:
            self.apply_to_deck_checkbox.setChecked(False)

    def run_full_process(self):
        calculated_rate = self.calculate_schedule()
        if calculated_rate is None: return
        if self.radio_rate.isChecked() and self.apply_to_deck_checkbox.isChecked():
            deck_id = self.deck_selector.currentData()
            deck_name = self.deck_selector.currentText().strip()
            if not deck_id:
                showWarning("No deck selected. Cannot apply settings.", parent=self)
                return
            self.confirm_and_apply_settings(deck_id, deck_name, calculated_rate)

    def confirm_and_apply_settings(self, deck_id, deck_name, new_limit):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Confirm Deck Update")
        msg_box.setText(f"Are you sure you want to change the 'New cards/day' limit for the deck <b>'{deck_name}'</b> to <b>{new_limit}</b>?")
        msg_box.setInformativeText("This will modify your deck's option group.")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)
        msg_box.setDefaultButton(QMessageBox.StandardButton.Cancel)
        reply = msg_box.exec()
        if reply == QMessageBox.StandardButton.Yes:
            self.apply_deck_settings(deck_id, deck_name, new_limit)

    def apply_deck_settings(self, deck_id, deck_name, new_limit):
        try:
            conf = mw.col.decks.config_dict_for_deck_id(deck_id)
            conf['new']['perDay'] = new_limit
            mw.col.decks.update_config(conf)
            deck = mw.col.decks.get(deck_id)
            deck['conf'] = conf['id']
            mw.col.decks.save(deck)
            mw.reset()
            tooltip(f"Deck '{deck_name}' updated successfully.", parent=self.parent())
            self.output_text.append(f"\n✅ Successfully set 'New cards/day' for deck '{deck_name}' to {new_limit}.")
        except Exception as e:
            traceback.print_exc()
            showWarning(f"Could not update deck settings. See console for details.\nError: {e}", parent=self)

    def calculate_schedule(self):
        try:
            total_cards = self.total_cards_input.value()
            start_date = self.start_date_input.date().toPyDate()
            study_on_weekends = self.weekends_checkbox.isChecked()
            verbose = self.verbose_checkbox.isChecked()
            output_summary, schedule_output, calculated_rate_for_deck = "", "", None
            if self.radio_rate.isChecked():
                num_days = self.duration_input.value()
                if num_days <= 0: raise ValueError("'Target Duration' must be positive.")
                study_days = num_days if study_on_weekends else sum(1 for i in range(num_days) if (start_date + timedelta(days=i)).weekday() < 5)
                if study_days <= 0: raise ValueError("No study days found in the selected duration.")
                per_day = math.ceil(total_cards / study_days)
                calculated_rate_for_deck = per_day
                total_cards_scheduled = per_day * study_days
                end_date, days_with_tasks_scheduled, temp_day_counter = start_date, 0, 0
                while days_with_tasks_scheduled < study_days and temp_day_counter < num_days:
                    current_day_offset = start_date + timedelta(days=temp_day_counter)
                    if study_on_weekends or current_day_offset.weekday() < 5:
                        if verbose: schedule_output += f"{current_day_offset.strftime('%Y-%m-%d (%a)')} — {per_day} cards\n"
                        days_with_tasks_scheduled += 1
                        end_date = current_day_offset
                    temp_day_counter += 1
                output_summary = (f"--- MODE: CALCULATE DAILY RATE ---\nRequired pace: {per_day} cards/day\nTotal study days: {study_days}\nCalculated End Date: {end_date.strftime('%Y-%m-%d (%a)')}\nTotal cards scheduled: {total_cards_scheduled} (of {total_cards})\n")
            else:
                cards_per_day = self.rate_input.value()
                if cards_per_day <= 0: raise ValueError("'Cards per Day' must be positive.")
                study_days_needed = math.ceil(total_cards / cards_per_day) if total_cards > 0 else 0
                end_date = start_date
                if study_days_needed > 0:
                    days_with_tasks_scheduled, day_offset = 0, 0
                    while days_with_tasks_scheduled < study_days_needed:
                        current_day_offset = start_date + timedelta(days=day_offset)
                        if study_on_weekends or current_day_offset.weekday() < 5:
                            if verbose: schedule_output += f"{current_day_offset.strftime('%Y-%m-%d (%a)')} — {cards_per_day} cards\n"
                            days_with_tasks_scheduled += 1
                            end_date = current_day_offset
                        day_offset += 1
                else: end_date = start_date - timedelta(days=1)
                calendar_days = (end_date - start_date).days + 1 if study_days_needed > 0 else 0
                output_summary = (f"--- MODE: CALCULATE END DATE ---\nTarget pace: {cards_per_day} cards/day\nTotal study days needed: {study_days_needed}\nYou will finish on: {end_date.strftime('%Y-%m-%d (%a)')}\nTotal calendar time: {calendar_days} days\n")
            final_output = output_summary
            if verbose and schedule_output: final_output += "\nDaily Schedule:\n" + schedule_output
            self.output_text.setPlainText(final_output)
            return calculated_rate_for_deck
        except Exception as e:
            self.output_text.setPlainText(f"❌ Error: {e}\n\nPlease check your inputs.")
            return None

# --- Anki Integration ---

# Function to open the dialog, now accepts an optional deck_id
def open_scheduler_dialog(deck_id=None):
    dialog = SchedulerDialog(mw, deck_id=deck_id)
    dialog.exec()

# Original menu item in "Tools"
tools_action = QAction("Study Scheduler...", mw)
tools_action.triggered.connect(lambda: open_scheduler_dialog())
mw.form.menuTools.addAction(tools_action)


# --- NEW: Deck Gear Icon Integration ---
def add_scheduler_to_deck_menu(menu, deck_id):
    """Adds a menu item to the deck's gear icon menu."""
    action = menu.addAction("Create Study Schedule...")
    action.triggered.connect(lambda: open_scheduler_dialog(deck_id))

# Use a hook to add our function to the gear menu
# addHook("deck_browser_will_show_options_menu", add_scheduler_to_deck_menu)
deck_browser_will_show_options_menu.append(add_scheduler_to_deck_menu)