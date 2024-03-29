from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm, PasswordResetForm
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Count
from .forms import (
    ArteForm,
    IdeiaForm,
    AutorForm,
    LivroForm,
    LoginForm,
    ProfileForm,
    EditoraForm,
    MensagemForm,
    PensamentoForm,
    LivroFormSemAutor,
    MensagemUsersForm,
    ComentarioLivroForm,
    ComentarioLivrosForm,
    PensamentoAutoresForm,
    CustomUserCreationForm,
)
from .models import (
    Arte,
    Ideia,
    Autor,
    Livro,
    Profile,
    Editora,
    Mensagem,
    Categoria,
    Pensamento,
    ComentarioLivro,
    MensagemEnviada,
)

def index(request):
    return render(request, 'index.html')

def registrar(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Conta criada para {username}! Você pode fazer login agora.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registro.html', {'form': form})

def fazer_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Autenticado com sucesso!')
                return redirect('index')  
            else:
                form.add_error(None, 'Credenciais inválidas. Por favor, tente novamente.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def painel_controle(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    comentarios = ComentarioLivro.objects.filter(usuario=profile.user)
    pensamentos = Pensamento.objects.filter(usuario=profile.user)
    autores = Autor.objects.filter(usuario=profile.user)
    editoras = Editora.objects.filter(usuario=profile.user)
    artes = Arte.objects.filter(usuario=profile.user)
    livros = Livro.objects.filter(usuario=profile.user)
    ideias = Ideia.objects.filter(usuario=profile.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('painel_controle')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'painel_controle.html', 
        {
            'form': form, 
            'profile': profile, 
            'comentarios': comentarios,
            'pensamentos': pensamentos,
            'autores': autores,
            'editoras': editoras,
            'total_autores': len(autores),
            'total_editoras': len(editoras),
            'total_artes': len(artes),
            'total_livros': len(livros),
            'total_comentarios': len(comentarios),
            'total_pensamentos': len(pensamentos),
            'total_ideias': len(ideias)
        }
    )

def alterar_senha(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Sua senha foi alterada com sucesso!')
            return redirect('index')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'alterar_senha.html', {
        'form': form
    })

def redefinir_senha(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(request=request)
            messages.success(request, 'Um email com instruções para redefinir sua senha foi enviado.')
            return redirect('login')
    else:
        form = PasswordResetForm()
    return render(request, 'redefinir_senha.html', {'form': form})

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'recuperar_senha.html'

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'recuperar_senha_concluido.html'

@login_required
def detalhes_usuario(request, user_id):
    usuario = get_object_or_404(User, pk=user_id)
    profile = Profile.objects.get(user=usuario)
    comentarios = ComentarioLivro.objects.filter(usuario=profile.user)
    pensamentos = Pensamento.objects.filter(usuario=profile.user)
    autores = Autor.objects.filter(usuario=profile.user)
    editoras = Editora.objects.filter(usuario=profile.user)
    return render(request, 'detalhes_usuario.html', 
        {
            'usuario': usuario, 
            'profile': profile, 
            'comentarios': comentarios,
            'pensamentos': pensamentos,
            'autores': autores,
            'editoras': editoras
        }
    )

@login_required
def enviar_mensagem(request, id_destinatario):
    destinatario = get_object_or_404(User, pk=id_destinatario)
    if request.method == 'POST':
        form = MensagemForm(request.POST)
        if form.is_valid():
            mensagem = form.save(commit=False)
            mensagem.remetente = request.user
            mensagem.destinatario = destinatario
            mensagem.save()

            mensagem_enviada = MensagemEnviada.objects.create(
                remetente=request.user,
                destinatario=destinatario,
                assunto=mensagem.assunto,
                corpo=mensagem.corpo
            )
            messages.success(request, f'Mensagem enviada com sucesso para {destinatario}!')
            return redirect('caixa_saida')
    else:
        form = MensagemForm()
    return render(request, 'enviar_mensagem.html', {'form': form, 'destinatario': destinatario})

@login_required
def enviar_mensagem_usuarios(request):
    if request.method == 'POST':
        form = MensagemUsersForm(request.POST, user=request.user)
        if form.is_valid():
            destinatario = form.cleaned_data['destinatario']
            destinatario = get_object_or_404(User, pk=destinatario.id)
            mensagem = form.save(commit=False)
            mensagem.remetente = request.user
            mensagem.destinatario = destinatario
            mensagem.save()

            mensagem_enviada = MensagemEnviada.objects.create(
                remetente=request.user,
                destinatario=destinatario,
                assunto=mensagem.assunto,
                corpo=mensagem.corpo
            )
            messages.success(request, f'Mensagem enviada com sucesso para {destinatario}!')
            return redirect('caixa_saida')
    else:
        form = MensagemUsersForm(user=request.user)
    return render(request, 'enviar_mensagem_usuarios.html', {'form': form})

@login_required
def excluir_mensagem(request, mensagem_id):
    mensagem = get_object_or_404(Mensagem, pk=mensagem_id)
    if request.user == mensagem.destinatario:
        mensagem.delete()
        messages.success(request, 'Mensagem removida com sucesso.')
    else:
        messages.error(request, 'Você não tem permissão para excluir esta mensagem.')
    return redirect('caixa_entrada')

@login_required
def excluir_mensagem_saida(request, mensagem_id):
    mensagem = get_object_or_404(MensagemEnviada, pk=mensagem_id)
    if request.user == mensagem.remetente:
        mensagem.delete()
        messages.success(request, 'Mensagem removida com sucesso.')
    else:
        messages.error(request, 'Você não tem permissão para excluir esta mensagem.')
    return redirect('caixa_saida')

@login_required
def caixa_entrada(request):
    mensagens_recebidas = Mensagem.objects.filter(destinatario=request.user).order_by('-timestamp')
    paginator = Paginator(mensagens_recebidas, 5)

    page = request.GET.get('page')
    try:
        mensagens_pagina = paginator.page(page)
    except PageNotAnInteger:
        mensagens_pagina = paginator.page(1)
    except EmptyPage:
        mensagens_pagina = paginator.page(paginator.num_pages)

    return render(request, 'caixa_entrada.html', 
        {
            'mensagens': mensagens_pagina, 
            'mensagens_recebidas': mensagens_recebidas
        }
    )

@login_required
def caixa_saida(request):
    mensagens_enviadas = MensagemEnviada.objects.filter(remetente=request.user).order_by('-timestamp')
    paginator = Paginator(mensagens_enviadas, 5) 

    page = request.GET.get('page')
    try:
        mensagens_pagina = paginator.page(page)
    except PageNotAnInteger:
        mensagens_pagina = paginator.page(1)
    except EmptyPage:
        mensagens_pagina = paginator.page(paginator.num_pages)

    return render(request, 'caixa_saida.html', 
        {
            'mensagens': mensagens_pagina, 
            'mensagens_enviadas': mensagens_enviadas
        }
    )

@login_required
def buscar_usuarios(request):
    query = request.GET.get('query', '')
    usuarios = User.objects.filter(username__icontains=query)[:10]  # Limita a 10 resultados
    usuarios_data = [{'username': usuario.username, 'id': usuario.id} for usuario in usuarios]

    return JsonResponse({'usuarios': usuarios_data})

@login_required
def fazer_logout(request):
    logout(request)
    messages.success(request, 'Desconectado com sucesso!')
    return redirect('index')

@login_required
def autores(request):
    autores_list = Autor.objects.all().order_by('nome')
    
    query = request.GET.get('q')
    if query:
        autores_list = autores_list.filter(nome__icontains=query)

    autores_por_pagina = 5
    
    paginator = Paginator(autores_list, autores_por_pagina)
    page = request.GET.get('page')
    try:
        autores = paginator.page(page)
    except PageNotAnInteger:
        autores = paginator.page(1)
    except EmptyPage:
        autores = paginator.page(paginator.num_pages)
    
    return render(request, 'autores.html', {'autores': autores, 'query': query, 'total': len(autores_list)})

@login_required
def buscar_autores(request):
    query = request.GET.get('query', '')
    autores = Autor.objects.filter(nome__icontains=query)[:10] # Limita a 10 resultados
    autores_data = [{'nome': autor.nome, 'id': autor.id} for autor in autores]

    return JsonResponse({'autores': autores_data})

@login_required
def detalhes_autor(request, autor_id):
    autor = get_object_or_404(Autor, pk=autor_id)
    pensamentos = Pensamento.objects.filter(autor=autor).order_by('-data_criacao')

    pensamentos_por_pagina = 5

    paginator = Paginator(pensamentos, pensamentos_por_pagina)
    page = request.GET.get('page')

    livros_por_pagina = 5
    livros = Livro.objects.filter(autor=autor).order_by('titulo')
    
    paginator_livros = Paginator(livros, livros_por_pagina)
    page_livros = request.GET.get('page_livros')

    if request.method == 'POST':
        form = PensamentoForm(request.POST)
        if form.is_valid():
            pensamento = form.save(commit=False)
            pensamento.autor = autor
            pensamento.usuario = request.user
            pensamento.save()
            messages.success(request, 'Pensamento adicionado com sucesso!')
            return redirect('detalhes_autor', autor_id=autor_id)
    else:
        form = PensamentoForm()

    try:
        pensamentos_pagina = paginator.page(page)
    except PageNotAnInteger:
        pensamentos_pagina = paginator.page(1)
    except EmptyPage:
        pensamentos_pagina = paginator.page(paginator.num_pages)

    try:
        livros_pagina = paginator_livros.page(page_livros)
    except PageNotAnInteger:
        livros_pagina = paginator_livros.page(1)
    except EmptyPage:
        livros_pagina = paginator_livros.page(paginator_livros.num_pages)

    return render(request, 'detalhes_autor.html', 
        {
            'autor': autor, 
            'pensamentos_pagina': pensamentos_pagina,
            'livros_pagina': livros_pagina,
            'form': form,
            'total_pensamentos': len(pensamentos),
            'total_livros': len(livros)
        }
    )

@login_required
def adicionar_autor(request):
    if request.method == 'POST':
        form = AutorForm(request.POST, request.FILES)
        if form.is_valid():
            autor = form.save(commit=False)  # Salvando o autor sem commit
            autor.usuario = request.user
            autor.save()  # Salvando o autor no banco de dados
            messages.success(request, f'Autor "{autor.nome}" adicionado com sucesso!')
            return redirect('detalhes_autor', autor_id=autor.id)
    else:
        form = AutorForm()
    return render(request, 'adicionar_autor.html', {'form': form})

@login_required
def editar_autor(request, autor_id):
    autor = get_object_or_404(Autor, pk=autor_id)
    if request.user != autor.usuario:
        messages.error(request, 'Você não tem permissão para editar este autor.')
        return redirect('autores')
    if request.method == 'POST':
        form = AutorForm(request.POST, request.FILES, instance=autor)
        if form.is_valid():
            autor = form.save(commit=False)  # Salvando o autor sem commit
            autor.save()  # Salvando o autor no banco de dados
            messages.success(request, f'Autor {autor.nome} alterado com sucesso!')
            return redirect('detalhes_autor', autor_id=autor_id)
    else:
        form = AutorForm(instance=autor)
    return render(request, 'editar_autor.html', {'form': form, 'autor': autor})

@login_required
def excluir_autor(request, autor_id):
    autor = get_object_or_404(Autor, pk=autor_id)
    if request.user != autor.usuario:
        messages.error(request, 'Você não tem permissão para excluir este autor.')
        return redirect('autores')
    autor.delete()
    messages.success(request, f'O autor "{autor.nome}" foi excluído com sucesso.')
    return redirect('autores')

@login_required
def adicionar_pensamento(request):
    if request.method == 'POST':
        form = PensamentoAutoresForm(request.POST)
        if form.is_valid():
            pensamento = form.save(commit=False)
            pensamento.usuario = request.user
            pensamento.save()
            autor_id = form.cleaned_data['autor'].id
            messages.error(request, f'Pensamento adicionado com sucesso.')
            return redirect('detalhes_autor', autor_id=autor_id)
    else:
        form = PensamentoAutoresForm()
    return render(request, 'adicionar_pensamento.html', {'form': form})

@login_required
def editar_pensamento(request, pensamento_id, autor_id):
    pensamento = get_object_or_404(Pensamento, pk=pensamento_id)
    if request.user != pensamento.usuario:
        messages.error(request, 'Você não tem permissão para editar este pensamento.')
        return redirect('detalhes_autor', autor_id=autor_id)
    if request.method == 'POST':
        form = PensamentoForm(request.POST, request.FILES, instance=pensamento)
        if form.is_valid():
            form.save()
            messages.success(request, f'Pensamento de id {pensamento_id} alterado com sucesso!')
            return redirect('detalhes_autor', autor_id=autor_id)
    else:
        form = PensamentoForm(instance=pensamento)
    return render(request, 'editar_pensamento.html', {'form': form, 'pensamento': pensamento, 'autor_id': autor_id})

@login_required
def excluir_pensamento(request, pensamento_id, autor_id):
    pensamento = get_object_or_404(Pensamento, pk=pensamento_id)
    if request.user != pensamento.usuario:
        messages.error(request, 'Você não tem permissão para excluir este pensamento.')
        return redirect('detalhes_autor', autor_id=autor_id)
    pensamento.delete()
    messages.success(request, f'O pensamento de id {pensamento_id} foi excluído.')
    return redirect('detalhes_autor', autor_id=autor_id)

@login_required
def livros(request):
    livros_list = Livro.objects.all().order_by('titulo')
    
    query = request.GET.get('q')
    if query:
        livros_list = livros_list.filter(titulo__icontains=query)

    livros_por_pagina = 5
    
    paginator = Paginator(livros_list, livros_por_pagina)
    page = request.GET.get('page')
    try:
        livros = paginator.page(page)
    except PageNotAnInteger:
        livros = paginator.page(1)
    except EmptyPage:
        livros = paginator.page(paginator.num_pages)
    
    return render(request, 'livros.html', {'livros': livros, 'query': query, 'total': len(livros_list)})

@login_required
def livros_por_editora(request, editora_id):
    livros_list = Livro.objects.filter(editora_id=editora_id).order_by('titulo')
    editora = get_object_or_404(Editora, pk=editora_id)

    livros_por_pagina = 5
    
    paginator = Paginator(livros_list, livros_por_pagina)
    page = request.GET.get('page')
    try:
        livros = paginator.page(page)
    except PageNotAnInteger:
        livros = paginator.page(1)
    except EmptyPage:
        livros = paginator.page(paginator.num_pages)
    
    return render(request, 'livros_por_editora.html', 
        {
            'livros': livros, 
            'total': len(livros_list),
            'editora': editora
        }
    )

@login_required
def livros_por_autor(request, autor_id):
    livros_list = Livro.objects.filter(autor_id=autor_id).order_by('titulo')
    autor = get_object_or_404(Autor, pk=autor_id)

    livros_por_pagina = 5
    
    paginator = Paginator(livros_list, livros_por_pagina)
    page = request.GET.get('page')
    try:
        livros = paginator.page(page)
    except PageNotAnInteger:
        livros = paginator.page(1)
    except EmptyPage:
        livros = paginator.page(paginator.num_pages)
    
    return render(request, 'livros_por_autor.html', 
        {
            'livros': livros, 
            'total': len(livros_list),
            'autor': autor
        }
    )

@login_required
def livros_por_categoria(request, categoria_id):
    livros_list = Livro.objects.filter(categoria_id=categoria_id).order_by('titulo')
    categoria = get_object_or_404(Categoria, pk=categoria_id)

    livros_por_pagina = 5
    
    paginator = Paginator(livros_list, livros_por_pagina)
    page = request.GET.get('page')
    try:
        livros = paginator.page(page)
    except PageNotAnInteger:
        livros = paginator.page(1)
    except EmptyPage:
        livros = paginator.page(paginator.num_pages)
    
    return render(request, 'livros_por_categoria.html', 
        {
            'livros': livros, 
            'total': len(livros_list),
            'categoria': categoria
        }
    )

@login_required
def buscar_livros(request):
    query = request.GET.get('query', '')
    livros = Livro.objects.filter(titulo__icontains=query)[:10] # Limita a 10 resultados
    livros_data = [{'titulo': livro.titulo, 'id': livro.id} for livro in livros]

    return JsonResponse({'livros': livros_data})

@login_required
def detalhes_livro(request, livro_id):
    livro = get_object_or_404(Livro, pk=livro_id)
    comentarios = livro.comentarios.all().order_by('-data_publicacao')

    comentarios_por_pagina = 5

    paginator = Paginator(comentarios, comentarios_por_pagina)
    page = request.GET.get('page')

    if request.method == 'POST':
        form = ComentarioLivroForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.livro = livro
            comentario.usuario = request.user
            comentario.save()
            messages.success(request, 'Comentário adicionado com sucesso!')
            return redirect('detalhes_livro', livro_id=livro_id)
    else:
        form = ComentarioLivroForm()

    try:
        comentarios_pagina = paginator.page(page)
    except PageNotAnInteger:
        comentarios_pagina = paginator.page(1)
    except EmptyPage:
        comentarios_pagina = paginator.page(paginator.num_pages)

    return render(request, 'detalhes_livro.html', 
        {
            'livro': livro, 
            'comentarios_pagina': comentarios_pagina, 
            'form': form,
            'total_comentarios': len(comentarios)
        }
    )

@login_required
def adicionar_livro(request):
    if request.method == 'POST':
        form = LivroForm(request.POST, request.FILES)
        if form.is_valid():
            livro = form.save(commit=False)
            livro.usuario = request.user
            livro.save()  
            messages.success(request, f'Livro "{livro.titulo}" adicionado com sucesso!')
            return redirect('livros')
    else:
        form = LivroForm()
    return render(request, 'adicionar_livro.html', {'form': form})

@login_required
def adicionar_livro_autor(request, autor_id):
    autor = get_object_or_404(Autor, pk=autor_id)
    if request.method == 'POST':
        form = LivroFormSemAutor(request.POST, request.FILES)
        if form.is_valid():
            livro = form.save(commit=False)
            livro.autor_id = autor_id  # Associando o autor especificado
            livro.usuario = request.user
            livro.save()
            messages.success(request, f'Livro "{livro.titulo}" adicionado para {autor.nome}!')
            return redirect('detalhes_autor', autor_id=autor_id)  # Redirecione para onde for apropriado
    else:
        form = LivroFormSemAutor()
    return render(request, 'adicionar_livro_autor.html', {'form': form, 'autor': autor})

@login_required
def editar_livro(request, livro_id):
    livro = get_object_or_404(Livro, pk=livro_id)
    if request.user != livro.usuario:
        messages.error(request, 'Você não tem permissão para editar este livro.')
        return redirect('livros')
    if request.method == 'POST':
        form = LivroForm(request.POST, request.FILES, instance=livro)
        if form.is_valid():
            livro = form.save(commit=False)
            livro.save()
            messages.success(request, f'Livro "{livro.titulo}" alterado com sucesso!')
            return redirect('livros')
    else:
        form = LivroForm(instance=livro)
    return render(request, 'editar_livro.html', {'form': form, 'livro': livro})

@login_required
def excluir_livro(request, livro_id):
    livro = get_object_or_404(Livro, pk=livro_id)
    if request.user != livro.usuario:
        messages.error(request, 'Você não tem permissão para excluir este livro.')
        return redirect('livros')
    livro.delete()
    messages.success(request, f'O livro "{livro.titulo}" foi excluído com sucesso.')
    return redirect('livros')

@login_required
def adicionar_comentario_livro(request):
    if request.method == 'POST':
        form = ComentarioLivrosForm(request.POST, user=request.user)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.usuario = request.user
            comentario.save()
            return redirect('detalhes_livro', livro_id=comentario.livro.id)
    else:
        form = ComentarioLivrosForm(user=request.user)
    return render(request, 'adicionar_comentario_livro.html', {'form': form})

@login_required
def editar_comentario(request, comentario_id, livro_id):
    comentario = get_object_or_404(ComentarioLivro, pk=comentario_id)
    if request.user != comentario.usuario:
        messages.error(request, 'Você não tem permissão para editar este comentário.')
        return redirect('detalhes_livro', livro_id=livro_id)
    if request.method == 'POST':
        form = ComentarioLivroForm(request.POST, instance=comentario)
        if form.is_valid():
            form.save()
            messages.success(request, f'Comentário de id {comentario_id} alterado com sucesso!')
            return redirect('detalhes_livro', livro_id=livro_id)
    else:
        form = ComentarioLivroForm(instance=comentario)
    return render(request, 'editar_comentario.html', {'form': form, 'comentario': comentario, 'livro_id': livro_id})

@login_required
def excluir_comentario(request, comentario_id, livro_id):
    comentario = get_object_or_404(ComentarioLivro, pk=comentario_id)
    if request.user != comentario.usuario:
        messages.error(request, 'Você não tem permissão para excluir este comentário.')
        return redirect('detalhes_livro', livro_id=livro_id)
    comentario.delete()
    messages.success(request, f'O comentário de id {comentario_id} foi excluído.')
    return redirect('detalhes_livro', livro_id=livro_id)

@login_required
def editoras(request):
    editoras_list = Editora.objects.all().order_by('nome')
    
    query = request.GET.get('q')
    if query:
        editoras_list = editoras_list.filter(nome__icontains=query)

    editoras_por_pagina = 5
    
    paginator = Paginator(editoras_list, editoras_por_pagina)
    page = request.GET.get('page')
    try:
        editoras = paginator.page(page)
    except PageNotAnInteger:
        editoras = paginator.page(1)
    except EmptyPage:
        editoras = paginator.page(paginator.num_pages)
    
    return render(request, 'editoras.html', {'editoras': editoras, 'query': query, 'total': len(editoras_list)})

@login_required
def buscar_editoras(request):
    query = request.GET.get('query', '')
    editoras = Editora.objects.filter(nome__icontains=query)[:10] # Limita a 10 resultados
    editoras_data = [{'nome': editora.nome, 'id': editora.id} for editora in editoras]

    return JsonResponse({'editoras': editoras_data})

@login_required
def adicionar_editora(request):
    if request.method == 'POST':
        form = EditoraForm(request.POST)
        if form.is_valid():
            editora = form.save(commit=False)
            editora.usuario = request.user
            editora.save()
            messages.success(request, f'Editora "{editora.nome}" adicionada com sucesso!')
            return redirect('editoras')
    else:
        form = EditoraForm()
    return render(request, 'adicionar_editora.html', {'form': form})

@login_required
def editar_editora(request, editora_id):
    editora = get_object_or_404(Editora, pk=editora_id)
    if request.user != editora.usuario:
        messages.error(request, 'Você não tem permissão para excluir esta editora.')
        return redirect('editoras')
    if request.method == 'POST':
        form = EditoraForm(request.POST, instance=editora)
        if form.is_valid():
            form.save()
            messages.success(request, f'Editora {editora.nome} alterada com sucesso!')
            return redirect('editoras')
    else:
        form = EditoraForm(instance=editora)
    return render(request, 'editar_editora.html', {'form': form, 'editora': editora})

@login_required
def excluir_editora(request, editora_id):
    editora = get_object_or_404(Editora, pk=editora_id)
    if request.user != editora.usuario:
        messages.error(request, 'Você não tem permissão para excluir esta editora.')
        return redirect('editoras')
    editora_nome = editora.nome 
    editora.delete()
    messages.success(request, f'A editora "{editora_nome}" foi excluída com sucesso.')
    return redirect('editoras')

@login_required
def artes(request):
    artes_list = Arte.objects.all().order_by('titulo')
    
    query = request.GET.get('q')
    if query:
        artes_list = artes_list.filter(titulo__icontains=query)

    artes_por_pagina = 5
    
    paginator = Paginator(artes_list, artes_por_pagina)
    page = request.GET.get('page')
    try:
        artes = paginator.page(page)
    except PageNotAnInteger:
        artes = paginator.page(1)
    except EmptyPage:
        artes = paginator.page(paginator.num_pages)
    
    return render(request, 'artes.html', {'artes': artes, 'query': query, 'total': len(artes_list)})

@login_required
def buscar_artes(request):
    query = request.GET.get('query', '')
    artes = Arte.objects.filter(titulo__icontains=query)[:10] # Limita a 10 resultados
    artes_data = [{'titulo': arte.titulo} for arte in artes]

    return JsonResponse({'artes': artes_data})

@login_required
def adicionar_arte(request):
    if request.method == 'POST':
        form = ArteForm(request.POST, request.FILES)
        if form.is_valid():
            arte = form.save(commit=False)
            arte.usuario = request.user
            arte.save()
            messages.success(request, f'Arte "{arte.titulo}" adicionada com sucesso!')
            return redirect('artes')
    else:
        form = ArteForm()
    return render(request, 'adicionar_arte.html', {'form': form})

@login_required
def editar_arte(request, arte_id):
    arte = get_object_or_404(Arte, pk=arte_id)
    if request.user != arte.usuario:
        messages.error(request, 'Você não tem permissão para excluir esta arte.')
        return redirect('artes')
    if request.method == 'POST':
        form = ArteForm(request.POST, request.FILES, instance=arte)
        if form.is_valid():
            form.save()
            messages.success(request, f'Obra {arte.titulo} alterada com sucesso!')
            return redirect('artes')
    else:
        form = ArteForm(instance=arte)
    return render(request, 'editar_arte.html', {'form': form, 'arte': arte})

@login_required
def excluir_arte(request, arte_id):
    arte = get_object_or_404(Arte, pk=arte_id)
    if request.user != arte.usuario:
        messages.error(request, 'Você não tem permissão para excluir esta arte.')
        return redirect('artes')
    arte_titulo = arte.titulo 
    arte.delete()
    messages.success(request, f'A obra "{arte_titulo}" foi excluída com sucesso.')
    return redirect('artes')

@login_required
def ideias(request):
    ideias_list = Ideia.objects.all().order_by('-data_publicacao')
    
    query = request.GET.get('q')
    if query:
        ideias_list = ideias_list.filter(texto__icontains=query)

    ideias_por_pagina = 8
    
    paginator = Paginator(ideias_list, ideias_por_pagina)
    page = request.GET.get('page')
    try:
        ideias = paginator.page(page)
    except PageNotAnInteger:
        ideias = paginator.page(1)
    except EmptyPage:
        ideias = paginator.page(paginator.num_pages)
    
    return render(request, 'ideias.html', {'ideias': ideias, 'query': query, 'total': len(ideias_list)})

@login_required
def buscar_ideias(request):
    query = request.GET.get('query', '')
    ideias = Ideia.objects.filter(texto__icontains=query)[:10] # Limita a 10 resultados
    ideias_data = [{'texto': ideia.texto} for ideia in ideias]

    return JsonResponse({'ideias': ideias_data})

@login_required
def adicionar_ideia(request):
    if request.method == 'POST':
        form = IdeiaForm(request.POST)
        if form.is_valid():
            ideia = form.save(commit=False)
            ideia.usuario = request.user
            ideia.save()
            messages.success(request, f'Ideia "{ideia.id}" adicionada com sucesso!')
            return redirect('ideias')
    else:
        form = IdeiaForm()
    return render(request, 'adicionar_ideia.html', {'form': form})

@login_required
def editar_ideia(request, ideia_id):
    ideia = get_object_or_404(Ideia, pk=ideia_id)
    if request.user != ideia.usuario:
        messages.error(request, 'Você não tem permissão para excluir esta ideia.')
        return redirect('ideias')
    if request.method == 'POST':
        form = IdeiaForm(request.POST, instance=ideia)
        if form.is_valid():
            form.save()
            messages.success(request, f'Ideia {ideia.id} alterada com sucesso!')
            return redirect('ideias')
    else:
        form = IdeiaForm(instance=ideia)
    return render(request, 'editar_ideia.html', {'form': form, 'ideia': ideia})

@login_required
def excluir_ideia(request, ideia_id):
    ideia = get_object_or_404(Ideia, pk=ideia_id)
    if request.user != ideia.usuario:
        messages.error(request, 'Você não tem permissão para excluir esta ideia.')
        return redirect('ideias')
    ideia_id = ideia.id 
    ideia.delete()
    messages.success(request, f'A ideia "{ideia_id}" foi excluída com sucesso.')
    return redirect('ideias')

def dashboard(request):
    autores = Autor.objects.annotate(num_livros=Count('livro'))
    data_autores = [{'nome': autor.nome, 'num_livros': autor.num_livros} for autor in autores]

    categorias = Categoria.objects.annotate(num_livros=Count('livro'))
    data_categorias = [{'nome': categoria.nome, 'num_livros': categoria.num_livros} for categoria in categorias]

    editoras = Editora.objects.annotate(num_livros=Count('livro'))
    data_editoras = [{'nome': editora.nome, 'num_livros': editora.num_livros} for editora in editoras]

    autores_pensamentos = Autor.objects.annotate(num_pensamentos=Count('pensamento'))
    data_autores_pensamentos = [{'nome': autor.nome, 'num_pensamentos': autor.num_pensamentos} for autor in autores_pensamentos]

    livros = Livro.objects.annotate(num_comentarios=Count('comentarios'))
    data_livros_comentarios = [{'nome': livro.titulo, 'num_comentarios': livro.num_comentarios} for livro in livros]

    livros_usuarios = User.objects.annotate(count=Count('livro'))
    data_livros_usuarios = [{'nome': livro.username, 'count': livro.count} for livro in livros_usuarios]

    autores_usuarios = User.objects.annotate(count=Count('autor'))
    data_autores_usuarios = [{'nome': autor.username, 'count': autor.count} for autor in autores_usuarios]

    pensamentos_usuarios = User.objects.annotate(count=Count('pensamento'))
    data_pensamentos_usuarios = [{'nome': pensamento.username, 'count': pensamento.count} for pensamento in pensamentos_usuarios]

    comentarios_usuarios = User.objects.annotate(count=Count('comentariolivro'))
    data_comentarios_usuarios = [{'nome': comentario.username, 'count': comentario.count} for comentario in comentarios_usuarios]

    artes_usuarios = User.objects.annotate(count=Count('arte'))
    data_artes_usuarios = [{'nome': arte.username, 'count': arte.count} for arte in artes_usuarios]

    ideias_usuarios = User.objects.annotate(count=Count('ideia'))
    data_ideias_usuarios = [{'nome': ideia.username, 'count': ideia.count} for ideia in ideias_usuarios]

    return render(request, 'dashboard.html', {
        'data_autores': data_autores,
        'data_categorias': data_categorias,
        'data_editoras': data_editoras,
        'data_autores_pensamentos': data_autores_pensamentos,
        'data_livros_comentarios': data_livros_comentarios,
        'data_livros_usuarios': data_livros_usuarios,
        'data_autores_usuarios': data_autores_usuarios,
        'data_pensamentos_usuarios': data_pensamentos_usuarios,
        'data_comentarios_usuarios': data_comentarios_usuarios,
        'data_artes_usuarios': data_artes_usuarios,
        'data_ideias_usuarios': data_ideias_usuarios
    })