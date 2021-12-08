from django.urls import include, path
from rest_framework.routers import DefaultRouter

from core.views.acc_bank import AccBankViewSet
from core.views.article import ArticleViewSet
from core.views.author import AuthorNewArticleViewSet
from core.views.comment import ArticleCommentViewSet, ArticleCommentReplyViewSet
from core.views.stock_counter import StockCounterViewSet
from core.views.topic import TopicViewSet
from core.views.user import user
from core.views.user.article import UserArticleViewSet
from core.views.user.article_img_path import UserArticleImgViewSet
from core.views.user.user_img_path import UserImgPathViewSet

router = DefaultRouter()
router.register(r'acc/banks', AccBankViewSet)
router.register(r'topics', TopicViewSet)
router.register(r'stock/counters', StockCounterViewSet)

router.register(r'articles', ArticleViewSet)
router.register(r'articles/(?P<article_id>[0-9]+)/comments', ArticleCommentViewSet)
router.register(r'articles/(?P<article_id>[0-9]+)/comments/(?P<comment_id>[0-9]+)/replies',
                ArticleCommentReplyViewSet)

# router.register(r'authors/(?P<author_id>[0-9]+)/articles', ArticleViewSet)
router.register(r'authors/(?P<author_id>[0-9]+)/new-articles', AuthorNewArticleViewSet)

router.register(r'user/profile/author/article-imgs', UserArticleImgViewSet)
router.register(r'user/profile/author/articles', UserArticleViewSet)
router.register(r'user/profile/imgs', UserImgPathViewSet)

urlpatterns = [
    path('user/profile/', user.profile),
    path('user/profile/author-registration/', user.author_registration),
    path('user/profile/author/', user.author),

    path('', include(router.urls)),
]
