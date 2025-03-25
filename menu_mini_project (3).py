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

    def register_players():
        player1_name = entry_player1.get()
        player2_name = entry_player2.get()

        if player1_name == "" or player2_name == "":
            messagebox.showerror("خطا", "لطفا نام هر دو بازیکن را وارد کنید.")
        else:
            c.execute("INSERT INTO players (name) VALUES (?)", (player1_name,))
            c.execute("INSERT INTO players (name) VALUES (?)", (player2_name,))
            conn.commit()

            messagebox.showinfo("موفقیت", "بازیکنان با موفقیت ثبت شدند!")

            entry_player1.delete(0, tk.END)
            entry_player2.delete(0, tk.END)

    root = tk.Tk()
    root.title("ثبت نام بازی")

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    label_player1 = tk.Label(frame, text="نام بازیکن اول:")
    label_player1.grid(row=0, column=0, pady=5)

    entry_player1 = tk.Entry(frame)
    entry_player1.grid(row=0, column=1, pady=5)

    label_player2 = tk.Label(frame, text="نام بازیکن دوم:")
    label_player2.grid(row=1, column=0, pady=5)

    entry_player2 = tk.Entry(frame)
    entry_player2.grid(row=1, column=1, pady=5)

    register_button = tk.Button(frame, text="ثبت نام", command=register_players)
    register_button.grid(row=2, column=0, columnspan=2, pady=10)

    root.mainloop()

except Exception as e:
    print(f"خطا: {e}", file=sys.stderr)
finally:
    conn.close()
