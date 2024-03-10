from django.contrib import admin
from .models import (
    ComentarioLivro,
    ListaDesejos, 
    Pensamento,
    Categoria, 
    Mensagem,
    Editora, 
    Profile,
    Autor, 
    Livro, 
)

class PensamentoInline(admin.TabularInline):
    model = Pensamento
    extra = 0

class LivroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'editora', 'categoria', 'data_publicacao', 'usuario')
    list_filter = ('editora', 'categoria')
    search_fields = ('titulo', 'autor__nome', 'categoria__nome')

class ComentarioLivroAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'livro', 'texto')
    list_filter = ('usuario', 'livro')
    search_fields = ('texto',)

class ListaDesejosAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'livros_list')

    def livros_list(self, obj):
        return ", ".join([livro.titulo for livro in obj.livros.all()])

class AutorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'data_nascimento')
    search_fields = ('nome',)
    inlines = [PensamentoInline]

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'birth_date')
    list_filter = ('birth_date',)
    search_fields = ('user',)

class PensamentoAdmin(admin.ModelAdmin):
    list_display = ('autor', 'texto', 'data_criacao')
    list_filter = ('autor', 'data_criacao')
    search_fields = ('texto',)

class MensagemAdmin(admin.ModelAdmin):
    list_display = ('remetente', 'destinatario', 'assunto', 'timestamp')
    list_filter = ('remetente', 'destinatario')
    search_fields = ('assunto',)

admin.site.register(Editora)
admin.site.register(Categoria)
admin.site.register(Livro, LivroAdmin)
admin.site.register(ComentarioLivro, ComentarioLivroAdmin)
admin.site.register(ListaDesejos, ListaDesejosAdmin)
admin.site.register(Autor, AutorAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Mensagem, MensagemAdmin)
admin.site.register(Pensamento, PensamentoAdmin)