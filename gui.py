import subprocess
import threading
import sys
import os
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulador de Estabelecimento de Chaves")
        self.geometry("720x500")
        self.configure(bg="#1e1e1e")

        self.process = None
        self.create_widgets()

    def create_widgets(self):
        # Frame principal
        frame = tk.Frame(self, bg="#1e1e1e")
        frame.pack(padx=20, pady=20, fill="x")

        # Quantidade de testes
        tk.Label(frame, text="Quantidade de testes:", fg="white", bg="#1e1e1e", anchor="w").pack(fill="x")
        self.entry_testes = tk.Entry(frame)
        self.entry_testes.insert(0, "100")
        self.entry_testes.pack(fill="x", pady=(0, 10))

        # Tamanho da cadeia
        tk.Label(frame, text="Tamanho da cadeia de bits:", fg="white", bg="#1e1e1e", anchor="w").pack(fill="x")
        self.combo_bits = ttk.Combobox(frame, values=[7, 15, 127, 255], state="readonly")
        self.combo_bits.set(15)
        self.combo_bits.pack(fill="x", pady=(0, 10))

        # Amplificação de privacidade sempre habilitada
        tk.Label(frame, text="Amplificação de privacidade (SHA-256): HABILITADA", fg="#00ff00", bg="#1e1e1e", anchor="w").pack(fill="x", pady=(0, 10))

        # Botões
        btn_frame = tk.Frame(frame, bg="#1e1e1e")
        btn_frame.pack(fill="x", pady=10)

        self.btn_run = tk.Button(btn_frame, text="▶ Executar", bg="#007acc", fg="white", command=self.run_script)
        self.btn_run.pack(side="left", expand=True, fill="x", padx=(0, 5))

        self.btn_stop = tk.Button(btn_frame, text="⏹ Parar", bg="#cc0000", fg="white", state="disabled", command=self.stop_script)
        self.btn_stop.pack(side="left", expand=True, fill="x", padx=(5, 0))

        # Saída de texto
        tk.Label(self, text="Saída do programa:", fg="white", bg="#1e1e1e", anchor="w").pack(fill="x", padx=20)
        self.output = scrolledtext.ScrolledText(self, wrap=tk.WORD, bg="#252526", fg="#d4d4d4", insertbackground="white")
        self.output.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def run_script(self):
        if self.process is not None:
            messagebox.showwarning("Aviso", "O processo já está em execução.")
            return

        try:
            quantidade = int(self.entry_testes.get())
            bits = int(self.combo_bits.get())
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos.")
            return

        amplificacao = 's'  # Amplificação sempre habilitada

        self.output.delete("1.0", tk.END)
        self.append_output(f"Iniciando execução...\n\n")

        # Monta o input simulado (sem pergunta de amplificação)
        user_input = f"{quantidade}\n{bits}\n"

        # Caminho do main.py
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.py")

        def target():
            try:
                # Executa o main.py e envia a entrada simulada
                self.process = subprocess.Popen(
                    [sys.executable, script_path],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1
                )

                # Envia todo o input e obtém a saída completa
                output, _ = self.process.communicate(user_input)

                # Mostra a saída no TextBox
                self.append_output(output)

            except Exception as e:
                self.append_output(f"\n[ERRO] {e}\n")

            finally:
                self.process = None
                self.btn_run.config(state="normal")
                self.btn_stop.config(state="disabled")
                self.append_output("\nExecução finalizada.\n")

        # Atualiza botões
        self.btn_run.config(state="disabled")
        self.btn_stop.config(state="normal")

        # Executa em thread separada para não travar a GUI
        thread = threading.Thread(target=target, daemon=True)
        thread.start()

    def stop_script(self):
        if self.process:
            self.process.terminate()
            self.process = None
            self.append_output("\nProcesso interrompido pelo usuário.\n")
        self.btn_run.config(state="normal")
        self.btn_stop.config(state="disabled")

    def append_output(self, text):
        self.output.insert(tk.END, text)
        self.output.see(tk.END)

if __name__ == "__main__":
    app = App()
    app.mainloop()
