import calendar
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog

import json
from datetime import date

# Color palette
yellow = "#f18d00"
brown = "#180e00"
blue = "#64a7e8"
darkgray = "#101418"
white = "#ffffff"
black = "#000000"
lt_yellow = "#fadcb2"

# Create the main application window
class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calendar App with Reminders")
        self.root.geometry("800x600")
        self.root.configure(bg=yellow)

        self.current_year = 2025
        self.current_month = 1

        self.reminders = self.load_reminders()

        self.create_widgets()
        self.display_calendar()

    def create_widgets(self):
        # Container
        full_frame = tk.Frame(self.root, bg="white")
        full_frame.pack(padx=10, fill="y", expand=True)

        # Navigation frame
        nav_frame = tk.Frame(full_frame, bg="white")
        nav_frame.pack(pady=10, padx=10)

        self.prev_button = tk.Button(nav_frame, text="<", command=self.prev_month, fg=yellow, bg="white", borderwidth=0, font=("Helvetica", 16, "bold"))
        self.prev_button.pack(side=tk.LEFT, padx=10)

        self.label = tk.Label(nav_frame, text="", fg="black", bg="white", borderwidth=0, font=("Helvetica", 16, "bold"))
        self.label.pack(side=tk.LEFT)

        self.next_button = tk.Button(nav_frame, text=">", command=self.next_month, fg=yellow, bg="white", borderwidth=0, font=("Helvetica", 16, "bold"))
        self.next_button.pack(side=tk.RIGHT, padx=10)

        # Calendar display frame
        self.calendar_frame = tk.Frame(full_frame, bg="white")
        self.calendar_frame.pack(expand=True, padx=50, pady=5)

        # Reminder input area
        self.reminder_frame = tk.Frame(full_frame, bg=lt_yellow)
        self.reminder_frame.pack(pady=10, padx=20, expand=True)

        tk.Label(self.reminder_frame, text="Day:", bg=lt_yellow, fg=brown, font=("Helvetica", 12, "bold")).grid(row=0, column=0, padx=5, pady=2)
        self.day_entry = tk.Entry(self.reminder_frame, width=20, font=("Helvetica", 12, "bold"))
        self.day_entry.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(self.reminder_frame, text="Month:", bg=lt_yellow, fg=brown, font=("Helvetica", 12, "bold")).grid(row=1, column=0, padx=5, pady=2)
        self.month_entry = tk.Entry(self.reminder_frame, width=20, font=("Helvetica", 12, "bold"))
        self.month_entry.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(self.reminder_frame, text="Reminder:", bg=lt_yellow, fg=brown, font=("Helvetica", 12, "bold")).grid(row=2, column=0, padx=5, pady=2)
        self.reminder_entry = tk.Entry(self.reminder_frame, width=20, font=("Helvetica", 12, "bold"))
        self.reminder_entry.grid(row=2, column=1, padx=5, pady=2)

        save_button = tk.Button(self.reminder_frame, text="Save", command=self.set_reminder, bg=yellow, fg="#fff", font=("Helvetica", 11), relief=FLAT)
        save_button.grid(row=3, column=0, padx=10, pady=5)

        self.manage_button = tk.Button(self.reminder_frame, text="Manage", command=self.manage_reminders, bg=blue, fg="white", font=("Helvetica", 11), relief=FLAT)
        self.manage_button.grid(row=3, column=1, padx=10, pady=5)

    def display_calendar(self):
        # Clear previous calendar
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        # Display the month and year
        self.label.config(text=f"{calendar.month_name[self.current_month]} {self.current_year}")

        # Get the month's calendar
        month_calendar = calendar.monthcalendar(self.current_year, self.current_month)
        days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

        # Highlight today's date
        today = date.today()
        is_current_month = (self.current_year == today.year and self.current_month == today.month)

        # Display day labels
        for col, day in enumerate(days_of_week):
            tk.Label(self.calendar_frame, text=day, width=8, height=2, bg=yellow, fg="black", font=("Helvetica", 10, "bold")).grid(row=0, column=col, padx=1, pady=1)

        # Display days
        for row, week in enumerate(month_calendar):
            for col, day in enumerate(week):
                day_label = tk.Label(self.calendar_frame, text=str(day) if day != 0 else "", width=8, height=3, fg=black, bg=lt_yellow, font=("Helvetica", 10, "bold"))
                

                if day != 0 and (day, self.current_month, self.current_year) in self.reminders:
                    day_label.config(bg="#f8c67f", fg="red")  # Highlight days with reminders
                    day_label.bind("<Button-1>", lambda event, d=day: self.view_day_reminders(d))  # Add click event
                if is_current_month and day == today.day:
                    day_label.config(bg="#f3a332", fg=white)  # Highlight today's date
                day_label.grid(row=row + 1, column=col, pady=1)

    def set_reminder(self):
        try:
            day = int(self.day_entry.get())
            month = int(self.month_entry.get())
            if day < 1 or day > calendar.monthrange(self.current_year, month)[1]:
                raise ValueError("Invalid day")

            if month < 1 or month > 12:
                raise ValueError("Invalid month")

            reminder_text = self.reminder_entry.get()
            if reminder_text.strip():
                self.reminders[(day, month, self.current_year)] = reminder_text
                self.save_reminders()
                self.display_calendar()
                messagebox.showinfo("Success", "Reminder set successfully!")
                self.day_entry.delete(0, END)
                self.month_entry.delete(0, END)
                self.reminder_entry.delete(0, END)
            else:
                messagebox.showwarning("Warning", "Reminder text cannot be empty.")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def manage_reminders(self):
        manage_window = tk.Toplevel(self.root)
        manage_window.title("Manage Reminders")
        manage_window.geometry("400x400")
        manage_window.configure(bg=lt_yellow)

        for reminder, text in self.reminders.items():
            reminder_text = f"{reminder[0]}/{reminder[1]}/{reminder[2]}: {text}"
            frame = tk.Frame(manage_window, bg=lt_yellow,)
            frame.pack(fill="x", padx=10, pady=5)

            tk.Label(frame, text=reminder_text, bg=lt_yellow, font=("Helvetica", 10, "bold")).pack(side=tk.LEFT)
            tk.Button(frame, text="Edit", command=lambda r=reminder: self.edit_reminder(r), bg=yellow, fg=white, font=("Helvetica", 8), relief=FLAT).pack(side=tk.RIGHT, padx=5)
            tk.Button(frame, text="Delete", command=lambda r=reminder: self.delete_reminder(r), bg="red", fg=white, font=("Helvetica", 8), relief=FLAT).pack(side=tk.RIGHT)

    def edit_reminder(self, reminder):
        day, month, year = reminder
        new_text = simpledialog.askstring("Edit Reminder", f"Edit reminder for {day}/{month}/{year}:")
        if new_text:
            self.reminders[reminder] = new_text
            self.save_reminders()
            self.display_calendar()
            messagebox.showinfo("Success", "Reminder updated successfully!")
            
    def delete_reminder(self, reminder):
        if messagebox.askyesno("Delete Reminder", "Are you sure you want to delete this reminder?"):
            del self.reminders[reminder]
            self.save_reminders()
            self.display_calendar()
            messagebox.showinfo("Success", "Reminder deleted successfully!")
        else:
            self.manage_reminders()

    def view_day_reminders(self, day):
        reminders = [text for (d, m, y), text in self.reminders.items() if d == day and m == self.current_month and y == self.current_year]
        if reminders:
            reminder_text = "\n".join(reminders)
            messagebox.showinfo("Reminders", f"Reminders for {day}/{self.current_month}/{self.current_year}:\n{reminder_text}")
        else:
            messagebox.showinfo("Reminders", f"No reminders for {day}/{self.current_month}/{self.current_year}.")

    def prev_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.display_calendar()

    def next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.display_calendar()

    def save_reminders(self):
        with open("reminders.json", "w") as file:
            json.dump({f"{key[0]}-{key[1]}-{key[2]}": value for key, value in self.reminders.items()}, file)

    def load_reminders(self):
        try:
            with open("reminders.json", "r") as file:
                return {tuple(map(int, k.split("-"))): v for k, v in json.load(file).items()}
        except (FileNotFoundError, json.JSONDecodeError):
            return {}


# Run the application
if __name__ == "__main__":
    root = Tk()
    app = CalendarApp(root)
    root.mainloop()
