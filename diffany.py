#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk
import difflib

class TextLineNumbers(tk.Canvas):
    def __init__(self, *args, fg='#FFFFFF', **kwargs):
        super().__init__(*args, **kwargs)
        self.fg = fg  # Store the foreground color
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget
        # Bind events to update line numbers
        text_widget.bind('<KeyRelease>', self.redraw)
        text_widget.bind('<MouseWheel>', self.redraw)  # For Windows
        text_widget.bind('<Button-4>', self.redraw)    # For Linux scroll up
        text_widget.bind('<Button-5>', self.redraw)    # For Linux scroll down
        text_widget.bind('<Configure>', self.redraw)   # Window resized

    def redraw(self, *args):
        self.delete("all")
        if not self.textwidget:
            return
        i = self.textwidget.index("@0,0")
        while True:
            dline = self.textwidget.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            linenum = self.textwidget.index(i).split(".")[0]
            self.create_text(2, y, anchor="nw", text=linenum, fill=self.fg)
            i = self.textwidget.index(f"{i}+1line")

class DiffAnywhereApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DiffAnywhere 1.0")  # Updated window title

        # Bring the window to the front and ensure it is visible
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after(100, lambda: self.root.attributes('-topmost', False))

        # Set a minimum window size
        self.root.minsize(800, 600)

        # Define colors
        BACKGROUND_COLOR = '#1F2223'
        TITLE_BAR_COLOR = '#1A5492'
        FONT_COLOR = '#FFFFFF'
        SEPARATOR_COLOR = '#2A2D2E'  # Slightly lighter gray for borders

        self.root.configure(bg=BACKGROUND_COLOR)

        # Apply a style to make the UI prettier
        style = ttk.Style()
        style.theme_use('clam')

        style.configure('TFrame', background=BACKGROUND_COLOR)
        style.configure('Custom.TLabel', background=TITLE_BAR_COLOR, foreground=FONT_COLOR, font=('TkDefaultFont', 10, 'bold'))
        style.configure('Vertical.TScrollbar', background=BACKGROUND_COLOR)
        style.configure('TSeparator', background=SEPARATOR_COLOR)

        main_frame = ttk.Frame(self.root, style='TFrame')
        main_frame.pack(fill=tk.BOTH, expand=1)

        # Top frame for input text widgets
        top_frame = ttk.Frame(main_frame, style='TFrame')
        top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # First text widget
        frame1 = ttk.Frame(top_frame, style='TFrame', relief='flat', borderwidth=1)
        frame1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0,1))
        label1 = ttk.Label(frame1, text="Paste Code 1:", style='Custom.TLabel')
        label1.pack(side=tk.TOP, anchor="w", fill=tk.X)
        text1_frame = ttk.Frame(frame1, style='TFrame')
        text1_frame.pack(fill=tk.BOTH, expand=True)
        self.text1_linenumbers = TextLineNumbers(text1_frame, width=30, bg=BACKGROUND_COLOR, fg=FONT_COLOR, bd=0, highlightthickness=0)
        self.text1_linenumbers.pack(side="left", fill="y")
        self.text1 = tk.Text(text1_frame, wrap=tk.NONE, bg=BACKGROUND_COLOR, fg=FONT_COLOR, insertbackground=FONT_COLOR, bd=0, highlightthickness=0)
        self.text1.pack(side="left", fill="both", expand=True)
        scrollbar1 = ttk.Scrollbar(text1_frame, orient=tk.VERTICAL, command=self.text1.yview)
        scrollbar1.pack(side="right", fill="y")
        self.text1.configure(yscrollcommand=scrollbar1.set)
        self.text1_linenumbers.attach(self.text1)
        self.text1.bind('<<Modified>>', self.on_text_modified)
        self.text1.bind('<Configure>', lambda e: self.text1_linenumbers.redraw())

        # Second text widget
        frame2 = ttk.Frame(top_frame, style='TFrame', relief='flat', borderwidth=1)
        frame2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(1,0))
        label2 = ttk.Label(frame2, text="Paste Code 2:", style='Custom.TLabel')
        label2.pack(side=tk.TOP, anchor="w", fill=tk.X)
        text2_frame = ttk.Frame(frame2, style='TFrame')
        text2_frame.pack(fill=tk.BOTH, expand=True)
        self.text2_linenumbers = TextLineNumbers(text2_frame, width=30, bg=BACKGROUND_COLOR, fg=FONT_COLOR, bd=0, highlightthickness=0)
        self.text2_linenumbers.pack(side="left", fill="y")
        self.text2 = tk.Text(text2_frame, wrap=tk.NONE, bg=BACKGROUND_COLOR, fg=FONT_COLOR, insertbackground=FONT_COLOR, bd=0, highlightthickness=0)
        self.text2.pack(side="left", fill="both", expand=True)
        scrollbar2 = ttk.Scrollbar(text2_frame, orient=tk.VERTICAL, command=self.text2.yview)
        scrollbar2.pack(side="right", fill="y")
        self.text2.configure(yscrollcommand=scrollbar2.set)
        self.text2_linenumbers.attach(self.text2)
        self.text2.bind('<<Modified>>', self.on_text_modified)
        self.text2.bind('<Configure>', lambda e: self.text2_linenumbers.redraw())

        # Separator between top frames
        separator = ttk.Separator(main_frame, orient='horizontal')
        separator.pack(side=tk.TOP, fill=tk.X)

        # Diff text widget at the bottom
        frame_diff = ttk.Frame(main_frame, style='TFrame', relief='flat', borderwidth=1)
        frame_diff.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, pady=(1,0))
        label_diff = ttk.Label(frame_diff, text="Differences:", style='Custom.TLabel')
        label_diff.pack(side=tk.TOP, anchor="w", fill=tk.X)
        diff_frame = ttk.Frame(frame_diff, style='TFrame')
        diff_frame.pack(fill=tk.BOTH, expand=True)
        self.diff_linenumbers = TextLineNumbers(diff_frame, width=30, bg=BACKGROUND_COLOR, fg=FONT_COLOR, bd=0, highlightthickness=0)
        self.diff_linenumbers.pack(side="left", fill="y")
        self.diff_text = tk.Text(diff_frame, wrap=tk.NONE, bg=BACKGROUND_COLOR, fg=FONT_COLOR, insertbackground=FONT_COLOR, bd=0, highlightthickness=0)
        self.diff_text.pack(side="left", fill="both", expand=True)
        scrollbar_diff = ttk.Scrollbar(diff_frame, orient=tk.VERTICAL, command=self.diff_text.yview)
        scrollbar_diff.pack(side="right", fill="y")
        self.diff_text.configure(yscrollcommand=scrollbar_diff.set)
        self.diff_linenumbers.attach(self.diff_text)
        self.diff_text.bind('<Configure>', lambda e: self.diff_linenumbers.redraw())

        # Adjusted tag configurations with updated colors
        self.diff_text.tag_configure("insert", foreground="#98FB98")  # PaleGreen
        self.diff_text.tag_configure("delete", foreground="#FF6B6B")  # Bright red
        self.diff_text.tag_configure("replace", foreground="#FFD700")  # Gold
        self.diff_text.tag_configure("highlight", background="#FFD700", foreground="#000000")  # Black font
        self.diff_text.tag_configure("line_number", foreground=FONT_COLOR, font=('TkDefaultFont', 10, 'bold'))
        self.diff_text.tag_configure("equal", foreground=FONT_COLOR)

    def on_text_modified(self, event):
        event.widget.edit_modified(0)  # Reset the modified flag
        text1_content = self.text1.get("1.0", tk.END).splitlines()
        text2_content = self.text2.get("1.0", tk.END).splitlines()

        self.diff_text.delete("1.0", tk.END)

        max_lines = max(len(text1_content), len(text2_content))
        for i in range(max_lines):
            line1 = text1_content[i] if i < len(text1_content) else ''
            line2 = text2_content[i] if i < len(text2_content) else ''
            line_num = i + 1

            if line1 == line2:
                continue  # Skip equal lines
            else:
                # Insert line number
                self.diff_text.insert(tk.END, f"Line {line_num}:\n", 'line_number')

                # Insert text from text1 with highlights
                self.diff_text.insert(tk.END, "- ", 'delete')
                self.insert_with_highlight(line1, line2, 'delete')
                self.diff_text.insert(tk.END, "\n")

                # Insert text from text2 with highlights
                self.diff_text.insert(tk.END, "+ ", 'insert')
                self.insert_with_highlight(line2, line1, 'insert')
                self.diff_text.insert(tk.END, "\n")

        # Update line numbers
        self.diff_linenumbers.redraw()
        self.text1_linenumbers.redraw()
        self.text2_linenumbers.redraw()

    def insert_with_highlight(self, line_main, line_compare, tag):
        # Use SequenceMatcher to find matching blocks
        sm = difflib.SequenceMatcher(None, line_main, line_compare)
        for opcode, a0, a1, b0, b1 in sm.get_opcodes():
            text = line_main[a0:a1]
            if opcode == 'equal':
                self.diff_text.insert(tk.END, text, tag)
            else:
                self.diff_text.insert(tk.END, text, 'highlight')

def main():
    root = tk.Tk()
    app = DiffAnywhereApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
