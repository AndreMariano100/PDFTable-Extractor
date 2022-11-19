import tkinter as tk
import tkinter.ttk as ttk
from ttkbootstrap import Style
from tkinter.filedialog import askopenfilename, asksaveasfilename
import compoundwidgets as cw

import fitz
import os
import json
from threading import Thread
import pandas
from pdf_extraction_methods import read_pdf_table


class ASMEPdfExtract(tk.Tk):
    """ Main application window"""

    def __init__(self):

        # Window configuration
        if True:
            super().__init__()
            self.style = Style(theme='darkly')
            self.path = os.getcwd()
            self.iconbitmap(os.path.join(self.path, 'petrobras.ico'))
            self.title('ASME PDF Extract Tool')

            window_width = 800
            window_height = 600
            self.minsize(window_width, window_height)
            self.resizable(True, True)
            self.geometry(self.screen_position(self))

            self.protocol("WM_DELETE_WINDOW", self.finish)

            self.columnconfigure(0, weight=0, minsize=400)
            self.columnconfigure(1, weight=1, minsize=100)
            self.rowconfigure(0, weight=1)

        # Left and right frames
        if True:
            left_frame = ttk.Frame(self, padding=10)
            left_frame.grid(row=0, column=0, sticky='nsew')
            left_frame.columnconfigure(0, weight=1)
            left_frame.rowconfigure(3, weight=1)

            self.right_frame = ttk.Frame(self, padding=10)
            self.right_frame.grid(row=0, column=1, sticky='nsew')
            self.right_frame.columnconfigure(0, weight=1)
            self.right_frame.rowconfigure(0, weight=1)

        # Left frame - open pdf and navigation
        if True:
            local_frame = ttk.LabelFrame(left_frame, text='PDF File Selection', padding=10)
            local_frame.grid(row=0, column=0, sticky='nsew')
            local_frame.columnconfigure(0, weight=1)
            local_frame.rowconfigure(0, weight=1)
            local_frame.rowconfigure(1, weight=1)
            local_frame.rowconfigure(2, weight=1)

            widget = ttk.Button(local_frame, text='Select PDF file', command=self.select_pdf_file)
            widget.grid(row=0, column=0, columnspan=2, sticky='nsew')

            self.pdf_page_var = tk.IntVar(value=0)
            self.pdf_page_widget = ttk.Spinbox(local_frame, from_=1, to=0, increment=1, width=6, state='disabled',
                                               command=self.spin_box_selected, textvariable=self.pdf_page_var,
                                               justify='center')
            self.pdf_page_widget.grid(row=1, column=1, sticky='nsew', pady=(5, 0), padx=(5, 0))
            self.pdf_page_widget.bind('<Return>', self.pdf_page_selected)
            self.pdf_page_widget.bind('<FocusOut>', self.pdf_page_selected)

            widget = ttk.Label(local_frame, text='Select PDF Page:', anchor='e')
            widget.grid(row=1, column=0, sticky='nsew', pady=(5, 0))

            self.pdf_page_label = ttk.Label(local_frame, text='', anchor='e', style='secondary.TLabel')
            self.pdf_page_label.grid(row=2, column=0, columnspan=2, sticky='nsew', pady=(5, 0))

        # Left frame - pdf page range
        if True:
            self.page_range_select_frame = ttk.LabelFrame(left_frame, text='Pages Range Selection', padding=10)
            self.page_range_select_frame.grid(row=1, column=0, sticky='nsew', pady=(5, 0))
            self.page_range_select_frame.columnconfigure(0, weight=1)
            self.page_range_select_frame.columnconfigure(1, weight=1)
            self.page_range_select_frame.rowconfigure(0, weight=1)
            self.page_range_select_frame.rowconfigure(1, weight=0)
            self.page_range_select_frame.grid_remove()

            self.start_page = cw.LabelEntry(self.page_range_select_frame, label_text='Start Page:', entry_value=1,
                                            entry_numeric=True, entry_width=6, entry_method=self.range_selected)
            self.start_page.grid(row=0, column=0, sticky='nsew')

            self.end_page = cw.LabelEntry(self.page_range_select_frame, label_text='End Page:', entry_value=1,
                                          entry_numeric=True, entry_width=6, entry_method=self.range_selected)
            self.end_page.grid(row=0, column=1, sticky='nsew', padx=(5, 0))

            self.page_range_label = ttk.Label(self.page_range_select_frame, text='', anchor='e',
                                              style='secondary.TLabel')
            self.page_range_label.grid(row=1, column=0, columnspan=2, sticky='nsew', pady=(5, 0))

        # Left frame - table number of pages
        if True:
            self.table_data_frame = ttk.LabelFrame(left_frame, text='Table Number of Pages', padding=10)
            self.table_data_frame.grid(row=2, column=0, sticky='nsew', pady=(5, 0))
            self.table_data_frame.columnconfigure(0, weight=1)
            self.table_data_frame.columnconfigure(1, weight=1)
            self.table_data_frame.rowconfigure(0, weight=1)
            self.table_data_frame.rowconfigure(1, weight=1)
            self.table_data_frame.grid_remove()

            self.pages_per_table = cw.LabelEntry(self.table_data_frame, label_text='Pages per Table:', entry_value=1,
                                                 entry_numeric=True, entry_width=6,
                                                 entry_method=self.pages_per_table_selected)
            self.pages_per_table.grid(row=0, column=0, sticky='nsew')

            self.pages_to_skip = cw.LabelEntry(self.table_data_frame, label_text='Pages to skip:', entry_value=0,
                                               entry_numeric=True, entry_width=6,
                                               entry_method=self.pages_per_table_selected)
            self.pages_to_skip.grid(row=0, column=1, sticky='nsew')

            self.pages_per_table_label = ttk.Label(self.table_data_frame, text='', anchor='e',
                                                   style='secondary.TLabel')
            self.pages_per_table_label.grid(row=1, column=0, columnspan=2, sticky='nsew', pady=(5, 0))

        # Left frame - table configuration
        if True:
            self.border_configuration_frame = ttk.LabelFrame(left_frame, text='Borders Configuration', padding=10)
            self.border_configuration_frame.grid(row=3, column=0, sticky='nsew', pady=(5, 0))
            self.border_configuration_frame.columnconfigure(0, weight=1)
            self.border_configuration_frame.grid_remove()

            # Navigation buttons
            if True:
                local_frame = ttk.Frame(self.border_configuration_frame)
                local_frame.grid(row=0, column=0, sticky='nsew', pady=(0, 5))
                local_frame.columnconfigure(1, weight=1)
                local_frame.rowconfigure(0, weight=1)

                self.previous_border_button = ttk.Button(local_frame, text='<<', command=self.previous_border)
                self.previous_border_button.grid(row=0, column=0, sticky='nsew')

                self.next_border_button = ttk.Button(local_frame, text='>>', command=self.next_border)
                self.next_border_button.grid(row=0, column=2, sticky='nsew')

                self.border_name = ttk.Label(local_frame, text='Type 1 Border', style='secondary.Inverse.TLabel',
                                             anchor='center')
                self.border_name.grid(row=0, column=1, sticky='nsew')

            # External borders data
            if True:
                self.borders_data_frame = ttk.Frame(self.border_configuration_frame)
                self.borders_data_frame.grid(row=1, column=0, sticky='nsew')
                self.borders_data_frame.columnconfigure(0, weight=1)
                self.borders_data_frame.columnconfigure(1, weight=1)

                labels = ('Top Border', 'Bottom Border', 'Left Border', 'Right Border')
                self.borders_widgets = []
                for i, text in enumerate(labels):
                    widget = cw.LabelSpinbox(self.borders_data_frame, label_text=f'{text}:', spin_start=0,
                                             spin_end=10, spin_increment=1, entry_method=self.read_border_values,
                                             entry_width=4, spin_precision=0)
                    widget.grid(row=i // 2, column=i % 2, sticky='nsew', pady=2)
                    widget.spin.bind("<ButtonRelease-1>", self.read_border_values, add='+')
                    self.borders_widgets.append(widget)

                widget = cw.LabelSpinbox(self.borders_data_frame, label_text=f'Number of Columns:', spin_start=1,
                                         spin_end=20, spin_increment=1, entry_method=self.read_border_values,
                                         entry_width=4, spin_precision=0)
                widget.grid(row=2, column=0, columnspan=2,  sticky='nsew', pady=2)
                widget.spin.bind("<ButtonRelease-1>", self.read_border_values, add='+')
                self.borders_widgets.append(widget)

            # Internal borders data
            if True:
                for i in range(20):
                    widget = cw.LabelSpinbox(self.borders_data_frame, label_text=f'Column {i+1} End:', spin_start=0,
                                             spin_end=10, spin_increment=1, entry_method=self.read_border_values,
                                             entry_width=4, spin_precision=0)
                    widget.grid(row=i // 2 + 3, column=i % 2, sticky='nsew', pady=1)
                    widget.spin.bind("<ButtonRelease-1>", self.read_border_values, add='+')
                    self.borders_widgets.append(widget)
                    widget.grid_remove()

        # Left frame - buttons
        if True:
            self.buttons_frame = ttk.Frame(left_frame)
            self.buttons_frame.grid(row=4, column=0, sticky='nsew', pady=(5, 0))
            self.buttons_frame.rowconfigure(0, weight=1)
            for i in range(4):
                self.buttons_frame.columnconfigure(i, weight=1)
            self.buttons_frame.grid_remove()

            button = ttk.Button(self.buttons_frame, text='Load Table Data', command=self.load_table_data)
            button.grid(row=0, column=0, sticky='nsew', pady=(5, 0))
            button = ttk.Button(self.buttons_frame, text='Clear Table Data', command=self.clear_table_data)
            button.grid(row=0, column=1, sticky='nsew', pady=(5, 0), padx=(2, 0))
            button = ttk.Button(self.buttons_frame, text='Save Table Data', command=self.save_table_data)
            button.grid(row=0, column=2, sticky='nsew', pady=(5, 0), padx=(2, 0))
            button = ttk.Button(self.buttons_frame, text='Extract Table', command=self.extract_table)
            button.grid(row=0, column=3, sticky='nsew', pady=(5, 0), padx=(2, 0))

        # Right frame - canvas to show the pdf pages
        if True:
            self.pdf_canvas = tk.Canvas(self.right_frame, borderwidth=0, highlightthickness=0)
            self.pdf_canvas.grid(row=0, column=0, sticky='nsew')
            self.pdf_canvas.configure(bg=self.style.colors.dark)
            self.pdf_canvas.bind("<MouseWheel>", self.pdf_page_scroll)
            self._drag_data = {"x": 0, "y": 0, "item": None}
            self.pdf_canvas.tag_bind('draggable', "<ButtonPress-1>", self.check_draggable)
            self.pdf_canvas.tag_bind('draggable', "<ButtonRelease-1>", self.drag_stop)
            self.pdf_canvas.tag_bind('draggable', "<B1-Motion>", self.drag)

        # Attributes
        if True:
            self.pdf_file_name = ''                 # PDF file location
            self.pdf_file_images = []               # List with all the pdf pages in a byte format
            self.number_of_models = 1               # number of border models
            self.border_values_dict = {}            # dictionary with the border values (not actual position)
            self.header_dict = {}                   # dictionary for the table headers
            self.border_labels_list = \
                ['Type 1 Border']                   # list of the border labels including skip pages
            pandas.set_option("display.max_rows", None, "display.max_columns", None)

    # PDF File Selection -----------------------------------------------------------------------------------------------
    def select_pdf_file(self):
        """ Retrieves the full path for the PDF file """

        try:
            desktop = os.path.normpath(os.path.expanduser("~/Desktop"))
            file_name = askopenfilename(initialdir=desktop, title="Select File",
                                        filetypes=(("PDF files", "*.pdf"),
                                                   ("All files", "*.*")))
        except IOError or FileNotFoundError:
            return
        else:
            if not file_name:
                return

            self.pdf_file_name = file_name
            t1 = Thread(target=self.load_pdf_file)
            t1.start()

    def load_pdf_file(self):
        """ Opens the PDF file and saves the images to a list """

        self.pdf_file_images.clear()
        self.number_of_models = 1
        self.border_values_dict.clear()

        open_pdf = fitz.open(self.pdf_file_name)
        total = len(open_pdf)

        progress_bar = cw.ProgressBar(self, message='Reading PDF file...', final_value=total)

        # Resolution matrix
        zoom = 1.0
        mat = fitz.Matrix(zoom, zoom)

        for i, page in enumerate(open_pdf):
            progress_bar.update_bar(i)
            pix = page.get_pixmap(matrix=mat)
            pix1 = fitz.Pixmap(pix, 0) if pix.alpha else pix
            img = pix1.tobytes("ppm")
            timg = tk.PhotoImage(data=img)
            self.pdf_file_images.append(timg)

        progress_bar.destroy()
        open_pdf.close()
        self.adjust_widgets()

    def adjust_widgets(self):
        """ Adjusts the widgets once the PDF file was read """

        # Adjust PDF page selection widgets
        total = len(self.pdf_file_images)
        self.pdf_page_widget.configure(state='enable', from_=1, to=total)
        self.pdf_page_var.set(1)
        self.pdf_page_selected()
        text = f'File Name: {os.path.split(self.pdf_file_name)[1]} ({total} pages)'
        self.pdf_page_label.config(text=text)

        # Adjust the page range selection widgets
        self.page_range_select_frame.grid()
        self.start_page.set(1)
        self.end_page.set(total)
        self.range_selected()

        # Adjust the table data widgets
        self.table_data_frame.grid()
        self.pages_per_table.set(1)
        self.pages_per_table_selected()

        # Adjust the border configuration widgets
        image = self.pdf_file_images[0]
        image_width = image.width()
        image_height = image.height()
        self.border_configuration_frame.grid()
        self.borders_widgets[0].spin.config(to=image_height)
        self.borders_widgets[0].end = image_height
        self.borders_widgets[1].spin.config(to=image_height)
        self.borders_widgets[1].end = image_height
        self.borders_widgets[2].spin.config(to=image_width)
        self.borders_widgets[2].end = image_width
        self.borders_widgets[3].spin.config(to=image_width)
        self.borders_widgets[3].end = image_width

        # Buttons frame
        self.buttons_frame.grid()

    # PDF pages navigation ---------------------------------------------------------------------------------------------
    def spin_box_selected(self):
        """ Method for the spinbox buttons"""

        self.update()
        current_page = int(self.pdf_page_var.get())
        start = int(self.start_page.get())
        end = int(self.end_page.get())

        if not start <= current_page <= end:
            self.pdf_page_var.set(start)
        elif current_page < start:
            self.pdf_page_var.set(start)
        elif current_page > end:
            self.pdf_page_var.set(end)

        self.pdf_page_widget.event_generate('<Return>')

    def pdf_page_scroll(self, event):
        """ Reacts to the mouse wheel events"""

        current_page = int(self.pdf_page_var.get())
        total = len(self.pdf_file_images)

        if event.delta < 0:
            if current_page == total or current_page >= int(self.end_page.get()):
                return
            self.pdf_page_var.set(int(self.pdf_page_var.get() + 1))
        else:
            if current_page == 1 or current_page <= int(self.start_page.get()):
                return
            self.pdf_page_var.set(int(self.pdf_page_var.get() - 1))

        self.pdf_page_selected(event)

    def pdf_page_selected(self, event=None):
        """ Shows the selected PDF page on the canvas """

        current_page = int(self.pdf_page_var.get())
        start = int(self.start_page.get())
        end = int(self.end_page.get())

        if not start <= current_page <= end:
            self.pdf_page_var.set(start)
        elif current_page < start:
            self.pdf_page_var.set(start)
        elif current_page > end:
            self.pdf_page_var.set(end)

        self.find_applicable_border()

        image = self.pdf_file_images[current_page-1]
        self.pdf_canvas.delete("all")
        self.pdf_canvas.create_image(0, 0, anchor='nw', image=image, tag='main')
        self.draw_borders()

    # Pages range and pages per table selection ------------------------------------------------------------------------
    def range_selected(self, event=None):
        """ Adjusts the values for the selected range of pages """

        total = len(self.pdf_file_images)

        # Corrects for empty values
        if True:
            start_page = self.start_page.get()
            if not start_page:
                start_page = 1
                self.start_page.set(1)
            start_page = int(start_page)

            end_page = self.end_page.get()
            if not end_page:
                end_page = total
                self.end_page.set(end_page)
            end_page = int(end_page)

        # Corrects nonsense values
        if True:
            if not (1 <= int(start_page) <= total):
                start_page = 1
                self.start_page.set(1)

            if not (start_page <= int(end_page) <= total):
                end_page = total
                self.end_page.set(end_page)

        self.page_range_label.configure(text=f'({end_page-start_page + 1} page range selected)')
        self.pages_per_table_selected()

    def pages_per_table_selected(self, event=None):
        """ Checks is the range and the pages per data values are consistent """

        # Range and total numer of pages
        start_page = int(self.start_page.get())
        end_page = int(self.end_page.get())
        total_pages = end_page-start_page + 1

        # Corrects for empty values
        pages_per_data = self.pages_per_table.get()
        if not pages_per_data or int(pages_per_data) == 0:
            pages_per_data = 1
            self.pages_per_table.set(pages_per_data)
        pages_per_data = int(pages_per_data)

        pages_to_skip = self.pages_to_skip.get()
        if not pages_to_skip:
            pages_to_skip = 0
            self.pages_to_skip.set(pages_to_skip)
        pages_to_skip = int(pages_to_skip)

        # Range and pages-per-table must match, otherwise disables extraction
        if total_pages % (pages_per_data + pages_to_skip):
            self.pages_per_table_label.configure(text='(Range and table size not consistent)')
            self.number_of_models = 0
        else:
            number_of_tables = total_pages // (pages_per_data + pages_to_skip)
            self.pages_per_table_label.configure(text=f'(Total number of tables: {number_of_tables})')
            self.number_of_models = pages_per_data

        # Adjust the number of entries in the border dictionary
        for i in range(self.number_of_models):
            if str(i+1) not in self.border_values_dict:
                self.border_values_dict[str(i+1)] = {}
                for widget in self.borders_widgets:
                    self.border_values_dict[str(i+1)][widget.label.cget('text').replace(':', '')] = widget.get()

        # Removes items that no longer exist in the border dictionary
        all_borders_list = [k for k in self.border_values_dict.keys() if int(k) <= self.number_of_models]
        temp_dict = {k: v for k, v in self.border_values_dict.items() if k in all_borders_list}
        self.border_values_dict.clear()
        self.border_values_dict.update(temp_dict)

        # Adjust the border labels list
        self.border_labels_list.clear()
        for i in range(self.number_of_models):
            self.border_labels_list.append(f'Type {i+1} Border')
        for i in range(pages_to_skip):
            self.border_labels_list.append(f'SKIP')

        if not self.border_labels_list:
            self.border_labels_list.append('Type 1 Border')

        self.adjust_border_widgets()

    def adjust_border_widgets(self):
        """ Enables /  disables the border widgets """

        if not self.number_of_models:
            self.previous_border_button.config(state='disabled')
            self.next_border_button.config(state='disabled')
            self.borders_data_frame.grid_remove()
            self.clear_borders()
            return
        else:
            self.previous_border_button.config(state='normal')
            self.next_border_button.config(state='normal')
            self.borders_data_frame.grid()
            self.pdf_page_var.set(self.start_page.get())
            self.pdf_page_selected()

    # Border widgets methods -------------------------------------------------------------------------------------------
    def previous_border(self):
        """ Shows the previous border data """

        # Finds the next border that will be shown
        current_index = self.border_labels_list.index(self.border_name.cget('text'))
        new_border = self.border_labels_list[current_index-1]
        self.border_name.config(text=new_border)

        self.fill_values()

        # Changes the PDF page accordingly
        current_pdf_page = int(self.pdf_page_var.get())
        if current_pdf_page == 1:
            self.pdf_page_var.set(len(self.pdf_file_images))
        else:
            self.pdf_page_var.set(current_pdf_page - 1)
        self.pdf_page_selected()

    def next_border(self):
        """ Shows the next border data """

        # Finds the next border that will be shown
        current_index = self.border_labels_list.index(self.border_name.cget('text'))
        if current_index == len(self.border_labels_list) - 1:
            new_border = self.border_labels_list[0]
        else:
            new_border = self.border_labels_list[current_index+1]
        self.border_name.config(text=new_border)

        self.fill_values()

        # Changes the PDF page accordingly
        current_pdf_page = int(self.pdf_page_var.get())
        if current_pdf_page == len(self.pdf_file_images):
            self.pdf_page_var.set(1)
        else:
            self.pdf_page_var.set(current_pdf_page + 1)
        self.pdf_page_selected()

    def find_applicable_border(self):
        """ When changing the PDF pages selects the border that applies to the current page """

        # Protects against empty values
        if True:
            if not self.number_of_models or not self.pdf_file_images:
                return

            current_page = self.pdf_page_var.get()
            if not current_page:
                return
            current_page = int(current_page)

        # Select the border model
        index = current_page % len(self.border_labels_list) - 1
        self.border_name.config(text=self.border_labels_list[index])
        self.fill_values()

    def fill_values(self):
        """ Fills the current border values stored at the self.border_values_dict """

        current_border = self.border_name.cget('text')

        if current_border == 'SKIP':
            self.clear_borders()
            self.borders_data_frame.grid_remove()
        else:
            self.borders_data_frame.grid()
            current_border = current_border.split()[1]

            # If there is no dictionary, creates it
            if current_border not in self.border_values_dict:
                self.border_values_dict[current_border] = {}
                for widget in self.borders_widgets:
                    self.border_values_dict[current_border][widget.label.cget('text').replace(':', '')] = 0
                self.border_values_dict[current_border]['Number of Columns'] = 1

            # Shows / Hides the column related widgets
            if True:
                num_columns = int(self.border_values_dict[current_border]['Number of Columns'])
                for i in range(num_columns-1):
                    self.borders_widgets[5+i].grid()
                for i in range(4+num_columns, len(self.borders_widgets)):
                    self.borders_widgets[i].grid_remove()

            # Fills the values to the screen
            for widget in self.borders_widgets:
                widget.set(self.border_values_dict[current_border][widget.label.cget('text').replace(':', '')])

            self.draw_borders()

    def read_border_values(self, event=None):
        """ Reads and stores all the border data """

        current_model = self.border_name.cget('text')
        if current_model == 'SKIP':
            return

        current_border = current_model.split()[1]

        canvas_size = (self.pdf_canvas.winfo_width(), self.pdf_canvas.winfo_height())

        # Shows / hides the internal columns widgets
        if True:
            num_columns = self.borders_widgets[4].get() or 1
            num_columns = int(num_columns)
            for i in range(num_columns - 1):
                self.borders_widgets[5 + i].grid()

            for i in range(4 + num_columns, len(self.borders_widgets)):
                self.borders_widgets[i].grid_remove()
                self.borders_widgets[i].set(0)
                self.border_values_dict[current_border][f'Column {i-4} End'] = 0

        # Reads main borders data and protects against nonsense
        if True:
            top_border = self.borders_widgets[0].get()
            if top_border:
                if not 0 <= int(top_border) <= canvas_size[1]:
                    top_border = 0
                    self.borders_widgets[0].set(top_border)

            bottom_border = self.borders_widgets[1].get()
            if bottom_border:
                if not 0 <= int(bottom_border) <= canvas_size[1]:
                    bottom_border = canvas_size[1]
                    self.borders_widgets[1].set(bottom_border)

            left_border = self.borders_widgets[2].get()
            if left_border:
                if not 0 <= int(left_border) <= canvas_size[0]:
                    left_border = 0
                    self.borders_widgets[2].set(left_border)

            right_border = self.borders_widgets[3].get()
            if right_border:
                if not 0 <= int(right_border) <= canvas_size[0]:
                    right_border = canvas_size[0]
                    self.borders_widgets[3].set(right_border)

            num_columns = self.borders_widgets[4].get()
            if num_columns:
                if int(num_columns) < 1:
                    num_columns = 1
                    self.borders_widgets[4].set(num_columns)

        # Reads the columns data and protects against nonsense
        if True:
            borders = [item.get() for item in self.borders_widgets if item.winfo_ismapped()]
            columns_borders = borders[5:]
            columns_borders.insert(0, int(left_border))

            for i, value in enumerate(columns_borders):
                if not i:
                    continue
                if value < columns_borders[i-1]:
                    columns_borders[i] = columns_borders[i-1] + 5

                if value > right_border:
                    columns_borders[i] = right_border

            columns_borders_2 = columns_borders[1:]
            for i, value in enumerate(columns_borders_2):
                self.borders_widgets[5+i].set(value)

        # Writes the main data to the dict
        if True:
            temp_dict = {
                'Top Border': int(top_border),
                'Bottom Border': int(bottom_border),
                'Left Border': int(left_border),
                'Right Border': int(right_border),
                'Number of Columns': int(num_columns),
            }
            if current_border not in self.border_values_dict:
                self.border_values_dict[current_border] = {}
            self.border_values_dict[current_border].update(temp_dict)

        # Adjusts the limits for the widgets
        for i in range(5, len(self.borders_widgets)):
            self.borders_widgets[i].spin.config(from_=left_border, to=right_border)
            self.borders_widgets[i].spin.start = left_border
            self.borders_widgets[i].spin.end = right_border

        # Reads all values
        temp_dict = {}
        for i in range(5, len(self.borders_widgets)):
            temp_dict[self.borders_widgets[i].label.cget('text').replace(':', '')] = self.borders_widgets[i].get()
        self.border_values_dict[current_border].update(temp_dict)

        self.draw_borders()

    # Drawing methods --------------------------------------------------------------------------------------------------
    def draw_borders(self):
        """ Draws the borders on the image """

        if not self.number_of_models or not self.pdf_file_images:
            return

        current_model = self.border_name.cget('text')
        if current_model == 'SKIP':
            position = (int(self.pdf_canvas.winfo_width() / 2), int(self.pdf_canvas.winfo_height() / 2))
            self.pdf_canvas.create_text(*position, text=f'SKIP', anchor='center',
                                        fill='red', tag='top border text', font=('OpenSans', '30'))
            return

        current_model = current_model.split()[1]
        if current_model not in self.border_values_dict:
            return

        data = self.border_values_dict[current_model]
        canvas_size = (self.pdf_canvas.winfo_width(), self.pdf_canvas.winfo_height())

        self.clear_borders()

        # Draw the top border
        if data['Top Border']:
            y_pos = float(data['Top Border'])
            location = (0, y_pos, canvas_size[0], y_pos)
            location_2 = (5, y_pos+5)
            self.pdf_canvas.create_line(*location, fill='red', width=2, tag=['top border line', 'draggable'])
            self.pdf_canvas.create_text(*location_2, text=f'Top Border', anchor='nw',
                                        fill='red', tag='top border text')

        # Draw the bottom border
        if data['Bottom Border']:
            y_pos = float(data['Bottom Border'])
            location = (0, y_pos, canvas_size[0], y_pos)
            location_2 = (5, y_pos-5)
            self.pdf_canvas.create_line(*location, fill='red', width=2, tag=['bottom border line', 'draggable'])
            self.pdf_canvas.create_text(*location_2, text=f'Bottom Border', anchor='sw',
                                        fill='red', tag='bottom border text')

        # Draw the left border
        if data['Left Border']:
            x_pos = float(data['Left Border'])
            location = (x_pos, 0, x_pos, canvas_size[1])
            location_2 = (x_pos+5, 5)
            self.pdf_canvas.create_line(*location, fill='red', width=2, tag=['left border line', 'draggable'])
            self.pdf_canvas.create_text(*location_2, text=f'Left Border', anchor='nw',
                                        fill='red', tag='left border text')

        # Draw the right border
        if data['Right Border']:
            x_pos = float(data['Right Border'])
            location = (x_pos, 0, x_pos, canvas_size[1])
            location_2 = (x_pos-5, 5)
            self.pdf_canvas.create_line(*location, fill='red', width=2, tag=['right border line', 'draggable'])
            self.pdf_canvas.create_text(*location_2, text=f'Right Border', anchor='ne',
                                        fill='red', tag='right border text')

        # Draws the columns
        if True:
            internal_borders = {k: v for k, v in data.items() if 'End' in k and int(v) != 0}
            count = 1
            for k, v in internal_borders.items():
                x_pos = float(v)
                location = (x_pos, 0, x_pos, canvas_size[1])
                location_2 = (x_pos - 5, 5)
                self.pdf_canvas.create_line(*location, fill='orange', width=2,
                                            tag=[f'column line {count}', 'draggable'])
                self.pdf_canvas.create_text(*location_2, text=k, anchor='ne',
                                            fill='orange', tag='column text')
                count += 1

    def check_draggable(self, event):
        """ Checks whether the object can be dragged """

        item = self.pdf_canvas.find_closest(event.x, event.y, halo=2)[0]
        tag = self.pdf_canvas.gettags(item)[0]
        if str(tag) == 'main':
            return
        else:
            self.drag_start(event)

    def drag_start(self, event):
        """Beginning drag of an object"""

        self._drag_data["item"] = self.pdf_canvas.find_closest(event.x, event.y, halo=5)[0]
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def drag_stop(self, event):
        """End drag of an object"""

        moved_item = self._drag_data["item"]

        # reset the drag information
        self._drag_data["item"] = None
        self._drag_data["x"] = 0
        self._drag_data["y"] = 0

        if moved_item:
            self.adjust_values(moved_item)

    def drag(self, event):
        """Handle dragging of an object"""

        # compute how much the mouse has moved
        delta_x = event.x - self._drag_data["x"]
        delta_y = event.y - self._drag_data["y"]
        # move the object the appropriate amount
        self.pdf_canvas.move(self._drag_data["item"], delta_x, delta_y)
        # record the new position
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def clear_borders(self):
        """ Clears the current canvas from all borders """

        for item in self.pdf_canvas.find_all():
            tags = self.pdf_canvas.gettags(item)
            if 'main' not in tags:
                self.pdf_canvas.delete(item)

    def adjust_values(self, item):
        """ Adjust the coordinates for the object once it has been moved """

        tag = self.pdf_canvas.gettags(item)[0]
        coordinates = self.pdf_canvas.coords(tag)

        if tag == 'top border line':
            self.borders_widgets[0].set(int(coordinates[1]))
            self.borders_widgets[0].event_generate('<FocusOut>')
        elif tag == 'bottom border line':
            self.borders_widgets[1].set(int(coordinates[1]))
            self.borders_widgets[1].event_generate('<FocusOut>')
        elif tag == 'left border line':
            self.borders_widgets[2].set(int(coordinates[0]))
            self.borders_widgets[2].event_generate('<FocusOut>')
        elif tag == 'right border line':
            self.borders_widgets[3].set(int(coordinates[0]))
            self.borders_widgets[3].event_generate('<FocusOut>')
        elif 'column line' in tag:
            index = int(tag.split()[-1])
            self.borders_widgets[4+index].set(int(coordinates[0]))
            self.borders_widgets[4+index].event_generate('<FocusOut>')

        self.read_border_values()
        self.draw_borders()

    # Extract table methods --------------------------------------------------------------------------------------------
    def save_table_data(self):
        """ Saves the table data to an external file """

        # Obtain the file name
        if True:
            desktop = os.path.normpath(os.path.expanduser("~/Desktop"))
            filename = asksaveasfilename(initialdir=desktop, title="Select file name",
                                         filetypes=(("COORDS files", "*.coords"), ("All files", "*.*")))
            if not filename:
                return

            if filename.find('.coords') == -1:
                filename = filename + '.coords'

            with open(filename, mode='w') as file_object:
                json.dump((self.border_values_dict, self.header_dict), file_object)

    def load_table_data(self):
        """ Loads a previously saved table data """

        try:
            desktop = os.path.normpath(os.path.expanduser("~/Desktop"))
            file_name = askopenfilename(initialdir=desktop, title="Select File",
                                        filetypes=(("COORDS files", "*.coords"), ("All files", "*.*")))
        except IOError or FileNotFoundError:
            return

        else:
            # Checks if a file was actually selected
            if not file_name:
                return

            self.border_values_dict.clear()
            self.header_dict.clear()

            with open(file_name, mode='r') as file_object:
                temp_dict_1, temp_dict_2 = json.load(file_object)

            self.border_values_dict.update(temp_dict_1)
            self.header_dict.update(temp_dict_2)
            self.number_of_models = len(self.border_values_dict)
            self.pages_per_table.set(self.number_of_models)

            self.pdf_page_selected()
            self.fill_values()

    def clear_table_data(self):
        """ Clears the current table data """

        self.border_values_dict.clear()
        self.header_dict.clear()
        self.number_of_models = 1
        self.pages_per_table.set(1)
        self.pdf_page_selected()
        self.fill_values()

    def get_header_data(self):
        """ Gets the header values from USER """

        for i in range(self.number_of_models):
            if str(i+1) not in self.header_dict:
                current_list = []
                self.header_dict[str(i+1)] = current_list
            else:
                current_list = '//'.join(self.header_dict[str(i+1)])

            # Puts the PDF on the right page
            self.pdf_page_var.set(i+1)
            self.pdf_page_selected()

            # Shows the Top Level window
            local_top = tk.Toplevel()
            local_top.minsize(600, 150)
            local_top.iconbitmap(os.path.join(self.path, 'petrobras.ico'))
            local_top.title('ASME PDF Extract Tool')
            local_top.columnconfigure(0, weight=1)
            local_top.rowconfigure(1, weight=1)

            # Message
            message = f'Enter header from border model {i+1} (separate with double forward slash - // )'
            label = ttk.Label(local_top, text=message)
            label.grid(row=0, column=0, columnspan=2, sticky='nsew', padx=10, pady=10)

            var = tk.StringVar(value=current_list)
            text = ttk.Entry(local_top, textvariable=var)
            text.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=10)

            button = ttk.Button(local_top, text='OK', command=lambda: local_top.destroy(), width=20)
            button.grid(row=2, column=1, sticky='nsew', padx=10, pady=10)

            local_top.lift()
            local_top.grab_set()
            local_top.wait_window()

            local_string = var.get()
            current_list = local_string.split('//')

            self.header_dict[str(i+1)] = current_list

    def extract_table(self):
        """ Method to extract the tables values """

        if not self.pdf_file_images:
            return

        # Header data from user
        self.get_header_data()

        # Extracts table
        _start = int(self.start_page.get())
        _end = int(self.end_page.get())
        _step = self.number_of_models
        _skip = 0
        df = read_pdf_table(self.pdf_file_name, _start, _end, _step, _skip,
                            self.border_values_dict, self.header_dict)

        if True:
            desktop = os.path.normpath(os.path.expanduser("~/Desktop"))
            filename = asksaveasfilename(initialdir=desktop, title="Select file name",
                                         filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))
            if not filename:
                return

            if filename.find('.csv') == -1:
                filename = filename + '.csv'

            df.to_csv(filename, sep=';')

            pandas.set_option("display.max_rows", None, "display.max_columns", None)
            print(df)

    # Root methods -----------------------------------------------------------------------------------------------------
    @staticmethod
    def screen_position(window, parent=None, delta_x=0, delta_y=0):
        """
        Defines the screen position for a given widget
        Input:
            window: widget (tk.Tk() or tk.TopLevel()) being positioned
            parent: reference to the screen positioning
            delta_x: additional distance relative to the center in the X direction (positive is right)
            delta_y: additional distance relative to the center in the Y direction (positive is down)
        Returns:
            position_string: string to be passed to the geometry manager to position the widget (self.geometry(string))
        """

        # Window (widget) Size
        if window.minsize()[0]:
            window_width = window.minsize()[0]
            window_height = window.minsize()[1]
        else:
            window_width = window.winfo_width()
            window_height = window.winfo_height()

        if parent:
            # Finds the parent position and center coordinates
            parent_x = parent.winfo_x()
            parent_y = parent.winfo_y()
            parent_width = parent.winfo_width()
            parent_height = parent.winfo_height()
            parent_center_x = int(parent_x + parent_width / 2)
            parent_center_y = int(parent_y + parent_height / 2)

            # Determines the new window start position (upper left)
            x_position = int(parent_center_x - window_width / 2) + int(delta_x)
            y_position = int(parent_center_y - window_height / 2) + int(delta_y)

        else:
            # Finds th screen size
            screen_width = window.winfo_screenwidth()
            screen_height = window.winfo_screenheight()

            # Determines the new window start position (upper left)
            x_position = int((screen_width - window_width) / 2) + int(delta_x)
            y_position = int((screen_height - window_height) / 2) + int(delta_y)

        return f'{window_width}x{window_height}+{x_position}+{y_position}'

    def start(self):
        self.mainloop()

    def finish(self):
        self.destroy()
        exit()


if __name__ == '__main__':
    root = ASMEPdfExtract()
    root.start()
