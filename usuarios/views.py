from django.shortcuts import render, redirect
from django.db import connection

# Página de Login
def login_view(request):
    error_message = None
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        senha = request.POST.get('senha')

        if usuario == 'admin' and senha == 'nimda':
            return redirect('home')  
        else:
            error_message = "Usuário ou senha incorretos!"

    return render(request, 'login.html', {'error_message': error_message})

# Página principal
def home_view(request):
    return render(request, 'home.html')

# Consulta ao banco de Dados para exibir as receitas cadastradas
def ficha_view(request):
    if request.method == 'POST':
        id_ficha = request.POST.get('id_ficha')

        with connection.cursor() as cursor:
            # Query 0 - Identificação da receita
            cursor.execute("""
                SELECT f.id_ficha_tecnica, f.nome_receita, f.descricao_receita, 
                       c.nome_categoria, f.numero_porcoes, f.peso_da_porcao
                FROM ficha_tecnica f
                JOIN categoria_receita c ON f.id_categoria = c.id_categoria
                WHERE f.id_ficha_tecnica = %s
            """, [id_ficha])
            dados_receita = dictfetchone(cursor)

            # Query 1 - Ingredientes
            cursor.execute("""
                SELECT i.descricao_ingrediente, lif.quantidade, um.abreviacao,
                       lif.custo_unitario, lif.custo_total_item
                FROM lista_ingredientes_ficha_tecnica lif
                JOIN ingredientes i ON lif.id_ingrediente = i.id_ingrediente
                JOIN unidades_medida um ON lif.id_unidade = um.id_unidade
                WHERE lif.id_ficha_tecnica = %s
            """, [id_ficha])
            ingredientes = dictfetchall(cursor)

            # Query 2 - Custo Total
            cursor.execute("""
                SELECT SUM(custo_total_item) AS custo_total
                FROM lista_ingredientes_ficha_tecnica
                WHERE id_ficha_tecnica = %s
            """, [id_ficha])
            custo_total_dict = dictfetchone(cursor)
            custo_total = custo_total_dict['custo_total'] if custo_total_dict else 0

            # Query 4 - Equipamentos
            cursor.execute("""
                SELECT e.descricao, lef.quantidade
                FROM lista_equipamentos_ficha_tecnica lef
                JOIN equipamentos e ON lef.id_equipamento = e.id_equipamento
                WHERE lef.id_ficha_tecnica = %s
            """, [id_ficha])
            equipamentos = dictfetchall(cursor)

            # Query 5 - Modo de preparo
            cursor.execute("""
                SELECT sequencia, texto_passo, tempo_minutos
                FROM modo_preparo_passos
                WHERE id_ficha_tecnica = %s
                ORDER BY sequencia
            """, [id_ficha])
            modo_preparo = dictfetchall(cursor)

        # Calcula o preço de custo por porção (evitando divisão por zero)
        numero_porcoes = dados_receita.get('numero_porcoes') if dados_receita else 0
        preco_custo_por_porcao = 0
        if numero_porcoes and custo_total:
            preco_custo_por_porcao = custo_total / numero_porcoes

        contexto = {
            'dados_receita': dados_receita,
            'ingredientes': ingredientes,
            'custo_total': custo_total,
            'preco_custo_por_porcao': preco_custo_por_porcao,
            'equipamentos': equipamentos,
            'modo_preparo': modo_preparo
        }

        return render(request, 'ficha.html', contexto)

    return redirect('home')  # segurança

def dictfetchall(cursor):
    "Retorna todos os resultados como lista de dicionários"
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def dictfetchone(cursor):
    "Retorna um único resultado como dicionário"
    row = cursor.fetchone()
    if row is None:
        return None
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))
