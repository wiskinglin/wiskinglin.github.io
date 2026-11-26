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

    // 4. Load report cover & related articles from klio-reports-data.js
    function mountCoverAndRelated() {
      var reports = window.KLIO_REPORTS;
      if (!reports || !reports.length) return;
      var fname = window.location.pathname.split('/').pop();
      var current = reports.find(function (r) { return r.file === fname; });
      if (!current) return;

      if (current.cover && !mainEl.querySelector('.klio-article-cover')) {
        var cov = document.createElement('div');
        cov.className = 'klio-article-cover';
        cov.innerHTML = '<img src="' + current.cover.replace('./', BASE) + '" alt="' + current.title.replace(/"/g, '&quot;') + '">';
        mainEl.insertBefore(cov, prose);
      }

      var related = reports.filter(function (r) {
        return r.category === current.category && r.file !== current.file;
      }).slice(0, 4);

      if (related.length > 0 && !sidebarEl.querySelector('.klio-related-card')) {
        var relCard = document.createElement('div');
        relCard.className = 'klio-side-card klio-related-card';
        relCard.innerHTML =
          '<div class="klio-toc-title">Related / 同領域精選</div>' +
          '<div class="klio-related-list">' +
          related.map(function (r) {
            var thumbSrc = (r.cover || '').replace('./', BASE);
            return (
              '<a class="klio-related-item" href="./' + encodeURIComponent(r.file) + '">' +
              '<div class="klio-related-thumb">' +
              (thumbSrc ? '<img src="' + thumbSrc + '" alt="" loading="lazy">' : '') +
              '</div>' +
              '<span class="klio-related-title">' + r.title.replace(/</g, '&lt;') + '</span>' +
              '</a>'
            );
          }).join('') +
          '</div>';
        sidebarEl.appendChild(relCard);
      }
    }

    if (window.KLIO_REPORTS) {
      mountCoverAndRelated();
    } else {
      var s = document.createElement('script');
      s.src = BASE + 'assets/js/klio-reports-data.js';
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
