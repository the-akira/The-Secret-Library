from django.contrib.auth.models import User
from django.conf import settings
from django.db import models

class Autor(models.Model):
    nome = models.CharField(max_length=100)
    biografia = models.TextField(blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    foto = models.ImageField(upload_to='autores_fotos/', blank=True, null=True, default='author.png')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nome

class Pensamento(models.Model):
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    texto = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Pensamento de {self.autor.nome} em {self.data_criacao}"

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nome

class Editora(models.Model):
    nome = models.CharField(max_length=100)
    website = models.URLField(blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nome

class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    editora = models.ForeignKey(Editora, on_delete=models.SET_NULL, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    sinopse = models.TextField(blank=True, null=True)
    data_publicacao = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    capa = models.ImageField(upload_to='livros_covers/', blank=True, null=True, default='book.png')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    link = models.URLField(max_length=350, null=True, blank=True)
    
    def __str__(self):
        return self.titulo

class ComentarioLivro(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE, related_name='comentarios')
    texto = models.TextField()
    data_publicacao = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comentário de {self.usuario.username} em {self.livro.titulo}"

class ListaDesejos(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    livros = models.ManyToManyField(Livro)
    
    def __str__(self):
        return f"Lista de Desejos de {self.usuario.username}"

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    avatar = models.ImageField(upload_to='usuarios_avatares/', blank=True, null=True, default='profile.png')

    def __str__(self):
        return f"Profile of {self.user.username}"