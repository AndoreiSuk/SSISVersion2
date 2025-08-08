import tkinter as tk
import ttkbootstrap as ttk
from tkinter import font as tkfont
from .database import programs, students, colleges
from .informations import StudentInfo, ProgramInfo, CollegeInfo
import random
class StudentTable(ttk.Treeview):
    def __init__(self, master):
        super().__init__(
            master=master,
            bootstyle='info',
            height=12,
            columns=('ID_Display', 'FIRSTNAME_Display', 'LASTNAME_Display', 'SEX_Display', 'PROGRAM_Display', 'YEAR_LEVEL_Display'),
            show='headings'
        )
        self.heading('ID_Display', text='STUDENT ID')
        self.heading('FIRSTNAME_Display', text='FIRST NAME')
        self.heading('LASTNAME_Display', text='LAST NAME')
        self.heading('SEX_Display', text='SEX')
        self.heading('PROGRAM_Display', text='PROGRAM')
        self.heading('YEAR_LEVEL_Display', text='YEAR LEVEL')
        self.column('ID_Display', width=100, anchor='center')
        self.column('FIRSTNAME_Display', width=150, anchor='center')
        self.column('LASTNAME_Display', width=150, anchor='center')
        self.column('SEX_Display', width=80, anchor='center')
        self.column('PROGRAM_Display', width=120, anchor='center')
        self.column('YEAR_LEVEL_Display', width=100, anchor='center')
class ProgramTable(ttk.Treeview):
    def __init__(self, master):
        super().__init__(
            master=master,
            bootstyle='info',
            height=12,
            columns=('CODE_Display', 'NAME_Display', 'COLLEGE_Display'),
            show='headings'
        )
        self.heading('CODE_Display', text='PROGRAM CODE')
        self.heading('NAME_Display', text='PROGRAM NAME')
        self.heading('COLLEGE_Display', text='COLLEGE')
        self.column('CODE_Display', width=80, anchor='center')
        self.column('NAME_Display', width=300, anchor='center')
        self.column('COLLEGE_Display', width=150, anchor='center')
class CollegeTable(ttk.Treeview):
    def __init__(self, master):
        super().__init__(
            master=master,
            bootstyle='info',
            height=12,
            columns=('CODE_Display', 'NAME_Display'),
            show='headings'
        )
        self.heading('CODE_Display', text='COLLEGE CODE')
        self.heading('NAME_Display', text='COLLEGE NAME')
        self.column('CODE_Display', width=100, anchor='center')
        self.column('NAME_Display', width=550, anchor='center')
class SortStudentDialog(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master_app = master
        self.title("Sort Students")
        self.transient(master)
        self.resizable(False, False)
        window_width = 350
        window_height = 550
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        self.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        main_frame = ttk.Frame(self, padding=15)
        main_frame.pack(fill='both', expand=True)
        self.sort_variable = tk.StringVar(value=self.master_app.current_student_sort_option)
        ttk.Label(main_frame, text="SORT BY", font=('Default', 12, 'bold')).pack(pady=(0, 10))
        id_frame = ttk.Labelframe(main_frame, text="Student ID Number", padding=10)
        id_frame.pack(fill='x', pady=2)
        ttk.Radiobutton(id_frame, text="Ascending to Descending", variable=self.sort_variable, value="id_asc").pack(anchor='w')
        ttk.Radiobutton(id_frame, text="Descending to Ascending", variable=self.sort_variable, value="id_desc").pack(anchor='w')
        firstname_frame = ttk.Labelframe(main_frame, text="First Name", padding=10)
        firstname_frame.pack(fill='x', pady=2)
        ttk.Radiobutton(firstname_frame, text="A-Z", variable=self.sort_variable, value="firstname_az").pack(anchor='w')
        ttk.Radiobutton(firstname_frame, text="Z-A", variable=self.sort_variable, value="firstname_za").pack(anchor='w')
        lastname_frame = ttk.Labelframe(main_frame, text="Last Name", padding=10)
        lastname_frame.pack(fill='x', pady=2)
        ttk.Radiobutton(lastname_frame, text="A-Z", variable=self.sort_variable, value="lastname_az").pack(anchor='w')
        ttk.Radiobutton(lastname_frame, text="Z-A", variable=self.sort_variable, value="lastname_za").pack(anchor='w')
        sex_frame = ttk.Labelframe(main_frame, text="Sex", padding=10)
        sex_frame.pack(fill='x', pady=2)
        ttk.Radiobutton(sex_frame, text="Male to Female", variable=self.sort_variable, value="sex_mf").pack(anchor='w')
        ttk.Radiobutton(sex_frame, text="Female to Male", variable=self.sort_variable, value="sex_fm").pack(anchor='w')
        program_frame = ttk.Labelframe(main_frame, text="Program Code", padding=10)
        program_frame.pack(fill='x', pady=2)
        ttk.Radiobutton(program_frame, text="A-Z", variable=self.sort_variable, value="program_az").pack(anchor='w')
        ttk.Radiobutton(program_frame, text="Z-A", variable=self.sort_variable, value="program_za").pack(anchor='w')
        year_frame = ttk.Labelframe(main_frame, text="Year Level", padding=10)
        year_frame.pack(fill='x', pady=2)
        ttk.Radiobutton(year_frame, text="First Year to Fourth Year", variable=self.sort_variable, value="year_asc").pack(anchor='w')
        ttk.Radiobutton(year_frame, text="Fourth Year to First Year", variable=self.sort_variable, value="year_desc").pack(anchor='w')
        button_frame = ttk.Frame(main_frame, padding=(0, 15, 0, 0))
        button_frame.pack(fill='x', side='bottom')
        apply_button = ttk.Button(button_frame, text="Update Changes", bootstyle="primary", command=self.apply_sort)
        apply_button.pack(side='left', expand=True, padx=(0, 5), ipady=3)
        clear_button = ttk.Button(button_frame, text="Clear", bootstyle="info", command=self.clear_sort)
        clear_button.pack(side='left', expand=True, padx=5, ipady=3)
        cancel_button = ttk.Button(button_frame, text="Cancel", bootstyle="secondary", command=self.destroy)
        cancel_button.pack(side='right', expand=True, padx=(5, 0), ipady=3)
        self.grab_set()
    def apply_sort(self):
        selected_option = self.sort_variable.get()
        if selected_option and selected_option != 'None':
            self.master_app.current_student_sort_option = selected_option
            self.master_app.refresh_student_table(keyword=self.master_app.student_key_search.get())
        self.destroy()
    def clear_sort(self):
        self.master_app.current_student_sort_option = None
        self.master_app.refresh_student_table(keyword=self.master_app.student_key_search.get())
        self.destroy()
class SortProgramDialog(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master_app = master
        self.title("Sort Programs")
        self.transient(master)
        self.resizable(False, False)
        window_width = 350
        window_height = 350
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        self.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        main_frame = ttk.Frame(self, padding=15)
        main_frame.pack(fill='both', expand=True)
        self.sort_variable = tk.StringVar(value=self.master_app.current_program_sort_option)
        ttk.Label(main_frame, text="SORT BY", font=('Default', 12, 'bold')).pack(pady=(0, 10))
        code_frame = ttk.Labelframe(main_frame, text="Program Code", padding=10)
        code_frame.pack(fill='x', pady=2)
        ttk.Radiobutton(code_frame, text="A-Z", variable=self.sort_variable, value="code_az").pack(anchor='w')
        ttk.Radiobutton(code_frame, text="Z-A", variable=self.sort_variable, value="code_za").pack(anchor='w')
        name_frame = ttk.Labelframe(main_frame, text="Program Name", padding=10)
        name_frame.pack(fill='x', pady=2)
        ttk.Radiobutton(name_frame, text="A-Z", variable=self.sort_variable, value="name_az").pack(anchor='w')
        ttk.Radiobutton(name_frame, text="Z-A", variable=self.sort_variable, value="name_za").pack(anchor='w')
        college_frame = ttk.Labelframe(main_frame, text="College Code", padding=10)
        college_frame.pack(fill='x', pady=2)
        ttk.Radiobutton(college_frame, text="A-Z", variable=self.sort_variable, value="college_az").pack(anchor='w')
        ttk.Radiobutton(college_frame, text="Z-A", variable=self.sort_variable, value="college_za").pack(anchor='w')
        button_frame = ttk.Frame(main_frame, padding=(0, 15, 0, 0))
        button_frame.pack(fill='x', side='bottom')
        apply_button = ttk.Button(button_frame, text="Update Changes", bootstyle="primary", command=self.apply_sort)
        apply_button.pack(side='left', expand=True, padx=(0, 5), ipady=3)
        clear_button = ttk.Button(button_frame, text="Clear", bootstyle="info", command=self.clear_sort)
        clear_button.pack(side='left', expand=True, padx=5, ipady=3)
        cancel_button = ttk.Button(button_frame, text="Cancel", bootstyle="secondary", command=self.destroy)
        cancel_button.pack(side='right', expand=True, padx=(5, 0), ipady=3)
        self.grab_set()
    def apply_sort(self):
        selected_option = self.sort_variable.get()
        if selected_option and selected_option != 'None':
            self.master_app.current_program_sort_option = selected_option
            self.master_app.refresh_program_table(keyword=self.master_app.program_key_search.get())
        self.destroy()
    def clear_sort(self):
        self.master_app.current_program_sort_option = None
        self.master_app.refresh_program_table(keyword=self.master_app.program_key_search.get())
        self.destroy()
class SortCollegeDialog(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master_app = master
        self.title("Sort Colleges")
        self.transient(master)
        self.resizable(False, False)
        window_width = 350
        window_height = 350
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        self.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        main_frame = ttk.Frame(self, padding=15)
        main_frame.pack(fill='both', expand=True)
        self.sort_variable = tk.StringVar(value=self.master_app.current_college_sort_option)
        ttk.Label(main_frame, text="SORT BY", font=('Default', 12, 'bold')).pack(pady=(0, 10))
        code_frame = ttk.Labelframe(main_frame, text="College Code", padding=10)
        code_frame.pack(fill='x', pady=2)
        ttk.Radiobutton(code_frame, text="A-Z", variable=self.sort_variable, value="code_az").pack(anchor='w')
        ttk.Radiobutton(code_frame, text="Z-A", variable=self.sort_variable, value="code_za").pack(anchor='w')
        name_frame = ttk.Labelframe(main_frame, text="College Name", padding=10)
        name_frame.pack(fill='x', pady=2)
        ttk.Radiobutton(name_frame, text="A-Z", variable=self.sort_variable, value="name_az").pack(anchor='w')
        ttk.Radiobutton(name_frame, text="Z-A", variable=self.sort_variable, value="name_za").pack(anchor='w')
        button_frame = ttk.Frame(main_frame, padding=(0, 15, 0, 0))
        button_frame.pack(fill='x', side='bottom')
        apply_button = ttk.Button(button_frame, text="Update Changes", bootstyle="primary", command=self.apply_sort)
        apply_button.pack(side='left', expand=True, padx=(0, 5), ipady=3)
        clear_button = ttk.Button(button_frame, text="Clear", bootstyle="info", command=self.clear_sort)
        clear_button.pack(side='left', expand=True, padx=5, ipady=3)
        cancel_button = ttk.Button(button_frame, text="Cancel", bootstyle="secondary", command=self.destroy)
        cancel_button.pack(side='right', expand=True, padx=(5, 0), ipady=3)
        self.grab_set()
    def apply_sort(self):
        selected_option = self.sort_variable.get()
        if selected_option and selected_option != 'None':
            self.master_app.current_college_sort_option = selected_option
            self.master_app.refresh_college_table(keyword=self.master_app.college_key_search.get())
        self.destroy()
    def clear_sort(self):
        self.master_app.current_college_sort_option = None
        self.master_app.refresh_college_table(keyword=self.master_app.college_key_search.get())
        self.destroy()
class StudentInformationSystem(tk.Tk):
    def __init__(self):
        super().__init__()
        self.style = ttk.Style("superhero")
        self.title("Student Information System Version 2")
        self.resizable(False, False)
        window_width = 1240
        window_height = 700
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        self.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        title_font_family = "Montserrat"
        available_fonts = list(tkfont.families())
        self.style.configure("WhiteTitle.TLabel", foreground="white", font=(title_font_family, 25, 'bold'))
        main_title_label = ttk.Label(self, text="STUDENT INFORMATION SYSTEM", style="WhiteTitle.TLabel", anchor="center")
        main_title_label.pack(pady=(10,5), fill='x')
        self.current_student_sort_option = None
        self.current_program_sort_option = None
        self.current_college_sort_option = None
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=(5,10))
        self.students_frame = ttk.Frame(self.notebook)
        self.program_frame = ttk.Frame(self.notebook)
        self.college_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.students_frame, text="Students")
        self.notebook.add(self.program_frame, text="Programs")
        self.notebook.add(self.college_frame, text="Colleges")
        self.setup_students_tab()
        self.setup_programs_tab()
        self.setup_colleges_tab()
        self.refresh_college_table()
        self.refresh_program_table()
        self.refresh_student_table()
    def setup_students_tab(self):
        self.student_buttons = ttk.Frame(self.students_frame)
        self.student_buttons.pack(side='left', fill='y', padx=10, pady=10)
        self.student_label = ttk.Label(self.student_buttons, text="STUDENTS", font=('Default', 20, 'bold'))
        self.student_label.pack(padx=10, pady=10)
        self.new_student_button = ttk.Button(self.student_buttons, text="CREATE STUDENT", width=20, bootstyle="success", command=self.new_student_button_callback)
        self.new_student_button.pack(padx=10, pady=10, fill='x', ipady=5)
        self.edit_student_button = ttk.Button(self.student_buttons, text='EDIT STUDENT', width=20, bootstyle="info", command=self.edit_student_button_callback)
        self.edit_student_button.pack(padx=10, pady=10, fill='x', ipady=5)
        self.delete_student_button = ttk.Button(self.student_buttons, text='DELETE STUDENT', width=20, bootstyle="danger", command=self.delete_student_button_callback)
        self.delete_student_button.pack(padx=10, pady=10, fill='x', ipady=5)
        self.sort_student_button = ttk.Button(self.student_buttons, text="SORT STUDENT", width=20, bootstyle="secondary", command=self.sort_student_button_callback)
        self.sort_student_button.pack(padx=10, pady=10, fill='x', ipady=5)
        self.student_content = ttk.Frame(self.students_frame)
        self.student_content.pack(side='right', fill='both', expand=True, padx=10, pady=10)
        self.search_frame = ttk.Frame(self.student_content)
        self.search_frame.pack(fill='x', pady=(0,10))
        self.search_label = ttk.Label(self.search_frame, text="Search:", font=('Default', 10))
        self.search_label.pack(side='left', padx=5)
        self.student_key_search = tk.StringVar()
        self.student_search_tab = ttk.Entry(self.search_frame, width=50, textvariable=self.student_key_search)
        self.student_search_tab.pack(side='left', fill='x', expand=True, padx=5)
        self.students_table = StudentTable(self.student_content)
        self.students_table.pack(fill='both', expand=True)
        self.student_key_search.trace_add("write", self.student_search)
    def setup_programs_tab(self):
        self.program_buttons = ttk.Frame(self.program_frame)
        self.program_buttons.pack(side='left', fill='y', padx=10, pady=10)
        self.program_label = ttk.Label(self.program_buttons, text="PROGRAMS", font=('Default', 20, 'bold'))
        self.program_label.pack(padx=10, pady=10)
        self.new_program_button = ttk.Button(self.program_buttons, text="CREATE PROGRAM", width=20, bootstyle="success", command=self.new_program_button_callback)
        self.new_program_button.pack(padx=10, pady=10, fill='x', ipady=5)
        self.edit_program_button = ttk.Button(self.program_buttons, text='EDIT PROGRAM', width=20, bootstyle="info", command=self.edit_program_button_callback)
        self.edit_program_button.pack(padx=10, pady=10, fill='x', ipady=5)
        self.delete_program_button = ttk.Button(self.program_buttons, text='DELETE PROGRAM', width=20, bootstyle="danger", command=self.delete_program_button_callback)
        self.delete_program_button.pack(padx=10, pady=10, fill='x', ipady=5)
        self.sort_program_button = ttk.Button(self.program_buttons, text="SORT PROGRAM", width=20, bootstyle="secondary", command=self.sort_program_button_callback)
        self.sort_program_button.pack(padx=10, pady=10, fill='x', ipady=5)
        self.program_content = ttk.Frame(self.program_frame)
        self.program_content.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        self.program_search_frame = ttk.Frame(self.program_content)
        self.program_search_frame.pack(fill='x', pady=(0,10))
        self.program_search_label = ttk.Label(self.program_search_frame, text="Search:", font=('Default', 10))
        self.program_search_label.pack(side='left', padx=5)
        self.program_key_search = tk.StringVar()
        self.program_search_tab = ttk.Entry(self.program_search_frame, width=50, textvariable=self.program_key_search)
        self.program_search_tab.pack(side='left', fill='x', expand=True, padx=5)
        self.program_table = ProgramTable(self.program_content)
        self.program_table.pack(fill='both', expand=True)
        self.program_key_search.trace_add("write", self.program_search)
    def setup_colleges_tab(self):
        self.college_buttons = ttk.Frame(self.college_frame)
        self.college_buttons.pack(side='left', fill='y', padx=10, pady=10)
        self.college_label = ttk.Label(self.college_buttons, text="COLLEGES", font=('Default', 20, 'bold'))
        self.college_label.pack(padx=10, pady=10)
        self.new_college_button = ttk.Button(self.college_buttons, text="CREATE COLLEGE", width=20, bootstyle="success", command=self.new_college_button_callback)
        self.new_college_button.pack(padx=10, pady=10, fill='x', ipady=5)
        self.edit_college_button = ttk.Button(self.college_buttons, text='EDIT COLLEGE', width=20, bootstyle="info", command=self.edit_college_button_callback)
        self.edit_college_button.pack(padx=10, pady=10, fill='x', ipady=5)
        self.delete_college_button = ttk.Button(self.college_buttons, text='DELETE COLLEGE', width=20, bootstyle="danger", command=self.delete_college_button_callback)
        self.delete_college_button.pack(padx=10, pady=10, fill='x', ipady=5)
        self.sort_college_button = ttk.Button(self.college_buttons, text="SORT COLLEGE", width=20, bootstyle="secondary", command=self.sort_college_button_callback)
        self.sort_college_button.pack(padx=10, pady=10, fill='x', ipady=5)
        self.college_content = ttk.Frame(self.college_frame)
        self.college_content.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        self.college_search_frame = ttk.Frame(self.college_content)
        self.college_search_frame.pack(fill='x', pady=(0,10))
        self.college_search_label = ttk.Label(self.college_search_frame, text="Search:", font=('Default', 10))
        self.college_search_label.pack(side='left', padx=5)
        self.college_key_search = tk.StringVar()
        self.college_search_tab = ttk.Entry(self.college_search_frame, width=50, textvariable=self.college_key_search)
        self.college_search_tab.pack(side='left', fill='x', expand=True, padx=5)
        self.college_table = CollegeTable(self.college_content)
        self.college_table.pack(fill='both', expand=True)
        self.college_key_search.trace_add("write", self.college_search)
    def dialog(self, text, title="Message"):
        toplevel = ttk.Toplevel(self)
        toplevel.title(title)
        toplevel.transient(self)
        window_width = 350
        window_height = 180
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        toplevel.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        message_frame = ttk.Frame(toplevel, padding=(20, 20))
        message_frame.pack(fill='both', expand=True)
        msg_label = ttk.Label(message_frame, text=text, wraplength=window_width-60, justify='center', anchor='center')
        msg_label.pack(expand=True, fill='both', pady=(0,15))
        button_frame = ttk.Frame(message_frame)
        button_frame.pack(side='bottom', pady=(0,5))
        ok_button = ttk.Button(button_frame, text='Okay', bootstyle="primary", width=10, command=toplevel.destroy)
        ok_button.pack()
        toplevel.grab_set()
    def confirmation(self, text, func, title="Confirmation"):
        toplevel = ttk.Toplevel(self)
        toplevel.title(title)
        toplevel.transient(self)
        window_width = 380
        window_height = 200
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        toplevel.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        def confirmed_action():
            func()
            toplevel.destroy()
        message_frame = ttk.Frame(toplevel, padding=(20,20))
        message_frame.pack(fill='both', expand=True)
        msg_label = ttk.Label(message_frame, text=text, wraplength=window_width-60, justify='center', anchor='center')
        msg_label.pack(expand=True, fill='both', pady=(0,15))
        button_frame = ttk.Frame(message_frame)
        button_frame.pack(side='bottom', pady=(0,5))
        yes_button = ttk.Button(button_frame, text="Yes", bootstyle="primary", width=10, command=confirmed_action)
        yes_button.pack(side='left', padx=(0,10))
        cancel_button = ttk.Button(button_frame, text="Cancel", bootstyle="secondary", width=10, command=toplevel.destroy)
        cancel_button.pack(side='right')
        toplevel.grab_set()
    def sort_student_button_callback(self):
        SortStudentDialog(self)
    def student_search(self, *args):
        self.refresh_student_table(self.student_key_search.get())
    def refresh_student_table(self, keyword=None):
        for item in self.students_table.get_children():
            self.students_table.delete(item)
        all_student_data = students.get_all(keyword=keyword)
        sort_option = self.current_student_sort_option
        if sort_option and all_student_data:
            year_level_map = {"First Year": 1, "Second Year": 2, "Third Year": 3, "Fourth Year": 4}
            sex_map = {"Male": 1, "Female": 2}
            key_func = None
            reverse_order = False
            if sort_option == 'lastname_az':
                key_func = lambda s: str(s.get("LASTNAME", "") or "").upper()
                reverse_order = False
            elif sort_option == 'lastname_za':
                key_func = lambda s: str(s.get("LASTNAME", "") or "").upper()
                reverse_order = True
            elif sort_option == 'firstname_az':
                key_func = lambda s: str(s.get("FIRSTNAME", "") or "").upper()
                reverse_order = False
            elif sort_option == 'firstname_za':
                key_func = lambda s: str(s.get("FIRSTNAME", "") or "").upper()
                reverse_order = True
            elif sort_option == 'id_asc':
                key_func = lambda s: s.get("studentID", "")
                reverse_order = False
            elif sort_option == 'id_desc':
                key_func = lambda s: s.get("studentID", "")
                reverse_order = True
            elif sort_option == 'sex_mf':
                key_func = lambda s: sex_map.get(s.get("SEX", ""), 3)
                reverse_order = False
            elif sort_option == 'sex_fm':
                key_func = lambda s: sex_map.get(s.get("SEX", ""), 3)
                reverse_order = True
            elif sort_option == 'program_az':
                key_func = lambda s: str(s.get("programCODE", "") or "z").upper()
                reverse_order = False
            elif sort_option == 'program_za':
                key_func = lambda s: str(s.get("programCODE", "") or "z").upper()
                reverse_order = True
            elif sort_option == 'year_asc':
                key_func = lambda s: year_level_map.get(s.get("YEAR LEVEL", ""), 99)
                reverse_order = False
            elif sort_option == 'year_desc':
                key_func = lambda s: year_level_map.get(s.get("YEAR LEVEL", ""), 99)
                reverse_order = True
            if key_func:
                all_student_data.sort(key=key_func, reverse=reverse_order)
        elif all_student_data:
            random.shuffle(all_student_data)
        for idx, student_record in enumerate(all_student_data):
            if not isinstance(student_record, dict): continue
            program_code_val = student_record.get("programCODE") or "NOT ENROLLED"
            sex_display = student_record.get("SEX") or "NO SELECTION"
            year_level_display = student_record.get("YEAR LEVEL") or "NO SELECTION"
            self.students_table.insert('', 'end', iid=f"student_{idx}", values=(
                student_record.get("studentID", "N/A"),
                student_record.get("FIRSTNAME", ""),
                student_record.get("LASTNAME", ""),
                sex_display,
                program_code_val,
                year_level_display))
    def new_student_button_callback(self): StudentInfo(self, 'new')
    def edit_student_button_callback(self):
        selected_item_iid = self.students_table.selection()
        if not selected_item_iid: return self.dialog("Please select a student from the table first.")
        item_values = self.students_table.item(selected_item_iid[0], 'values')
        if not item_values: return self.dialog("Cannot get student ID from table.", "Error!!")
        student_id_val = item_values[0]
        student_data_for_edit = None
        all_stud_records = students.get_all(filter_criteria={"studentID": student_id_val})
        if all_stud_records and len(all_stud_records) > 0:
            student_data_for_edit = all_stud_records[0]
        if not student_data_for_edit:
            return self.dialog(f"Could not retrieve details for student ID {student_id_val}.", "Error")
        StudentInfo(self, 'edit', student_data_for_edit)
    def delete_student_data(self):
        selected_item_iid = self.students_table.selection()
        if not selected_item_iid: return
        item_values = self.students_table.item(selected_item_iid[0], 'values')
        if not item_values: return self.dialog("Cannot get student ID from table.", "Error")
        student_id_val = item_values[0]
        if students.remove(student_id_val):
            self.dialog(f"Successfully deleted Student #{student_id_val}")
            self.refresh_student_table()
        else:
            self.dialog(f"Failed to delete Student #{student_id_val}", "Error")
    def delete_student_button_callback(self):
        selected_item_iid = self.students_table.selection()
        if not selected_item_iid: return self.dialog("Please select a student from the table first.")
        item_values = self.students_table.item(selected_item_iid[0], 'values')
        if not item_values: return self.dialog("Cannot get student ID from table.", "Error")
        student_id_val = item_values[0]
        self.confirmation(f"Do you want to delete student #{student_id_val}?", self.delete_student_data)
    def sort_program_button_callback(self):
        SortProgramDialog(self)
    def program_search(self, *args): self.refresh_program_table(self.program_key_search.get())
    def refresh_program_table(self, keyword=None):
        for item in self.program_table.get_children(): self.program_table.delete(item)
        all_program_data = programs.get_all(keyword=keyword)
        sort_option = self.current_program_sort_option
        if sort_option and all_program_data:
            key_func = None
            reverse_order = False
            if sort_option == 'code_az':
                key_func = lambda p: str(p.get("programID", "") or "").upper()
                reverse_order = False
            elif sort_option == 'code_za':
                key_func = lambda p: str(p.get("programID", "") or "").upper()
                reverse_order = True
            elif sort_option == 'name_az':
                key_func = lambda p: str(p.get("programNAME", "") or "").upper()
                reverse_order = False
            elif sort_option == 'name_za':
                key_func = lambda p: str(p.get("programNAME", "") or "").upper()
                reverse_order = True
            elif sort_option == 'college_az':
                key_func = lambda p: str(p.get("collegeCODE", "") or "z").upper()
                reverse_order = False
            elif sort_option == 'college_za':
                key_func = lambda p: str(p.get("collegeCODE", "") or "z").upper()
                reverse_order = True
            if key_func:
                all_program_data.sort(key=key_func, reverse=reverse_order)
        for idx, program_record in enumerate(all_program_data):
            if not isinstance(program_record, dict): continue
            college_code_val = program_record.get("collegeCODE") or "N/A"
            self.program_table.insert('', 'end', iid=f"program_{idx}", values=(
                program_record.get("programID", "N/A"),
                program_record.get("programNAME", ""),
                college_code_val))
    def new_program_button_callback(self): ProgramInfo(self, 'new')
    def edit_program_button_callback(self):
        selected_item_iid = self.program_table.selection()
        if not selected_item_iid: return self.dialog("Please select a program from the table first.")
        item_values = self.program_table.item(selected_item_iid[0], 'values')
        if not item_values: return self.dialog("Cannot get program ID from table.", "Error")
        program_id_val = item_values[0]
        program_data_for_edit = None
        all_prog_records = programs.get_all(filter_criteria={"programID": program_id_val})
        if all_prog_records and len(all_prog_records) > 0:
            program_data_for_edit = all_prog_records[0]
        if not program_data_for_edit:
            return self.dialog(f"Could not retrieve details for program ID {program_id_val}.", "Error")
        ProgramInfo(self, 'edit', program_data_for_edit)
    def delete_program_data(self):
        selected_item_iid = self.program_table.selection()
        if not selected_item_iid: return
        item_values = self.program_table.item(selected_item_iid[0], 'values')
        if not item_values: return self.dialog("Cannot get program ID from table.", "Error")
        program_id_val = item_values[0]
        if programs.remove(program_id_val):
            self.dialog(f"Successfully deleted the Program {program_id_val}.\nThe students under the program will now be marked as 'NOT ENROLLED'.")
        else:
            self.dialog(f"Failed to delete Program {program_id_val}.", "Error")
        self.refresh_student_table()
        self.refresh_program_table()
    def delete_program_button_callback(self):
        selected_item_iid = self.program_table.selection()
        if not selected_item_iid: return self.dialog("Please select a program from the table first.")
        item_values = self.program_table.item(selected_item_iid[0], 'values')
        if not item_values: return self.dialog("Cannot get program ID from table.", "Error")
        program_id_val = item_values[0]
        self.confirmation(f"Do you want to delete Program {program_id_val}?\nStudents under this program will be marked as 'NOT ENROLLED'.\nDo you want to continue?", self.delete_program_data)
    def sort_college_button_callback(self):
        SortCollegeDialog(self)
    def college_search(self, *args): self.refresh_college_table(self.college_key_search.get())
    def refresh_college_table(self, keyword=None):
        self.college_table.delete(*self.college_table.get_children())
        all_college_data = colleges.get_all(keyword=keyword)
        sort_option = self.current_college_sort_option
        if sort_option and all_college_data:
            key_func = None
            reverse_order = False
            if sort_option == 'code_az':
                key_func = lambda c: str(c.get("collegeCODE", "") or "").upper()
                reverse_order = False
            elif sort_option == 'code_za':
                key_func = lambda c: str(c.get("collegeCODE", "") or "").upper()
                reverse_order = True
            elif sort_option == 'name_az':
                key_func = lambda c: str(c.get("collegeNAME", "") or "").upper()
                reverse_order = False
            elif sort_option == 'name_za':
                key_func = lambda c: str(c.get("collegeNAME", "") or "").upper()
                reverse_order = True
            if key_func:
                all_college_data.sort(key=key_func, reverse=reverse_order)
        for idx, college_record in enumerate(all_college_data):
            if not isinstance(college_record, dict): continue
            self.college_table.insert('', 'end', iid=f"college_{idx}", values=[
                college_record.get("collegeCODE", "N/A"),
                college_record.get("collegeNAME", "")])
    def new_college_button_callback(self): CollegeInfo(self, 'new')
    def edit_college_button_callback(self):
        selected_item_iid = self.college_table.selection()
        if not selected_item_iid: return self.dialog("Please select a college from the table first.")
        item_values = self.college_table.item(selected_item_iid[0], 'values')
        if not item_values: return self.dialog("Cannot get college ID from table.", "Error")
        college_id_val = item_values[0]
        college_data_for_edit = None
        all_coll_records = colleges.get_all(filter_criteria={"collegeCODE": college_id_val})
        if all_coll_records and len(all_coll_records) > 0:
            college_data_for_edit = all_coll_records[0]
        if not college_data_for_edit:
            return self.dialog(f"Could not retrieve details for college ID {college_id_val}.", "Error")
        CollegeInfo(self, 'edit', college_data_for_edit)
    def delete_college_data(self):
        selected_item_iid = self.college_table.selection()
        if not selected_item_iid: return
        item_values = self.college_table.item(selected_item_iid[0], 'values')
        if not item_values: return self.dialog("Cannot get college ID from table.", "Error")
        college_id_val = item_values[0]
        if colleges.remove(college_id_val):
            self.dialog(f"Successfully deleted the College {college_id_val}.\nThe programs under this college are now unassigned.")
        else:
            self.dialog(f"Failed to delete College {college_id_val}.", "Error")
        self.refresh_student_table()
        self.refresh_program_table()
        self.refresh_college_table()
    def delete_college_button_callback(self):
        selected_item_iid = self.college_table.selection()
        if not selected_item_iid: return self.dialog("Please select a college from the table first.")
        item_values = self.college_table.item(selected_item_iid[0], 'values')
        if not item_values: return self.dialog("Cannot get college ID from table.", "Error")
        college_id_val = item_values[0]
        self.confirmation(f"Do you want to delete the College: {college_id_val}?\nThe programs under this will lose their college assignment.\nDo you want to continue?", self.delete_college_data)
    def start(self):
        self.mainloop()