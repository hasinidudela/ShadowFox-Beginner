import tkinter as tk
from spellchecker import SpellChecker

spell = SpellChecker()

# ---------- FUNCTIONS ----------

def get_current_word(text):
    words = text.split()
    return words[-1] if words else ""

def update_suggestions(event=None):
    text = input_box.get("1.0", tk.END).strip()
    current_word = get_current_word(text)

    for btn in suggestion_buttons:
        btn.config(text="", state=tk.DISABLED)

    if current_word and current_word.lower() not in spell:
        suggestions = list(spell.candidates(current_word))[:3]

        for i, suggestion in enumerate(suggestions):
            suggestion_buttons[i].config(
                text=suggestion,
                state=tk.NORMAL
            )

def apply_suggestion(word):
    text = input_box.get("1.0", tk.END).strip().split()
    text[-1] = word
    input_box.delete("1.0", tk.END)
    input_box.insert(tk.END, " ".join(text) + " ")

    for btn in suggestion_buttons:
        btn.config(text="", state=tk.DISABLED)

def autocorrect_space(event):
    text = input_box.get("1.0", tk.END).strip()
    words = text.split()

    if words:
        last_word = words[-1]
        if last_word.lower() not in spell:
            words[-1] = spell.correction(last_word)

        input_box.delete("1.0", tk.END)
        input_box.insert(tk.END, " ".join(words) + " ")

    return "break"

# ---------- GUI ----------

root = tk.Tk()
root.title("Android-Style Autocorrect Keyboard")
root.geometry("600x350")
root.config(bg="#f2f2f2")

# Input Field
input_box = tk.Text(root, height=5, font=("Arial", 14))
input_box.pack(padx=10, pady=10, fill=tk.X)

input_box.bind("<KeyRelease>", update_suggestions)
input_box.bind("<space>", autocorrect_space)

# Suggestion Bar
suggestion_frame = tk.Frame(root, bg="#d9d9d9")
suggestion_frame.pack(fill=tk.X, padx=10, pady=5)

suggestion_buttons = []
for _ in range(3):
    btn = tk.Button(
        suggestion_frame,
        text="",
        font=("Arial", 12),
        width=15,
        state=tk.DISABLED
    )
    btn.pack(side=tk.LEFT, padx=5, pady=5)
    suggestion_buttons.append(btn)

# Bind buttons
for btn in suggestion_buttons:
    btn.config(command=lambda b=btn: apply_suggestion(b.cget("text")))

root.mainloop()

