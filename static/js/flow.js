/**
 * Flow (Co-Writer) - Alpine.js component for the full writing workspace.
 * Handles document CRUD, auto-save, rich text formatting, AI features,
 * research, notes, citations, export, and sharing.
 */
function flowEditor(isAuthenticated) {
    return {
        // ---- State ----
        isAuthenticated: isAuthenticated || false,
        documents: [],
        currentDoc: {
            uuid: null,
            title: 'Untitled Document',
            content: '',
            is_shared: false,
            share_token: null,
        },
        notes: [],
        notesChanged: false,
        wordCount: 0,
        saveStatus: 'Ready',
        saveTimer: null,
        autoSaveInterval: null,

        // UI state
        showDocList: true,
        showSidebar: false,
        sidebarTab: 'research',
        showSmartStart: false,
        showShareModal: false,
        errorMsg: '',

        // AI Suggest
        aiSuggestion: '',
        aiSuggestLoading: false,

        // Smart Start
        smartStartKeywords: '',
        smartStartLoading: false,

        // Research
        researchQuery: '',
        researchResults: [],
        researchLoading: false,

        // AI Review
        reviewData: null,
        reviewLoading: false,

        // Share
        shareUrl: '',
        shareCopied: false,

        // Citations
        citationStyle: 'apa',
        citationAuthor: '',
        citationTitle: '',
        citationYear: '',
        citationSource: '',
        generatedCitation: '',

        // ---- Init ----
        init() {
            if (this.isAuthenticated) {
                this.loadDocuments();

                // Auto-save every 30 seconds
                this.autoSaveInterval = setInterval(() => {
                    if (this.currentDoc.uuid && this.saveStatus === 'Unsaved changes') {
                        this.saveDocument();
                    }
                }, 30000);
            }

            // Auto-clear error messages after 5 seconds
            this.$watch('errorMsg', (val) => {
                if (val) {
                    setTimeout(() => { this.errorMsg = ''; }, 5000);
                }
            });
        },

        // ---- CSRF Helper ----
        getCSRF() {
            var token = document.querySelector('[name=csrfmiddlewaretoken]');
            if (token) return token.value;
            // Fallback: read from cookie
            var match = document.cookie.match(/csrftoken=([^;]+)/);
            return match ? match[1] : '';
        },

        // ---- API Helper ----
        async apiRequest(url, method, body) {
            var opts = {
                method: method || 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRF(),
                },
            };
            if (body) {
                opts.body = JSON.stringify(body);
            }
            var response = await fetch(url, opts);
            var data = await response.json();
            if (!response.ok) {
                throw new Error(data.error || 'Request failed');
            }
            return data;
        },

        // ---- Document CRUD ----
        async loadDocuments() {
            try {
                var data = await this.apiRequest('/api/flow/documents/');
                this.documents = data.documents || [];
                // Load the first document if exists, or create a new one
                if (this.documents.length > 0 && !this.currentDoc.uuid) {
                    await this.loadDocument(this.documents[0].uuid);
                } else if (this.documents.length === 0) {
                    await this.createDocument();
                }
            } catch (e) {
                this.errorMsg = 'Failed to load documents.';
            }
        },

        async createDocument() {
            try {
                var data = await this.apiRequest('/api/flow/documents/', 'POST', {
                    title: 'Untitled Document',
                    content: '',
                });
                this.currentDoc = {
                    uuid: data.uuid,
                    title: data.title,
                    content: data.content,
                    is_shared: data.is_shared,
                    share_token: null,
                };
                this.notes = [];
                this.wordCount = 0;
                this.setEditorContent('');
                this.saveStatus = 'Saved';
                await this.loadDocuments();
            } catch (e) {
                this.errorMsg = 'Failed to create document.';
            }
        },

        async loadDocument(uuid) {
            try {
                // Save current document first if there are unsaved changes
                if (this.currentDoc.uuid && this.saveStatus === 'Unsaved changes') {
                    await this.saveDocument();
                }
                var data = await this.apiRequest('/api/flow/documents/' + uuid + '/');
                this.currentDoc = {
                    uuid: data.uuid,
                    title: data.title,
                    content: data.content,
                    is_shared: data.is_shared,
                    share_token: data.share_token,
                };
                this.notes = (data.notes || []).map(function(n) {
                    return { content: n.content, id: n.id };
                });
                this.setEditorContent(data.content || '');
                this.updateWordCount();
                this.saveStatus = 'Saved';
                this.reviewData = null;
                this.aiSuggestion = '';
            } catch (e) {
                this.errorMsg = 'Failed to load document.';
            }
        },

        async saveDocument() {
            if (!this.currentDoc.uuid) return;
            this.saveStatus = 'Saving...';
            try {
                var editor = document.getElementById('editor');
                var content = editor ? editor.innerHTML : '';
                var payload = {
                    title: this.currentDoc.title,
                    content: content,
                };
                // Include notes if changed
                if (this.notesChanged) {
                    payload.notes = this.notes.map(function(n) {
                        return { content: n.content };
                    });
                    this.notesChanged = false;
                }
                var data = await this.apiRequest('/api/flow/documents/' + this.currentDoc.uuid + '/', 'PUT', payload);
                this.wordCount = data.word_count || this.wordCount;
                this.saveStatus = 'Saved';

                // Update document in the list
                var idx = this.documents.findIndex(function(d) { return d.uuid === data.uuid; });
                if (idx !== -1) {
                    this.documents[idx].title = this.currentDoc.title;
                    this.documents[idx].word_count = data.word_count;
                    this.documents[idx].updated_at = data.updated_at;
                }
            } catch (e) {
                this.saveStatus = 'Save failed';
                this.errorMsg = 'Failed to save document.';
            }
        },

        async deleteDocument(uuid) {
            if (!confirm('Are you sure you want to delete this document?')) return;
            try {
                await this.apiRequest('/api/flow/documents/' + uuid + '/', 'DELETE');
                this.documents = this.documents.filter(function(d) { return d.uuid !== uuid; });
                if (this.currentDoc.uuid === uuid) {
                    this.currentDoc = { uuid: null, title: 'Untitled Document', content: '', is_shared: false, share_token: null };
                    this.setEditorContent('');
                    this.wordCount = 0;
                    if (this.documents.length > 0) {
                        await this.loadDocument(this.documents[0].uuid);
                    } else {
                        await this.createDocument();
                    }
                }
            } catch (e) {
                this.errorMsg = 'Failed to delete document.';
            }
        },

        // ---- Editor Helpers ----
        setEditorContent(html) {
            var editor = document.getElementById('editor');
            if (editor) {
                editor.innerHTML = html;
            }
        },

        getEditorContent() {
            var editor = document.getElementById('editor');
            return editor ? editor.innerHTML : '';
        },

        getEditorText() {
            var editor = document.getElementById('editor');
            return editor ? (editor.innerText || editor.textContent || '') : '';
        },

        onEditorInput() {
            this.updateWordCount();
            this.saveStatus = 'Unsaved changes';
            // Debounced save - reset timer on each input
            clearTimeout(this.saveTimer);
            this.saveTimer = setTimeout(() => {
                this.saveDocument();
            }, 3000);
        },

        updateWordCount() {
            var text = this.getEditorText().trim();
            this.wordCount = text ? text.split(/\s+/).filter(function(w) { return w.length > 0; }).length : 0;
        },

        // ---- Rich Text Formatting ----
        formatText(command) {
            document.execCommand(command, false, null);
            document.getElementById('editor').focus();
        },

        formatBlock(tag) {
            document.execCommand('formatBlock', false, '<' + tag + '>');
            document.getElementById('editor').focus();
        },

        insertLink() {
            var url = prompt('Enter URL:');
            if (url) {
                document.execCommand('createLink', false, url);
                document.getElementById('editor').focus();
            }
        },

        // ---- AI Suggest ----
        async aiSuggest() {
            if (this.aiSuggestLoading) return;
            this.aiSuggestLoading = true;
            this.aiSuggestion = '';
            try {
                var content = this.getEditorContent();
                var data = await this.apiRequest('/api/flow/ai-suggest/', 'POST', {
                    content: content,
                });
                this.aiSuggestion = data.suggestion || '';
            } catch (e) {
                this.errorMsg = e.message || 'Failed to get AI suggestion.';
            } finally {
                this.aiSuggestLoading = false;
            }
        },

        acceptSuggestion() {
            if (!this.aiSuggestion) return;
            var editor = document.getElementById('editor');
            if (editor) {
                // Append the suggestion at the end
                editor.focus();
                document.execCommand('insertText', false, ' ' + this.aiSuggestion);
                this.aiSuggestion = '';
                this.onEditorInput();
            }
        },

        // ---- AI Review ----
        async getAIReview() {
            if (this.reviewLoading) return;
            var text = this.getEditorText().trim();
            if (!text) {
                this.errorMsg = 'Please write some content before requesting a review.';
                return;
            }
            this.reviewLoading = true;
            this.reviewData = null;
            try {
                var content = this.getEditorContent();
                var data = await this.apiRequest('/api/flow/ai-review/', 'POST', {
                    content: content,
                });
                this.reviewData = data.review || null;
            } catch (e) {
                this.errorMsg = e.message || 'Failed to get AI review.';
            } finally {
                this.reviewLoading = false;
            }
        },

        // ---- Smart Start ----
        async runSmartStart() {
            if (this.smartStartLoading || !this.smartStartKeywords.trim()) return;
            this.smartStartLoading = true;
            try {
                var data = await this.apiRequest('/api/flow/smart-start/', 'POST', {
                    keywords: this.smartStartKeywords,
                });
                if (data.outline) {
                    this.setEditorContent(data.outline);
                    this.onEditorInput();
                    this.showSmartStart = false;
                    this.smartStartKeywords = '';
                }
            } catch (e) {
                this.errorMsg = e.message || 'Failed to generate outline.';
            } finally {
                this.smartStartLoading = false;
            }
        },

        // ---- Research ----
        async searchResearch() {
            if (this.researchLoading || !this.researchQuery.trim()) return;
            this.researchLoading = true;
            this.researchResults = [];
            try {
                // Use a simple GET approach with query param
                var response = await fetch('/api/flow/ai-suggest/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': this.getCSRF(),
                    },
                    body: JSON.stringify({
                        content: 'Research query: ' + this.researchQuery,
                    }),
                });
                // For now, show placeholder results since research_search is a placeholder
                this.researchResults = [
                    {
                        title: 'Search: ' + this.researchQuery,
                        snippet: 'Web search integration coming soon. Use the AI Suggest feature to get writing assistance based on your topic.',
                        url: '#',
                    }
                ];
            } catch (e) {
                this.errorMsg = 'Research search is not yet available.';
            } finally {
                this.researchLoading = false;
            }
        },

        // ---- Notes ----
        addNote() {
            this.notes.push({ content: '', id: null });
            this.notesChanged = true;
        },

        deleteNote(idx) {
            this.notes.splice(idx, 1);
            this.notesChanged = true;
        },

        // ---- Citations ----
        generateCitation() {
            var author = this.citationAuthor.trim();
            var title = this.citationTitle.trim();
            var year = this.citationYear.trim();
            var source = this.citationSource.trim();

            if (!author && !title) {
                this.errorMsg = 'Please provide at least an author or title.';
                return;
            }

            var citation = '';
            switch (this.citationStyle) {
                case 'apa':
                    citation = (author || 'Unknown') + ' (' + (year || 'n.d.') + '). ' +
                               (title ? title + '. ' : '') +
                               (source || '') + '.';
                    break;
                case 'mla':
                    citation = (author || 'Unknown') + '. "' + (title || 'Untitled') + '." ' +
                               (source ? source + ', ' : '') + (year || '') + '.';
                    break;
                case 'chicago':
                    citation = (author || 'Unknown') + '. "' + (title || 'Untitled') + '." ' +
                               (source || '') + (year ? ' (' + year + ')' : '') + '.';
                    break;
                case 'harvard':
                    citation = (author || 'Unknown') + ' (' + (year || 'n.d.') + ') ' +
                               (title ? "'" + title + "', " : '') +
                               (source || '') + '.';
                    break;
                case 'ieee':
                    citation = (author || 'Unknown') + ', "' + (title || 'Untitled') + '," ' +
                               (source || '') + (year ? ', ' + year : '') + '.';
                    break;
                default:
                    citation = author + '. ' + title + '. ' + source + ' ' + year + '.';
            }
            this.generatedCitation = citation.replace(/\.\./g, '.').replace(/\s+/g, ' ').trim();
        },

        insertCitation() {
            if (!this.generatedCitation) return;
            var editor = document.getElementById('editor');
            if (editor) {
                editor.focus();
                document.execCommand('insertText', false, ' (' + this.generatedCitation + ')');
                this.onEditorInput();
            }
        },

        // ---- Export ----
        exportDoc(format) {
            var content = '';
            var filename = (this.currentDoc.title || 'document').replace(/[^a-z0-9]/gi, '_');
            var mimeType = 'text/plain';

            switch (format) {
                case 'txt':
                    content = this.getEditorText();
                    filename += '.txt';
                    mimeType = 'text/plain';
                    break;
                case 'html':
                    content = '<!DOCTYPE html><html><head><meta charset="utf-8"><title>' +
                              (this.currentDoc.title || 'Document') +
                              '</title></head><body>' +
                              this.getEditorContent() +
                              '</body></html>';
                    filename += '.html';
                    mimeType = 'text/html';
                    break;
                case 'md':
                    content = this.htmlToMarkdown(this.getEditorContent());
                    filename += '.md';
                    mimeType = 'text/markdown';
                    break;
                default:
                    content = this.getEditorText();
                    filename += '.txt';
            }

            var blob = new Blob([content], { type: mimeType + ';charset=utf-8' });
            var url = URL.createObjectURL(blob);
            var a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        },

        htmlToMarkdown(html) {
            // Basic HTML to Markdown conversion
            var md = html;
            md = md.replace(/<h1[^>]*>(.*?)<\/h1>/gi, '# $1\n\n');
            md = md.replace(/<h2[^>]*>(.*?)<\/h2>/gi, '## $1\n\n');
            md = md.replace(/<h3[^>]*>(.*?)<\/h3>/gi, '### $1\n\n');
            md = md.replace(/<h4[^>]*>(.*?)<\/h4>/gi, '#### $1\n\n');
            md = md.replace(/<strong[^>]*>(.*?)<\/strong>/gi, '**$1**');
            md = md.replace(/<b[^>]*>(.*?)<\/b>/gi, '**$1**');
            md = md.replace(/<em[^>]*>(.*?)<\/em>/gi, '*$1*');
            md = md.replace(/<i[^>]*>(.*?)<\/i>/gi, '*$1*');
            md = md.replace(/<u[^>]*>(.*?)<\/u>/gi, '$1');
            md = md.replace(/<a[^>]*href="([^"]*)"[^>]*>(.*?)<\/a>/gi, '[$2]($1)');
            md = md.replace(/<li[^>]*>(.*?)<\/li>/gi, '- $1\n');
            md = md.replace(/<\/?(ul|ol|div|span|br|p)[^>]*>/gi, '\n');
            md = md.replace(/<[^>]+>/g, '');
            md = md.replace(/&nbsp;/g, ' ');
            md = md.replace(/&amp;/g, '&');
            md = md.replace(/&lt;/g, '<');
            md = md.replace(/&gt;/g, '>');
            md = md.replace(/\n{3,}/g, '\n\n');
            return md.trim();
        },

        // ---- Share ----
        async toggleShare() {
            if (!this.currentDoc.uuid) return;

            // If already shared, show the existing share URL without unsharing
            if (this.currentDoc.is_shared && this.currentDoc.share_token) {
                this.shareUrl = window.location.origin + '/flow/shared/' + this.currentDoc.share_token + '/';
                this.showShareModal = true;
                this.shareCopied = false;
                return;
            }

            try {
                var data = await this.apiRequest('/api/flow/share/', 'POST', {
                    uuid: this.currentDoc.uuid,
                });
                this.currentDoc.is_shared = data.is_shared;
                if (data.is_shared && data.share_url) {
                    this.currentDoc.share_token = data.share_token;
                    this.shareUrl = data.share_url;
                    this.showShareModal = true;
                    this.shareCopied = false;
                } else {
                    this.shareUrl = '';
                    this.showShareModal = false;
                }
            } catch (e) {
                this.errorMsg = e.message || 'Failed to toggle sharing.';
            }
        },

        async unshareDocument() {
            if (!this.currentDoc.uuid) return;
            try {
                var data = await this.apiRequest('/api/flow/share/', 'POST', {
                    uuid: this.currentDoc.uuid,
                });
                this.currentDoc.is_shared = false;
                this.currentDoc.share_token = null;
                this.shareUrl = '';
                this.showShareModal = false;
            } catch (e) {
                this.errorMsg = e.message || 'Failed to unshare document.';
            }
        },

        copyShareLink() {
            if (!this.shareUrl) return;
            var self = this;
            navigator.clipboard.writeText(this.shareUrl).then(function() {
                self.shareCopied = true;
                setTimeout(function() { self.shareCopied = false; }, 2000);
            }).catch(function() {
                // Fallback for older browsers
                var input = document.createElement('input');
                input.value = self.shareUrl;
                document.body.appendChild(input);
                input.select();
                document.execCommand('copy');
                document.body.removeChild(input);
                self.shareCopied = true;
                setTimeout(function() { self.shareCopied = false; }, 2000);
            });
        },

        // ---- Utility ----
        formatDate(isoString) {
            if (!isoString) return '';
            var d = new Date(isoString);
            var now = new Date();
            var diff = now - d;
            // Less than a minute
            if (diff < 60000) return 'Just now';
            // Less than an hour
            if (diff < 3600000) return Math.floor(diff / 60000) + 'm ago';
            // Less than a day
            if (diff < 86400000) return Math.floor(diff / 3600000) + 'h ago';
            // Less than a week
            if (diff < 604800000) return Math.floor(diff / 86400000) + 'd ago';
            // Otherwise show date
            return d.toLocaleDateString();
        },
    };
}
