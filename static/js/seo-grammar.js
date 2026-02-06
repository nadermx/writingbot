/**
 * SEO Grammar Checker Landing Page component.
 * Reuses the grammar checker API endpoint with a simplified UI for SEO landing pages.
 */
function seoGrammarChecker() {
    return {
        text: '',
        corrections: [],
        loading: false,
        fixingAll: false,
        hasChecked: false,
        errorMessage: null,
        highlightedHtml: '',

        init() {
            this.$watch('corrections', () => this.updateHighlights());
            this.$watch('text', () => {
                if (this.corrections.length > 0) {
                    this.updateHighlights();
                }
            });
        },

        get wordCount() {
            if (!this.text.trim()) return 0;
            return this.text.trim().split(/\s+/).length;
        },

        get groupedCorrections() {
            var groups = {};
            this.corrections.forEach(function(c) {
                var type = c.type || 'other';
                if (!groups[type]) {
                    groups[type] = { type: type, items: [] };
                }
                groups[type].items.push(c);
            });

            var order = ['grammar', 'spelling', 'punctuation', 'style', 'clarity', 'wordiness', 'passive_voice', 'other'];
            return order
                .filter(function(t) { return groups[t]; })
                .map(function(t) { return groups[t]; });
        },

        onTextInput() {
            // Clear stale state on significant text changes
        },

        getCSRFToken() {
            var el = document.querySelector('[name=csrfmiddlewaretoken]');
            if (el) return el.value;
            var match = document.cookie.match(/csrftoken=([^;]+)/);
            return match ? match[1] : '';
        },

        checkGrammar() {
            var self = this;
            if (!self.text.trim() || self.loading) return;

            self.loading = true;
            self.errorMessage = null;

            fetch('/api/grammar/check/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': self.getCSRFToken()
                },
                body: JSON.stringify({
                    text: self.text,
                    dialect: 'en-us'
                })
            })
            .then(function(response) {
                return response.json().then(function(data) {
                    return { ok: response.ok, data: data };
                });
            })
            .then(function(result) {
                self.loading = false;
                self.hasChecked = true;

                if (!result.ok) {
                    self.errorMessage = result.data.error || 'An error occurred';
                    return;
                }

                self.corrections = result.data.corrections || [];
                self.updateHighlights();
            })
            .catch(function(err) {
                self.loading = false;
                self.errorMessage = 'Network error. Please try again.';
                console.error('Grammar check error:', err);
            });
        },

        fixAll() {
            var self = this;
            if (!self.corrections.length || self.fixingAll) return;

            self.fixingAll = true;
            self.errorMessage = null;

            fetch('/api/grammar/fix/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': self.getCSRFToken()
                },
                body: JSON.stringify({
                    text: self.text,
                    corrections: self.corrections,
                    mode: 'all'
                })
            })
            .then(function(response) {
                return response.json().then(function(data) {
                    return { ok: response.ok, data: data };
                });
            })
            .then(function(result) {
                self.fixingAll = false;

                if (!result.ok) {
                    self.errorMessage = result.data.error || 'An error occurred';
                    return;
                }

                self.text = result.data.fixed_text || self.text;
                self.corrections = [];
                self.highlightedHtml = '';
            })
            .catch(function(err) {
                self.fixingAll = false;
                self.errorMessage = 'Network error. Please try again.';
                console.error('Fix all error:', err);
            });
        },

        applySingle(correction) {
            var self = this;
            self.errorMessage = null;

            fetch('/api/grammar/fix/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': self.getCSRFToken()
                },
                body: JSON.stringify({
                    text: self.text,
                    correction: correction,
                    mode: 'single'
                })
            })
            .then(function(response) {
                return response.json().then(function(data) {
                    return { ok: response.ok, data: data };
                });
            })
            .then(function(result) {
                if (!result.ok) {
                    self.errorMessage = result.data.error || 'An error occurred';
                    return;
                }

                self.text = result.data.fixed_text || self.text;

                // Remove the applied correction
                self.corrections = self.corrections.filter(function(c) {
                    return c !== correction;
                });
                self.updateHighlights();
            })
            .catch(function(err) {
                self.errorMessage = 'Network error. Please try again.';
                console.error('Fix single error:', err);
            });
        },

        updateHighlights() {
            if (!this.corrections.length || !this.text) {
                this.highlightedHtml = '';
                return;
            }

            var sorted = this.corrections.slice().sort(function(a, b) {
                var aStart = (a.position && a.position.start) || 0;
                var bStart = (b.position && b.position.start) || 0;
                return aStart - bStart;
            });

            var html = '';
            var lastEnd = 0;
            var text = this.text;

            sorted.forEach(function(c) {
                var start = (c.position && c.position.start) || 0;
                var end = (c.position && c.position.end) || 0;

                if (start < lastEnd || start >= text.length) return;

                html += seoEscapeHtml(text.substring(lastEnd, start));

                var typeColor = seoGetErrorColor(c.type);
                html += '<mark style="background-color: ' + typeColor + '; border-radius: 2px; padding: 0 1px;">';
                html += seoEscapeHtml(text.substring(start, end));
                html += '</mark>';

                lastEnd = end;
            });

            html += seoEscapeHtml(text.substring(lastEnd));

            this.highlightedHtml = html;
        },

        formatType(type) {
            return type.replace(/_/g, ' ');
        },

        getTypeBadgeClass(type) {
            var classes = {
                grammar: 'bg-danger',
                spelling: 'bg-warning text-dark',
                punctuation: 'bg-info',
                style: 'bg-secondary',
                clarity: 'bg-primary',
                wordiness: 'bg-dark',
                passive_voice: 'bg-secondary'
            };
            return classes[type] || 'bg-secondary';
        }
    };
}

function seoEscapeHtml(text) {
    var div = document.createElement('div');
    div.appendChild(document.createTextNode(text));
    return div.innerHTML;
}

function seoGetErrorColor(type) {
    var colors = {
        grammar: 'rgba(239, 68, 68, 0.25)',
        spelling: 'rgba(234, 179, 8, 0.3)',
        punctuation: 'rgba(59, 130, 246, 0.25)',
        style: 'rgba(107, 114, 128, 0.25)',
        clarity: 'rgba(139, 92, 246, 0.25)',
        wordiness: 'rgba(249, 115, 22, 0.25)',
        passive_voice: 'rgba(156, 163, 175, 0.25)'
    };
    return colors[type] || 'rgba(239, 68, 68, 0.2)';
}
