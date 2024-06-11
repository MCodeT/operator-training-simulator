import tkinter as tk
from tkinter import ttk
import serial
import time

arduino = serial.Serial('COM6', 9600)

window = tk.Tk()
window.configure(bg="white")

# Set the window size to 90% of the screen size
window_width = int(window.winfo_screenwidth() * 0.9)
window_height = int(window.winfo_screenheight() * 0.9)
window.geometry(f"{window_width}x{window_height}")


def create_header(parent):
    # Add bd and relief parameters for border
    header = tk.Frame(parent, height=50, bg='gray', bd=2, relief="solid")
    header.grid(row=0, column=0, sticky="ew")
    parent.grid_columnconfigure(0, weight=1)  # Make column 0 stretchable

    # Load the logo image
    # Adjust the path to your logo file
    logo = tk.PhotoImage(file="src/Yazaki_Group_Logo.png")
    logo = logo.subsample(10, 10)
    logo_label = tk.Label(header, image=logo, bg='gray')
    logo_label.image = logo  # Keep a reference to avoid garbage collection
    logo_label.grid(row=0, column=0, padx=10, pady=30, sticky="nw")

    # Create title label
    title_label = tk.Label(
        header, text="Operator Training Simulator", bg='gray', font=("Arial", 40))
    title_label.grid(row=0, column=0, padx=10, pady=10, sticky="n")
    parent.grid_columnconfigure(0, weight=1)  # Make column 0 stretchable
    # Center the title label
    title_label.place(relx=0.5, rely=0.5, anchor="center")

    return header


def on_closing():
    arduino.write(b'0')
    arduino.close()
    window.destroy()


def countdown_screen():
    # Remove the main menu screen
    for widget in window.winfo_children():
        widget.destroy()
    create_header(window)

    # Set background color for the frame
    countdown_screen = tk.Frame(window, bg='white')
    countdown_screen.grid(row=0, column=0)
    # Center the countdown screen
    countdown_screen.place(relx=0.5, rely=0.5, anchor="center")

    # Exit button
    exit_button = tk.Button(countdown_screen, text="Cancel", command=lambda: [
                            countdown_screen.destroy(), create_main_menu()], font=("Arial", 16), width=10, height=2, bg="red")
    exit_button.pack(side="bottom", pady=20)

    countdown_label = tk.Label(countdown_screen, text="", font=(
        # Set bg and highlightbackground to the same value
        "Arial", 72), bg='white', highlightbackground='white')
    countdown_label.pack(pady=50)

    def countdown(seconds):
        if seconds > 0:
            countdown_label.config(text=seconds)
            window.after(1000, countdown, seconds - 1)
        else:
            countdown_label.config(text="Go!")
            start_test()

    countdown(3)


def start_test():
    for widget in window.winfo_children():
        widget.destroy()

    create_header(window)

    initial_time = 101

    # Create the game screen
    # Set background color for the frame
    game_screen = tk.Frame(window, bg='white')
    game_screen.grid(row=0, column=0)
    # Center the game screen
    game_screen.place(relx=0.5, rely=0.5, anchor="center")

    counter = 0
    start_time = time.time()

    countdown_label = tk.Label(game_screen, text="Time Left: 5", font=(
        "Arial", 16), bg='white', fg='black')  # Set bg to white and fg to black
    countdown_label.pack(pady=10)
    counter_label = tk.Label(game_screen, text="Counter: " + str(counter), font=(
        "Arial", 16), bg='white', fg='black')  # Set bg to white and fg to black
    counter_label.pack(pady=10)

    success_label = tk.Label(game_screen, text="Success!", font=(
        "Arial", 24), fg="green", bg='white')  # Set background color for the label
    failure_label = tk.Label(game_screen, text="Failure!", font=(
        "Arial", 24), fg="red", bg='white')  # Set background color for the label

    progress_bar = ttk.Progressbar(game_screen, orient="horizontal", length=200,
                                   mode="determinate", maximum=initial_time)  # Set maximum value
    progress_bar.pack(pady=10)

    def test():
        nonlocal counter
        remaining_time = initial_time - (time.time() - start_time)
        countdown_label.config(text="Time Left: " + str(int(remaining_time)))
        progress_bar['value'] = remaining_time  # Update progress bar value

        if arduino.in_waiting > 0:
            message = arduino.readline().decode('utf-8').strip()
            if message == "Hole detected":
                counter += 1
                counter_label.config(text="Counter: " + str(counter))

        if remaining_time <= 0:
            if counter >= 10:
                success_label.pack()
            else:
                failure_label.pack()
                # Add a button to go back to the main menu
                back_button = tk.Button(game_screen, text="Back to Menu", command=create_main_menu, font=(
                    "Arial", 16), width=15, height=2, bg='white')  # Set bg to white
                back_button.pack(pady=20)
        else:
            window.after(100, test)
    test()


def create_main_menu():

    for widget in window.winfo_children():
        widget.destroy()

    create_header(window)
    main_menu = tk.Frame(window)
    main_menu.configure(bg="white")
    main_menu.grid(row=1, column=0, pady=50)  # Adjust pady as needed
    # Difficulty settings
    difficulty_label = tk.Label(
        main_menu, text="Select Difficulty:", font=("Arial", 16), bg='white')
    difficulty_label.grid(row=0, column=0, pady=10)

    difficulty_var = tk.StringVar()
    difficulty_var.set("Easy")  # Default difficulty setting

    difficulty_options = ["Easy", "Medium", "Hard"]
    difficulty_menu = tk.OptionMenu(
        main_menu, difficulty_var, *difficulty_options)
    difficulty_menu.config(font=("Arial", 14))
    difficulty_menu.grid(row=1, column=0, pady=10)

    # Start button
    start_button = tk.Button(main_menu, text="Start", command=countdown_screen, font=(
        "Arial", 16), width=10, height=2)
    start_button.grid(row=2, column=0, pady=20)
    # Exit button
    exit_button = tk.Button(main_menu, text="Exit", command=lambda: [
                            window.destroy(), on_closing()], font=("Arial", 16), width=10, height=2, bg="red")
    exit_button.grid(row=3, column=0, pady=20)


create_main_menu()

window.mainloop()
