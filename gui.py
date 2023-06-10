import tkinter as tk
from tkinter import ttk, messagebox

from data_visualizer import DataVisualizer
from esrb_model import ESRBModel
from rating import Category, Level, Type, Group, Rating, get_category_by_criteria

try:
    from ctypes import windll

    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

class GUI:

    def __init__(self, esrb_model: ESRBModel):
        self.esrb_model = esrb_model
        self.root = tk.Tk()
        self.category_state = {category: tk.IntVar(value=0) for category in Category}
        self.level_states = {level: tk.IntVar(value=0) for level in Level}
        self.type_states = {_type: tk.IntVar(value=0) for _type in Type}
        self.root.resizable(False, False)
        self.root.title("ESRB Predict")
        self.root.config(padx=10, pady=10)
        self.root.eval('tk::PlaceWindow . center')
        self.notebook = ttk.Notebook(self.root)
        self._set_violence_page(ttk.Frame(self.notebook, padding=5))
        self._set_sexual_page(ttk.Frame(self.notebook, padding=5))
        self._set_adult_language_page(ttk.Frame(self.notebook, padding=5))
        self._set_adult_content_page(ttk.Frame(self.notebook, padding=5))
        self._set_predict_page(ttk.Frame(self.notebook, padding=5))
        self._set_visuals_page(ttk.Frame(self.notebook, padding=5))
        self.combo_boxes = [self.blood_combobox, self.cartoon_violence_combobox, self.fantasy_violence_combobox,
                            self.language_combobox, self.lyrics_combobox, self.nudity_combobox,
                            self.sexual_content_combobox, self.suggest_themes_combobox,
                            self.use_of_drugs_alcohol_combobox, self.violence_combobox]
        self.check_buttons = [self.alcohol_reference_checkbutton, self.animated_blood_checkbutton,
                              self.crude_humor_checkbutton, self.drug_reference_checkbutton,
                              self.mature_humor_checkbutton, self.sexual_themes_checkbutton,
                              self.simulated_gambling_checkbutton]
        self.notebook.grid(padx=5, pady=10, sticky='NSEW')
        self.notebook.columnconfigure(0, weight=1)
        self.notebook.rowconfigure(0, weight=1)

        self.root.mainloop()

    def _set_adult_content_page(self, page):
        self.notebook.add(page, text=Type.CONTENT.description)
        self.alcohol_reference_checkbutton = self._create_category_line(page, row=0,
                                                                        category=Category.ALCOHOL_REFERENCE)
        self.drug_reference_checkbutton = self._create_category_line(page, row=1, category=Category.DRUG_REFERENCE)
        self.use_of_drugs_alcohol_combobox = self._create_category_line(page, row=2, group=Group.USE_OF_DRUG_ALCOHOL)
        self.simulated_gambling_checkbutton = self._create_category_line(page, row=3,
                                                                         category=Category.SIMULATED_GAMBLING)

    def _set_adult_language_page(self, page):
        self.notebook.add(page, text=Type.LANGUAGE.description)
        self.language_combobox = self._create_category_line(page, row=0, group=Group.LANGUAGE)
        self.lyrics_combobox = self._create_category_line(page, row=1, group=Group.LYRICS)
        self.crude_humor_checkbutton = self._create_category_line(page, row=2, category=Category.CRUDE_HUMOR)
        self.mature_humor_checkbutton = self._create_category_line(page, row=3, category=Category.MATURE_HUMOR)

    def _set_sexual_page(self, page):
        self.notebook.add(page, text=Type.SEXUAL.description)
        self.sexual_content_combobox = self._create_category_line(page, row=0, group=Group.SEXUAL)
        self.suggest_themes_combobox = self._create_category_line(page, row=1, group=Group.SUGGESTIVE_THEMES)
        self.nudity_combobox = self._create_category_line(page, row=2, group=Group.NUDITY)
        self.sexual_themes_checkbutton = self._create_category_line(page, row=3, category=Category.SEXUAL_THEMES)

    def _set_violence_page(self, page):
        self.notebook.add(page, text=Type.VIOLENCE.description)
        self.violence_combobox = self._create_category_line(page, row=0, group=Group.VIOLENCE)
        self.fantasy_violence_combobox = self._create_category_line(page, row=1, group=Group.FANTASY_VIOLENCE)
        self.cartoon_violence_combobox = self._create_category_line(page, row=2, group=Group.CARTOON_VIOLENCE)
        self.blood_combobox = self._create_category_line(page, row=3, group=Group.BLOOD)
        self.animated_blood_checkbutton = self._create_category_line(page, row=3, category=Category.ANIMATED_BLOOD)

    def _set_predict_page(self, page):
        predict_frame = ttk.Frame(page)
        predict_frame.pack(expand=True)
        self.reset_button = tk.Button(predict_frame, text='Reset Selections', command=self._reset_selections)
        self.reset_button.grid(row=0, column=0, pady=20)
        self.predict_button = tk.Button(predict_frame, text='Get Prediction', command=self._get_prediction)
        self.predict_button.grid(row=1, column=0, pady=20)
        self.notebook.add(page, text='Prediction')

    def _set_visuals_page(self, page):
        levels_frame = ttk.Labelframe(page, text='Levels')
        self.mild_level_checkbutton = tk.Checkbutton(levels_frame, text=Level.MILD.description,
                                                     variable=self.level_states[Level.MILD], onvalue=1, offvalue=0)
        self.mild_level_checkbutton.grid(row=0, column=1)
        self.average_level_checkbutton = tk.Checkbutton(levels_frame, text=Level.AVERAGE.description,
                                                        variable=self.level_states[Level.AVERAGE],
                                                        onvalue=1, offvalue=0)
        self.average_level_checkbutton.grid(row=0, column=2)
        self.extreme_level_checkbutton = tk.Checkbutton(levels_frame, text=Level.EXTREME.description,
                                                        variable=self.level_states[Level.EXTREME],
                                                        onvalue=1, offvalue=0)
        self.extreme_level_checkbutton.grid(row=0, column=3)
        levels_frame.grid(row=0, column=0, sticky='E', padx=10)

        type_frame = ttk.Labelframe(page, text='Types')
        self.content_type_checkbutton = tk.Checkbutton(type_frame, text=Type.CONTENT.description,
                                                       variable=self.type_states[Type.CONTENT], onvalue=1, offvalue=0)
        self.content_type_checkbutton.grid(row=0, column=1)
        self.language_type_checkbutton = tk.Checkbutton(type_frame, text=Type.LANGUAGE.description,
                                                       variable=self.type_states[Type.LANGUAGE], onvalue=1, offvalue=0)
        self.language_type_checkbutton.grid(row=0, column=2)
        self.sexual_type_checkbutton = tk.Checkbutton(type_frame, text=Type.SEXUAL.description,
                                                       variable=self.type_states[Type.SEXUAL], onvalue=1, offvalue=0)
        self.sexual_type_checkbutton.grid(row=0, column=3)
        self.violence_type_checkbutton = tk.Checkbutton(type_frame, text=Type.VIOLENCE.description,
                                                       variable=self.type_states[Type.VIOLENCE], onvalue=1, offvalue=0)
        self.violence_type_checkbutton.grid(row=0, column=4)
        type_frame.grid(row=1, column=0, sticky='E', padx=10)

        button_frame = ttk.Frame(page)
        self.confusion_matrix_button = tk.Button(button_frame, text='Confusion Matrix',
                                                 command=self._display_confusion_matrix)
        self.confusion_matrix_button.grid(sticky='EW', row=0, column=0)
        self.pie_chart_button = tk.Button(button_frame, text='Pie Chart', command=self._display_pie_chart)
        self.pie_chart_button.grid(sticky='EW', row=1, column=0)
        self.bar_chart_button = tk.Button(button_frame, text='Bar Chart', command=self._display_bar_chart)
        self.bar_chart_button.grid(sticky='EW', row=2, column=0)
        button_frame.grid(row=0, column=1, rowspan=2)
        self.notebook.add(page, text='Visuals')

    def _create_category_line(self, page, row, category=None, group=None):
        column = 0
        new_frame = ttk.Frame(page)
        new_frame.pack(anchor='w', expand=True)
        if group:
            values = [''] + list(group.group)
            ttk.Label(new_frame, text=str(group) + ':', padding=5).grid(row=row, column=column)
            combobox = ttk.Combobox(new_frame, values=values)
            column += 1
            combobox.grid(row=row, column=column, padx=5, sticky='EW')
            new_frame.columnconfigure(column, weight=1)
            combobox.columnconfigure(column, weight=1)
            combobox['state'] = 'readonly'
            combobox.__dict__['group'] = values
            combobox.bind('<<ComboboxSelected>>', self._set_combo_box_states)
            return combobox
        elif category:
            checkbutton = tk.Checkbutton(new_frame, text=category, variable=self.category_state[category],
                                         onvalue=1, offvalue=0)
            checkbutton.grid(row=row, column=column)
            return checkbutton

    def _set_combo_box_states(self, event):
        for combobox in self.combo_boxes:
            selected_value = combobox.current()
            for i, category in enumerate(combobox.__dict__['group']):
                if i == 0:
                    continue
                if selected_value == i and category:
                    self.category_state[category].set(1)
                else:
                    self.category_state[category].set(0)

    def _get_prediction(self):
        prediction_dict = {category.column: value.get() for category, value in self.category_state.items()}
        self.prediction = self.esrb_model.predict_rating(prediction_dict)
        rating = [rating for rating in Rating if rating.name == self.prediction][0]
        messagebox.showinfo('Predicted Rating', f'The predicted ESRB rating of this game based\non the selected options'
                                                f' is "{rating.name}" for "{rating.description}"')

    def _reset_selections(self):
        for checkbutton in self.check_buttons:
            checkbutton.deselect()
        for combobox in self.combo_boxes:
            combobox.current(0)
        for category, value in self.category_state.items():
            value.set(0)

    def _display_pie_chart(self):
        categories = self._get_visual_categories()
        if categories:
            DataVisualizer.get_pie_chart(self.esrb_model, categories, True)

    def _display_bar_chart(self):
        categories = self._get_visual_categories()
        if categories:
            DataVisualizer.get_bar_chart(self.esrb_model, categories, True)

    def _display_confusion_matrix(self):
        DataVisualizer.get_confusion_matrix(self.esrb_model)

    def _get_visual_categories(self):
        levels = [level for level, state in self.level_states.items() if state.get() == 1]
        content_types = [_type for _type, state in self.type_states.items() if state.get() == 1]
        return get_category_by_criteria(levels, content_types)
