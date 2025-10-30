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

        # Tipo de modulação
        tk.Label(frame, text="Tipo de modulação:", fg="white", bg="#1e1e1e", anchor="w").pack(fill="x")
        self.combo_modulacao = ttk.Combobox(frame, values=["BPSK", "QPSK"], state="readonly")
        self.combo_modulacao.set("BPSK")
        self.combo_modulacao.pack(fill="x", pady=(0, 10))

        # Amplificação de privacidade sempre habilitada
        tk.Label(frame, text="Amplificação de privacidade (SHA-256): HABILITADA", fg="#00ff00", bg="#1e1e1e", anchor="w").pack(fill="x", pady=(0, 10))

        # Barra de progresso
        self.progress_frame = tk.Frame(frame, bg="#1e1e1e")
        self.progress_frame.pack(fill="x", pady=(0, 10))
        
        self.progress_label = tk.Label(self.progress_frame, text="", fg="#cccccc", bg="#1e1e1e", anchor="w")
        self.progress_label.pack(fill="x")
        
        self.progressbar = ttk.Progressbar(self.progress_frame, mode='indeterminate')
        
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

        # Determina o tipo de modulação selecionado
        modulacao_tipo = self.combo_modulacao.get()
        modulacao_input = "1" if modulacao_tipo == "BPSK" else "2"

        amplificacao = 's'  # Amplificação sempre habilitada

        self.output.delete("1.0", tk.END)
        self.append_output(f"Iniciando execução...\n\n")
        
        # Mostra e inicia a barra de progresso
        self.progress_label.config(text="Executando simulação...")
        self.progressbar.pack(fill="x", pady=(5, 0))
        self.progressbar.start(10)

        # Monta o input simulado (com escolha de modulação)
        user_input = f"{quantidade}\n{bits}\n{modulacao_input}\n"

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
                    bufsize=1,
                    universal_newlines=True
                )

                # Envia o input
                self.process.stdin.write(user_input)
                self.process.stdin.flush()
                self.process.stdin.close()

                # Lê a saída linha por linha em tempo real
                for line in iter(self.process.stdout.readline, ''):
                    if line:
                        # Atualiza label de progresso se for linha de progresso
                        if "Progresso geral" in line or "σ=" in line:
                            # Extrai informação de progresso
                            import re
                            match = re.search(r'(\d+)%', line)
                            if match:
                                percent = match.group(1)
                                self.progress_label.config(text=f"Progresso: {percent}%")
                        
                        self.append_output(line)
                    
                # Aguarda o processo terminar
                self.process.wait()

            except Exception as e:
                self.append_output(f"\n[ERRO] {e}\n")

            finally:
                self.process = None
                self.btn_run.config(state="normal")
                self.btn_stop.config(state="disabled")
                
                # Para e esconde a barra de progresso
                self.progressbar.stop()
                self.progressbar.pack_forget()
                self.progress_label.config(text="")
                
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
        
        # Para e esconde a barra de progresso
        self.progressbar.stop()
        self.progressbar.pack_forget()
        self.progress_label.config(text="")
        
        self.btn_run.config(state="normal")
        self.btn_stop.config(state="disabled")

    def append_output(self, text):
        self.output.insert(tk.END, text)
        self.output.see(tk.END)

if __name__ == "__main__":
    app = App()
    app.mainloop()
