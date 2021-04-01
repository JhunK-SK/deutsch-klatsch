from django import forms
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

from mptt.forms import TreeNodeChoiceField
from .models import Post, Comment, TopicRequest


class PostCreationForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ['title', 'post',]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control mb-4',
                'placeholder': 'Subjekt',
            }),
            'post': SummernoteWidget(),
        }
        

class CommentCreationForm(forms.ModelForm):
    parent = TreeNodeChoiceField(queryset=Comment.objects.all())
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['parent'].widget.attrs.update({'class': 'd-none'})
        self.fields['parent'].label = ''
        self.fields['parent'].required = False
        
    
    class Meta:
        model = Comment
        fields = ['comment', 'parent']
        labels = {
            'comment': ('Kommentar'),
        }
        widgets = {
            'comment': SummernoteWidget(attrs={
                'summernote': {
                    'width': '100%',
                    'height': '280',
                    'toolbar': [
                        ['style', []],
                        ['font', ['bold', 'underline',]],
                        ['fontname', []],
                        ['color', ['color']],
                        ['insert', ['link',]],
                    ],
                }
            })
        }
        

class PostSearchFormInTopic(forms.Form):
    search_option = (
        ('title_post', 'Thema + Inhalt'),
        ('writer', 'Schwätzer'),
    )
    select = forms.ChoiceField(
        choices=search_option,
        label='',
        widget=forms.Select(attrs={'class': 'form-control form-control-sm'}),
    )
    search = forms.CharField(label='')
    
    
class TopicRequestForm(forms.ModelForm):
    
    class Meta:
        model = TopicRequest
        fields = ['category', 'topic', 'purpose']
        widgets = {
            'purpose': forms.Textarea(attrs={
                'placeholder': 'Sie werden diese Anfrage nicht löschen können'}
            )
        }
        labels = {
            'category': 'Kategorie',
            'topic': 'Thema',
            'purpose': 'Absicht',
        }