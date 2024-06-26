import tkinter as tk
from tkinter import ttk
import serial
import time

window = tk.Tk()
window.configure(bg="white")
initial_time = 100


arduino = serial.Serial('COM6',9600)
time.sleep(2)
window.attributes('-fullscreen', True)


def create_header(parent):
    header = tk.Frame(parent, height=50, bg='gray', bd=2, relief="solid")
    header.grid(row=0, column=0, sticky="ew")
    parent.grid_columnconfigure(0, weight=1)

    logo = tk.PhotoImage(
        file=r"assets\logo.png")
    logo = logo.subsample(10, 10)
    logo_label = tk.Label(header, image=logo, bg='gray')
    logo_label.image = logo
    logo_label.grid(row=0, column=0, padx=10, pady=30, sticky="nw")

    title_label = tk.Label(
        header, text="Operator Training Simulator", bg='gray', font=("Arial", 40))
    title_label.grid(row=0, column=0, padx=10, pady=10, sticky="n")
    parent.grid_columnconfigure(0, weight=1)
    title_label.place(relx=0.5, rely=0.5, anchor="center")

    return header


def on_closing():
    arduino.write(b'CLOSE\n')
    arduino.close()
    window.destroy()


def countdown_screen():
    for widget in window.winfo_children():
        widget.destroy()
    create_header(window)

    countdown_screen = tk.Frame(window, bg='white')
    countdown_screen.grid(row=0, column=0)
    countdown_screen.place(relx=0.5, rely=0.5, anchor="center")

    exit_button = tk.Button(countdown_screen, text="Cancel", command=lambda: [
                            countdown_screen.destroy(), create_main_menu()], font=("Arial", 16), width=10, height=2, bg="red")
    exit_button.pack(side="bottom", pady=20)

    countdown_label = tk.Label(countdown_screen, text="", font=(
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
        
    arduino.write(b'RUNNING\n')
    create_header(window)
    game_screen = tk.Frame(window, bg='white')
    game_screen.grid(row=0, column=0)
    game_screen.place(relx=0.5, rely=0.5, anchor="center")
    
    canvas = tk.Canvas(game_screen, width=540, height=250, background='white')
    canvas.pack()
    
    squares = []
    square_size = 100
    spacing = 10
    current_square = 0
    
    for i in range(2):
        for j in range(5):
            x0 = (square_size + spacing) * j
            y0 = (square_size + spacing) * i
            x1 = x0 + square_size
            y1 = y0 + square_size
            square = canvas.create_rectangle(x0, y0, x1, y1, fill='red')
            squares.append(square)

    start_time = time.time()

    countdown_label = tk.Label(game_screen, text="Time Left: 100", font=("Arial", 24), bg='white', fg='black')
    countdown_label.pack(pady=50)

    success_label = tk.Label(game_screen, text="Success!", font=(
        "Arial", 24), fg="green", bg='white')
    failure_label = tk.Label(game_screen, text="Failure!", font=(
        "Arial", 24), fg="red", bg='white')

    progress_bar = ttk.Progressbar(
        game_screen, orient="horizontal", length=800, mode="determinate", maximum=initial_time)
    progress_bar.pack(pady=10)
    
    def update_grid():
        nonlocal current_square
        canvas.itemconfig(squares[current_square], fill='green')
        current_square = current_square + 1
        
    remaining_time = initial_time - (time.time() - start_time)
    countdown_label.config(text="Time Left: " + str(int(remaining_time)))
    progress_bar['value'] = remaining_time
    
    button_frame = tk.Frame(game_screen, bg='white')
    button_frame.pack(pady=20)
    
    def test():
        nonlocal current_square
        remaining_time = initial_time - (time.time() - start_time)
        countdown_label.config(text="Time Left: " + str(int(remaining_time)))
        progress_bar['value'] = remaining_time
        if arduino.in_waiting > 0:
            message = arduino.readline().decode('utf-8').strip()
            if message == "GREEN":
                update_grid()

        if current_square == 10:
            success_label.pack()
            back_button = tk.Button(button_frame, text="Back to Menu", command=create_main_menu, font=("Arial", 16), width=15, height=2, bg='white')
            back_button.grid(row=0, column=1, padx=10)
        elif remaining_time <= 0 and current_square != 10:
            failure_label.pack()
            back_button = tk.Button(button_frame, text="Back to Menu", command=create_main_menu, font=("Arial", 16), width=15, height=2, bg='white')
            back_button.grid(row=0, column=1, padx=10)
        else:
            window.after(100, test)
                
    test()

        


def create_main_menu():
    for widget in window.winfo_children():
        widget.destroy()

    def update_initial_time(*args):
        global initial_time
        selected_difficulty = difficulty_var.get()
        if selected_difficulty == "Easy":
            initial_time = 100
        elif selected_difficulty == "Medium":
            initial_time = 20
        elif selected_difficulty == "Hard":
            initial_time = 10

    create_header(window)
    main_menu = tk.Frame(window)
    main_menu.configure(bg="white")
    main_menu.grid(row=1, column=0, pady=50)

    difficulty_label = tk.Label(main_menu, text="Select Difficulty:", font=("Arial", 38), bg='white')
    difficulty_label.grid(row=0, column=0, pady=20)

    difficulty_var = tk.StringVar()
    difficulty_var.set("Easy")
    difficulty_var.trace("w", update_initial_time)

    difficulty_options = ["Easy", "Medium", "Hard"]
    difficulty_menu = tk.OptionMenu(main_menu, difficulty_var, *difficulty_options)
    difficulty_menu.config(font=("Arial", 16), width=10, pady=20)
    difficulty_menu.grid(row=1, column=0, pady=20)

    start_button = tk.Button(main_menu, text="Start", command=countdown_screen, font=("Arial", 16), width=10, height=2, pady=15)
    start_button.grid(row=2, column=0, pady=20)
    exit_button = tk.Button(main_menu, text="Exit", command=lambda: [window.destroy(), on_closing()], font=("Arial", 16), width=10, height=2, bg="red")
    exit_button.grid(row=3, column=0, pady=200, sticky="s")


def run():
    create_main_menu()
    window.protocol("WM_DELETE_WINDOW", on_closing)
    window.mainloop()


if __name__ == "__main__":
    run()
