import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import qrcode
from PIL import Image, ImageTk
import datetime

# ============================================================
# BANCO DE DADOS
# ============================================================

conexao = sqlite3.connect("pagamentos.db")
cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS titulos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descricao TEXT,
    beneficiario TEXT,
    data TEXT,
    valor REAL
)
""")
conexao.commit()

# ============================================================
# FUNÇÕES
# ============================================================

def limpar():
    entrada_descricao.delete(0, tk.END)
    entrada_beneficiario.delete(0, tk.END)
    entrada_data.delete(0, tk.END)
    entrada_valor.delete(0, tk.END)

def colocar_data():
    hoje = datetime.date.today().strftime("%Y-%m-%d")
    entrada_data.delete(0, tk.END)
    entrada_data.insert(0, hoje)

# CREATE
def cadastrar():
    try:
        descricao = entrada_descricao.get().strip()
        beneficiario = entrada_beneficiario.get().strip()
        data = entrada_data.get().strip()
        valor = float(entrada_valor.get().replace(",", ".").strip())

        if not descricao or not beneficiario or not data:
            raise ValueError("Preencha todos os campos obrigatórios.")

        cursor.execute("""
        INSERT INTO titulos (descricao, beneficiario, data, valor)
        VALUES (?, ?, ?, ?)
        """, (descricao, beneficiario, data, valor))
        conexao.commit()

        messagebox.showinfo("Cadastro realizado", "Registro salvo com sucesso!")
        limpar()

    except Exception as e:
        messagebox.showerror("Erro", str(e))

# READ
def listar():
    cursor.execute("SELECT * FROM titulos")
    dados = cursor.fetchall()

    texto_lista.delete("1.0", tk.END)

    if not dados:
        texto_lista.insert(tk.END, "Nenhum registro encontrado.")
        return

    for d in dados:
        texto_lista.insert(tk.END,
            f"ID: {d[0]}\n"
            f"Cliente: {d[2]}\n"
            f"Descrição: {d[1]}\n"
            f"Data: {d[3]}\n"
            f"Valor: R$ {d[4]:.2f}\n"
            f"{'-'*30}\n"
        )

# UPDATE
def atualizar():
    try:
        id_reg = entrada_id.get().strip()

        if not id_reg.isdigit():
            messagebox.showerror("Erro", "ID inválido.")
            return

        descricao = entrada_descricao_update.get().strip()
        beneficiario = entrada_beneficiario_update.get().strip()
        data = entrada_data_update.get().strip()

        if not descricao or not beneficiario or not data:
            raise ValueError("Preencha todos os campos.")

        valor = float(entrada_valor_update.get().replace(",", ".").strip())

        cursor.execute("""
        UPDATE titulos
        SET descricao=?, beneficiario=?, data=?, valor=?
        WHERE id=?
        """, (descricao, beneficiario, data, valor, id_reg))

        conexao.commit()
        messagebox.showinfo("Sucesso", "Registro atualizado!")

    except Exception as e:
        messagebox.showerror("Erro", str(e))

# DELETE
def excluir():
    id_reg = entrada_id.get().strip()

    if not id_reg.isdigit():
        messagebox.showerror("Erro", "ID inválido.")
        return

    cursor.execute("SELECT * FROM titulos WHERE id=?", (id_reg,))
    if not cursor.fetchone():
        messagebox.showerror("Erro", "ID não encontrado.")
        return

    cursor.execute("DELETE FROM titulos WHERE id=?", (id_reg,))
    conexao.commit()

    messagebox.showinfo("Sucesso", "Registro excluído!")

# RECIBO + QR
def gerar_recibo():
    try:
        descricao = entrada_descricao.get().strip()
        beneficiario = entrada_beneficiario.get().strip()
        data = entrada_data.get().strip()
        valor = float(entrada_valor.get().replace(",", ".").strip())

        if not descricao or not beneficiario or not data:
            raise ValueError("Preencha todos os campos.")

        recibo = f"""
==============================
       RECIBO DE PAGAMENTO
==============================

Recebemos de: {beneficiario}

Referente a: {descricao}

Valor pago: R$ {valor:.2f}

Data do pagamento: {data}

______________________________
Assinatura
"""

        nome_arquivo = f"recibo_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write(recibo)

        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(recibo)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        nome_qr = f"qr_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        img.save(nome_qr)

        img_qr = Image.open(nome_qr)
        img_qr = img_qr.resize((150, 150))

        img_tk = ImageTk.PhotoImage(img_qr)
        label_qr.config(image=img_tk)
        label_qr.image = img_tk

        texto_recibo.delete("1.0", tk.END)
        texto_recibo.insert(tk.END, recibo)

        messagebox.showinfo("Sucesso", "Recibo e QR Code gerados!")

    except Exception as e:
        messagebox.showerror("Erro", str(e))

# ============================================================
# TELA
# ============================================================

janela = tk.Tk()
janela.title("Controle de Recebimentos")
janela.geometry("520x550")
janela.configure(bg="#f4f4f4")

abas = ttk.Notebook(janela)
abas.pack(expand=True, fill="both")

# ===== ABA CADASTRO =====
aba1 = tk.Frame(abas, bg="#f4f4f4")
abas.add(aba1, text="Cadastro")

tk.Label(aba1, text="Descrição", bg="#f4f4f4").grid(row=0, column=0, padx=5, pady=5)
entrada_descricao = tk.Entry(aba1)
entrada_descricao.grid(row=0, column=1, padx=5, pady=5)

tk.Label(aba1, text="Beneficiário", bg="#f4f4f4").grid(row=1, column=0, padx=5, pady=5)
entrada_beneficiario = tk.Entry(aba1)
entrada_beneficiario.grid(row=1, column=1, padx=5, pady=5)

tk.Label(aba1, text="Data", bg="#f4f4f4").grid(row=2, column=0, padx=5, pady=5)
entrada_data = tk.Entry(aba1)
entrada_data.grid(row=2, column=1, padx=5, pady=5)

tk.Button(aba1, text="Hoje", command=colocar_data).grid(row=2, column=2, padx=5)

tk.Label(aba1, text="Valor (R$)", bg="#f4f4f4").grid(row=3, column=0, padx=5, pady=5)
entrada_valor = tk.Entry(aba1)
entrada_valor.grid(row=3, column=1, padx=5, pady=5)

tk.Button(aba1, text="Salvar cadastro", command=cadastrar).grid(row=4, column=0, columnspan=2, pady=10)
tk.Button(aba1, text="Gerar recibo com QR", command=gerar_recibo).grid(row=5, column=0, columnspan=2)

label_qr = tk.Label(aba1, bg="#f4f4f4")
label_qr.grid(row=6, column=0, columnspan=2, pady=10)

tk.Button(aba1, text="Limpar campos", command=limpar).grid(row=7, column=0, columnspan=2)

texto_recibo = tk.Text(aba1, height=8, width=45)
texto_recibo.grid(row=8, column=0, columnspan=3, pady=10)

# ===== ABA LISTA =====
aba2 = tk.Frame(abas, bg="#f4f4f4")
abas.add(aba2, text="Registros")

tk.Button(aba2, text="Atualizar lista", command=listar).pack(pady=10)

texto_lista = tk.Text(aba2, height=15, width=45)
texto_lista.pack()

# ===== ABA EDITAR / EXCLUIR =====
aba3 = tk.Frame(abas, bg="#f4f4f4")
abas.add(aba3, text="Editar/Excluir")

tk.Label(aba3, text="ID do registro", bg="#f4f4f4").pack(pady=5)
entrada_id = tk.Entry(aba3)
entrada_id.pack(pady=5)

tk.Label(aba3, text="Nova Descrição", bg="#f4f4f4").pack(pady=5)
entrada_descricao_update = tk.Entry(aba3)
entrada_descricao_update.pack(pady=5)

tk.Label(aba3, text="Novo Beneficiário", bg="#f4f4f4").pack(pady=5)
entrada_beneficiario_update = tk.Entry(aba3)
entrada_beneficiario_update.pack(pady=5)

tk.Label(aba3, text="Nova Data", bg="#f4f4f4").pack(pady=5)
entrada_data_update = tk.Entry(aba3)
entrada_data_update.pack(pady=5)

tk.Label(aba3, text="Novo Valor", bg="#f4f4f4").pack(pady=5)
entrada_valor_update = tk.Entry(aba3)
entrada_valor_update.pack(pady=5)

tk.Button(aba3, text="Atualizar", command=atualizar).pack(pady=5)
tk.Button(aba3, text="Excluir", command=excluir).pack(pady=5)

janela.mainloop()