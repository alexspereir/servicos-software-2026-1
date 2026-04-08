# Detector de Objetos com YOLO

Este projeto é uma aplicação multicontainer desenvolvida utilizando **Docker, API REST e Gradio**, com o objetivo de detectar objetos em imagens usando um modelo de visão computacional YOLO pré-treinado.

---

## Arquitetura do Projeto

A aplicação é composta por dois containers:

- **Frontend (Gradio)**  
  Interface web onde o usuário envia imagens e visualiza os resultados.

- **Backend (Flask API)**  
  Responsável por processar as imagens utilizando o modelo YOLO e retornar os resultados.

---

## Funcionamento

1. O usuário envia uma imagem pela interface (Gradio).
2. O frontend envia a imagem para o backend via **requisição POST (API REST)**.
3. O backend:
   - recebe a imagem
   - aplica o modelo YOLO
   - desenha as caixas de detecção
   - conta os objetos detectados
4. O backend retorna:
   - a imagem processada
   - a contagem dos objetos detectados
5. O frontend exibe o resultado ao usuário.

---

## Funcionalidades

   - Upload de imagens
   - Detecção de objetos com YOLO
   - Contagem automática de objetos detectados
   - Ajuste do nível de confiança (**confidence threshold**) via slider
   - Retorno visual com caixas delimitadoras
   - Comunicação entre containers via API REST

---

## Estrutura do Projeto

```bash
servicos_software_p/
├── gradio-visao/   # Frontend (interface do usuário)
├── api-visao/      # Backend (API + YOLO)
└── compose.yaml    # Orquestração dos containers
```

---

## Como Executar
1. Clone o repositório
   - git clone https://github.com/alexspereir/servicos-software-2026-1.git
   - cd servicos-software-2026-1/servicos_software_p
2. Execute os containers
   - docker compose up --build
3. Acesse a aplicação
4. Abra no navegador:
   - http://localhost:7861

---

## Como Usar
1. Envie uma imagem
2. Ajuste o slider de confiança (confidence)
3. Aguarde o processamento

4. Veja:
a imagem com os objetos detectados
a contagem de cada objeto

5. Exemplo de Saída
   - Objetos detectados:
   - person: 10
   - car: 2
   - backpack: 3
   - traffic light: 1

---

## Tecnologias Utilizadas
   - Python
   - Flask
   - Gradio
   - YOLO (Ultralytics)
   - OpenCV
   - Docker
