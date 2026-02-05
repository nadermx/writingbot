/**
 * WritingBot.ai - Utility Functions
 * Common utilities used across all tools.
 */
var wb = (function () {
    'use strict';

    return {
        // API helpers
        api: api,
        apiJson: apiJson,
        getCookie: getCookie,
        getCSRFToken: getCSRFToken,

        // UI helpers
        showNotification: showNotification,
        copyToClipboard: copyToClipboard,
        countWords: countWords,
        countChars: countChars,
        debounce: debounce,
        formatNumber: formatNumber,
        secondsToTime: secondsToTime,

        // Legacy compatibility
        showNoCredits: showNoCredits,
        showRateLimitModal: showRateLimitModal,
        showSizeExceededModal: showSizeExceededModal,
    };

    /**
     * Make an API request using fetch.
     */
    function api(endpoint, method, data, options) {
        var config = {
            method: method || 'GET',
            headers: {
                'X-CSRFToken': getCSRFToken(),
            },
            credentials: 'same-origin',
        };

        if (data) {
            if (data instanceof FormData) {
                config.body = data;
            } else {
                config.headers['Content-Type'] = 'application/json';
                config.body = JSON.stringify(data);
            }
        }

        if (options) {
            Object.assign(config, options);
        }

        return fetch(endpoint, config);
    }

    /**
     * Make an API request and parse JSON response.
     */
    function apiJson(endpoint, method, data) {
        return api(endpoint, method, data).then(function (response) {
            if (!response.ok) {
                return response.json().then(function (err) {
                    throw err;
                });
            }
            return response.json();
        });
    }

    function getCookie(name) {
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
    }

    function getCSRFToken() {
        var token = getCookie('csrftoken');
        if (!token) {
            var meta = document.querySelector('meta[name="csrf-token"]');
            if (meta) token = meta.getAttribute('content');
        }
        return token || '';
    }

    function showNotification(message, type) {
        type = type || 'info';
        var colors = {
            success: 'bg-green-500',
            error: 'bg-red-500',
            warning: 'bg-yellow-500',
            info: 'bg-indigo-500',
        };

        var toast = document.createElement('div');
        toast.className = 'fixed top-4 right-4 z-50 px-6 py-3 rounded-lg text-white shadow-lg transition-all transform translate-x-full ' + (colors[type] || colors.info);
        toast.textContent = message;
        document.body.appendChild(toast);

        requestAnimationFrame(function () {
            toast.classList.remove('translate-x-full');
        });

        setTimeout(function () {
            toast.classList.add('translate-x-full');
            setTimeout(function () { toast.remove(); }, 300);
        }, 3000);
    }

    function copyToClipboard(text) {
        if (navigator.clipboard) {
            navigator.clipboard.writeText(text).then(function () {
                showNotification('Copied to clipboard!', 'success');
            });
        } else {
            var textarea = document.createElement('textarea');
            textarea.value = text;
            document.body.appendChild(textarea);
            textarea.select();
            document.execCommand('copy');
            textarea.remove();
            showNotification('Copied to clipboard!', 'success');
        }
    }

    function countWords(text) {
        if (!text || !text.trim()) return 0;
        return text.trim().split(/\s+/).length;
    }

    function countChars(text) {
        if (!text) return 0;
        return text.length;
    }

    function debounce(func, wait) {
        var timeout;
        return function () {
            var context = this, args = arguments;
            clearTimeout(timeout);
            timeout = setTimeout(function () {
                func.apply(context, args);
            }, wait);
        };
    }

    function formatNumber(num) {
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    }

    function secondsToTime(totalSeconds) {
        var h = Math.floor(totalSeconds / 3600);
        var m = Math.floor((totalSeconds - h * 3600) / 60);
        var s = totalSeconds - h * 3600 - m * 60;
        return (h < 10 ? '0' : '') + h + ':' + (m < 10 ? '0' : '') + m + ':' + (s < 10 ? '0' : '') + s;
    }

    function showNoCredits() {
        showNotification('No credits remaining. Please upgrade your plan.', 'warning');
    }

    function showRateLimitModal() {
        showNotification('Rate limit reached. Please wait before trying again.', 'warning');
    }

    function showSizeExceededModal() {
        showNotification('File size exceeds the maximum allowed limit.', 'error');
    }
}());
