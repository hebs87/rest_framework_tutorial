from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
# Allows us to populate the highlighted field when the model is saved
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight


# Create your models here.
LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


class Snippet(models.Model):
    """
    A model used to store code snippets
    """
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    lineons = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)
    # Used to represent the user who created the snippet
    owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)
    # Used to store the HTML representation of the code snippet
    highlighted = models.TextField()

    class Meta:
        ordering = ['created']

    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML
        representation of the code snippet.
        """
        lexer = get_lexer_by_name(self.language)
        lineons = 'table' if self.lineons else False
        options = {'title': self.title} if self.title else {}
        formatter = HtmlFormatter(style=self.style, lineons=lineons,
                                  full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super(Snippet, self).save(*args, **kwargs)
