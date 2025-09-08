# Alterações no Código

1. Correção da modulação

Antes: bits eram gerados em {0,1} → equivalente a OOK.

Alterado para BPSK: bits convertidos para {−1,+1} (2*bits - 1).



2. Modelagem do canal

Adição de canal Rayleigh (complexo) para simular cenários realistas sem linha de visada.



3. Ruído AWGN

Inclusão de cálculo do ruído gaussiano aditivo com base no valor de SNR desejado.

Normalização do sinal transmitido para manter potência unitária antes de calcular variância do ruído.



4. Detecção no receptor

Alterado para decisão por sinal positivo ou negativo (>= 0 → bit 1, < 0 → bit 0).

Isso substituiu a comparação binária anterior, compatível com BPSK.



5. Cálculo da KDR

Inclusão de função que compara bit a bit as chaves de Alice e Bob e retorna a Key Disagreement Rate (% de discrepância).



6. Reconciliação de informação (Code-Offset Method)

Implementado esquema com BCH codes para corrigir diferenças entre as chaves.

Incluídas etapas: geração de código, XOR com chave de Alice, reconstrução em Bob, decodificação e verificação.



7. Organização do fluxo do programa

Estruturado em etapas claras:

1. Geração de bits.


2. Modulação (BPSK).


3. Canal + ruído.


4. Recepção/demodulação.


5. Comparação (KDR).


6. Reconciliação com BCH.