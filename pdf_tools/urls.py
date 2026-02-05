from django.urls import path

from pdf_tools.views import (
    PDFToolsIndex, PDFToolPage,
    PDFMergeAPI, PDFSplitAPI, PDFConvertAPI, PDFCompressAPI,
    PDFRotateAPI, PDFRemovePagesAPI, PDFReorderPagesAPI, PDFInfoAPI, ChatPDFAPI,
)

urlpatterns = [
    # Page views
    path('pdf-tools/', PDFToolsIndex.as_view(), name='pdf_tools_index'),
    path('pdf-tools/<slug:tool_slug>/', PDFToolPage.as_view(), name='pdf_tool_page'),

    # API endpoints
    path('api/pdf/merge/', PDFMergeAPI.as_view(), name='pdf_merge_api'),
    path('api/pdf/split/', PDFSplitAPI.as_view(), name='pdf_split_api'),
    path('api/pdf/convert/', PDFConvertAPI.as_view(), name='pdf_convert_api'),
    path('api/pdf/compress/', PDFCompressAPI.as_view(), name='pdf_compress_api'),
    path('api/pdf/rotate/', PDFRotateAPI.as_view(), name='pdf_rotate_api'),
    path('api/pdf/remove-pages/', PDFRemovePagesAPI.as_view(), name='pdf_remove_pages_api'),
    path('api/pdf/reorder/', PDFReorderPagesAPI.as_view(), name='pdf_reorder_api'),
    path('api/pdf/info/', PDFInfoAPI.as_view(), name='pdf_info_api'),
    path('api/pdf/chat/', ChatPDFAPI.as_view(), name='pdf_chat_api'),
]
