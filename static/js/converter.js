/**
 * File Converter Alpine.js component.
 * Handles file upload, conversion via the appropriate API, and download.
 * Configuration is injected via window.CONVERTER_CONFIG from the template.
 */
function converterTool() {
    return {
        // State
        file: null,
        fileName: '',
        fileUploaded: false,
        dragging: false,
        processing: false,
        downloadReady: false,
        downloadUrl: '',
        resultPreviewUrl: '',
        previewUrl: '',
        error: '',
        quality: 90,

        // Config (populated from window.CONVERTER_CONFIG)
        config: {},

        init() {
            this.config = window.CONVERTER_CONFIG || {};
        },

        handleFileSelect(event) {
            var f = event.target.files[0];
            if (!f) return;
            this.setFile(f);
        },

        handleDrop(event) {
            this.dragging = false;
            var f = event.dataTransfer.files[0];
            if (!f) return;
            this.setFile(f);
        },

        setFile(f) {
            this.file = f;
            this.fileName = f.name;
            this.fileUploaded = true;
            this.downloadReady = false;
            this.downloadUrl = '';
            this.resultPreviewUrl = '';
            this.error = '';

            // Generate image preview if applicable
            if (f.type && f.type.startsWith('image/')) {
                this.previewUrl = URL.createObjectURL(f);
            } else {
                this.previewUrl = '';
            }
        },

        resetTool() {
            this.file = null;
            this.fileName = '';
            this.fileUploaded = false;
            this.downloadReady = false;
            this.downloadUrl = '';
            this.previewUrl = '';
            this.resultPreviewUrl = '';
            this.error = '';
        },

        async convert() {
            if (!this.file) return;

            this.processing = true;
            this.error = '';
            this.downloadReady = false;
            this.resultPreviewUrl = '';

            try {
                var formData = new FormData();
                formData.append('file', this.file);

                var cfg = this.config;

                if (cfg.apiMethod === 'image') {
                    // Image-to-image conversion via /api/media/convert-image/
                    formData.append('format', cfg.targetFormat);
                    formData.append('quality', this.quality);
                } else if (cfg.apiMethod === 'pdf') {
                    // Document conversion via /api/pdf/convert/
                    formData.append('direction', cfg.direction);
                    formData.append('format', cfg.targetFormat);
                }

                var response = await fetch(cfg.apiEndpoint, {
                    method: 'POST',
                    headers: { 'X-CSRFToken': this.getCsrfToken() },
                    body: formData
                });

                if (!response.ok) {
                    var contentType = response.headers.get('content-type') || '';
                    if (contentType.indexOf('application/json') !== -1) {
                        var data = await response.json();
                        this.error = data.error || 'An error occurred during conversion.';
                    } else {
                        this.error = 'An error occurred during conversion. Please try again.';
                    }
                    this.processing = false;
                    return;
                }

                var blob = await response.blob();
                this.downloadUrl = URL.createObjectURL(blob);

                // Show image preview for image outputs
                if (blob.type && blob.type.startsWith('image/')) {
                    this.resultPreviewUrl = this.downloadUrl;
                }

                this.downloadReady = true;

            } catch (e) {
                this.error = 'Network error. Please check your connection and try again.';
            }

            this.processing = false;
        },

        getCsrfToken() {
            var el = document.querySelector('[name=csrfmiddlewaretoken]');
            if (el) return el.value;
            var metaEl = document.querySelector('meta[name="csrf-token"]');
            if (metaEl) return metaEl.content;
            var match = document.cookie.match(/csrftoken=([^;]+)/);
            return match ? match[1] : '';
        }
    };
}
