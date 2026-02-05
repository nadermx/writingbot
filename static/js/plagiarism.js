function plagiarismApp() {
    var defaultUsage = window.__plagiarismUsage || { words_used: 0, words_limit: 30000, words_remaining: 30000 };

    return {
        inputText: '',
        wordCount: 0,
        checking: false,
        result: null,
        errorMsg: '',
        usage: defaultUsage,

        get usagePercent() {
            if (!this.usage || !this.usage.words_limit) return 0;
            return Math.min(100, Math.round((this.usage.words_used / this.usage.words_limit) * 100));
        },

        get gaugeColor() {
            if (!this.result) return '#198754';
            var pct = this.result.similarity_percentage;
            if (pct <= 10) return '#198754';   // green
            if (pct <= 30) return '#ffc107';   // yellow
            return '#dc3545';                   // red
        },

        get highlightedText() {
            if (!this.result || !this.result.matches || this.result.matches.length === 0) {
                return this.escapeHtml(this.inputText);
            }

            var text = this.inputText;
            var highlighted = this.escapeHtml(text);

            // Highlight matched text portions
            for (var i = 0; i < this.result.matches.length; i++) {
                var match = this.result.matches[i];
                var matchedText = match.matched_text;
                if (!matchedText) continue;

                // Find the best matching portion in the input text
                var segments = this.findBestOverlap(text, matchedText);
                for (var j = 0; j < segments.length; j++) {
                    var seg = this.escapeHtml(segments[j]);
                    if (seg.length > 20) {
                        highlighted = highlighted.replace(
                            seg,
                            '<mark class="bg-warning bg-opacity-50" title="Source: ' +
                            this.escapeHtml(match.title || match.source_url) + '">' + seg + '</mark>'
                        );
                    }
                }
            }

            return highlighted;
        },

        getCSRFToken() {
            var token = document.querySelector('[name=csrfmiddlewaretoken]');
            if (token) return token.value;
            var cookie = document.cookie.split(';').find(function(c) {
                return c.trim().startsWith('csrftoken=');
            });
            return cookie ? cookie.split('=')[1] : '';
        },

        escapeHtml(text) {
            if (!text) return '';
            var div = document.createElement('div');
            div.appendChild(document.createTextNode(text));
            return div.innerHTML;
        },

        findBestOverlap(source, matchedText) {
            // Find words from matchedText that appear as sequences in source
            var results = [];
            var matchWords = matchedText.toLowerCase().split(/\s+/);
            var sourceWords = source.toLowerCase().split(/\s+/);
            var originalWords = source.split(/\s+/);

            // Sliding window to find matching sequences
            for (var i = 0; i < sourceWords.length; i++) {
                var matchCount = 0;
                for (var j = 0; j < matchWords.length && (i + j) < sourceWords.length; j++) {
                    if (sourceWords[i + j] === matchWords[j]) {
                        matchCount++;
                    }
                }
                if (matchCount >= 4) {
                    var segment = originalWords.slice(i, i + matchCount).join(' ');
                    if (segment.length > 20) {
                        results.push(segment);
                    }
                }
            }

            return results;
        },

        updateWordCount() {
            var text = this.inputText.trim();
            this.wordCount = text ? text.split(/\s+/).length : 0;
        },

        handleFileUpload(event) {
            var file = event.target.files[0];
            if (!file) return;

            // Only handle text files
            if (file.type === 'text/plain' || file.name.endsWith('.txt')) {
                var reader = new FileReader();
                var self = this;
                reader.onload = function(e) {
                    self.inputText = e.target.result;
                    self.updateWordCount();
                };
                reader.readAsText(file);
            } else {
                this.errorMsg = 'Currently only .txt files are supported for upload. Please paste your text directly for other formats.';
            }

            // Reset file input
            event.target.value = '';
        },

        async checkPlagiarism() {
            if (this.wordCount < 15) {
                this.errorMsg = 'Please provide at least 15 words to check.';
                return;
            }

            this.checking = true;
            this.errorMsg = '';
            this.result = null;

            try {
                var response = await fetch('/api/plagiarism/check/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': this.getCSRFToken(),
                    },
                    body: JSON.stringify({ text: this.inputText }),
                });

                var data = await response.json();

                if (!response.ok) {
                    this.errorMsg = data.error || 'An error occurred during the plagiarism check.';
                    return;
                }

                this.result = data;

                // Update usage from response
                if (data.usage) {
                    this.usage = data.usage;
                }
            } catch (err) {
                this.errorMsg = 'An error occurred while checking for plagiarism. Please try again.';
            } finally {
                this.checking = false;
            }
        },

        exportReport() {
            if (!this.result) return;

            var lines = [];
            lines.push('PLAGIARISM CHECK REPORT');
            lines.push('======================');
            lines.push('');
            lines.push('Overall Similarity: ' + this.result.similarity_percentage + '%');
            lines.push('Words Checked: ' + this.result.word_count);
            lines.push('Sources Found: ' + this.result.matches.length);
            lines.push('');
            lines.push('---');
            lines.push('');

            if (this.result.matches.length > 0) {
                lines.push('MATCHED SOURCES:');
                lines.push('');
                for (var i = 0; i < this.result.matches.length; i++) {
                    var match = this.result.matches[i];
                    lines.push((i + 1) + '. ' + (match.title || 'Untitled'));
                    lines.push('   URL: ' + match.source_url);
                    lines.push('   Similarity: ' + match.similarity_percent + '%');
                    lines.push('   Matched text: ' + match.matched_text.substring(0, 200));
                    lines.push('');
                }
            } else {
                lines.push('No matching sources found. The text appears to be original.');
            }

            lines.push('---');
            lines.push('');
            lines.push('ORIGINAL TEXT:');
            lines.push('');
            lines.push(this.inputText);

            var content = lines.join('\n');
            var blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
            var url = URL.createObjectURL(blob);
            var a = document.createElement('a');
            a.href = url;
            a.download = 'plagiarism-report.txt';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        },
    };
}
