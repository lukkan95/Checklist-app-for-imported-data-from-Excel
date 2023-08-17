import os
from tkinter.ttk import Progressbar
import pandas as pd
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from datetime import datetime


class Importdata(object):

    @staticmethod
    def get_data(sheet_choice):
        filename = 'Procedury startowe.xlsx'
        df = pd.read_excel(filename, sheet_name=f'{sheet_choice}', engine='openpyxl', dtype=object, header=None)
        list_1 = df.values.tolist()
        data = []
        for elem in list_1[1:]:
            if str(elem[1]) == 'nan' or str(elem[0]) == 'nan':
                continue
            else:
                data.append(f'{elem[0]} {elem[1]}')
        return data


class DataLogs(object):

    def create_text_file(self):
        filename = f'Data_logs_{self.get_time()}.txt'
        if not os.path.isfile(filename):
            with open(filename, 'w') as file:
                file.write(f"Start logging: {self.get_time()}\n")
        return filename

    def get_time(self):
        now = datetime.now()
        dt_string = now.strftime("%d_%m_%Y %H-%M-%S")
        return dt_string

    # def confirm_procedure(self):
    #     pass
    #
    # def cancellation_procedure(self):
    #     pass

    def log_status_of_checkbutton(self, listbox, name, value, sheet_name, filename):
        current_data = self.get_time()
        if value == 1:
            listbox.insert('end', f'{current_data} {sheet_name}: Zakończono procedurę: {name}')
            listbox.itemconfig('end', fg='green')
            with open(filename, 'a+') as file:
                file.write(f'{current_data} {sheet_name}: Zakończono procedurę: {name}\n')
        else:
            listbox.insert('end', f'{current_data} {sheet_name}: Anuulowano procedurę: {name}')
            listbox.itemconfig('end', fg='red')
            with open(filename, 'a+') as file:
                file.write(f'{current_data} {sheet_name}: Anuulowano procedurę: {name}\n')

class Figure1(object):

    def __init__(self, root=tk.Tk()):

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

        self.timer_label()

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

        self.tfr.tkraise()
        self.pb1.tkraise()
        self.lb1.tkraise()

        self.filename = DataLogs().create_text_file()

    def root_mainloop_start(self):
        self.root.attributes("-topmost", True)
        self.root.title('Rejestrator procedury startowej')
        self.root.config(bg='#ff6666')

        self.root.mainloop()

    def start_parameters(self):
        self.x = 1200
        self.y = 800
        self.root.geometry(f'{self.x}x{self.y}')
        self.root.resizable(False, False)
        self.root.title('Figure1')

    def create_dict_check_status(self):
        self.dict_check_status = {self.sheet_1: {},
                                  self.sheet_2: {},
                                  self.sheet_3: {}}

    def page1_frame(self):
        self.tfr = tk.Frame(self.root, width=0.1, height=0.1)
        self.tfr.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.5)

    def page2_frame(self):
        self.p2f = tk.Frame(self.root, width=0.1, height=0.1, bg='yellow')
        self.p2f.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.5)

    def page3_frame(self):
        self.p3f = tk.Frame(self.root, width=0.1, height=0.1, bg='green')
        self.p3f.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.5)

    def lower_frame(self):
        self.dfr = tk.Frame(self.root, width=0.1, height=0.1, bg='white')
        self.dfr.place(relx=0.1, rely=0.7, relwidth=0.8, relheight=0.25)

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
        self.clock = tk.Label(self.root, text=self.get_time_to_timer())
        self.clock.place(relx=0.8, rely=0.05, relwidth=0.1, relheight=0.03)
        self.clock.after(1000, self.timer_label())


    def get_time_to_timer(self):
        now = datetime.now()
        dt_string = now.strftime("%H:%M:%S")
        return dt_string

    def create_scrolltext(self, root):
        self.scrolltexture = ScrolledText(root, x=int(self.x * 0.05), y=int(self.x * 0.2), width=int(self.x * 0.1),
                                          height=int(self.y * 0.04))
        self.scrolltexture.pack()

    def add_to_scrolltext(self, sheet_choice, progressbar, label_progressbar):
        import_data = Importdata.get_data(sheet_choice)
        for elem in import_data:
            self.dict_check_status[sheet_choice][elem] = 0
            new_checkbutton = self.add_checkbutton(elem, sheet_choice, progressbar, label_progressbar)
            self.scrolltexture['state'] = 'normal'
            self.scrolltexture.window_create('end', window=new_checkbutton)
            self.scrolltexture.insert('end', '\n')
            self.scrolltexture['state'] = 'disabled'

    def add_checkbutton(self, elem, sheet_choice, progressbar, label_progressbar):
        var = tk.IntVar()
        cb = tk.Checkbutton(self.scrolltexture, text=f'{elem}', bg='white', anchor='w', variable=var,
                            command=lambda: [DataLogs().log_status_of_checkbutton(self.listbox_1, elem, var.get(), sheet_choice, self.filename),
                                             self.change_color_buttons(cb, var.get()),
                                             self.change_status_checkbutton(elem, var.get(), sheet_choice), self.check_if_status_completed(sheet_choice), self.update_progressbar(progressbar, sheet_choice), self.update_label_progressbar(sheet_choice, label_progressbar)])
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
            self.root.config(background="#4dffa6")
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
        self.btn1.place(relx=0.1, rely=0.05, relwidth=0.1, relheight=0.03)


    def add_button2(self):
        self.btn2 = tk.Button(self.root, text=self.sheet_2,
                              command=lambda: [self.p2f.tkraise(), self.pb2.tkraise(), self.lb2.tkraise(),
                                               self.check_if_status_completed(self.sheet_2)])
        self.btn2.place(relx=0.21, rely=0.05, relwidth=0.1, relheight=0.03)

    def add_button3(self):
        self.btn3 = tk.Button(self.root, text=self.sheet_3,
                              command=lambda: [self.p3f.tkraise(), self.pb3.tkraise(), self.lb3.tkraise(),
                                               self.check_if_status_completed(self.sheet_3)])
        self.btn3.place(relx=0.32, rely=0.05, relwidth=0.1, relheight=0.03)

    def label_example(self):
        pass

if __name__ == '__main__':
    figure = Figure1()
    figure.root_mainloop_start()
