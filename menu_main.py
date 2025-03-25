import sqlite3
import tkinter as tk
from tkinter import messagebox
import sys

try:
    conn = sqlite3.connect('players.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    conn.commit()

    def open_login_window():
        for widget in frame.winfo_children():
            widget.destroy()

        root.title("Login to Game")

        label_player1 = tk.Label(frame, text="Player 1 username:")
        label_player1.grid(row=0, column=0, pady=10, padx=10)

        entry_player1 = tk.Entry(frame)
        entry_player1.grid(row=0, column=1, pady=10, padx=10)

        label_player2 = tk.Label(frame, text="Player 2 username:")
        label_player2.grid(row=1, column=0, pady=10, padx=10)

        entry_player2 = tk.Entry(frame)
        entry_player2.grid(row=1, column=1, pady=10, padx=10)

        def login():
            player1_name = entry_player1.get().strip()
            player2_name = entry_player2.get().strip()

            if not player1_name or not player2_name:
                messagebox.showerror("Error", "Please enter player usernames.")
                return

            c.execute("SELECT COUNT(*) FROM players WHERE name=?", (player1_name,))
            player1_exists = c.fetchone()[0] > 0

            c.execute("SELECT COUNT(*) FROM players WHERE name=?", (player2_name,))
            player2_exists = c.fetchone()[0] > 0

            if player1_exists and player2_exists:
                messagebox.showinfo("Success", "Login successful! Starting the game...")
                root.destroy()
            else:
                messagebox.showerror("Error", "Invalid player names. Please try again.")

        login_button = tk.Button(frame, text="Login", command=login)
        login_button.grid(row=2, column=0, columnspan=2, pady=20)

    def register_players():
        player1_name = entry_player1.get().strip()
        player2_name = entry_player2.get().strip()

        if not player1_name or not player2_name:
            messagebox.showerror("Error", "Please enter player usernames.")
        else:
            c.execute("INSERT INTO players (name) VALUES (?)", (player1_name,))
            c.execute("INSERT INTO players (name) VALUES (?)", (player2_name,))
            conn.commit()

            messagebox.showinfo("Successful", "Players sign in was successful. Go to login.")
            entry_player1.delete(0, tk.END)
            entry_player2.delete(0, tk.END)
            open_login_window()

    root = tk.Tk()
    root.title("Sign in Game")
    root.geometry("400x250")

    root.eval('tk::PlaceWindow . center')

    frame = tk.Frame(root)
    frame.pack(padx=20, pady=20)

    label_player1 = tk.Label(frame, text="Player 1 username:")
    label_player1.grid(row=0, column=0, pady=10, padx=10)

    entry_player1 = tk.Entry(frame)
    entry_player1.grid(row=0, column=1, pady=10, padx=10)

    label_player2 = tk.Label(frame, text="Player 2 username:")
    label_player2.grid(row=1, column=0, pady=10, padx=10)

    entry_player2 = tk.Entry(frame)
    entry_player2.grid(row=1, column=1, pady=10, padx=10)

    register_button = tk.Button(frame, text="Sign in", command=register_players)
    register_button.grid(row=2, column=0, columnspan=2, pady=20)

    root.mainloop()

except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
finally:
    conn.close()