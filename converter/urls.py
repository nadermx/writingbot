from django.urls import path

from converter.views import ConverterIndexPage, ConverterPairPage

urlpatterns = [
    path('convert/', ConverterIndexPage.as_view(), name='converter_index'),
    path('convert/<str:source>-to-<str:target>/', ConverterPairPage.as_view(), name='converter_pair'),
]
