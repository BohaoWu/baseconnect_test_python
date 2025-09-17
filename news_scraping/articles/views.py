from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages

from .forms import UrlForm
from .models import Articles
from .services import extract_news, get_abstract, score_risk


def index(request):
    rows = Articles.objects.order_by("-created_at")[:50]  # 50件まで取得
    form = UrlForm()
    return render(request, "articles/index.html", {
        "rows": rows,
        "form": form,
    })


def detail(request, article_id):
    question = get_object_or_404(Articles, pk=article_id)
    return render(request, "polls/detail.html", {"question": question})


def create(request):
    if request.method != "POST":
        return redirect("articles:index")

    form = UrlForm(request.POST)
    if not form.is_valid():
        messages.error(request, "URLが正しくありません。")
        rows = Articles.objects.order_by("-created_at")[:50]
        return render(request, "articles/index.html", {"form": form, "rows": rows})

    article = extract_news(form.cleaned_data["url"])
    article.abstract = get_abstract(article.text)
    article.risk_score = score_risk(article.text)

    article.save()
    messages.success(request, "記事を保存しました。")
    
    return redirect("articles:index")