import tkinter as tk
import ttkbootstrap as ttk
import mysql.connector
from ..database import programs, colleges, students, get_db_connection

class ProgramInfo(tk.Toplevel):
    def __init__(self, master, mode: str, data: dict = None):
        super().__init__(master=master)
        self.mode = mode
        self.data = data
        self.transient(master)
        window_width = 350
        window_height = 300
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        self.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        self.title('New Program' if mode == 'new' else 'Edit Program Information')
        form_frame = ttk.Frame(self, padding=20)
        form_frame.pack(fill='both', expand=True)
        ttk.Label(form_frame, text="PROGRAM CODE", font=('Default', 10)).pack(pady=(0,5), anchor='w')
        self.id_entry = ttk.Entry(form_frame)
        self.id_entry.pack(padx=0, fill='x', pady=(0,10))
        ttk.Label(form_frame, text="PROGRAM NAME", font=('Default', 10)).pack(pady=(0,5), anchor='w')
        self.name_entry = ttk.Entry(form_frame)
        self.name_entry.pack(padx=0, fill='x', pady=(0,10))
        ttk.Label(form_frame, text="COLLEGE", font=('Default', 10)).pack(pady=(0,5), anchor='w')
        college_codes_list = [ccode for ccode in colleges.get_college_ids() if ccode]
        if not college_codes_list or college_codes_list[0] != "No Selection":
            college_codes_list.insert(0, "No Selection")
        self.college_option = ttk.Combobox(form_frame, values=college_codes_list, state='readonly')
        self.college_option.pack(fill='x', padx=0, pady=(0,20))
        self.buttons_frame = ttk.Frame(form_frame)
        self.create_button = ttk.Button(self.buttons_frame, text="Create" if mode == 'new' else 'Save Changes', width=15, bootstyle="success" if mode == 'new' else "primary", command=self.create_button_callback)
        self.create_button.pack(side='left', fill='x', expand=True, padx=(0,5), ipady=3)
        self.cancel_button = ttk.Button(self.buttons_frame, text="Cancel", width=15, bootstyle="secondary", command=self.destroy)
        self.cancel_button.pack(side='right', fill='x', expand=True, padx=(5,0), ipady=3)
        self.buttons_frame.pack(side='bottom', padx=0, pady=(10,0), fill='x')
        if self.data is not None:
            self.id_entry.insert(0, self.data.get('programID', ''))
            self.name_entry.insert(0, self.data.get("programNAME", ''))
            current_college_code = self.data.get("collegeCODE", "No Selection")
            self.college_option.set(current_college_code if current_college_code in college_codes_list else "No Selection")
        else:
            self.college_option.set("No Selection")
        self.grab_set()

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
        outer_frame = ttk.Frame(toplevel)
        outer_frame.pack(expand=True, fill='both', padx=10, pady=10)
        msg_label = ttk.Label(outer_frame, text=text, wraplength=window_width-60, justify='center', anchor='center')
        msg_label.pack(expand=True, fill='both', pady=(0,15))
        button_frame = ttk.Frame(outer_frame)
        button_frame.pack(side='bottom', pady=(0,5))
        ok_button = ttk.Button(button_frame, text='OK', width=10, command=toplevel.destroy, bootstyle="primary")
        ok_button.pack()
        toplevel.grab_set()

    def create_button_callback(self):
        prog_id_val = self.id_entry.get().strip()
        prog_name_val = self.name_entry.get().strip()
        selected_college_code = self.college_option.get()
        db_college_code = selected_college_code if selected_college_code != "No Selection" else None
        current_data_payload = {"programID": prog_id_val, "programNAME": prog_name_val, "collegeCODE": db_college_code}

        if not prog_id_val or not prog_name_val:
            return self.dialog("Program Code and Program Name are required.", "Input Error")

        if self.mode == 'new':
            if programs.check(prog_id_val): return self.dialog("This program code already exists!!", "Please try again.")
            programs.insert_one(current_data_payload)
            self.dialog(f"Successfully created the Program: {prog_id_val}", "Success!!!")
        else:
            original_prog_id = self.data.get('programID')
            if self.data and original_prog_id == prog_id_val and self.data.get("programNAME", "") == prog_name_val and self.data.get("collegeCODE") == db_college_code:
                return self.dialog("No changes were made. Please try again.", "Information")

            if original_prog_id != prog_id_val:
                if programs.check(prog_id_val):
                    return self.dialog("The new Program Code you just entered already exists.", "Update Error")
                
                conn = None
                try:
                    conn = get_db_connection()
                    if conn is None:
                        raise mysql.connector.Error("Failed to establish database connection.")
                    cursor = conn.cursor()
                    
                    cursor.execute("SET foreign_key_checks = 0;")
                    
                    update_program_query = "UPDATE programs SET programID = %s, programNAME = %s, collegeCODE = %s WHERE programID = %s"
                    cursor.execute(update_program_query, (prog_id_val, prog_name_val, db_college_code, original_prog_id))
                    
                    update_students_query = "UPDATE students SET programCODE = %s WHERE programCODE = %s"
                    cursor.execute(update_students_query, (prog_id_val, original_prog_id))
                    
                    cursor.execute("SET foreign_key_checks = 1;")
                    
                    conn.commit()
                    self.dialog(f"Successfully updated the Program.", "Success!!!")
                
                except mysql.connector.Error as err:
                    if conn:
                        conn.rollback()
                    self.dialog(f"A database error occurred: {err}", "Update Error")
                finally:
                    if conn and conn.is_connected():
                        conn.close()
            else:
                programs.edit(original_prog_id, current_data_payload)
                self.dialog(f"Successfully updated the Program: {original_prog_id}", "Success!!!")
        
        if hasattr(self.master, 'refresh_program_table'): self.master.refresh_program_table()
        if hasattr(self.master, 'refresh_student_table'): self.master.refresh_student_table()
        self.destroy()