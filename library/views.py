from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from .forms import (
    AutorForm,
    LivroForm,
    LoginForm,
    ProfileForm,
    EditoraForm,
    PensamentoForm,
    LivroFormSemAutor,
    ComentarioLivroForm,
    ComentarioLivrosForm,
    PensamentoAutoresForm,
    CustomUserCreationForm,
)
from .models import (
    Autor,
    Livro,
    Profile,
    Editora,
    Pensamento,
    ComentarioLivro
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
            'editoras': editoras
        }
    )

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