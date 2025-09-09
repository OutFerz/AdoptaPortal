from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField("Nombre", max_length=60, unique=True)
    slug = models.SlugField("Slug", max_length=70, unique=True)
    description = models.TextField("Descripción", blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ("name",)


class Tag(models.Model):
    name = models.CharField("Nombre", max_length=32, unique=True)
    slug = models.SlugField("Slug", max_length=40, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Etiqueta"
        verbose_name_plural = "Etiquetas"
        ordering = ("name",)


STATUS_CHOICES = (("draft", "Borrador"), ("published", "Publicado"))


class Post(models.Model):
    title = models.CharField("Título", max_length=140)
    slug = models.SlugField("Slug", max_length=160, unique=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="posts",
        verbose_name="Autor",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="posts",
        verbose_name="Categoría",
    )
    content = models.TextField("Contenido")
    hero_image = models.ImageField("Imagen principal", upload_to="blog/", blank=True, null=True)
    status = models.CharField("Estado", max_length=10, choices=STATUS_CHOICES, default="draft")
    published_at = models.DateTimeField("Fecha de publicación", blank=True, null=True)
    updated_at = models.DateTimeField("Actualizado", auto_now=True)

    # Tags como relación ManyToMany
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts", verbose_name="Etiquetas")

    class Meta:
        db_table = "blog_posts"
        verbose_name = "Publicación"
        verbose_name_plural = "Publicaciones"
        ordering = ("-published_at", "title")
        indexes = [
            models.Index(fields=["-published_at"]),
            models.Index(fields=["category", "-published_at"]),
            models.Index(fields=["slug"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.slug])

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments", verbose_name="Publicación")
    name = models.CharField("Nombre", max_length=80)
    email = models.EmailField("Email")
    body = models.TextField("Comentario")
    created_at = models.DateTimeField("Creado", auto_now_add=True)
    approved = models.BooleanField("Aprobado", default=True)

    class Meta:
        verbose_name = "Comentario"
        verbose_name_plural = "Comentarios"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comentario de {self.name} en {self.post.title}"