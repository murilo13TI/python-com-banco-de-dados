from flask import Flask, render_template, request, flash, url_for, redirect
import fdb
from flask_bcrypt import bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdfghjhghfdxzfghjkjyjtrtersazxfgjhkjthrsdzxc'


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
    return render_template('editar.html', titulo='editar livro')

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

@app.route('/deletar/<int:id>', methods=('POST',))
def deletar(id):
    cursor = con.cursor()  # Abre o cursor

    try:
        cursor.execute('DELETE FROM livros WHERE id_livro = ?', (id,))
        con.commit()  # Salva as alterações no banco de dados
        flash('Livro excluído com sucesso!', 'success')  # Mensagem de sucesso
    except Exception as e:
        con.rollback()  # Reverte as alterações em caso de erro
        flash('Erro ao excluir o livro.', 'error')  # Mensagem de erro
    finally:
        cursor.close()  # Fecha o cursor independentemente do resultado

    return redirect(url_for('index'))  # Redireciona para a página principal

@app.route('/cadastro_usuario')
def cadastro_usuario():
    return render_template('cadastro_usuario.html')

@app.route('/usuario')
def usuario():
    cursor = con.cursor()
    cursor.execute('SELECT id_usuario, nome_usuario, email, senha from usuario')
    usuario = cursor.fetchall()
    cursor.close()

    return render_template('usuario.html', usuario=usuario)

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome_usuario = request.form['Nome']
    email = request.form['Email']
    senha = request.form['Senha']

    cursor = con.cursor()
    try:
        cursor.execute('SELECT 1 FROM usuario WHERE  email = ?', (email,))
        if cursor.fetchone():
            flash('Erro: usuario ja cadastrado', 'error')
            return redirect(url_for('cadastrar'))

        cursor.execute("INSERT INTO usuario (nome_usuario, email, senha) VALUES (?, ?, ?)",
                       (nome_usuario, email, senha))
        con.commit()

    finally:
    # Fechar o cursor manualmente, mesmo que haja erro
        cursor.close()

    flash("Livro cadastrado com sucesso!", "success")
    return redirect(url_for('index'))


@app.route('/editar_usuario/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    cursor = con.cursor()

    cursor.execute('SELECT 1 FROM usuario WHERE id_usuario = ?', (id,))
    usuario = cursor.fetchone()

    if not usuario:
        cursor.close()
        flash('usuário não encontrado', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        nome_usuario = request.form['Nome']
        email = request.form['Email']
        senha = request.form['Senha']

        cursor.execute('UPDATE usuario SET nome_usuario = ? , email = ?, senha = ?', (nome_usuario, email, senha,))
        con.commit()
        flash("usuario atualizado com sucesso!", "success")
        return redirect(url_for('index'))

@app.route('/deletar_usuario/<int:id>', methods=['POST'])
def deletar_usuario(id):
    cursor = con.cursor()

    try:
        cursor.execute("DELETE FROM USUARIO WHERE id_usuario = ?" , (id,))
        con.commit()
        flash("o usuario foi deletado com sucesso! ",  'sucess')
    except Exception as e:
        con.rollback()
        flash("erro ao excluir usuario", 'error')
    finally:
        cursor.close()

    return redirect(url_for('index'))

@app.route('/login/<int:id>', methods=['POST'])
def login():
    cursor = con.cursor()

    senha_cripto = bcrypt.generate_password_hash(senha).decode('utf-8')
    if bcrypt.check_password_hash(senha_hash, senha)
        flash('login executado com sucesso', 'sucess')
    else:
        flash('erro login não executado', 'error')




if __name__ == '__main__':
    app.run(debug=True)