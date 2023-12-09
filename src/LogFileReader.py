import tkinter as tk
from tkinter import filedialog
import pandas as pd

file_path = ""  # file_pathをグローバルスコープで初期化


def open_file():
    global iterator, max_lines, file_path
    file_path = filedialog.askopenfilename(
        initialdir="/", title="Select File", filetypes=(("All files", "*.*"),))
    if file_path:
        df = pd.read_csv(file_path, header=None)  # ヘッダー行を含めずに読み込む
        max_lines = len(df)
        max_lines_label.config(text=f"Max Lines: {max_lines}")


def display_next_lines():
    global iterator, max_lines, file_path
    try:
        lines_to_read = entry_lines.get()
        start_line = entry_start_line.get()

        # 入力が空白の場合はエラーを表示
        if not lines_to_read or not start_line:
            raise ValueError("Please enter both lines to read and start line.")

        lines_to_read = int(lines_to_read)
        start_line = int(start_line)

        iterator = pd.read_csv(file_path, skiprows=range(
            1, start_line), chunksize=lines_to_read, iterator=True)

        # ファイルが読み込まれるまでTextウィジェットを非表示にする
        text_widget.pack_forget()
        display_next_chunk()

    except ValueError as e:
        text_widget.config(state=tk.NORMAL)
        text_widget.delete("1.0", tk.END)
        text_widget.insert(tk.END, f"Error: {e}")
        text_widget.config(state=tk.DISABLED)


def display_next_chunk():
    global iterator
    try:
        chunk = next(iterator)
        if not chunk.empty:
            content = "\n".join(chunk.astype(str).apply(
                lambda row: "\t".join(row), axis=1).tolist())
            text_widget.config(state=tk.NORMAL)  # 編集可能にする
            text_widget.delete("1.0", tk.END)  # 既存のテキストをクリア
            text_widget.insert(tk.END, content)
            text_widget.config(state=tk.DISABLED)  # 編集不可にする
            text_widget.pack(pady=10, padx=10)  # ファイルが読み込まれたら再表示
        else:
            text_widget.config(state=tk.NORMAL)
            text_widget.delete("1.0", tk.END)
            text_widget.insert(tk.END, "End of File")
            text_widget.config(state=tk.DISABLED)
    except StopIteration:
        text_widget.config(state=tk.NORMAL)
        text_widget.delete("1.0", tk.END)
        text_widget.insert(tk.END, "End of File")
        text_widget.config(state=tk.DISABLED)


# GUIのセットアップ
root = tk.Tk()
root.title("Log file reader")

# ウィンドウの初期サイズを指定 (幅x高さ)
root.geometry("500x500")

# ファイルを読み込むボタン
open_button = tk.Button(root, text="対象ファイルの選択", command=open_file)
open_button.pack(pady=10)

# 最大行数を表示するラベルを追加
max_lines_label = tk.Label(root, text="保存されている行数: 0")
max_lines_label.pack(pady=5)

# 行数を入力するフィールドを追加
label_lines = tk.Label(root, text="表示させる行数（数字を入力）:")
label_lines.pack(pady=5)

entry_lines = tk.Entry(root)
entry_lines.pack(pady=5)

# 開始行を入力するフィールドを追加
label_start_line = tk.Label(root, text="開始位置（表示させたいログの開始行を入力）:")
label_start_line.pack(pady=5)

entry_start_line = tk.Entry(root)
entry_start_line.pack(pady=5)

# テキストウィジェットに変更
text_widget = tk.Text(root, wrap=tk.WORD, state=tk.DISABLED)  # 編集不可に設定

# ボタンを押すと非表示のテキストウィジェットが表示されるようになります
show_text_button = tk.Button(
    root, text="内容を表示する", command=display_next_lines)
show_text_button.pack(pady=10)

# メインループ
root.mainloop()
