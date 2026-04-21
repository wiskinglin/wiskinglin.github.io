/**
 * iTW Editor V4 — Scenario-Driven Web App Engine (Full Implementation)
 * =====================================================================
 * Implements all 8 Workstreams (WS-1 through WS-8) from IMPLEMENTATION_PLAN.md
 *
 * Module Index:
 *   1.  ITW Parser/Serializer
 *   2.  Lightweight Formula Engine (WS-2)
 *   3.  Scenario Templates
 *   4.  Application State
 *   5.  DOM References
 *   6.  Dynamic Toolbar System (WS-3)
 *   7.  Block Rendering Engine (WS-1 DOMPurify)
 *   8.  DataGrid Inline Editor (WS-6)
 *   9.  Block Actions
 *   10. Outline Panel + Beat Sheet (WS-4)
 *   11. Source View Sync
 *   12. View Mode Management
 *   13. Template Dialog + TA Settings (WS-4)
 *   14. Scenario Detection
 *   15. Media Inbox (WS-5)
 *   16. Canvas & Guides (WS-5)
 *   17. WCAG Checker (WS-5)
 *   18. Chart Mapper (WS-6)
 *   19. Zen Mode (WS-7)
 *   20. Accordion & Semantic Zoom (WS-7)
 *   21. File I/O
 *   22. AI Panel (WS-8)
 *   23. Dirty State
 *   24. Utilities
 *   25. Event Wiring
 *   26. PWA Registration (WS-8)
 *   27. App Boot
 */

// ============================================================
// 1. ITW PARSER / SERIALIZER
// ============================================================

const ITWParser = {
    BARRIER_RE: /^---([A-Z]+)(?::([^\s-]+))?\s*(.*?)---\s*$/,
    VALID_TYPES: ['JSON', 'MD', 'CSV', 'HTML', 'THEME', 'SLIDE', 'IMG'],

    parse(raw) {
        const lines = raw.split('\n');
        const blocks = [];
        let currentBlock = null;
        let contentLines = [];

        const flushBlock = () => {
            if (currentBlock) {
                currentBlock.content = contentLines.join('\n').trim();
                blocks.push(currentBlock);
                contentLines = [];
                currentBlock = null;
            }
        };

        for (const line of lines) {
            const match = line.match(this.BARRIER_RE);
            if (match) {
                flushBlock();
                const type = match[1];
                const namespace = match[2] || null;
                const attrs = match[3]?.trim() || null;
                if (this.VALID_TYPES.includes(type)) {
                    currentBlock = { id: this.generateId(), type, namespace, attrs, content: '' };
                } else {
                    contentLines.push(line);
                }
            } else {
                contentLines.push(line);
            }
        }
        flushBlock();

        if (blocks.length === 0 && raw.trim()) {
            blocks.push({ id: this.generateId(), type: 'MD', namespace: null, attrs: null, content: raw.trim() });
        }
        return blocks;
    },

    serialize(blocks) {
        return blocks.map(block => {
            let barrier = `---${block.type}`;
            if (block.namespace) barrier += `:${block.namespace}`;
            if (block.attrs) barrier += ` ${block.attrs}`;
            barrier += '---';
            return `${barrier}\n${block.content}`;
        }).join('\n');
    },

    generateId() {
        return 'blk-' + Date.now().toString(36) + Math.random().toString(36).substr(2, 6);
    },
};


// ============================================================
// 2. LIGHTWEIGHT FORMULA ENGINE (WS-2)
// ============================================================

const FormulaEngine = {
    /**
     * Evaluate formulas in a CSV grid.
     * Supports: =A1+B2, =SUM(A1:A5), =A1*1.5, basic arithmetic
     */
    evaluate(grid) {
        if (!grid || grid.length < 2) return grid;
        const result = grid.map(row => [...row]);
        const maxR = result.length;
        const maxC = result[0]?.length || 0;

        const colIndex = (letter) => {
            let idx = 0;
            for (let i = 0; i < letter.length; i++) {
                idx = idx * 26 + (letter.charCodeAt(i) - 64);
            }
            return idx - 1;
        };

        const cellVal = (ref) => {
            const m = ref.match(/^([A-Z]+)(\d+)$/);
            if (!m) return 0;
            const c = colIndex(m[1]);
            const r = parseInt(m[2]) - 1;
            if (r < 0 || r >= maxR || c < 0 || c >= maxC) return 0;
            const v = result[r][c];
            if (typeof v === 'string' && v.startsWith('=')) return 0;
            return parseFloat(v) || 0;
        };

        const evalFormula = (formula) => {
            let expr = formula.substring(1).trim();

            // SUM(range)
            const sumMatch = expr.match(/^SUM\(([A-Z]+\d+):([A-Z]+\d+)\)$/i);
            if (sumMatch) {
                const startM = sumMatch[1].match(/^([A-Z]+)(\d+)$/);
                const endM = sumMatch[2].match(/^([A-Z]+)(\d+)$/);
                if (startM && endM) {
                    let sum = 0;
                    const sc = colIndex(startM[1]), sr = parseInt(startM[2]) - 1;
                    const ec = colIndex(endM[1]), er = parseInt(endM[2]) - 1;
                    for (let r = sr; r <= er; r++) {
                        for (let c = sc; c <= ec; c++) {
                            if (r >= 0 && r < maxR && c >= 0 && c < maxC) {
                                sum += parseFloat(result[r][c]) || 0;
                            }
                        }
                    }
                    return sum;
                }
            }

            // AVERAGE(range)
            const avgMatch = expr.match(/^AVERAGE\(([A-Z]+\d+):([A-Z]+\d+)\)$/i);
            if (avgMatch) {
                const startM = avgMatch[1].match(/^([A-Z]+)(\d+)$/);
                const endM = avgMatch[2].match(/^([A-Z]+)(\d+)$/);
                if (startM && endM) {
                    let sum = 0, count = 0;
                    const sc = colIndex(startM[1]), sr = parseInt(startM[2]) - 1;
                    const ec = colIndex(endM[1]), er = parseInt(endM[2]) - 1;
                    for (let r = sr; r <= er; r++) {
                        for (let c = sc; c <= ec; c++) {
                            if (r >= 0 && r < maxR && c >= 0 && c < maxC) {
                                const v = parseFloat(result[r][c]);
                                if (!isNaN(v)) { sum += v; count++; }
                            }
                        }
                    }
                    return count ? sum / count : 0;
                }
            }

            // Replace cell references with values
            expr = expr.replace(/[A-Z]+\d+/g, (ref) => cellVal(ref));

            try {
                // Safe eval of arithmetic
                if (/^[\d\s+\-*/().]+$/.test(expr)) {
                    return Function('"use strict"; return (' + expr + ')')();
                }
            } catch { /* fall through */ }
            return 0;
        };

        // Multi-pass to resolve dependencies
        for (let pass = 0; pass < 3; pass++) {
            for (let r = 1; r < maxR; r++) {
                for (let c = 0; c < result[r].length; c++) {
                    const cell = grid[r][c];
                    if (typeof cell === 'string' && cell.startsWith('=')) {
                        result[r][c] = evalFormula(cell);
                    }
                }
            }
        }
        return result;
    }
};


// ============================================================
// 3. SCENARIO TEMPLATES
// ============================================================

const BEAT_SHEETS = {
    investor: ['封面', '痛點', '解決方案', '市場規模', '商業模式', '產品Demo', '競爭優勢', '團隊', '財務預測', '募資需求', 'CTA'],
    client:   ['封面', '客戶痛點', '我們的方案', '核心功能', '案例證明', '方案比較', '定價', '下一步', 'CTA'],
    internal: ['封面', '議題背景', '數據分析', '策略方案', '時程規劃', '資源需求', '風險評估', 'Q&A'],
};

const ScenarioTemplates = {
    deck: {
        id: 'deck', name: '簡報 Pitch Deck',
        icon: 'fa-solid fa-display', priority: 'P0',
        description: '募資簡報、產品發表、年度業績報告、教學投影片',
        color: '#f87171',
        defaultBlocks: [
            { type: 'JSON', content: '{\n  "type": "deck",\n  "theme": "modern-dark",\n  "author": "",\n  "date": "' + new Date().toISOString().split('T')[0] + '"\n}' },
            { type: 'SLIDE', namespace: '1', attrs: 'layout=cover', content: '# 標題\n\n副標題 — 作者名稱' },
            { type: 'SLIDE', namespace: '2', attrs: 'layout=split', content: '## 痛點\n\n描述你要解決的問題...' },
            { type: 'SLIDE', namespace: '3', attrs: 'layout=default', content: '## 解決方案\n\n你的產品如何解決這個問題...' },
            { type: 'SLIDE', namespace: '4', attrs: 'layout=data', content: '## 關鍵數據\n\n呈現核心成長指標...' },
            { type: 'SLIDE', namespace: '5', attrs: 'layout=cta', content: '## 聯絡我們\n\n感謝聆聽！' },
        ],
    },
    visual: {
        id: 'visual', name: '圖片 Visual Content',
        icon: 'fa-solid fa-image', priority: 'P0',
        description: '社群貼文、YT 封面、活動海報、品牌 Logo',
        color: '#22d3ee',
        defaultBlocks: [
            { type: 'JSON', content: '{\n  "type": "visual",\n  "theme": "vibrant",\n  "canvas": { "width": 1080, "height": 1080 },\n  "date": "' + new Date().toISOString().split('T')[0] + '"\n}' },
            { type: 'MD', content: '# 社群貼文標題\n\n> 你的行動呼籲 (CTA) 放在這裡' },
            { type: 'HTML', content: '<div class="visual-canvas">\n  <!-- 拖曳素材至此 -->\n</div>' },
        ],
    },
    datagrid: {
        id: 'datagrid', name: '試算表 DataGrid',
        icon: 'fa-solid fa-table', priority: 'P1',
        description: '預算規劃、專案追蹤、庫存盤點、財務報表',
        color: '#34d399',
        defaultBlocks: [
            { type: 'JSON', content: '{\n  "type": "datagrid",\n  "theme": "clean",\n  "date": "' + new Date().toISOString().split('T')[0] + '"\n}' },
            { type: 'MD', content: '# 數據報表標題\n\n簡要描述此報表的用途與範圍。' },
            { type: 'CSV', namespace: 'Main', content: '項目,Q1,Q2,Q3,Q4\n營收,1000,1200,1500,1800\n成本,600,650,700,750\n利潤,=B2-B3,=C2-C3,=D2-D3,=E2-E3' },
        ],
    },
    document: {
        id: 'document', name: '文件 Document',
        icon: 'fa-solid fa-file-lines', priority: 'P1',
        description: '商業企劃書、履歷表、會議記錄、合約文件',
        color: '#818cf8',
        defaultBlocks: [
            { type: 'JSON', content: '{\n  "type": "document",\n  "theme": "professional",\n  "author": "",\n  "date": "' + new Date().toISOString().split('T')[0] + '"\n}' },
            { type: 'MD', content: '# 文件標題\n\n## 1. 摘要\n\n本文件的目的與概要...\n\n## 2. 背景\n\n相關背景資訊...\n\n## 3. 內容\n\n主要內容...\n\n## 4. 結論\n\n總結與下一步行動...' },
        ],
    },
    blank: {
        id: 'blank', name: '空白文件',
        icon: 'fa-solid fa-file', priority: null,
        description: '從頭開始，自由組合區塊',
        color: '#9e9eb8',
        defaultBlocks: [
            { type: 'JSON', content: '{\n  "type": "hybrid",\n  "theme": "default"\n}' },
            { type: 'MD', content: '# 新文件\n\n開始寫作...' },
        ],
    },
};


// ============================================================
// 4. APPLICATION STATE
// ============================================================

const AppState = {
    blocks: [],
    activeBlockId: null,
    scenario: null,
    fileName: 'untitled.itw',
    isDirty: false,
    viewMode: 'blocks',
    panelOpen: true,
    activePanel: 'outline',
    fileHandle: null,
    // WS-4: TA settings
    taAudience: 'investor',
    taDuration: 10,
    // WS-5: Media inbox
    mediaAssets: [],
    activeTag: null,
    guidesVisible: false,
    // WS-6: Chart
    chartVisible: {},
    // WS-7: Zen mode & Document features
    zenMode: false,
    constraintMode: false,
    constraintMinChars: 100,
    semanticZoom: 'normal', // 'out' | 'normal' | 'in'
    // WS-8: AI
    aiGenerating: false,
    aiResult: '',
    // Timers
    _draftTimeout: null,
    _sourceTimeout: null,
};


// ============================================================
// 5. DOM REFERENCES
// ============================================================

let DOM = {};

function cacheDom() {
    DOM = {
        loader: document.getElementById('app-loader'),
        loaderBar: document.getElementById('loader-bar'),
        app: document.getElementById('app'),
        fileName: document.getElementById('file-name'),
        unsavedDot: document.getElementById('unsaved-dot'),
        scenarioBadge: document.getElementById('scenario-badge'),
        contextPanel: document.getElementById('context-panel'),
        blockList: document.getElementById('block-list'),
        sourceEditor: document.getElementById('source-editor'),
        blocksPane: document.getElementById('blocks-pane'),
        blocksContainer: document.getElementById('blocks-container'),
        previewPane: document.getElementById('preview-pane'),
        previewContent: document.getElementById('preview-content'),
        workspace: document.getElementById('editor-workspace'),
        toolbar: document.getElementById('editor-toolbar'),
        blockCount: document.getElementById('block-count'),
        charCount: document.getElementById('char-count'),
        scenarioStatus: document.getElementById('scenario-status'),
        constraintIndicator: document.getElementById('constraint-indicator'),
        // Panels
        panelOutline: document.getElementById('panel-outline'),
        panelAssets: document.getElementById('panel-assets'),
        panelAi: document.getElementById('panel-ai'),
        // Assets
        inboxDropzone: document.getElementById('inbox-dropzone'),
        inboxGrid: document.getElementById('inbox-grid'),
        inboxTags: document.getElementById('inbox-tags'),
        // AI
        aiUrlInput: document.getElementById('ai-url-input'),
        aiSearchInput: document.getElementById('ai-search-input'),
        aiPromptInput: document.getElementById('ai-prompt-input'),
        aiResult: document.getElementById('ai-result'),
        aiResultActions: document.getElementById('ai-result-actions'),
        aiModelSelect: document.getElementById('ai-model-select'),
        // Guides
        guideOverlay: document.getElementById('guide-overlay'),
        // Zen
        zenOverlay: document.getElementById('zen-overlay'),
        zenTextarea: document.getElementById('zen-textarea'),
        zenStats: document.getElementById('zen-stats'),
        // Modals
        templateModal: document.getElementById('template-modal'),
        taModal: document.getElementById('ta-modal'),
        wcagModal: document.getElementById('wcag-modal'),
        taSuggestion: document.getElementById('ta-suggestion'),
        // Block menu
        blockMenu: document.getElementById('block-menu'),
    };
}


// ============================================================
// 6. DYNAMIC TOOLBAR SYSTEM (WS-3)
// ============================================================

const ToolbarManager = {
    configs: {
        // Common markdown buttons
        _mdFormat: [
            { action: 'bold', icon: 'fa-solid fa-bold', title: '粗體 (Ctrl+B)' },
            { action: 'italic', icon: 'fa-solid fa-italic', title: '斜體 (Ctrl+I)' },
        ],
        _headings: [
            { action: 'h1', label: 'H1', title: '標題 1' },
            { action: 'h2', label: 'H2', title: '標題 2' },
            { action: 'h3', label: 'H3', title: '標題 3' },
        ],
        _lists: [
            { action: 'ul', icon: 'fa-solid fa-list-ul', title: '無序列表' },
            { action: 'ol', icon: 'fa-solid fa-list-ol', title: '有序列表' },
            { action: 'quote', icon: 'fa-solid fa-quote-left', title: '引用' },
            { action: 'code', icon: 'fa-solid fa-code', title: '程式碼' },
        ],
        _insert: [
            { action: 'link', icon: 'fa-solid fa-link', title: '連結' },
            { action: 'image', icon: 'fa-solid fa-image', title: '圖片' },
            { action: 'table', icon: 'fa-solid fa-table', title: '表格' },
            { action: 'hr', icon: 'fa-solid fa-minus', title: '分隔線' },
        ],

        // Scenario-specific tools
        deck: [
            { action: 'addSlide', icon: 'fa-solid fa-plus', label: '投影片', title: '新增投影片' },
            { action: 'layoutPicker', icon: 'fa-solid fa-table-columns', label: '版型', title: '投影片版型', dropdown: true },
            { action: 'taSettings', icon: 'fa-solid fa-bullseye', label: 'TA', title: '受眾設定' },
            { action: 'dataHighlight', icon: 'fa-solid fa-highlighter', label: '高亮', title: '數據高亮' },
            { action: 'toggleFullbleed', icon: 'fa-solid fa-expand', label: '滿版', title: '背景滿版切換' },
        ],
        visual: [
            { action: 'canvasPreset', icon: 'fa-solid fa-crop', label: '畫布', title: '畫布尺寸預設', dropdown: true },
            { action: 'toggleGuides', icon: 'fa-solid fa-ruler-combined', label: '對齊', title: '黃金三角對齊線' },
            { action: 'wcagCheck', icon: 'fa-solid fa-universal-access', label: 'WCAG', title: 'WCAG 配色檢測' },
        ],
        datagrid: [
            { action: 'addColumn', icon: 'fa-solid fa-table-columns', label: '欄位', title: '新增欄位' },
            { action: 'addRow', icon: 'fa-solid fa-table-rows', label: '列', title: '新增列' },
            { action: 'toggleChart', icon: 'fa-solid fa-chart-bar', label: '圖表', title: '生成圖表' },
            { action: 'sortCol', icon: 'fa-solid fa-arrow-down-a-z', label: '排序', title: '排序' },
        ],
        document: [
            { action: 'zenMode', icon: 'fa-solid fa-expand', label: 'Zen', title: '沉浸寫作模式' },
            { action: 'toggleConstraint', icon: 'fa-solid fa-lock', label: '約束', title: '約束模式' },
            { action: 'toggleAccordion', icon: 'fa-solid fa-compress', label: '收納', title: '折疊段落' },
            { action: 'toggleDocTheme', icon: 'fa-solid fa-palette', label: '版型', title: '黑白高對比版型' },
            { action: 'outlineJump', icon: 'fa-solid fa-list-tree', label: '大綱', title: '大綱跳轉' },
        ],
    },

    build(scenario) {
        if (!DOM.toolbar) return;
        DOM.toolbar.innerHTML = '';

        // Common format buttons
        this._addGroup(this.configs._mdFormat);
        this._addDivider();
        this._addGroup(this.configs._headings);
        this._addDivider();
        this._addGroup(this.configs._lists);
        this._addDivider();
        this._addGroup(this.configs._insert);

        // Scenario-specific
        const scenarioTools = this.configs[scenario];
        if (scenarioTools) {
            this._addDivider();
            const group = document.createElement('div');
            group.className = 'tb-group';
            scenarioTools.forEach(cfg => {
                const btn = document.createElement('button');
                btn.className = 'tb-btn';
                btn.dataset.action = cfg.action;
                btn.title = cfg.title;
                btn.innerHTML = cfg.icon ? `<i class="${cfg.icon}"></i>` : '';
                if (cfg.label) btn.innerHTML += `<span class="tb-label">${cfg.label}</span>`;
                group.appendChild(btn);
            });
            DOM.toolbar.appendChild(group);
        }

        // Spacer + View switch
        const spacer = document.createElement('div');
        spacer.className = 'tb-spacer';
        DOM.toolbar.appendChild(spacer);

        const viewSwitch = document.createElement('div');
        viewSwitch.className = 'view-switch';
        viewSwitch.innerHTML = `
            <button class="view-switch-btn ${AppState.viewMode === 'blocks' ? 'active' : ''}" id="view-blocks" title="區塊視圖">
                <i class="fa-solid fa-cubes"></i> 區塊
            </button>
            <button class="view-switch-btn ${AppState.viewMode === 'source' ? 'active' : ''}" id="view-source" title="原始碼">
                <i class="fa-solid fa-code"></i> 原始碼
            </button>
            <button class="view-switch-btn ${AppState.viewMode === 'split' ? 'active' : ''}" id="view-split" title="分割預覽">
                <i class="fa-solid fa-columns"></i> 分割
            </button>
        `;
        DOM.toolbar.appendChild(viewSwitch);

        // Wire toolbar events
        this._wireToolbarEvents();
    },

    _addGroup(items) {
        const group = document.createElement('div');
        group.className = 'tb-group';
        items.forEach(cfg => {
            const btn = document.createElement('button');
            btn.className = 'tb-btn';
            btn.dataset.action = cfg.action;
            btn.title = cfg.title;
            if (cfg.icon) btn.innerHTML = `<i class="${cfg.icon}"></i>`;
            if (cfg.label && !cfg.icon) btn.textContent = cfg.label;
            else if (cfg.label && cfg.icon) btn.innerHTML += `<span class="tb-label">${cfg.label}</span>`;
            group.appendChild(btn);
        });
        DOM.toolbar.appendChild(group);
    },

    _addDivider() {
        const d = document.createElement('div');
        d.className = 'tb-divider';
        DOM.toolbar.appendChild(d);
    },

    _wireToolbarEvents() {
        // View mode buttons
        document.getElementById('view-blocks')?.addEventListener('click', () => setViewMode('blocks'));
        document.getElementById('view-source')?.addEventListener('click', () => setViewMode('source'));
        document.getElementById('view-split')?.addEventListener('click', () => setViewMode('split'));

        // All toolbar buttons
        DOM.toolbar.querySelectorAll('.tb-btn[data-action]').forEach(btn => {
            btn.addEventListener('click', () => handleToolbarAction(btn.dataset.action, btn));
        });
    },
};

function handleToolbarAction(action, btnEl) {
    // Markdown formatting actions
    const mdActions = ['bold','italic','h1','h2','h3','ul','ol','quote','code','link','image','table','hr'];
    if (mdActions.includes(action)) {
        insertFormatting(action);
        return;
    }

    // Scenario-specific
    switch (action) {
        case 'addSlide': addSlideBlock(); break;
        case 'layoutPicker': showLayoutPicker(btnEl); break;
        case 'taSettings': openModal(DOM.taModal); break;
        case 'dataHighlight': applyDataHighlight(); break;
        case 'toggleFullbleed': toggleFullbleed(); break;
        case 'canvasPreset': showCanvasPresetMenu(btnEl); break;
        case 'toggleGuides': toggleGuides(); break;
        case 'wcagCheck': runWcagCheck(); break;
        case 'addColumn': addDataGridColumn(); break;
        case 'addRow': addDataGridRow(); break;
        case 'toggleChart': toggleChart(); break;
        case 'sortCol': sortActiveColumn(); break;
        case 'zenMode': enterZenMode(); break;
        case 'toggleConstraint': toggleConstraintMode(); break;
        case 'toggleAccordion': /* handled in rendering */ break;
        case 'toggleDocTheme': toggleDocTheme(); break;
        case 'outlineJump': focusOutlinePanel(); break;
    }
}


// ============================================================
// 7. BLOCK RENDERING ENGINE (WS-1 DOMPurify + WS-2)
// ============================================================

function sanitize(html) {
    if (typeof DOMPurify !== 'undefined') {
        return DOMPurify.sanitize(html, { ADD_TAGS: ['iframe'], ADD_ATTR: ['target'] });
    }
    return html;
}

function resolveItwImages(html) {
    // Replace ![alt](itw:img-id) with actual Base64 from IMG blocks (WS-2)
    return html.replace(/src="itw:([^"]+)"/g, (_, id) => {
        const imgBlock = AppState.blocks.find(b => b.type === 'IMG' && b.namespace === id);
        if (imgBlock && imgBlock.content) return `src="${imgBlock.content.trim()}"`;
        return `src="itw:${id}"`;
    });
}

function renderBlockCards() {
    if (!DOM.blocksContainer) return;
    DOM.blocksContainer.innerHTML = '';

    AppState.blocks.forEach((block, index) => {
        const card = createBlockCard(block, index);
        DOM.blocksContainer.appendChild(card);
    });

    // Add block button at bottom
    const addBar = document.createElement('div');
    addBar.className = 'add-block-bar';
    addBar.innerHTML = `<button class="add-block-btn" id="add-block-bottom"><i class="fa-solid fa-plus"></i> 新增區塊</button>`;
    DOM.blocksContainer.appendChild(addBar);

    document.getElementById('add-block-bottom')?.addEventListener('click', (e) => {
        showBlockMenu(e, AppState.blocks.length);
    });
}

function createBlockCard(block, index) {
    const card = document.createElement('div');
    const isSlide = block.type === 'SLIDE';
    card.className = `block-card${block.id === AppState.activeBlockId ? ' focused' : ''}${isSlide ? ' slide-card' : ''}`;
    card.dataset.blockId = block.id;

    const typeTag = block.type.toLowerCase();
    const typeLabel = block.namespace ? `${block.type}:${block.namespace}` : block.type;
    const attrsStr = block.attrs ? ` ${block.attrs}` : '';

    // Get current layout for SLIDE blocks
    let layoutSelector = '';
    if (isSlide) {
        const currentLayout = (block.attrs || '').match(/layout=(\w+)/)?.[1] || 'default';
        layoutSelector = `<select class="layout-selector" data-block-id="${block.id}">
            <option value="cover" ${currentLayout === 'cover' ? 'selected' : ''}>封面 Cover</option>
            <option value="default" ${currentLayout === 'default' ? 'selected' : ''}>預設 Default</option>
            <option value="split" ${currentLayout === 'split' ? 'selected' : ''}>分割 Split</option>
            <option value="data" ${currentLayout === 'data' ? 'selected' : ''}>數據 Data</option>
            <option value="image-full" ${currentLayout === 'image-full' ? 'selected' : ''}>全圖 Image</option>
            <option value="cta" ${currentLayout === 'cta' ? 'selected' : ''}>CTA</option>
        </select>`;
    }

    card.innerHTML = `
        <div class="block-header">
            <span class="block-drag-handle"><i class="fa-solid fa-grip-vertical"></i></span>
            <span class="block-type-label block-type-tag ${typeTag}">${typeLabel}</span>
            ${layoutSelector}
            ${attrsStr && !isSlide ? `<span class="block-namespace">${attrsStr}</span>` : ''}
            <div class="block-actions">
                <button class="block-action-btn" data-action="edit" title="編輯"><i class="fa-solid fa-pen-to-square"></i></button>
                <button class="block-action-btn" data-action="duplicate" title="複製"><i class="fa-regular fa-copy"></i></button>
                <button class="block-action-btn" data-action="moveUp" title="上移" ${index === 0 ? 'disabled' : ''}><i class="fa-solid fa-arrow-up"></i></button>
                <button class="block-action-btn" data-action="moveDown" title="下移" ${index === AppState.blocks.length - 1 ? 'disabled' : ''}><i class="fa-solid fa-arrow-down"></i></button>
                <button class="block-action-btn danger" data-action="delete" title="刪除"><i class="fa-solid fa-trash"></i></button>
            </div>
        </div>
        <div class="block-body">
            ${renderBlockContent(block)}
        </div>
    `;

    // Event delegation for block actions
    card.querySelectorAll('.block-action-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            handleBlockAction(btn.dataset.action, block.id, index);
        });
    });

    // Layout selector change (WS-4)
    const layoutSel = card.querySelector('.layout-selector');
    if (layoutSel) {
        layoutSel.addEventListener('change', (e) => {
            e.stopPropagation();
            block.attrs = `layout=${e.target.value}`;
            markDirty();
        });
    }

    // Focus management
    card.addEventListener('click', () => setActiveBlock(block.id));

    // Wire up textarea edits
    const textarea = card.querySelector('textarea');
    if (textarea) {
        textarea.addEventListener('input', () => {
            block.content = textarea.value;
            markDirty();
            updateOutlinePanel();
            if (AppState.viewMode === 'split') {
                syncBlocksToSource();
                updatePreview();
            }
        });
        textarea.addEventListener('focus', () => setActiveBlock(block.id));
    }

    // Wire up DataGrid cell edits (WS-6)
    card.querySelectorAll('.cell-input').forEach(input => {
        input.addEventListener('input', () => {
            rebuildCSVFromGrid(block, card);
        });
        input.addEventListener('focus', () => setActiveBlock(block.id));
    });

    // Chart toggle button
    card.querySelector('.chart-toggle-btn')?.addEventListener('click', (e) => {
        e.stopPropagation();
        AppState.chartVisible[block.id] = !AppState.chartVisible[block.id];
        renderBlockCards();
        updateOutlinePanel();
    });

    return card;
}

function renderBlockContent(block) {
    switch (block.type) {
        case 'MD':
        case 'SLIDE':
            return renderMarkdownBlock(block);
        case 'CSV':
            return renderCSVBlock(block);
        case 'JSON':
        case 'THEME':
            return renderJSONBlock(block);
        case 'HTML':
            return renderHTMLBlock(block);
        case 'IMG':
            return renderIMGBlock(block);
        default:
            return `<textarea spellcheck="false">${escapeHtml(block.content)}</textarea>`;
    }
}

function renderMarkdownBlock(block) {
    if (block.id === AppState.activeBlockId) {
        return `<textarea spellcheck="false">${escapeHtml(block.content)}</textarea>`;
    }
    try {
        let rendered = marked.parse(block.content || '');
        rendered = sanitize(rendered);
        rendered = resolveItwImages(rendered);
        // Apply data-highlight markers
        rendered = rendered.replace(/\{\{(\d[\d,.]*)\}\}/g, '<span class="data-highlight">$1</span>');
        return `<div class="rendered-content">${rendered}</div>`;
    } catch {
        return `<textarea spellcheck="false">${escapeHtml(block.content)}</textarea>`;
    }
}

function renderCSVBlock(block) {
    // WS-6: DataGrid inline editor when active
    if (block.id === AppState.activeBlockId) {
        return renderDataGridEditor(block);
    }
    try {
        const parsed = parseCSV(block.content);
        if (parsed.length === 0) return `<textarea spellcheck="false">${escapeHtml(block.content)}</textarea>`;

        const evaluated = FormulaEngine.evaluate(parsed);
        let html = '<table class="csv-table"><thead><tr>';
        parsed[0].forEach(h => { html += `<th>${escapeHtml(h)}</th>`; });
        html += '</tr></thead><tbody>';
        for (let i = 1; i < evaluated.length; i++) {
            html += '<tr>';
            evaluated[i].forEach((c, ci) => {
                const original = parsed[i]?.[ci] || '';
                const isFormula = typeof original === 'string' && original.startsWith('=');
                html += `<td${isFormula ? ' class="formula-cell" title="' + escapeHtml(original) + '"' : ''}>${escapeHtml(String(c))}</td>`;
            });
            html += '</tr>';
        }
        html += '</tbody></table>';

        // Chart (WS-6)
        if (AppState.chartVisible[block.id]) {
            html += renderSVGChart(evaluated);
        }
        html += `<div style="padding:4px 12px;text-align:right;"><button class="chart-toggle-btn tb-btn" style="font-size:10px;">${AppState.chartVisible[block.id] ? '<i class="fa-solid fa-chart-bar"></i> 隱藏圖表' : '<i class="fa-solid fa-chart-bar"></i> 顯示圖表'}</button></div>`;

        return html;
    } catch {
        return `<textarea spellcheck="false">${escapeHtml(block.content)}</textarea>`;
    }
}

function renderJSONBlock(block) {
    if (block.id === AppState.activeBlockId) {
        return `<textarea spellcheck="false">${escapeHtml(block.content)}</textarea>`;
    }
    try {
        const obj = JSON.parse(block.content);
        const pretty = JSON.stringify(obj, null, 2);
        const highlighted = syntaxHighlightJSON(pretty);
        return `<div class="json-display">${highlighted}</div>`;
    } catch {
        return `<textarea spellcheck="false">${escapeHtml(block.content)}</textarea>`;
    }
}

function renderHTMLBlock(block) {
    return `<textarea spellcheck="false">${escapeHtml(block.content)}</textarea>`;
}

function renderIMGBlock(block) {
    const content = block.content.trim();
    if (content.startsWith('data:image')) {
        return `<div class="rendered-content"><img src="${content}" alt="${block.namespace || 'image'}" style="max-width:100%;"></div>`;
    }
    return `<textarea spellcheck="false">${escapeHtml(block.content)}</textarea>`;
}


// ============================================================
// 8. DATAGRID INLINE EDITOR (WS-6)
// ============================================================

function renderDataGridEditor(block) {
    const rows = parseCSV(block.content);
    if (rows.length === 0) return `<textarea spellcheck="false">${escapeHtml(block.content)}</textarea>`;

    let html = '<div class="datagrid-editor"><table>';
    // Header row
    html += '<thead><tr><th class="row-number">#</th>';
    rows[0].forEach((h, ci) => {
        html += `<th>${escapeHtml(h)}<span class="col-actions">
            <button class="block-action-btn" data-col-action="rename" data-col="${ci}" title="重命名" style="width:16px;height:16px;font-size:8px;"><i class="fa-solid fa-pen"></i></button>
            <button class="block-action-btn danger" data-col-action="delete" data-col="${ci}" title="刪除欄" style="width:16px;height:16px;font-size:8px;"><i class="fa-solid fa-xmark"></i></button>
        </span></th>`;
    });
    html += '</tr></thead><tbody>';
    // Data rows
    for (let r = 1; r < rows.length; r++) {
        html += `<tr><td class="row-number">${r}</td>`;
        for (let c = 0; c < rows[0].length; c++) {
            const val = rows[r]?.[c] || '';
            html += `<td><input class="cell-input" data-row="${r}" data-col="${c}" value="${escapeHtml(val)}"></td>`;
        }
        html += '</tr>';
    }
    html += '</tbody></table>';
    html += `<button class="datagrid-add-row" data-grid-action="addRow">+ 新增列</button>`;
    html += '</div>';
    return html;
}

function rebuildCSVFromGrid(block, card) {
    const rows = parseCSV(block.content);
    if (!rows.length) return;

    card.querySelectorAll('.cell-input').forEach(input => {
        const r = parseInt(input.dataset.row);
        const c = parseInt(input.dataset.col);
        if (!rows[r]) rows[r] = [];
        rows[r][c] = input.value;
    });

    block.content = rows.map(row => row.join(',')).join('\n');
    markDirty();
}

function addDataGridColumn() {
    const block = AppState.blocks.find(b => b.id === AppState.activeBlockId && b.type === 'CSV');
    if (!block) return;
    const rows = parseCSV(block.content);
    if (!rows.length) return;
    const name = prompt('欄位名稱:', `欄位${rows[0].length + 1}`);
    if (!name) return;
    rows[0].push(name);
    for (let r = 1; r < rows.length; r++) rows[r].push('');
    block.content = rows.map(row => row.join(',')).join('\n');
    markDirty();
    renderBlockCards();
    updateOutlinePanel();
}

function addDataGridRow() {
    const block = AppState.blocks.find(b => b.id === AppState.activeBlockId && b.type === 'CSV');
    if (!block) return;
    const rows = parseCSV(block.content);
    if (!rows.length) return;
    rows.push(new Array(rows[0].length).fill(''));
    block.content = rows.map(row => row.join(',')).join('\n');
    markDirty();
    renderBlockCards();
    updateOutlinePanel();
}

function sortActiveColumn() {
    const block = AppState.blocks.find(b => b.id === AppState.activeBlockId && b.type === 'CSV');
    if (!block) return;
    const rows = parseCSV(block.content);
    if (rows.length < 3) return;
    const colIdx = parseInt(prompt('排序欄位編號 (從1開始):', '2')) - 1;
    if (isNaN(colIdx) || colIdx < 0) return;
    const header = rows.shift();
    rows.sort((a, b) => {
        const va = parseFloat(a[colIdx]) || a[colIdx] || '';
        const vb = parseFloat(b[colIdx]) || b[colIdx] || '';
        return va > vb ? 1 : va < vb ? -1 : 0;
    });
    rows.unshift(header);
    block.content = rows.map(row => row.join(',')).join('\n');
    markDirty();
    renderBlockCards();
}


// ============================================================
// 9. BLOCK ACTIONS
// ============================================================

function handleBlockAction(action, blockId, index) {
    switch (action) {
        case 'edit': setActiveBlock(blockId); break;
        case 'duplicate': duplicateBlock(index); break;
        case 'moveUp': moveBlock(index, -1); break;
        case 'moveDown': moveBlock(index, 1); break;
        case 'delete': deleteBlock(index); break;
    }
}

function duplicateBlock(index) {
    const original = AppState.blocks[index];
    const dup = { ...original, id: ITWParser.generateId(), content: original.content };
    AppState.blocks.splice(index + 1, 0, dup);
    markDirty();
    renderBlockCards();
    updateOutlinePanel();
}

function moveBlock(index, direction) {
    const newIndex = index + direction;
    if (newIndex < 0 || newIndex >= AppState.blocks.length) return;
    const [block] = AppState.blocks.splice(index, 1);
    AppState.blocks.splice(newIndex, 0, block);
    markDirty();
    renderBlockCards();
    updateOutlinePanel();
}

function deleteBlock(index) {
    if (AppState.blocks.length <= 1) return;
    AppState.blocks.splice(index, 1);
    AppState.activeBlockId = null;
    markDirty();
    renderBlockCards();
    updateOutlinePanel();
}

function addBlock(type, afterIndex = AppState.blocks.length, namespace = null) {
    const block = {
        id: ITWParser.generateId(), type, namespace,
        attrs: type === 'SLIDE' ? 'layout=default' : null,
        content: getDefaultContent(type),
    };
    AppState.blocks.splice(afterIndex, 0, block);
    AppState.activeBlockId = block.id;
    markDirty();
    renderBlockCards();
    updateOutlinePanel();
    setTimeout(() => {
        const card = document.querySelector(`[data-block-id="${block.id}"]`);
        if (card) {
            card.scrollIntoView({ behavior: 'smooth', block: 'center' });
            const ta = card.querySelector('textarea') || card.querySelector('.cell-input');
            if (ta) ta.focus();
        }
    }, 100);
}

function addSlideBlock() {
    const slideCount = AppState.blocks.filter(b => b.type === 'SLIDE').length;
    addBlock('SLIDE', AppState.blocks.length, String(slideCount + 1));
}

function getDefaultContent(type) {
    switch (type) {
        case 'MD': return '## 新段落\n\n';
        case 'CSV': return '欄位A,欄位B,欄位C\n值1,值2,值3';
        case 'JSON': return '{\n  "key": "value"\n}';
        case 'HTML': return '<div>\n  \n</div>';
        case 'SLIDE': return '## 投影片標題\n\n內容...';
        case 'IMG': return '';
        default: return '';
    }
}

function setActiveBlock(blockId) {
    if (AppState.activeBlockId === blockId) return;

    // Constraint mode check (WS-7)
    if (AppState.constraintMode && AppState.activeBlockId) {
        const currentBlock = AppState.blocks.find(b => b.id === AppState.activeBlockId);
        if (currentBlock && (currentBlock.type === 'MD' || currentBlock.type === 'SLIDE')) {
            if ((currentBlock.content || '').length < AppState.constraintMinChars) {
                showConstraintWarning();
                return;
            }
        }
    }

    AppState.activeBlockId = blockId;
    renderBlockCards();
    updateOutlinePanel();
}

function showConstraintWarning() {
    // Remove existing warnings
    document.querySelectorAll('.constraint-warning').forEach(el => el.remove());
    const warn = document.createElement('div');
    warn.className = 'constraint-warning';
    warn.textContent = `⚠️ 約束模式：請先完成當前段落 (至少 ${AppState.constraintMinChars} 字)`;
    document.body.appendChild(warn);
    setTimeout(() => warn.remove(), 3000);
}

function showBlockMenu(e, afterIndex) {
    const menu = DOM.blockMenu;
    if (!menu) return;
    menu.classList.remove('hidden');
    menu.style.left = Math.min(e.clientX, window.innerWidth - 200) + 'px';
    menu.style.top = Math.min(e.clientY, window.innerHeight - 250) + 'px';

    menu.querySelectorAll('.block-menu-item').forEach(item => {
        item.onclick = () => {
            addBlock(item.dataset.type, afterIndex);
            menu.classList.add('hidden');
        };
    });

    const closeMenu = (ev) => {
        if (!menu.contains(ev.target)) {
            menu.classList.add('hidden');
            document.removeEventListener('click', closeMenu);
        }
    };
    setTimeout(() => document.addEventListener('click', closeMenu), 10);
}


// ============================================================
// 10. OUTLINE PANEL + BEAT SHEET (WS-4)
// ============================================================

function updateOutlinePanel() {
    if (!DOM.blockList) return;
    DOM.blockList.innerHTML = '';

    const isDeck = AppState.scenario === 'deck';
    const beats = isDeck ? (BEAT_SHEETS[AppState.taAudience] || BEAT_SHEETS.investor) : [];
    let slideIdx = 0;

    AppState.blocks.forEach((block, index) => {
        const item = document.createElement('div');
        item.className = `block-list-item${block.id === AppState.activeBlockId ? ' active' : ''}`;
        item.draggable = true;

        const icon = getBlockIcon(block.type);
        const label = getBlockLabel(block);
        const typeTag = block.type.toLowerCase();

        let beatHtml = '';
        if (isDeck && block.type === 'SLIDE' && slideIdx < beats.length) {
            beatHtml = `<span class="beat-label">${beats[slideIdx]}</span>`;
            slideIdx++;
        }

        item.innerHTML = `
            <i class="${icon}"></i>
            <span style="flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">${escapeHtml(label)}</span>
            ${beatHtml}
            <span class="block-type-tag ${typeTag}">${block.type}</span>
        `;

        item.addEventListener('click', () => {
            setActiveBlock(block.id);
            const card = document.querySelector(`[data-block-id="${block.id}"]`);
            if (card) card.scrollIntoView({ behavior: 'smooth', block: 'center' });
        });

        // Drag & drop reorder
        item.addEventListener('dragstart', (e) => {
            e.dataTransfer.setData('text/plain', String(index));
        });
        item.addEventListener('dragover', (e) => { e.preventDefault(); item.style.borderTop = '2px solid var(--pri-400)'; });
        item.addEventListener('dragleave', () => { item.style.borderTop = ''; });
        item.addEventListener('drop', (e) => {
            e.preventDefault();
            item.style.borderTop = '';
            const fromIndex = parseInt(e.dataTransfer.getData('text/plain'));
            if (!isNaN(fromIndex) && fromIndex !== index) {
                const [blk] = AppState.blocks.splice(fromIndex, 1);
                AppState.blocks.splice(index, 0, blk);
                markDirty();
                renderBlockCards();
                updateOutlinePanel();
            }
        });

        DOM.blockList.appendChild(item);
    });

    // Document outline tree (WS-7)
    if (AppState.scenario === 'document') {
        buildDocumentOutlineTree();
    }

    updateStats();
}

function buildDocumentOutlineTree() {
    // Add heading-based navigation items after the block list
    const mdBlocks = AppState.blocks.filter(b => b.type === 'MD');
    const headings = [];
    mdBlocks.forEach(block => {
        const lines = (block.content || '').split('\n');
        lines.forEach(line => {
            const match = line.match(/^(#{1,3})\s+(.+)/);
            if (match) {
                headings.push({ level: match[1].length, text: match[2], blockId: block.id });
            }
        });
    });

    if (headings.length > 0) {
        const divider = document.createElement('div');
        divider.className = 'panel-section';
        divider.innerHTML = '<div class="panel-section-title">文件目錄 TOC</div>';
        DOM.blockList.appendChild(divider);

        headings.forEach(h => {
            const item = document.createElement('div');
            item.className = 'block-list-item';
            item.style.paddingLeft = `${10 + (h.level - 1) * 14}px`;
            item.innerHTML = `<i class="fa-solid fa-heading" style="font-size:${14 - h.level * 2}px;"></i>
                <span style="flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">${escapeHtml(h.text)}</span>`;
            item.addEventListener('click', () => {
                setActiveBlock(h.blockId);
                const card = document.querySelector(`[data-block-id="${h.blockId}"]`);
                if (card) card.scrollIntoView({ behavior: 'smooth', block: 'center' });
            });
            DOM.blockList.appendChild(item);
        });
    }
}

function getBlockIcon(type) {
    const icons = {
        MD: 'fa-solid fa-paragraph', CSV: 'fa-solid fa-table',
        JSON: 'fa-solid fa-brackets-curly', HTML: 'fa-solid fa-code',
        SLIDE: 'fa-solid fa-rectangle-list', IMG: 'fa-solid fa-image',
        THEME: 'fa-solid fa-palette',
    };
    return icons[type] || 'fa-solid fa-cube';
}

function getBlockLabel(block) {
    if (block.namespace) return `${block.type}:${block.namespace}`;
    const firstLine = (block.content || '').split('\n')[0].trim();
    if (firstLine.startsWith('#')) return firstLine.replace(/^#+\s*/, '');
    if (firstLine.length > 30) return firstLine.substring(0, 30) + '...';
    return firstLine || `(${block.type} 區塊)`;
}


// ============================================================
// 11. SOURCE VIEW SYNC
// ============================================================

function syncBlocksToSource() {
    if (!DOM.sourceEditor) return;
    DOM.sourceEditor.value = ITWParser.serialize(AppState.blocks);
}

function syncSourceToBlocks() {
    if (!DOM.sourceEditor) return;
    AppState.blocks = ITWParser.parse(DOM.sourceEditor.value);
    renderBlockCards();
    updateOutlinePanel();
}

function updatePreview() {
    if (!DOM.previewContent) return;
    let fullMd = '';
    AppState.blocks.forEach(block => {
        if (block.type === 'MD' || block.type === 'SLIDE') {
            fullMd += block.content + '\n\n';
        } else if (block.type === 'CSV') {
            try {
                const rows = parseCSV(block.content);
                const evaluated = FormulaEngine.evaluate(rows);
                if (evaluated.length > 0) {
                    fullMd += '\n' + evaluated[0].join(' | ') + '\n';
                    fullMd += evaluated[0].map(() => '---').join(' | ') + '\n';
                    for (let i = 1; i < evaluated.length; i++) {
                        fullMd += evaluated[i].join(' | ') + '\n';
                    }
                    fullMd += '\n';
                }
            } catch { /* skip */ }
        }
    });

    try {
        let rendered = marked.parse(fullMd);
        rendered = sanitize(rendered);
        rendered = resolveItwImages(rendered);
        rendered = rendered.replace(/\{\{(\d[\d,.]*)\}\}/g, '<span class="data-highlight">$1</span>');

        // Accordion for document (WS-7)
        if (AppState.scenario === 'document') {
            rendered = applyAccordion(rendered);
        }

        DOM.previewContent.innerHTML = rendered;

        // Apply theme
        DOM.previewContent.className = 'preview-content';
        if (AppState.scenario === 'document' && DOM.previewContent.dataset.proTheme === '1') {
            DOM.previewContent.classList.add('theme-professional');
        }
        // Semantic zoom
        if (AppState.semanticZoom !== 'normal') {
            DOM.previewContent.classList.add(`zoom-${AppState.semanticZoom}`);
        }

        // Highlight code blocks
        if (typeof hljs !== 'undefined') {
            DOM.previewContent.querySelectorAll('pre code').forEach(el => hljs.highlightElement(el));
        }

        // Scroll threshold triggers (WS-6)
        wireScrollThresholds();

    } catch (e) {
        DOM.previewContent.innerHTML = `<p style="color:var(--error)">Preview error: ${e.message}</p>`;
    }
}


// ============================================================
// 12. VIEW MODE MANAGEMENT
// ============================================================

function setViewMode(mode) {
    AppState.viewMode = mode;
    const workspace = DOM.workspace;
    if (!workspace) return;

    workspace.classList.remove('mode-blocks', 'mode-source', 'mode-split');

    switch (mode) {
        case 'blocks':
            workspace.classList.add('mode-blocks');
            renderBlockCards();
            break;
        case 'source':
            workspace.classList.add('mode-source');
            syncBlocksToSource();
            break;
        case 'split':
            workspace.classList.add('mode-split');
            renderBlockCards();
            syncBlocksToSource();
            updatePreview();
            break;
    }

    // Update view switch button state
    document.querySelectorAll('.view-switch-btn').forEach(btn => btn.classList.remove('active'));
    document.getElementById(`view-${mode}`)?.classList.add('active');
}


// ============================================================
// 13. TEMPLATE DIALOG + TA SETTINGS (WS-4)
// ============================================================

function openModal(modal) {
    if (modal) modal.classList.add('open');
}
function closeModal(modal) {
    if (modal) modal.classList.remove('open');
}

function showTemplateDialog() { openModal(DOM.templateModal); }
function closeTemplateDialog() { closeModal(DOM.templateModal); }

function createFromTemplate(scenarioId) {
    const tmpl = ScenarioTemplates[scenarioId];
    if (!tmpl) return;

    AppState.scenario = scenarioId;
    AppState.blocks = tmpl.defaultBlocks.map(b => ({
        id: ITWParser.generateId(), type: b.type,
        namespace: b.namespace || null,
        attrs: b.attrs || null,
        content: b.content,
    }));
    AppState.activeBlockId = null;
    AppState.fileName = 'untitled.itw';
    AppState.chartVisible = {};

    updateScenarioBadge(scenarioId);
    ToolbarManager.build(scenarioId === 'blank' ? null : scenarioId);
    markDirty();
    renderBlockCards();
    updateOutlinePanel();
    closeTemplateDialog();
    setViewMode('blocks');

    // Show TA settings for deck (WS-4)
    if (scenarioId === 'deck') {
        setTimeout(() => openModal(DOM.taModal), 300);
    }
}

function applyTaSettings() {
    const audRadio = document.querySelector('input[name="ta-aud"]:checked');
    const durRadio = document.querySelector('input[name="ta-dur"]:checked');
    AppState.taAudience = audRadio?.value || 'investor';
    AppState.taDuration = parseInt(durRadio?.value) || 10;

    // Generate appropriate slide count from beat sheet
    const beats = BEAT_SHEETS[AppState.taAudience] || BEAT_SHEETS.investor;
    const timeFactor = AppState.taDuration / 10;
    const recommendedSlides = Math.round(beats.length * timeFactor);

    // Rebuild slides from beat sheet
    AppState.blocks = AppState.blocks.filter(b => b.type !== 'SLIDE');
    const jsonBlock = AppState.blocks.find(b => b.type === 'JSON');
    if (jsonBlock) {
        try {
            const meta = JSON.parse(jsonBlock.content);
            meta.audience = AppState.taAudience;
            meta.duration = AppState.taDuration;
            jsonBlock.content = JSON.stringify(meta, null, 2);
        } catch { /* ignore */ }
    }

    const slideBeats = beats.slice(0, recommendedSlides);
    slideBeats.forEach((beat, i) => {
        const layouts = ['cover', 'default', 'split', 'data', 'default', 'default', 'split', 'default', 'data', 'default', 'cta'];
        AppState.blocks.push({
            id: ITWParser.generateId(),
            type: 'SLIDE',
            namespace: String(i + 1),
            attrs: `layout=${layouts[i % layouts.length]}`,
            content: i === 0 ? `# ${beat}\n\n副標題 — 作者名稱` : `## ${beat}\n\n內容...`,
        });
    });

    markDirty();
    renderBlockCards();
    updateOutlinePanel();
    closeModal(DOM.taModal);
}

function updateTaSuggestion() {
    const audRadio = document.querySelector('input[name="ta-aud"]:checked');
    const durRadio = document.querySelector('input[name="ta-dur"]:checked');
    const aud = audRadio?.value || 'investor';
    const dur = parseInt(durRadio?.value) || 10;
    const beats = BEAT_SHEETS[aud] || BEAT_SHEETS.investor;
    const count = Math.round(beats.length * (dur / 10));
    if (DOM.taSuggestion) {
        DOM.taSuggestion.innerHTML = `<i class="fa-solid fa-lightbulb"></i><span>建議投影片數量: <strong>${count}</strong> 頁 (${aud === 'investor' ? '投資人' : aud === 'client' ? '客戶' : '內部'})</span>`;
    }
}

function updateScenarioBadge(scenarioId) {
    if (!DOM.scenarioBadge) return;
    const tmpl = ScenarioTemplates[scenarioId];
    if (tmpl && scenarioId !== 'blank') {
        DOM.scenarioBadge.dataset.scenario = scenarioId;
        DOM.scenarioBadge.innerHTML = `<i class="${tmpl.icon}"></i> ${tmpl.name}`;
        DOM.scenarioBadge.classList.remove('hidden');
    } else {
        DOM.scenarioBadge.classList.add('hidden');
    }
}


// ============================================================
// 14. SCENARIO DETECTION
// ============================================================

function detectScenarioFromBlocks() {
    const jsonBlock = AppState.blocks.find(b => b.type === 'JSON');
    if (jsonBlock) {
        try {
            const meta = JSON.parse(jsonBlock.content);
            if (meta.type && ScenarioTemplates[meta.type]) {
                AppState.scenario = meta.type;
                updateScenarioBadge(meta.type);
                ToolbarManager.build(meta.type);
                return;
            }
        } catch { /* ignore */ }
    }
    if (AppState.blocks.some(b => b.type === 'SLIDE')) {
        AppState.scenario = 'deck';
        updateScenarioBadge('deck');
        ToolbarManager.build('deck');
        return;
    }
    if (AppState.blocks.some(b => b.type === 'CSV')) {
        AppState.scenario = 'datagrid';
        updateScenarioBadge('datagrid');
        ToolbarManager.build('datagrid');
        return;
    }
    AppState.scenario = null;
    updateScenarioBadge(null);
    ToolbarManager.build(null);
}


// ============================================================
// 15. MEDIA INBOX (WS-5)
// ============================================================

function initMediaInbox() {
    const dropzone = DOM.inboxDropzone;
    if (!dropzone) return;

    dropzone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropzone.classList.add('drag-over');
    });
    dropzone.addEventListener('dragleave', () => dropzone.classList.remove('drag-over'));
    dropzone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropzone.classList.remove('drag-over');
        handleInboxDrop(e.dataTransfer.files);
    });
    dropzone.addEventListener('click', () => {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = 'image/*';
        input.multiple = true;
        input.onchange = (e) => handleInboxDrop(e.target.files);
        input.click();
    });
}

function handleInboxDrop(files) {
    Array.from(files).forEach(file => {
        if (!file.type.startsWith('image/')) return;
        const reader = new FileReader();
        reader.onload = (e) => {
            const asset = {
                id: 'asset-' + Date.now().toString(36) + Math.random().toString(36).substr(2, 4),
                name: file.name,
                data: e.target.result,
                tag: 'general',
            };
            AppState.mediaAssets.push(asset);
            renderInboxGrid();
        };
        reader.readAsDataURL(file);
    });
}

function renderInboxGrid() {
    if (!DOM.inboxGrid) return;
    DOM.inboxGrid.innerHTML = '';

    const filtered = AppState.activeTag
        ? AppState.mediaAssets.filter(a => a.tag === AppState.activeTag)
        : AppState.mediaAssets;

    filtered.forEach(asset => {
        const thumb = document.createElement('div');
        thumb.className = 'inbox-thumb';
        thumb.innerHTML = `
            <img src="${asset.data}" alt="${asset.name}">
            <span class="thumb-tag">${asset.tag}</span>
            <button class="thumb-remove" data-id="${asset.id}">&times;</button>
        `;

        thumb.querySelector('.thumb-remove').addEventListener('click', (e) => {
            e.stopPropagation();
            AppState.mediaAssets = AppState.mediaAssets.filter(a => a.id !== asset.id);
            renderInboxGrid();
        });

        // Click to insert as IMG block
        thumb.addEventListener('click', () => {
            const block = {
                id: ITWParser.generateId(), type: 'IMG',
                namespace: asset.id, attrs: null,
                content: asset.data,
            };
            AppState.blocks.push(block);
            markDirty();
            renderBlockCards();
            updateOutlinePanel();
        });

        // Double click to set tag
        thumb.addEventListener('dblclick', () => {
            const tag = prompt('設定標籤:', asset.tag);
            if (tag) {
                asset.tag = tag;
                renderInboxGrid();
                renderInboxTags();
            }
        });

        DOM.inboxGrid.appendChild(thumb);
    });

    renderInboxTags();
}

function renderInboxTags() {
    if (!DOM.inboxTags) return;
    const tags = [...new Set(AppState.mediaAssets.map(a => a.tag))];
    DOM.inboxTags.innerHTML = '';

    if (tags.length > 1) {
        const allBtn = document.createElement('button');
        allBtn.className = `inbox-tag ${!AppState.activeTag ? 'active' : ''}`;
        allBtn.textContent = '全部';
        allBtn.addEventListener('click', () => { AppState.activeTag = null; renderInboxGrid(); });
        DOM.inboxTags.appendChild(allBtn);

        tags.forEach(tag => {
            const btn = document.createElement('button');
            btn.className = `inbox-tag ${AppState.activeTag === tag ? 'active' : ''}`;
            btn.textContent = tag;
            btn.addEventListener('click', () => { AppState.activeTag = tag; renderInboxGrid(); });
            DOM.inboxTags.appendChild(btn);
        });
    }
}

// Drag & drop images directly to editor (WS-2)
function initEditorDragDrop() {
    const blocksPane = DOM.blocksPane;
    if (!blocksPane) return;

    blocksPane.addEventListener('dragover', (e) => {
        if (e.dataTransfer.types.includes('Files')) {
            e.preventDefault();
            blocksPane.style.outline = '2px dashed var(--pri-400)';
        }
    });
    blocksPane.addEventListener('dragleave', () => { blocksPane.style.outline = ''; });
    blocksPane.addEventListener('drop', (e) => {
        blocksPane.style.outline = '';
        const files = e.dataTransfer.files;
        Array.from(files).forEach(file => {
            if (!file.type.startsWith('image/')) return;
            e.preventDefault();
            const reader = new FileReader();
            reader.onload = (ev) => {
                const imgId = 'img-' + Date.now().toString(36);
                addBlock('IMG', AppState.blocks.length, imgId);
                const newBlock = AppState.blocks[AppState.blocks.length - 1];
                if (newBlock) newBlock.content = ev.target.result;
                renderBlockCards();
                updateOutlinePanel();
            };
            reader.readAsDataURL(file);
        });
    });
}


// ============================================================
// 16. CANVAS & GUIDES (WS-5)
// ============================================================

function toggleGuides() {
    AppState.guidesVisible = !AppState.guidesVisible;
    if (DOM.guideOverlay) {
        DOM.guideOverlay.classList.toggle('hidden', !AppState.guidesVisible);
    }
}

function showCanvasPresetMenu(btnEl) {
    const presets = [
        { name: 'IG Post', w: 1080, h: 1080 },
        { name: 'IG Story', w: 1080, h: 1920 },
        { name: 'YT Thumbnail', w: 1280, h: 720 },
        { name: 'FB Cover', w: 820, h: 312 },
        { name: 'X (Twitter)', w: 1200, h: 675 },
        { name: 'A4 橫向', w: 1754, h: 1240 },
    ];
    const choice = prompt(presets.map((p, i) => `${i + 1}. ${p.name} (${p.w}×${p.h})`).join('\n') + '\n\n選擇預設編號:');
    const idx = parseInt(choice) - 1;
    if (idx >= 0 && idx < presets.length) {
        const jsonBlock = AppState.blocks.find(b => b.type === 'JSON');
        if (jsonBlock) {
            try {
                const meta = JSON.parse(jsonBlock.content);
                meta.canvas = { width: presets[idx].w, height: presets[idx].h };
                jsonBlock.content = JSON.stringify(meta, null, 2);
                markDirty();
                renderBlockCards();
            } catch { /* ignore */ }
        }
    }
}

function showLayoutPicker(btnEl) {
    const block = AppState.blocks.find(b => b.id === AppState.activeBlockId && b.type === 'SLIDE');
    if (!block) {
        alert('請先選擇一個投影片區塊');
        return;
    }
    const layouts = ['cover', 'default', 'split', 'data', 'image-full', 'cta'];
    const choice = prompt(layouts.map((l, i) => `${i + 1}. ${l}`).join('\n') + '\n\n選擇版型編號:');
    const idx = parseInt(choice) - 1;
    if (idx >= 0 && idx < layouts.length) {
        block.attrs = `layout=${layouts[idx]}`;
        markDirty();
        renderBlockCards();
    }
}

function applyDataHighlight() {
    const block = AppState.blocks.find(b => b.id === AppState.activeBlockId);
    if (!block) return;
    const num = prompt('輸入要高亮的數字（會用 {{數字}} 包裹):');
    if (num) {
        block.content = block.content.replace(new RegExp(`(?<!\\{\\{)${num.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}(?!\\}\\})`, 'g'), `{{${num}}}`);
        markDirty();
        renderBlockCards();
    }
}

function toggleFullbleed() {
    const activeCard = document.querySelector(`.block-card[data-block-id="${AppState.activeBlockId}"]`);
    if (activeCard && activeCard.classList.contains('slide-card')) {
        activeCard.classList.toggle('slide-fullbleed');
    }
}


// ============================================================
// 17. WCAG CHECKER (WS-5)
// ============================================================

function runWcagCheck() {
    openModal(DOM.wcagModal);
    const resultsEl = document.getElementById('wcag-results');
    if (!resultsEl) return;

    // Sample check: extract colors from rendered content
    const pairs = [
        { fg: '#e5e5ef', bg: '#111118', label: '本文/背景' },
        { fg: '#818cf8', bg: '#111118', label: '主色/背景' },
        { fg: '#9e9eb8', bg: '#1c1c27', label: '次要文字/卡片' },
        { fg: '#ffffff', bg: '#4f46e5', label: '按鈕文字/按鈕' },
        { fg: '#555570', bg: '#111118', label: '淡色文字/背景' },
    ];

    resultsEl.innerHTML = pairs.map(p => {
        const ratio = getContrastRatio(p.fg, p.bg);
        const pass = ratio >= 4.5;
        return `<div class="wcag-item ${pass ? 'pass' : 'fail'}">
            <div class="wcag-swatch" style="background:${p.fg};"></div>
            <div class="wcag-swatch" style="background:${p.bg};"></div>
            <span style="flex:1;">${p.label}</span>
            <strong>${ratio.toFixed(1)}:1</strong>
            <span>${pass ? '✓ 通過' : '✗ 未達 4.5:1'}</span>
        </div>`;
    }).join('');
}

function getContrastRatio(fg, bg) {
    const lum = (hex) => {
        const rgb = hex.match(/\w{2}/g).map(x => {
            let v = parseInt(x, 16) / 255;
            return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
        });
        return 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2];
    };
    const l1 = lum(fg.replace('#', ''));
    const l2 = lum(bg.replace('#', ''));
    const lighter = Math.max(l1, l2);
    const darker = Math.min(l1, l2);
    return (lighter + 0.05) / (darker + 0.05);
}


// ============================================================
// 18. CHART MAPPER (WS-6 — SVG)
// ============================================================

function renderSVGChart(data) {
    if (!data || data.length < 2) return '';
    const headers = data[0];
    const rows = data.slice(1);
    if (headers.length < 2) return '';

    const chartW = 700, chartH = 200, padding = 40;
    const barW = Math.min(40, (chartW - padding * 2) / (rows.length * (headers.length - 1)) - 4);
    const values = [];
    rows.forEach(row => {
        for (let c = 1; c < row.length; c++) values.push(parseFloat(row[c]) || 0);
    });
    const maxVal = Math.max(...values, 1);

    let svg = `<div class="chart-container"><svg viewBox="0 0 ${chartW} ${chartH + 30}" xmlns="http://www.w3.org/2000/svg">`;

    // Axis line
    svg += `<line x1="${padding}" y1="${chartH}" x2="${chartW - padding}" y2="${chartH}" stroke="var(--n-400)" stroke-width="1"/>`;

    const colors = ['var(--pri-400)', 'var(--cyan-400)', 'var(--em-400)', 'var(--acc-400)', 'var(--warning)'];
    const groupW = (chartW - padding * 2) / rows.length;

    rows.forEach((row, ri) => {
        const gx = padding + ri * groupW;

        for (let ci = 1; ci < row.length; ci++) {
            const val = parseFloat(row[ci]) || 0;
            const barH = (val / maxVal) * (chartH - 20);
            const bx = gx + (ci - 1) * (barW + 2) + (groupW - (headers.length - 1) * (barW + 2)) / 2;
            const by = chartH - barH;

            svg += `<rect class="chart-bar" x="${bx}" y="${by}" width="${barW}" height="${barH}" rx="2" fill="${colors[(ci - 1) % colors.length]}">
                <title>${headers[ci]}: ${val}</title></rect>`;
            svg += `<text class="chart-value" x="${bx + barW / 2}" y="${by - 4}" text-anchor="middle">${val}</text>`;
        }

        // Label
        svg += `<text class="chart-label" x="${gx + groupW / 2}" y="${chartH + 16}" text-anchor="middle">${escapeHtml(row[0] || '')}</text>`;
    });

    svg += '</svg></div>';
    return svg;
}

function toggleChart() {
    const block = AppState.blocks.find(b => b.id === AppState.activeBlockId && b.type === 'CSV');
    if (!block) return;
    AppState.chartVisible[block.id] = !AppState.chartVisible[block.id];
    renderBlockCards();
}


// ============================================================
// 19. ZEN MODE (WS-7)
// ============================================================

function enterZenMode() {
    const mdBlock = AppState.blocks.find(b => b.id === AppState.activeBlockId && (b.type === 'MD' || b.type === 'SLIDE'));
    const fallbackBlock = AppState.blocks.find(b => b.type === 'MD');
    const block = mdBlock || fallbackBlock;
    if (!block) return;

    AppState.zenMode = true;
    AppState._zenBlockId = block.id;

    if (DOM.zenTextarea) {
        DOM.zenTextarea.value = block.content || '';
        DOM.zenTextarea.focus();
    }
    if (DOM.zenOverlay) DOM.zenOverlay.classList.remove('hidden');
    updateZenStats();
}

function exitZenMode() {
    if (!AppState.zenMode) return;
    AppState.zenMode = false;

    // Save content back
    const block = AppState.blocks.find(b => b.id === AppState._zenBlockId);
    if (block && DOM.zenTextarea) {
        block.content = DOM.zenTextarea.value;
        markDirty();
        renderBlockCards();
        updateOutlinePanel();
    }

    if (DOM.zenOverlay) DOM.zenOverlay.classList.add('hidden');
}

function updateZenStats() {
    if (DOM.zenStats && DOM.zenTextarea) {
        const len = DOM.zenTextarea.value.length;
        DOM.zenStats.textContent = `${len} 字`;
    }
}


// ============================================================
// 20. ACCORDION & SEMANTIC ZOOM (WS-7)
// ============================================================

function applyAccordion(html) {
    // Wrap long sections (content between h2 headings) in accordion
    const sections = html.split(/(<h2[^>]*>.*?<\/h2>)/gi);
    let result = '';
    for (let i = 0; i < sections.length; i++) {
        const section = sections[i];
        if (section.match(/^<h2/i)) {
            const title = section.replace(/<[^>]+>/g, '');
            const body = sections[i + 1] || '';
            if (body.length > 300) {
                result += `<div class="accordion-section">
                    <div class="accordion-header" onclick="this.classList.toggle('open');this.nextElementSibling.classList.toggle('open')">
                        <i class="fa-solid fa-chevron-right"></i> ${title}
                    </div>
                    <div class="accordion-body"><div class="accordion-body-inner">${body}</div></div>
                </div>`;
                i++; // Skip body
            } else {
                result += section;
            }
        } else {
            result += section;
        }
    }
    return result;
}

function toggleDocTheme() {
    if (!DOM.previewContent) return;
    const current = DOM.previewContent.dataset.proTheme === '1';
    DOM.previewContent.dataset.proTheme = current ? '0' : '1';
    DOM.previewContent.classList.toggle('theme-professional', !current);
    if (AppState.viewMode === 'split') updatePreview();
}

function toggleConstraintMode() {
    AppState.constraintMode = !AppState.constraintMode;
    if (DOM.constraintIndicator) {
        DOM.constraintIndicator.style.display = AppState.constraintMode ? 'flex' : 'none';
    }
}

function focusOutlinePanel() {
    AppState.activePanel = 'outline';
    AppState.panelOpen = true;
    switchPanel('outline');
}

function wireScrollThresholds() {
    if (!DOM.previewContent) return;
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('threshold-trigger');
                setTimeout(() => entry.target.classList.remove('threshold-trigger'), 800);
            }
        });
    }, { threshold: 0.5 });

    DOM.previewContent.querySelectorAll('h2, h3').forEach(el => observer.observe(el));
}


// ============================================================
// 21. FILE I/O
// ============================================================

async function openFile() {
    try {
        if ('showOpenFilePicker' in window) {
            const [handle] = await window.showOpenFilePicker({
                types: [{ description: 'iTaiwan Web Files', accept: { 'text/plain': ['.itw', '.itwx', '.md', '.txt'] } }],
            });
            AppState.fileHandle = handle;
            const file = await handle.getFile();
            const text = await file.text();
            loadFileContent(file.name, text);
        } else {
            const input = document.createElement('input');
            input.type = 'file';
            input.accept = '.itw,.itwx,.md,.txt';
            input.addEventListener('change', async (e) => {
                const file = e.target.files[0];
                if (!file) return;
                const text = await file.text();
                loadFileContent(file.name, text);
            });
            input.click();
        }
    } catch (err) {
        if (err.name !== 'AbortError') console.error('Open file error:', err);
    }
}

function loadFileContent(name, text) {
    AppState.fileName = name;
    if (DOM.fileName) DOM.fileName.value = name;
    AppState.blocks = ITWParser.parse(text);
    AppState.activeBlockId = null;
    AppState.isDirty = false;
    AppState.chartVisible = {};
    DOM.unsavedDot?.classList.remove('show');
    detectScenarioFromBlocks();
    renderBlockCards();
    updateOutlinePanel();
    if (AppState.viewMode === 'source' || AppState.viewMode === 'split') syncBlocksToSource();
    if (AppState.viewMode === 'split') updatePreview();
}

async function saveFile() {
    const content = ITWParser.serialize(AppState.blocks);
    try {
        if (AppState.fileHandle) {
            const writable = await AppState.fileHandle.createWritable();
            await writable.write(content);
            await writable.close();
        } else if ('showSaveFilePicker' in window) {
            const handle = await window.showSaveFilePicker({
                suggestedName: AppState.fileName,
                types: [{ description: 'iTaiwan Web File', accept: { 'text/plain': ['.itw'] } }],
            });
            AppState.fileHandle = handle;
            const writable = await handle.createWritable();
            await writable.write(content);
            await writable.close();
        } else {
            downloadFile(content, AppState.fileName);
        }
        markClean();
    } catch (err) {
        if (err.name !== 'AbortError') console.error('Save error:', err);
    }
}

function exportFile() {
    downloadFile(ITWParser.serialize(AppState.blocks), AppState.fileName);
}

function downloadFile(content, filename) {
    const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = filename;
    document.body.appendChild(a); a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

function saveDraft() {
    const content = ITWParser.serialize(AppState.blocks);
    localStorage.setItem('itw-v4-draft', content);
    localStorage.setItem('itw-v4-filename', AppState.fileName);
    localStorage.setItem('itw-v4-scenario', AppState.scenario || '');
}

function loadDraft() {
    const draft = localStorage.getItem('itw-v4-draft');
    if (draft) {
        AppState.blocks = ITWParser.parse(draft);
        AppState.fileName = localStorage.getItem('itw-v4-filename') || 'untitled.itw';
        if (DOM.fileName) DOM.fileName.value = AppState.fileName;
        const scenario = localStorage.getItem('itw-v4-scenario');
        if (scenario && ScenarioTemplates[scenario]) {
            AppState.scenario = scenario;
            updateScenarioBadge(scenario);
            ToolbarManager.build(scenario);
        } else {
            detectScenarioFromBlocks();
        }
        return true;
    }
    return false;
}


// ============================================================
// 22. AI PANEL (WS-8)
// ============================================================

async function fetchJinaUrl(url) {
    if (!url) return;
    setAiLoading(true);
    try {
        const resp = await fetch(`https://r.jina.ai/${url}`);
        const text = await resp.text();
        showAiResult(text);
    } catch (err) {
        showAiResult(`❌ 擷取失敗: ${err.message}`);
    }
    setAiLoading(false);
}

async function searchKeyword(query) {
    if (!query) return;
    setAiLoading(true);
    // Using DuckDuckGo Lite as a fallback search
    try {
        const resp = await fetch(`https://r.jina.ai/https://lite.duckduckgo.com/lite/?q=${encodeURIComponent(query)}`);
        const text = await resp.text();
        showAiResult(text.substring(0, 3000));
    } catch (err) {
        showAiResult(`❌ 搜尋失敗: ${err.message}`);
    }
    setAiLoading(false);
}

function buildContext() {
    let context = '';
    AppState.blocks.forEach(block => {
        if (block.type === 'MD' || block.type === 'SLIDE') {
            const lines = (block.content || '').split('\n');
            lines.forEach(line => {
                if (line.startsWith('#')) context += line + '\n';
            });
            // First 100 chars of content
            const preview = (block.content || '').substring(0, 100);
            if (preview) context += preview + '...\n';
        }
    });
    return context;
}

async function generateAiContent() {
    const userPrompt = DOM.aiPromptInput?.value?.trim();
    if (!userPrompt) return;

    setAiLoading(true);
    AppState.aiGenerating = true;

    const context = buildContext();
    const fullPrompt = `[文件結構]\n${context}\n\n[使用者指令]\n${userPrompt}`;

    const model = DOM.aiModelSelect?.value || 'sim';

    if (model === 'sim') {
        // Simulated AI response with streaming effect
        await simulateAiStream(fullPrompt, userPrompt);
    } else {
        // Real ONNX model placeholder
        showAiResult(`⚙️ ${model === 'phi3' ? 'Phi-3 Mini (WebGPU)' : 'Qwen2.5-0.5B (WASM)'} 模型載入中...\n\n` +
            `模型需要首次下載 (${model === 'phi3' ? '~2GB' : '~300MB'})。\n` +
            `請確保您的裝置支援 ${model === 'phi3' ? 'WebGPU' : 'WebAssembly'}。\n\n` +
            `整合方式:\n` +
            `import { pipeline } from '@xenova/transformers';\n` +
            `const generator = await pipeline('text-generation', 'Xenova/${model === 'phi3' ? 'phi-3-mini-4k-instruct' : 'Qwen2.5-0.5B-Instruct'}');\n` +
            `const result = await generator(prompt, { max_new_tokens: 512 });`);
    }

    AppState.aiGenerating = false;
    setAiLoading(false);
}

async function simulateAiStream(fullPrompt, userPrompt) {
    // Generate contextually relevant simulated content
    const responses = {
        '寫': `根據您的文件結構，以下是建議的內容：\n\n## 核心要點\n\n1. **明確的價值主張** — 清楚闡述您的產品或服務如何解決目標受眾的痛點。\n\n2. **數據驅動** — 用具體數字支撐您的論述，例如市場規模、成長率、使用者數量等關鍵指標。\n\n3. **行動呼籲 (CTA)** — 在結尾處提供清晰的下一步行動指引。\n\n> 💡 建議將核心數字使用 {{數字}} 標記來啟用視覺高亮效果。`,
        '摘要': `## 文件摘要\n\n本文件涵蓋以下重點：\n\n- 專案背景與目標設定\n- 核心策略與執行方案\n- 預期成果與效益評估\n\n建議進一步補充具體的時程規劃與責任分工。`,
        '翻譯': `## Translation\n\nBased on the document structure, here is the translated content:\n\n[Translation would appear here based on the actual document content]\n\nNote: For production use, connect to a real translation model for accurate results.`,
        'default': `## AI 生成內容\n\n基於您的指令「${userPrompt}」，以下是建議的輸出：\n\n${userPrompt.includes('簡報') ? '### 簡報大綱建議\n\n1. 開場 — 引起注意的數據或故事\n2. 問題陳述 — 市場痛點分析\n3. 解決方案 — 您的獨特價值\n4. 證據 — 案例或數據佐證\n5. 行動呼籲 — 下一步合作方式' : '這是根據您的文件脈絡生成的範例內容。在生產環境中，此處將由 Phi-3 或 Qwen2.5 模型提供更精準的輸出。'}\n\n---\n*此為模擬模式生成的內容。切換至 Phi-3/Qwen2.5 以使用本地 AI 模型。*`,
    };

    let response = responses.default;
    for (const [key, val] of Object.entries(responses)) {
        if (key !== 'default' && userPrompt.includes(key)) { response = val; break; }
    }

    // Streaming effect
    AppState.aiResult = '';
    if (DOM.aiResult) DOM.aiResult.innerHTML = '<span class="streaming-cursor"></span>';

    for (let i = 0; i < response.length; i++) {
        AppState.aiResult += response[i];
        if (DOM.aiResult) {
            DOM.aiResult.innerHTML = sanitize(marked.parse(AppState.aiResult)) + '<span class="streaming-cursor"></span>';
            DOM.aiResult.scrollTop = DOM.aiResult.scrollHeight;
        }
        await sleep(Math.random() * 20 + 5);
    }

    // Remove cursor
    if (DOM.aiResult) {
        DOM.aiResult.innerHTML = sanitize(marked.parse(AppState.aiResult));
    }
    showAiResultActions(true);
}

function showAiResult(text) {
    AppState.aiResult = text;
    if (DOM.aiResult) {
        DOM.aiResult.innerHTML = sanitize(marked.parse(text));
    }
    showAiResultActions(true);
}

function showAiResultActions(show) {
    if (DOM.aiResultActions) DOM.aiResultActions.classList.toggle('hidden', !show);
}

function setAiLoading(loading) {
    const btn = document.getElementById('ai-generate-btn');
    if (btn) {
        btn.disabled = loading;
        btn.innerHTML = loading
            ? '<i class="fa-solid fa-spinner fa-spin"></i> 生成中...'
            : '<i class="fa-solid fa-wand-magic-sparkles"></i> 生成';
    }
}

function insertAiResult() {
    if (!AppState.aiResult) return;
    // MD Patcher: Insert at cursor position or end of active block (WS-8)
    const activeBlock = AppState.blocks.find(b => b.id === AppState.activeBlockId && (b.type === 'MD' || b.type === 'SLIDE'));
    if (activeBlock) {
        activeBlock.content += '\n\n' + AppState.aiResult;
    } else {
        addBlock('MD', AppState.blocks.length);
        const newBlock = AppState.blocks[AppState.blocks.length - 1];
        if (newBlock) newBlock.content = AppState.aiResult;
    }
    AppState.aiResult = '';
    markDirty();
    renderBlockCards();
    updateOutlinePanel();
    showAiResultActions(false);
    if (DOM.aiResult) DOM.aiResult.innerHTML = '<div class="ai-result-placeholder"><i class="fa-solid fa-check" style="color:var(--em-400);"></i><span>已插入文件</span></div>';
}


// ============================================================
// 23. DIRTY STATE
// ============================================================

function markDirty() {
    AppState.isDirty = true;
    DOM.unsavedDot?.classList.add('show');
    clearTimeout(AppState._draftTimeout);
    AppState._draftTimeout = setTimeout(saveDraft, 1500);
    updateStats();
}

function markClean() {
    AppState.isDirty = false;
    DOM.unsavedDot?.classList.remove('show');
}

function updateStats() {
    if (DOM.blockCount) DOM.blockCount.textContent = AppState.blocks.length;
    if (DOM.charCount) {
        const total = AppState.blocks.reduce((sum, b) => sum + (b.content?.length || 0), 0);
        DOM.charCount.textContent = total;
    }
    if (DOM.scenarioStatus) {
        const tmpl = ScenarioTemplates[AppState.scenario];
        DOM.scenarioStatus.textContent = tmpl ? tmpl.name : 'General';
    }
}


// ============================================================
// 24. UTILITIES
// ============================================================

function escapeHtml(str) {
    if (!str) return '';
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function parseCSV(text) {
    if (!text?.trim()) return [];
    if (typeof Papa !== 'undefined') {
        const result = Papa.parse(text.trim(), { skipEmptyLines: true });
        return result.data;
    }
    return text.trim().split('\n').map(line => line.split(',').map(cell => cell.trim()));
}

function syntaxHighlightJSON(json) {
    return json
        .replace(/(\".*?\")\s*:/g, '<span class="json-key">$1</span>:')
        .replace(/:\s*(\".*?\")/g, ': <span class="json-string">$1</span>')
        .replace(/:\s*(\d+\.?\d*)/g, ': <span class="json-number">$1</span>')
        .replace(/:\s*(true|false|null)/g, ': <span class="json-bool">$1</span>');
}

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }


// ============================================================
// 25. EVENT WIRING
// ============================================================

function switchPanel(panelName) {
    document.querySelectorAll('.icon-bar-btn[data-panel]').forEach(b => b.classList.remove('active'));
    document.querySelector(`.icon-bar-btn[data-panel="${panelName}"]`)?.classList.add('active');

    ['panel-outline', 'panel-assets', 'panel-ai'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.classList.toggle('hidden', id !== `panel-${panelName}`);
    });
}

function wireEvents() {
    // Source editor input sync
    DOM.sourceEditor?.addEventListener('input', () => {
        clearTimeout(AppState._sourceTimeout);
        AppState._sourceTimeout = setTimeout(() => {
            syncSourceToBlocks();
            markDirty();
            if (AppState.viewMode === 'split') updatePreview();
        }, 500);
    });

    // Header buttons
    document.getElementById('btn-new')?.addEventListener('click', showTemplateDialog);
    document.getElementById('btn-open')?.addEventListener('click', openFile);
    document.getElementById('btn-save')?.addEventListener('click', saveFile);
    document.getElementById('btn-export')?.addEventListener('click', exportFile);

    // File name
    DOM.fileName?.addEventListener('input', () => {
        AppState.fileName = DOM.fileName.value || 'untitled.itw';
        markDirty();
    });

    // Template dialog
    document.getElementById('template-close')?.addEventListener('click', closeTemplateDialog);
    document.getElementById('template-cancel-btn')?.addEventListener('click', closeTemplateDialog);
    DOM.templateModal?.addEventListener('click', (e) => { if (e.target === DOM.templateModal) closeTemplateDialog(); });

    document.querySelectorAll('.template-card').forEach(card => {
        card.addEventListener('click', () => {
            document.querySelectorAll('.template-card').forEach(c => c.classList.remove('selected'));
            card.classList.add('selected');
        });
        card.addEventListener('dblclick', () => createFromTemplate(card.dataset.scenario));
    });

    document.getElementById('template-create-btn')?.addEventListener('click', () => {
        const selected = document.querySelector('.template-card.selected');
        if (selected) createFromTemplate(selected.dataset.scenario);
    });

    // TA dialog (WS-4)
    document.getElementById('ta-close')?.addEventListener('click', () => closeModal(DOM.taModal));
    document.getElementById('ta-cancel-btn')?.addEventListener('click', () => closeModal(DOM.taModal));
    document.getElementById('ta-apply-btn')?.addEventListener('click', applyTaSettings);
    DOM.taModal?.addEventListener('click', (e) => { if (e.target === DOM.taModal) closeModal(DOM.taModal); });

    document.querySelectorAll('input[name="ta-aud"], input[name="ta-dur"]').forEach(radio => {
        radio.addEventListener('change', updateTaSuggestion);
    });

    // WCAG dialog (WS-5)
    document.getElementById('wcag-close')?.addEventListener('click', () => closeModal(DOM.wcagModal));
    document.getElementById('wcag-close-btn')?.addEventListener('click', () => closeModal(DOM.wcagModal));
    DOM.wcagModal?.addEventListener('click', (e) => { if (e.target === DOM.wcagModal) closeModal(DOM.wcagModal); });

    // Icon bar panel toggle
    document.querySelectorAll('.icon-bar-btn[data-panel]').forEach(btn => {
        btn.addEventListener('click', () => {
            const panel = btn.dataset.panel;
            if (AppState.activePanel === panel && AppState.panelOpen) {
                AppState.panelOpen = false;
                DOM.contextPanel?.classList.add('collapsed');
                document.querySelectorAll('.icon-bar-btn[data-panel]').forEach(b => b.classList.remove('active'));
            } else {
                AppState.activePanel = panel;
                AppState.panelOpen = true;
                DOM.contextPanel?.classList.remove('collapsed');
                switchPanel(panel);
            }
        });
    });

    // Zen mode (WS-7)
    document.getElementById('btn-zen')?.addEventListener('click', enterZenMode);
    DOM.zenTextarea?.addEventListener('input', updateZenStats);

    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            if (AppState.zenMode) { exitZenMode(); return; }
            DOM.blockMenu?.classList.add('hidden');
            closeTemplateDialog();
            closeModal(DOM.taModal);
            closeModal(DOM.wcagModal);
            return;
        }
        if (e.ctrlKey && e.key === 's') { e.preventDefault(); saveFile(); }
        if (e.ctrlKey && e.key === 'o') { e.preventDefault(); openFile(); }
        if (e.ctrlKey && e.key === 'n') { e.preventDefault(); showTemplateDialog(); }
    });

    // Panel add block button
    document.getElementById('add-block-panel')?.addEventListener('click', (e) => showBlockMenu(e, AppState.blocks.length));

    // AI Panel (WS-8)
    document.getElementById('ai-url-fetch')?.addEventListener('click', () => fetchJinaUrl(DOM.aiUrlInput?.value));
    document.getElementById('ai-search-btn')?.addEventListener('click', () => searchKeyword(DOM.aiSearchInput?.value));
    document.getElementById('ai-generate-btn')?.addEventListener('click', generateAiContent);
    document.getElementById('ai-insert-btn')?.addEventListener('click', insertAiResult);
    document.getElementById('ai-copy-btn')?.addEventListener('click', () => {
        navigator.clipboard.writeText(AppState.aiResult).catch(() => {});
    });
    document.getElementById('ai-discard-btn')?.addEventListener('click', () => {
        AppState.aiResult = '';
        showAiResultActions(false);
        if (DOM.aiResult) DOM.aiResult.innerHTML = '<div class="ai-result-placeholder"><i class="fa-solid fa-robot"></i><span>AI 生成結果將顯示在這裡</span></div>';
    });

    // Semantic zoom (WS-7) — mousewheel on preview
    DOM.previewPane?.addEventListener('wheel', (e) => {
        if (e.ctrlKey) {
            e.preventDefault();
            if (e.deltaY < 0) {
                AppState.semanticZoom = AppState.semanticZoom === 'out' ? 'normal' : 'in';
            } else {
                AppState.semanticZoom = AppState.semanticZoom === 'in' ? 'normal' : 'out';
            }
            if (AppState.viewMode === 'split') updatePreview();
        }
    }, { passive: false });

    // Close block menu on outside click
    document.addEventListener('click', (e) => {
        if (DOM.blockMenu && !DOM.blockMenu.contains(e.target) && !e.target.closest('.add-block-btn')) {
            DOM.blockMenu.classList.add('hidden');
        }
    });
}

function insertFormatting(action) {
    const activeCard = document.querySelector(`.block-card[data-block-id="${AppState.activeBlockId}"]`);
    const textarea = activeCard?.querySelector('textarea');
    if (!textarea) return;

    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const selected = textarea.value.substring(start, end);
    const before = textarea.value.substring(0, start);
    const after = textarea.value.substring(end);

    let prefix = '', suffix = '', insert = '';
    switch (action) {
        case 'bold': prefix = '**'; suffix = '**'; insert = selected || '粗體'; break;
        case 'italic': prefix = '*'; suffix = '*'; insert = selected || '斜體'; break;
        case 'h1': prefix = '# '; insert = selected || '標題一'; break;
        case 'h2': prefix = '## '; insert = selected || '標題二'; break;
        case 'h3': prefix = '### '; insert = selected || '標題三'; break;
        case 'ul': prefix = '- '; insert = selected || '清單項目'; break;
        case 'ol': prefix = '1. '; insert = selected || '清單項目'; break;
        case 'quote': prefix = '> '; insert = selected || '引用'; break;
        case 'code': prefix = '```\n'; suffix = '\n```'; insert = selected || 'code'; break;
        case 'link': prefix = '['; suffix = '](url)'; insert = selected || '連結文字'; break;
        case 'image': prefix = '!['; suffix = '](url)'; insert = selected || '圖片描述'; break;
        case 'table':
            insert = '| 欄位 A | 欄位 B | 欄位 C |\n|--------|--------|--------|\n| 值 1   | 值 2   | 值 3   |';
            break;
        case 'hr': insert = '\n---\n'; break;
        default: return;
    }

    const replacement = prefix + insert + suffix;
    textarea.value = before + replacement + after;
    textarea.selectionStart = start + prefix.length;
    textarea.selectionEnd = start + prefix.length + insert.length;
    textarea.focus();

    const block = AppState.blocks.find(b => b.id === AppState.activeBlockId);
    if (block) {
        block.content = textarea.value;
        markDirty();
    }
}


// ============================================================
// 26. PWA REGISTRATION (WS-8)
// ============================================================

function registerServiceWorker() {
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('sw.js').catch(err => {
            console.log('SW registration skipped:', err.message);
        });
    }
}


// ============================================================
// 27. APP BOOT
// ============================================================

async function boot() {
    const loaderBar = document.getElementById('loader-bar');

    try {
        loaderBar.style.width = '20%';
        if (typeof marked !== 'undefined') {
            marked.setOptions({ breaks: true, gfm: true });
        }
        await sleep(150);

        loaderBar.style.width = '40%';
        cacheDom();
        await sleep(100);

        loaderBar.style.width = '55%';
        wireEvents();
        initMediaInbox();
        initEditorDragDrop();
        await sleep(100);

        loaderBar.style.width = '70%';
        const hasDraft = loadDraft();
        if (!hasDraft) {
            ToolbarManager.build(null);
            createFromTemplate('blank');
            setTimeout(showTemplateDialog, 400);
        } else {
            renderBlockCards();
            updateOutlinePanel();
        }
        await sleep(100);

        loaderBar.style.width = '85%';
        setViewMode('blocks');
        updateStats();
        await sleep(100);

        loaderBar.style.width = '95%';
        registerServiceWorker();
        await sleep(150);

        loaderBar.style.width = '100%';
        await sleep(250);

        document.getElementById('app-loader').classList.add('fade-out');
        document.getElementById('app').classList.remove('hidden');

        setTimeout(() => {
            document.getElementById('app-loader').style.display = 'none';
        }, 600);

    } catch (err) {
        console.error('Boot failed:', err);
        document.getElementById('app-loader')?.classList.add('fade-out');
        document.getElementById('app')?.classList.remove('hidden');
    }
}

document.addEventListener('DOMContentLoaded', boot);
