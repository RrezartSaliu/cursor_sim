import tkinter as tk
from datetime import datetime


class CursorMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("Normalized Cursor Monitor")
        self.root.geometry("1000x700")
        self.root.configure(bg="black")

        self.target_x = 0.0
        self.target_y = 0.0

        self.x_norm = 0.0
        self.y_norm = 0.0
        self.error_x = 0.0
        self.error_y = 0.0

        self.info = tk.Label(
            root,
            text="Move your cursor inside the black area",
            fg="white",
            bg="black",
            font=("Consolas", 13),
            justify="left",
            anchor="nw"
        )
        self.info.pack(fill="x", padx=20, pady=15)

        self.canvas = tk.Canvas(
            root,
            bg="black",
            highlightthickness=1,
            highlightbackground="#444444",
            cursor="crosshair"
        )
        self.canvas.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.canvas.bind("<Configure>", self.draw_target)

        self.draw_target()
        self.update_timestamp()

    def draw_target(self, event=None):
        self.canvas.delete("target")

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        if width <= 1 or height <= 1:
            return

        cx = width / 2
        cy = height / 2

        self.canvas.create_line(
            cx - 15, cy, cx + 15, cy,
            fill="#00ff00", width=2, tags="target"
        )
        self.canvas.create_line(
            cx, cy - 15, cx, cy + 15,
            fill="#00ff00", width=2, tags="target"
        )
        self.canvas.create_oval(
            cx - 5, cy - 5, cx + 5, cy + 5,
            outline="#00ff00", width=2, tags="target"
        )

    def on_mouse_move(self, event):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        if width <= 1 or height <= 1:
            return

        # Normalize coordinates to [-1, +1].
        # X: left=-1, center=0, right=+1.
        # Y: top=+1, center=0, bottom=-1.
        self.x_norm = 2.0 * event.x / width - 1.0
        self.y_norm = 1.0 - 2.0 * event.y / height

        # Error relative to the target.
        self.error_x = self.x_norm - self.target_x
        self.error_y = self.y_norm - self.target_y

        self.update_info()

    def update_info(self):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        timestamp = datetime.now().astimezone().isoformat(
            timespec="milliseconds"
        )

        self.info.config(
            text=(
                "NORMALIZED CURSOR MONITOR\n"
                f"Pixel position:  X={self.x_norm * width / 2 + width / 2:.0f}  "
                f"Y={height / 2 - self.y_norm * height / 2:.0f}\n"
                f"Normalized X:   {self.x_norm:+.4f}\n"
                f"Normalized Y:   {self.y_norm:+.4f}\n"
                f"X Error:        {self.error_x:+.4f}\n"
                f"Y Error:        {self.error_y:+.4f}\n"
                f"Target:         X={self.target_x:+.2f}  "
                f"Y={self.target_y:+.2f}\n"
                f"Canvas:         {width} x {height} pixels\n"
                f"Timestamp:      {timestamp}"
            )
        )

    def update_timestamp(self):
        self.update_info()
        self.root.after(50, self.update_timestamp)


if __name__ == "__main__":
    root = tk.Tk()
    app = CursorMonitor(root)
    root.mainloop()
