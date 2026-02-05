function citationApp() {
    return {
        selectedStyle: 'apa',
        sourceType: 'website',
        sourceTypes: [
            { code: 'website', label: 'Website' },
            { code: 'book', label: 'Book' },
            { code: 'journal', label: 'Journal' },
            { code: 'article', label: 'Article' },
            { code: 'video', label: 'Video' },
            { code: 'podcast', label: 'Podcast' },
        ],
        form: {
            author: '',
            title: '',
            date: '',
            url: '',
            publisher: '',
            volume: '',
            issue: '',
            pages: '',
            doi: '',
            isbn: '',
            journal: '',
        },
        autociteUrl: '',
        autociting: false,
        generating: false,
        result: null,
        citationList: [],
        errorMsg: '',
        copied: '',

        getCSRFToken() {
            var token = document.querySelector('[name=csrfmiddlewaretoken]');
            if (token) return token.value;
            var cookie = document.cookie.split(';').find(function(c) {
                return c.trim().startsWith('csrftoken=');
            });
            return cookie ? cookie.split('=')[1] : '';
        },

        resetForm() {
            this.form = {
                author: '',
                title: '',
                date: '',
                url: '',
                publisher: '',
                volume: '',
                issue: '',
                pages: '',
                doi: '',
                isbn: '',
                journal: '',
            };
            this.result = null;
            this.errorMsg = '';
        },

        onStyleChange() {
            // If we have a result, regenerate with new style
            if (this.result && this.form.title) {
                this.generateCitation();
            }
        },

        async autocite() {
            var url = this.autociteUrl.trim();
            if (!url) {
                this.errorMsg = 'Please enter a URL to autocite.';
                return;
            }

            this.autociting = true;
            this.errorMsg = '';

            try {
                var response = await fetch('/api/citations/autocite/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': this.getCSRFToken(),
                    },
                    body: JSON.stringify({ url: url }),
                });

                var data = await response.json();

                if (!response.ok) {
                    this.errorMsg = data.error || 'Failed to fetch URL metadata.';
                    return;
                }

                var metadata = data.metadata;
                if (metadata) {
                    this.form.title = metadata.title || this.form.title;
                    this.form.author = metadata.author || this.form.author;
                    this.form.date = metadata.date || this.form.date;
                    this.form.url = metadata.url || this.form.url;
                    this.form.publisher = metadata.publisher || this.form.publisher;
                }
            } catch (err) {
                this.errorMsg = 'An error occurred while fetching the URL.';
            } finally {
                this.autociting = false;
            }
        },

        async generateCitation() {
            if (!this.form.title) {
                this.errorMsg = 'A title is required to generate a citation.';
                return;
            }

            this.generating = true;
            this.errorMsg = '';

            // Build metadata object
            var metadata = {};
            var keys = Object.keys(this.form);
            for (var i = 0; i < keys.length; i++) {
                var key = keys[i];
                if (this.form[key]) {
                    metadata[key] = this.form[key];
                }
            }

            try {
                var response = await fetch('/api/citations/generate/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': this.getCSRFToken(),
                    },
                    body: JSON.stringify({
                        source_type: this.sourceType,
                        style: this.selectedStyle,
                        metadata: metadata,
                    }),
                });

                var data = await response.json();

                if (!response.ok) {
                    this.errorMsg = data.error || 'Failed to generate citation.';
                    return;
                }

                this.result = data;
            } catch (err) {
                this.errorMsg = 'An error occurred while generating the citation.';
            } finally {
                this.generating = false;
            }
        },

        addToList() {
            if (!this.result) return;

            this.citationList.push({
                formatted_text: this.result.formatted_text,
                in_text_citation: this.result.in_text_citation,
                style: this.result.style,
                source_type: this.result.source_type,
                metadata: Object.assign({}, this.form),
            });

            // Reset for next citation
            this.resetForm();
        },

        removeCitation(index) {
            this.citationList.splice(index, 1);
        },

        copyText(text) {
            if (!text) return;
            // Strip HTML tags for clipboard
            var temp = document.createElement('div');
            temp.innerHTML = text;
            var plainText = temp.textContent || temp.innerText || '';
            navigator.clipboard.writeText(plainText);
            this.copied = 'ref';
            var self = this;
            setTimeout(function() { self.copied = ''; }, 2000);
        },

        copyInText() {
            if (!this.result) return;
            navigator.clipboard.writeText(this.result.in_text_citation);
            this.copied = 'intext';
            var self = this;
            setTimeout(function() { self.copied = ''; }, 2000);
        },

        copySingleCitation(index) {
            var citation = this.citationList[index];
            if (!citation) return;
            var temp = document.createElement('div');
            temp.innerHTML = citation.formatted_text;
            var plainText = temp.textContent || temp.innerText || '';
            navigator.clipboard.writeText(plainText);
        },

        copyAllCitations() {
            var allText = [];
            for (var i = 0; i < this.citationList.length; i++) {
                var temp = document.createElement('div');
                temp.innerHTML = this.citationList[i].formatted_text;
                var plainText = temp.textContent || temp.innerText || '';
                allText.push(plainText);
            }
            navigator.clipboard.writeText(allText.join('\n\n'));
            this.copied = 'all';
            var self = this;
            setTimeout(function() { self.copied = ''; }, 2000);
        },

        exportCitations() {
            var lines = [];
            for (var i = 0; i < this.citationList.length; i++) {
                var temp = document.createElement('div');
                temp.innerHTML = this.citationList[i].formatted_text;
                var plainText = temp.textContent || temp.innerText || '';
                lines.push(plainText);
            }
            var content = lines.join('\n\n');
            var blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
            var url = URL.createObjectURL(blob);
            var a = document.createElement('a');
            a.href = url;
            a.download = 'citations.txt';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        },
    };
}
