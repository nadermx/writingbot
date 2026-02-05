/**
 * AI Tools - Alpine.js component for the generator UI.
 * Handles form submission, API calls, output display, and copy functionality.
 */
function aiToolApp() {
    return {
        params: { tone: '' },
        output: '',
        error: '',
        loading: false,
        copied: false,
        showUpgrade: false,
        remaining: parseInt(document.querySelector('[x-text="remaining"]')?.textContent || '-1'),
        wordCount: 0,

        init() {
            // Initialize params from form fields
            var form = document.getElementById('toolForm');
            if (form) {
                form.querySelectorAll('input, textarea, select').forEach(function(el) {
                    if (el.name && el.name !== 'csrfmiddlewaretoken') {
                        this.params[el.name] = el.value || '';
                    }
                }.bind(this));
            }
        },

        async generate() {
            this.error = '';
            this.showUpgrade = false;
            this.loading = true;

            // Get tool slug from URL path
            var pathParts = window.location.pathname.split('/').filter(Boolean);
            var toolSlug = pathParts[pathParts.length - 1];

            // Build request payload
            var payload = { tool: toolSlug };
            for (var key in this.params) {
                if (this.params.hasOwnProperty(key) && this.params[key] !== undefined && this.params[key] !== null) {
                    payload[key] = this.params[key];
                }
            }

            // CSRF token
            var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';

            try {
                var response = await fetch('/api/ai-tools/generate/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken,
                    },
                    body: JSON.stringify(payload),
                });

                var data = await response.json();

                if (!response.ok) {
                    this.error = data.error || 'An error occurred. Please try again.';
                    if (data.upgrade) {
                        this.showUpgrade = true;
                    }
                    return;
                }

                this.output = data.output || '';
                this.wordCount = this.countWords(this.output);

                // Update remaining counter from server response
                if (data.remaining !== undefined && data.remaining >= 0) {
                    this.remaining = data.remaining;
                }

            } catch (err) {
                this.error = 'Network error. Please check your connection and try again.';
            } finally {
                this.loading = false;
            }
        },

        formatOutput(text) {
            if (!text) return '';

            // Escape HTML first
            var html = text
                .replace(/&/g, '&amp;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;');

            // Convert markdown headings
            html = html.replace(/^### (.*?)$/gm, '<strong>$1</strong>');
            html = html.replace(/^## (.*?)$/gm, '<strong style="font-size:1.05em;">$1</strong>');
            html = html.replace(/^# (.*?)$/gm, '<strong style="font-size:1.1em;">$1</strong>');

            // Convert bold and italic
            html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
            html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');

            // Convert markdown bullet lists
            html = html.replace(/^- (.+)$/gm, '&bull; $1');
            html = html.replace(/^\* (.+)$/gm, '&bull; $1');

            // Paragraphs and line breaks
            html = html.replace(/\n\n/g, '</p><p>');
            html = html.replace(/\n/g, '<br>');

            return '<p>' + html + '</p>';
        },

        async copyOutput() {
            if (!this.output) return;

            try {
                await navigator.clipboard.writeText(this.output);
                this.copied = true;
                setTimeout(function() { this.copied = false; }.bind(this), 2000);
            } catch (err) {
                // Fallback for older browsers
                var textarea = document.createElement('textarea');
                textarea.value = this.output;
                textarea.style.position = 'fixed';
                textarea.style.opacity = '0';
                document.body.appendChild(textarea);
                textarea.select();
                document.execCommand('copy');
                document.body.removeChild(textarea);
                this.copied = true;
                setTimeout(function() { this.copied = false; }.bind(this), 2000);
            }
        },

        countWords(text) {
            if (!text || !text.trim()) return 0;
            return text.trim().split(/\s+/).length;
        },
    };
}
