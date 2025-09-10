from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from django.contrib import messages

from .models import Post, Category, Tag, Comment
from .forms import CommentForm  # usa el ModelForm que te propuse en blog/forms.py


def post_list(request):
    q = (request.GET.get("q") or "").strip()
    tag_slug = (request.GET.get("tag") or "").strip()
    cat_slug = (request.GET.get("cat") or "").strip()

    qs = (
        Post.objects.filter(status="published")
        .select_related("category", "author")
        .prefetch_related("tags")
        .order_by("-published_at", "-id")
    )

    if q:
        qs = qs.filter(
            Q(title__icontains=q) |
            Q(content__icontains=q) |
            Q(tags__name__icontains=q) |
            Q(tags__slug__icontains=q)
        )

    if tag_slug:
        qs = qs.filter(tags__slug=tag_slug)

    if cat_slug:
        qs = qs.filter(category__slug=cat_slug)

    qs = qs.distinct()

    context = {
        "posts": qs,
        "q": q,
        "tag": tag_slug,
        "cat": cat_slug,
    }
    return render(request, "blog/post_list.html", context)


def post_detail(request, slug):
    post = get_object_or_404(
        Post.objects.select_related("category", "author").prefetch_related("tags"),
        slug=slug,
        status="published",
    )

    # Lista de comentarios aprobados (orden más reciente primero)
    comments = post.comments.filter(approved=True).order_by("-created_at")

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