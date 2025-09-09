from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from django.utils import timezone
from .models import Post, Category, Comment
from django import forms

class CommentForm(forms.Form):
    name = forms.CharField(max_length=80)
    email = forms.EmailField()
    body = forms.CharField(widget=forms.Textarea)

def post_list(request):
    q = request.GET.get("q") or ""
    tag = request.GET.get("tag")
    cat = request.GET.get("cat")

    qs = Post.objects.filter(status="published").order_by("-published_at")
    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(content__icontains=q) | Q(tags__icontains=q))
    if tag:
        qs = qs.filter(tags__icontains=tag)
    if cat:
        qs = qs.filter(category__slug=cat)

    return render(request, "blog/post_list.html", {"posts": qs, "q": q, "tag": tag, "cat": cat})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status="published")
    form = CommentForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data
        comments = post.comments or []
        comments.append(Comment(**data))
        post.comments = comments
        if not post.published_at:
            post.published_at = timezone.now()
        post.save()
        return redirect("blog:post_detail", slug=post.slug)
    return render(request, "blog/post_detail.html", {"post": post, "form": form})