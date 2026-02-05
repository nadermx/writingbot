function translator(initialLanguages) {
    return {
        inputText: '',
        translatedText: '',
        sourceLang: 'auto',
        targetLang: 'es',
        charCount: 0,
        loading: false,
        error: '',
        copied: false,
        detectedLang: '',
        languages: initialLanguages || [],

        init() {
            if (!this.languages || this.languages.length === 0) {
                this.fetchLanguages();
            }
        },

        fetchLanguages() {
            var self = this;
            fetch('/api/translate/languages/')
                .then(function (response) {
                    return response.json();
                })
                .then(function (data) {
                    self.languages = data.languages || [];
                })
                .catch(function () {
                    // Silently fail, languages may be passed from template
                });
        },

        updateCharCount() {
            this.charCount = this.inputText.length;
        },

        swapLanguages() {
            if (this.sourceLang === 'auto') return;

            var tempLang = this.sourceLang;
            this.sourceLang = this.targetLang;
            this.targetLang = tempLang;

            // Also swap the text if we have a translation
            if (this.translatedText) {
                var tempText = this.inputText;
                this.inputText = this.translatedText;
                this.translatedText = tempText;
                this.updateCharCount();
            }
        },

        translate() {
            if (this.charCount === 0) {
                this.error = 'Please enter some text to translate.';
                return;
            }

            if (!this.targetLang) {
                this.error = 'Please select a target language.';
                return;
            }

            this.loading = true;
            this.error = '';
            this.translatedText = '';
            this.detectedLang = '';

            var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            var self = this;

            fetch('/api/translate/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({
                    text: this.inputText,
                    source_lang: this.sourceLang,
                    target_lang: this.targetLang
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
                    return;
                }

                self.translatedText = result.data.translated_text;
                if (self.sourceLang === 'auto') {
                    self.detectedLang = result.data.source_lang;
                }
            })
            .catch(function (err) {
                self.loading = false;
                self.error = 'Network error. Please check your connection and try again.';
            });
        },

        copyTranslation() {
            var self = this;
            navigator.clipboard.writeText(this.translatedText).then(function () {
                self.copied = true;
                setTimeout(function () {
                    self.copied = false;
                }, 2000);
            });
        },

        clearInput() {
            this.inputText = '';
            this.translatedText = '';
            this.charCount = 0;
            this.error = '';
            this.detectedLang = '';
            this.copied = false;
        },

        getLanguageName(code) {
            for (var i = 0; i < this.languages.length; i++) {
                if (this.languages[i].code === code) {
                    return this.languages[i].name;
                }
            }
            return code;
        }
    };
}
