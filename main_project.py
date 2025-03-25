import sqlite3
import tkinter as tk
from tkinter import messagebox

# Database setup
conn = sqlite3.connect('players.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        score INTEGER DEFAULT 0,
        wins INTEGER DEFAULT 0,
        losses INTEGER DEFAULT 0,
        draws INTEGER DEFAULT 0
    )
''')
conn.commit()

def update_score(player_name, score, result):
    c.execute("SELECT score, wins, losses, draws FROM scores WHERE name=?", (player_name,))
    result_data = c.fetchone()
    
    if result_data:
        new_score = result_data[0] + score
        wins = result_data[1]
        losses = result_data[2]
        draws = result_data[3]

        if result == 'win':
            wins += 1
        elif result == 'loss':
            losses += 1
        elif result == 'draw':
            draws += 1

        c.execute("UPDATE scores SET score=?, wins=?, losses=?, draws=? WHERE name=?",
                  (new_score, wins, losses, draws, player_name))
    else:
        wins = 1 if result == 'win' else 0
        losses = 1 if result == 'loss' else 0
        draws = 1 if result == 'draw' else 0
        c.execute("INSERT INTO scores (name, score, wins, losses, draws) VALUES (?, ?, ?, ?, ?)",
                  (player_name, score, wins, losses, draws))

    conn.commit()

def show_leaderboard():
    leaderboard_window = tk.Toplevel()
    leaderboard_window.title("Leaderboard")
    leaderboard_window.geometry("600x400")
    leaderboard_window.config(bg="#2E4053")

    c.execute("SELECT name, score, wins, losses, draws FROM scores ORDER BY score DESC")
    scores = c.fetchall()

    tk.Label(leaderboard_window, text="🏆 Leaderboard 🏆", font=("Arial", 24, "bold"), fg="#F4D03F", bg="#2E4053").pack(pady=20)
    frame = tk.Frame(leaderboard_window, bg="#2E4053")
    frame.pack()

    header_labels = ["Rank", "Name", "Score", "Wins", "Losses", "Draws"]
    for col, text in enumerate(header_labels):
        tk.Label(frame, text=text, font=("Arial", 12, "bold"), fg="#FDFEFE", bg="#34495E", padx=10, pady=5, width=10).grid(row=0, column=col)

    for idx, (name, score, wins, losses, draws) in enumerate(scores, start=1):
        data = [idx, name, score, wins, losses, draws]
        for col, value in enumerate(data):
            tk.Label(frame, text=str(value), font=("Arial", 12), fg="#FDFEFE", bg="#2E4053", padx=10, pady=5, width=10).grid(row=idx, column=col)

def register_players():
    player1_name = entry_player1.get().strip()
    player2_name = entry_player2.get().strip()

    if not player1_name or not player2_name:
        messagebox.showerror("Error", "Please enter player usernames.")
    else:
        c.execute("INSERT INTO players (name) VALUES (?)", (player1_name,))
        c.execute("INSERT INTO players (name) VALUES (?)", (player2_name,))
        conn.commit()
        messagebox.showinfo("Successful", "Players registered successfully. Go to login.")
        entry_player1.delete(0, tk.END)
        entry_player2.delete(0, tk.END)
        open_login_window()

def open_login_window():
    for widget in frame.winfo_children():
        widget.destroy()

    root.title("Login to Game")

    tk.Label(frame, text="Player 1 Username:", font=("Arial", 12), fg="#1C2833", bg="#D5DBDB").grid(row=0, column=0, pady=10, padx=10)
    entry_player1 = tk.Entry(frame, font=("Arial", 12))
    entry_player1.grid(row=0, column=1, pady=10, padx=10)

    tk.Label(frame, text="Player 2 Username:", font=("Arial", 12), fg="#1C2833", bg="#D5DBDB").grid(row=1, column=0, pady=10, padx=10)
    entry_player2 = tk.Entry(frame, font=("Arial", 12))
    entry_player2.grid(row=1, column=1, pady=10, padx=10)

    tk.Button(frame, text="Login", command=lambda: login_players(entry_player1.get().strip(), entry_player2.get().strip()), font=("Arial", 12), bg="#2ECC71", fg="white", padx=20).grid(row=2, column=0, columnspan=2, pady=20)

def login_players(player1_name, player2_name):
    # Check if player names exist in the database
    c.execute("SELECT name FROM players WHERE name=?", (player1_name,))
    player1_exists = c.fetchone()

    c.execute("SELECT name FROM players WHERE name=?", (player2_name,))
    player2_exists = c.fetchone()

    if not player1_exists or not player2_exists:
        messagebox.showerror("Error", "One or both usernames do not exist in the database. Please try again.")
        entry_player1.delete(0, tk.END)
        entry_player2.delete(0, tk.END)
    else:
        messagebox.showinfo("Login", "Login successful!")

# Main Window
root = tk.Tk()
root.title("Game Menu")
root.geometry("450x350")
root.config(bg="#D5DBDB")
root.eval('tk::PlaceWindow . center')

frame = tk.Frame(root, bg="#D5DBDB")
frame.pack(padx=20, pady=20)

tk.Label(frame, text="Player 1 Username:", font=("Arial", 12), fg="#1C2833", bg="#D5DBDB").grid(row=0, column=0, pady=10, padx=10)
entry_player1 = tk.Entry(frame, font=("Arial", 12))
entry_player1.grid(row=0, column=1, pady=10, padx=10)

tk.Label(frame, text="Player 2 Username:", font=("Arial", 12), fg="#1C2833", bg="#D5DBDB").grid(row=1, column=0, pady=10, padx=10)
entry_player2 = tk.Entry(frame, font=("Arial", 12))
entry_player2.grid(row=1, column=1, pady=10, padx=10)

tk.Button(frame, text="Sign In", command=register_players, font=("Arial", 12), bg="#3498DB", fg="white", padx=20).grid(row=2, column=0, columnspan=2, pady=10)
tk.Button(frame, text="Show Leaderboard", command=show_leaderboard, font=("Arial", 12), bg="#F39C12", fg="white", padx=20).grid(row=3, column=0, columnspan=2, pady=10)

root.mainloop()
conn.close()
