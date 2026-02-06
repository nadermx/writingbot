function characterCounterApp() {
    return {
        text: '',
        characters: 0,
        charactersNoSpaces: 0,
        words: 0,
        sentenceCount: 0,
        paragraphCount: 0,

        platforms: [
            { name: 'Twitter/X', limit: 280 },
            { name: 'SEO Title', limit: 60 },
            { name: 'SMS', limit: 160 },
            { name: 'SEO Description', limit: 160 },
            { name: 'eBay Title', limit: 80 },
            { name: 'Reddit Title', limit: 300 },
            { name: 'Pinterest Pin', limit: 500 },
            { name: 'Instagram Caption', limit: 2200 },
            { name: 'Yelp Review', limit: 5000 },
            { name: 'LinkedIn Post', limit: 13000 },
            { name: 'Facebook Post', limit: 63206 }
        ],

        init() {
            this.$watch('text', () => this.analyze());
        },

        analyze() {
            var text = this.text;

            // Characters
            this.characters = text.length;
            this.charactersNoSpaces = text.replace(/\s/g, '').length;

            // Words
            this.words = this.getWords(text).length;

            // Sentences
            this.sentenceCount = this.countSentences(text);

            // Paragraphs
            this.paragraphCount = this.countParagraphs(text);
        },

        getWords(text) {
            if (!text.trim()) return [];
            return text.trim().split(/\s+/).filter(function(w) { return w.length > 0; });
        },

        countSentences(text) {
            if (!text.trim()) return 0;
            var sentences = text.split(/[.!?]+/).filter(function(s) {
                return s.trim().length > 0;
            });
            return sentences.length;
        },

        countParagraphs(text) {
            if (!text.trim()) return 0;
            var paragraphs = text.split(/\n\s*\n/).filter(function(p) {
                return p.trim().length > 0;
            });
            return Math.max(paragraphs.length, text.trim() ? 1 : 0);
        },

        getProgressBarClass(current, limit) {
            var ratio = current / limit;
            if (ratio >= 1) return 'bg-danger';
            if (ratio >= 0.9) return 'bg-warning';
            return 'bg-primary';
        },

        get readingTime() {
            if (this.words === 0) return '0 sec';
            var minutes = this.words / 238;
            return this.formatTime(minutes);
        },

        get speakingTime() {
            if (this.words === 0) return '0 sec';
            var minutes = this.words / 150;
            return this.formatTime(minutes);
        },

        formatTime(minutes) {
            if (minutes < 1) {
                var seconds = Math.round(minutes * 60);
                return seconds + ' sec';
            }
            var mins = Math.floor(minutes);
            var secs = Math.round((minutes - mins) * 60);

            if (mins >= 60) {
                var hours = Math.floor(mins / 60);
                mins = mins % 60;
                return hours + ' hr ' + mins + ' min';
            }

            if (secs > 0) {
                return mins + ' min ' + secs + ' sec';
            }
            return mins + ' min';
        },

        clearText() {
            this.text = '';
            this.analyze();
        }
    };
}
