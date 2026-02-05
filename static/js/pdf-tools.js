/**
 * PDF Tools Alpine.js component.
 * Handles file upload, processing, and download for all PDF tool pages.
 */
function pdfTool() {
    return {
        // State
        files: [],
        fileNames: [],
        fileName: '',
        fileUploaded: false,
        dragging: false,
        processing: false,
        downloadReady: false,
        downloadUrl: '',
        error: '',
        savingsPercent: '',

        // Tool-specific options
        pageSelection: '',
        rotatePageNum: 1,
        rotateAngle: '90',
        compressionQuality: 'medium',
        pageOrder: '',
        pageCount: 0,

        // Chat PDF
        question: '',
        messages: [],

        init() {
            // Detect tool slug from URL
            const pathParts = window.location.pathname.split('/').filter(Boolean);
            this.toolSlug = pathParts[pathParts.length - 1] || '';
        },

        handleFileSelect(event) {
            const fileList = event.target.files;
            if (!fileList || fileList.length === 0) return;
            this.setFiles(Array.from(fileList));
        },

        handleDrop(event) {
            this.dragging = false;
            const fileList = event.dataTransfer.files;
            if (!fileList || fileList.length === 0) return;
            this.setFiles(Array.from(fileList));
        },

        setFiles(fileArray) {
            this.files = fileArray;
            this.fileNames = fileArray.map(f => f.name);
            this.fileName = fileArray[0]?.name || '';
            this.fileUploaded = true;
            this.downloadReady = false;
            this.downloadUrl = '';
            this.error = '';
            this.savingsPercent = '';
            this.messages = [];

            // Get PDF info for chat tool
            if (this.toolSlug === 'chat-pdf' && fileArray.length > 0) {
                this.getPDFInfo(fileArray[0]);
            }
        },

        resetTool() {
            this.files = [];
            this.fileNames = [];
            this.fileName = '';
            this.fileUploaded = false;
            this.downloadReady = false;
            this.downloadUrl = '';
            this.error = '';
            this.savingsPercent = '';
            this.messages = [];
            this.question = '';
            this.pageCount = 0;
        },

        async getPDFInfo(file) {
            try {
                const formData = new FormData();
                formData.append('file', file);
                const response = await fetch('/api/pdf/info/', {
                    method: 'POST',
                    headers: { 'X-CSRFToken': this.getCsrfToken() },
                    body: formData
                });
                if (response.ok) {
                    const data = await response.json();
                    this.pageCount = data.page_count || 0;
                }
            } catch (e) {
                // Non-critical, proceed without page count
            }
        },

        async processFile() {
            if (this.files.length === 0) return;

            this.processing = true;
            this.error = '';
            this.downloadReady = false;
            this.savingsPercent = '';

            try {
                const formData = new FormData();
                let endpoint = '';

                switch (this.toolSlug) {
                    case 'merge-pdf':
                        endpoint = '/api/pdf/merge/';
                        this.files.forEach(f => formData.append('files', f));
                        break;

                    case 'split-pdf':
                        endpoint = '/api/pdf/split/';
                        formData.append('file', this.files[0]);
                        formData.append('pages', this.pageSelection || 'all');
                        break;

                    case 'compress-pdf':
                        endpoint = '/api/pdf/compress/';
                        formData.append('file', this.files[0]);
                        formData.append('quality', this.compressionQuality);
                        break;

                    case 'rotate-pdf':
                        endpoint = '/api/pdf/rotate/';
                        formData.append('file', this.files[0]);
                        formData.append('page', this.rotatePageNum);
                        formData.append('angle', this.rotateAngle);
                        break;

                    case 'remove-pages':
                        endpoint = '/api/pdf/remove-pages/';
                        formData.append('file', this.files[0]);
                        formData.append('pages', this.pageSelection);
                        break;

                    case 'reorder-pages':
                        endpoint = '/api/pdf/reorder/';
                        formData.append('file', this.files[0]);
                        const orderArray = this.pageOrder.split(',').map(s => parseInt(s.trim())).filter(n => !isNaN(n));
                        formData.append('order', JSON.stringify(orderArray));
                        break;

                    case 'pdf-to-word':
                        endpoint = '/api/pdf/convert/';
                        formData.append('file', this.files[0]);
                        formData.append('direction', 'from_pdf');
                        formData.append('format', 'docx');
                        break;

                    case 'word-to-pdf':
                        endpoint = '/api/pdf/convert/';
                        formData.append('file', this.files[0]);
                        formData.append('direction', 'to_pdf');
                        break;

                    case 'pdf-to-jpg':
                        endpoint = '/api/pdf/convert/';
                        formData.append('file', this.files[0]);
                        formData.append('direction', 'from_pdf');
                        formData.append('format', 'jpg');
                        break;

                    case 'jpg-to-pdf':
                        endpoint = '/api/pdf/convert/';
                        formData.append('file', this.files[0]);
                        formData.append('direction', 'to_pdf');
                        break;

                    case 'pdf-to-png':
                        endpoint = '/api/pdf/convert/';
                        formData.append('file', this.files[0]);
                        formData.append('direction', 'from_pdf');
                        formData.append('format', 'png');
                        break;

                    case 'png-to-pdf':
                        endpoint = '/api/pdf/convert/';
                        formData.append('file', this.files[0]);
                        formData.append('direction', 'to_pdf');
                        break;

                    case 'pdf-to-ppt':
                        endpoint = '/api/pdf/convert/';
                        formData.append('file', this.files[0]);
                        formData.append('direction', 'from_pdf');
                        formData.append('format', 'pptx');
                        break;

                    case 'ppt-to-pdf':
                        endpoint = '/api/pdf/convert/';
                        formData.append('file', this.files[0]);
                        formData.append('direction', 'to_pdf');
                        break;

                    case 'pdf-editor':
                        // Editor defaults to split (extract) if pages given, otherwise just re-saves
                        endpoint = '/api/pdf/split/';
                        formData.append('file', this.files[0]);
                        formData.append('pages', this.pageSelection || 'all');
                        break;

                    default:
                        this.error = 'Unknown tool.';
                        this.processing = false;
                        return;
                }

                const response = await fetch(endpoint, {
                    method: 'POST',
                    headers: { 'X-CSRFToken': this.getCsrfToken() },
                    body: formData
                });

                if (!response.ok) {
                    const contentType = response.headers.get('content-type') || '';
                    if (contentType.includes('application/json')) {
                        const data = await response.json();
                        this.error = data.error || 'An error occurred.';
                    } else {
                        this.error = 'An error occurred while processing your file.';
                    }
                    this.processing = false;
                    return;
                }

                // Check for compression savings headers
                const savings = response.headers.get('X-Savings-Percent');
                if (savings) {
                    this.savingsPercent = savings;
                }

                const blob = await response.blob();
                this.downloadUrl = URL.createObjectURL(blob);
                this.downloadReady = true;

            } catch (e) {
                this.error = 'Network error. Please try again.';
            }

            this.processing = false;
        },

        async askQuestion() {
            if (!this.question.trim() || this.files.length === 0) return;

            const q = this.question.trim();
            this.messages.push({ role: 'user', content: q });
            this.question = '';
            this.processing = true;

            try {
                const formData = new FormData();
                formData.append('file', this.files[0]);
                formData.append('question', q);

                const response = await fetch('/api/pdf/chat/', {
                    method: 'POST',
                    headers: { 'X-CSRFToken': this.getCsrfToken() },
                    body: formData
                });

                const data = await response.json();

                if (response.ok) {
                    this.messages.push({ role: 'assistant', content: data.answer });
                } else {
                    this.messages.push({ role: 'assistant', content: data.error || 'Sorry, an error occurred.' });
                }

                // Scroll to bottom
                this.$nextTick(() => {
                    if (this.$refs.chatMessages) {
                        this.$refs.chatMessages.scrollTop = this.$refs.chatMessages.scrollHeight;
                    }
                });

            } catch (e) {
                this.messages.push({ role: 'assistant', content: 'Network error. Please try again.' });
            }

            this.processing = false;
        },

        getCsrfToken() {
            const el = document.querySelector('[name=csrfmiddlewaretoken]');
            if (el) return el.value;
            const match = document.cookie.match(/csrftoken=([^;]+)/);
            return match ? match[1] : '';
        }
    };
}
