function aiDetector() {
    return {
        inputText: '',
        wordCount: 0,
        loading: false,
        error: '',
        hasResults: false,
        overallScore: 0,
        classification: '',
        classificationLabel: '',
        sentences: [],
        resultWordCount: 0,
        selectedSentence: null,

        updateWordCount() {
            var text = this.inputText.trim();
            this.wordCount = text.length > 0 ? text.split(/\s+/).length : 0;
        },

        handleFileUpload(event) {
            var file = event.target.files[0];
            if (!file) return;

            if (file.name.endsWith('.txt')) {
                var reader = new FileReader();
                var self = this;
                reader.onload = function (e) {
                    self.inputText = e.target.result;
                    self.updateWordCount();
                };
                reader.readAsText(file);
            } else {
                this.error = 'Please upload a .txt file.';
            }
            event.target.value = '';
        },

        detectAI() {
            if (this.wordCount < 80) {
                this.error = 'Please enter at least 80 words for accurate detection.';
                return;
            }

            this.loading = true;
            this.error = '';
            this.hasResults = false;

            var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            var self = this;

            fetch('/api/ai-detect/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ text: this.inputText })
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
                    return;
                }

                self.overallScore = result.data.overall_score;
                self.classification = result.data.classification;
                self.classificationLabel = result.data.classification_label;
                self.sentences = result.data.sentences;
                self.resultWordCount = result.data.word_count;
                self.hasResults = true;
                self.selectedSentence = null;
            })
            .catch(function (err) {
                self.loading = false;
                self.error = 'Network error. Please check your connection and try again.';
            });
        },

        clearAll() {
            this.inputText = '';
            this.wordCount = 0;
            this.error = '';
            this.hasResults = false;
            this.overallScore = 0;
            this.classification = '';
            this.classificationLabel = '';
            this.sentences = [];
            this.resultWordCount = 0;
            this.selectedSentence = null;
        },

        getScoreColor(score) {
            if (score >= 80) return '#dc3545';
            if (score >= 60) return '#fd7e14';
            if (score >= 30) return '#ffc107';
            return '#198754';
        },

        getSentenceBgColor(color) {
            var colors = {
                'red': 'rgba(220, 53, 69, 0.2)',
                'orange': 'rgba(253, 126, 20, 0.2)',
                'yellow': 'rgba(255, 193, 7, 0.15)',
                'green': 'rgba(25, 135, 84, 0.15)'
            };
            return colors[color] || 'transparent';
        },

        getClassificationDescription() {
            var descriptions = {
                'ai_generated': 'This text is very likely generated entirely by AI.',
                'ai_refined': 'This text appears to be AI-generated with some human editing.',
                'human_refined': 'This text appears to be human-written with some AI assistance.',
                'human_written': 'This text appears to be written entirely by a human.'
            };
            return descriptions[this.classification] || '';
        }
    };
}
