function wordCounterApp() {
    return {
        text: '',
        words: 0,
        characters: 0,
        charactersNoSpaces: 0,
        sentenceCount: 0,
        paragraphCount: 0,
        readabilityScore: 0,
        readabilityLabel: 'N/A',
        keywords: [],

        // Social media character limits
        socialLimits: [
            { name: 'Twitter / X', limit: 280 },
            { name: 'Instagram Caption', limit: 2200 },
            { name: 'Facebook Post', limit: 63206 },
            { name: 'LinkedIn Post', limit: 3000 },
            { name: 'Pinterest Pin', limit: 500 },
            { name: 'Reddit Title', limit: 300 },
            { name: 'YouTube Title', limit: 100 },
            { name: 'YouTube Description', limit: 5000 },
            { name: 'TikTok Caption', limit: 2200 },
            { name: 'SMS Message', limit: 160 },
            { name: 'SEO Title', limit: 60 },
            { name: 'SEO Description', limit: 160 },
            { name: 'eBay Title', limit: 80 },
        ],

        // Common English stop words to exclude from keyword density
        stopWords: new Set([
            'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i',
            'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
            'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her',
            'she', 'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there',
            'their', 'what', 'so', 'up', 'out', 'if', 'about', 'who', 'get',
            'which', 'go', 'me', 'when', 'make', 'can', 'like', 'time', 'no',
            'just', 'him', 'know', 'take', 'people', 'into', 'year', 'your',
            'good', 'some', 'could', 'them', 'see', 'other', 'than', 'then',
            'now', 'look', 'only', 'come', 'its', 'over', 'think', 'also',
            'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first',
            'well', 'way', 'even', 'new', 'want', 'because', 'any', 'these',
            'give', 'day', 'most', 'us', 'is', 'are', 'was', 'were', 'been',
            'has', 'had', 'did', 'does', 'am', 'being', 'should', 'may',
            'might', 'must', 'shall', 'very', 'much', 'more', 'too', 'each',
            'every', 'both', 'few', 'many', 'such', 'own', 'same', 'still'
        ]),

        init() {
            this.$watch('text', () => this.analyze());
        },

        analyze() {
            var text = this.text;

            // Characters
            this.characters = text.length;
            this.charactersNoSpaces = text.replace(/\s/g, '').length;

            // Words
            var wordArray = this.getWords(text);
            this.words = wordArray.length;

            // Sentences
            this.sentenceCount = this.countSentences(text);

            // Paragraphs
            this.paragraphCount = this.countParagraphs(text);

            // Readability (Flesch-Kincaid)
            this.calculateReadability(text, wordArray);

            // Keywords
            this.calculateKeywords(wordArray);
        },

        getWords(text) {
            if (!text.trim()) return [];
            return text.trim().split(/\s+/).filter(function(w) { return w.length > 0; });
        },

        countSentences(text) {
            if (!text.trim()) return 0;
            // Match sentence-ending punctuation followed by space or end of string
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
            // If there's text but no double newline, count as 1 paragraph
            return Math.max(paragraphs.length, text.trim() ? 1 : 0);
        },

        countSyllables(word) {
            word = word.toLowerCase().replace(/[^a-z]/g, '');
            if (!word) return 0;
            if (word.length <= 3) return 1;

            // Remove silent e at end
            word = word.replace(/(?:[^laeiouy]es|ed|[^laeiouy]e)$/, '');
            word = word.replace(/^y/, '');

            var syllableMatch = word.match(/[aeiouy]{1,2}/g);
            return syllableMatch ? syllableMatch.length : 1;
        },

        calculateReadability(text, wordArray) {
            if (wordArray.length < 10) {
                this.readabilityScore = 0;
                this.readabilityLabel = 'N/A';
                return;
            }

            var totalWords = wordArray.length;
            var totalSentences = Math.max(this.sentenceCount, 1);
            var totalSyllables = 0;

            var self = this;
            wordArray.forEach(function(word) {
                totalSyllables += self.countSyllables(word);
            });

            // Flesch-Kincaid Reading Ease formula
            var score = 206.835
                - (1.015 * (totalWords / totalSentences))
                - (84.6 * (totalSyllables / totalWords));

            score = Math.round(Math.max(0, Math.min(100, score)));
            this.readabilityScore = score;
            this.readabilityLabel = this.getReadabilityLabel(score);
        },

        getReadabilityLabel(score) {
            if (score >= 90) return 'Very Easy';
            if (score >= 80) return 'Easy';
            if (score >= 70) return 'Fairly Easy';
            if (score >= 60) return 'Standard';
            if (score >= 50) return 'Fairly Difficult';
            if (score >= 30) return 'Difficult';
            return 'Very Difficult';
        },

        getReadabilityColor() {
            var score = this.readabilityScore;
            if (score >= 70) return '#22c55e';
            if (score >= 50) return '#eab308';
            if (score >= 30) return '#f97316';
            return '#ef4444';
        },

        calculateKeywords(wordArray) {
            if (wordArray.length === 0) {
                this.keywords = [];
                return;
            }

            var self = this;
            var freq = {};
            var totalWords = wordArray.length;

            wordArray.forEach(function(word) {
                var cleaned = word.toLowerCase().replace(/[^a-z0-9'-]/g, '');
                if (cleaned.length < 2) return;
                if (self.stopWords.has(cleaned)) return;

                freq[cleaned] = (freq[cleaned] || 0) + 1;
            });

            // Sort by frequency descending
            var sorted = Object.keys(freq).map(function(word) {
                return {
                    word: word,
                    count: freq[word],
                    density: ((freq[word] / totalWords) * 100).toFixed(1)
                };
            }).sort(function(a, b) {
                return b.count - a.count;
            });

            // Return top 15
            this.keywords = sorted.slice(0, 15);
        },

        get readingTime() {
            if (this.words === 0) return '0 sec';
            var minutes = this.words / 238; // Average reading speed: 238 wpm
            return this.formatTime(minutes);
        },

        get speakingTime() {
            if (this.words === 0) return '0 sec';
            var minutes = this.words / 150; // Average speaking speed: 150 wpm
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
