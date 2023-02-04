import tkinter.messagebox
import customtkinter
from tkinter import *
from math import floor
from datetime import datetime
import pandas as pd


# GUI constants
BACKGROUND = "#29262e"
HOVER_COLOUR = "#e6c2a8"
BUTTON_COLOUR = "#a45957"
FONT = ("Better Together", 50, "bold")
TIMER = ""


def generate_data():
    # Function that calculates how many days and hours user has coded
    # See if user_data file exists, if not create one
    try:
        df = pd.read_csv("user_data.csv")
    except FileNotFoundError:
        # Create an empty DataFrame with two columns
        df = pd.DataFrame(columns=["Date", "Hours Coded"])
        # Write the DataFrame to a CSV file
        df.to_csv("user_data.csv", index=False)
    else:
        # Extract Column A as a list
        days = df["Date"].tolist()
        # Remove duplicates
        days = [*set(days)]
        # Sum column B, total hours coded
        total_hours = round(df["Hours Coded"].sum(), 1)
        return len(days), total_hours


class GuiCtk(customtkinter.CTk):
    """Activate GUI"""

    def __init__(self):
        super().__init__()
        self.count = 0
        self.timer = "00:00:00"

        self.title("My Coding Journey")
        self.config(padx=50, pady=30, bg=BACKGROUND, highlightthickness=0)

        # Add image
        self.image = PhotoImage(file="coding_journey.png")
        card_canvas = Canvas(width=400, height=400, bg=BACKGROUND, highlightthickness=0)
        card_canvas.create_image(200, 200, image=self.image)
        card_canvas.grid(column=0, row=2, columnspan=2)

        # Run data generation
        [self.days_coded, self.hours_coded] = generate_data()

        # Add labels
        self.title_label = Label(text="My Coding Journey", bg=BACKGROUND, fg="white",
                                 font=("Better Together", 60), width=15)
        self.title_label.grid(column=0, row=0, columnspan=2)

        self.streak_label = Label(text=f"Days Coded: {self.days_coded}", bg=BACKGROUND, fg="white",
                                  font=("Better Together", 30), width=15)
        self.streak_label.grid(column=0, row=1)

        self.total_label = Label(text=f"Total Hours Coded: {self.hours_coded}", bg=BACKGROUND, fg="white",
                                 font=("Better Together", 30), width=15)
        self.total_label.grid(column=1, row=1)

        self.timer_label = Label(text=f"TIMER: {self.timer}", bg=BACKGROUND, fg="white",
                                 font=("Squarely", 40), width=15)
        self.timer_label.grid(column=0, row=3, columnspan=2)

        # Add buttons
        self.start_button = customtkinter.CTkButton(master=self, text="START", command=self.start_timer,
                                                    hover_color=HOVER_COLOUR, fg_color=BUTTON_COLOUR, width=120,
                                                    font=("Better Together", 30))
        self.start_button.grid(column=0, row=4)
        self.stop_button = customtkinter.CTkButton(master=self, text="STOP", command=self.stop_timer,
                                                   hover_color=HOVER_COLOUR, fg_color=BUTTON_COLOUR, width=120,
                                                   font=("Better Together", 30))
        self.stop_button.grid(column=0, row=5, pady=20)
        self.finish_button = customtkinter.CTkButton(master=self, text="FINISH", command=self.finish,
                                                     hover_color=HOVER_COLOUR, fg_color=BUTTON_COLOUR, width=120,
                                                     font=("Better Together", 30))
        self.finish_button.grid(column=1, row=4)

    def start_timer(self):
        # Function that starts the timer
        global TIMER
        self.count += 1
        secs = self.count % 60
        if secs < 10:
            secs = f"0{secs}"
        mins = int((self.count / 60) % 60)
        if mins < 10:
            mins = f"0{mins}"
        hours = floor(self.count/3600)
        if hours < 10:
            hours = f"0{hours}"
        self.timer_label.config(text=f"TIMER: {hours}:{mins}:{secs}")
        TIMER = self.after(1000, func=self.start_timer)

    def stop_timer(self):
        # Function that stops the timer
        global TIMER
        self.after_cancel(TIMER)

    def finish(self):
        # Function that updates the csv file with date and hours coded
        hours = round(self.count / 3600, 5)
        mins = round(self.count / 60, 2)
        response = tkinter.messagebox.askyesno(title="Coding Journey",
                                               message=f"Do you want to log {mins} mins?")
        if response:
            today = datetime.today().strftime("%Y%m%d")
            # Create list of data
            data = [[today, hours]]
            # Convert list to dataframe
            df = pd.DataFrame(data, columns=["Date", "Hours Coded"])
            # Write the DataFrame to a CSV file
            df.to_csv('user_data.csv', mode='a', index=False, header=False)
        self.quit()


if __name__ == "__main__":
    app = GuiCtk()
    app.mainloop()
