nós estamos fazendo a simulação em banda base (baseband)
Não usa portadora
Trabalha diretamente com símbolos BPSK {-1, +1} ou QPSK complexos
Aplica ganho Rayleigh + ruído direto nos símbolos

simular frequencia de portadora seria bom para:
Simular interferência entre canais adjacentes
Calcular banda de coerência do canal
Implementar receptor real com demodulação

RODAR:
source .venv/bin/activate
python interfaces/teoria/teoria_ber_bpsk.py
python interfaces/teoria/teoria_ber_qpsk.py
python interfaces/teoria/plot_fases_modulacao.py