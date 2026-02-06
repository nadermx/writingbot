/**
 * WritingBot.ai Paraphraser - Alpine.js Component
 *
 * Handles all client-side logic for the paraphrasing tool:
 * - Text input/output management
 * - Mode selection and settings
 * - Frozen words
 * - Synonym popup on word click
 * - Color-coded diff highlighting (toggle)
 * - Compare modes (3-column comparison)
 * - File upload (.txt, .docx)
 * - Copy to clipboard
 * - History loading (premium)
 */
function paraphraser() {
    return {
        // State
        inputText: '',
        outputText: '',
        outputHtml: '',
        diffHtml: '',
        showDiff: false,
        mode: 'standard',
        synonymLevel: 3,
        frozenWords: [],
        isLoading: false,
        isComparing: false,
        errorMessage: '',
        showUpgrade: false,
        copyLabel: 'Copy',
        inputWordCount: 0,
        outputWordCount: 0,

        // Compare results
        compareResults: [],

        // Config passed from template
        isPremium: false,
        freeWordLimit: 500,
        freeModes: [],

        // Settings
        paraphraseSettings: {
            use_contractions: false,
            active_voice: false,
            custom_instructions: '',
        },

        // Synonym popup
        synonymPopup: {
            visible: false,
            x: 0,
            y: 0,
            word: '',
            wordIndex: -1,
            synonyms: [],
            loading: false,
        },

        // History
        historyItems: [],

        // Computed: unique input words for freeze UI
        get uniqueInputWords() {
            if (!this.inputText.trim()) return [];
            var words = this.inputText.trim().split(/\s+/);
            var seen = {};
            var unique = [];
            for (var i = 0; i < words.length; i++) {
                var clean = words[i].replace(/[^a-zA-Z0-9'-]/g, '').toLowerCase();
                if (clean && !seen[clean] && clean.length > 1) {
                    seen[clean] = true;
                    unique.push(clean);
                }
            }
            return unique;
        },

        init: function () {
            // Read config from the DOM data attributes or inline variables
            var container = document.querySelector('[x-data]');
            this.isPremium = document.body.dataset.isPremium === 'true' ||
                (typeof window._paraphraserConfig !== 'undefined' && window._paraphraserConfig.isPremium);
            this.freeWordLimit = (typeof window._paraphraserConfig !== 'undefined' && window._paraphraserConfig.freeWordLimit) || 500;
            this.freeModes = (typeof window._paraphraserConfig !== 'undefined' && window._paraphraserConfig.freeModes) || ['standard', 'fluency'];

            // Try reading from script tag or hidden inputs
            var isPremEl = document.getElementById('isPremium');
            if (isPremEl) this.isPremium = isPremEl.value === 'true';
            var limitEl = document.getElementById('freeWordLimit');
            if (limitEl) this.freeWordLimit = parseInt(limitEl.value, 10) || 500;
            var modesEl = document.getElementById('freeModes');
            if (modesEl && modesEl.value) {
                this.freeModes = modesEl.value.split(',').map(function(s) { return s.trim(); }).filter(Boolean);
            }

            // Load history for premium users
            if (this.isPremium) {
                this.loadHistory();
            }
        },

        selectMode: function (newMode) {
            if (!this.isPremium && !this.freeModes.includes(newMode)) {
                this.errorMessage = 'The "' + newMode + '" mode is available for premium users only.';
                this.showUpgrade = true;
                return;
            }
            this.mode = newMode;
            this.errorMessage = '';
            this.showUpgrade = false;
        },

        updateInputWordCount: function () {
            this.inputWordCount = this.countWords(this.inputText);
        },

        countWords: function (text) {
            if (!text || !text.trim()) return 0;
            return text.trim().split(/\s+/).length;
        },

        /**
         * Main paraphrase action - POST to /api/paraphrase/
         */
        paraphrase: function () {
            var self = this;
            var text = this.inputText.trim();

            if (!text) {
                this.errorMessage = 'Please enter some text to paraphrase.';
                return;
            }

            this.errorMessage = '';
            this.showUpgrade = false;
            this.isLoading = true;
            this.outputHtml = '';
            this.outputText = '';
            this.diffHtml = '';
            this.showDiff = false;
            this.outputWordCount = 0;
            this.synonymPopup.visible = false;
            this.compareResults = [];

            var payload = {
                text: text,
                mode: this.mode,
                synonym_level: parseInt(this.synonymLevel, 10),
                frozen_words: this.frozenWords,
                settings: {
                    use_contractions: this.paraphraseSettings.use_contractions,
                    active_voice: this.paraphraseSettings.active_voice,
                },
                language: 'en',
            };

            if (this.mode === 'custom' && this.paraphraseSettings.custom_instructions) {
                payload.settings.custom_instructions = this.paraphraseSettings.custom_instructions;
            }

            fetch('/api/paraphrase/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': self.getCsrfToken(),
                },
                body: JSON.stringify(payload),
            })
            .then(function (resp) {
                return resp.json().then(function (data) {
                    return { ok: resp.ok, status: resp.status, data: data };
                });
            })
            .then(function (result) {
                self.isLoading = false;

                if (!result.ok) {
                    self.errorMessage = result.data.error || 'An error occurred.';
                    self.showUpgrade = !!result.data.upgrade;
                    return;
                }

                self.outputText = result.data.output_text;
                self.outputWordCount = result.data.output_word_count || self.countWords(self.outputText);
                self.outputHtml = self._renderOutputWords(self.outputText);
                self.diffHtml = self.computeDiff(self.inputText, self.outputText);
            })
            .catch(function (err) {
                self.isLoading = false;
                self.errorMessage = 'Network error. Please check your connection and try again.';
            });
        },

        /**
         * Toggle the diff view on/off
         */
        toggleDiff: function () {
            if (!this.diffHtml && this.inputText && this.outputText) {
                this.diffHtml = this.computeDiff(this.inputText, this.outputText);
            }
            this.showDiff = !this.showDiff;
        },

        /**
         * Compare paraphrase: run text through 3 different modes simultaneously
         */
        compareParaphrase: function () {
            var self = this;
            var text = this.inputText.trim();

            if (!text) {
                this.errorMessage = 'Please enter some text to compare.';
                return;
            }

            // Pick 3 modes for comparison: current mode + 2 others
            var compareModes = this._pickCompareModes(this.mode);

            this.errorMessage = '';
            this.showUpgrade = false;
            this.isComparing = true;
            this.compareResults = [];

            var promises = [];
            var csrfToken = this.getCsrfToken();

            for (var i = 0; i < compareModes.length; i++) {
                var cMode = compareModes[i];

                // Check if mode is available for user
                if (!this.isPremium && !this.freeModes.includes(cMode)) {
                    continue;
                }

                var payload = {
                    text: text,
                    mode: cMode,
                    synonym_level: parseInt(this.synonymLevel, 10),
                    frozen_words: this.frozenWords,
                    settings: {
                        use_contractions: this.paraphraseSettings.use_contractions,
                        active_voice: this.paraphraseSettings.active_voice,
                    },
                    language: 'en',
                };

                promises.push(
                    (function(mode) {
                        return fetch('/api/paraphrase/', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'X-CSRFToken': csrfToken,
                            },
                            body: JSON.stringify({
                                text: text,
                                mode: mode,
                                synonym_level: parseInt(self.synonymLevel, 10),
                                frozen_words: self.frozenWords,
                                settings: {
                                    use_contractions: self.paraphraseSettings.use_contractions,
                                    active_voice: self.paraphraseSettings.active_voice,
                                },
                                language: 'en',
                            }),
                        })
                        .then(function(resp) {
                            return resp.json().then(function(data) {
                                return { ok: resp.ok, data: data, mode: mode };
                            });
                        });
                    })(cMode)
                );
            }

            if (promises.length === 0) {
                this.isComparing = false;
                this.errorMessage = 'No modes available for comparison. Upgrade to access more modes.';
                this.showUpgrade = true;
                return;
            }

            Promise.all(promises)
                .then(function(results) {
                    self.isComparing = false;
                    var compareItems = [];
                    for (var r = 0; r < results.length; r++) {
                        var res = results[r];
                        if (res.ok && res.data.output_text) {
                            compareItems.push({
                                mode: res.mode,
                                text: res.data.output_text,
                                wordCount: res.data.output_word_count || self.countWords(res.data.output_text),
                                copyLabel: 'Copy',
                            });
                        }
                    }
                    self.compareResults = compareItems;
                })
                .catch(function() {
                    self.isComparing = false;
                    self.errorMessage = 'Failed to compare modes. Please try again.';
                });
        },

        /**
         * Pick 3 modes for comparison. Uses the current mode plus 2 different ones.
         */
        _pickCompareModes: function (currentMode) {
            // Define comparison sets based on the current mode category
            var allModes = ['standard', 'fluency', 'formal', 'academic', 'simple', 'creative'];
            var selected = [currentMode];

            // Add different modes that offer meaningful contrast
            var modeContrasts = {
                'standard': ['formal', 'creative'],
                'fluency': ['formal', 'simple'],
                'formal': ['standard', 'creative'],
                'academic': ['standard', 'simple'],
                'simple': ['standard', 'formal'],
                'creative': ['standard', 'formal'],
                'expand': ['standard', 'shorten'],
                'shorten': ['standard', 'expand'],
                'custom': ['standard', 'formal'],
                'humanizer': ['standard', 'creative'],
            };

            var contrasts = modeContrasts[currentMode] || ['standard', 'formal'];

            for (var i = 0; i < contrasts.length; i++) {
                if (selected.indexOf(contrasts[i]) === -1) {
                    selected.push(contrasts[i]);
                }
            }

            // Ensure we have exactly 3 modes
            for (var m = 0; m < allModes.length && selected.length < 3; m++) {
                if (selected.indexOf(allModes[m]) === -1) {
                    selected.push(allModes[m]);
                }
            }

            return selected.slice(0, 3);
        },

        /**
         * Use a compare result as the main output
         */
        useCompareResult: function (index) {
            var cr = this.compareResults[index];
            if (!cr) return;

            this.outputText = cr.text;
            this.outputWordCount = cr.wordCount;
            this.outputHtml = this._renderOutputWords(this.outputText);
            this.diffHtml = this.computeDiff(this.inputText, this.outputText);
            this.compareResults = [];
        },

        /**
         * Copy a compare result to clipboard
         */
        copyCompareResult: function (index) {
            var self = this;
            var cr = this.compareResults[index];
            if (!cr) return;

            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(cr.text).then(function () {
                    self.compareResults[index].copyLabel = 'Copied!';
                    setTimeout(function () {
                        self.compareResults[index].copyLabel = 'Copy';
                    }, 2000);
                });
            } else {
                var textarea = document.createElement('textarea');
                textarea.value = cr.text;
                textarea.style.position = 'fixed';
                textarea.style.opacity = '0';
                document.body.appendChild(textarea);
                textarea.select();
                document.execCommand('copy');
                document.body.removeChild(textarea);
                self.compareResults[index].copyLabel = 'Copied!';
                setTimeout(function () {
                    self.compareResults[index].copyLabel = 'Copy';
                }, 2000);
            }
        },

        /**
         * Render output words as clickable spans (no diff coloring).
         * Used for the default (non-diff) output view.
         */
        _renderOutputWords: function (text) {
            if (!text) return '';
            var words = text.trim().split(/\s+/);
            var html = [];
            for (var i = 0; i < words.length; i++) {
                html.push(
                    '<span class="output-word" data-word="' +
                    this._escapeHtml(words[i]) + '" data-index="' + i + '">' +
                    this._escapeHtml(words[i]) + '</span> '
                );
            }
            return html.join('');
        },

        /**
         * Compute color-coded diff between input and output.
         * Uses Longest Common Subsequence (LCS) to identify changes.
         * Changed/added words: green background
         * Removed words: red strikethrough
         * Unchanged words: normal text (still clickable)
         */
        computeDiff: function (input, output) {
            if (!input || !output) return '';

            var inputWords = input.trim().split(/\s+/);
            var outputWords = output.trim().split(/\s+/);

            // Build LCS table for word-level diff
            var lcs = this._lcs(inputWords, outputWords);

            var html = [];
            var i = 0;
            var j = 0;
            var lcsIdx = 0;
            var outputWordIndex = 0;

            while (i < inputWords.length || j < outputWords.length) {
                if (lcsIdx < lcs.length &&
                    i < inputWords.length &&
                    j < outputWords.length &&
                    this._normalizeWord(inputWords[i]) === this._normalizeWord(lcs[lcsIdx]) &&
                    this._normalizeWord(outputWords[j]) === this._normalizeWord(lcs[lcsIdx])) {
                    // Unchanged word
                    html.push(
                        '<span class="output-word diff-unchanged" data-word="' +
                        this._escapeHtml(outputWords[j]) + '" data-index="' + outputWordIndex + '">' +
                        this._escapeHtml(outputWords[j]) + '</span> '
                    );
                    i++;
                    j++;
                    lcsIdx++;
                    outputWordIndex++;
                } else if (j < outputWords.length &&
                    (lcsIdx >= lcs.length || this._normalizeWord(outputWords[j]) !== this._normalizeWord(lcs[lcsIdx]))) {
                    // Added/changed word in output
                    html.push(
                        '<span class="output-word diff-added" data-word="' +
                        this._escapeHtml(outputWords[j]) + '" data-index="' + outputWordIndex + '">' +
                        this._escapeHtml(outputWords[j]) + '</span> '
                    );
                    j++;
                    outputWordIndex++;
                } else if (i < inputWords.length &&
                    (lcsIdx >= lcs.length || this._normalizeWord(inputWords[i]) !== this._normalizeWord(lcs[lcsIdx]))) {
                    // Removed word from input (shown as strikethrough)
                    html.push(
                        '<span class="diff-removed">' +
                        this._escapeHtml(inputWords[i]) + '</span> '
                    );
                    i++;
                } else {
                    // Safety: advance both to prevent infinite loop
                    if (j < outputWords.length) {
                        html.push(
                            '<span class="output-word diff-added" data-word="' +
                            this._escapeHtml(outputWords[j]) + '" data-index="' + outputWordIndex + '">' +
                            this._escapeHtml(outputWords[j]) + '</span> '
                        );
                        j++;
                        outputWordIndex++;
                    }
                    if (i < inputWords.length) {
                        i++;
                    }
                }
            }

            return html.join('');
        },

        /**
         * Legacy alias - the old calculateDiff now calls computeDiff
         */
        calculateDiff: function (input, output) {
            return this.computeDiff(input, output);
        },

        /**
         * Fetch synonyms for a word in the output
         */
        fetchSynonyms: function (word, wordIndex, x, y) {
            var self = this;
            this.synonymPopup.visible = true;
            this.synonymPopup.word = word;
            this.synonymPopup.wordIndex = wordIndex;
            this.synonymPopup.x = x;
            this.synonymPopup.y = y;
            this.synonymPopup.synonyms = [];
            this.synonymPopup.loading = true;

            fetch('/api/paraphrase/synonyms/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': self.getCsrfToken(),
                },
                body: JSON.stringify({
                    word: word,
                    context: self.outputText,
                }),
            })
            .then(function (resp) { return resp.json(); })
            .then(function (data) {
                self.synonymPopup.loading = false;
                if (data.synonyms) {
                    self.synonymPopup.synonyms = data.synonyms;
                }
            })
            .catch(function () {
                self.synonymPopup.loading = false;
                self.synonymPopup.synonyms = [];
            });
        },

        /**
         * Replace a word in the output with a chosen synonym
         */
        replaceSynonym: function (synonym) {
            var words = this.outputText.split(/(\s+)/);
            var wordIdx = this.synonymPopup.wordIndex;

            // words array includes whitespace tokens, so map to actual word indices
            var actualIndex = 0;
            for (var i = 0; i < words.length; i++) {
                if (words[i].trim() === '') continue;
                if (actualIndex === wordIdx) {
                    // Preserve any punctuation attached to the word
                    var leading = words[i].match(/^([^a-zA-Z0-9]*)/)[0];
                    var trailing = words[i].match(/([^a-zA-Z0-9]*)$/)[0];
                    words[i] = leading + synonym + trailing;
                    break;
                }
                actualIndex++;
            }

            this.outputText = words.join('');
            this.outputHtml = this._renderOutputWords(this.outputText);
            this.diffHtml = this.computeDiff(this.inputText, this.outputText);
            this.outputWordCount = this.countWords(this.outputText);
            this.synonymPopup.visible = false;
        },

        /**
         * Handle clicking on a word in the output pane
         */
        handleOutputClick: function (event) {
            var target = event.target;
            if (!target.classList.contains('output-word')) return;

            var word = target.dataset.word;
            var wordIndex = parseInt(target.dataset.index, 10);
            if (!word) return;

            // Calculate popup position relative to the output container
            var container = target.closest('.card-body');
            var containerRect = container.getBoundingClientRect();
            var targetRect = target.getBoundingClientRect();

            var x = targetRect.left - containerRect.left;
            var y = targetRect.bottom - containerRect.top + 4;

            // Prevent overflow off the right
            if (x + 160 > containerRect.width) {
                x = containerRect.width - 170;
            }

            this.fetchSynonyms(word, wordIndex, x, y);
        },

        toggleFreezeWord: function (word) {
            var idx = this.frozenWords.indexOf(word);
            if (idx === -1) {
                this.frozenWords.push(word);
            } else {
                this.frozenWords.splice(idx, 1);
            }
        },

        /**
         * Copy output text to clipboard
         */
        copyOutput: function () {
            var self = this;
            if (!this.outputText) return;

            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(this.outputText).then(function () {
                    self.copyLabel = 'Copied!';
                    setTimeout(function () { self.copyLabel = 'Copy'; }, 2000);
                });
            } else {
                // Fallback
                var textarea = document.createElement('textarea');
                textarea.value = this.outputText;
                textarea.style.position = 'fixed';
                textarea.style.opacity = '0';
                document.body.appendChild(textarea);
                textarea.select();
                document.execCommand('copy');
                document.body.removeChild(textarea);
                this.copyLabel = 'Copied!';
                setTimeout(function () { self.copyLabel = 'Copy'; }, 2000);
            }
        },

        /**
         * Compute LCS of two word arrays (for diff highlighting).
         * Uses dynamic programming. For very long texts, falls back to a
         * simplified approach to avoid O(n^2) memory issues.
         */
        _lcs: function (a, b) {
            var m = a.length;
            var n = b.length;

            // For very large inputs, use a simplified line-by-line approach
            if (m * n > 500000) {
                return this._lcsSimple(a, b);
            }

            var dp = [];
            var i, j;

            for (i = 0; i <= m; i++) {
                dp[i] = [];
                for (j = 0; j <= n; j++) {
                    dp[i][j] = 0;
                }
            }

            for (i = 1; i <= m; i++) {
                for (j = 1; j <= n; j++) {
                    if (this._normalizeWord(a[i - 1]) === this._normalizeWord(b[j - 1])) {
                        dp[i][j] = dp[i - 1][j - 1] + 1;
                    } else {
                        dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
                    }
                }
            }

            // Backtrack to find the LCS sequence
            var result = [];
            i = m;
            j = n;
            while (i > 0 && j > 0) {
                if (this._normalizeWord(a[i - 1]) === this._normalizeWord(b[j - 1])) {
                    result.unshift(a[i - 1]);
                    i--;
                    j--;
                } else if (dp[i - 1][j] > dp[i][j - 1]) {
                    i--;
                } else {
                    j--;
                }
            }

            return result;
        },

        /**
         * Simplified LCS for large inputs - uses a greedy matching approach
         */
        _lcsSimple: function (a, b) {
            var result = [];
            var bIndex = 0;
            for (var i = 0; i < a.length && bIndex < b.length; i++) {
                for (var j = bIndex; j < b.length; j++) {
                    if (this._normalizeWord(a[i]) === this._normalizeWord(b[j])) {
                        result.push(a[i]);
                        bIndex = j + 1;
                        break;
                    }
                }
            }
            return result;
        },

        _normalizeWord: function (w) {
            return w.toLowerCase().replace(/[^a-z0-9]/g, '');
        },

        _escapeHtml: function (str) {
            var div = document.createElement('div');
            div.appendChild(document.createTextNode(str));
            return div.innerHTML;
        },

        /**
         * Handle file upload (.txt or .docx)
         */
        handleFileUpload: function (event) {
            var self = this;
            var file = event.target.files[0];
            if (!file) return;

            var name = file.name.toLowerCase();

            if (name.endsWith('.txt')) {
                var reader = new FileReader();
                reader.onload = function (e) {
                    self.inputText = e.target.result;
                    self.updateInputWordCount();
                };
                reader.readAsText(file);
            } else if (name.endsWith('.docx')) {
                // Read .docx as ArrayBuffer and extract text from XML
                var reader = new FileReader();
                reader.onload = function (e) {
                    self._extractDocxText(e.target.result).then(function (text) {
                        self.inputText = text;
                        self.updateInputWordCount();
                    }).catch(function () {
                        self.errorMessage = 'Could not read the .docx file. Please try copying and pasting your text instead.';
                    });
                };
                reader.readAsArrayBuffer(file);
            } else {
                this.errorMessage = 'Unsupported file type. Please upload a .txt or .docx file.';
            }

            // Reset file input so the same file can be selected again
            event.target.value = '';
        },

        /**
         * Extract plain text from a .docx file (ZIP containing XML)
         */
        _extractDocxText: function (arrayBuffer) {
            // Use JSZip-like approach: .docx files are ZIP archives.
            // We use the browser's built-in decompression if available,
            // otherwise fall back to a simple regex extraction on the raw XML.
            return new Promise(function (resolve, reject) {
                try {
                    // Try using the Blob/Response API to read the zip
                    var blob = new Blob([arrayBuffer]);

                    // Simple approach: read the raw bytes and find document.xml content
                    var uint8 = new Uint8Array(arrayBuffer);
                    var text = '';

                    // Convert to string to find XML content (simplified extraction)
                    var decoder = new TextDecoder('utf-8', { fatal: false });
                    var rawText = decoder.decode(uint8);

                    // Find content between <w:t> tags (Word XML text nodes)
                    var matches = rawText.match(/<w:t[^>]*>([^<]*)<\/w:t>/g);
                    if (matches && matches.length > 0) {
                        var parts = [];
                        for (var i = 0; i < matches.length; i++) {
                            var content = matches[i].replace(/<w:t[^>]*>/, '').replace(/<\/w:t>/, '');
                            parts.push(content);
                        }
                        text = parts.join('');
                        // Add paragraph breaks
                        text = text.replace(/\s{2,}/g, '\n\n');
                        resolve(text.trim());
                    } else {
                        reject('No text content found');
                    }
                } catch (e) {
                    reject(e);
                }
            });
        },

        /**
         * Load paraphrase history (premium users)
         */
        loadHistory: function () {
            var self = this;
            fetch('/api/paraphrase/history/', {
                method: 'GET',
                headers: {
                    'X-CSRFToken': self.getCsrfToken(),
                },
            })
            .then(function (resp) { return resp.json(); })
            .then(function (data) {
                if (data.history) {
                    self.historyItems = data.history;
                }
            })
            .catch(function () {
                // Silently fail - history is a convenience feature
            });
        },

        /**
         * Load a history entry back into the editor
         */
        loadFromHistory: function (item) {
            this.inputText = item.input_text;
            this.outputText = item.output_text;
            this.outputHtml = this._renderOutputWords(item.output_text);
            this.diffHtml = this.computeDiff(item.input_text, item.output_text);
            this.showDiff = false;
            this.updateInputWordCount();
            this.outputWordCount = this.countWords(item.output_text);
            this.mode = item.mode;
        },

        /**
         * Get CSRF token from cookie
         */
        getCsrfToken: function () {
            var name = 'csrftoken';
            var cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        },
    };
}
