from django.urls import include, path
from rest_framework.routers import DefaultRouter

from core.views.acc_bank import AccBankViewSet
from core.views.stock_counter import StockCounterViewSet
from core.views.topic import TopicViewSet

router = DefaultRouter()
router.register(r'acc/banks', AccBankViewSet)
router.register(r'topics', TopicViewSet)
router.register(r'stock/counters', StockCounterViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
