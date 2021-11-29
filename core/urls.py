from django.urls import include, path
from rest_framework.routers import DefaultRouter

from core.views.acc_bank import AccBankViewSet
from core.views.stock_counter import StockCounterViewSet
from core.views.topic import TopicViewSet
from core.views.user import user
from core.views.user.article import UserArticleViewSet

router = DefaultRouter()
router.register(r'acc/banks', AccBankViewSet)
router.register(r'topics', TopicViewSet)
router.register(r'stock/counters', StockCounterViewSet)

router.register(r'user/profile/author/articles/', UserArticleViewSet, basename='user-articles')

urlpatterns = [
    path('user/profile/', user.profile),
    path('user/profile/author-registration/', user.author_registration),
    path('user/profile/author/', user.author),

    path('', include(router.urls)),
]
