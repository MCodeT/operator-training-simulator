import tkinter as tk
import serial
import time

arduino = serial.Serial('COM5', 9600)

window = tk.Tk()
arduino.write(b'1')

# Set the window size to 90% of the screen size
window_width = int(window.winfo_screenwidth() * 0.9)
window_height = int(window.winfo_screenheight() * 0.9)
window.geometry(f"{window_width}x{window_height}")

def on_closing():
    arduino.write(b'0')
    arduino.close()
    window.destroy()



# Create the countdown label
    
def countdown_screen():
    # Remove the main menu screen
    for widget in window.winfo_children():
        widget.destroy()
        
    # Create the countdown screen
    countdown_screen = tk.Frame(window)
    countdown_screen.pack()
    
    # Exit button
    exit_button = tk.Button(countdown_screen, text="Cancel", command=lambda: [countdown_screen.destroy(), create_main_menu()], font=("Arial", 16), width=10, height=2, bg="red")
    exit_button.pack(side="bottom", pady=20)

    countdown_label = tk.Label(countdown_screen, text="", font=("Arial", 48))
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
    # Create the game screen
    game_screen = tk.Frame(window)
    game_screen.pack()

    counter = 0
    start_time = time.time()
    
    countdown_label = tk.Label(game_screen, text="Time Left: 5", font=("Arial", 16))
    countdown_label.pack(pady=10)
    
    def increment_counter():
        nonlocal counter
        counter += 1

    button = tk.Button(game_screen, text="Click Me!", command=increment_counter, font=("Arial", 16), width=10, height=2)
    button.pack(pady=20)

    success_label = tk.Label(game_screen, text="Success!", font=("Arial", 24), fg="green")
    failure_label = tk.Label(game_screen, text="Failure!", font=("Arial", 24), fg="red")


    def test():
        remaining_time = 6 - (time.time() - start_time)
        countdown_label.config(text="Time Left: " + str(int(remaining_time)))
        if remaining_time <= 0:
            if counter >= 10:
                success_label.pack()
            else:
                failure_label.pack()
            # Add a button to go back to the main menu
            back_button = tk.Button(game_screen, text="Back to Menu", command=create_main_menu, font=("Arial", 16), width=15, height=2)
            back_button.pack(pady=20)
        else:
            window.after(100, test)
    
    test()
    
def create_main_menu():
    
    for widget in window.winfo_children():
        widget.destroy()
    # Create the game screen
    # Create the main menu screen
    main_menu = tk.Frame(window)
    main_menu.pack()
    # Difficulty settings
    difficulty_label = tk.Label(main_menu, text="Select Difficulty:", font=("Arial", 16))
    difficulty_label.pack(pady=10)

    difficulty_var = tk.StringVar()
    difficulty_var.set("Easy")  # Default difficulty setting

    difficulty_options = ["Easy", "Medium", "Hard"]
    difficulty_menu = tk.OptionMenu(main_menu, difficulty_var, *difficulty_options)
    difficulty_menu.config(font=("Arial", 14))
    difficulty_menu.pack(pady=10)

    # Start button
    start_button = tk.Button(main_menu, text="Start", command=countdown_screen, font=("Arial", 16), width=10, height=2)
    start_button.pack(pady=20)
    # Exit button
    exit_button = tk.Button(main_menu, text="Exit", command=lambda: [window.destroy(), on_closing()], font=("Arial", 16), width=10, height=2, bg="red")
    exit_button.pack(side="bottom", pady=20)

create_main_menu()

window.mainloop()
