from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from accounts.models import User


def upload_to(instance, filename):
    return 'product/{product_name}/{filename}'.format(
        product_name=instance.user, filename=filename)


class Category(models.Model):
    category_name = models.CharField(max_length=50, verbose_name=_("Nome da categoria"),null=True, blank=True)
    created_date = models.DateTimeField(verbose_name=_('Data criação'), default=timezone.now, editable=False)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.category_name
    
    class Meta:
        verbose_name = _("Categoria")
        verbose_name_plural = _("Categorias")


class Products(models.Model):
    user = models.ForeignKey(User,verbose_name=_("Usuário"), on_delete=models.CASCADE)
    category = models.ForeignKey(Category,verbose_name=_("Categoria"), on_delete=models.CASCADE)
    product_name = models.CharField(max_length=150, verbose_name=_("Nome do produto"), null=True, blank=True)
    image = models.ImageField(upload_to=upload_to, verbose_name=_("Imagem do produto"), null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Preço do produto"), null=True, blank=True)
    description = models.TextField(max_length=500, verbose_name=_("Descrição do produto"), null=True, blank=True)
    created_date = models.DateTimeField(verbose_name=_('Data criação'), default=timezone.now, editable=False)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.product_name
    
    class Meta:
        verbose_name = _("Produto")
        verbose_name_plural = _("Produtos")

