/**
 * Media Tools Alpine.js component.
 * Handles image conversion, background removal, QR codes, voice generation,
 * transcription, logo generation, character generation, word clouds,
 * banner generation, and presentation creation.
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

        // AI result (shared for text-returning tools)
        aiResult: '',

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

        // Logo generator
        logoBusinessName: '',
        logoIndustry: '',
        logoStyle: 'modern',
        logoColors: '',
        logoAdditional: '',

        // Character generator
        charName: '',
        charTraits: '',
        charStyle: 'concept',
        charGender: '',
        charAge: '',
        charAdditional: '',

        // Word cloud
        wcText: '',
        wcWidth: '800',
        wcHeight: '400',
        wcBgColor: 'white',
        wcColormap: 'viridis',
        wcMaxWords: '200',

        // Banner generator
        bannerTitle: '',
        bannerSubtitle: '',
        bannerCta: '',
        bannerSize: '1200x628',
        bannerStyle: '',
        bannerColors: '',
        bannerAdditional: '',

        // Presentation maker
        presTopic: '',
        presSlides: 10,
        presStyle: 'professional',
        presAudience: '',
        presAdditional: '',

        init() {
            // Detect tool type from URL
            const path = window.location.pathname;
            if (path.includes('image-converter') || path.includes('converter-tools')) this.toolType = 'image-converter';
            else if (path.includes('background-remover')) this.toolType = 'background-remover';
            else if (path.includes('qr-code')) this.toolType = 'qr-code';
            else if (path.includes('ai-voice')) this.toolType = 'voice-generator';
            else if (path.includes('transcription') || path.includes('speech-to-text')) this.toolType = 'transcription';
            else if (path.includes('logo-generator')) this.toolType = 'logo-generator';
            else if (path.includes('character-generator')) this.toolType = 'character-generator';
            else if (path.includes('word-cloud')) this.toolType = 'word-cloud';
            else if (path.includes('banner-generator')) this.toolType = 'banner-generator';
            else if (path.includes('presentation-maker')) this.toolType = 'presentation-maker';
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
            this.aiResult = '';

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
            this.aiResult = '';
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

        async transcribeAudio() {
            if (!this.file) return;
            this.processing = true;
            this.error = '';
            this.aiResult = '';

            try {
                const formData = new FormData();
                formData.append('file', this.file);

                const response = await fetch('/api/media/transcribe/', {
                    method: 'POST',
                    headers: { 'X-CSRFToken': this.getCsrfToken() },
                    body: formData
                });

                const data = await response.json();
                if (!response.ok) {
                    this.error = data.error || 'Failed to transcribe audio.';
                } else {
                    this.aiResult = data.result;
                }

            } catch (e) {
                this.error = 'Network error. Please try again.';
            }
            this.processing = false;
        },

        async generateLogo() {
            if (!this.logoBusinessName.trim()) return;
            this.processing = true;
            this.error = '';
            this.aiResult = '';

            try {
                const response = await fetch('/api/media/logo/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': this.getCsrfToken()
                    },
                    body: JSON.stringify({
                        business_name: this.logoBusinessName,
                        industry: this.logoIndustry,
                        style: this.logoStyle,
                        colors: this.logoColors,
                        additional: this.logoAdditional,
                    })
                });

                const data = await response.json();
                if (!response.ok) {
                    this.error = data.error || 'Failed to generate logo design.';
                } else {
                    this.aiResult = data.result;
                }

            } catch (e) {
                this.error = 'Network error. Please try again.';
            }
            this.processing = false;
        },

        async generateCharacter() {
            if (!this.charTraits.trim()) return;
            this.processing = true;
            this.error = '';
            this.aiResult = '';

            try {
                const response = await fetch('/api/media/character/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': this.getCsrfToken()
                    },
                    body: JSON.stringify({
                        name: this.charName,
                        traits: this.charTraits,
                        style: this.charStyle,
                        gender: this.charGender,
                        age: this.charAge,
                        additional: this.charAdditional,
                    })
                });

                const data = await response.json();
                if (!response.ok) {
                    this.error = data.error || 'Failed to generate character.';
                } else {
                    this.aiResult = data.result;
                }

            } catch (e) {
                this.error = 'Network error. Please try again.';
            }
            this.processing = false;
        },

        async generateWordCloud() {
            if (!this.wcText.trim()) return;
            this.processing = true;
            this.error = '';
            this.downloadReady = false;

            try {
                const response = await fetch('/api/media/word-cloud/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': this.getCsrfToken()
                    },
                    body: JSON.stringify({
                        text: this.wcText,
                        width: parseInt(this.wcWidth),
                        height: parseInt(this.wcHeight),
                        bg_color: this.wcBgColor,
                        colormap: this.wcColormap,
                        max_words: parseInt(this.wcMaxWords),
                    })
                });

                if (!response.ok) {
                    const ct = response.headers.get('content-type') || '';
                    if (ct.includes('application/json')) {
                        const data = await response.json();
                        this.error = data.error || 'Failed to generate word cloud.';
                    } else {
                        this.error = 'An error occurred while generating the word cloud.';
                    }
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

        async generateBanner() {
            if (!this.bannerTitle.trim()) return;
            this.processing = true;
            this.error = '';
            this.aiResult = '';

            try {
                const response = await fetch('/api/media/banner/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': this.getCsrfToken()
                    },
                    body: JSON.stringify({
                        title: this.bannerTitle,
                        subtitle: this.bannerSubtitle,
                        cta: this.bannerCta,
                        size: this.bannerSize,
                        style: this.bannerStyle,
                        brand_colors: this.bannerColors,
                        additional: this.bannerAdditional,
                    })
                });

                const data = await response.json();
                if (!response.ok) {
                    this.error = data.error || 'Failed to generate banner design.';
                } else {
                    this.aiResult = data.result;
                }

            } catch (e) {
                this.error = 'Network error. Please try again.';
            }
            this.processing = false;
        },

        async generatePresentation() {
            if (!this.presTopic.trim()) return;
            this.processing = true;
            this.error = '';
            this.aiResult = '';

            try {
                const response = await fetch('/api/media/presentation/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': this.getCsrfToken()
                    },
                    body: JSON.stringify({
                        topic: this.presTopic,
                        num_slides: parseInt(this.presSlides),
                        style: this.presStyle,
                        audience: this.presAudience,
                        additional: this.presAdditional,
                    })
                });

                const data = await response.json();
                if (!response.ok) {
                    this.error = data.error || 'Failed to generate presentation.';
                } else {
                    this.aiResult = data.result;
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

        copyResult() {
            if (this.aiResult) {
                navigator.clipboard.writeText(this.aiResult);
            }
        },

        /**
         * Basic markdown-to-HTML formatter for AI results.
         * Handles headings, bold, italic, bullet lists, and code blocks.
         */
        formatMarkdown(text) {
            if (!text) return '';
            let html = text
                // Escape HTML
                .replace(/&/g, '&amp;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;')
                // Code blocks
                .replace(/```([\s\S]*?)```/g, '<pre class="bg-dark text-light p-3 rounded my-2"><code>$1</code></pre>')
                // Inline code
                .replace(/`([^`]+)`/g, '<code class="bg-secondary bg-opacity-10 px-1 rounded">$1</code>')
                // Headers
                .replace(/^### (.+)$/gm, '<h5 class="fw-semibold mt-3 mb-1">$1</h5>')
                .replace(/^## (.+)$/gm, '<h4 class="fw-semibold mt-3 mb-1">$1</h4>')
                .replace(/^# (.+)$/gm, '<h3 class="fw-bold mt-3 mb-2">$1</h3>')
                // Bold + italic
                .replace(/\*\*\*(.+?)\*\*\*/g, '<strong><em>$1</em></strong>')
                // Bold
                .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
                // Italic
                .replace(/\*(.+?)\*/g, '<em>$1</em>')
                // Bullet lists
                .replace(/^[-*] (.+)$/gm, '<li>$1</li>')
                // Numbered lists
                .replace(/^\d+\. (.+)$/gm, '<li>$1</li>')
                // Wrap consecutive <li> in <ul>
                .replace(/((?:<li>.*<\/li>\n?)+)/g, '<ul class="mb-2">$1</ul>')
                // Paragraphs (double newline)
                .replace(/\n\n/g, '</p><p class="mb-2">')
                // Single newlines
                .replace(/\n/g, '<br>');
            return '<p class="mb-2">' + html + '</p>';
        },

        getCsrfToken() {
            const el = document.querySelector('[name=csrfmiddlewaretoken]');
            if (el) return el.value;
            const match = document.cookie.match(/csrftoken=([^;]+)/);
            return match ? match[1] : '';
        }
    };
}
