(function () {
  var THEME_KEY = 'klio-theme';

  function getSavedTheme() {
    try {
      var saved = localStorage.getItem(THEME_KEY);
      if (saved === 'light' || saved === 'dark') return saved;
    } catch (e) { }
    return 'dark';
  }

  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    try {
      localStorage.setItem(THEME_KEY, theme);
    } catch (e) { }
    window.dispatchEvent(new CustomEvent('klio:themechange', { detail: { theme: theme } }));
    updateThemeButtons(theme);
  }

  var scriptEl = document.currentScript || document.querySelector('script[data-klio-shell]');

  function getBasePath() {
    if (scriptEl && scriptEl.getAttribute('data-base') !== null) {
      return scriptEl.getAttribute('data-base');
    }
    var path = window.location.pathname;
    if (path.indexOf('/reports/') !== -1 || path.indexOf('/tools/') !== -1 || path.indexOf('/bookmark/') !== -1) {
      return '../';
    }
    return './';
  }

  var BASE = getBasePath();
  var MODE = (scriptEl && scriptEl.getAttribute('data-mode')) || 'page';

  function detectActiveNav() {
    if (scriptEl && scriptEl.getAttribute('data-active')) {
      return scriptEl.getAttribute('data-active');
    }
    var p = window.location.pathname;
    if (p.indexOf('/tools/') !== -1) return 'tools';
    if (p.indexOf('/bookmark/') !== -1) return 'bookmarks';
    if (p.indexOf('new.html') !== -1) return 'new';
    return 'reports';
  }

  var SUN_SVG =
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg>';
  var MOON_SVG =
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';
  var MENU_SVG =
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="4" y1="6" x2="20" y2="6"/><line x1="4" y1="12" x2="20" y2="12"/><line x1="4" y1="18" x2="20" y2="18"/></svg>';

  function updateThemeButtons(theme) {
    var btns = document.querySelectorAll('[data-klio-theme-toggle]');
    for (var i = 0; i < btns.length; i++) {
      var isDark = theme === 'dark';
      btns[i].setAttribute('aria-label', isDark ? '切換為淺色模式' : '切換為深色模式');
      btns[i].setAttribute('title', isDark ? '切換為淺色模式' : '切換為深色模式');
      btns[i].innerHTML = (isDark ? SUN_SVG : MOON_SVG) + '<span class="klio-contact-label">' + (isDark ? '淺色' : '深色') + '</span>';
    }
  }

  // Apply saved theme immediately before paint (skip root theme override on standalone tool apps)
  if (MODE === 'tool') {
    document.documentElement.setAttribute('data-klio-mode', 'tool');
  } else {
    applyTheme(getSavedTheme());
  }

  function injectToolDock() {
    if (document.querySelector('.klio-tool-dock')) return;
    var dock = document.createElement('div');
    dock.className = 'klio-tool-dock';
    dock.innerHTML =
      '<div class="klio-tool-menu" id="klio-tool-menu" role="menu" aria-label="KLIO 站內導覽">' +
      '<a href="' + BASE + 'index.html">觀察筆記</a>' +
      '<a href="' + BASE + 'tools/index.html">工具箱總覽</a>' +
      '<a href="' + BASE + 'bookmark/index.html">靈感書籤</a>' +
      '<a href="' + BASE + 'new.html">更新日誌</a>' +
      '</div>' +
      '<button type="button" class="klio-tool-pill" id="klio-tool-pill" aria-expanded="false" aria-controls="klio-tool-menu">' +
      '<span>KLIO<span class="klio-brand-dot">.</span></span>' +
      '<span style="font-weight:500;font-size:0.78rem;color:var(--klio-text-secondary);">導覽</span>' +
      '</button>';
    document.body.appendChild(dock);

    var pill = document.getElementById('klio-tool-pill');
    var menu = document.getElementById('klio-tool-menu');
    pill.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = menu.classList.toggle('is-open');
      pill.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    document.addEventListener('click', function () {
      menu.classList.remove('is-open');
      pill.setAttribute('aria-expanded', 'false');
    });
  }

  function injectShell() {
    if (MODE === 'tool') {
      injectToolDock();
      return;
    }

    if (document.querySelector('.klio-header')) return;

    document.body.classList.add('klio-body');
    var active = detectActiveNav();

    var navItems = [
      { id: 'reports', label: '觀察筆記', href: BASE + 'index.html' },
      { id: 'tools', label: '工具箱', href: BASE + 'tools/index.html' },
      { id: 'bookmarks', label: '靈感書籤', href: BASE + 'bookmark/index.html' },
      { id: 'new', label: '更新日誌', href: BASE + 'new.html' }
    ];

    var navLinksHtml = navItems
      .map(function (item) {
        var cls = 'klio-nav-link' + (active === item.id ? ' is-active' : '');
        return '<a class="' + cls + '" href="' + item.href + '">' + item.label + '</a>';
      })
      .join('');

    var header = document.createElement('header');
    header.className = 'klio-header';
    header.innerHTML =
      '<div class="klio-header-inner">' +
      '<a class="klio-brand" href="' + BASE + 'index.html">KLIO<span class="klio-brand-dot">.</span></a>' +
      '<nav class="klio-nav" aria-label="主導覽列">' + navLinksHtml + '</nav>' +
      '<div class="klio-header-actions">' +
      '<button type="button" class="klio-icon-btn" data-klio-theme-toggle></button>' +
      '<button type="button" class="klio-icon-btn klio-mobile-toggle" data-klio-menu-toggle aria-label="開啟選單" aria-expanded="false">' + MENU_SVG + '</button>' +
      '</div>' +
      '</div>';

    var drawer = document.createElement('div');
    drawer.className = 'klio-mobile-drawer';
    drawer.setAttribute('aria-label', '行動版導覽選單');
    drawer.innerHTML = navLinksHtml;

    document.body.insertBefore(drawer, document.body.firstChild);
    document.body.insertBefore(header, document.body.firstChild);

    if (!document.querySelector('.klio-footer')) {
      var footer = document.createElement('footer');
      footer.className = 'klio-footer';
      footer.innerHTML =
        '<div class="klio-footer-inner">' +
        '<span>KLIO. — Think Smart, Look Amazing</span>' +
        '<div class="klio-footer-links">' +
        '<a href="' + BASE + 'index.html">觀察筆記</a>' +
        '<a href="' + BASE + 'tools/index.html">工具箱</a>' +
        '<a href="' + BASE + 'bookmark/index.html">靈感書籤</a>' +
        '<a href="' + BASE + 'new.html">更新日誌</a>' +
        '</div>' +
        '</div>';
      document.body.appendChild(footer);
    }

    updateThemeButtons(getSavedTheme());

    header.querySelector('[data-klio-theme-toggle]').addEventListener('click', function () {
      var current = document.documentElement.getAttribute('data-theme') || 'dark';
      applyTheme(current === 'dark' ? 'light' : 'dark');
    });

    var menuBtn = header.querySelector('[data-klio-menu-toggle]');
    menuBtn.addEventListener('click', function () {
      var open = drawer.classList.toggle('is-open');
      menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        drawer.classList.remove('is-open');
      }
    });

    enhanceArticleReading();
  }

  function enhanceArticleReading() {
    var page = document.querySelector('.klio-article-page');
    var prose = document.querySelector('.klio-prose');
    if (!page || !prose) return;

    // 1. Reading time
    var text = (prose.textContent || '').trim();
    var cjkCount = (text.match(/[\u4e00-\u9fff]/g) || []).length;
    var wordCount = (text.replace(/[\u4e00-\u9fff]/g, ' ').match(/[A-Za-z0-9_]+/g) || []).length;
    var minutes = Math.max(1, Math.round(cjkCount / 380 + wordCount / 220));

    var headerMeta = document.querySelector('.klio-article-header > div');
    if (headerMeta && !document.querySelector('.klio-reading-meta')) {
      var metaSpan = document.createElement('span');
      metaSpan.className = 'klio-reading-meta';
      metaSpan.textContent = '· 約 ' + minutes + ' 分鐘閱讀';
      headerMeta.appendChild(metaSpan);
    }

    // 2. Build 2-column layout (Main column + Sticky Sidebar) on desktop
    var layout = document.querySelector('.klio-article-layout');
    if (!layout) {
      layout = document.createElement('div');
      layout.className = 'klio-article-layout';
      var mainCol = document.createElement('div');
      mainCol.className = 'klio-article-main';
      var sidebar = document.createElement('aside');
      sidebar.className = 'klio-article-sidebar';
      sidebar.setAttribute('aria-label', '文章導覽與延伸閱讀');

      var headerEl = page.querySelector('.klio-article-header');
      var navEl = page.querySelector('.klio-article-nav');
      if (headerEl) mainCol.appendChild(headerEl);
      mainCol.appendChild(prose);
      if (navEl) mainCol.appendChild(navEl);

      layout.appendChild(mainCol);
      layout.appendChild(sidebar);
      page.appendChild(layout);
    }

    var sidebarEl = layout.querySelector('.klio-article-sidebar');
    var mainEl = layout.querySelector('.klio-article-main');

    // 3. Auto Table of Contents in Sticky Sidebar + Font Controls + Scrollspy
    var headings = prose.querySelectorAll('h2');
    var tocLinks = [];
    if (!document.querySelector('.klio-toc-box')) {
      var tocBox = document.createElement('nav');
      tocBox.className = 'klio-side-card klio-toc-box';
      tocBox.setAttribute('aria-label', '本文目錄');
      var itemsHtml = '';
      for (var i = 0; i < headings.length; i++) {
        var h = headings[i];
        var label = (h.textContent || '').trim();
        if (!label) continue;
        var hid = h.id || 'sec-' + (i + 1);
        h.id = hid;
        itemsHtml += '<li><a href="#' + hid + '" data-toc-id="' + hid + '">' + label.replace(/</g, '&lt;') + '</a></li>';
      }
      tocBox.innerHTML =
        '<div class="klio-toc-header">' +
        '<div class="klio-toc-title" style="margin:0;">Contents / 導讀</div>' +
        '<div class="klio-font-controls" aria-label="調整閱讀字級">' +
        '<button type="button" class="klio-font-btn" id="klio-font-dec" aria-label="縮小字級">A-</button>' +
        '<button type="button" class="klio-font-btn" id="klio-font-inc" aria-label="放大字級">A+</button>' +
        '</div>' +
        '</div>' +
        (itemsHtml ? '<ul class="klio-toc-list">' + itemsHtml + '</ul>' : '');
      sidebarEl.appendChild(tocBox);
      tocLinks = Array.prototype.slice.call(tocBox.querySelectorAll('[data-toc-id]'));

      // Font size persistence
      var fontSize = 16.5;
      try {
        var savedSize = parseFloat(localStorage.getItem('klio-font-size'));
        if (savedSize >= 15 && savedSize <= 20) fontSize = savedSize;
      } catch (e) { }
      prose.style.fontSize = fontSize + 'px';

      document.getElementById('klio-font-dec').addEventListener('click', function () {
        fontSize = Math.max(15, +(fontSize - 0.75).toFixed(2));
        prose.style.fontSize = fontSize + 'px';
        try { localStorage.setItem('klio-font-size', String(fontSize)); } catch (e) { }
      });
      document.getElementById('klio-font-inc').addEventListener('click', function () {
        fontSize = Math.min(20, +(fontSize + 0.75).toFixed(2));
        prose.style.fontSize = fontSize + 'px';
        try { localStorage.setItem('klio-font-size', String(fontSize)); } catch (e) { }
      });
    }

    // 3b. Reading progress bar & active TOC scrollspy
    if (!document.getElementById('klio-read-progress')) {
      var track = document.createElement('div');
      track.className = 'klio-read-track';
      var progBar = document.createElement('div');
      progBar.id = 'klio-read-progress';
      progBar.className = 'klio-read-progress';
      track.appendChild(progBar);
      document.body.appendChild(track);

      function updateProgressAndSpy() {
        var scrollTop = window.scrollY || document.documentElement.scrollTop;
        var docHeight = document.documentElement.scrollHeight - window.innerHeight;
        var pct = docHeight > 0 ? Math.min(100, Math.max(4, (scrollTop / docHeight) * 100)) : 4;
        progBar.style.width = pct.toFixed(1) + '%';

        if (tocLinks.length > 0) {
          var activeId = tocLinks[0].getAttribute('data-toc-id');
          for (var j = 0; j < headings.length; j++) {
            var rect = headings[j].getBoundingClientRect();
            if (rect.top <= 130) {
              activeId = headings[j].id;
            }
          }
          for (var k = 0; k < tocLinks.length; k++) {
            tocLinks[k].classList.toggle('is-active', tocLinks[k].getAttribute('data-toc-id') === activeId);
          }
        }
      }

      window.addEventListener('scroll', updateProgressAndSpy, { passive: true });
      updateProgressAndSpy();
    }

    // 4. Load report cover, series path & related articles from klio-reports-data.js
    function escapeHtml(str) {
      return String(str || '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
    }

    function mountCoverAndRelated() {
      var reports = window.KLIO_REPORTS;
      if (!reports || !reports.length) return;
      var seriesList = window.KLIO_REPORTS_SERIES || [];
      var fname = window.location.pathname.split('/').pop();
      var current = reports.find(function (r) { return r.file === fname; });
      if (!current) return;

      var seriesMeta = current.series
        ? seriesList.find(function (s) { return s.id === current.series; })
        : null;

      var seriesPosts = seriesMeta
        ? reports
            .filter(function (r) { return r.series === seriesMeta.id; })
            .slice()
            .sort(function (a, b) {
              return a.date.localeCompare(b.date) || a.file.localeCompare(b.file);
            })
        : [];
      var currentSeriesIndex = seriesPosts.findIndex(function (r) { return r.file === current.file; });

      // 4a. Series pill in article header
      if (seriesMeta && headerMeta && !headerMeta.querySelector('.klio-series-pill')) {
        var seriesPill = document.createElement('a');
        seriesPill.className = 'klio-series-pill';
        seriesPill.href = BASE + 'index.html?series=' + encodeURIComponent(seriesMeta.id);
        seriesPill.textContent =
          '專題 · ' + seriesMeta.label +
          (currentSeriesIndex !== -1 ? ' (' + (currentSeriesIndex + 1) + '/' + seriesPosts.length + ')' : '');
        headerMeta.appendChild(seriesPill);
      }

      // 4b. Cover image
      if (current.cover && !mainEl.querySelector('.klio-article-cover')) {
        var cov = document.createElement('div');
        cov.className = 'klio-article-cover';
        cov.innerHTML = '<img src="' + current.cover.replace('./', BASE) + '" alt="' + escapeHtml(current.title) + '">';
        mainEl.insertBefore(cov, prose);
      }

      // 4c. Prioritize related items: manual relatedFiles -> same series -> same category
      var seen = {};
      seen[current.file] = true;
      var prioritized = [];
      var hasCuratedMatch = false;

      if (Array.isArray(current.relatedFiles)) {
        current.relatedFiles.forEach(function (rf) {
          if (seen[rf]) return;
          var match = reports.find(function (r) { return r.file === rf; });
          if (match) {
            seen[rf] = true;
            prioritized.push(match);
            hasCuratedMatch = true;
          }
        });
      }

      if (seriesPosts.length > 1) {
        // Put next-in-series first, then other series posts
        var orderedSeries = [];
        if (currentSeriesIndex !== -1 && currentSeriesIndex + 1 < seriesPosts.length) {
          orderedSeries.push(seriesPosts[currentSeriesIndex + 1]);
        }
        seriesPosts.forEach(function (r) {
          if (!seen[r.file] && orderedSeries.indexOf(r) === -1) {
            orderedSeries.push(r);
          }
        });
        orderedSeries.forEach(function (r) {
          if (!seen[r.file]) {
            seen[r.file] = true;
            prioritized.push(r);
            hasCuratedMatch = true;
          }
        });
      }

      var curatedItems = prioritized.slice();

      reports.forEach(function (r) {
        if (prioritized.length >= 4) return;
        if (!seen[r.file] && r.category === current.category) {
          seen[r.file] = true;
          prioritized.push(r);
        }
      });

      var sidebarRelated = prioritized.slice(0, 4);

      if (sidebarRelated.length > 0 && !sidebarEl.querySelector('.klio-related-card')) {
        var relCard = document.createElement('div');
        relCard.className = 'klio-side-card klio-related-card';
        relCard.innerHTML =
          '<div class="klio-toc-title">' + (hasCuratedMatch ? '專題延伸閱讀' : '同領域精選') + '</div>' +
          '<div class="klio-related-list">' +
          sidebarRelated.map(function (r) {
            var thumbSrc = (r.cover || '').replace('./', BASE);
            return (
              '<a class="klio-related-item" href="./' + encodeURIComponent(r.file) + '">' +
              '<div class="klio-related-thumb">' +
              (thumbSrc ? '<img src="' + thumbSrc + '" alt="" loading="lazy">' : '') +
              '</div>' +
              '<span class="klio-related-title">' + escapeHtml(r.title) + '</span>' +
              '</a>'
            );
          }).join('') +
          '</div>';
        sidebarEl.appendChild(relCard);
      }

      // 4d. End-of-article reading path & related reads (before .klio-article-nav)
      if (!mainEl.querySelector('.klio-series-endcap')) {
        var endcap = document.createElement('section');
        endcap.className = 'klio-series-endcap';
        endcap.setAttribute('aria-label', '專題脈絡與延伸閱讀');

        var endcapHtml = '';
        if (seriesMeta && seriesPosts.length > 1) {
          var stepsHtml = seriesPosts.map(function (r, idx) {
            var isCur = r.file === current.file;
            var isNext = currentSeriesIndex !== -1 && idx === currentSeriesIndex + 1;
            var numLabel = String(idx + 1).padStart(2, '0');
            var statusText = isCur ? '目前閱讀' : (isNext ? '下一篇 · ' + r.date : r.date);
            if (isCur) {
              return (
                '<li class="klio-series-step is-current">' +
                  '<span class="klio-series-step-num">' + numLabel + '</span>' +
                  '<span class="klio-series-step-title">' + escapeHtml(r.title) + '</span>' +
                  '<span class="klio-series-step-meta">' + escapeHtml(statusText) + '</span>' +
                '</li>'
              );
            }
            return (
              '<li>' +
                '<a class="klio-series-step" href="./' + encodeURIComponent(r.file) + '">' +
                  '<span class="klio-series-step-num">' + numLabel + '</span>' +
                  '<span class="klio-series-step-title">' + escapeHtml(r.title) + '</span>' +
                  '<span class="klio-series-step-meta">' + escapeHtml(statusText) + '</span>' +
                '</a>' +
              '</li>'
            );
          }).join('');

          endcapHtml +=
            '<div class="klio-series-endcap-head">' +
              '<div>' +
                '<div class="klio-series-endcap-kicker">專題閱讀路徑</div>' +
                '<h2 class="klio-series-endcap-title">' + escapeHtml(seriesMeta.label) + '</h2>' +
                '<p class="klio-series-endcap-desc">' + escapeHtml(seriesMeta.description) + '</p>' +
              '</div>' +
              '<a class="klio-series-pill" href="' + BASE + 'index.html?series=' + encodeURIComponent(seriesMeta.id) + '">查看全部 ' + seriesPosts.length + ' 篇</a>' +
            '</div>' +
            '<ol class="klio-series-path">' + stepsHtml + '</ol>';
        }

        // Extra curated or category next reads (when no series path, or when manual relatedFiles exist)
        var extraReads = (seriesMeta && seriesPosts.length > 1)
          ? curatedItems.filter(function (r) { return r.series !== seriesMeta.id; }).slice(0, 2)
          : prioritized.slice(0, 2);

        if (extraReads.length > 0) {
          if (!endcapHtml) {
            endcapHtml +=
              '<div class="klio-series-endcap-head">' +
                '<div>' +
                  '<div class="klio-series-endcap-kicker">延伸閱讀</div>' +
                  '<h2 class="klio-series-endcap-title">順著脈絡繼續讀</h2>' +
                '</div>' +
              '</div>';
          }
          endcapHtml +=
            '<div class="klio-end-related-grid">' +
            extraReads.map(function (r) {
              return (
                '<a class="klio-end-related-card" href="./' + encodeURIComponent(r.file) + '">' +
                  '<span class="klio-end-related-meta">' + escapeHtml(r.categoryLabel) + ' · ' + escapeHtml(r.date) + '</span>' +
                  '<span class="klio-end-related-title">' + escapeHtml(r.title) + '</span>' +
                '</a>'
              );
            }).join('') +
            '</div>';
        }

        if (endcapHtml) {
          endcap.innerHTML = endcapHtml;
          var navNode = mainEl.querySelector('.klio-article-nav');
          if (navNode) {
            mainEl.insertBefore(endcap, navNode);
          } else {
            mainEl.appendChild(endcap);
          }
        }
      }
    }

    if (window.KLIO_REPORTS) {
      mountCoverAndRelated();
    } else {
      var s = document.createElement('script');
      s.src = BASE + 'assets/js/klio-reports-data.js?v=20261126c';
      s.onload = mountCoverAndRelated;
      document.head.appendChild(s);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', injectShell);
  } else {
    injectShell();
  }

  window.KLIO_SHELL = {
    getTheme: getSavedTheme,
    setTheme: applyTheme,
    basePath: BASE
  };
})();
