# 📄 Sistema de Recibos com QR Code (CRUD)

Sistema em Python com interface gráfica para cadastro de pagamentos, geração de recibos e QR Code, utilizando banco de dados SQLite.

---

## 📌 Descrição

Este projeto permite registrar pagamentos de forma simples, armazenando os dados em um banco SQLite e gerando automaticamente um recibo em formato `.txt` com um QR Code contendo as informações.

Além disso, o sistema possui operações completas de CRUD (Criar, Ler, Atualizar e Excluir registros), permitindo total controle sobre os dados cadastrados.

A interface gráfica foi desenvolvida com Tkinter, tornando o sistema fácil de usar.

---

## ⚙️ Funcionalidades

### 📥 Cadastro (CREATE)

* Inserir:

  * Descrição
  * Beneficiário
  * Data
  * Valor
* Salvamento automático no banco de dados

---

### 📋 Listagem (READ)

* Visualização de todos os registros cadastrados
* Exibição organizada dos dados

---

### ✏️ Atualização (UPDATE)

* Atualizar registros existentes pelo ID

---

### ❌ Exclusão (DELETE)

* Remover registros do banco pelo ID

---

### 🧾 Recibo + QR Code

* Geração de recibo em arquivo `.txt`
* Geração automática de QR Code
* Exibição do QR Code na tela

---

## 💻 Tecnologias utilizadas

* Python
* Tkinter (interface gráfica)
* SQLite (`sqlite3`)
* qrcode (geração de QR Code)
* Pillow (`PIL`) (manipulação de imagens)

---

## ▶️ Como executar

### 1. Instalar dependências

```bash
pip install qrcode[pil] pillow
```

---

### 2. Executar o sistema

```bash
python recibo.py
```

---

## 📂 Estrutura do projeto

* `recibo.py` → código principal do sistema
* `pagamentos.db` → banco de dados (criado automaticamente)
* `recibo_*.txt` → recibos gerados
* `qr_*.png` → QR Codes gerados

---

## 🖥 Interface

O sistema possui 3 abas:

### 🔹 Cadastro

* Inserção de dados
* Geração de recibo e QR Code

### 🔹 Registros

* Listagem de todos os dados cadastrados

### 🔹 Editar/Excluir

* Atualização de registros
* Exclusão de registros pelo ID

---

## 📌 Observações

* O banco de dados é criado automaticamente na primeira execução
* Os arquivos de recibo e QR Code são salvos na mesma pasta do projeto
* O ID é gerado automaticamente pelo sistema

---

## 🎯 Objetivo

Projeto desenvolvido para prática de:

* CRUD com banco de dados SQLite
* Interface gráfica com Tkinter
* Manipulação de arquivos
* Geração de QR Code
* Organização de sistemas completos em Python

---

## 🔮 Possíveis melhorias

* Exportar recibos em PDF
* Adicionar busca por nome ou data
* Melhorar layout da interface
* Validação automática de datas
* Filtros de registros

---

## 👨‍💻 Autor

Desenvolvido por **Hélio Castro** 🚀

---
