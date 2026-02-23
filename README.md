
# 🖐️ Hand Control PC

Controle o mouse do computador utilizando gestos da mão através da webcam.

Este projeto utiliza **Visão Computacional em tempo real** para capturar landmarks da mão com MediaPipe e traduzir gestos em ações no sistema operacional.

> Projeto desenvolvido com foco educacional e demonstração prática de Interação Humano-Computador (HCI).

---

## 🎯 Funcionalidades

- 🖱️ Levantar apenas o dedo indicador → Move o mouse  
- 👊 Manter o punho fechado por 1 segundo → Fecha o programa  
- 🖐️ Rastreamento de até duas mãos  
- 🎯 Detecção baseada em geometria dos landmarks  

---

## 🧠 Conceitos Aplicados

Este projeto demonstra:

- Rastreamento de 21 landmarks da mão
- Cálculo de distância euclidiana entre pontos
- Classificação de gestos baseada em regras geométricas
- Arquitetura modular em Python
- Controle do sistema operacional via automação

---

## 🏗️ Arquitetura do Projeto

```

hand_control_pc/
│
├── requirements.txt
├── README.md
└── src/
├── main.py                # Loop principal e integração
├── hand_tracker.py        # Captura e processamento dos landmarks
├── gesture_recognizer.py  # Lógica de reconhecimento de gestos
└── gesture_actions.py     # Execução das ações no sistema

```

### 🔹 Responsabilidades

- **HandTracker** → Comunicação com MediaPipe  
- **GestureRecognizer** → Interpretação geométrica dos gestos  
- **GestureActions** → Execução das ações (mouse, encerramento)  
- **main.py** → Orquestração do sistema  

Essa separação facilita manutenção, escalabilidade e expansão futura.

---

## ⚙️ Tecnologias Utilizadas

- Python 3.11  
- OpenCV  
- MediaPipe  
- PyAutoGUI  

---

## 📐 Como o Reconhecimento Funciona

O MediaPipe retorna 21 landmarks com coordenadas normalizadas:

```

(x, y, z) ∈ [0, 1]

```

A lógica de reconhecimento utiliza:

### 1️⃣ Comparação de posição vertical

Para verificar se um dedo está levantado:

```

tip_y < base_y

```

### 2️⃣ Distância entre landmarks

Para verificar proximidade entre dedos:

```

dist = √((x1 - x2)² + (y1 - y2)²)

````

### 3️⃣ Hierarquia de decisão

Os gestos são avaliados em ordem para evitar conflitos:

1. Punho fechado  
2. Movimento do mouse  
3. Outros gestos  

---

## 🚀 Como Executar

### 1️⃣ Clone o repositório

```bash
git clone https://github.com/SEU_USUARIO/hand_control_pc.git
cd hand_control_pc
````

### 2️⃣ Instale as dependências

```bash
pip install -r requirements.txt
```

### 3️⃣ Execute o projeto

```bash
python src/main.py
```

---

## 🧩 Decisões de Engenharia

* Uso de coordenadas normalizadas para independência de resolução
* Threshold ajustável para calibração de distância
* Separação clara entre detecção, reconhecimento e ação
* Estrutura preparada para expansão de novos gestos

---

## 📈 Melhorias Futuras

* Suavização do movimento do mouse (filtro exponencial)
* Calibração dinâmica baseada no tamanho da mão
* Implementação futura com Machine Learning supervisionado
* Adição de clique por gesto de pinça
* Controle de scroll por gesto

---

## 🎓 Objetivo

Demonstrar aplicação prática de:

* Visão Computacional
* Interação Humano-Computador
* Estruturação modular em Python
* Desenvolvimento de sistemas em tempo real

---

## 📜 Licença

MIT License
