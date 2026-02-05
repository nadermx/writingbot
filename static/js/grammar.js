function grammarChecker() {
    return {
        text: '',
        dialect: 'en-us',
        corrections: [],
        scores: {
            grammar: 0,
            fluency: 0,
            clarity: 0,
            engagement: 0,
            delivery: 0
        },
        tone: 'neutral',
        readabilityScore: null,
        loading: false,
        fixingAll: false,
        hasChecked: false,
        hasScores: false,
        errorMessage: null,
        highlightedHtml: '',

        scoreLabels: {
            grammar: 'Grammar',
            fluency: 'Fluency',
            clarity: 'Clarity',
            engagement: 'Engagement',
            delivery: 'Delivery'
        },

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

        get charCount() {
            return this.text.length;
        },

        get tonePosition() {
            var toneMap = {
                'formal': 5,
                'semi-formal': 25,
                'neutral': 50,
                'semi-casual': 75,
                'casual': 95
            };
            return toneMap[this.tone] || 50;
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

            // Sort: grammar first, then spelling, punctuation, etc.
            var order = ['grammar', 'spelling', 'punctuation', 'style', 'clarity', 'wordiness', 'passive_voice', 'other'];
            return order
                .filter(function(t) { return groups[t]; })
                .map(function(t) { return groups[t]; });
        },

        onTextInput() {
            // Clear corrections when text changes significantly
            // (keeps corrections if small edit)
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
                    dialect: self.dialect
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
                self.scores = result.data.writing_scores || self.scores;
                self.tone = result.data.tone || 'neutral';
                self.readabilityScore = result.data.readability_score || null;
                self.hasScores = true;
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

            // Sort corrections by position start ascending
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

                // Text before this error
                html += escapeHtml(text.substring(lastEnd, start));

                // Highlighted error
                var typeColor = getErrorColor(c.type);
                html += '<mark style="background-color: ' + typeColor + '; border-radius: 2px; padding: 0 1px;">';
                html += escapeHtml(text.substring(start, end));
                html += '</mark>';

                lastEnd = end;
            });

            // Remaining text
            html += escapeHtml(text.substring(lastEnd));

            this.highlightedHtml = html;
        },

        scrollToError(correction) {
            // Focus the textarea and set cursor position
            var textarea = this.$el.querySelector('textarea');
            if (textarea && correction.position) {
                textarea.focus();
                textarea.setSelectionRange(correction.position.start, correction.position.end);
            }
        },

        getScoreColor(score) {
            if (score >= 80) return '#22c55e';
            if (score >= 60) return '#eab308';
            if (score >= 40) return '#f97316';
            return '#ef4444';
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

function escapeHtml(text) {
    var div = document.createElement('div');
    div.appendChild(document.createTextNode(text));
    return div.innerHTML;
}

function getErrorColor(type) {
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
