#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
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
        self.root.title("DiffAnywhere 1.0")

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

        # Initialize options
        self.ignore_case = tk.BooleanVar(value=False)
        self.ignore_whitespace = tk.BooleanVar(value=False)
        self.ignore_blank_lines = tk.BooleanVar(value=False)
        self.suppress_common_lines = tk.BooleanVar(value=False)
        self.context_lines = tk.IntVar(value=3)
        self.side_by_side = tk.BooleanVar(value=False)

        # Create the menu bar
        self.create_menu()

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

    def create_menu(self):
        # Use standard Menu without custom colors
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open File 1", command=self.open_file1)
        file_menu.add_command(label="Open File 2", command=self.open_file2)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Options Menu
        options_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Options", menu=options_menu)
        options_menu.add_checkbutton(label="Ignore Case Differences", variable=self.ignore_case, command=self.on_option_changed)
        options_menu.add_checkbutton(label="Ignore All Whitespace", variable=self.ignore_whitespace, command=self.on_option_changed)
        options_menu.add_checkbutton(label="Ignore Blank Lines", variable=self.ignore_blank_lines, command=self.on_option_changed)
        options_menu.add_checkbutton(label="Suppress Common Lines", variable=self.suppress_common_lines, command=self.on_option_changed)
        options_menu.add_checkbutton(label="Side-by-Side View", variable=self.side_by_side, command=self.on_option_changed)

        # Context Lines Submenu
        context_menu = tk.Menu(options_menu, tearoff=0)
        options_menu.add_cascade(label="Context Lines", menu=context_menu)
        for num in [0, 1, 2, 3, 4, 5]:
            context_menu.add_radiobutton(label=str(num), variable=self.context_lines, value=num, command=self.on_option_changed)

        # Help Menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    def open_file1(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
            self.text1.delete('1.0', tk.END)
            self.text1.insert(tk.END, content)

    def open_file2(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
            self.text2.delete('1.0', tk.END)
            self.text2.insert(tk.END, content)

    def show_about(self):
        messagebox.showinfo("About DiffAnywhere", "DiffAnywhere 1.0\nA cross-platform GUI application to compare code or text.\n\nDeveloped using Python and Tkinter.")

    def on_option_changed(self):
        self.on_text_modified(None)

    def on_text_modified(self, event):
        if event:
            event.widget.edit_modified(0)  # Reset the modified flag
        text1_content = self.text1.get("1.0", tk.END).splitlines()
        text2_content = self.text2.get("1.0", tk.END).splitlines()

        # Apply options
        text1_processed = self.process_text(text1_content)
        text2_processed = self.process_text(text2_content)

        # Use difflib with options
        sm = difflib.SequenceMatcher(None, text1_processed, text2_processed)
        opcodes = sm.get_opcodes()

        self.diff_text.delete("1.0", tk.END)

        if self.side_by_side.get():
            # Side-by-side view
            for tag, i1, i2, j1, j2 in opcodes:
                for idx in range(max(i2 - i1, j2 - j1)):
                    left_line = text1_processed[i1 + idx] if i1 + idx < i2 else ''
                    right_line = text2_processed[j1 + idx] if j1 + idx < j2 else ''
                    if tag == 'equal':
                        if not self.suppress_common_lines.get():
                            self.diff_text.insert(tk.END, f"{left_line:<50}    {right_line}\n", 'equal')
                    elif tag == 'replace':
                        self.diff_text.insert(tk.END, f"{left_line:<50}    {right_line}\n", 'replace')
                    elif tag == 'delete':
                        self.diff_text.insert(tk.END, f"{left_line:<50}    \n", 'delete')
                    elif tag == 'insert':
                        self.diff_text.insert(tk.END, f"{'':<50}    {right_line}\n", 'insert')
        else:
            # Normal diff view
            context = self.context_lines.get()
            differ = difflib.Differ(charjunk=None if not self.ignore_whitespace.get() else difflib.IS_CHARACTER_JUNK)
            diff = list(differ.compare(text1_processed, text2_processed))
            if self.suppress_common_lines.get():
                diff = [line for line in diff if not line.startswith('  ')]
            if context > 0:
                diff = self.add_context(diff, context)
            self.diff_text.insert(tk.END, '\n'.join(diff))

        # Update line numbers
        self.diff_linenumbers.redraw()
        self.text1_linenumbers.redraw()
        self.text2_linenumbers.redraw()

    def add_context(self, diff_lines, context):
        result = []
        buffer = []
        context_counter = 0
        for line in diff_lines:
            if line.startswith(('  ', '? ')):
                if context_counter < context:
                    buffer.append(line)
                    context_counter += 1
            else:
                if buffer:
                    result.extend(buffer)
                    buffer = []
                    context_counter = 0
                result.append(line)
        return result

    def process_text(self, text_lines):
        processed = []
        for line in text_lines:
            original_line = line
            if self.ignore_case.get():
                line = line.lower()
            if self.ignore_whitespace.get():
                line = ''.join(line.split())
            elif self.ignore_blank_lines.get():
                if line.strip() == '':
                    continue
            processed.append(line)
        return processed

def main():
    root = tk.Tk()
    app = DiffAnywhereApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
