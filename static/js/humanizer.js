function humanizer() {
    return {
        inputText: '',
        outputText: '',
        mode: 'basic',
        wordCount: 0,
        loading: false,
        error: '',
        hasResults: false,
        aiScoreBefore: 0,
        aiScoreAfter: 0,
        copied: false,

        updateWordCount() {
            var text = this.inputText.trim();
            this.wordCount = text.length > 0 ? text.split(/\s+/).length : 0;
        },

        humanize() {
            if (this.wordCount === 0) {
                this.error = 'Please enter some text to humanize.';
                return;
            }

            this.loading = true;
            this.error = '';
            this.hasResults = false;
            this.outputText = '';

            var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            var self = this;

            fetch('/api/humanize/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({
                    text: this.inputText,
                    mode: this.mode
                })
            })
            .then(function (response) {
                return response.json().then(function (data) {
                    return { ok: response.ok, data: data };
                });
            })
            .then(function (result) {
                self.loading = false;
                if (!result.ok) {
                    self.error = result.data.error || 'An error occurred.';
                    if (result.data.premium_required) {
                        self.error = 'Advanced mode requires a Premium subscription. Please upgrade or switch to Basic mode.';
                    }
                    if (result.data.limit_exceeded) {
                        self.error = result.data.error;
                    }
                    return;
                }

                self.outputText = result.data.output_text;
                self.aiScoreBefore = result.data.ai_score_before;
                self.aiScoreAfter = result.data.ai_score_after;
                self.hasResults = true;
            })
            .catch(function (err) {
                self.loading = false;
                self.error = 'Network error. Please check your connection and try again.';
            });
        },

        copyOutput() {
            var self = this;
            navigator.clipboard.writeText(this.outputText).then(function () {
                self.copied = true;
                setTimeout(function () {
                    self.copied = false;
                }, 2000);
            });
        },

        clearAll() {
            this.inputText = '';
            this.outputText = '';
            this.wordCount = 0;
            this.error = '';
            this.hasResults = false;
            this.aiScoreBefore = 0;
            this.aiScoreAfter = 0;
            this.copied = false;
        },

        getScoreColor(score) {
            if (score >= 80) return '#dc3545';
            if (score >= 60) return '#fd7e14';
            if (score >= 30) return '#ffc107';
            return '#198754';
        }
    };
}
