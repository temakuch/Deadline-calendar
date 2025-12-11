import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import calendar
from datetime import datetime
<<<<<<< Updated upstream
=======
from db import DatabaseManager
>>>>>>> Stashed changes

class DeadlineCalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Deadline Calendar")
        self.root.geometry("900x600")

<<<<<<< Updated upstream
=======
        self.db = DatabaseManager()
>>>>>>> Stashed changes

        self.current_date = datetime.now()
        self.selected_date = self.current_date.strftime("%Y-%m-%d")
        self.year = self.current_date.year
        self.month = self.current_date.month

        self.setup_ui()
        self.draw_calendar_grid()
        self.update_event_list()

    def setup_ui(self):
        """Налаштування розмітки вікна"""

        self.left_frame = tk.Frame(self.root, width=500, bg="#f0f0f0", padx=10, pady=10)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.right_frame = tk.Frame(self.root, width=350, bg="white", padx=10, pady=10)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH)

        nav_frame = tk.Frame(self.left_frame, bg="#f0f0f0")
        nav_frame.pack(fill=tk.X, pady=5)
        
        tk.Button(nav_frame, text="< Попер.", command=self.prev_month).pack(side=tk.LEFT)
        self.month_label = tk.Label(nav_frame, text="", font=("Arial", 16, "bold"), bg="#f0f0f0")
        self.month_label.pack(side=tk.LEFT, expand=True)
        tk.Button(nav_frame, text="Наст. >", command=self.next_month).pack(side=tk.RIGHT)

        self.calendar_frame = tk.Frame(self.left_frame, bg="#f0f0f0")
        self.calendar_frame.pack(expand=True, fill=tk.BOTH)

        tk.Label(self.right_frame, text="Дедлайни на дату:", font=("Arial", 12), bg="white").pack(anchor="w")
        self.lbl_selected_date = tk.Label(self.right_frame, text=self.selected_date, font=("Arial", 16, "bold"), fg="#d32f2f", bg="white")
        self.lbl_selected_date.pack(anchor="w", pady=(0, 10))

        columns = ("time", "title")
        self.tree = ttk.Treeview(self.right_frame, columns=columns, show="headings", height=15)
        self.tree.heading("time", text="Час")
        self.tree.heading("title", text="Завдання")
        self.tree.column("time", width=50)
        self.tree.column("title", width=200)
        self.tree.pack(fill=tk.BOTH, expand=True)

        btn_frame = tk.Frame(self.right_frame, bg="white")
        btn_frame.pack(fill=tk.X, pady=10)
        tk.Button(btn_frame, text="Додати дедлайн", bg="#4caf50", fg="white", command=self.open_add_window).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        tk.Button(btn_frame, text="Видалити", bg="#f44336", fg="white", command=self.delete_selected_event).pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=2)

    def draw_calendar_grid(self):
        """Малює сітку календаря"""
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        month_name = calendar.month_name[self.month]
        self.month_label.config(text=f"{month_name} {self.year}")

        days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Нд"]
        for idx, day in enumerate(days):
            tk.Label(self.calendar_frame, text=day, bg="#ddd", width=5).grid(row=0, column=idx, sticky="nsew", padx=1, pady=1)

        cal = calendar.monthcalendar(self.year, self.month)
        
        for r, week in enumerate(cal):
            for c, day in enumerate(week):
                if day != 0:
                    date_val = f"{self.year}-{self.month:02d}-{day:02d}"
                    btn_bg = "white"
                    if date_val == self.selected_date:
                        btn_bg = "#add8e6"
                    elif date_val == datetime.now().strftime("%Y-%m-%d"):
                        btn_bg = "#e0ffe0"

                    events = self.db.get_events_by_date(date_val)
                    fg_color = "red" if events else "black"
                    font_style = ("Arial", 10, "bold") if events else ("Arial", 10)

                    btn = tk.Button(self.calendar_frame, text=str(day), bg=btn_bg, fg=fg_color, font=font_style,
                                    command=lambda d=day: self.select_day(d))
                    btn.grid(row=r+1, column=c, sticky="nsew", padx=1, pady=1)

        for i in range(7):
            self.calendar_frame.columnconfigure(i, weight=1)
        for i in range(len(cal) + 1):
            self.calendar_frame.rowconfigure(i, weight=1)

    def select_day(self, day):
        self.selected_date = f"{self.year}-{self.month:02d}-{day:02d}"
        self.lbl_selected_date.config(text=self.selected_date)
        self.draw_calendar_grid()
        self.update_event_list()

    def prev_month(self):
        self.month -= 1
        if self.month == 0:
            self.month = 12
            self.year -= 1
        self.draw_calendar_grid()

    def next_month(self):
        self.month += 1
        if self.month == 13:
            self.month = 1
            self.year += 1
        self.draw_calendar_grid()

    def update_event_list(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        events = self.db.get_events_by_date(self.selected_date)
        for event in events:
            self.tree.insert("", "end", values=(event[4], event[1]), iid=event[0])

    def open_add_window(self):
        top = tk.Toplevel(self.root)
        top.title("Новий дедлайн")
        top.geometry("300x300")

        tk.Label(top, text="Назва задачі:").pack(pady=5)
        e_title = tk.Entry(top)
        e_title.pack(pady=5)

        tk.Label(top, text="Опис:").pack(pady=5)
        e_desc = tk.Entry(top)
        e_desc.pack(pady=5)

        tk.Label(top, text="Час (HH:MM):").pack(pady=5)
        e_time = tk.Entry(top)
        e_time.insert(0, "23:59")
        e_time.pack(pady=5)

        def save():
            title = e_title.get()
            desc = e_desc.get()
            time = e_time.get()
            if title:
                self.db.add_event(title, desc, self.selected_date, time)
                self.update_event_list()
                self.draw_calendar_grid()
                top.destroy()
            else:
                messagebox.showwarning("Помилка", "Введіть назву!")

        tk.Button(top, text="Зберегти", bg="#4caf50", fg="white", command=save).pack(pady=20)

    def delete_selected_event(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        event_id = selected_item[0]
        self.db.delete_event(event_id)
        self.update_event_list()
        self.draw_calendar_grid()