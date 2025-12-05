import subprocess
import threading
import sys
import os
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import numpy as np

class AdvancedApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulador Avançado de Estabelecimento de Chaves")
        self.geometry("900x700")
        self.configure(bg="#1e1e1e")

        self.process = None
        self.create_widgets()

    def create_widgets(self):
        # Frame principal com scroll
        main_frame = tk.Frame(self, bg="#1e1e1e")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Canvas com scrollbar para os parâmetros
        canvas = tk.Canvas(main_frame, bg="#1e1e1e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#1e1e1e")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # ===== SEÇÃO 1: PARÂMETROS BÁSICOS =====
        self.create_section_header(scrollable_frame, "PARÂMETROS BÁSICOS")

        # Quantidade de testes
        self.create_labeled_entry(scrollable_frame, "Quantidade de testes:", "100", "entry_testes")

        # Tamanho da cadeia
        self.create_labeled_combobox(scrollable_frame, "Tamanho da cadeia de bits:", 
                                     [7, 15, 127, 255], 15, "combo_bits")

        # Tipo de modulação
        self.create_labeled_combobox(scrollable_frame, "Tipo de modulação:", 
                                     ["BPSK", "QPSK"], "BPSK", "combo_modulacao")

        # ===== SEÇÃO 2: PARÂMETROS DO CANAL =====
        self.create_section_header(scrollable_frame, "PARÂMETROS DO CANAL")

        # Parâmetro Rayleigh (sigma)
        self.create_labeled_entry(scrollable_frame, "Parâmetro Rayleigh (σ):", 
                                 f"{1.0/np.sqrt(2):.6f}", "entry_sigma",
                                 hint="Padrão normalizado: 1/√2 ≈ 0.707")

        # Correlação do canal
        self.create_labeled_entry(scrollable_frame, "Correlação do canal (ρ):", "0.9", "entry_correlacao",
                                 hint="Reciprocidade (0.0 a 1.0)")

        # ===== SEÇÃO 3: PARÂMETROS DE SNR =====
        self.create_section_header(scrollable_frame, "📡 PARÂMETROS DE SNR")

        # SNR mínimo
        self.create_labeled_entry(scrollable_frame, "SNR mínimo (dB):", "-10", "entry_snr_min")

        # SNR máximo
        self.create_labeled_entry(scrollable_frame, "SNR máximo (dB):", "30", "entry_snr_max")

        # Número de pontos SNR
        self.create_labeled_entry(scrollable_frame, "Número de pontos SNR:", "18", "entry_snr_pontos")

        # ===== SEÇÃO 4: PARÂMETROS DE RUÍDO =====
        self.create_section_header(scrollable_frame, "🔊 PARÂMETROS DE RUÍDO")

        # Potência do sinal
        self.create_labeled_entry(scrollable_frame, "Potência do sinal (Es):", "1.0", "entry_potencia",
                                 hint="Padrão: 1.0 (normalizado)")

        # Média do ruído
        self.create_labeled_entry(scrollable_frame, "Média do ruído:", "0.0", "entry_media_ruido",
                                 hint="Padrão: 0.0 (gaussiano centrado)")

        # ===== SEÇÃO 5: OPÇÕES AVANÇADAS =====
        self.create_section_header(scrollable_frame, "⚙️ OPÇÕES AVANÇADAS")

        # Amplificação de privacidade
        frame_amp = tk.Frame(scrollable_frame, bg="#1e1e1e")
        frame_amp.pack(fill="x", pady=5)
        
        self.var_amplificacao = tk.BooleanVar(value=True)
        tk.Checkbutton(frame_amp, text="Habilitar amplificação de privacidade (SHA-256)", 
                      variable=self.var_amplificacao, fg="white", bg="#1e1e1e", 
                      selectcolor="#007acc", activebackground="#1e1e1e",
                      activeforeground="white").pack(anchor="w")

        # ===== BARRA DE PROGRESSO =====
        self.progress_frame = tk.Frame(scrollable_frame, bg="#1e1e1e")
        self.progress_frame.pack(fill="x", pady=(20, 5))
        
        self.progress_label = tk.Label(self.progress_frame, text="", fg="#00ff00", 
                                      bg="#1e1e1e", anchor="w", font=("Arial", 9, "bold"))
        self.progress_label.pack(fill="x")
        
        self.progressbar = ttk.Progressbar(self.progress_frame, mode='determinate')

        # ===== BOTÕES =====
        btn_frame = tk.Frame(scrollable_frame, bg="#1e1e1e")
        btn_frame.pack(fill="x", pady=20)

        self.btn_run = tk.Button(btn_frame, text="▶ Executar Simulação", bg="#007acc", 
                                fg="white", font=("Arial", 10, "bold"), command=self.run_script)
        self.btn_run.pack(side="left", expand=True, fill="x", padx=(0, 5))

        self.btn_stop = tk.Button(btn_frame, text="⏹ Parar", bg="#cc0000", fg="white", 
                                 font=("Arial", 10, "bold"), state="disabled", command=self.stop_script)
        self.btn_stop.pack(side="left", expand=True, fill="x", padx=(5, 0))

        # ===== SAÍDA DE TEXTO =====
        output_frame = tk.Frame(self, bg="#1e1e1e")
        output_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        tk.Label(output_frame, text="📋 Saída do programa:", fg="white", bg="#1e1e1e", 
                anchor="w", font=("Arial", 10, "bold")).pack(fill="x")
        
        self.output = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, bg="#252526", 
                                               fg="#d4d4d4", insertbackground="white", 
                                               font=("Consolas", 9))
        self.output.pack(fill="both", expand=True)

    def create_section_header(self, parent, text):
        """Cria um cabeçalho de seção"""
        frame = tk.Frame(parent, bg="#2d2d30", height=2)
        frame.pack(fill="x", pady=(15, 10))
        
        label = tk.Label(parent, text=text, fg="#00d4ff", bg="#1e1e1e", 
                        anchor="w", font=("Arial", 11, "bold"))
        label.pack(fill="x", pady=(0, 5))

    def create_labeled_entry(self, parent, label_text, default_value, attr_name, hint=None):
        """Cria um label e um entry"""
        frame = tk.Frame(parent, bg="#1e1e1e")
        frame.pack(fill="x", pady=3)
        
        tk.Label(frame, text=label_text, fg="white", bg="#1e1e1e", 
                anchor="w", width=35).pack(side="left")
        
        entry = tk.Entry(frame, width=20)
        entry.insert(0, default_value)
        entry.pack(side="left", padx=(5, 0))
        
        setattr(self, attr_name, entry)
        
        if hint:
            tk.Label(frame, text=f"  💡 {hint}", fg="#888888", bg="#1e1e1e", 
                    anchor="w", font=("Arial", 8)).pack(side="left", padx=(10, 0))

    def create_labeled_combobox(self, parent, label_text, values, default_value, attr_name):
        """Cria um label e um combobox"""
        frame = tk.Frame(parent, bg="#1e1e1e")
        frame.pack(fill="x", pady=3)
        
        tk.Label(frame, text=label_text, fg="white", bg="#1e1e1e", 
                anchor="w", width=35).pack(side="left")
        
        combo = ttk.Combobox(frame, values=values, state="readonly", width=18)
        combo.set(default_value)
        combo.pack(side="left", padx=(5, 0))
        
        setattr(self, attr_name, combo)

    def validate_inputs(self):
        """Valida todas as entradas"""
        try:
            quantidade = int(self.entry_testes.get())
            bits = int(self.combo_bits.get())
            sigma = float(self.entry_sigma.get())
            correlacao = float(self.entry_correlacao.get())
            snr_min = float(self.entry_snr_min.get())
            snr_max = float(self.entry_snr_max.get())
            snr_pontos = int(self.entry_snr_pontos.get())
            potencia = float(self.entry_potencia.get())
            media_ruido = float(self.entry_media_ruido.get())
            
            # Validações
            if quantidade <= 0:
                raise ValueError("Quantidade de testes deve ser positiva")
            if sigma <= 0:
                raise ValueError("Sigma deve ser positivo")
            if not (0 <= correlacao <= 1):
                raise ValueError("Correlação deve estar entre 0 e 1")
            if snr_min >= snr_max:
                raise ValueError("SNR mínimo deve ser menor que SNR máximo")
            if snr_pontos <= 0:
                raise ValueError("Número de pontos SNR deve ser positivo")
            if potencia <= 0:
                raise ValueError("Potência do sinal deve ser positiva")
            
            return True
            
        except ValueError as e:
            messagebox.showerror("Erro de Validação", str(e))
            return False

    def run_script(self):
        if self.process is not None:
            messagebox.showwarning("Aviso", "O processo já está em execução.")
            return

        if not self.validate_inputs():
            return

        # Coleta todos os parâmetros
        params = {
            'quantidade': self.entry_testes.get(),
            'bits': self.combo_bits.get(),
            'modulacao': "1" if self.combo_modulacao.get() == "BPSK" else "2",
            'sigma': self.entry_sigma.get(),
            'correlacao': self.entry_correlacao.get(),
            'snr_min': self.entry_snr_min.get(),
            'snr_max': self.entry_snr_max.get(),
            'snr_pontos': self.entry_snr_pontos.get(),
            'potencia': self.entry_potencia.get(),
            'media_ruido': self.entry_media_ruido.get(),
            'amplificacao': 's' if self.var_amplificacao.get() else 'n'
        }

        self.output.delete("1.0", tk.END)
        self.append_output(f"🚀 Iniciando simulação avançada...\n")
        self.append_output(f"{'='*60}\n")
        self.append_output(f"PARÂMETROS CONFIGURADOS:\n")
        self.append_output(f"  • Testes: {params['quantidade']}\n")
        self.append_output(f"  • Bits: {params['bits']}\n")
        self.append_output(f"  • Modulação: {self.combo_modulacao.get()}\n")
        self.append_output(f"  • Sigma (σ): {params['sigma']}\n")
        self.append_output(f"  • Correlação (ρ): {params['correlacao']}\n")
        self.append_output(f"  • SNR: {params['snr_min']} a {params['snr_max']} dB ({params['snr_pontos']} pontos)\n")
        self.append_output(f"  • Potência: {params['potencia']}\n")
        self.append_output(f"  • Amplificação: {'SIM' if params['amplificacao']=='s' else 'NÃO'}\n")
        self.append_output(f"{'='*60}\n\n")
        
        # Mostra barra de progresso
        self.progress_label.config(text="Aguardando início...")
        self.progressbar.pack(fill="x", pady=(5, 0))
        self.progressbar['value'] = 0

        # Monta o input
        user_input = '\n'.join([
            params['quantidade'],
            params['bits'],
            params['modulacao'],
            params['sigma'],
            params['correlacao'],
            params['snr_min'],
            params['snr_max'],
            params['snr_pontos'],
            params['potencia'],
            params['media_ruido'],
            params['amplificacao']
        ]) + '\n'

        # Caminho do main_advanced.py
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main_advanced.py")

        def target():
            try:
                self.process = subprocess.Popen(
                    [sys.executable, script_path],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    universal_newlines=True
                )

                self.process.stdin.write(user_input)
                self.process.stdin.flush()
                self.process.stdin.close()

                import re
                for line in iter(self.process.stdout.readline, ''):
                    if line:
                        # Atualiza progresso
                        match = re.search(r'(\d+)%', line)
                        if match:
                            percent = int(match.group(1))
                            self.progressbar['value'] = percent
                            self.progress_label.config(text=f"Progresso: {percent}%")
                        
                        self.append_output(line)
                
                self.process.wait()

            except Exception as e:
                self.append_output(f"\n❌ [ERRO] {e}\n")

            finally:
                self.process = None
                self.btn_run.config(state="normal")
                self.btn_stop.config(state="disabled")
                self.progressbar.pack_forget()
                self.progress_label.config(text="")
                self.append_output("\n✅ Execução finalizada.\n")

        self.btn_run.config(state="disabled")
        self.btn_stop.config(state="normal")

        thread = threading.Thread(target=target, daemon=True)
        thread.start()

    def stop_script(self):
        if self.process:
            self.process.terminate()
            self.process = None
            self.append_output("\n⏹ Processo interrompido pelo usuário.\n")
        
        self.progressbar.pack_forget()
        self.progress_label.config(text="")
        self.btn_run.config(state="normal")
        self.btn_stop.config(state="disabled")

    def append_output(self, text):
        """Adiciona texto à saída"""
        self.output.insert(tk.END, text)
        self.output.see(tk.END)
        self.update_idletasks()


if __name__ == "__main__":
    app = AdvancedApp()
    app.mainloop()