/**
 * iTW Editor V4 — Scenario-Driven Web App Engine
 * ================================================
 * Core modules:
 *   1. ITW Parser/Serializer  — .itw ⇄ AST
 *   2. Block Editor Engine    — Block-based editing
 *   3. Scenario Templates     — Dynamic UI per app type
 *   4. File I/O               — File System Access API + IndexedDB
 *   5. App Shell              — UI orchestration
 */

// ============================================================
// 1. ITW PARSER / SERIALIZER
// ============================================================

const ITWParser = {
    /**
     * Barrier line regex: ---TYPE--- or ---TYPE:NAMESPACE---
     * Optionally with extra attrs like layout=X
     */
    BARRIER_RE: /^---([A-Z]+)(?::([^\s-]+))?\s*(.*?)---\s*$/,

    VALID_TYPES: ['JSON', 'MD', 'CSV', 'HTML', 'THEME', 'SLIDE', 'IMG'],

    /**
     * Parse raw .itw text into an AST (array of blocks)
     * @param {string} raw - Raw .itw file content
     * @returns {Array<{type: string, namespace?: string, attrs?: string, content: string, id: string}>}
     */
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
                    currentBlock = {
                        id: this.generateId(),
                        type,
                        namespace,
                        attrs,
                        content: '',
                    };
                } else {
                    // Unknown type, treat as content of previous block
                    contentLines.push(line);
                }
            } else {
                contentLines.push(line);
            }
        }

        // Flush final block
        flushBlock();

        // If no blocks found, treat entire content as a single MD block
        if (blocks.length === 0 && raw.trim()) {
            blocks.push({
                id: this.generateId(),
                type: 'MD',
                namespace: null,
                attrs: null,
                content: raw.trim(),
            });
        }

        return blocks;
    },

    /**
     * Serialize AST back to .itw plain text
     * @param {Array} blocks
     * @returns {string}
     */
    serialize(blocks) {
        return blocks.map(block => {
            let barrier = `---${block.type}`;
            if (block.namespace) barrier += `:${block.namespace}`;
            barrier += '---';
            if (block.attrs) {
                barrier = `---${block.type}`;
                if (block.namespace) barrier += `:${block.namespace}`;
                barrier += ` ${block.attrs}---`;
            }
            return `${barrier}\n${block.content}`;
        }).join('\n');
    },

    generateId() {
        return 'blk-' + Date.now().toString(36) + Math.random().toString(36).substr(2, 6);
    },
};


// ============================================================
// 2. SCENARIO TEMPLATES
// ============================================================

const ScenarioTemplates = {
    deck: {
        id: 'deck',
        name: '簡報 Pitch Deck',
        icon: 'fa-solid fa-presentation-screen',
        iconFallback: 'fa-solid fa-display',
        priority: 'P0',
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
        id: 'visual',
        name: '圖片 Visual Content',
        icon: 'fa-solid fa-image',
        iconFallback: 'fa-solid fa-image',
        priority: 'P0',
        description: '社群貼文、YT 封面、活動海報、品牌 Logo',
        color: '#22d3ee',
        defaultBlocks: [
            { type: 'JSON', content: '{\n  "type": "visual",\n  "theme": "vibrant",\n  "canvas": { "width": 1080, "height": 1080 },\n  "date": "' + new Date().toISOString().split('T')[0] + '"\n}' },
            { type: 'MD', content: '# 社群貼文標題\n\n> 你的行動呼籲 (CTA) 放在這裡' },
            { type: 'HTML', content: '<div class="visual-canvas">\n  <!-- 拖曳素材至此 -->\n</div>' },
        ],
    },

    datagrid: {
        id: 'datagrid',
        name: '試算表 DataGrid',
        icon: 'fa-solid fa-table-cells',
        iconFallback: 'fa-solid fa-table',
        priority: 'P1',
        description: '預算規劃、專案追蹤、庫存盤點、財務報表',
        color: '#34d399',
        defaultBlocks: [
            { type: 'JSON', content: '{\n  "type": "datagrid",\n  "theme": "clean",\n  "date": "' + new Date().toISOString().split('T')[0] + '"\n}' },
            { type: 'MD', content: '# 數據報表標題\n\n簡要描述此報表的用途與範圍。' },
            { type: 'CSV', namespace: 'Main', content: '項目,Q1,Q2,Q3,Q4\n營收,1000,1200,1500,1800\n成本,600,650,700,750\n利潤,=B2-B3,=C2-C3,=D2-D3,=E2-E3' },
        ],
    },

    document: {
        id: 'document',
        name: '文件 Document',
        icon: 'fa-solid fa-file-lines',
        iconFallback: 'fa-solid fa-file-lines',
        priority: 'P1',
        description: '商業企劃書、履歷表、會議記錄、合約文件',
        color: '#818cf8',
        defaultBlocks: [
            { type: 'JSON', content: '{\n  "type": "document",\n  "theme": "professional",\n  "author": "",\n  "date": "' + new Date().toISOString().split('T')[0] + '"\n}' },
            { type: 'MD', content: '# 文件標題\n\n## 1. 摘要\n\n本文件的目的與概要...\n\n## 2. 背景\n\n相關背景資訊...\n\n## 3. 內容\n\n主要內容...\n\n## 4. 結論\n\n總結與下一步行動...' },
        ],
    },

    blank: {
        id: 'blank',
        name: '空白文件',
        icon: 'fa-solid fa-file',
        iconFallback: 'fa-solid fa-file',
        priority: null,
        description: '從頭開始，自由組合區塊',
        color: '#9e9eb8',
        defaultBlocks: [
            { type: 'JSON', content: '{\n  "type": "hybrid",\n  "theme": "default"\n}' },
            { type: 'MD', content: '# 新文件\n\n開始寫作...' },
        ],
    },
};


// ============================================================
// 3. APPLICATION STATE
// ============================================================

const AppState = {
    blocks: [],              // Current AST blocks
    activeBlockId: null,     // Currently focused block
    scenario: null,          // Current scenario template id
    fileName: 'untitled.itw',
    isDirty: false,
    viewMode: 'blocks',      // 'blocks' | 'source' | 'split'
    panelOpen: true,
    activePanel: 'outline',  // 'outline' | 'assets' | 'ai'
    fileHandle: null,        // File System Access API handle
};


// ============================================================
// 4. DOM REFERENCES (lazy init)
// ============================================================

let DOM = {};

function cacheDom() {
    DOM = {
        loader: document.getElementById('app-loader'),
        loaderBar: document.getElementById('loader-bar'),
        app: document.getElementById('app'),
        // Header
        fileName: document.getElementById('file-name'),
        unsavedDot: document.getElementById('unsaved-dot'),
        scenarioBadge: document.getElementById('scenario-badge'),
        // Panels
        contextPanel: document.getElementById('context-panel'),
        blockList: document.getElementById('block-list'),
        // Workspace
        sourceEditor: document.getElementById('source-editor'),
        blocksPane: document.getElementById('blocks-pane'),
        blocksContainer: document.getElementById('blocks-container'),
        previewPane: document.getElementById('preview-pane'),
        previewContent: document.getElementById('preview-content'),
        // View buttons
        viewBlocks: document.getElementById('view-blocks'),
        viewSource: document.getElementById('view-source'),
        viewSplit: document.getElementById('view-split'),
        // Status
        blockCount: document.getElementById('block-count'),
        charCount: document.getElementById('char-count'),
        scenarioStatus: document.getElementById('scenario-status'),
        // Modals
        templateModal: document.getElementById('template-modal'),
    };
}


// ============================================================
// 5. BLOCK RENDERING ENGINE
// ============================================================

function renderBlockCards() {
    if (!DOM.blocksContainer) return;
    DOM.blocksContainer.innerHTML = '';

    AppState.blocks.forEach((block, index) => {
        const card = createBlockCard(block, index);
        DOM.blocksContainer.appendChild(card);
    });

    // Add "add block" button at the end
    const addBar = document.createElement('div');
    addBar.className = 'add-block-bar';
    addBar.innerHTML = `
        <button class="add-block-btn" id="add-block-bottom">
            <i class="fa-solid fa-plus"></i> 新增區塊
        </button>
    `;
    DOM.blocksContainer.appendChild(addBar);

    document.getElementById('add-block-bottom')?.addEventListener('click', () => {
        showAddBlockMenu(AppState.blocks.length);
    });
}

function createBlockCard(block, index) {
    const card = document.createElement('div');
    card.className = `block-card${block.id === AppState.activeBlockId ? ' focused' : ''}`;
    card.dataset.blockId = block.id;

    const typeTag = block.type.toLowerCase();
    const typeLabel = block.namespace
        ? `${block.type}:${block.namespace}`
        : block.type;
    const attrsStr = block.attrs ? ` ${block.attrs}` : '';

    card.innerHTML = `
        <div class="block-header">
            <span class="block-drag-handle"><i class="fa-solid fa-grip-vertical"></i></span>
            <span class="block-type-label block-type-tag ${typeTag}">${typeLabel}</span>
            ${attrsStr ? `<span class="block-namespace">${attrsStr}</span>` : ''}
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

    // Focus management
    card.addEventListener('click', () => {
        setActiveBlock(block.id);
    });

    // Wire up textarea edits
    const textarea = card.querySelector('textarea');
    if (textarea) {
        textarea.addEventListener('input', () => {
            block.content = textarea.value;
            markDirty();
            updateOutlinePanel();
            // Live sync: update source view if in split
            if (AppState.viewMode === 'split') {
                syncBlocksToSource();
            }
        });
        textarea.addEventListener('focus', () => setActiveBlock(block.id));
    }

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
            return `<textarea>${escapeHtml(block.content)}</textarea>`;
    }
}

function renderMarkdownBlock(block) {
    if (block.id === AppState.activeBlockId) {
        return `<textarea spellcheck="false">${escapeHtml(block.content)}</textarea>`;
    }
    try {
        const rendered = marked.parse(block.content || '');
        return `<div class="rendered-content">${rendered}</div>`;
    } catch {
        return `<textarea spellcheck="false">${escapeHtml(block.content)}</textarea>`;
    }
}

function renderCSVBlock(block) {
    if (block.id === AppState.activeBlockId) {
        return `<textarea spellcheck="false">${escapeHtml(block.content)}</textarea>`;
    }
    try {
        const rows = parseCSV(block.content);
        if (rows.length === 0) return `<textarea spellcheck="false">${escapeHtml(block.content)}</textarea>`;

        let html = '<table class="csv-table"><thead><tr>';
        rows[0].forEach(h => { html += `<th>${escapeHtml(h)}</th>`; });
        html += '</tr></thead><tbody>';
        for (let i = 1; i < rows.length; i++) {
            html += '<tr>';
            rows[i].forEach(c => { html += `<td>${escapeHtml(c)}</td>`; });
            html += '</tr>';
        }
        html += '</tbody></table>';
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
// 6. BLOCK ACTIONS
// ============================================================

function handleBlockAction(action, blockId, index) {
    switch (action) {
        case 'edit':
            setActiveBlock(blockId);
            break;
        case 'duplicate':
            duplicateBlock(index);
            break;
        case 'moveUp':
            moveBlock(index, -1);
            break;
        case 'moveDown':
            moveBlock(index, 1);
            break;
        case 'delete':
            deleteBlock(index);
            break;
    }
}

function duplicateBlock(index) {
    const original = AppState.blocks[index];
    const dup = {
        ...original,
        id: ITWParser.generateId(),
        content: original.content,
    };
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
    if (AppState.blocks.length <= 1) return; // Don't delete the last block
    AppState.blocks.splice(index, 1);
    if (AppState.activeBlockId === AppState.blocks[index]?.id) {
        AppState.activeBlockId = null;
    }
    markDirty();
    renderBlockCards();
    updateOutlinePanel();
}

function addBlock(type, afterIndex = AppState.blocks.length, namespace = null) {
    const block = {
        id: ITWParser.generateId(),
        type,
        namespace,
        attrs: null,
        content: getDefaultContent(type),
    };
    AppState.blocks.splice(afterIndex, 0, block);
    AppState.activeBlockId = block.id;
    markDirty();
    renderBlockCards();
    updateOutlinePanel();

    // Auto-scroll and focus
    setTimeout(() => {
        const card = document.querySelector(`[data-block-id="${block.id}"]`);
        if (card) {
            card.scrollIntoView({ behavior: 'smooth', block: 'center' });
            const ta = card.querySelector('textarea');
            if (ta) ta.focus();
        }
    }, 100);
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
    AppState.activeBlockId = blockId;
    renderBlockCards();
    updateOutlinePanel();
}

function showAddBlockMenu(afterIndex) {
    const types = ['MD', 'CSV', 'JSON', 'HTML', 'SLIDE'];
    const typeNames = {
        MD: 'Markdown',
        CSV: '試算表',
        JSON: '元數據',
        HTML: '自訂 HTML',
        SLIDE: '投影片',
    };

    // Simple menu (could be upgraded to a floating panel)
    const choice = prompt(
        `新增區塊類型：\n${types.map((t, i) => `${i + 1}. ${typeNames[t]} (${t})`).join('\n')}\n\n輸入編號 (1-${types.length}):`
    );

    const idx = parseInt(choice) - 1;
    if (idx >= 0 && idx < types.length) {
        addBlock(types[idx], afterIndex);
    }
}


// ============================================================
// 7. OUTLINE PANEL
// ============================================================

function updateOutlinePanel() {
    if (!DOM.blockList) return;
    DOM.blockList.innerHTML = '';

    AppState.blocks.forEach((block, index) => {
        const item = document.createElement('div');
        item.className = `block-list-item${block.id === AppState.activeBlockId ? ' active' : ''}`;

        const typeTag = block.type.toLowerCase();
        const icon = getBlockIcon(block.type);
        const label = getBlockLabel(block);

        item.innerHTML = `
            <i class="${icon}"></i>
            <span style="flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">${escapeHtml(label)}</span>
            <span class="block-type-tag ${typeTag}">${block.type}</span>
        `;

        item.addEventListener('click', () => {
            setActiveBlock(block.id);
            const card = document.querySelector(`[data-block-id="${block.id}"]`);
            if (card) card.scrollIntoView({ behavior: 'smooth', block: 'center' });
        });

        DOM.blockList.appendChild(item);
    });

    // Update stats
    if (DOM.blockCount) DOM.blockCount.textContent = AppState.blocks.length;
    if (DOM.charCount) {
        const total = AppState.blocks.reduce((sum, b) => sum + (b.content?.length || 0), 0);
        DOM.charCount.textContent = total;
    }
}

function getBlockIcon(type) {
    const icons = {
        MD: 'fa-solid fa-paragraph',
        CSV: 'fa-solid fa-table',
        JSON: 'fa-solid fa-brackets-curly',
        HTML: 'fa-solid fa-code',
        SLIDE: 'fa-solid fa-rectangle-list',
        IMG: 'fa-solid fa-image',
        THEME: 'fa-solid fa-palette',
    };
    return icons[type] || 'fa-solid fa-cube';
}

function getBlockLabel(block) {
    if (block.namespace) return `${block.type}:${block.namespace}`;
    // Extract first heading or first line
    const firstLine = (block.content || '').split('\n')[0].trim();
    if (firstLine.startsWith('#')) return firstLine.replace(/^#+\s*/, '');
    if (firstLine.length > 30) return firstLine.substring(0, 30) + '...';
    return firstLine || `(${block.type} 區塊)`;
}


// ============================================================
// 8. SOURCE VIEW SYNC
// ============================================================

function syncBlocksToSource() {
    if (!DOM.sourceEditor) return;
    DOM.sourceEditor.value = ITWParser.serialize(AppState.blocks);
}

function syncSourceToBlocks() {
    if (!DOM.sourceEditor) return;
    const raw = DOM.sourceEditor.value;
    AppState.blocks = ITWParser.parse(raw);
    // Preserve active block if possible
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
            // Render CSV as markdown table
            try {
                const rows = parseCSV(block.content);
                if (rows.length > 0) {
                    fullMd += '\n' + rows[0].map(h => h).join(' | ') + '\n';
                    fullMd += rows[0].map(() => '---').join(' | ') + '\n';
                    for (let i = 1; i < rows.length; i++) {
                        fullMd += rows[i].join(' | ') + '\n';
                    }
                    fullMd += '\n';
                }
            } catch { /* skip */ }
        }
    });

    try {
        DOM.previewContent.innerHTML = marked.parse(fullMd);
        // highlight code blocks
        if (typeof hljs !== 'undefined') {
            DOM.previewContent.querySelectorAll('pre code').forEach(block => {
                hljs.highlightElement(block);
            });
        }
    } catch (e) {
        DOM.previewContent.innerHTML = `<p style="color:var(--error)">Preview error: ${e.message}</p>`;
    }
}


// ============================================================
// 9. VIEW MODE MANAGEMENT
// ============================================================

function setViewMode(mode) {
    AppState.viewMode = mode;

    // Toggle active button
    [DOM.viewBlocks, DOM.viewSource, DOM.viewSplit].forEach(btn => {
        if (btn) btn.classList.remove('active');
    });

    const workspace = document.querySelector('.editor-workspace');
    if (!workspace) return;

    // Remove old classes
    workspace.classList.remove('mode-blocks', 'mode-source', 'mode-split');

    switch (mode) {
        case 'blocks':
            workspace.classList.add('mode-blocks');
            DOM.viewBlocks?.classList.add('active');
            renderBlockCards();
            break;
        case 'source':
            workspace.classList.add('mode-source');
            DOM.viewSource?.classList.add('active');
            syncBlocksToSource();
            break;
        case 'split':
            workspace.classList.add('mode-split');
            DOM.viewSplit?.classList.add('active');
            renderBlockCards();
            syncBlocksToSource();
            updatePreview();
            break;
    }
}


// ============================================================
// 10. TEMPLATE DIALOG
// ============================================================

function showTemplateDialog() {
    if (DOM.templateModal) {
        DOM.templateModal.classList.add('open');
    }
}

function closeTemplateDialog() {
    if (DOM.templateModal) {
        DOM.templateModal.classList.remove('open');
    }
}

function createFromTemplate(scenarioId) {
    const tmpl = ScenarioTemplates[scenarioId];
    if (!tmpl) return;

    AppState.scenario = scenarioId;
    AppState.blocks = tmpl.defaultBlocks.map(b => ({
        id: ITWParser.generateId(),
        type: b.type,
        namespace: b.namespace || null,
        attrs: b.attrs || null,
        content: b.content,
    }));
    AppState.activeBlockId = null;
    AppState.fileName = `untitled.itw`;

    // Update UI
    updateScenarioBadge(scenarioId);
    markDirty();
    renderBlockCards();
    updateOutlinePanel();
    closeTemplateDialog();
    setViewMode('blocks');
}

function updateScenarioBadge(scenarioId) {
    if (!DOM.scenarioBadge) return;
    const tmpl = ScenarioTemplates[scenarioId];
    if (tmpl && scenarioId !== 'blank') {
        DOM.scenarioBadge.dataset.scenario = scenarioId;
        DOM.scenarioBadge.innerHTML = `<i class="${tmpl.iconFallback}"></i> ${tmpl.name}`;
        DOM.scenarioBadge.classList.remove('hidden');
    } else {
        DOM.scenarioBadge.classList.add('hidden');
    }
}

function detectScenarioFromBlocks() {
    const jsonBlock = AppState.blocks.find(b => b.type === 'JSON');
    if (jsonBlock) {
        try {
            const meta = JSON.parse(jsonBlock.content);
            if (meta.type && ScenarioTemplates[meta.type]) {
                AppState.scenario = meta.type;
                updateScenarioBadge(meta.type);
                return;
            }
            // Map theme to scenario
            if (meta.theme === 'deck') { AppState.scenario = 'deck'; updateScenarioBadge('deck'); return; }
        } catch { /* ignore */ }
    }
    // Check if there are SLIDE blocks
    if (AppState.blocks.some(b => b.type === 'SLIDE')) {
        AppState.scenario = 'deck';
        updateScenarioBadge('deck');
        return;
    }
    // Check if there are CSV blocks
    if (AppState.blocks.some(b => b.type === 'CSV')) {
        AppState.scenario = 'datagrid';
        updateScenarioBadge('datagrid');
        return;
    }
    AppState.scenario = null;
    updateScenarioBadge(null);
}


// ============================================================
// 11. FILE I/O
// ============================================================

async function openFile() {
    try {
        if ('showOpenFilePicker' in window) {
            const [handle] = await window.showOpenFilePicker({
                types: [{
                    description: 'iTaiwan Web Files',
                    accept: { 'text/plain': ['.itw', '.itwx', '.md', '.txt'] },
                }],
            });
            AppState.fileHandle = handle;
            const file = await handle.getFile();
            const text = await file.text();

            AppState.fileName = file.name;
            DOM.fileName.value = file.name;

            AppState.blocks = ITWParser.parse(text);
            AppState.activeBlockId = null;
            AppState.isDirty = false;
            DOM.unsavedDot?.classList.remove('show');

            detectScenarioFromBlocks();
            renderBlockCards();
            updateOutlinePanel();

            if (AppState.viewMode === 'source' || AppState.viewMode === 'split') {
                syncBlocksToSource();
            }
            if (AppState.viewMode === 'split') {
                updatePreview();
            }
        } else {
            // Fallback: file input
            const input = document.createElement('input');
            input.type = 'file';
            input.accept = '.itw,.itwx,.md,.txt';
            input.addEventListener('change', async (e) => {
                const file = e.target.files[0];
                if (!file) return;
                const text = await file.text();
                AppState.fileName = file.name;
                DOM.fileName.value = file.name;
                AppState.blocks = ITWParser.parse(text);
                AppState.activeBlockId = null;
                detectScenarioFromBlocks();
                renderBlockCards();
                updateOutlinePanel();
            });
            input.click();
        }
    } catch (err) {
        if (err.name !== 'AbortError') {
            console.error('Open file error:', err);
        }
    }
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
                types: [{
                    description: 'iTaiwan Web File',
                    accept: { 'text/plain': ['.itw'] },
                }],
            });
            AppState.fileHandle = handle;
            const writable = await handle.createWritable();
            await writable.write(content);
            await writable.close();
        } else {
            // Fallback: download
            downloadFile(content, AppState.fileName);
        }
        markClean();
    } catch (err) {
        if (err.name !== 'AbortError') {
            console.error('Save error:', err);
        }
    }
}

function exportFile() {
    const content = ITWParser.serialize(AppState.blocks);
    downloadFile(content, AppState.fileName);
}

function downloadFile(content, filename) {
    const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// Auto-save to localStorage
function saveDraft() {
    const content = ITWParser.serialize(AppState.blocks);
    localStorage.setItem('itw-v4-draft', content);
    localStorage.setItem('itw-v4-filename', AppState.fileName);
    localStorage.setItem('itw-v4-scenario', AppState.scenario || '');
}

function loadDraft() {
    const draft = localStorage.getItem('itw-v4-draft');
    const filename = localStorage.getItem('itw-v4-filename');
    const scenario = localStorage.getItem('itw-v4-scenario');

    if (draft) {
        AppState.blocks = ITWParser.parse(draft);
        AppState.fileName = filename || 'untitled.itw';
        if (DOM.fileName) DOM.fileName.value = AppState.fileName;

        if (scenario && ScenarioTemplates[scenario]) {
            AppState.scenario = scenario;
            updateScenarioBadge(scenario);
        } else {
            detectScenarioFromBlocks();
        }
        return true;
    }
    return false;
}


// ============================================================
// 12. DIRTY STATE MANAGEMENT
// ============================================================

function markDirty() {
    AppState.isDirty = true;
    DOM.unsavedDot?.classList.add('show');

    // Debounced auto-save
    clearTimeout(AppState._draftTimeout);
    AppState._draftTimeout = setTimeout(saveDraft, 1500);

    // Update stats
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
// 13. UTILITY FUNCTIONS
// ============================================================

function escapeHtml(str) {
    if (!str) return '';
    return str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
}

function parseCSV(text) {
    if (!text?.trim()) return [];
    return text.trim().split('\n').map(line =>
        line.split(',').map(cell => cell.trim())
    );
}

function syntaxHighlightJSON(json) {
    return json
        .replace(/(".*?")(\s*:)/g, '<span class="json-key">$1</span>$2')
        .replace(/:\s*(".*?")/g, ': <span class="json-string">$1</span>')
        .replace(/:\s*(\d+\.?\d*)/g, ': <span class="json-number">$1</span>')
        .replace(/:\s*(true|false|null)/g, ': <span class="json-bool">$1</span>');
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}


// ============================================================
// 14. EVENT WIRING
// ============================================================

function wireEvents() {
    // View mode buttons
    DOM.viewBlocks?.addEventListener('click', () => setViewMode('blocks'));
    DOM.viewSource?.addEventListener('click', () => setViewMode('source'));
    DOM.viewSplit?.addEventListener('click', () => setViewMode('split'));

    // Source editor input → sync back
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

    // File name change
    DOM.fileName?.addEventListener('input', () => {
        AppState.fileName = DOM.fileName.value || 'untitled.itw';
        markDirty();
    });

    // Template dialog
    document.getElementById('template-close')?.addEventListener('click', closeTemplateDialog);
    DOM.templateModal?.addEventListener('click', (e) => {
        if (e.target === DOM.templateModal) closeTemplateDialog();
    });

    // Template cards
    document.querySelectorAll('.template-card').forEach(card => {
        card.addEventListener('click', () => {
            // Deselect all
            document.querySelectorAll('.template-card').forEach(c => c.classList.remove('selected'));
            card.classList.add('selected');
        });
        card.addEventListener('dblclick', () => {
            createFromTemplate(card.dataset.scenario);
        });
    });

    document.getElementById('template-create-btn')?.addEventListener('click', () => {
        const selected = document.querySelector('.template-card.selected');
        if (selected) {
            createFromTemplate(selected.dataset.scenario);
        }
    });

    // Icon bar panel toggle
    document.querySelectorAll('.icon-bar-btn[data-panel]').forEach(btn => {
        btn.addEventListener('click', () => {
            const panel = btn.dataset.panel;
            document.querySelectorAll('.icon-bar-btn[data-panel]').forEach(b => b.classList.remove('active'));

            if (AppState.activePanel === panel && AppState.panelOpen) {
                // Toggle off
                AppState.panelOpen = false;
                DOM.contextPanel?.classList.add('collapsed');
            } else {
                AppState.activePanel = panel;
                AppState.panelOpen = true;
                btn.classList.add('active');
                DOM.contextPanel?.classList.remove('collapsed');
            }
        });
    });

    // Toolbar buttons
    document.querySelectorAll('.tb-btn[data-action]').forEach(btn => {
        btn.addEventListener('click', () => {
            insertFormatting(btn.dataset.action);
        });
    });

    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.key === 's') {
            e.preventDefault();
            saveFile();
        }
        if (e.ctrlKey && e.key === 'o') {
            e.preventDefault();
            openFile();
        }
        if (e.ctrlKey && e.key === 'n') {
            e.preventDefault();
            showTemplateDialog();
        }
    });

    // Panel "Add Block" button
    document.getElementById('add-block-panel')?.addEventListener('click', () => {
        showAddBlockMenu(AppState.blocks.length);
    });
}

function insertFormatting(action) {
    // Find the active block's textarea
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

    // Update block content
    const block = AppState.blocks.find(b => b.id === AppState.activeBlockId);
    if (block) {
        block.content = textarea.value;
        markDirty();
    }
}


// ============================================================
// 15. APP BOOT
// ============================================================

async function boot() {
    const loaderBar = document.getElementById('loader-bar');

    try {
        // Phase 1: Init libraries
        loaderBar.style.width = '20%';
        if (typeof marked !== 'undefined') {
            marked.setOptions({ breaks: true, gfm: true });
        }
        await sleep(200);

        // Phase 2: Cache DOM
        loaderBar.style.width = '40%';
        cacheDom();
        await sleep(150);

        // Phase 3: Wire events
        loaderBar.style.width = '60%';
        wireEvents();
        await sleep(150);

        // Phase 4: Load data
        loaderBar.style.width = '80%';
        const hasDraft = loadDraft();
        if (!hasDraft) {
            // Show template dialog for new users
            setTimeout(showTemplateDialog, 500);
            // Start with blank
            createFromTemplate('blank');
        }
        await sleep(150);

        // Phase 5: Render
        loaderBar.style.width = '95%';
        setViewMode('blocks');
        updateStats();
        await sleep(200);

        // Done: Reveal
        loaderBar.style.width = '100%';
        await sleep(300);

        document.getElementById('app-loader').classList.add('fade-out');
        document.getElementById('app').classList.remove('hidden');

        setTimeout(() => {
            document.getElementById('app-loader').style.display = 'none';
        }, 600);

    } catch (err) {
        console.error('Boot failed:', err);
        document.getElementById('app-loader').classList.add('fade-out');
        document.getElementById('app').classList.remove('hidden');
    }
}

document.addEventListener('DOMContentLoaded', boot);
