function aiToolApp() {
    return {
        params: {},
        output: '',
        error: '',
        loading: false,
        copied: false,
        remaining: parseInt(document.querySelector('[x-text="remaining"]')?.textContent || '-1'),
        wordCount: 0,

        init() {
            // Initialize params from form fields
            const form = document.getElementById('toolForm');
            if (form) {
                form.querySelectorAll('input, textarea, select').forEach(el => {
                    if (el.name) {
                        this.params[el.name] = el.value || '';
                    }
                });
            }
        },

        async generate() {
            this.error = '';
            this.loading = true;

            // Get tool slug from URL
            const pathParts = window.location.pathname.split('/').filter(Boolean);
            const toolSlug = pathParts[pathParts.length - 1];

            // Build request body
            const body = { tool: toolSlug, ...this.params };

            try {
                const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value
                    || document.querySelector('meta[name="csrf-token"]')?.content
                    || '';

                const response = await fetch('/api/ai-tools/generate/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken,
                    },
                    body: JSON.stringify(body),
                });

                const data = await response.json();

                if (!response.ok) {
                    this.error = data.error || 'An error occurred. Please try again.';
                    if (data.upgrade) {
                        this.error += ' <a href="/pricing/" class="alert-link">Upgrade to Premium</a>';
                    }
                    return;
                }

                this.output = data.output || '';
                this.wordCount = this.output.split(/\s+/).filter(w => w).length;

                // Decrement remaining counter
                if (this.remaining > 0) {
                    this.remaining--;
                }

            } catch (err) {
                this.error = 'Network error. Please check your connection and try again.';
            } finally {
                this.loading = false;
            }
        },

        formatOutput(text) {
            if (!text) return '';
            // Basic markdown-like formatting
            let html = text
                // Escape HTML
                .replace(/&/g, '&amp;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;')
                // Bold
                .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                // Italic
                .replace(/\*(.*?)\*/g, '<em>$1</em>')
                // Headers
                .replace(/^### (.*?)$/gm, '<h3>$1</h3>')
                .replace(/^## (.*?)$/gm, '<h2>$1</h2>')
                .replace(/^# (.*?)$/gm, '<h1>$1</h1>')
                // Line breaks
                .replace(/\n\n/g, '</p><p>')
                .replace(/\n/g, '<br>');

            return '<p>' + html + '</p>';
        },

        async copyOutput() {
            try {
                await navigator.clipboard.writeText(this.output);
                this.copied = true;
                setTimeout(() => { this.copied = false; }, 2000);
            } catch (err) {
                // Fallback
                const textarea = document.createElement('textarea');
                textarea.value = this.output;
                document.body.appendChild(textarea);
                textarea.select();
                document.execCommand('copy');
                document.body.removeChild(textarea);
                this.copied = true;
                setTimeout(() => { this.copied = false; }, 2000);
            }
        },
    };
}
