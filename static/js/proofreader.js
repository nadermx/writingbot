function proofreaderApp() {
    return {
        // Input state
        inputMode: 'paste',
        text: '',
        selectedFile: null,
        dragOver: false,

        // UI state
        loading: false,
        downloading: false,
        hasResult: false,
        errorMessage: null,
        copied: false,
        viewMode: 'corrected',
        filterType: 'all',

        // Result data
        result: {
            overall_score: 0,
            summary: '',
            error_counts: {},
            total_errors: 0,
            corrections: [],
            corrected_text: '',
            original_text: '',
            word_count: 0
        },

        // Category definitions
        errorCategories: [
            { key: 'grammar', label: 'Grammar', color: '#ef4444' },
            { key: 'spelling', label: 'Spelling', color: '#eab308' },
            { key: 'punctuation', label: 'Punctuation', color: '#3b82f6' },
            { key: 'style', label: 'Style', color: '#8b5cf6' },
            { key: 'clarity', label: 'Clarity', color: '#06b6d4' },
            { key: 'wordiness', label: 'Wordiness', color: '#f97316' }
        ],

        init() {
            // Nothing special needed on init
        },

        get wordCount() {
            if (!this.text.trim()) return 0;
            return this.text.trim().split(/\s+/).length;
        },

        get filteredCorrections() {
            if (!this.result.corrections) return [];
            if (this.filterType === 'all') return this.result.corrections;
            return this.result.corrections.filter(function(c) {
                return c.type === this.filterType;
            }.bind(this));
        },

        getCSRFToken() {
            var el = document.querySelector('[name=csrfmiddlewaretoken]');
            if (el) return el.value;
            var match = document.cookie.match(/csrftoken=([^;]+)/);
            return match ? match[1] : '';
        },

        handleFileSelect(event) {
            var files = event.target.files;
            if (files && files.length > 0) {
                this.selectedFile = files[0];
                this.errorMessage = null;
            }
        },

        handleDrop(event) {
            this.dragOver = false;
            var files = event.dataTransfer.files;
            if (files && files.length > 0) {
                var file = files[0];
                var name = file.name.toLowerCase();
                if (name.endsWith('.docx') || name.endsWith('.txt') || name.endsWith('.pdf')) {
                    this.selectedFile = file;
                    this.errorMessage = null;
                } else {
                    this.errorMessage = 'Unsupported file type. Please upload a DOCX, TXT, or PDF file.';
                }
            }
        },

        clearFile() {
            this.selectedFile = null;
            if (this.$refs.fileInput) {
                this.$refs.fileInput.value = '';
            }
        },

        formatFileSize(bytes) {
            if (bytes < 1024) return bytes + ' B';
            if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
            return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
        },

        proofread() {
            var self = this;
            if (self.loading) return;

            // Validate input
            if (self.inputMode === 'paste' && !self.text.trim()) {
                self.errorMessage = 'Please paste some text to proofread.';
                return;
            }
            if (self.inputMode === 'upload' && !self.selectedFile) {
                self.errorMessage = 'Please select a document to upload.';
                return;
            }

            self.loading = true;
            self.errorMessage = null;

            var formData = new FormData();

            if (self.inputMode === 'upload' && self.selectedFile) {
                formData.append('file', self.selectedFile);
            } else {
                formData.append('text', self.text);
            }

            fetch('/api/proofread/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': self.getCSRFToken()
                },
                body: formData
            })
            .then(function(response) {
                return response.json().then(function(data) {
                    return { ok: response.ok, data: data };
                });
            })
            .then(function(res) {
                self.loading = false;

                if (!res.ok) {
                    self.errorMessage = res.data.error || 'An error occurred during proofreading.';
                    if (res.data.upgrade) {
                        self.errorMessage += ' Upgrade to Premium for unlimited proofreading.';
                    }
                    return;
                }

                self.result = res.data;
                self.hasResult = true;
                self.viewMode = 'corrected';
                self.filterType = 'all';

                // Scroll to top of results
                window.scrollTo({ top: 0, behavior: 'smooth' });
            })
            .catch(function(err) {
                self.loading = false;
                self.errorMessage = 'Network error. Please check your connection and try again.';
                console.error('Proofread error:', err);
            });
        },

        downloadCorrected(format) {
            var self = this;
            if (self.downloading || !self.result.corrected_text) return;

            self.downloading = true;

            fetch('/api/proofread/download/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': self.getCSRFToken()
                },
                body: JSON.stringify({
                    corrected_text: self.result.corrected_text,
                    format: format
                })
            })
            .then(function(response) {
                if (!response.ok) {
                    return response.json().then(function(data) {
                        throw new Error(data.error || 'Download failed');
                    });
                }
                return response.blob();
            })
            .then(function(blob) {
                self.downloading = false;
                var ext = format === 'txt' ? 'txt' : 'docx';
                var url = window.URL.createObjectURL(blob);
                var a = document.createElement('a');
                a.href = url;
                a.download = 'proofread_document.' + ext;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);
            })
            .catch(function(err) {
                self.downloading = false;
                self.errorMessage = err.message || 'Failed to download the document.';
                console.error('Download error:', err);
            });
        },

        copyCorrected() {
            var self = this;
            if (!self.result.corrected_text) return;

            navigator.clipboard.writeText(self.result.corrected_text).then(function() {
                self.copied = true;
                setTimeout(function() { self.copied = false; }, 2000);
            }).catch(function() {
                // Fallback for older browsers
                var textarea = document.createElement('textarea');
                textarea.value = self.result.corrected_text;
                textarea.style.position = 'fixed';
                textarea.style.opacity = '0';
                document.body.appendChild(textarea);
                textarea.select();
                document.execCommand('copy');
                document.body.removeChild(textarea);
                self.copied = true;
                setTimeout(function() { self.copied = false; }, 2000);
            });
        },

        resetAll() {
            this.hasResult = false;
            this.result = {
                overall_score: 0,
                summary: '',
                error_counts: {},
                total_errors: 0,
                corrections: [],
                corrected_text: '',
                original_text: '',
                word_count: 0
            };
            this.errorMessage = null;
            this.filterType = 'all';
            this.viewMode = 'corrected';
            this.copied = false;
        },

        getScoreColor(score) {
            if (score >= 80) return '#22c55e';
            if (score >= 60) return '#eab308';
            if (score >= 40) return '#f97316';
            return '#ef4444';
        },

        getScoreLabel(score) {
            if (score >= 90) return 'Excellent';
            if (score >= 80) return 'Very Good';
            if (score >= 70) return 'Good';
            if (score >= 60) return 'Fair';
            if (score >= 40) return 'Needs Improvement';
            return 'Poor';
        },

        getCategoryColor(type) {
            var map = {
                grammar: '#ef4444',
                spelling: '#eab308',
                punctuation: '#3b82f6',
                style: '#8b5cf6',
                clarity: '#06b6d4',
                wordiness: '#f97316'
            };
            return map[type] || '#6b7280';
        }
    };
}
