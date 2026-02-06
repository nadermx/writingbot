function summarizerApp() {
    return {
        text: '',
        mode: 'paragraph',
        summaryLength: 3,
        showBullets: true,
        summary: '',
        sentences: [],
        stats: {
            original_words: 0,
            summary_words: 0,
            reduction_percent: 0,
            sentence_count: 0
        },
        loading: false,
        copied: false,
        errorMessage: null,
        inputWordCount: 0,

        // Custom mode
        customInstructions: '',

        // Keywords
        keywords: [],
        keywordInput: '',

        init() {
            this.$watch('text', () => this.updateWordCount());
        },

        updateWordCount() {
            if (!this.text.trim()) {
                this.inputWordCount = 0;
                return;
            }
            this.inputWordCount = this.text.trim().split(/\s+/).length;
        },

        addKeyword() {
            var kw = this.keywordInput.trim().replace(/,$/,'').trim();
            if (kw && this.keywords.indexOf(kw) === -1 && this.keywords.length < 20) {
                this.keywords.push(kw);
            }
            this.keywordInput = '';
        },

        removeKeyword(idx) {
            this.keywords.splice(idx, 1);
        },

        showUpgradeForCustom() {
            this.errorMessage = 'Custom mode is available for Premium users only. Upgrade to unlock custom summarization instructions.';
        },

        clearInput() {
            this.text = '';
            this.summary = '';
            this.sentences = [];
            this.stats = { original_words: 0, summary_words: 0, reduction_percent: 0, sentence_count: 0 };
            this.inputWordCount = 0;
        },

        getCSRFToken() {
            var el = document.querySelector('[name=csrfmiddlewaretoken]');
            if (el) return el.value;
            var match = document.cookie.match(/csrftoken=([^;]+)/);
            return match ? match[1] : '';
        },

        summarize() {
            var self = this;
            if (!self.text.trim() || self.loading) return;

            // Validate custom mode has instructions
            if (self.mode === 'custom' && !self.customInstructions.trim()) {
                self.errorMessage = 'Please provide custom instructions for custom mode.';
                return;
            }

            self.loading = true;
            self.errorMessage = null;
            self.summary = '';
            self.sentences = [];

            var payload = {
                text: self.text,
                mode: self.mode,
                length: self.summaryLength
            };

            // Add custom instructions for custom mode
            if (self.mode === 'custom' && self.customInstructions.trim()) {
                payload.custom_instructions = self.customInstructions.trim();
            }

            // Add keywords if any
            if (self.keywords.length > 0) {
                payload.keywords = self.keywords;
            }

            fetch('/api/summarize/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': self.getCSRFToken()
                },
                body: JSON.stringify(payload)
            })
            .then(function(response) {
                return response.json().then(function(data) {
                    return { ok: response.ok, data: data };
                });
            })
            .then(function(result) {
                self.loading = false;

                if (!result.ok) {
                    self.errorMessage = result.data.error || 'An error occurred';
                    return;
                }

                self.summary = result.data.summary || '';
                self.sentences = result.data.sentences || [];
                self.stats = result.data.stats || self.stats;
            })
            .catch(function(err) {
                self.loading = false;
                self.errorMessage = 'Network error. Please try again.';
                console.error('Summarize error:', err);
            });
        },

        copySummary() {
            var self = this;
            if (!self.summary) return;

            var textToCopy = self.summary;

            // For key_sentences mode with bullets, format as bullet list
            if (self.mode === 'key_sentences' && self.sentences.length > 0 && self.showBullets) {
                textToCopy = self.sentences.map(function(s) { return '- ' + s; }).join('\n');
            }

            navigator.clipboard.writeText(textToCopy).then(function() {
                self.copied = true;
                setTimeout(function() {
                    self.copied = false;
                }, 2000);
            }).catch(function() {
                // Fallback for older browsers
                var textarea = document.createElement('textarea');
                textarea.value = textToCopy;
                document.body.appendChild(textarea);
                textarea.select();
                document.execCommand('copy');
                document.body.removeChild(textarea);
                self.copied = true;
                setTimeout(function() {
                    self.copied = false;
                }, 2000);
            });
        }
    };
}
