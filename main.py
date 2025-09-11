from flask import Flask, render_template, request, flash, url_for, redirect
import fdb

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a'


host = 'localhost'
database = r'C:\Users\Aluno\Downloads\livros\BANCO.FDB'
user = 'sysdba'
password = 'sysdba'

con = fdb.connect(host=host, database=database, user=user, password=password)

@app.route('/')
def index():
    cursor = con.cursor()
    cursor.execute('SELECT id_livro, livro_nome , autor, ano_publicado FROM LIVROS')
    livros = cursor.fetchall()
    cursor.close()

    return render_template('livros.html', livros=livros)


@app.route('/novo')
def novo():
        return render_template('novo.html', titulo='Novo Livro')

@app.route('/criar', methods=['POST'])
def criar():
    titulo = request.form['titulo']
    autor = request.form['autor']
    ano_publicacao = request.form['ano_publicacao']

    # Criando o cursor
    cursor = con.cursor()

    try:
        # Verificar se o livro já existe
        cursor.execute("SELECT 1 FROM livros WHERE livro_nome = ?", (titulo,))
        if cursor.fetchone():  # Se existir algum registro
            flash("Erro: Livro já cadastrado.", "error")
            return redirect(url_for('novo'))

        # Inserir o novo livro (sem capturar o ID)
        cursor.execute("INSERT INTO livros (livro_nome, AUTOR, ANO_PUBLICADO) VALUES (?, ?, ?)",
                       (titulo, autor, ano_publicacao))
        con.commit()
    finally:
        # Fechar o cursor manualmente, mesmo que haja erro
        cursor.close()

    flash("Livro cadastrado com sucesso!", "success")
    return redirect(url_for('index'))

@app.route('/atualizar')
def atualizar():
    return render_template('editar.html', livro_nome='editar livro')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    cursor = con.cursor()  # Abre o cursor

    # Buscar o livro específico para edição
    cursor.execute("SELECT ID_LIVRO, livro_nome, AUTOR, ANO_PUBLICADO FROM livros WHERE ID_LIVRO = ?", (id,))
    livro = cursor.fetchone()

    if not livro:
        cursor.close()  # Fecha o cursor se o livro não for encontrado
        flash("Livro não encontrado!", "error")
        return redirect(url_for('index'))  # Redireciona para a página principal se o livro não for encontrado

    if request.method == 'POST':
        # Coleta os dados do formulário
        titulo = request.form['titulo']
        autor = request.form['autor']
        ano_publicacao = request.form['ano_publicacao']

        # Atualiza o livro no banco de dados
        cursor.execute("UPDATE livros SET livro_nome = ?, AUTOR = ?, ANO_PUBLICADO = ? WHERE ID_LIVRO = ?",
                       (titulo, autor, ano_publicacao, id))
        con.commit()  # Salva as mudanças no banco de dados
        cursor.close()  # Fecha o cursor
        flash("Livro atualizado com sucesso!", "success")
        return redirect(url_for('index'))  # Redireciona para a página principal após a atualização

    cursor.close()  # Fecha o cursor ao final da função, se não for uma requisição POST
    return render_template('editar.html', livro=livro, titulo='Editar Livro')  # Renderiza a página de edição

if __name__ == '__main__':
    app.run(debug=True)