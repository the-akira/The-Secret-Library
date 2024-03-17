from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import (
    Arte,
    Ideia,
    Autor,
    Livro, 
    Editora,
    Profile,
    Mensagem,
    Pensamento,
    ComentarioLivro
)

class LoginForm(forms.Form):
    username = forms.CharField(label='Nome de Usuário', max_length=100)
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)

class ArteForm(forms.ModelForm):
    class Meta:
        model = Arte
        fields = ['titulo', 'obra']
        widgets = {
            'titulo': forms.TextInput(attrs={'placeholder': 'Título'}),
        }

class IdeiaForm(forms.ModelForm):
    class Meta:
        model = Ideia
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={'placeholder': 'Texto'}),
        }

class AutorForm(forms.ModelForm):
    data_nascimento = forms.DateField(
        widget=forms.DateInput(format='%d-%m-%Y', attrs={'placeholder': '25-12-1900'}),
        input_formats=('%d-%m-%Y',)
    )
    
    class Meta:
        model = Autor
        fields = ['nome', 'biografia', 'data_nascimento', 'foto']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Nome do Autor'}),
            'biografia': forms.Textarea(attrs={'placeholder': 'Biografia do Autor'})
        }

class PensamentoForm(forms.ModelForm):
    class Meta:
        model = Pensamento
        fields = ['texto']

class PensamentoAutoresForm(forms.ModelForm):
    class Meta:
        model = Pensamento
        fields = ['autor', 'texto']
        widgets = {
            'autor': forms.Select(attrs={'class': 'form-control'}),
            'texto': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super(PensamentoAutoresForm, self).__init__(*args, **kwargs)
        self.fields['autor'].queryset = Autor.objects.all()

class LivroForm(forms.ModelForm):
    data_publicacao = forms.DateField(
        widget=forms.DateInput(format='%d-%m-%Y', attrs={'placeholder': 'dd-mm-yyyy'}),
        input_formats=('%d-%m-%Y',)
    )

    class Meta:
        model = Livro
        fields = ['titulo', 'autor', 'editora', 'categoria', 'sinopse', 'data_publicacao', 'isbn', 'link', 'capa']
        widgets = {
            'titulo': forms.TextInput(attrs={'placeholder': 'Título do Livro'}),
            'sinopse': forms.Textarea(attrs={'placeholder': 'Sinopse do Livro'}),
            'isbn': forms.TextInput(attrs={'placeholder': 'ISBN do Livro'}),
            'link': forms.URLInput(attrs={'placeholder': 'Link do Livro'}),
        }

class LivroFormSemAutor(LivroForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('autor')

class ComentarioLivroForm(forms.ModelForm):
    class Meta:
        model = ComentarioLivro
        fields = ['texto']

class ComentarioLivrosForm(forms.ModelForm):
    class Meta:
        model = ComentarioLivro
        fields = ['livro', 'texto']
        widgets = {
            'livro': forms.Select(attrs={'class': 'form-control'}),
            'texto': forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ComentarioLivrosForm, self).__init__(*args, **kwargs)
        self.fields['livro'].queryset = Livro.objects.all()

class EditoraForm(forms.ModelForm):
    class Meta:
        model = Editora
        fields = ['nome', 'website']
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Nome da Editora'}),
            'website': forms.URLInput(attrs={'placeholder': 'Website da Editora'}),
        }

class ProfileForm(forms.ModelForm):
    birth_date = forms.DateField(
        widget=forms.DateInput(format='%d-%m-%Y', attrs={'placeholder': '25-12-1900'}),
        input_formats=('%d-%m-%Y',)
    )
    
    class Meta:
        model = Profile
        fields = ['bio', 'birth_date', 'avatar']

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class MensagemForm(forms.ModelForm):
    class Meta:
        model = Mensagem
        fields = ['assunto', 'corpo']
        labels = {
            'assunto': 'Assunto',
            'corpo': 'Mensagem',
        }
        widgets = {
            'corpo': forms.Textarea(attrs={'rows': 5}),
        }

class MensagemUsersForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(MensagemUsersForm, self).__init__(*args, **kwargs)
        self.fields['destinatario'].queryset = User.objects.exclude(pk=user.pk)

    destinatario = forms.ModelChoiceField(queryset=User.objects.all(), label='Destinatário')

    class Meta:
        model = Mensagem
        fields = ['destinatario', 'assunto', 'corpo']
        labels = {
            'assunto': 'Assunto',
            'corpo': 'Mensagem',
        }
        widgets = {
            'corpo': forms.Textarea(attrs={'rows': 5}),
        }