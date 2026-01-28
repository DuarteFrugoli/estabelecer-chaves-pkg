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
        self.geometry("720x700")
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

        # Perfil de dispositivo IoT
        tk.Label(frame, text="Perfil de dispositivo IoT:", fg="white", bg="#1e1e1e", anchor="w").pack(fill="x")
        self.combo_dispositivo = ttk.Combobox(
            frame, 
            values=[
                "1. Pessoa Andando (v=5 km/h, fc=2.4 GHz)",
                "2. Sensor Estático (v=0 km/h)",
                "3. Veículo Urbano (v=60 km/h, fc=5.9 GHz)",
                "4. Drone (v=30 km/h, fc=2.4 GHz)",
                "5. NB-IoT (v=3 km/h, fc=900 MHz)",
                "6. Configuração Manual"
            ], 
            state="readonly"
        )
        self.combo_dispositivo.set("1. Pessoa Andando (v=5 km/h, fc=2.4 GHz)")
        self.combo_dispositivo.bind("<<ComboboxSelected>>", self.on_dispositivo_change)
        self.combo_dispositivo.pack(fill="x", pady=(0, 10))

        # Campos de configuração manual (sempre visíveis, mas inicialmente desabilitados)
        self.label_erro = tk.Label(frame, text="Erro de estimativa (0.0-1.0):", fg="#888888", bg="#1e1e1e", anchor="w")
        self.label_erro.pack(fill="x")
        self.entry_erro = tk.Entry(frame, state="disabled")
        self.entry_erro.insert(0, "0.10")
        self.entry_erro.pack(fill="x", pady=(0, 5))
        
        self.label_vel = tk.Label(frame, text="Velocidade (km/h):", fg="#888888", bg="#1e1e1e", anchor="w")
        self.label_vel.pack(fill="x")
        self.entry_velocidade = tk.Entry(frame, state="disabled")
        self.entry_velocidade.insert(0, "5.0")
        self.entry_velocidade.pack(fill="x", pady=(0, 5))
        
        self.label_guard = tk.Label(frame, text="Guard band (múltiplos de σ):", fg="#888888", bg="#1e1e1e", anchor="w")
        self.label_guard.pack(fill="x")
        self.entry_guard = tk.Entry(frame, state="disabled")
        self.entry_guard.insert(0, "0.5")
        self.entry_guard.pack(fill="x", pady=(0, 10))

        # Amplificação de privacidade sempre habilitada
        tk.Label(frame, text="Amplificação de privacidade (SHA-256): HABILITADA", fg="#00ff00", bg="#1e1e1e", anchor="w").pack(fill="x", pady=(10, 10))

        # Barra de progresso geral
        self.progress_frame_geral = tk.Frame(frame, bg="#1e1e1e")
        self.progress_frame_geral.pack(fill="x", pady=(0, 5))
        
        self.progress_label_geral = tk.Label(self.progress_frame_geral, text="", fg="#00ff00", bg="#1e1e1e", anchor="w", font=("Arial", 9, "bold"))
        self.progress_label_geral.pack(fill="x")
        
        self.progressbar_geral = ttk.Progressbar(self.progress_frame_geral, mode='determinate')
        
        # Barra de progresso do subplot atual
        self.progress_frame = tk.Frame(frame, bg="#1e1e1e")
        self.progress_frame.pack(fill="x", pady=(0, 10))
        
        self.progress_label = tk.Label(self.progress_frame, text="", fg="#00aaff", bg="#1e1e1e", anchor="w", font=("Arial", 8))
        self.progress_label.pack(fill="x")
        
        self.progressbar = ttk.Progressbar(self.progress_frame, mode='determinate')
        
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

    def on_dispositivo_change(self, event):
        """Habilita/desabilita campos de configuração manual"""
        dispositivo_selecionado = self.combo_dispositivo.get()
        if dispositivo_selecionado.startswith("6."):
            # Habilita os campos e muda cor das labels para laranja
            self.entry_erro.config(state="normal")
            self.entry_velocidade.config(state="normal")
            self.entry_guard.config(state="normal")
            self.label_erro.config(fg="#ffaa00")
            self.label_vel.config(fg="#ffaa00")
            self.label_guard.config(fg="#ffaa00")
        else:
            # Desabilita os campos e muda cor das labels para cinza
            self.entry_erro.config(state="disabled")
            self.entry_velocidade.config(state="disabled")
            self.entry_guard.config(state="disabled")
            self.label_erro.config(fg="#888888")
            self.label_vel.config(fg="#888888")
            self.label_guard.config(fg="#888888")

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

        # Determina o perfil de dispositivo selecionado (extrai apenas o número)
        dispositivo_selecionado = self.combo_dispositivo.get()
        dispositivo_input = dispositivo_selecionado.split(".")[0]  # Extrai "1", "2", etc.

        # Monta o input base (quantidade, bits, modulação, dispositivo)
        user_input = f"{quantidade}\n{bits}\n{modulacao_input}\n{dispositivo_input}\n"

        # Se for configuração manual (opção 6), adiciona os parâmetros manualmente
        if dispositivo_input == "6":
            try:
                erro = float(self.entry_erro.get())
                velocidade = float(self.entry_velocidade.get())
                guard = float(self.entry_guard.get())
                
                # Valida valores
                if not (0.0 <= erro <= 1.0):
                    messagebox.showerror("Erro", "Erro de estimativa deve estar entre 0.0 e 1.0")
                    return
                if velocidade < 0:
                    messagebox.showerror("Erro", "Velocidade não pode ser negativa")
                    return
                if not (0.0 <= guard <= 2.0):
                    messagebox.showerror("Erro", "Guard band deve estar entre 0.0 e 2.0")
                    return
                    
                # Adiciona parâmetros ao input
                user_input += f"{erro}\n{velocidade}\n{guard}\n"
            except ValueError:
                messagebox.showerror("Erro", "Valores de configuração manual inválidos")
                return

        amplificacao = 's'  # Amplificação sempre habilitada

        self.output.delete("1.0", tk.END)
        self.append_output(f"Iniciando execução...\n\n")
        
        # Mostra e inicia as barras de progresso
        self.progress_label_geral.config(text="Progresso geral: 0%")
        self.progressbar_geral.pack(fill="x", pady=(5, 0))
        self.progressbar_geral['value'] = 0
        
        self.progress_label.config(text="Aguardando início...")
        self.progressbar.pack(fill="x", pady=(5, 0))
        self.progressbar['value'] = 0

        # Monta o input simulado (quantidade, bits, modulação, dispositivo)
        user_input = f"{quantidade}\n{bits}\n{modulacao_input}\n{dispositivo_input}\n"

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
                        import re
                        
                        # Progresso geral (barra verde)
                        if "Progresso geral" in line:
                            match = re.search(r'(\d+)%', line)
                            if match:
                                percent = int(match.group(1))
                                self.progressbar_geral['value'] = percent
                                self.progress_label_geral.config(text=f"Progresso geral: {percent}%")
                        
                        # Progresso do subplot atual (barra azul)
                        elif "σ=" in line:
                            # Extrai o valor de sigma e a porcentagem
                            match_sigma = re.search(r'σ=([\d.]+)', line)
                            match_percent = re.search(r'(\d+)%', line)
                            if match_sigma and match_percent:
                                sigma = match_sigma.group(1)
                                percent = int(match_percent.group(1))
                                self.progressbar['value'] = percent
                                self.progress_label.config(text=f"σ={sigma}: {percent}%")
                        
                        self.append_output(line)
                    
                # Aguarda o processo terminar
                self.process.wait()

            except Exception as e:
                self.append_output(f"\n[ERRO] {e}\n")

            finally:
                self.process = None
                self.btn_run.config(state="normal")
                self.btn_stop.config(state="disabled")
                
                # Esconde as barras de progresso
                self.progressbar_geral.pack_forget()
                self.progress_label_geral.config(text="")
                
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
        
        # Esconde as barras de progresso
        self.progressbar_geral.pack_forget()
        self.progress_label_geral.config(text="")
        
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
