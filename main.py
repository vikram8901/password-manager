from tkinter import *
from tkinter import messagebox
import json
import random
import string
import pyperclip

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = string.ascii_letters
    numbers = string.digits
    symbols = "!@#$%^&*()"

    password = (
        random.choice(letters) +
        random.choice(numbers) +
        random.choice(symbols) +
        ''.join(random.choice(letters + numbers + symbols) for _ in range(9))
    )

    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    if len(website) == 0 or len(password) == 0:
        messagebox.showerror("Error", "Please don't leave fields empty.")
        return

    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

    data.update(new_data)

    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)

    website_entry.delete(0, END)
    password_entry.delete(0, END)

# ---------------------------- SEARCH PASSWORD ------------------------------- #
def search_password():
    website = website_entry.get()

    try:
        with open("data.json", "r") as file:
            data = json.load(file)

        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(
                title=website,
                message=f"Email: {email}\nPassword: {password}"
            )
        else:
            messagebox.showerror("Not Found", "No details found.")

    except FileNotFoundError:
        messagebox.showerror("Error", "No data file found.")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

Label(text="Website:").grid(row=0, column=0)
Label(text="Email:").grid(row=1, column=0)
Label(text="Password:").grid(row=2, column=0)

website_entry = Entry(width=35)
website_entry.grid(row=0, column=1)
website_entry.focus()

email_entry = Entry(width=35)
email_entry.grid(row=1, column=1)
email_entry.insert(0, "you@example.com")

password_entry = Entry(width=21)
password_entry.grid(row=2, column=1)

Button(text="Generate", command=generate_password).grid(row=2, column=2)
Button(text="Save", width=36, command=save_password).grid(row=3, column=1, columnspan=2)
Button(text="Search", command=search_password).grid(row=0, column=2)

window.mainloop()
