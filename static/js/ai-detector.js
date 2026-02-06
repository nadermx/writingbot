function aiDetector() {
    return {
        // Tab state
        activeTab: 'single',

        // Single analysis state
        inputText: '',
        wordCount: 0,
        loading: false,
        error: '',
        hasResults: false,
        overallScore: 0,
        classification: '',
        classificationLabel: '',
        classificationDescription: '',
        categoryConfidences: {
            ai_generated: 0,
            ai_generated_ai_refined: 0,
            human_written_ai_refined: 0,
            human_written: 0
        },
        sentences: [],
        resultWordCount: 0,
        selectedSentence: null,

        // Bulk analysis state
        bulkFiles: [],
        bulkDragOver: false,
        bulkLoading: false,
        bulkProgress: 0,
        bulkError: '',
        bulkResults: [],
        bulkErrors: [],

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
                self.classificationDescription = result.data.classification_description || self.getClassificationDescription();
                self.categoryConfidences = result.data.category_confidences || {
                    ai_generated: 0,
                    ai_generated_ai_refined: 0,
                    human_written_ai_refined: 0,
                    human_written: 0
                };
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
            this.classificationDescription = '';
            this.categoryConfidences = {
                ai_generated: 0,
                ai_generated_ai_refined: 0,
                human_written_ai_refined: 0,
                human_written: 0
            };
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

        getClassificationBadgeClass() {
            var classes = {
                'ai_generated': 'bg-danger',
                'ai_generated_ai_refined': 'bg-warning text-dark',
                'human_written_ai_refined': 'bg-warning bg-opacity-50 text-dark',
                'human_written': 'bg-success'
            };
            return classes[this.classification] || 'bg-secondary';
        },

        getClassificationDescription() {
            var descriptions = {
                'ai_generated': 'This text appears to be entirely generated by AI with no human involvement.',
                'ai_generated_ai_refined': 'This text appears to be AI-generated and then further polished or refined by AI tools.',
                'human_written_ai_refined': 'This text appears to be originally written by a human but edited or polished using AI tools.',
                'human_written': 'This text appears to be entirely written by a human with no AI assistance.'
            };
            return descriptions[this.classification] || '';
        },

        getBulkClassBadge(classification) {
            var classes = {
                'ai_generated': 'bg-danger',
                'ai_generated_ai_refined': 'bg-warning text-dark',
                'human_written_ai_refined': 'bg-warning bg-opacity-50 text-dark',
                'human_written': 'bg-success'
            };
            return classes[classification] || 'bg-secondary';
        },

        // Bulk analysis methods
        handleBulkDrop(event) {
            this.bulkDragOver = false;
            var files = Array.from(event.dataTransfer.files);
            this.addBulkFiles(files);
        },

        handleBulkFileSelect(event) {
            var files = Array.from(event.target.files);
            this.addBulkFiles(files);
            event.target.value = '';
        },

        addBulkFiles(files) {
            var allowed = ['.txt', '.pdf', '.docx'];
            var maxFiles = 10;
            var maxSize = 5 * 1024 * 1024;

            for (var i = 0; i < files.length; i++) {
                if (this.bulkFiles.length >= maxFiles) {
                    this.bulkError = 'Maximum ' + maxFiles + ' files allowed.';
                    break;
                }

                var file = files[i];
                var ext = '.' + file.name.split('.').pop().toLowerCase();

                if (allowed.indexOf(ext) === -1) {
                    this.bulkError = file.name + ': Unsupported file type. Use TXT, PDF, or DOCX.';
                    continue;
                }

                if (file.size > maxSize) {
                    this.bulkError = file.name + ': File too large. Maximum 5 MB.';
                    continue;
                }

                // Check for duplicates
                var isDuplicate = false;
                for (var j = 0; j < this.bulkFiles.length; j++) {
                    if (this.bulkFiles[j].name === file.name && this.bulkFiles[j].size === file.size) {
                        isDuplicate = true;
                        break;
                    }
                }
                if (!isDuplicate) {
                    this.bulkFiles.push(file);
                }
            }
        },

        removeBulkFile(idx) {
            this.bulkFiles.splice(idx, 1);
        },

        clearBulkFiles() {
            this.bulkFiles = [];
            this.bulkError = '';
            this.bulkResults = [];
            this.bulkErrors = [];
        },

        formatFileSize(bytes) {
            if (bytes < 1024) return bytes + ' B';
            if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
            return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
        },

        runBulkAnalysis() {
            if (this.bulkFiles.length === 0 || this.bulkLoading) return;

            this.bulkLoading = true;
            this.bulkProgress = 0;
            this.bulkError = '';
            this.bulkResults = [];
            this.bulkErrors = [];

            var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            var self = this;

            var formData = new FormData();
            for (var i = 0; i < this.bulkFiles.length; i++) {
                formData.append('files', this.bulkFiles[i]);
            }

            // Show progress as "uploading"
            self.bulkProgress = 'uploading';

            fetch('/api/ai-detect/bulk/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken
                },
                body: formData
            })
            .then(function (response) {
                return response.json().then(function (data) {
                    return { ok: response.ok, data: data };
                });
            })
            .then(function (result) {
                self.bulkLoading = false;
                self.bulkProgress = 0;

                if (!result.ok) {
                    self.bulkError = result.data.error || 'An error occurred during bulk analysis.';
                    return;
                }

                self.bulkResults = result.data.results || [];
                self.bulkErrors = result.data.errors || [];

                if (self.bulkResults.length === 0 && self.bulkErrors.length > 0) {
                    self.bulkError = 'All files failed to process. Check the errors below.';
                }
            })
            .catch(function (err) {
                self.bulkLoading = false;
                self.bulkProgress = 0;
                self.bulkError = 'Network error. Please check your connection and try again.';
            });
        }
    };
}
