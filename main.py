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
    
    recorder_window = Toplevel(root)
    recorder_window.title("Set Key to Press")
    recorder_window.iconbitmap("assets/favicon.ico")
    recorder_window.geometry("300x300")
    recorder_window.resizable(False, False)
    recorder_window.transient(root)
    recorder_window.grab_set()  # Make it modal
    
    instruction_label = tk.Label(
        recorder_window, 
        text="Press any key to set...",
        font=("Arial", 10)
    )
    instruction_label.pack(pady=20)
    
    key_display = tk.Label(
        recorder_window,
        text="",
        font=("Arial", 12, "bold"),
        fg="blue"
    )
    key_display.pack(pady=10)
    
    hook = None
    
    def on_key_press(event):
        global current_key
        
        # Check if window still exists
        if not recorder_window.winfo_exists():
            return
        
        # Get the key name
        key_name = event.name
        
        # Update display
        try:
            key_display.config(text=f"Key: {key_name}")
        except:
            return
        
        # Set new key
        current_key = key_name
        key_button.config(text=f"{current_key}")
        update_subtitle()
        
        # Close window after a short delay
        recorder_window.after(500, lambda: close_recorder(hook))
    
    def close_recorder(hook_to_remove):
        if hook_to_remove:
            try:
                keyboard.unhook(hook_to_remove)
            except:
                pass
        try:
            recorder_window.destroy()
        except:
            pass
    
    # Hook the key press event
    hook = keyboard.on_press(on_key_press, suppress=False)
    
    recorder_window.protocol("WM_DELETE_WINDOW", lambda: close_recorder(hook))


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
style.configure("Card.TFrame", background="#111827")  # card bg
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

# Register F5 hotkey
keyboard.add_hotkey(START_STOP_KEY, toggle)

root.mainloop()