/**
 * SEO Landing Page paraphraser component.
 * Reuses the paraphraser API endpoint with a simplified UI.
 */
function seoParaphraser() {
    return {
        inputText: '',
        outputText: '',
        mode: 'standard',
        synonymLevel: 3,
        wordCount: 0,
        processing: false,
        error: '',

        updateWordCount() {
            const text = this.inputText.trim();
            this.wordCount = text ? text.split(/\s+/).length : 0;
        },

        async paraphrase() {
            if (!this.inputText.trim()) return;

            this.processing = true;
            this.error = '';
            this.outputText = '';

            try {
                const response = await fetch('/api/paraphrase/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': this.getCsrfToken(),
                    },
                    body: JSON.stringify({
                        text: this.inputText,
                        mode: this.mode,
                        synonym_level: parseInt(this.synonymLevel),
                        frozen_words: [],
                        settings: {},
                        language: 'en',
                    })
                });

                const data = await response.json();

                if (response.ok) {
                    this.outputText = data.output_text;
                } else {
                    this.error = data.error || 'An error occurred. Please try again.';
                }

            } catch (e) {
                this.error = 'Network error. Please check your connection and try again.';
            }

            this.processing = false;
        },

        copyOutput() {
            if (this.outputText) {
                navigator.clipboard.writeText(this.outputText);
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
