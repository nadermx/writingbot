function textCaseConverterApp() {
    return {
        inputText: '',
        outputText: '',
        activeMode: '',
        copied: false,

        init() {},

        get charCount() {
            return this.inputText.length;
        },

        convert(mode) {
            if (!this.inputText.trim()) return;

            switch (mode) {
                case 'uppercase':
                    this.outputText = this.inputText.toUpperCase();
                    this.activeMode = 'UPPERCASE';
                    break;
                case 'lowercase':
                    this.outputText = this.inputText.toLowerCase();
                    this.activeMode = 'lowercase';
                    break;
                case 'titlecase':
                    this.outputText = this.toTitleCase(this.inputText);
                    this.activeMode = 'Title Case';
                    break;
                case 'sentencecase':
                    this.outputText = this.toSentenceCase(this.inputText);
                    this.activeMode = 'Sentence case';
                    break;
                case 'camelcase':
                    this.outputText = this.toCamelCase(this.inputText);
                    this.activeMode = 'camelCase';
                    break;
                case 'snakecase':
                    this.outputText = this.toSnakeCase(this.inputText);
                    this.activeMode = 'snake_case';
                    break;
                case 'kebabcase':
                    this.outputText = this.toKebabCase(this.inputText);
                    this.activeMode = 'kebab-case';
                    break;
                case 'constantcase':
                    this.outputText = this.toConstantCase(this.inputText);
                    this.activeMode = 'CONSTANT_CASE';
                    break;
                case 'alternating':
                    this.outputText = this.toAlternatingCase(this.inputText);
                    this.activeMode = 'aLtErNaTiNg';
                    break;
                case 'inverse':
                    this.outputText = this.toInverseCase(this.inputText);
                    this.activeMode = 'iNVERSE';
                    break;
            }
            this.copied = false;
        },

        toTitleCase(text) {
            return text.replace(/\w\S*/g, function(word) {
                return word.charAt(0).toUpperCase() + word.substring(1).toLowerCase();
            });
        },

        toSentenceCase(text) {
            return text.toLowerCase().replace(/(^\s*\w|[.!?]\s+\w)/g, function(match) {
                return match.toUpperCase();
            });
        },

        toCamelCase(text) {
            // Split on non-alphanumeric characters
            var words = text.split(/[^a-zA-Z0-9]+/).filter(function(w) { return w.length > 0; });
            if (words.length === 0) return '';

            return words.map(function(word, index) {
                var lower = word.toLowerCase();
                if (index === 0) return lower;
                return lower.charAt(0).toUpperCase() + lower.substring(1);
            }).join('');
        },

        toSnakeCase(text) {
            // Handle camelCase input
            var expanded = text.replace(/([a-z])([A-Z])/g, '$1 $2');
            var words = expanded.split(/[^a-zA-Z0-9]+/).filter(function(w) { return w.length > 0; });
            return words.map(function(w) { return w.toLowerCase(); }).join('_');
        },

        toKebabCase(text) {
            var expanded = text.replace(/([a-z])([A-Z])/g, '$1 $2');
            var words = expanded.split(/[^a-zA-Z0-9]+/).filter(function(w) { return w.length > 0; });
            return words.map(function(w) { return w.toLowerCase(); }).join('-');
        },

        toConstantCase(text) {
            var expanded = text.replace(/([a-z])([A-Z])/g, '$1 $2');
            var words = expanded.split(/[^a-zA-Z0-9]+/).filter(function(w) { return w.length > 0; });
            return words.map(function(w) { return w.toUpperCase(); }).join('_');
        },

        toAlternatingCase(text) {
            var result = '';
            var charIndex = 0;
            for (var i = 0; i < text.length; i++) {
                var ch = text[i];
                if (/[a-zA-Z]/.test(ch)) {
                    if (charIndex % 2 === 0) {
                        result += ch.toLowerCase();
                    } else {
                        result += ch.toUpperCase();
                    }
                    charIndex++;
                } else {
                    result += ch;
                }
            }
            return result;
        },

        toInverseCase(text) {
            var result = '';
            for (var i = 0; i < text.length; i++) {
                var ch = text[i];
                if (ch === ch.toUpperCase()) {
                    result += ch.toLowerCase();
                } else {
                    result += ch.toUpperCase();
                }
            }
            return result;
        },

        copyOutput() {
            var self = this;
            if (self.outputText) {
                navigator.clipboard.writeText(self.outputText).then(function() {
                    self.copied = true;
                    setTimeout(function() {
                        self.copied = false;
                    }, 2000);
                });
            }
        },

        clearText() {
            this.inputText = '';
            this.outputText = '';
            this.activeMode = '';
        }
    };
}
