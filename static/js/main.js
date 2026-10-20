// main.js - 2026 Konkan Guide Performance & Instant Interaction Engine
(function() {
    'use strict';

    // --------------------------------------------------------------------------
    // 1. LIGHTWEIGHT ACCESSIBLE TOAST SYSTEM
    // --------------------------------------------------------------------------
    window.showToast = function(message, type = 'info') {
        let container = document.getElementById('toast-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toast-container';
            container.className = 'fixed bottom-20 sm:bottom-6 right-4 sm:right-6 z-50 flex flex-col gap-2 max-w-xs pointer-events-none';
            document.body.appendChild(container);
        }

        const toast = document.createElement('div');
        const bgColors = {
            success: 'bg-emerald-900 text-white border-emerald-700 shadow-emerald-900/30',
            info: 'bg-slate-900 text-white border-slate-700 shadow-slate-900/30',
            warning: 'bg-amber-900 text-white border-amber-700 shadow-amber-900/30',
            error: 'bg-rose-900 text-white border-rose-700 shadow-rose-900/30'
        };

        const icons = {
            success: 'fa-check-circle text-emerald-400',
            info: 'fa-circle-info text-sky-400',
            warning: 'fa-triangle-exclamation text-amber-400',
            error: 'fa-circle-exclamation text-rose-400'
        };

        const colorClass = bgColors[type] || bgColors.info;
        const iconClass = icons[type] || icons.info;

        toast.className = `flex items-center gap-2.5 px-4 py-3 rounded-2xl shadow-xl border text-xs font-semibold transform transition-all duration-300 translate-y-3 opacity-0 pointer-events-auto ${colorClass}`;
        toast.innerHTML = `<i class="fas ${iconClass} text-sm flex-shrink-0"></i><span>${message}</span>`;

        container.appendChild(toast);

        // Animate in
        requestAnimationFrame(() => {
            toast.classList.remove('translate-y-3', 'opacity-0');
            toast.classList.add('translate-y-0', 'opacity-100');
        });

        // Auto dismiss
        setTimeout(() => {
            toast.classList.remove('translate-y-0', 'opacity-100');
            toast.classList.add('translate-y-2', 'opacity-0');
            setTimeout(() => toast.remove(), 300);
        }, 3200);
    };

    // --------------------------------------------------------------------------
    // 2. DOUBLE-CLICK PREVENTION & BUTTON FEEDBACK
    // --------------------------------------------------------------------------
    document.addEventListener('submit', function(e) {
        const form = e.target;
        if (form.getAttribute('data-no-lock') !== null) return;

        const submitBtn = form.querySelector('button[type="submit"], input[type="submit"]');
        if (submitBtn && !submitBtn.disabled) {
            submitBtn.style.pointerEvents = 'none';
            submitBtn.classList.add('opacity-75', 'cursor-wait');

            // Insert mini spinner if it's a standard button
            if (submitBtn.tagName === 'BUTTON' && !submitBtn.querySelector('.fa-spinner')) {
                const spinner = document.createElement('i');
                spinner.className = 'fas fa-spinner fa-spin mr-1.5 text-xs';
                submitBtn.prepend(spinner);
            }

            // Fallback unlock in 8s in case network stalls
            setTimeout(() => {
                submitBtn.style.pointerEvents = 'auto';
                submitBtn.classList.remove('opacity-75', 'cursor-wait');
                const spin = submitBtn.querySelector('.fa-spinner');
                if (spin) spin.remove();
            }, 8000);
        }
    });

    // --------------------------------------------------------------------------
    // 3. OPTIMISTIC UI: SAVE TO TRIP / BOOKMARK
    // --------------------------------------------------------------------------
    window.updateMobileBadge = function() {
        let saved = [];
        try {
            saved = JSON.parse(localStorage.getItem('konkan_saved_places') || localStorage.getItem('konkan_saved_trip') || '[]');
        } catch (e) {
            saved = [];
        }
        const badge = document.getElementById('mobile-trip-count-badge');
        if (badge) {
            if (saved.length > 0) {
                badge.innerText = saved.length;
                badge.classList.remove('hidden');
            } else {
                badge.classList.add('hidden');
            }
        }
    };

    window.savePlaceToTrip = function(id, title, category, slug, btn) {
        let saved = [];
        try {
            saved = JSON.parse(localStorage.getItem('konkan_saved_places') || localStorage.getItem('konkan_saved_trip') || '[]');
        } catch (err) {
            saved = [];
        }

        const existingIdx = saved.findIndex(item => String(item.id) === String(id));
        const cleanTitle = title || 'Place';

        if (existingIdx !== -1) {
            // Remove from saved trip
            saved.splice(existingIdx, 1);
            localStorage.setItem('konkan_saved_places', JSON.stringify(saved));
            localStorage.setItem('konkan_saved_trip', JSON.stringify(saved));

            if (btn) {
                const icon = btn.querySelector('i');
                if (icon) icon.className = 'far fa-bookmark text-slate-400';
                btn.classList.remove('text-ocean-mid', 'bg-emerald-50');
            }
            window.showToast(`Removed "${cleanTitle}" from your trip`, 'info');
        } else {
            // Add to saved trip
            saved.push({
                id: String(id),
                title: cleanTitle,
                category: category || 'Landmark',
                slug: slug || '',
                addedAt: new Date().toISOString()
            });
            localStorage.setItem('konkan_saved_places', JSON.stringify(saved));
            localStorage.setItem('konkan_saved_trip', JSON.stringify(saved));

            if (btn) {
                const icon = btn.querySelector('i');
                if (icon) {
                    icon.className = 'fas fa-bookmark text-ocean-mid animate-bounce';
                    setTimeout(() => icon.classList.remove('animate-bounce'), 800);
                }
                btn.classList.add('text-ocean-mid');
            }
            window.showToast(`Saved "${cleanTitle}" to your trip!`, 'success');
        }

        window.updateMobileBadge();
        window.dispatchEvent(new Event('storage'));
    };

    function initOptimisticTripSaves() {
        document.addEventListener('click', function(e) {
            const btn = e.target.closest('[data-save-trip]');
            if (!btn) return;

            e.preventDefault();
            e.stopPropagation();

            const placeId = btn.getAttribute('data-save-trip');
            const placeTitle = btn.getAttribute('data-place-title') || 'Place';
            const placeCategory = btn.getAttribute('data-place-category') || 'Landmark';
            const placeSlug = btn.getAttribute('data-place-slug') || '';

            window.savePlaceToTrip(placeId, placeTitle, placeCategory, placeSlug, btn);
        });
    }

    function syncSavedBookmarkIcons() {
        let saved = [];
        try {
            saved = JSON.parse(localStorage.getItem('konkan_saved_places') || localStorage.getItem('konkan_saved_trip') || '[]');
        } catch (e) {
            saved = [];
        }
        const savedIds = new Set(saved.map(s => String(s.id)));

        document.querySelectorAll('[data-save-trip]').forEach(btn => {
            const id = btn.getAttribute('data-save-trip');
            const icon = btn.querySelector('i');
            if (savedIds.has(String(id))) {
                if (icon) icon.className = 'fas fa-bookmark text-ocean-mid';
                btn.classList.add('text-ocean-mid');
            } else {
                if (icon) icon.className = 'far fa-bookmark text-slate-400';
                btn.classList.remove('text-ocean-mid');
            }
        });

        window.updateMobileBadge();
    }

    // --------------------------------------------------------------------------
    // 4. INSTANT DEBOUNCED LIVE SEARCH WITH ABORTCONTROLLER
    // --------------------------------------------------------------------------
    function initInstantSearch() {
        const searchInput = document.getElementById('search-input-modal');
        const resultsContainer = document.getElementById('modal-search-results');
        if (!searchInput || !resultsContainer) return;

        let debounceTimer = null;
        let activeAbortController = null;

        searchInput.addEventListener('input', function() {
            const q = searchInput.value.trim();
            clearTimeout(debounceTimer);

            if (activeAbortController) {
                activeAbortController.abort();
            }

            if (q.length < 2) {
                resultsContainer.innerHTML = '';
                resultsContainer.classList.add('hidden');
                return;
            }

            debounceTimer = setTimeout(() => {
                activeAbortController = new AbortController();
                resultsContainer.classList.remove('hidden');
                resultsContainer.innerHTML = `
                    <div class="p-4 text-center text-xs text-slate-400">
                        <i class="fas fa-spinner fa-spin mr-1.5 text-ocean-mid"></i> Searching Ratnagiri...
                    </div>
                `;

                fetch(`/search/?format=json&q=${encodeURIComponent(q)}`, {
                    signal: activeAbortController.signal,
                    headers: { 'X-Requested-With': 'XMLHttpRequest' }
                })
                .then(res => {
                    if (!res.ok) throw new Error('Search failed');
                    return res.json();
                })
                .then(data => {
                    renderLiveSearchResults(data, resultsContainer);
                })
                .catch(err => {
                    if (err.name !== 'AbortError') {
                        resultsContainer.innerHTML = '<div class="p-3 text-xs text-rose-500 text-center">Search error. Press Enter for full results.</div>';
                    }
                });
            }, 200);
        });
    }

    function renderLiveSearchResults(data, container) {
        const hasDest = data.destinations && data.destinations.length > 0;
        const hasSpots = data.spots && data.spots.length > 0;
        const hasFood = data.food && data.food.length > 0;

        if (!hasDest && !hasSpots && !hasFood) {
            container.innerHTML = '<div class="p-4 text-center text-xs text-slate-400">No matching places found. Try "Beach", "Fort", or "Mango".</div>';
            return;
        }

        let html = '<div class="p-2 space-y-1 max-h-80 overflow-y-auto">';
        
        if (hasDest) {
            html += '<div class="text-[10px] uppercase font-bold tracking-wider text-slate-400 px-3 py-1">Landmarks & Beaches</div>';
            data.destinations.forEach(item => {
                const imgHtml = item.image 
                    ? `<img src="${item.image}" alt="${item.title || ''}" class="w-9 h-9 rounded-lg object-cover flex-shrink-0 bg-slate-200" loading="lazy">` 
                    : `<div class="w-9 h-9 rounded-lg bg-sky-100 flex items-center justify-center text-sky-600 flex-shrink-0"><i class="fas fa-map-pin text-xs"></i></div>`;
                html += `
                    <a href="${item.url || '#'}" class="flex items-center gap-3 p-2 rounded-xl hover:bg-slate-100 transition-colors group">
                        ${imgHtml}
                        <div class="min-w-0 flex-1">
                            <div class="text-xs font-bold text-slate-800 group-hover:text-ocean-mid truncate">${item.title || ''}</div>
                            <div class="text-[10px] text-slate-500 truncate">${item.category || ''} • ${item.location || 'Ratnagiri'}</div>
                        </div>
                        <i class="fas fa-chevron-right text-[10px] text-slate-300 group-hover:text-ocean-mid"></i>
                    </a>
                `;
            });
        }

        if (hasFood) {
            html += '<div class="text-[10px] uppercase font-bold tracking-wider text-slate-400 px-3 py-1 mt-2">Local Flavors</div>';
            data.food.forEach(item => {
                const imgHtml = item.image 
                    ? `<img src="${item.image}" alt="${item.title || ''}" class="w-9 h-9 rounded-lg object-cover flex-shrink-0 bg-slate-200" loading="lazy">` 
                    : `<div class="w-9 h-9 rounded-lg bg-amber-100 flex items-center justify-center text-amber-600 flex-shrink-0"><i class="fas fa-utensils text-xs"></i></div>`;
                html += `
                    <a href="${item.url || '#'}" class="flex items-center gap-3 p-2 rounded-xl hover:bg-slate-100 transition-colors group">
                        ${imgHtml}
                        <div class="min-w-0 flex-1">
                            <div class="text-xs font-bold text-slate-800 group-hover:text-sand-coral truncate">${item.title || ''}</div>
                            <div class="text-[10px] text-slate-500">Konkan Cuisine</div>
                        </div>
                        <i class="fas fa-chevron-right text-[10px] text-slate-300 group-hover:text-sand-coral"></i>
                    </a>
                `;
            });
        }

        html += '</div>';
        container.innerHTML = html;
    }

    // --------------------------------------------------------------------------
    // 5. SMART LINK PREFETCHING ON HOVER / TOUCHSTART
    // --------------------------------------------------------------------------
    function initSmartPrefetching() {
        // Skip on Data Saver mode
        if (navigator.connection && (navigator.connection.saveData || navigator.connection.effectiveType === '2g')) {
            return;
        }

        const prefetchedUrls = new Set();

        function prefetch(url) {
            if (!url || prefetchedUrls.has(url) || (url.startsWith('http') && !url.includes(window.location.host))) return;
            prefetchedUrls.add(url);

            const link = document.createElement('link');
            link.rel = 'prefetch';
            link.href = url;
            document.head.appendChild(link);
        }

        document.addEventListener('mouseover', function(e) {
            const a = e.target.closest('a[href^="/itineraries/"], a[href^="/destinations/"], a[href^="/companion/"], a[href^="/near-me/"], a[href^="/food/"], a[href^="/spots/"]');
            if (a && a.href) {
                prefetch(a.href);
            }
        }, { passive: true });

        document.addEventListener('touchstart', function(e) {
            const a = e.target.closest('a[href^="/itineraries/"], a[href^="/destinations/"], a[href^="/companion/"], a[href^="/near-me/"], a[href^="/food/"], a[href^="/spots/"]');
            if (a && a.href) {
                prefetch(a.href);
            }
        }, { passive: true });
    }

    // --------------------------------------------------------------------------
    // 6. NETWORK STATUS & OFFLINE DETECTION
    // --------------------------------------------------------------------------
    function initNetworkMonitor() {
        window.addEventListener('online', function() {
            window.showToast('You are back online!', 'success');
        });

        window.addEventListener('offline', function() {
            window.showToast('You are offline. Saved trips and guides remain available.', 'warning');
        });
    }

    // --------------------------------------------------------------------------
    // INITIALIZATION
    // --------------------------------------------------------------------------
    document.addEventListener('DOMContentLoaded', function() {
        // Header Scroll
        const header = document.getElementById('main-header');
        if (header) {
            window.addEventListener('scroll', function() {
                if (window.scrollY > 30) {
                    header.classList.add('bg-white/95', 'shadow-md', 'border-slate-200/90');
                    header.classList.remove('bg-white/80', 'border-slate-200/60');
                } else {
                    header.classList.remove('bg-white/95', 'shadow-md', 'border-slate-200/90');
                    header.classList.add('bg-white/80', 'border-slate-200/60');
                }
            }, { passive: true });
        }

        // Search Modal Keybindings
        const searchModal = document.getElementById('search-modal');
        if (searchModal) {
            window.addEventListener('keydown', function(e) {
                if (e.key === 'Escape' && !searchModal.classList.contains('hidden')) {
                    searchModal.classList.add('hidden');
                }
                if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
                    e.preventDefault();
                    searchModal.classList.remove('hidden');
                    const searchInput = document.getElementById('search-input-modal');
                    if (searchInput) searchInput.focus();
                }
            });

            searchModal.addEventListener('click', function(e) {
                if (e.target === searchModal) {
                    searchModal.classList.add('hidden');
                }
            });
        }

        // Initialize Engine Modules
        initOptimisticTripSaves();
        syncSavedBookmarkIcons();
        initInstantSearch();
        initSmartPrefetching();
        initNetworkMonitor();
    });

})();
