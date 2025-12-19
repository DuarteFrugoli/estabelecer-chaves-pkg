# Referências Bibliográficas Utilizadas no Artigo

Este documento resume as referências bibliográficas utilizadas no artigo sobre Geração de Chaves Criptográficas em Camada Física.

---

## 📚 Livros Fundamentais

### cirani_iot (2019)
**Título:** Internet of Things: Architectures, Protocols and Standards  
**Autores:** Cirani, Simone; Picone, Marco; Veltri, Luca; Ferrari, Gianluigi  
**Editora:** John Wiley & Sons

**Sobre o que trata:**  
Livro fundamental sobre arquiteturas e protocolos de Internet das Coisas (IoT). Aborda os desafios de segurança, escalabilidade e eficiência energética em dispositivos IoT. Utilizado para contextualizar os requisitos de dispositivos com recursos limitados e justificar a necessidade de mecanismos leves de estabelecimento de chaves.

---

### stallings_crypto (2017)
**Título:** Cryptography and Network Security: Principles and Practice (7ª edição)  
**Autor:** Stallings, William  
**Editora:** Pearson

**Sobre o que trata:**  
Referência clássica sobre criptografia e segurança de redes. Cobre os cinco pilares da segurança da informação (confidencialidade, integridade, autenticidade, irretratabilidade, disponibilidade), algoritmos criptográficos simétricos (AES, DES) e assimétricos (RSA), além de protocolos de comunicação segura. Utilizado para fundamentar os conceitos básicos de criptografia e explicar o problema de distribuição de chaves.

---

### goldsmith_wireless (2005)
**Título:** Wireless Communications  
**Autora:** Goldsmith, Andrea  
**Editora:** Cambridge University Press

**Sobre o que trata:**  
Livro fundamental sobre comunicações sem fio. Aborda modelagem de canais, desvanecimento Rayleigh, propagação multipercurso, e propriedades estatísticas do canal wireless. Utilizado para fundamentar a modelagem matemática do canal e explicar o desvanecimento (fading) utilizado na geração de entropia.

---

### tse_viswanath (2005)
**Título:** Fundamentals of Wireless Communication  
**Autores:** Tse, David; Viswanath, Pramod  
**Editora:** Cambridge University Press

**Sobre o que trata:**  
Livro acadêmico sobre fundamentos de comunicação sem fio. Cobre teoria da informação aplicada a canais wireless, capacidade de canal, desvanecimento multipercurso, e técnicas de modulação. Utilizado para fundamentar as propriedades estatísticas do canal que viabilizam a PKG.

---

### proakis_digital (2008)
**Título:** Digital Communications (5ª edição)  
**Autores:** Proakis, John G.; Salehi, Masoud  
**Editora:** McGraw-Hill

**Sobre o que trata:**  
Referência clássica sobre comunicações digitais. Aborda modulação digital (BPSK, QPSK), códigos corretores de erro (incluindo códigos BCH), detecção de sinais, e análise de desempenho em canais com ruído. Utilizado para fundamentar as técnicas de modulação, reconciliação com códigos BCH, e análise de BER.

---

### bloch_wireless_security (2011)
**Título:** Physical-Layer Security: From Information Theory to Security Engineering  
**Autores:** Bloch, Matthieu; Barros, João  
**Editora:** Cambridge University Press

**Sobre o que trata:**  
Livro fundamental sobre segurança em camada física (Physical Layer Security - PLS). Aborda teoria da informação aplicada à segurança, conceitos de capacidade de sigilo, decorrelação espacial, quantização de observações do canal, e técnicas de amplificação de privacidade. Utilizado como referência principal para justificar a abordagem de PKG e explicar os fundamentos teóricos do sistema proposto.

---

## 📄 Artigos Científicos Clássicos

### diffie_hellman (1976)
**Título:** New Directions in Cryptography  
**Autores:** Diffie, Whitfield; Hellman, Martin  
**Periódico:** IEEE Transactions on Information Theory, vol. 22, n. 6, pp. 644-654

**Sobre o que trata:**  
Artigo seminal que introduziu a criptografia de chave pública (assimétrica) e o protocolo Diffie-Hellman para troca de chaves. Revolucionou a criptografia ao resolver o problema de distribuição de chaves sem canal seguro prévio. Utilizado para contextualizar os métodos convencionais de estabelecimento de chaves e suas limitações (alto custo computacional).

---

### wyner_wiretap (1975)
**Título:** The wire-tap channel  
**Autor:** Wyner, Aaron D.  
**Periódico:** Bell System Technical Journal, vol. 54, n. 8, pp. 1355-1387

**Sobre o que trata:**  
Artigo pioneiro que estabeleceu os fundamentos teóricos da segurança em camada física. Introduziu o conceito de "canal com interceptação" (wiretap channel) onde um invasor (Eve) tenta interceptar a comunicação entre transmissor e receptor legítimos. Estabeleceu o modelo Alice-Bob-Eve utilizado até hoje. Utilizado para fundamentar o modelo de segurança e o conceito de adversário passivo.

---

### maurer_secret_key (1993)
**Título:** Secret key agreement by public discussion based on common information  
**Autor:** Maurer, Ueli M.  
**Periódico:** IEEE Transactions on Information Theory, vol. 39, n. 3, pp. 733-742

**Sobre o que trata:**  
Artigo fundamental sobre geração de chaves secretas a partir de informação comum entre duas partes, permitindo discussão pública. Estabelece os fundamentos teóricos de reconciliação de informação e amplificação de privacidade. Utilizado para justificar o protocolo de reconciliação (code-offset) e explicar o vazamento de informação durante a reconciliação.

---

## 📊 Surveys e Artigos de Revisão

### zhang_pks_survey (2016)
**Título:** Key Generation From Wireless Channels: A Review  
**Autores:** Zhang, Junqing; Duong, Trung Q.; Marshall, Alan; Woods, Roger  
**Periódico:** IEEE Access, vol. 4, pp. 614-626

**Sobre o que trata:**  
Survey abrangente sobre geração de chaves a partir de canais wireless (PKG). Revisa técnicas de sondagem de canal, quantização, reconciliação, amplificação de privacidade, e métricas de desempenho. Compara diferentes abordagens e discute desafios práticos. Utilizado como referência principal para o estado da arte em PKG e para contextualizar a contribuição do trabalho.

---

### zhou_pls_survey (2013)
**Título:** Physical Layer Security in Wireless Communications: A Survey  
**Autores:** Zhou, Xiangyun; Song, Lingyang; Zhang, Yan  
**Periódico:** IEEE Communications Surveys & Tutorials, vol. 15, n. 1, pp. 1-14

**Sobre o que trata:**  
Survey sobre segurança em camada física (PLS) em comunicações wireless. Revisa técnicas de codificação para sigilo, beamforming seguro, cooperative jamming, e geração de chaves físicas. Discute aplicações em redes celulares e ad-hoc. Utilizado para contextualizar a PLS como alternativa aos métodos criptográficos tradicionais.

---

### zeng_pkg_challenges (2015)
**Título:** Physical Layer Key Generation in Wireless Networks: Challenges and Opportunities  
**Autores:** Zeng, Kai; Zhang, Yao; Gu, Rongxing  
**Periódico:** IEEE Communications Magazine, vol. 53, n. 6, pp. 33-39

**Sobre o que trata:**  
Artigo que discute desafios e oportunidades da geração de chaves em camada física. Aborda limitações práticas (correlação imperfeita, assimetria de hardware, mobilidade), requisitos de IoT e 5G/6G (baixo consumo energético, escalabilidade), e direções futuras. Utilizado para justificar a relevância do trabalho para cenários IoT e redes de próxima geração.

---

## 🔬 Artigos sobre Implementação

### mathur_pks (2008)
**Título:** Radio-telepathy: Extracting a Secret Key from an Unauthenticated Wireless Channel  
**Autores:** Mathur, Sandeep; Ye, Chih-Min; Reznik, Alex; Shah, Yinan; Trappe, Wade; Mandayam, Narayan  
**Periódico:** Proceedings of the 14th ACM International Conference on Mobile Computing and Networking, pp. 128-139

**Sobre o que trata:**  
Artigo seminal que demonstrou experimentalmente a viabilidade de extrair chaves secretas de canais wireless não autenticados. Implementou um sistema real de PKG usando dispositivos 802.11 e demonstrou que Alice e Bob conseguem gerar chaves idênticas explorando reciprocidade do canal. Trabalho pioneiro que inspirou muitas pesquisas subsequentes. Utilizado como referência principal para a abordagem prática de PKG.

---

### mosca_quantum (2018)
**Título:** Cybersecurity in an Era with Quantum Computers  
**Autor:** Mosca, Michele  
**Periódico:** IEEE Security & Privacy, vol. 16, n. 5, pp. 38-41

**Sobre o que trata:**  
Artigo sobre ameaças de computadores quânticos à criptografia atual. Explica como algoritmos quânticos (Shor, Grover) quebram criptografia assimétrica baseada em fatoração e logaritmo discreto (RSA, Diffie-Hellman). Discute necessidade de criptografia pós-quântica e alternativas como PKG. Utilizado para justificar a resiliência da PKG contra ataques quânticos.

---

## 📋 Documentos Técnicos (RFCs)

### rfc_tls (2008)
**Título:** The Transport Layer Security (TLS) Protocol Version 1.2  
**Autores:** Dierks, Tim; Rescorla, Eric  
**Tipo:** RFC 5246

**Sobre o que trata:**  
Especificação técnica do protocolo TLS 1.2, padrão de segurança na camada de transporte. Define handshake, estabelecimento de chaves usando criptografia assimétrica, e proteção de dados usando criptografia simétrica. Utilizado para exemplificar protocolos consolidados de comunicação segura que dependem de estabelecimento de chaves.

---

### rfc_ipsec (2005)
**Título:** Security Architecture for the Internet Protocol  
**Autores:** Kent, Stephen; Seo, Karen  
**Tipo:** RFC 4301

**Sobre o que trata:**  
Especificação da arquitetura de segurança IPsec, padrão de segurança na camada de rede. Define mecanismos de autenticação (AH), confidencialidade (ESP), e gerenciamento de chaves (IKE). Utilizado para exemplificar protocolos de comunicação segura na camada de rede que dependem de estabelecimento de chaves criptográficas.

---

## 📖 Resumo de Uso por Seção do Artigo

### Introdução
- **cirani_iot**: Contexto IoT e desafios de segurança
- **stallings_crypto**: Cinco pilares da segurança, algoritmos criptográficos
- **diffie_hellman**: Métodos convencionais de troca de chaves
- **mosca_quantum**: Vulnerabilidades quânticas
- **bloch_wireless_security, zhou_pls_survey**: PLS como alternativa
- **mathur_pks, zhang_pks_survey**: PKG e estado da arte
- **zeng_pkg_challenges**: Relevância para 5G/6G/IoT
- **proakis_digital**: Códigos corretores BCH

### Seção II (Fundamentação Teórica)
- **rfc_tls, rfc_ipsec**: Protocolos de comunicação segura
- **stallings_crypto**: Criptografia simétrica e assimétrica
- **diffie_hellman**: Problemas de distribuição de chaves
- **wyner_wiretap, bloch_wireless_security**: Modelo Alice-Bob-Eve
- **mathur_pks, zhang_pks_survey**: PKG e sondagem de canal
- **goldsmith_wireless, tse_viswanath**: Propriedades do canal wireless
- **proakis_digital**: Ruído AWGN, códigos de correção
- **maurer_secret_key**: Reconciliação e vazamento de informação

### Seção III (Implementação)
- **proakis_digital**: Modulação BPSK/QPSK, códigos BCH
- **matplotlib**: Geração de gráficos (referência implícita)

---

## 🔍 Classificação por Tema

### Fundamentos de Criptografia
- stallings_crypto
- diffie_hellman
- mosca_quantum

### Comunicações Sem Fio
- goldsmith_wireless
- tse_viswanath
- proakis_digital

### Segurança em Camada Física (PLS)
- wyner_wiretap
- bloch_wireless_security
- zhou_pls_survey

### Geração de Chaves Físicas (PKG)
- mathur_pks
- zhang_pks_survey
- maurer_secret_key
- zeng_pkg_challenges

### Aplicações e Contexto
- cirani_iot (IoT)
- rfc_tls, rfc_ipsec (Protocolos)
- mosca_quantum (Computação Quântica)

---

**Última atualização:** 18 de dezembro de 2025
