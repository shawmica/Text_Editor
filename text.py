import tkinter as tk
from tkinter import filedialog, messagebox, font, ttk
from tkinter.scrolledtext import ScrolledText
from spellchecker import SpellChecker

class Notepad:
    def __init__(self, root):
        self.root = root
        self.root.title("📝 Notepad - Spell Checker")
        self.root.geometry("900x600")
        self.root.configure(bg="#f4f4f4")

        self.filename = None
        self.wrap = tk.BooleanVar(value=True)
        self.spell = SpellChecker()

        # Font & style setup
        self.custom_font = font.Font(family="Consolas", size=14)

        # Styled text area
        self.text_area = ScrolledText(root, undo=True, wrap=tk.WORD, font=self.custom_font, bg="#ffffff", fg="#222222", insertbackground="black", padx=10, pady=10, relief=tk.FLAT, borderwidth=5)
        self.text_area.pack(expand=1, fill='both', padx=10, pady=(5, 0))
        self.text_area.focus_set()

        # Status Bar
        self.status = tk.Label(root, text="Ln 1, Col 1", anchor='e', bg="#dddddd", fg="#444444", font=("Segoe UI", 10))
        self.status.pack(fill='x', side='bottom')

        self.text_area.bind('<KeyRelease>', self.on_key_release)
        self.text_area.bind('<ButtonRelease>', self.update_status)

        self._create_menu()

    def _create_menu(self):
        menu = tk.Menu(self.root, bg="#f0f0f0", fg="#000000", activebackground="#d3d3d3", font=("Segoe UI", 10))
        self.root.config(menu=menu)

        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open...", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As...", command=self.save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_app)

        edit_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=self.text_area.edit_undo)
        edit_menu.add_command(label="Redo", command=self.text_area.edit_redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=lambda: self.text_area.event_generate("<<Cut>>"))
        edit_menu.add_command(label="Copy", command=lambda: self.text_area.event_generate("<<Copy>>"))
        edit_menu.add_command(label="Paste", command=lambda: self.text_area.event_generate("<<Paste>>"))
        edit_menu.add_command(label="Select All", command=lambda: self.text_area.event_generate("<<SelectAll>>"))

        format_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Format", menu=format_menu)
        format_menu.add_checkbutton(label="Word Wrap", onvalue=True, offvalue=False,
                                    variable=self.wrap, command=self.toggle_wrap)

        font_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Font", menu=font_menu)
        font_menu.add_command(label="Increase Font", command=self.increase_font)
        font_menu.add_command(label="Decrease Font", command=self.decrease_font)

    def new_file(self):
        if self.confirm_unsaved_changes():
            self.text_area.delete(1.0, tk.END)
            self.filename = None
            self.root.title("📝 Notepad - Spell Checker")

    def open_file(self):
        if self.confirm_unsaved_changes():
            file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
            if file_path:
                with open(file_path, 'r', encoding='utf-8') as file:
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(tk.END, file.read())
                    self.filename = file_path
                    self.root.title(f"📝 Notepad - {self.filename}")
                    self.spell_check()

    def save_file(self):
        if self.filename:
            with open(self.filename, 'w', encoding='utf-8') as file:
                file.write(self.text_area.get(1.0, tk.END).strip())
        else:
            self.save_as()

    def save_as(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            self.filename = file_path
            self.save_file()
            self.root.title(f"📝 Notepad - {self.filename}")

    def exit_app(self):
        if self.confirm_unsaved_changes():
            self.root.destroy()

    def confirm_unsaved_changes(self):
        if self.text_area.edit_modified():
            result = messagebox.askyesnocancel("Unsaved Changes", "Do you want to save changes?")
            if result:  # Yes
                self.save_file()
            elif result is None:  # Cancel
                return False
        return True

    def toggle_wrap(self):
        self.text_area.config(wrap=tk.WORD if self.wrap.get() else tk.NONE)

    def increase_font(self):
        current_size = self.custom_font['size']
        self.custom_font.configure(size=current_size + 2)

    def decrease_font(self):
        current_size = self.custom_font['size']
        if current_size > 6:
            self.custom_font.configure(size=current_size - 2)

    def update_status(self, event=None):
        row, col = self.text_area.index(tk.INSERT).split('.')
        self.status.config(text=f"Ln {row}, Col {int(col) + 1}")

    def on_key_release(self, event=None):
        self.update_status()
        self.spell_check()

    def spell_check(self):
        self.text_area.tag_remove("misspelled", "1.0", tk.END)
        text = self.text_area.get("1.0", tk.END)
        words = text.split()
        misspelled = self.spell.unknown(words)

        for word in misspelled:
            start_idx = "1.0"
            while True:
                pos = self.text_area.search(rf'\y{word}\y', start_idx, stopindex=tk.END, regexp=True)
                if not pos:
                    break
                end_pos = f"{pos}+{len(word)}c"
                self.text_area.tag_add("misspelled", pos, end_pos)
                start_idx = end_pos

        self.text_area.tag_config("misspelled", underline=True, foreground="red")


# Run the Notepad
if __name__ == "__main__":
    root = tk.Tk()
    app = Notepad(root)
    root.mainloop()
