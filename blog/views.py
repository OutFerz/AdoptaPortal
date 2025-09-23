# blog/views.py
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q, Prefetch
from django.contrib import messages

from .models import Post, Category, Tag, Comment
from .forms import CommentForm


def post_list(request):
    """
    Lista del blog con buscador robusto.
    - Acepta q / query / s
    - Acepta tag / etiqueta / t
    - Acepta cat / categoria / c (slug o id)
    - Filtra por título, contenido, categoría, autor y tags
    """
    q_raw   = (request.GET.get("q") or request.GET.get("query") or request.GET.get("s") or "").strip()
    tag_raw = (request.GET.get("tag") or request.GET.get("etiqueta") or request.GET.get("t") or "").strip()
    cat_raw = (request.GET.get("cat") or request.GET.get("categoria") or request.GET.get("c") or "").strip()

    qs = (
        Post.objects.filter(status="published")
        .select_related("category", "author")
        .prefetch_related("tags")
        .order_by("-published_at", "-updated_at", "-id")
    )

    # Búsqueda de texto
    if q_raw:
        qs = qs.filter(
            Q(title__icontains=q_raw)
            | Q(content__icontains=q_raw)
            | Q(category__name__icontains=q_raw)
            | Q(author__username__icontains=q_raw)
            | Q(tags__name__icontains=q_raw)
            | Q(tags__slug__icontains=q_raw)
        )

    # Filtro por tag (slug o nombre)
    if tag_raw:
        qs = qs.filter(Q(tags__slug=tag_raw) | Q(tags__name__iexact=tag_raw))

    # Filtro por categoría (slug o id)
    if cat_raw:
        if cat_raw.isdigit():
            qs = qs.filter(category_id=int(cat_raw))
        else:
            qs = qs.filter(Q(category__slug=cat_raw) | Q(category__name__iexact=cat_raw))

    qs = qs.distinct()

    context = {
        "posts": qs,
        "q": q_raw,
        "tag": tag_raw,
        "cat": cat_raw,
    }
    return render(request, "blog/post_list.html", context)


def post_detail(request, slug):
    """
    Detalle del post + comentarios aprobados y formulario de comentario.
    """
    # Prefetch solo comentarios aprobados
    approved_comments_qs = Comment.objects.filter(approved=True).order_by("-created_at")
    post = get_object_or_404(
        Post.objects.select_related("category", "author").prefetch_related(
            "tags",
            Prefetch("comments", queryset=approved_comments_qs, to_attr="approved_comments"),
        ),
        slug=slug,
        status="published",
    )

    comments = getattr(post, "approved_comments", [])

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.post = post
            c.save()
            messages.success(request, "¡Gracias! Tu comentario se publicó correctamente.")
            return redirect("blog:post_detail", slug=post.slug)
        else:
            messages.error(request, "Revisa los errores del formulario.")
    else:
        form = CommentForm()

    return render(
        request,
        "blog/post_detail.html",
        {"post": post, "comments": comments, "form": form},
    )