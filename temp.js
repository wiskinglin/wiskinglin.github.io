
/* ================================================================
 * iTAIWAN TWF EDITOR — Core JavaScript
 * Spec: iTaiwan.md v2.1
 * Architecture: Parser → AST → Renderers → Serializer
 * ================================================================ */

// ============================================
// 1. ITW PARSER — .itw text → AST
// ============================================
const ITWParser = {
    /**
     * Parse .itw text into structured AST
     * Supports: ---JSON--- | ---MD--- | ---CSV:Name--- | ---HTML---
     * Unknown types preserved as raw blocks(forward-compatible)
     */
    parse(text) {
        const ast = {
            frontMatter: {},
            sections: [],
            raw: text
        };

        if (!text || !text.trim()) return ast;

        // Normalize line endings
        text = text.replace(/\r\n/g, '\n');

        // Pattern: ---TYPE--- or ---TYPE:Namespace--- or ---TYPE:Namespace key=value---
        const sectionPattern = /^---([A-Z]+)(?::([\w-]+))?(?:\s+(.*?))?---$/gm;
        const markers = [];
        let match;

        while ((match = sectionPattern.exec(text)) !== null) {
            markers.push({
                type: match[1],
                namespace: match[2] || null,
                meta: match[3] || null,
                index: match.index,
                endIndex: match.index + match[0].length
            });
        }

        if (markers.length === 0) {
            // No markers — treat entire content as MD
            ast.sections.push({ type: 'MD', namespace: null, content: text.trim() });
            return ast;
        }

        for (let i = 0; i < markers.length; i++) {
            const marker = markers[i];
            const contentStart = marker.endIndex + 1; // skip newline after marker
            const contentEnd = (i + 1 < markers.length) ? markers[i + 1].index - 1 : text.length;
            const content = text.substring(contentStart, contentEnd).trim();

            if (marker.type === 'JSON' && !marker.namespace) {
                try {
                    ast.frontMatter = JSON.parse(content);
                } catch (e) {
                    ast.frontMatter = { _parseError: e.message, _raw: content };
                }
            } else {
                ast.sections.push({
                    type: marker.type,
                    namespace: marker.namespace,
                    meta: marker.meta,
                    content: content
                });
            }
        }

        return ast;
    }
};

// ============================================
// 2. ITW SERIALIZER — AST → .itw text
// ============================================
const ITWSerializer = {
    serialize(ast) {
        let output = '';

        // Front Matter
        if (ast.frontMatter && Object.keys(ast.frontMatter).length > 0) {
            if (!ast.frontMatter._parseError) {
                output += '---JSON---\n';
                output += JSON.stringify(ast.frontMatter, null, 2) + '\n';
            }
        }

        // Sections
        for (const section of ast.sections) {
            const ns = section.namespace ? `:${section.namespace}` : '';
            const meta = section.meta ? ` ${section.meta}` : '';
            output += `---${section.type}${ns}${meta}---\n`;
            output += section.content + '\n';
        }

        return output.trimEnd() + '\n';
    }
};

// ============================================
// 3. THEME ENGINE — THEME section
// ============================================
const ThemeEngine = {
    applyTheme(theme) {
        document.body.dataset.preset = theme.preset || 'default';
        if (theme.accent) {
            document.documentElement.style.setProperty('--itw-primary', theme.accent);
            document.documentElement.style.setProperty('--itw-gradient', `linear-gradient(135deg, ${theme.accent}, var(--itw-secondary))`);
        } else {
            document.documentElement.style.removeProperty('--itw-primary');
            document.documentElement.style.removeProperty('--itw-gradient');
        }
        if (theme.font) {
            document.documentElement.style.setProperty('--font-content', `${theme.font}, sans-serif`);
        } else {
            document.documentElement.style.removeProperty('--font-content');
        }
    }
};

// ============================================
// 4. BLOCK ENGINE — WYSIWYG Document Editing
// ============================================
const BlockEngine = {
    canvas: null,
    slashMenu: null,
    activeSlashIndex: 0,
    slashItems: null,
    isSlashOpen: false,

    init() {
        this.canvas = document.getElementById('editor-area');
        this.slashMenu = document.getElementById('slash-menu');
        this.slashItems = this.slashMenu.querySelectorAll('.slash-item');

        this.canvas.addEventListener('keydown', (e) => this.handleKeyDown(e));
        this.canvas.addEventListener('input', (e) => this.handleInput(e));

        this.slashItems.forEach((item, idx) => {
            item.addEventListener('mouseenter', () => this.updateSlashSelection(idx));
            item.addEventListener('click', () => this.executeSlashCommand(item.dataset.type));
        });

        document.addEventListener('click', (e) => {
            if (this.isSlashOpen && !this.slashMenu.contains(e.target)) this.closeSlashMenu();
        });
    },

    render(blocksData) {
        this.canvas.innerHTML = '';
        if (!blocksData || blocksData.length === 0) {
            this.canvas.appendChild(this.createBlock('p', ''));
            return;
        }
        blocksData.forEach(data => {
            this.canvas.appendChild(this.createBlock(data.type, data.content));
        });
    },

    save() {
        const blocks = [];
        this.canvas.querySelectorAll('.ce-block').forEach(el => {
            blocks.push({ type: el.dataset.type, content: el.innerText || '' });
        });
        return blocks;
    },

    createBlock(type, content = '') {
        const div = document.createElement('div');
        div.className = 'ce-block';
        div.contentEditable = (type !== 'hr');
        div.dataset.type = type;
        if (type !== 'hr') div.innerText = content;
        return div;
    },

    // Convert blocks → Markdown text
    blocksToMarkdown(blocks) {
        let md = '';
        for (const b of blocks) {
            switch (b.type) {
                case 'h1': md += `# ${b.content}\n\n`; break;
                case 'h2': md += `## ${b.content}\n\n`; break;
                case 'h3': md += `### ${b.content}\n\n`; break;
                case 'quote': md += `> ${b.content}\n\n`; break;
                case 'ul': md += `- ${b.content}\n`; break;
                case 'code': md += `\`\`\`\n${b.content}\n\`\`\`\n\n`; break;
                case 'hr': md += `---\n\n`; break;
                case 'p': default: md += `${b.content}\n\n`; break;
            }
        }
        return md.trim();
    },

    // Convert Markdown text → blocks
    markdownToBlocks(md) {
        if (!md || !md.trim()) return [{ type: 'p', content: '' }];
        const lines = md.split('\n');
        const blocks = [];
        let inCode = false;
        let codeBuffer = '';

        for (const line of lines) {
            if (line.startsWith('```')) {
                if (inCode) {
                    blocks.push({ type: 'code', content: codeBuffer.trim() });
                    codeBuffer = '';
                    inCode = false;
                } else {
                    inCode = true;
                }
                continue;
            }
            if (inCode) { codeBuffer += line + '\n'; continue; }

            const trimmed = line.trim();
            if (!trimmed) continue; // skip empty lines

            if (trimmed === '---' || trimmed === '***' || trimmed === '___') {
                blocks.push({ type: 'hr', content: '' });
            } else if (trimmed.startsWith('### ')) {
                blocks.push({ type: 'h3', content: trimmed.substring(4) });
            } else if (trimmed.startsWith('## ')) {
                blocks.push({ type: 'h2', content: trimmed.substring(3) });
            } else if (trimmed.startsWith('# ')) {
                blocks.push({ type: 'h1', content: trimmed.substring(2) });
            } else if (trimmed.startsWith('> ')) {
                blocks.push({ type: 'quote', content: trimmed.substring(2) });
            } else if (trimmed.startsWith('- ') || trimmed.startsWith('* ')) {
                blocks.push({ type: 'ul', content: trimmed.substring(2) });
            } else if (/^\d+\.\s/.test(trimmed)) {
                blocks.push({ type: 'ul', content: trimmed.replace(/^\d+\.\s/, '') });
            } else {
                blocks.push({ type: 'p', content: trimmed });
            }
        }

        if (inCode && codeBuffer) {
            blocks.push({ type: 'code', content: codeBuffer.trim() });
        }

        return blocks.length > 0 ? blocks : [{ type: 'p', content: '' }];
    },

    // Keyboard handler
    handleKeyDown(e) {
        const block = e.target;
        if (!block.classList.contains('ce-block')) return;

        // Slash menu navigation
        if (this.isSlashOpen) {
            if (e.key === 'ArrowDown') { e.preventDefault(); this.updateSlashSelection((this.activeSlashIndex + 1) % this.slashItems.length); return; }
            if (e.key === 'ArrowUp') { e.preventDefault(); this.updateSlashSelection((this.activeSlashIndex - 1 + this.slashItems.length) % this.slashItems.length); return; }
            if (e.key === 'Enter') { e.preventDefault(); this.executeSlashCommand(this.slashItems[this.activeSlashIndex].dataset.type); return; }
            if (e.key === 'Escape') { e.preventDefault(); this.closeSlashMenu(); return; }
        }

        // Enter — split block
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            const sel = window.getSelection();
            const range = sel.getRangeAt(0);
            const afterRange = range.cloneRange();
            afterRange.selectNodeContents(block);
            afterRange.setStart(range.endContainer, range.endOffset);
            const textAfter = afterRange.toString();
            afterRange.deleteContents();

            let nextType = 'p';
            if (block.dataset.type === 'ul') {
                if (block.innerText.trim() === '') { block.dataset.type = 'p'; return; }
                nextType = 'ul';
            }

            const newBlock = this.createBlock(nextType, textAfter);
            block.after(newBlock);
            this.setCaret(newBlock, 0);
            App.markDirty();
        }

        // Backspace — merge or convert block
        if (e.key === 'Backspace') {
            const sel = window.getSelection();
            if (sel.focusOffset === 0 && sel.isCollapsed) {
                e.preventDefault();
                const prev = block.previousElementSibling;
                if (block.dataset.type !== 'p' && block.innerText.trim() === '') {
                    block.dataset.type = 'p';
                } else if (prev) {
                    if (prev.dataset.type === 'hr') { prev.remove(); }
                    else {
                        const prevLen = prev.innerText.length;
                        prev.innerText += block.innerText;
                        block.remove();
                        this.setCaret(prev, prevLen);
                    }
                }
                App.markDirty();
            }
        }

        // Tab — indent (prevent default)
        if (e.key === 'Tab') {
            e.preventDefault();
        }
    },

    // Input handler — Markdown shortcuts & slash menu
    handleInput(e) {
        const block = e.target;
        if (!block.classList.contains('ce-block')) return;
        const text = block.innerText;
        const sel = window.getSelection();

        // Slash menu trigger
        if (text.endsWith('/') && sel.isCollapsed) {
            const range = sel.getRangeAt(0);
            const rect = range.getBoundingClientRect();
            this.openSlashMenu(rect.left, rect.bottom);
        } else if (this.isSlashOpen && !text.includes('/')) {
            this.closeSlashMenu();
        }

        // Markdown transformers
        if (block.dataset.type === 'p') {
            let transformed = false;
            if (text.startsWith('# ')) { block.dataset.type = 'h1'; block.innerText = text.substring(2); transformed = true; }
            else if (text.startsWith('## ')) { block.dataset.type = 'h2'; block.innerText = text.substring(3); transformed = true; }
            else if (text.startsWith('### ')) { block.dataset.type = 'h3'; block.innerText = text.substring(4); transformed = true; }
            else if (text.startsWith('> ')) { block.dataset.type = 'quote'; block.innerText = text.substring(2); transformed = true; }
            else if (text.startsWith('- ') || text.startsWith('* ')) { block.dataset.type = 'ul'; block.innerText = text.substring(2); transformed = true; }
            else if (text.startsWith('```')) { block.dataset.type = 'code'; block.innerText = text.substring(3); transformed = true; }
            else if (text === '---' || text === '***') { block.dataset.type = 'hr'; block.innerText = ''; block.contentEditable = false; transformed = true; }

            if (transformed) this.setCaret(block, block.innerText.length);
        }

        App.markDirty();
    },

    // Toolbar formatting
    format(command) {
        document.execCommand(command, false, null);
        App.markDirty();
    },

    setBlockType(type) {
        const sel = window.getSelection();
        if (!sel.rangeCount) return;
        let node = sel.anchorNode;
        while (node && !node.classList?.contains('ce-block')) node = node.parentNode;
        if (node) {
            node.dataset.type = type;
            node.contentEditable = (type !== 'hr');
            if (type === 'hr') node.innerText = '';
            App.markDirty();
        }
    },

    insertHR() {
        const sel = window.getSelection();
        if (!sel.rangeCount) return;
        let node = sel.anchorNode;
        while (node && !node.classList?.contains('ce-block')) node = node.parentNode;
        if (node) {
            const hr = this.createBlock('hr', '');
            const newP = this.createBlock('p', '');
            node.after(hr);
            hr.after(newP);
            this.setCaret(newP, 0);
            App.markDirty();
        }
    },

    // Slash menu
    openSlashMenu(x, y) {
        this.isSlashOpen = true;
        this.slashMenu.classList.add('active');
        this.slashMenu.style.left = `${Math.min(x, window.innerWidth - 280)}px`;
        this.slashMenu.style.top = `${y + 8}px`;
        this.updateSlashSelection(0);
    },

    closeSlashMenu() {
        this.isSlashOpen = false;
        this.slashMenu.classList.remove('active');
    },

    updateSlashSelection(idx) {
        this.slashItems[this.activeSlashIndex]?.classList.remove('selected');
        this.activeSlashIndex = idx;
        this.slashItems[this.activeSlashIndex]?.classList.add('selected');
        this.slashItems[this.activeSlashIndex]?.scrollIntoView({ block: 'nearest' });
    },

    executeSlashCommand(type) {
        const sel = window.getSelection();
        if (!sel.rangeCount) return;
        let block = sel.anchorNode;
        while (block && !block.classList?.contains('ce-block')) block = block.parentNode;
        if (block) {
            block.innerText = block.innerText.replace(/\/$/, '');
            if (type === 'hr') {
                block.dataset.type = 'hr';
                block.contentEditable = false;
                block.innerText = '';
                const newP = this.createBlock('p', '');
                block.after(newP);
                this.setCaret(newP, 0);
            } else {
                block.dataset.type = type;
                this.setCaret(block, block.innerText.length);
            }
        }
        this.closeSlashMenu();
        App.markDirty();
    },

    setCaret(el, offset) {
        const sel = window.getSelection();
        const range = document.createRange();
        if (el.childNodes.length > 0) {
            const tn = el.childNodes[0];
            if (tn.nodeType === 3) range.setStart(tn, Math.min(offset, tn.length));
            else { range.selectNodeContents(el); range.collapse(false); }
        } else {
            range.selectNodeContents(el);
            range.collapse(false);
        }
        sel.removeAllRanges();
        sel.addRange(range);
    }
};

// ============================================
// 4. SPREADSHEET RENDERER
// ============================================
const SpreadsheetRenderer = {
    sheets: {},       // { sheetName: { data: [[]], formulas: [[]] } }
    activeSheet: null,
    selectedCell: null,

    init() {
        document.getElementById('formula-input').addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                this.commitFormulaBar();
            }
        });
    },

    // Load CSV sections from AST
    loadFromAST(ast) {
        this.sheets = {};
        const csvSections = ast.sections.filter(s => s.type === 'CSV');

        if (csvSections.length === 0) {
            this.sheets['Sheet1'] = { data: this.createEmptyGrid(20, 10) };
        } else {
            for (const section of csvSections) {
                const name = section.namespace || 'default';
                const parsed = Papa.parse(section.content, { skipEmptyLines: true });
                this.sheets[name] = { data: this.padGrid(parsed.data, 20, 10) };
            }
        }

        this.activeSheet = Object.keys(this.sheets)[0];
        this.renderTabs();
        this.renderGrid();
    },

    createEmptyGrid(rows, cols) {
        return Array.from({ length: rows }, () => Array.from({ length: cols }, () => ''));
    },

    padGrid(data, minRows, minCols) {
        while (data.length < minRows) data.push([]);
        for (let r = 0; r < data.length; r++) {
            while (data[r].length < minCols) data[r].push('');
        }
        return data;
    },

    renderTabs() {
        const container = document.getElementById('sheet-tabs');
        container.innerHTML = '';
        for (const name of Object.keys(this.sheets)) {
            const tab = document.createElement('button');
            tab.className = 'sheet-tab' + (name === this.activeSheet ? ' active' : '');
            tab.textContent = name;
            tab.onclick = () => { this.activeSheet = name; this.renderTabs(); this.renderGrid(); };
            container.appendChild(tab);
        }
        const addBtn = document.createElement('button');
        addBtn.className = 'sheet-tab-add';
        addBtn.textContent = '+';
        addBtn.onclick = () => this.addSheet();
        container.appendChild(addBtn);
    },

    addSheet() {
        let num = Object.keys(this.sheets).length + 1;
        let name = `Sheet${num}`;
        while (this.sheets[name]) name = `Sheet${++num}`;
        this.sheets[name] = { data: this.createEmptyGrid(20, 10) };
        this.activeSheet = name;
        this.renderTabs();
        this.renderGrid();
        App.markDirty();
    },

    renderGrid() {
        const wrapper = document.getElementById('datagrid-wrapper');
        const sheet = this.sheets[this.activeSheet];
        if (!sheet) return;
        const data = sheet.data;

        let html = '<table class="datagrid"><thead><tr><th class="corner"></th>';
        const cols = data[0]?.length || 10;
        for (let c = 0; c < cols; c++) {
            html += `<th>${this.colLetter(c)}</th>`;
        }
        html += '</tr></thead><tbody>';

        for (let r = 0; r < data.length; r++) {
            html += `<tr><th class="row-header">${r + 1}</th>`;
            for (let c = 0; c < cols; c++) {
                const raw = data[r]?.[c] || '';
                const display = this.evaluateCell(raw, data);
                const isFormula = typeof raw === 'string' && raw.startsWith('=');
                const isHeader = (r === 0);
                const cls = (isFormula ? ' formula-cell' : '') + (isHeader ? ' header-row' : '');
                html += `<td class="${cls}" data-r="${r}" data-c="${c}" title="${this.escHtml(raw)}">${this.escHtml(display)}</td>`;
            }
            html += '</tr>';
        }
        html += '</tbody></table>';
        wrapper.innerHTML = html;

        // Cell click handlers
        wrapper.querySelectorAll('td').forEach(td => {
            td.addEventListener('click', () => this.selectCell(td));
            td.addEventListener('dblclick', () => this.editCell(td));
        });
    },

    selectCell(td) {
        wrapper_el = document.getElementById('datagrid-wrapper');
        wrapper_el.querySelectorAll('td.selected').forEach(el => el.classList.remove('selected'));
        td.classList.add('selected');
        const r = parseInt(td.dataset.r);
        const c = parseInt(td.dataset.c);
        this.selectedCell = { r, c, td };
        document.getElementById('active-cell-ref').textContent = `${this.colLetter(c)}${r + 1}`;
        document.getElementById('formula-input').value = this.sheets[this.activeSheet].data[r]?.[c] || '';
    },

    editCell(td) {
        const r = parseInt(td.dataset.r);
        const c = parseInt(td.dataset.c);
        const raw = this.sheets[this.activeSheet].data[r]?.[c] || '';
        td.classList.add('editing');
        td.innerHTML = `<input type="text" value="${this.escHtml(raw)}" />`;
        const input = td.querySelector('input');
        input.focus();
        input.select();

        const commit = () => {
            const val = input.value;
            this.sheets[this.activeSheet].data[r][c] = val;
            td.classList.remove('editing');
            td.textContent = this.evaluateCell(val, this.sheets[this.activeSheet].data);
            if (val.startsWith('=')) td.classList.add('formula-cell');
            else td.classList.remove('formula-cell');
            document.getElementById('formula-input').value = val;
            // Re-render to update dependent formulas
            this.renderGrid();
            App.markDirty();
        };

        input.addEventListener('blur', commit);
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') { e.preventDefault(); commit(); }
            if (e.key === 'Escape') { td.classList.remove('editing'); td.textContent = this.evaluateCell(raw, this.sheets[this.activeSheet].data); }
            if (e.key === 'Tab') { e.preventDefault(); commit(); this.moveSelection(0, e.shiftKey ? -1 : 1); }
        });
    },

    commitFormulaBar() {
        if (!this.selectedCell) return;
        const { r, c } = this.selectedCell;
        const val = document.getElementById('formula-input').value;
        this.sheets[this.activeSheet].data[r][c] = val;
        this.renderGrid();
        App.markDirty();
    },

    moveSelection(dr, dc) {
        if (!this.selectedCell) return;
        const nr = this.selectedCell.r + dr;
        const nc = this.selectedCell.c + dc;
        const td = document.querySelector(`td[data-r="${nr}"][data-c="${nc}"]`);
        if (td) this.selectCell(td);
    },

    // Basic formula evaluator
    evaluateCell(raw, data) {
        if (typeof raw !== 'string' || !raw.startsWith('=')) return raw;
        try {
            const formula = raw.substring(1).trim();

            // SUM(A1:A5) pattern
            const sumMatch = formula.match(/^SUM\(([A-Z]+)(\d+):([A-Z]+)(\d+)\)$/i);
            if (sumMatch) {
                const c1 = this.colIndex(sumMatch[1]), r1 = parseInt(sumMatch[2]) - 1;
                const c2 = this.colIndex(sumMatch[3]), r2 = parseInt(sumMatch[4]) - 1;
                let sum = 0;
                for (let r = r1; r <= r2; r++) for (let c = c1; c <= c2; c++) {
                    const v = parseFloat(this.evaluateCell(data[r]?.[c] || '', data));
                    if (!isNaN(v)) sum += v;
                }
                return sum;
            }

            // AVERAGE(A1:A5)
            const avgMatch = formula.match(/^AVERAGE\(([A-Z]+)(\d+):([A-Z]+)(\d+)\)$/i);
            if (avgMatch) {
                const c1 = this.colIndex(avgMatch[1]), r1 = parseInt(avgMatch[2]) - 1;
                const c2 = this.colIndex(avgMatch[3]), r2 = parseInt(avgMatch[4]) - 1;
                let sum = 0, count = 0;
                for (let r = r1; r <= r2; r++) for (let c = c1; c <= c2; c++) {
                    const v = parseFloat(this.evaluateCell(data[r]?.[c] || '', data));
                    if (!isNaN(v)) { sum += v; count++; }
                }
                return count > 0 ? (sum / count).toFixed(2) : 0;
            }

            // Simple cell reference: A1+B1, A1*B1
            const resolved = formula.replace(/([A-Z]+)(\d+)/gi, (_, col, row) => {
                const c = this.colIndex(col), r = parseInt(row) - 1;
                const v = this.evaluateCell(data[r]?.[c] || '0', data);
                return isNaN(v) ? '0' : v;
            });

            // Safe eval (only math operations)
            if (/^[\d\s+\-*/().]+$/.test(resolved)) {
                return Number(Function(`"use strict"; return (${resolved})`)()).valueOf();
            }

            return raw;
        } catch (e) {
            return '#ERR';
        }
    },

    colLetter(n) {
        let s = '';
        n++;
        while (n > 0) { n--; s = String.fromCharCode(65 + (n % 26)) + s; n = Math.floor(n / 26); }
        return s;
    },

    colIndex(letter) {
        let n = 0;
        for (let i = 0; i < letter.length; i++) {
            n = n * 26 + (letter.charCodeAt(i) - 64);
        }
        return n - 1;
    },

    // Export sheets back to CSV sections
    toSections() {
        const sections = [];
        for (const [name, sheet] of Object.entries(this.sheets)) {
            // Trim empty trailing rows
            let lastDataRow = sheet.data.length - 1;
            while (lastDataRow > 0 && sheet.data[lastDataRow].every(c => !c)) lastDataRow--;
            const trimmed = sheet.data.slice(0, lastDataRow + 1);
            const csv = trimmed.map(row => row.map(cell => {
                if (typeof cell === 'string' && cell.includes(',')) return `"${cell}"`;
                return cell;
            }).join(',')).join('\n');

            if (csv.trim()) {
                sections.push({ type: 'CSV', namespace: name === 'default' ? null : name, content: csv });
            }
        }
        return sections;
    },

    escHtml(s) {
        if (s == null) return '';
        return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }
};

// ============================================
// 6. PRESENTATION RENDERER
// ============================================
const PresentationRenderer = {
    slides: [],
    currentSlide: 0,
    customCSS: '',
    isFullscreen: false,

    loadFromAST(ast) {
        const slideSections = ast.sections.filter(s => s.type === 'SLIDE');
        const htmlSection = ast.sections.find(s => s.type === 'HTML');
        this.customCSS = htmlSection ? htmlSection.content : '';
        this.slides = [];

        if (slideSections.length > 0) {
            this.slides = slideSections.map(s => ({
                id: s.namespace,
                layout: s.meta ? s.meta.replace('layout=', '').trim() : 'default',
                content: s.content
            }));
        } else {
            // backward compatibility for MD
            const mdSection = ast.sections.find(s => s.type === 'MD');
            if (mdSection) {
                const parts = mdSection.content.split(/\n---\n|\n\*\*\*\n|\n___\n/);
                this.slides = parts.map((part, i) => ({
                    id: String(i + 1),
                    layout: 'default',
                    content: part.trim()
                })).filter(s => s.content);
            }
        }

        if (this.slides.length === 0) {
            this.slides = [{ id: '1', layout: 'title-hero', content: '# 空白簡報\n\n按下編輯開始撰寫內容' }];
        }

        this.currentSlide = 0;
        this.renderSlide();
    },

    renderSlide() {
        const frame = document.getElementById('slide-frame');
        const fullFrame = document.getElementById('fullscreen-slide');
        const slide = this.slides[this.currentSlide] || { layout: 'default', content: '' };

        let md = slide.content;
        
        // Basic parser for :left: / :right: in two-col layouts
        if (slide.layout === 'two-col') {
            const leftMatch = md.indexOf(':left:');
            const rightMatch = md.indexOf(':right:');
            if (leftMatch !== -1 && rightMatch !== -1) {
                const header = md.substring(0, leftMatch);
                const left = md.substring(leftMatch + 6, rightMatch).trim();
                const right = md.substring(rightMatch + 7).trim();
                md = `${header}\n<div style="display:flex;gap:40px;text-align:left;width:100%;justify-content:space-between;"><div style="flex:1">\n\n${left}\n\n</div><div style="flex:1">\n\n${right}\n\n</div></div>`;
            }
        }

        // Render Markdown to HTML, sanitize
        let html = DOMPurify.sanitize(marked.parse(md), { ADD_ATTR: ['style'] });

        // Inject custom CSS
        if (this.customCSS) {
            html = `<style>${DOMPurify.sanitize(this.customCSS, { ALLOWED_TAGS: ['style'] })}</style>` + html;
        }

        frame.innerHTML = html;
        fullFrame.innerHTML = html;

        frame.className = `slide-frame layout-${slide.layout}`;
        fullFrame.className = `slide-frame layout-${slide.layout}`;

        // Update counters
        const total = this.slides.length;
        const cur = this.currentSlide + 1;
        document.getElementById('slide-counter').textContent = `${cur} / ${total}`;
        document.getElementById('fullscreen-counter').textContent = `${cur} / ${total}`;
        document.getElementById('slide-prev').disabled = this.currentSlide === 0;
        document.getElementById('slide-next').disabled = this.currentSlide >= total - 1;
    },

    prev() {
        if (this.currentSlide > 0) { this.currentSlide--; this.renderSlide(); }
    },

    next() {
        if (this.currentSlide < this.slides.length - 1) { this.currentSlide++; this.renderSlide(); }
    },

    enterFullscreen() {
        this.isFullscreen = true;
        document.getElementById('fullscreen-pres').classList.add('active');
        this.renderSlide();
    },

    exitFullscreen() {
        this.isFullscreen = false;
        document.getElementById('fullscreen-pres').classList.remove('active');
    }
};

// ============================================
// 6. SOURCE MODE CONTROLLER
// ============================================
const SourceMode = {
    cm: null,
    isActive: false,

    init() {
        this.cm = CodeMirror.fromTextArea(document.getElementById('source-editor'), {
            mode: 'markdown',
            theme: document.documentElement.classList.contains('dark') ? 'dracula' : 'default',
            lineNumbers: true,
            lineWrapping: true,
            tabSize: 2,
            indentWithTabs: false,
            autofocus: false,
        });
        // Apply light theme wrapper
        if (!document.documentElement.classList.contains('dark')) {
            document.getElementById('source-canvas').classList.add('light-cm');
        }
    },

    activate(itwText) {
        this.isActive = true;
        this.cm.setValue(itwText);
        setTimeout(() => this.cm.refresh(), 50);
    },

    deactivate() {
        this.isActive = false;
        return this.cm.getValue();
    },

    updateTheme(isDark) {
        this.cm.setOption('theme', isDark ? 'dracula' : 'default');
        const srcEl = document.getElementById('source-canvas');
        if (isDark) srcEl.classList.remove('light-cm');
        else srcEl.classList.add('light-cm');
    }
};

// ============================================
// 7. TOAST SYSTEM
// ============================================
const Toast = {
    show(message, type = 'info', duration = 3000) {
        const container = document.getElementById('toast-container');
        const el = document.createElement('div');
        el.className = `toast ${type}`;
        const icons = { success: '✓', error: '✗', info: 'ℹ' };
        el.innerHTML = `<span>${icons[type] || '•'}</span> ${message}`;
        container.appendChild(el);
        setTimeout(() => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(8px)';
            el.style.transition = 'all 0.3s ease';
            setTimeout(() => el.remove(), 300);
        }, duration);
    }
};

// ============================================
// 8. FILE I/O (File System Access API)
// ============================================
const FileIO = {
    fileHandle: null,

    async open() {
        try {
            if (window.showOpenFilePicker) {
                const [handle] = await window.showOpenFilePicker({
                    types: [{ description: 'iTaiwan TWF Files', accept: { 'text/plain': ['.itw', '.itwx'] } }],
                    multiple: false
                });
                this.fileHandle = handle;
                const file = await handle.getFile();
                const text = await file.text();
                return { text, name: file.name };
            } else {
                // Fallback: file input
                return new Promise((resolve, reject) => {
                    const input = document.createElement('input');
                    input.type = 'file';
                    input.accept = '.itw,.itwx,.txt';
                    input.onchange = async () => {
                        const file = input.files[0];
                        if (!file) return reject('No file selected');
                        const text = await file.text();
                        resolve({ text, name: file.name });
                    };
                    input.click();
                });
            }
        } catch (e) {
            if (e.name !== 'AbortError') throw e;
            return null;
        }
    },

    async save(text, suggestedName = 'untitled.itw') {
        try {
            if (this.fileHandle) {
                const writable = await this.fileHandle.createWritable();
                await writable.write(text);
                await writable.close();
                return this.fileHandle.name;
            }

            if (window.showSaveFilePicker) {
                const handle = await window.showSaveFilePicker({
                    suggestedName,
                    types: [{ description: 'iTaiwan TWF Files', accept: { 'text/plain': ['.itw'] } }]
                });
                this.fileHandle = handle;
                const writable = await handle.createWritable();
                await writable.write(text);
                await writable.close();
                return handle.name;
            } else {
                // Fallback: download
                const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
                const a = document.createElement('a');
                a.href = URL.createObjectURL(blob);
                a.download = suggestedName;
                a.click();
                URL.revokeObjectURL(a.href);
                return suggestedName;
            }
        } catch (e) {
            if (e.name !== 'AbortError') throw e;
            return null;
        }
    }
};

// ============================================
// 9. IndexedDB DRAFT STORAGE
// ============================================
const DraftDB = {
    DB_NAME: 'itw_editor_drafts',
    STORE: 'drafts',

    async open() {
        return new Promise((resolve, reject) => {
            const req = indexedDB.open(this.DB_NAME, 1);
            req.onupgradeneeded = () => {
                const db = req.result;
                if (!db.objectStoreNames.contains(this.STORE)) {
                    db.createObjectStore(this.STORE, { keyPath: 'id' });
                }
            };
            req.onsuccess = () => resolve(req.result);
            req.onerror = () => reject(req.error);
        });
    },

    async saveDraft(id, content) {
        const db = await this.open();
        const tx = db.transaction(this.STORE, 'readwrite');
        tx.objectStore(this.STORE).put({ id, content, timestamp: Date.now() });
    },

    async loadDraft(id) {
        const db = await this.open();
        return new Promise((resolve) => {
            const tx = db.transaction(this.STORE, 'readonly');
            const req = tx.objectStore(this.STORE).get(id);
            req.onsuccess = () => resolve(req.result?.content || null);
        });
    }
};

// ============================================
// 10. APP CONTROLLER
// ============================================
const App = {
    currentMode: 'document',
    isSourceMode: false,
    isDirty: false,
    ast: null,
    saveTimer: null,
    fileName: '',

    init() {
        BlockEngine.init();
        SpreadsheetRenderer.init();
        SourceMode.init();

        // Load saved theme
        if (localStorage.getItem('itw-theme') === 'dark') {
            document.documentElement.classList.add('dark');
            document.getElementById('theme-icon').textContent = '☀️';
        }

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if ((e.ctrlKey || e.metaKey) && e.key === 's') { e.preventDefault(); this.saveFile(); }
            if ((e.ctrlKey || e.metaKey) && e.key === 'o') { e.preventDefault(); this.openFile(); }
            // Presentation keyboard nav
            if (this.currentMode === 'presentation' && !this.isSourceMode) {
                if (e.key === 'ArrowRight' || e.key === 'ArrowDown' || e.key === ' ') PresentationRenderer.next();
                if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') PresentationRenderer.prev();
                if (e.key === 'Escape') PresentationRenderer.exitFullscreen();
                if (e.key === 'f' || e.key === 'F5') { e.preventDefault(); PresentationRenderer.enterFullscreen(); }
            }
        });

        // Drag & Drop
        document.body.addEventListener('dragover', (e) => { e.preventDefault(); });
        document.body.addEventListener('drop', async (e) => {
            e.preventDefault();
            const file = e.dataTransfer.files[0];
            if (file && (file.name.endsWith('.itw') || file.name.endsWith('.itwx') || file.name.endsWith('.txt'))) {
                const text = await file.text();
                this.loadITW(text, file.name);
            }
        });

        // Auto-load last draft
        this.loadLastDraft();
    },

    async loadLastDraft() {
        try {
            const draft = await DraftDB.loadDraft('autosave');
            if (draft) {
                this.loadITW(draft);
                document.getElementById('welcome-overlay').classList.add('hidden');
                Toast.show('已恢復上次編輯的草稿', 'info');
            }
        } catch (e) {
            // Ignore draft load failures
        }
    },

    // Load .itw content into the editor
    loadITW(text, name = '') {
        this.ast = ITWParser.parse(text);
        this.fileName = name;
        document.getElementById('doc-title').value = this.ast.frontMatter?.title || name.replace(/\.itw$/i, '') || '';
        document.getElementById('welcome-overlay').classList.add('hidden');

        // Auto-detect mode from frontMatter
        const type = this.ast.frontMatter?.type || 'document';
        if (type === 'spreadsheet') this.switchMode('spreadsheet');
        else if (type === 'presentation') this.switchMode('presentation');
        else this.switchMode('document');

        // Load content into all renderers
        this.loadIntoRenderers();

        this.isDirty = false;
        this.updateStatus();
    },

    loadIntoRenderers() {
        // Apply Theme first
        const themeSection = this.ast.sections.find(s => s.type === 'THEME');
        if (themeSection) {
            const themeData = {};
            themeSection.content.split('\n').forEach(line => {
                const parts = line.split(':');
                if (parts.length >= 2) {
                    const k = parts[0].trim();
                    const v = parts.slice(1).join(':').trim();
                    themeData[k] = v;
                }
            });
            ThemeEngine.applyTheme(themeData);
        } else {
            ThemeEngine.applyTheme({}); // defaults
        }

        // Document mode — find first MD section
        const mdSection = this.ast.sections.find(s => s.type === 'MD');
        const mdContent = mdSection ? mdSection.content : '';
        const blocks = BlockEngine.markdownToBlocks(mdContent);
        BlockEngine.render(blocks);

        // Spreadsheet mode
        SpreadsheetRenderer.loadFromAST(this.ast);

        // Presentation mode
        PresentationRenderer.loadFromAST(this.ast);
    },

    // Build AST from current editor state
    buildAST() {
        const title = document.getElementById('doc-title').value;
        const ast = {
            frontMatter: {
                ...(this.ast?.frontMatter || {}),
                type: this.currentMode,
                title: title,
                modified: new Date().toISOString()
            },
            sections: []
        };

        // Set created date if not present
        if (!ast.frontMatter.created) {
            ast.frontMatter.created = new Date().toISOString();
        }
        ast.frontMatter.version = '2.1';

        // Preservation flags for multi-mode switching
        const preserveMD = (this.currentMode !== 'document');
        const preserveCSV = (this.currentMode !== 'spreadsheet');
        const preserveSlides = true; // Slides are edited in source mode for now

        // Theme preservation
        const themeSection = this.ast?.sections.find(s => s.type === 'THEME');
        if (themeSection) ast.sections.push(themeSection);

        // MD section
        if (!preserveMD) {
            const blocks = BlockEngine.save();
            const md = BlockEngine.blocksToMarkdown(blocks);
            if (md.trim()) ast.sections.push({ type: 'MD', namespace: null, content: md });
        } else {
            const existingMD = this.ast?.sections.find(s => s.type === 'MD');
            if (existingMD) ast.sections.push(existingMD);
        }

        // CSV sections
        if (!preserveCSV) {
            const csvSections = SpreadsheetRenderer.toSections();
            ast.sections.push(...csvSections);
        } else {
            const existingCSV = this.ast?.sections.filter(s => s.type === 'CSV') || [];
            ast.sections.push(...existingCSV);
        }

        // SLIDE sections
        if (preserveSlides) {
            const slideSections = this.ast?.sections.filter(s => s.type === 'SLIDE') || [];
            ast.sections.push(...slideSections);
        }

        // HTML section
        const existingHTML = this.ast?.sections.find(s => s.type === 'HTML');
        if (existingHTML) {
            ast.sections.push(existingHTML);
        }

        return ast;
    },

    // New file
    newFile() {
        const defaultContent = `---JSON---
{
  "type": "document",
  "title": "未命名文件",
  "version": "2.1"
}
---MD---
# 歡迎使用 iTaiwan TWF Editor

這是您的新文件。`.itw` 是一種純文字驅動的四合一文件格式。

## 開始寫作

直接在此輸入內容，或按 **/** 喚出指令選單。

- 📄 **文件模式** — 像 Word 一樣寫作
- 📊 **試算表模式** — 像 Excel 一樣處理數據
- 🎬 **簡報模式** — 像 PowerPoint 一樣展示

> 瀏覽器即辦公室，一個 .itw 檔案搞定一切。
`;
        this.loadITW(defaultContent, 'untitled.itw');
        Toast.show('已建立新文件', 'success');
    },

    // Open file
    async openFile() {
        try {
            const result = await FileIO.open();
            if (result) {
                this.loadITW(result.text, result.name);
                Toast.show(`已開啟 ${result.name}`, 'success');
            }
        } catch (e) {
            Toast.show(`開啟失敗：${e.message}`, 'error');
        }
    },

    // Save file
    async saveFile() {
        try {
            let ast;
            if (this.isSourceMode) {
                // In source mode, just save the raw text
                const rawText = SourceMode.deactivate();
                this.ast = ITWParser.parse(rawText);
                this.loadIntoRenderers();
                SourceMode.activate(rawText);
                ast = this.ast;
            } else {
                ast = this.buildAST();
                this.ast = ast;
            }

            const text = ITWSerializer.serialize(ast);
            const suggestedName = (ast.frontMatter?.title || 'untitled').replace(/[\\/:*?"<>|]/g, '_') + '.itw';
            const savedName = await FileIO.save(text, this.fileName || suggestedName);

            if (savedName) {
                this.fileName = savedName;
                this.isDirty = false;
                this.updateStatus();
                Toast.show(`已儲存 ${savedName}`, 'success');
            }

            // Save draft too
            await DraftDB.saveDraft('autosave', text);
        } catch (e) {
            Toast.show(`儲存失敗：${e.message}`, 'error');
        }
    },

    // Mode switching
    switchMode(mode) {
        this.currentMode = mode;

        // Update tabs
        document.querySelectorAll('.mode-tab').forEach(tab => {
            tab.classList.toggle('active', tab.dataset.mode === mode);
        });

        // Hide all panels, show target
        document.querySelectorAll('.canvas-panel').forEach(p => p.classList.remove('active'));

        if (!this.isSourceMode) {
            if (mode === 'document') document.getElementById('doc-canvas').classList.add('active');
            else if (mode === 'spreadsheet') document.getElementById('sheet-canvas').classList.add('active');
            else if (mode === 'presentation') document.getElementById('pres-canvas').classList.add('active');
        }

        // Toolbar visibility
        const toolbar = document.getElementById('toolbar');
        const formulaBar = document.getElementById('formula-bar');
        toolbar.style.display = (mode === 'document' && !this.isSourceMode) ? 'flex' : 'none';
        formulaBar.classList.toggle('visible', mode === 'spreadsheet' && !this.isSourceMode);

        // Status mode text
        const modeLabels = { document: '文件模式', spreadsheet: '試算表模式', presentation: '簡報模式' };
        document.getElementById('status-mode').textContent = modeLabels[mode] || mode;
    },

    // Source mode toggle
    toggleSource() {
        const btn = document.getElementById('source-toggle');
        this.isSourceMode = !this.isSourceMode;
        btn.classList.toggle('active', this.isSourceMode);

        if (this.isSourceMode) {
            // Sync current state to source
            const ast = this.buildAST();
            this.ast = ast;
            const text = ITWSerializer.serialize(ast);
            SourceMode.activate(text);

            // Show source panel, hide others
            document.querySelectorAll('.canvas-panel').forEach(p => p.classList.remove('active'));
            document.getElementById('source-canvas').classList.add('active');
            document.getElementById('toolbar').style.display = 'none';
            document.getElementById('formula-bar').classList.remove('visible');
            document.getElementById('status-mode').textContent = '原始碼模式';
        } else {
            // Parse source back
            const rawText = SourceMode.deactivate();
            this.loadITW(rawText, this.fileName);
            document.getElementById('source-canvas').classList.remove('active');
        }
    },

    // Theme toggle
    toggleTheme() {
        const isDark = document.documentElement.classList.toggle('dark');
        document.getElementById('theme-icon').textContent = isDark ? '☀️' : '🌙';
        localStorage.setItem('itw-theme', isDark ? 'dark' : 'light');
        SourceMode.updateTheme(isDark);
    },

    // Dirty state
    markDirty() {
        this.isDirty = true;
        this.updateStatus();

        clearTimeout(this.saveTimer);
        this.saveTimer = setTimeout(async () => {
            try {
                const ast = this.buildAST();
                const text = ITWSerializer.serialize(ast);
                await DraftDB.saveDraft('autosave', text);
            } catch (e) { /* silent */ }
        }, 2000);
    },

    // Status bar update
    updateStatus() {
        const dot = document.getElementById('status-dot');
        const statusText = document.getElementById('status-text');
        dot.classList.toggle('dirty', this.isDirty);
        statusText.textContent = this.isDirty ? '未儲存' : '已儲存';

        // Word count from block editor
        const blocks = BlockEngine.save();
        const allText = blocks.map(b => b.content).join(' ');
        const words = allText.trim() ? allText.trim().split(/\s+/).length : 0;
        const chars = allText.replace(/\s/g, '').length;
        const readMin = Math.max(1, Math.ceil(chars / 500));
        document.getElementById('status-words').textContent = `${chars} 字`;
        document.getElementById('status-read').textContent = `~${readMin} min read`;
    }
};

// ============================================
// BOOT
// ============================================
document.addEventListener('DOMContentLoaded', () => {
    App.init();
});
