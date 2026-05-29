import random
import tkinter as tk
from tkinter import font, messagebox


class SlotMachine(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("slots test")
        self.configure(bg="#FFF6FB")
        self.geometry("520x360")

        self.reel_symbols = ["🍒", "🍋", "🍇", "🍉", "⭐", "💎", "🍀"]
        self.cash = 1000

        self._build_ui()

    def _build_ui(self):
        header_font = font.Font(family="Helvetica", size=20, weight="bold")
        big_font = font.Font(family="Segoe UI Emoji", size=48)
        small_font = font.Font(family="Helvetica", size=12)

        header = tk.Label(self, text="slots test", bg="#FFF6FB", fg="#D6336C", font=header_font)
        header.pack(pady=(12, 4))

        info_frame = tk.Frame(self, bg="#FFF6FB")
        info_frame.pack()

        self.cash_var = tk.StringVar(value=f"cash: ${self.cash}")
        cash_label = tk.Label(info_frame, textvariable=self.cash_var, bg="#FFF6FB", fg="#2A2A2A", font=small_font)
        cash_label.grid(row=0, column=0, padx=8)

        bet_label = tk.Label(info_frame, text="bet:", bg="#FFF6FB", fg="#2A2A2A", font=small_font)
        bet_label.grid(row=0, column=1)
        self.bet_var = tk.IntVar(value=10)
        bet_spin = tk.Spinbox(info_frame, from_=1, to=500, textvariable=self.bet_var, width=6)
        bet_spin.grid(row=0, column=2, padx=6)

        self.message_var = tk.StringVar(value="good luck twin")
        message_label = tk.Label(info_frame, textvariable=self.message_var, bg="#FFF6FB", fg="#6B6B6B", font=small_font)
        message_label.grid(row=0, column=3, padx=12)

        reels_frame = tk.Frame(self, bg="#FFF6FB")
        reels_frame.pack(pady=12)

        self.reel_labels = []
        for i in range(3):
            lbl = tk.Label(reels_frame, text=random.choice(self.reel_symbols), font=big_font, bg="#FFF6FB")
            lbl.grid(row=0, column=i, padx=12)
            self.reel_labels.append(lbl)

        controls = tk.Frame(self, bg="#FFF6FB")
        controls.pack(pady=8)

        spin_btn = tk.Button(controls, text="spin", command=self.spin, bg="#FFB6D5", fg="#4A0040", width=10)
        spin_btn.grid(row=0, column=0, padx=8)
        max_btn = tk.Button(controls, text="bet max", command=self.bet_max, bg="#FFD6E8", fg="#4A0040", width=8)
        max_btn.grid(row=0, column=1, padx=6)
        reset_btn = tk.Button(controls, text="reset", command=self.reset_game, bg="#FFF1F7", fg="#4A0040", width=8)
        reset_btn.grid(row=0, column=2, padx=6)

        footer = tk.Label(self, text="match 3: x5  •  match 2: x2", bg="#FFF6FB", fg="#9A4A7B", font=small_font)
        footer.pack(side="bottom", pady=10)

    def bet_max(self):
        self.bet_var.set(self.cash)

    def reset_game(self):
        if messagebox.askyesno("reset", "reset cash to 1k?"):
            self.cash = 1000
            self.cash_var.set(f"cash: ${self.cash}")
            self.message_var.set("good luck twin")

    def spin(self):
        bet = int(self.bet_var.get())
        if bet <= 0:
            self.message_var.set("bet gotta be atleast 1")
            return
        if bet > self.cash:
            self.message_var.set("not enough cash for that bet")
            return

        self.message_var.set("spinning")
        # simple animation
        steps = 18
        delay = 60
        self._animate(0, steps, delay, bet)

    def _animate(self, step, steps, delay, bet):
        for lbl in self.reel_labels:
            lbl.config(text=random.choice(self.reel_symbols))

        if step < steps:
            self.after(delay + step * 6, lambda: self._animate(step + 1, steps, delay, bet))
            return

        # final result
        result = [random.choice(self.reel_symbols) for _ in range(3)]
        for i, lbl in enumerate(self.reel_labels):
            lbl.config(text=result[i])

        # evaluate
        payout = 0
        if result[0] == result[1] == result[2]:
            payout = bet * 5
            self.message_var.set(f"I JUST HIT THE JACKPOTT YOU WON {payout}")
        elif result[0] == result[1] or result[1] == result[2] or result[0] == result[2]:
            payout = bet * 2
            self.message_var.set(f"you won {payout}")
        else:
            payout = -bet
            self.message_var.set(f"you lost {bet}")

        self.cash += payout
        if self.cash < 0:
            self.cash = 0

        self.cash_var.set(f"cash: ${self.cash}")

        if self.cash == 0:
            self.message_var.set("no money twin, click reset to try again")


def main():
    app = SlotMachine()
    app.mainloop()


if __name__ == "__main__":
    main()
