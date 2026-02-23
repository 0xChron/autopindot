import time
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, Toplevel
import pyautogui
import keyboard

START_UP_DELAY = 5
START_STOP_KEY = "F5" 
running = False
worker_thread = None
current_key = "ctrl"
subtitle_label = None
toggle_button = None
key_button = None
timer_label = None
status_label = None
interval_entry = None

def press_keys(key, interval):
    global running
    print(f"Starting in {START_UP_DELAY} seconds...")
    for i in range(START_UP_DELAY, 0, -1):
        if not running:
            timer_label.config(text="")
            return
        timer_label.config(text=f"Starting in {i}s...")
        time.sleep(1)
    
    timer_label.config(text="")
    print("Started!")

    while running:
        pyautogui.press(key)
        print(f"Pressed {key}")
        time.sleep(interval)


def start():
    global running, worker_thread

    if running:
        return

    key = current_key
    interval = interval_entry.get().strip()

    if not key:
        messagebox.showerror("Error", "Please select a key.")
        return

    try:
        interval = float(interval)
        if interval <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Interval must be a positive number.")
        return

    running = True
    status_label.config(text="Status: Starting...")
    toggle_button.config(text="Stop (F5)", style="Danger.TButton")
    worker_thread = threading.Thread(
        target=press_keys, args=(key, interval), daemon=True
    )
    worker_thread.start()
    status_label.config(text="Status: Running")


def stop():
    global running
    running = False
    status_label.config(text="Status: Stopped")
    toggle_button.config(text="Start (F5)", style="Primary.TButton")
    timer_label.config(text="")


def toggle():
    if running:
        stop()
    else:
        start()


def validate_interval(value):
    """Allow only numbers and decimal point"""
    if value == "":
        return True
    try:
        float(value)
        return True
    except ValueError:
        return False


def update_subtitle():
    """Update the subtitle with current key and interval"""
    interval = interval_entry.get().strip() if interval_entry.get().strip() else "10"
    subtitle_label.config(text=f"Pindutin ang {current_key} tuwing {interval} seconds")


def open_key_recorder():
    """Open a window to record a key to press"""
    global current_key

    recorder = Toplevel(root)
    recorder.title("Set Key")
    try:
        recorder.iconbitmap("assets/favicon.ico")
    except Exception:
        pass

    recorder.resizable(False, False)
    recorder.transient(root)
    recorder.grab_set()

    # --- size + center over root ---
    w, h = 200, 200
    root.update_idletasks()
    x = root.winfo_rootx() + (root.winfo_width() - w) // 2
    y = root.winfo_rooty() + (root.winfo_height() - h) // 2
    recorder.geometry(f"{w}x{h}+{x}+{y}")

    # --- theme ---
    BG = "#0f172a"
    CARD = "#111827"
    TEXT = "#e5e7eb"
    MUTED = "#94a3b8"
    ACCENT = "#38bdf8"

    recorder.configure(bg=BG)

    # Card container (gives it a nice padded panel feel)
    card = tk.Frame(recorder, bg=CARD, bd=0, highlightthickness=1, highlightbackground="#1f2937")
    card.pack(fill="both", expand=True, padx=12, pady=12)

    # Layout in a simple vertical stack with good spacing
    title = tk.Label(card, text="Press a key", bg=CARD, fg=TEXT, font=("Segoe UI", 12, "bold"))
    title.pack(pady=(14, 4))

    hint = tk.Label(card, text="Esc or Cancel to close", bg=CARD, fg=MUTED, font=("Segoe UI", 8))
    hint.pack(pady=(0, 12))

    # Key display label
    key_display = tk.Label(card, text="", bg=CARD, fg=ACCENT, font=("Segoe UI", 14, "bold"))
    key_display.pack(pady=12)

    btn_row = tk.Frame(card, bg=CARD)
    btn_row.pack(side="bottom", fill="x", pady=(0, 12), padx=12)

    hook = None
    closed = False

    def close_recorder():
        nonlocal hook, closed
        if closed:
            return
        closed = True

        if hook is not None:
            try:
                keyboard.unhook(hook)
            except Exception:
                pass
            hook = None

        try:
            recorder.grab_release()
        except Exception:
            pass
        recorder.destroy()

    def on_key_press(event):
        nonlocal closed
        if closed:
            return

        key_name = getattr(event, "name", None)
        if not key_name:
            return

        def apply_key():
            nonlocal closed
            if closed or not recorder.winfo_exists():
                return

            # Update the display label
            try:
                key_display.config(text=f"Key: {key_name}")
            except Exception:
                pass

            global current_key
            current_key = key_name

            try:
                key_button.config(text=f"{current_key}")
            except Exception:
                pass

            try:
                update_subtitle()
            except Exception:
                pass

            recorder.after(450, close_recorder)

        # schedule UI updates on Tk main thread
        try:
            recorder.after(0, apply_key)
        except Exception:
            pass

    def cancel():
        close_recorder()

    cancel_btn = ttk.Button(
        btn_row, 
        text="Cancel", 
        command=cancel,
        style="Subtle.Small.TButton"
    )
    cancel_btn.pack(side="right")

    # Esc to cancel
    recorder.bind("<Escape>", lambda e: cancel())

    recorder.protocol("WM_DELETE_WINDOW", close_recorder)

    hook = keyboard.on_press(on_key_press, suppress=False)

    # Focus
    recorder.focus_force()

# gui
# --- Root window ---
root = tk.Tk()
root.title("Autopindot! v1.0")
try:
    root.iconbitmap("assets/favicon.ico")
except Exception:
    pass

root.geometry("360x320")
root.minsize(360, 320)
root.resizable(False, False)
root.configure(bg="#0f172a")  # deep slate

# --- Styling (ttk) ---
style = ttk.Style()
style.theme_use("clam")

style.configure("App.TFrame", background="#0f172a")
style.configure("Card.TFrame", background="#111827") 
style.configure("Title.TLabel", background="#0f172a", foreground="white", font=("Segoe UI", 16, "bold"))
style.configure("Sub.TLabel", background="#0f172a", foreground="#cbd5e1", font=("Segoe UI", 9))
style.configure("Label.TLabel", background="#111827", foreground="#e5e7eb", font=("Segoe UI", 10))
style.configure("Hint.TLabel", background="#111827", foreground="#94a3b8", font=("Segoe UI", 9))
style.configure("Status.TLabel", background="#111827", foreground="#cbd5e1", font=("Segoe UI", 9))

style.configure("Primary.TButton",
                font=("Segoe UI", 11, "bold"),
                padding=(12, 10),
                background="#22c55e",
                foreground="white")
style.map("Primary.TButton",
          background=[("active", "#16a34a")])

style.configure("Danger.TButton",
                font=("Segoe UI", 11, "bold"),
                padding=(12, 10),
                background="#ef4444",
                foreground="white")
style.map("Danger.TButton",
          background=[("active", "#dc2626")])

style.configure("Secondary.TButton",
                font=("Segoe UI", 10, "bold"),
                padding=(10, 8),
                background="#2563eb",
                foreground="white")
style.map("Secondary.TButton",
          background=[("active", "#1d4ed8")])

style.configure("TEntry",
                padding=(10, 8),
                fieldbackground="#0b1220",
                foreground="white")
style.configure(
    "Subtle.Small.TButton",
    font=("Segoe UI", 8),
    padding=(6, 2),
    background="#fa6260",
    foreground="white"
)
style.map(
    "Subtle.Small.TButton",
    background=[("active", "#ef4444")],
    foreground=[("active", "white")]
)

# --- Layout containers ---
app = ttk.Frame(root, style="App.TFrame", padding=16)
app.pack(fill="both", expand=True)

ttk.Label(app, text="Autopindot!", style="Title.TLabel").pack(anchor="w")
subtitle_label = ttk.Label(app, text=f"Pindutin ang {current_key} tuwing 10 seconds", style="Sub.TLabel")
subtitle_label.pack(anchor="w", pady=(0, 12))

card = ttk.Frame(app, style="Card.TFrame", padding=16)
card.pack(fill="both", expand=True)

# Make grid responsive
card.columnconfigure(0, weight=1)
card.columnconfigure(1, weight=1)

# --- Row 0: Key ---
ttk.Label(card, text="Key to press", style="Label.TLabel").grid(row=0, column=0, sticky="w")
key_button = ttk.Button(
    card,
    text=f"{current_key}",
    command=open_key_recorder,
    style="Secondary.TButton"
)
key_button.grid(row=1, column=0, sticky="ew", padx=(0, 8), pady=(6, 2))

ttk.Label(card, text="Click to record a key", style="Hint.TLabel").grid(row=2, column=0, sticky="w")

# --- Row 0: Interval ---
ttk.Label(card, text="Interval (seconds)", style="Label.TLabel").grid(row=0, column=1, sticky="w")
interval_entry = ttk.Entry(
    card,
    validate="key",
    validatecommand=(root.register(validate_interval), "%P")
)
interval_entry.insert(0, "10")
interval_entry.grid(row=1, column=1, sticky="ew", pady=(6, 2))
interval_entry.bind("<KeyRelease>", lambda e: update_subtitle())
ttk.Label(card, text="Example: 180 = 3 minutes", style="Hint.TLabel").grid(row=2, column=1, sticky="w")

# --- Toggle button full width ---
toggle_button = ttk.Button(
    card,
    text="Start (F5)",
    command=toggle,
    style="Primary.TButton"
)
toggle_button.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(16, 8))

# --- Timer + status ---
timer_label = ttk.Label(card, text="", style="Status.TLabel")
timer_label.grid(row=4, column=0, columnspan=2, sticky="w", pady=(2, 0))

status_label = ttk.Label(card, text="Status: Idle", style="Status.TLabel")
status_label.grid(row=5, column=0, columnspan=2, sticky="w", pady=(6, 0))

# --- Hotkey info ---
sep = ttk.Separator(card)
sep.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(14, 10))

ttk.Label(card, text=f"Press {START_STOP_KEY} to Start/Stop", style="Hint.TLabel").grid(
    row=7, column=0, columnspan=2, sticky="w"
)

keyboard.add_hotkey(START_STOP_KEY, toggle)

root.mainloop()