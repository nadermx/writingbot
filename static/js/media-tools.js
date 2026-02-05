/**
 * Media Tools Alpine.js component.
 * Handles image conversion, background removal, QR codes, and voice generation.
 */
function mediaTool() {
    return {
        // Shared state
        file: null,
        fileName: '',
        fileUploaded: false,
        dragging: false,
        processing: false,
        downloadReady: false,
        downloadUrl: '',
        resultPreviewUrl: '',
        previewUrl: '',
        audioUrl: '',
        error: '',
        toolType: '',

        // Image converter
        targetFormat: 'png',
        quality: 90,

        // QR code
        qrData: '',
        qrSize: '300',
        qrColor: '#000000',
        qrBgColor: '#FFFFFF',

        // Voice generator
        voiceText: '',
        voiceName: 'alloy',
        voiceSpeed: 1.0,

        // AI Image
        imageDescription: '',
        generatedPrompt: '',

        init() {
            // Detect tool type from page context
            const body = document.body;
            const meta = document.querySelector('meta[name="tool-type"]');
            // Infer from URL
            const path = window.location.pathname;
            if (path.includes('image-tools')) this.toolType = 'image-converter';
            else if (path.includes('background-remover')) this.toolType = 'background-remover';
            else if (path.includes('qr-code')) this.toolType = 'qr-code';
            else if (path.includes('ai-voice')) this.toolType = 'voice-generator';
            else if (path.includes('converter-tools')) this.toolType = 'ai-image-generator';
        },

        handleFileSelect(event) {
            const f = event.target.files[0];
            if (!f) return;
            this.setFile(f);
        },

        handleDrop(event) {
            this.dragging = false;
            const f = event.dataTransfer.files[0];
            if (!f) return;
            this.setFile(f);
        },

        setFile(f) {
            this.file = f;
            this.fileName = f.name;
            this.fileUploaded = true;
            this.downloadReady = false;
            this.error = '';
            this.resultPreviewUrl = '';

            // Generate preview
            if (f.type.startsWith('image/')) {
                this.previewUrl = URL.createObjectURL(f);
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
            this.audioUrl = '';
            this.error = '';
            this.generatedPrompt = '';
        },

        async processImage() {
            if (!this.file) return;
            this.processing = true;
            this.error = '';
            this.downloadReady = false;

            try {
                const formData = new FormData();
                formData.append('file', this.file);
                let endpoint = '';

                if (this.toolType === 'image-converter') {
                    endpoint = '/api/media/convert-image/';
                    formData.append('format', this.targetFormat);
                    formData.append('quality', this.quality);
                } else if (this.toolType === 'background-remover') {
                    endpoint = '/api/media/remove-bg/';
                }

                const response = await fetch(endpoint, {
                    method: 'POST',
                    headers: { 'X-CSRFToken': this.getCsrfToken() },
                    body: formData
                });

                if (!response.ok) {
                    const ct = response.headers.get('content-type') || '';
                    if (ct.includes('application/json')) {
                        const data = await response.json();
                        this.error = data.error || 'An error occurred.';
                    } else {
                        this.error = 'An error occurred while processing your image.';
                    }
                    this.processing = false;
                    return;
                }

                const blob = await response.blob();
                this.downloadUrl = URL.createObjectURL(blob);
                if (blob.type.startsWith('image/')) {
                    this.resultPreviewUrl = this.downloadUrl;
                }
                this.downloadReady = true;

            } catch (e) {
                this.error = 'Network error. Please try again.';
            }
            this.processing = false;
        },

        async generateQR() {
            if (!this.qrData.trim()) return;
            this.processing = true;
            this.error = '';
            this.downloadReady = false;

            try {
                const response = await fetch('/api/media/qr-code/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': this.getCsrfToken()
                    },
                    body: JSON.stringify({
                        data: this.qrData,
                        size: parseInt(this.qrSize),
                        color: this.qrColor,
                        bg_color: this.qrBgColor,
                    })
                });

                if (!response.ok) {
                    const data = await response.json();
                    this.error = data.error || 'Failed to generate QR code.';
                    this.processing = false;
                    return;
                }

                const blob = await response.blob();
                this.downloadUrl = URL.createObjectURL(blob);
                this.resultPreviewUrl = this.downloadUrl;
                this.downloadReady = true;

            } catch (e) {
                this.error = 'Network error. Please try again.';
            }
            this.processing = false;
        },

        async generateVoice() {
            if (!this.voiceText.trim()) return;
            this.processing = true;
            this.error = '';
            this.downloadReady = false;
            this.audioUrl = '';

            try {
                const response = await fetch('/api/media/text-to-speech/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': this.getCsrfToken()
                    },
                    body: JSON.stringify({
                        text: this.voiceText,
                        voice: this.voiceName,
                        speed: parseFloat(this.voiceSpeed),
                    })
                });

                if (!response.ok) {
                    const data = await response.json();
                    this.error = data.error || 'Failed to generate voice.';
                    this.processing = false;
                    return;
                }

                const blob = await response.blob();
                this.downloadUrl = URL.createObjectURL(blob);
                this.audioUrl = this.downloadUrl;
                this.downloadReady = true;

            } catch (e) {
                this.error = 'Network error. Please try again.';
            }
            this.processing = false;
        },

        async generateImagePrompt() {
            if (!this.imageDescription.trim()) return;
            this.processing = true;
            this.error = '';
            this.generatedPrompt = '';

            try {
                const response = await fetch('/api/media/ai-image/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': this.getCsrfToken()
                    },
                    body: JSON.stringify({ description: this.imageDescription })
                });

                const data = await response.json();
                if (!response.ok) {
                    this.error = data.error || 'Failed to generate prompt.';
                } else {
                    this.generatedPrompt = data.prompt;
                }

            } catch (e) {
                this.error = 'Network error. Please try again.';
            }
            this.processing = false;
        },

        copyPrompt() {
            if (this.generatedPrompt) {
                navigator.clipboard.writeText(this.generatedPrompt);
            }
        },

        getCsrfToken() {
            const el = document.querySelector('[name=csrfmiddlewaretoken]');
            if (el) return el.value;
            const match = document.cookie.match(/csrftoken=([^;]+)/);
            return match ? match[1] : '';
        }
    };
}
