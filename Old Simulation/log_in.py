# ============================================================================================================
# This module contains all functions for the log in screen
# Author Name: Teon Green
# Last Updated: 11/05/2022
# Bugs:
# ============================================================================================================

import tkinter as tk
from tkinter import ttk
from tkinter.colorchooser import askcolor
import tkinter.messagebox
from database_editor import connect_to_server, search_user, select_users, create_user, delete_user
import sys
from run_GUI import start_menu


# This function creates and displays the landing screen for the application
# 11

def landing_page():
    root = tk.Tk()

    root.geometry("670x400")
    root.configure(bg="#AEECE9")

    lp_welcome_label = tk.Label(root, text="Welcome to my Simulator!", borderwidth=0,
                                bg=root['bg'], font=("Helvetica", 25))
    lp_welcome_label.place(relx=0.2, rely=0.1, relwidth=0.6, relheight=0.1)
    lp_font = ("Helvetica", 10)

    # Where user will enter their username
    lp_name_label = tk.Label(root, text="Username:", borderwidth=2, relief="solid", font=lp_font)
    lp_name_label.place(relx=0.05, rely=0.3, relwidth=0.15, relheight=0.1)
    lp_name_entry = tk.Entry(root, borderwidth=2, relief="solid", font=lp_font, show="*")
    lp_name_entry.place(relx=0.2, rely=0.3, relwidth=0.75, relheight=0.1)

    # Where users will enter their password
    lp_password_label = tk.Label(root, text="Password:", borderwidth=2, relief="solid", font=lp_font)
    lp_password_label.place(relx=0.05, rely=0.5, relwidth=0.15, relheight=0.1)
    lp_password_entry = tk.Entry(root, borderwidth=2, relief="solid", show="*", font=lp_font)
    lp_password_entry.place(relx=0.2, rely=0.5, relwidth=0.75, relheight=0.1)

    # Button to exit the program
    lp_exit_button = tk.Button(root, text="Exit", command=lambda: sys.exit(),
                               borderwidth=3, relief="groove", font=lp_font)
    lp_exit_button.place(relx=0.05, rely=0.80, relwidth=0.1, relheight=0.1)

    # Button to log in with entered password and username
    lp_submit_button = tk.Button(root, text="Submit", command=lambda: validate(root, lp_name_entry.get(),
                                                                               lp_password_entry.get()),
                                 borderwidth=3, relief="groove", font=lp_font)
    lp_submit_button.place(relx=0.85, rely=0.80, relwidth=0.1, relheight=0.1)

    # lp_window_menu.add_command(label="Change Colour", command=lambda: choose_color())

    root.mainloop()


def admin_page():
    global ap_colour
    ap_colour = "#AEECE9"
    # Establishing a connection with the sql server
    connection = connect_to_server()
    # Dumping all users into a variable
    users = select_users(connection)
    users = []
    # Creating the root for the admin page
    admin_root = tk.Tk()
    admin_root.geometry("670x400")
    admin_root.configure(bg="#AEECE9")
    # Defining the style of the notebook to get a light blue background
    ap_notebook_style = ttk.Style()
    ap_notebook_style.configure('TNotebook', background=ap_colour)
    # Creating the notebook for the admin page
    admin_notebook = ttk.Notebook(admin_root)
    admin_notebook.place(relwidth=1, relheight=1)
    # Creating the 1st(Home) Page of the notebook
    ap_home_frame = tk.Frame(admin_notebook, bg=ap_colour, borderwidth=0)
    ap_home_frame.place(relheight=1, relwidth=1)
    admin_notebook.add(ap_home_frame, text='Home')
    # Creating the 2nd(Add User) Page of the notebook
    ap_add_frame = tk.Frame(admin_notebook, bg=ap_colour, borderwidth=0)
    ap_add_frame.place(relheight=1, relwidth=1)
    admin_notebook.add(ap_add_frame, text='Add User')
    # Creating the 3rd(Delete) Page of the notebook
    ap_delete_frame = tk.Frame(admin_notebook, bg=ap_colour, borderwidth=0)
    ap_delete_frame.place(relheight=1, relwidth=1)
    admin_notebook.add(ap_delete_frame, text='Delete User')
    # Creating the drop-down menu pf settings
    # ap_menu = Menu(admin_root)
    # admin_root.config(menu=ap_menu)
    # ap_window_menu = Menu(ap_menu)
    # ap_menu.add_cascade(label="Window", menu=ap_window_menu)
    # Welcome label of the home page
    ap_welcome_label = tk.Label(ap_home_frame, text="Welcome Admin!", borderwidth=0,
                                bg=admin_root['bg'], font=("sys", 25))
    ap_welcome_label.place(relx=0.2, rely=0.1, relwidth=0.6, relheight=0.1)

    ap_users_label = tk.Label(ap_home_frame, text="Current Users:", borderwidth=0, bg=admin_root['bg'],
                              font=("sys", 25), anchor="w")
    ap_users_label.place(rely=0.3, relwidth=0.35, relheight=0.1, anchor="w")
    # Frame to display all current users in
    ap_allusers_frame = tk.Frame(ap_home_frame, bg="#FFFFFF", borderwidth=3, relief="solid")
    ap_allusers_frame.place(rely=0.4, relwidth=1, relheight=0.6)

    current_placing = 0.1
    for user in users:
        formatted_data = f"Name: {user[0]} | Username: {user[1]} | Password: {user[2]}"
        temp_label = tk.Label(ap_allusers_frame, bg="#FFFFFF", text=formatted_data, font=("sys", 9), anchor="w")
        temp_label.place(rely=current_placing, relheight=0.09, relwidth=1)
        current_placing += 0.1

    # ap_allusers_scrollbar = ttk.Scrollbar(ap_home_frame, orient="vertical",
    #                                       command=ap_allusers_canvas.yview)
    # ap_allusers_frame = tk.Frame(ap_allusers_canvas)
    # ap_allusers_frame.bind("<Configure>", lambda e: ap_allusers_canvas.configure(
    #     scroll-region=ap_allusers_canvas.bbox("all")))

    # Adding an option to change the colour of the background

    # Code for add users frame
    add_welcome_label = tk.Label(ap_add_frame, bg="#FFFFFF", text="From this page you can add users to the database",
                                 font=("sys", 12), borderwidth=2, relief="solid")
    add_welcome_label.place(relx=0.2, rely=0.05, relwidth=0.6, relheight=0.1)
    add_name_label = tk.Label(ap_add_frame, bg=ap_colour, text="Fullname:", font=("sys", 10), anchor="w")
    add_name_label.place(rely=0.2, relwidth=0.1, relheight=0.1)
    add_name_entry = tk.Entry(ap_add_frame, bg="#FFFFFF", borderwidth=2, relief="solid")
    add_name_entry.place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.1)
    add_username_label = tk.Label(ap_add_frame, bg=ap_colour, text="Username:", font=("sys", 10), anchor="w")
    add_username_label.place(rely=0.4, relwidth=0.1, relheight=0.1)
    add_username_entry = tk.Entry(ap_add_frame, bg="#FFFFFF", borderwidth=2, relief="solid", show="*")
    add_username_entry.place(relx=0.1, rely=0.4, relwidth=0.8, relheight=0.1)
    add_password_label = tk.Label(ap_add_frame, bg=ap_colour, text="Password:", font=("sys", 10), anchor="w")
    add_password_label.place(rely=0.6, relwidth=0.1, relheight=0.1)
    add_password_entry = tk.Entry(ap_add_frame, bg="#FFFFFF", borderwidth=2, relief="solid", show="*")
    add_password_entry.place(relx=0.1, rely=0.6, relwidth=0.8, relheight=0.1)

    add_submit_button = tk.Button(ap_add_frame,
                                  bg="#FFFFFF", borderwidth=2, relief="groove", text="Submit",
                                  font=("sys", 12), command=lambda: create_user(connection, add_username_entry.get(),
                                                                                add_password_entry.get(),
                                                                                add_name_entry.get()))
    add_submit_button.place(relx=0.2, rely=0.8, relwidth=0.2, relheight=0.1)
    add_exit_button = tk.Button(ap_add_frame, bg="#FFFFFF", borderwidth=2, relief="groove", text="Exit",
                                font=("sys", 12), command=exit)
    add_exit_button.place(relx=0.6, rely=0.8, relwidth=0.2, relheight=0.1)

    # Code for delete users frame
    delete_welcome_label = tk.Label(ap_delete_frame, bg="#FFFFFF",
                                    text="From this page you can delete users from the database",
                                    font=("sys", 12), borderwidth=2, relief="solid")
    delete_welcome_label.place(relx=0.2, rely=0.05, relwidth=0.6, relheight=0.1)
    delete_username_label = tk.Label(ap_delete_frame, bg=ap_colour, text="Username:", font=("sys", 12), anchor="w")
    delete_username_label.place(rely=0.3, relwidth=0.15, relheight=0.1)
    delete_username_entry = tk.Entry(ap_delete_frame, bg="#FFFFFF", font=("sys", 12), borderwidth=2,
                                     relief="solid", show="*")
    delete_username_entry.place(relx=0.15, rely=0.3, relwidth=0.7, relheight=0.1)
    delete_confirm_label = tk.Label(ap_delete_frame, bg=ap_colour, font=("sys", 12), text="Admin Key:", anchor="w")
    delete_confirm_label.place(rely=0.5, relwidth=0.15, relheight=0.1)
    delete_confirm_entry = tk.Entry(ap_delete_frame, bg="#FFFFFF", font=("sys", 12), borderwidth=2,
                                    relief="solid", show="*")
    delete_confirm_entry.place(relx=0.15, rely=0.5, relwidth=0.7, relheight=0.1)
    delete_delete_button = tk.Button(ap_delete_frame, bg="#FFFFFF", font=("sys", 12), text="Delete",
                                     borderwidth=2, relief="solid",
                                     command=lambda: delete_login(connection, delete_username_entry.get(),
                                                                  delete_confirm_entry.get()))
    delete_delete_button.place(relx=0.6, rely=0.7, relwidth=0.2, relheight=0.1)

    admin_root.mainloop()


def validate(window_root, given_username, given_password):
    connection = connect_to_server()
    if given_username == "" or given_password == "":
        tkinter.messagebox.showerror("Error", "Username or Password cannot be empty")
        return
    else:
        result = search_user(connection, given_username, given_password)
        if not result:
            tkinter.messagebox.showerror("Error", "User not Found")
        elif result and given_username == "Admin":
            window_root.destroy()
            admin_page()
        else:
            window_root.destroy()
            start_menu()
            # placeholder For Simulation


def delete_login(connector, given_username, given_key):
    attempt = delete_user(connector, given_username, given_key)
    if attempt[1]:
        tkinter.messagebox.showinfo(message=f"{attempt[0]}")
    else:
        tkinter.messagebox.showerror(message=f"{attempt[0]}")


# 11111
if __name__ == "__main__":
    admin_page()
