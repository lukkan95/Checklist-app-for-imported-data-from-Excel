import os
from tkinter.ttk import Progressbar
import pandas as pd
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from datetime import datetime


class ImportExcelData(object):

    @staticmethod
    def get_data(filename, sheet_choice):
        filename = filename
        df = pd.read_excel(filename, sheet_name=f'{sheet_choice}', engine='openpyxl', dtype=object, header=None)
        list_1 = df.values.tolist()
        data = []
        for elem in list_1[1:]:
            if str(elem[1]) == 'nan' or str(elem[0]) == 'nan':
                continue
            else:
                data.append(f'{elem[0]} {elem[1]}')
        return data


class DataToTxt(object):

    def __init__(self):
        self.filename = None

    def create_text_file(self):
        self.filename = f'Data_logs_{ConvertedDateTime.get_time()}.txt'
        if not os.path.isfile(self.filename):
            with open(self.filename, 'w') as file:
                file.write(f"Start logging: {ConvertedDateTime.get_time()}\n")
        return self.filename

    @staticmethod
    def add_to_text_file(filename, text):
        with open(filename, 'a+') as file:
            file.write(text)

    @staticmethod
    def delete_txt_file(filename):
        path = f'{os.path.dirname(os.path.realpath(__file__))}\{filename}'
        os.remove(path)


class ConvertedDateTime(object):

    @staticmethod
    def get_time():
        now = datetime.now()
        dt_string = now.strftime("%d_%m_%Y %H-%M-%S")
        return dt_string


class DataLogs(object):

    @staticmethod
    def log_status_from_checkbutton_to_listbox_and_txt_file(listbox, name, value, sheet_name, filename=None):
        current_data = ConvertedDateTime.get_time()
        if value == 1:
            text = f'{current_data} {sheet_name} : Zakończono procedurę: {name}\n'
            listbox.insert('end', text)
            listbox.itemconfig('end', fg='green')
            DataToTxt.add_to_text_file(filename, text)

        else:
            text = f'{current_data} {sheet_name} : Anuulowano procedurę: {name}\n'
            listbox.insert('end', text)
            listbox.itemconfig('end', fg='red')
            DataToTxt.add_to_text_file(filename, text)

class Figure1(object):

    def __init__(self, root=tk.Tk()):


        self.excel_file_name = 'Procedury startowe.xlsx'
        self.sheet_1 = 'A'
        self.sheet_2 = 'B'
        self.sheet_3 = 'C'
        self.root = root
        self.start_parameters()
        self.create_dict_check_status()
        self.page2_frame()
        self.page1_frame()
        self.page3_frame()
        self.lower_frame()


        self.checkbuttons_storage = {f'{str(self.sheet_1)}':[],
                                     f'{str(self.sheet_2)}': [],
                                     f'{str(self.sheet_3)}': [],
                                     }

        self.bind_key_maximize_window()
        self.bind_key_exit_applicaiton()
        # self.bind_key_destroy()


        self.timer_label()
        self.update_timer_label()

        self.pb1 = self.progressbar()
        self.lb1 = self.label_progressbar(self.sheet_1)
        self.create_scrolltext(self.tfr)
        self.add_to_scrolltext(self.sheet_1, self.pb1, self.lb1)
        self.scrollbar_lower_frame()

        self.pb2 = self.progressbar()
        self.lb2 = self.label_progressbar(self.sheet_2)
        self.create_scrolltext(self.p2f)
        self.add_to_scrolltext(self.sheet_2, self.pb2, self.lb2)

        self.pb3 = self.progressbar()
        self.lb3 = self.label_progressbar(self.sheet_3)
        self.create_scrolltext(self.p3f)
        self.add_to_scrolltext(self.sheet_3, self.pb3, self.lb3)

        self.add_button1()
        self.add_button2()
        self.add_button3()
        self.add_button_import_data_from_txt()

        self.tfr.tkraise()
        self.pb1.tkraise()
        self.lb1.tkraise()



        self.exit_window = ExitWindow()
        # print(self.checkbuttons_storage[0]['variable'])
        self.filename = DataToTxt().create_text_file()

        self.state_active = tk.IntVar(self.root, value=1)
        self.state_inactive = tk.IntVar(self.root, value=0)


    def root_mainloop_start(self):
        self.root.attributes("-topmost", True)
        self.root.title('Rejestrator procedury startowej')
        self.root.config(bg='#ff6666')
        self.root.protocol('WM_DELETE_WINDOW', self.ask_if_exit)
        self.root.mainloop()

    def ask_if_exit(self):
        if self.exit_window.check is False:
            self.exit_window.start()
        else:
            pass

    def start_parameters(self):
        self.app_width = 1200
        self.app_height = 800
        self.center_window_on_screen(self.root, self.app_width, self.app_height)
        self.root.resizable(False, False)
        self.root.title('Figure1')

    @staticmethod
    def center_window_on_screen(root, width, height):
        ws = root.winfo_screenwidth()
        hs = root.winfo_screenheight()
        x = (ws / 2) - (width / 2)
        y = (hs / 2) - (height / 2)
        root.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

    def maximize_window(self):
        self.root.state('zoomed')
        self.bind_key_minimize_window()

    def minimize_window(self):
        self.root.state('normal')
        self.bind_key_maximize_window()

    def exit(self):
        DataToTxt.delete_txt_file(self.filename)
        self.root.destroy()



    def bind_key_maximize_window(self):
        self.root.bind('<Tab>', lambda e: self.maximize_window())

    def bind_key_minimize_window(self):
        self.root.bind('<Tab>', lambda e: self.minimize_window())

    def bind_key_exit_applicaiton(self):
        self.root.bind('<Escape>', lambda e: self.ask_if_exit())


    def create_dict_check_status(self):
        self.dict_check_status = {self.sheet_1: {},
                                  self.sheet_2: {},
                                  self.sheet_3: {}}

    def page1_frame(self):
        self.tfr = tk.Frame(self.root, width=0.1, height=0.1)
        self.tfr.place(relx=0.05, rely=0.1, relwidth=0.9, relheight=0.5)

    def page2_frame(self):
        self.p2f = tk.Frame(self.root, width=0.1, height=0.1, bg='yellow')
        self.p2f.place(relx=0.05, rely=0.1, relwidth=0.9, relheight=0.5)

    def page3_frame(self):
        self.p3f = tk.Frame(self.root, width=0.1, height=0.1, bg='green')
        self.p3f.place(relx=0.05, rely=0.1, relwidth=0.9, relheight=0.5)

    def lower_frame(self):
        self.dfr = tk.Frame(self.root, width=0.1, height=0.1, bg='white')
        self.dfr.place(relx=0.05, rely=0.7, relwidth=0.9, relheight=0.25)

    def scrollbar_lower_frame(self):
        self.scrollbar = tk.Scrollbar(self.dfr)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log = tk.Text(self.dfr, width=30, height=30, takefocus=0)
        self.scrollbar.config(command=self.log.yview)
        self.log.pack(fill='both', expand=1)
        self.log.config(yscrollcommand=self.scrollbar.set)
        self.listbox_1 = tk.Listbox(self.log, yscrollcommand=self.scrollbar.set)
        self.listbox_1.pack(side='left', fill='both', expand=1)
        self.log.config(yscrollcommand=self.listbox_1.yview())

    def timer_label(self):
        self.clock = tk.Label(self.root, text=self.get_time_to_timer(), font=("Segoe UI", "12"))
        self.clock.place(relx=0.85, rely=0.05, relwidth=0.1, relheight=0.03)

    def update_timer_label(self):
        self.clock.config(text=self.get_time_to_timer())
        self.clock.after(1000, self.update_timer_label)

    def get_time_to_timer(self):
        now = datetime.now()
        dt_string = now.strftime("%H : %M : %S")
        return dt_string

    def create_scrolltext(self, root):
        self.scrolltexture = ScrolledText(root)
        self.scrolltexture.place(relx=0, rely=0, relwidth=1, relheight=1)

    def add_to_scrolltext(self, sheet_choice, progressbar, label_progressbar):
        import_data = ImportExcelData.get_data(self.excel_file_name, sheet_choice)
        for elem in import_data:
            self.dict_check_status[sheet_choice][elem] = 0
            new_checkbutton = self.add_checkbutton(elem, sheet_choice, progressbar, label_progressbar)
            self.scrolltexture['state'] = 'normal'
            self.scrolltexture.window_create('end', window=new_checkbutton)
            self.scrolltexture.insert('end', '\n')
            self.scrolltexture['state'] = 'disabled'

    def add_checkbutton(self, elem, sheet_choice, progressbar, label_progressbar):
        var = tk.IntVar()
        cb = tk.Checkbutton(self.scrolltexture, text=f'{elem}', bg='white', anchor='w', variable=var, onvalue=1, offvalue=0,
                            command=lambda: [DataLogs().log_status_from_checkbutton_to_listbox_and_txt_file(
                                             self.listbox_1, elem, var.get(), sheet_choice, self.filename),
                                             self.change_color_buttons(cb, var.get()),
                                             self.change_status_checkbutton(elem, var.get(), sheet_choice),
                                             self.check_if_status_completed(sheet_choice),
                                             self.update_progressbar(progressbar, sheet_choice),
                                             self.update_label_progressbar(sheet_choice, label_progressbar)])
        self.checkbuttons_storage[sheet_choice].append(cb)
        return cb

    def change_color_buttons(self, elem, value):
        if value == 1:
            elem['fg'] = 'green'
        else:
            elem['fg'] = 'red'

    def change_status_checkbutton(self, elem, var, sheet):
        self.dict_check_status[sheet][elem] = int(var)

    def check_if_status_completed(self, sheet):
        if int(0) in self.dict_check_status[sheet].values():
            self.root.config(background="#ff6666")
            self.root.update()
        else:
            self.root.config(background="#006118")
            self.root.update()

    def progressbar(self):
        progressbar = Progressbar(self.root, orient='horizontal', length=1, mode='determinate', value=0)
        progressbar.place(relx=0.4, rely=0.62, relwidth=0.2, relheight=0.03)
        return progressbar

    def update_progressbar(self, progressbar, sheet):
        progressbar.configure(value=round((sum(self.dict_check_status[sheet].values()) / len(self.dict_check_status[sheet])) * 100))

    def label_progressbar(self, sheet):
        try:
            text = f'Wykonano {sum(self.dict_check_status[sheet].values())} z {len(self.dict_check_status[sheet])} zadań - {round((sum(self.dict_check_status[sheet].values())/len(self.dict_check_status[sheet]))*100)}%'
            value_label = tk.Label(self.root, text=text, bg="#ff6666", font=("Segoe UI", "10"))
            value_label.place(relx=0.4, rely=0.66, relwidth=0.2, relheight=0.03)
        except:
            value_label = tk.Label(self.root, text='Procedury nierozpoczęte',bg="#ff6666", font=("Segoe UI", "10"))
            value_label.place(relx=0.4, rely=0.66, relwidth=0.2, relheight=0.03)
        return value_label

    def update_label_progressbar(self, sheet, label_progressbar):
        label_progressbar.configure(text=f'Wykonano {sum(self.dict_check_status[sheet].values())} z {len(self.dict_check_status[sheet])} zadań - {round((sum(self.dict_check_status[sheet].values())/len(self.dict_check_status[sheet]))*100)}%')
        label_progressbar.update()
        if sum(self.dict_check_status[sheet].values()) == len(self.dict_check_status[sheet]):
            label_progressbar.configure(bg='#4dffa6')
        else:
            label_progressbar.configure(bg='#ff6666')


    def add_button1(self):
        self.btn1 = tk.Button(self.root, text=self.sheet_1, command=lambda: [self.tfr.tkraise(), self.pb1.tkraise(), self.lb1.tkraise(), self.check_if_status_completed(self.sheet_1),  self.update_progressbar(self.pb1, self.sheet_1), self.update_label_progressbar(self.sheet_1, self.lb1)])
        self.btn1.place(relx=0.05, rely=0.05, relwidth=0.1, relheight=0.03)


    def add_button2(self):
        self.btn2 = tk.Button(self.root, text=self.sheet_2,
                              command=lambda: [self.p2f.tkraise(), self.pb2.tkraise(), self.lb2.tkraise(),
                                               self.check_if_status_completed(self.sheet_2)])
        self.btn2.place(relx=0.16, rely=0.05, relwidth=0.1, relheight=0.03)

    def add_button3(self):
        self.btn3 = tk.Button(self.root, text=self.sheet_3,
                              command=lambda: [self.p3f.tkraise(), self.pb3.tkraise(), self.lb3.tkraise(),
                                               self.check_if_status_completed(self.sheet_3)])
        self.btn3.place(relx=0.27, rely=0.05, relwidth=0.1, relheight=0.03)

    def combine_number_with_sheet(self, arg):
        if arg == 'A':
            arg = 0
        elif arg == 'B':
            arg = 1
        else:
            arg = 2
        return arg

    def import_data_from_txt(self):
        filename = 'Data_logs_31_08_2023 21-38-57.txt'
        # print(self.checkbuttons_storage)
        with open(filename, 'r') as file:


            lines = file.readlines()
            for line in lines[1:]:

                imported_sheet = line.split(' ', 7)[2]
                imported_state = line.split(' ', 7)[4]
                imported_number_of_procedure = (line.split(' ', 7)[6])
                imported_activity = line.split(' ', 7)[7].replace('\n', '')
                temp_checkbutton = self.checkbuttons_storage[imported_sheet][int(imported_number_of_procedure)-1]
                print(temp_checkbutton['variable'])
                if imported_state == 'Zakończono':
                    # temp_checkbutton['variable'] = self.state_active.get()
                    # temp_checkbutton['variable'] = self.state_active
                    self.change_color_buttons(temp_checkbutton, self.state_active.get())
                    self.change_status_checkbutton(temp_checkbutton, self.state_active.get(), imported_sheet)
                    # temp_checkbutton['fg'] = 'green'


                elif imported_state == 'Anuulowano':
                    # temp_checkbutton['fg'] = 'red'
                    # temp_checkbutton['variable'] = self.state_inactive
                    self.change_color_buttons(temp_checkbutton, self.state_inactive.get())
                    self.change_status_checkbutton(temp_checkbutton, self.state_inactive.get(), imported_sheet)

                print(temp_checkbutton['variable'])




                # if imported_state == 'Zakończono':
                #     # print(self.checkbuttons_storage[self.combine_number_with_sheet(imported_sheet)])
                #     self.checkbuttons_storage[self.combine_number_with_sheet(imported_sheet)]['fg'] = 'green'
                #     self.checkbuttons_storage[self.combine_number_with_sheet(imported_sheet)]['variable'] = self.state_active
                #     # print(self.checkbuttons_storage[0])
                #     # print(self.dict_check_status['A'])
                #     # self.dict_check_status[imported_sheet][imported_activity] = self.state_active
                #     # self.check_if_status_completed(imported_sheet),
                #     # self.update_progressbar(self.pb1, imported_sheet),
                #     # self.update_label_progressbar(imported_sheet, self.lb1)
                #
                #
                # elif imported_state == 'Anuulowano':
                #     self.checkbuttons_storage[self.combine_number_with_sheet(imported_sheet)]['fg'] = 'red'
                #     self.checkbuttons_storage[self.combine_number_with_sheet(imported_sheet)]['variable'] = self.state_inactive
                #     # print(self.checkbuttons_storage[0]['variable'])
                #     # self.dict_check_status[imported_sheet][imported_activity] = self.state_inactive
                #     # self.check_if_status_completed(imported_sheet),
                #     # self.update_progressbar(self.pb1, imported_sheet),
                #     # self.update_label_progressbar(imported_sheet, self.lb1)
    def add_button_import_data_from_txt(self):
        self.btn3 = tk.Button(self.root, text='Import data',
                              command=lambda: [self.import_data_from_txt()])
        self.btn3.place(relx=0.38, rely=0.05, relwidth=0.1, relheight=0.03)


class ExitWindow(object):

    def __init__(self):
        self.check = False

    def start(self):
        self.check = True
        self.new_window = tk.Toplevel()
        self.geometry()
        self.title()
        self.label()
        self.confirm_exit_button()
        self.cancel_exit_button()

    def geometry(self):
        new_window_width = 300
        new_window_height = 150
        Figure1.center_window_on_screen(self.new_window, new_window_width, new_window_height)
        self.new_window.protocol('WM_DELETE_WINDOW', self.destroy_button)
        self.new_window.resizable(False, False)
        self.new_window.attributes('-topmost', True)
        self.new_window.grab_set()

    def title(self):
        self.new_window.title('Confirm Exit')

    def label(self):
        label = tk.Label(self.new_window, text='Do you want to quit?')
        label.place(relx=0, rely=0, relwidth=1, relheight=0.6)

    def confirm_exit_button(self):
        button = tk.Button(self.new_window, text='Yes', default='normal', command=lambda: Figure1().exit())
        button.place(relx=0.05, rely=0.7, relwidth=0.4, relheight=0.2)

    def change_status(self):
        self.check = False

    def cancel_exit_button(self):
        button = tk.Button(self.new_window, text='No', default='active', command=lambda:
        [
            self.new_window.destroy(),
            self.change_status()
        ])
        button.place(relx=0.55, rely=0.7, relwidth=0.4, relheight=0.2)

    def destroy_button(self):
        self.check = False
        self.new_window.destroy()




if __name__ == '__main__':
    figure = Figure1()
    figure.root_mainloop_start()
    DataToTxt.delete_txt_file(figure.filename)
    
