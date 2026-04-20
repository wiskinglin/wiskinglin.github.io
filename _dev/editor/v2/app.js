/**
 * AIMD Studio — AI Markdown Editor
 * =================================
 * Browser-native AI-powered Markdown editor.
 * Integrates: Markdown editing, Transformers.js (ONNX), Jina Reader API, Wikipedia API
 *
 * Uses a robust textarea-based editor with custom enhancements
 * (avoids slow ESM CDN imports for CodeMirror 6)
 */

// ============================================================
// Application State
// ============================================================
const AppState = {
    editorEl: null,             // textarea element
    aiPipeline: null,           // Transformers.js pipeline
    modelName: null,            // Current loaded model name
    isModelLoading: false,
    isGenerating: false,
    lastGeneratedContent: '',
    currentView: 'split',       // 'split' | 'editor' | 'preview'
    panelCollapsed: false,
    unsavedChanges: false,
    locale: 'zh-TW',           // Current language
    undoStack: [],
    redoStack: [],
};

// ============================================================
// i18n — Internationalization
// ============================================================
const i18n = {
    'zh-TW': {
        ai_assistant: 'AI 寫作助手',
        url_mode: '網址',
        search_mode: '搜尋',
        prompt_mode: '指令',
        target_url: '目標網址',
        jina_hint: 'Jina Reader API — 自動將網頁轉為乾淨 Markdown',
        instruction: '指令 (選填)',
        fetch_and_integrate: '抓取並整合',
        search_keywords: '搜尋關鍵字',
        search_hint: '使用 Wikipedia API 進行真實資料搜尋',
        search_and_generate: '搜尋並生成',
        ai_instruction: 'AI 指令',
        use_context: '包含目前文件上下文',
        generate: '生成',
        pipeline: '處理流程',
        step_fetch: '資料擷取',
        step_preprocess: '內容前處理',
        step_prompt: '組裝 Prompt',
        step_infer: 'ONNX 推理',
        logs: '執行記錄',
        preview_placeholder: '即時預覽將會顯示在這裡',
    },
    'en': {
        ai_assistant: 'AI Assistant',
        url_mode: 'URL',
        search_mode: 'Search',
        prompt_mode: 'Prompt',
        target_url: 'Target URL',
        jina_hint: 'Jina Reader API — auto-converts webpages to clean Markdown',
        instruction: 'Instruction (optional)',
        fetch_and_integrate: 'Fetch & Integrate',
        search_keywords: 'Search Keywords',
        search_hint: 'Uses Wikipedia API for real data retrieval',
        search_and_generate: 'Search & Generate',
        ai_instruction: 'AI Instruction',
        use_context: 'Include current document context',
        generate: 'Generate',
        pipeline: 'Processing Pipeline',
        step_fetch: 'Fetch Data',
        step_preprocess: 'Preprocess',
        step_prompt: 'Build Prompt',
        step_infer: 'ONNX Inference',
        logs: 'Logs',
        preview_placeholder: 'Live preview will appear here',
    },
    'ja': {
        ai_assistant: 'AI アシスタント',
        url_mode: 'URL',
        search_mode: '検索',
        prompt_mode: 'プロンプト',
        target_url: '対象URL',
        jina_hint: 'Jina Reader API — ウェブページをMarkdownに自動変換',
        instruction: '指示 (任意)',
        fetch_and_integrate: '取得して統合',
        search_keywords: '検索キーワード',
        search_hint: 'Wikipedia APIで実データを検索',
        search_and_generate: '検索して生成',
        ai_instruction: 'AI 指示',
        use_context: '現在のドキュメント文脈を含める',
        generate: '生成',
        pipeline: '処理パイプライン',
        step_fetch: 'データ取得',
        step_preprocess: '前処理',
        step_prompt: 'プロンプト構築',
        step_infer: 'ONNX 推論',
        logs: 'ログ',
        preview_placeholder: 'ライブプレビューがここに表示されます',
    }
};

const localeOrder = ['zh-TW', 'en', 'ja'];

function t(key) {
    return i18n[AppState.locale]?.[key] || i18n['en']?.[key] || key;
}

function applyI18n() {
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        el.textContent = t(key);
    });
}

// ============================================================
// Logger
// ============================================================
function log(message, type = 'info') {
    const logWindow = document.getElementById('log-window');
    if (!logWindow) return;
    const time = new Date().toLocaleTimeString('en-US', { hour12: false });
    const entry = document.createElement('div');
    entry.className = `log-entry ${type}`;
    entry.textContent = `[${time}] ${message}`;
    logWindow.appendChild(entry);
    logWindow.scrollTop = logWindow.scrollHeight;
}

// ============================================================
// Enhanced Textarea Editor
// ============================================================
function initEditor() {
    const host = document.getElementById('codemirror-host');
    if (!host) return;

    // Create advanced textarea editor
    const editorContainer = document.createElement('div');
    editorContainer.className = 'textarea-editor-container';
    editorContainer.innerHTML = `
        <div class="line-numbers" id="line-numbers"></div>
        <textarea id="md-editor" class="md-textarea" spellcheck="false" autocomplete="off" autocorrect="off" autocapitalize="off"></textarea>
    `;
    host.appendChild(editorContainer);

    const editor = document.getElementById('md-editor');
    AppState.editorEl = editor;

    // Load default content
    const defaultContent = localStorage.getItem('aimd-draft') || `# Welcome to AIMD Studio

Start writing your Markdown here, or use the **AI Assistant** panel on the left to:

- 🔗 **Fetch content** from any URL via Jina Reader API
- 🔍 **Search** topics using Wikipedia API
- 📝 **Generate** text with local ONNX AI models

---

## Features

| Feature | Status |
|---------|--------|
| Markdown Editor | ✅ Active |
| Live Preview | ✅ Active |
| Jina Reader API | ✅ Ready |
| Wikipedia Search | ✅ Ready |
| Local ONNX AI | ⏳ Load model |

> **Tip:** Click on "AI Model" in the header to load a local AI model for text generation.

\`\`\`javascript
// Everything runs in your browser — no server needed!
const editor = new AIMarkdownEditor();
editor.start();
\`\`\`
`;

    editor.value = defaultContent;

    // Event listeners
    editor.addEventListener('input', () => {
        updatePreview();
        updateStats();
        updateLineNumbers();
        markUnsaved();
    });

    editor.addEventListener('scroll', () => {
        syncLineNumberScroll();
    });

    editor.addEventListener('keyup', updateCursorFromTextarea);
    editor.addEventListener('click', updateCursorFromTextarea);

    // Tab key support
    editor.addEventListener('keydown', (e) => {
        if (e.key === 'Tab') {
            e.preventDefault();
            const start = editor.selectionStart;
            const end = editor.selectionEnd;
            editor.value = editor.value.substring(0, start) + '    ' + editor.value.substring(end);
            editor.selectionStart = editor.selectionEnd = start + 4;
            editor.dispatchEvent(new Event('input'));
        }
        // Ctrl+S
        if (e.ctrlKey && e.key === 's') {
            e.preventDefault();
            saveDraft();
        }
        // Ctrl+B
        if (e.ctrlKey && e.key === 'b') {
            e.preventDefault();
            insertMarkdown('bold');
        }
        // Ctrl+I
        if (e.ctrlKey && e.key === 'i') {
            e.preventDefault();
            insertMarkdown('italic');
        }
    });

    // Initial render
    updateLineNumbers();
    updatePreview();
    updateStats();
    updateCursorFromTextarea();

    log('Markdown editor initialized.');
}

function updateLineNumbers() {
    const editor = AppState.editorEl;
    if (!editor) return;
    const lineNums = document.getElementById('line-numbers');
    if (!lineNums) return;

    const lines = editor.value.split('\n');
    let html = '';
    for (let i = 1; i <= lines.length; i++) {
        html += `<div class="line-num">${i}</div>`;
    }
    lineNums.innerHTML = html;
}

function syncLineNumberScroll() {
    const editor = AppState.editorEl;
    const lineNums = document.getElementById('line-numbers');
    if (editor && lineNums) {
        lineNums.scrollTop = editor.scrollTop;
    }
}

function updateCursorFromTextarea() {
    const editor = AppState.editorEl;
    if (!editor) return;
    const pos = editor.selectionStart;
    const textBefore = editor.value.substring(0, pos);
    const lines = textBefore.split('\n');
    const lineNum = lines.length;
    const colNum = lines[lines.length - 1].length + 1;
    document.getElementById('cursor-info').textContent = `Ln ${lineNum}, Col ${colNum}`;
}

// ============================================================
// Markdown Preview (marked.js + highlight.js)
// ============================================================
function initMarked() {
    if (typeof marked === 'undefined') return;

    marked.setOptions({
        breaks: true,
        gfm: true,
        highlight: function (code, lang) {
            if (typeof hljs !== 'undefined') {
                if (lang && hljs.getLanguage(lang)) {
                    try { return hljs.highlight(code, { language: lang }).value; } catch (e) { }
                }
                return hljs.highlightAuto(code).value;
            }
            return code;
        },
    });
}

function updatePreview() {
    const content = getEditorContent();
    const previewEl = document.getElementById('preview-content');
    if (!previewEl) return;

    if (!content.trim()) {
        previewEl.innerHTML = `
            <div class="preview-placeholder">
                <i class="fa-solid fa-eye"></i>
                <p>${t('preview_placeholder')}</p>
            </div>`;
        return;
    }

    try {
        previewEl.innerHTML = marked.parse(content);
        // Apply highlight.js to code blocks
        if (typeof hljs !== 'undefined') {
            previewEl.querySelectorAll('pre code').forEach(block => {
                hljs.highlightElement(block);
            });
        }
    } catch (e) {
        previewEl.innerHTML = `<p style="color:var(--error)">Preview error: ${e.message}</p>`;
    }
}

// ============================================================
// Editor Helpers
// ============================================================
function getEditorContent() {
    return AppState.editorEl ? AppState.editorEl.value : '';
}

function setEditorContent(text) {
    if (!AppState.editorEl) return;
    AppState.editorEl.value = text;
    updatePreview();
    updateStats();
    updateLineNumbers();
}

function appendToEditor(text) {
    if (!AppState.editorEl) return;
    const separator = AppState.editorEl.value.length > 0 ? '\n\n' : '';
    AppState.editorEl.value += separator + text;
    updatePreview();
    updateStats();
    updateLineNumbers();
    AppState.editorEl.scrollTop = AppState.editorEl.scrollHeight;
}

async function streamToEditor(text, speed = 3) {
    if (!AppState.editorEl) return;
    const separator = AppState.editorEl.value.length > 0 ? '\n\n---\n\n' : '';

    if (separator) {
        AppState.editorEl.value += separator;
    }

    for (let i = 0; i < text.length; i += speed) {
        if (!AppState.isGenerating) break;
        const chunk = text.substring(i, i + speed);
        AppState.editorEl.value += chunk;
        updatePreview();
        updateLineNumbers();
        AppState.editorEl.scrollTop = AppState.editorEl.scrollHeight;
        await sleep(6);
    }

    updateStats();
}

function insertMarkdown(action) {
    const editor = AppState.editorEl;
    if (!editor) return;

    const start = editor.selectionStart;
    const end = editor.selectionEnd;
    const selectedText = editor.value.substring(start, end);
    const before = editor.value.substring(0, start);
    const after = editor.value.substring(end);

    let prefix = '', suffix = '', insert = '';

    switch (action) {
        case 'bold': prefix = '**'; suffix = '**'; insert = selectedText || 'bold text'; break;
        case 'italic': prefix = '*'; suffix = '*'; insert = selectedText || 'italic text'; break;
        case 'strikethrough': prefix = '~~'; suffix = '~~'; insert = selectedText || 'strikethrough'; break;
        case 'h1': prefix = '# '; insert = selectedText || 'Heading 1'; break;
        case 'h2': prefix = '## '; insert = selectedText || 'Heading 2'; break;
        case 'h3': prefix = '### '; insert = selectedText || 'Heading 3'; break;
        case 'ul': prefix = '- '; insert = selectedText || 'List item'; break;
        case 'ol': prefix = '1. '; insert = selectedText || 'List item'; break;
        case 'quote': prefix = '> '; insert = selectedText || 'Quote'; break;
        case 'code': prefix = '```\n'; suffix = '\n```'; insert = selectedText || 'code'; break;
        case 'link': prefix = '['; suffix = '](url)'; insert = selectedText || 'link text'; break;
        case 'image': prefix = '!['; suffix = '](url)'; insert = selectedText || 'alt text'; break;
        case 'table':
            insert = '| Header 1 | Header 2 | Header 3 |\n|----------|----------|----------|\n| Cell 1   | Cell 2   | Cell 3   |';
            break;
        case 'hr': insert = '\n---\n'; break;
        default: return;
    }

    const replacement = prefix + insert + suffix;
    editor.value = before + replacement + after;

    // Set cursor position
    const newPos = start + prefix.length + insert.length;
    editor.selectionStart = start + prefix.length;
    editor.selectionEnd = newPos;
    editor.focus();

    editor.dispatchEvent(new Event('input'));
}

// ============================================================
// Stats & Status
// ============================================================
function updateStats() {
    const content = getEditorContent();
    document.getElementById('char-count').textContent = content.length;
    document.getElementById('word-count').textContent = countWords(content);
    document.getElementById('line-count').textContent = content.split('\n').length;

    // Language detection
    const hasChinese = /[\u4e00-\u9fa5]/.test(content);
    const hasJapanese = /[\u3040-\u309f\u30a0-\u30ff]/.test(content);
    const hasKorean = /[\uac00-\ud7af]/.test(content);
    let lang = 'English';
    if (hasChinese) lang = '中文';
    else if (hasJapanese) lang = '日本語';
    else if (hasKorean) lang = '한국어';
    document.getElementById('detected-lang').textContent = lang;
}

function countWords(text) {
    const cjk = text.match(/[\u4e00-\u9fff\u3040-\u309f\u30a0-\u30ff\uac00-\ud7af]/g);
    const eng = text.replace(/[\u4e00-\u9fff\u3040-\u309f\u30a0-\u30ff\uac00-\ud7af]/g, ' ')
        .split(/\s+/).filter(w => w.length > 0);
    return (cjk ? cjk.length : 0) + eng.length;
}

function markUnsaved() {
    AppState.unsavedChanges = true;
    document.getElementById('unsaved-dot').classList.add('show');
}

function markSaved() {
    AppState.unsavedChanges = false;
    document.getElementById('unsaved-dot').classList.remove('show');
}

// ============================================================
// Draft Save / Load / Export
// ============================================================
function saveDraft() {
    const content = getEditorContent();
    localStorage.setItem('aimd-draft', content);
    localStorage.setItem('aimd-filename', document.getElementById('file-name-input').value);
    markSaved();
    log('Draft saved to localStorage.', 'success');

    const btn = document.getElementById('save-btn');
    btn.innerHTML = '<i class="fa-solid fa-check"></i>';
    setTimeout(() => { btn.innerHTML = '<i class="fa-regular fa-floppy-disk"></i>'; }, 1500);
}

function loadDraft() {
    const saved = localStorage.getItem('aimd-draft');
    const filename = localStorage.getItem('aimd-filename');
    if (saved) {
        setEditorContent(saved);
        log('Loaded draft from localStorage.', 'success');
    }
    if (filename) {
        document.getElementById('file-name-input').value = filename;
    }
}

function exportMarkdown() {
    const content = getEditorContent();
    const filename = document.getElementById('file-name-input').value || 'untitled.md';
    const blob = new Blob([content], { type: 'text/markdown;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    log(`Exported: ${filename}`, 'success');
}

// ============================================================
// AI Model Management (Transformers.js - Dynamic Import)
// ============================================================
async function loadModel(modelId) {
    if (AppState.isModelLoading) return;
    AppState.isModelLoading = true;

    const statusBtn = document.getElementById('model-status-btn');
    const statusIndicators = statusBtn.querySelectorAll('.status-indicator');
    const modelNameDisplay = document.getElementById('model-name-display');
    const progressSection = document.getElementById('model-progress-section');
    const progressBar = document.getElementById('model-download-bar');
    const progressPct = document.getElementById('model-download-pct');
    const progressLabel = document.getElementById('model-download-label');

    // Update UI
    statusIndicators.forEach(i => i.className = 'status-indicator loading');
    modelNameDisplay.textContent = 'Loading...';
    progressSection.style.display = 'block';
    progressBar.style.width = '0%';

    log(`Loading model: ${modelId}...`);
    log('Downloading Transformers.js runtime...');

    try {
        // Dynamic import of Transformers.js
        const { pipeline, env } = await import('https://cdn.jsdelivr.net/npm/@xenova/transformers@2.17.2');
        env.allowLocalModels = false;

        log('Transformers.js loaded. Downloading ONNX model...');

        // Create pipeline with progress callback
        AppState.aiPipeline = await pipeline('text2text-generation', modelId, {
            progress_callback: (progress) => {
                if (progress.status === 'download' || progress.status === 'progress') {
                    const pct = progress.progress ? Math.round(progress.progress) : 0;
                    progressBar.style.width = `${pct}%`;
                    progressPct.textContent = `${pct}%`;
                    progressLabel.textContent = progress.file
                        ? `Downloading ${progress.file}...`
                        : 'Downloading model files...';
                } else if (progress.status === 'init' || progress.status === 'ready') {
                    progressLabel.textContent = 'Initializing ONNX Runtime...';
                    progressBar.style.width = '100%';
                    progressPct.textContent = '100%';
                }
            },
        });

        AppState.modelName = modelId;
        AppState.isModelLoading = false;

        // Success
        statusIndicators.forEach(i => i.className = 'status-indicator ready');
        const shortName = modelId.split('/').pop();
        modelNameDisplay.textContent = shortName;
        progressLabel.textContent = 'Model loaded successfully!';

        log(`✅ Model loaded: ${shortName}`, 'success');

        // Update status bar
        const inferInfo = document.getElementById('inference-info');
        const inferIndicator = inferInfo.querySelector('.status-indicator');
        if (inferIndicator) inferIndicator.className = 'status-indicator ready';
        document.getElementById('inference-speed').textContent = 'ONNX Ready';

        // Close modal after short delay
        setTimeout(() => closeModal('model-modal'), 1200);

    } catch (error) {
        AppState.isModelLoading = false;
        statusIndicators.forEach(i => i.className = 'status-indicator error');
        modelNameDisplay.textContent = 'Load failed';
        progressLabel.textContent = `Error: ${error.message}`;
        log(`❌ Model load failed: ${error.message}`, 'error');
    }
}

// ============================================================
// Web Data Fetching
// ============================================================

// Jina Reader API
async function fetchViaJina(url) {
    log(`Fetching via Jina Reader: ${url}`);
    const jinaUrl = `https://r.jina.ai/${url.startsWith('http') ? url : 'https://' + url}`;

    const response = await fetch(jinaUrl);
    if (!response.ok) throw new Error(`Jina fetch failed: ${response.status}`);

    let text = await response.text();

    if (text.length > 6000) {
        text = text.substring(0, 6000) + '\n\n...(Content truncated for processing)';
        log('Content truncated to 6000 chars.', 'warn');
    }

    // Cache
    try {
        localStorage.setItem(`jina-cache-${url}`, JSON.stringify({ text, ts: Date.now() }));
    } catch (e) { /* cache full */ }

    log(`Fetched ${text.length} characters from URL.`, 'success');
    return text;
}

// Wikipedia API
async function searchWikipedia(keyword) {
    log(`Searching Wikipedia: "${keyword}"`);

    const langs = ['zh', 'en'];
    for (const lang of langs) {
        try {
            const url = `https://${lang}.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&exintro=true&explaintext=true&titles=${encodeURIComponent(keyword)}&origin=*`;
            const response = await fetch(url);
            const data = await response.json();
            const pages = data.query.pages;
            const pageId = Object.keys(pages)[0];

            if (pageId !== '-1' && pages[pageId].extract) {
                const extract = pages[pageId].extract.substring(0, 2000);
                log(`Found Wikipedia (${lang}) data: ${extract.length} chars.`, 'success');
                return { text: extract, source: `Wikipedia (${lang})`, title: pages[pageId].title };
            }
        } catch (e) {
            log(`Wikipedia (${lang}) failed: ${e.message}`, 'warn');
        }
    }

    log('No Wikipedia results found.', 'warn');
    return { text: '', source: 'Wikipedia', title: keyword };
}

// ============================================================
// AI Generation Pipeline
// ============================================================
async function runPipeline(mode, params) {
    if (AppState.isGenerating) return;
    AppState.isGenerating = true;

    const steps = ['fetch', 'preprocess', 'prompt', 'infer'];
    const progress = document.getElementById('pipeline-progress');

    // Reset pipeline UI
    steps.forEach(s => {
        document.getElementById(`step-${s}`).className = 'pipeline-step';
        document.getElementById(`step-${s}-status`).textContent = '—';
    });
    progress.style.width = '0%';

    try {
        let fetchedData = '';
        let instruction = '';

        // ---- Step 1: Fetch Data ----
        setStepActive('fetch');
        progress.style.width = '15%';

        if (mode === 'url') {
            const url = params.url;
            if (!url) throw new Error('Please enter a URL.');

            // Check cache
            const cacheKey = `jina-cache-${url}`;
            const cached = localStorage.getItem(cacheKey);
            if (cached) {
                const parsed = JSON.parse(cached);
                if (Date.now() - parsed.ts < 3600000) {
                    fetchedData = parsed.text;
                    log('Loaded from cache.', 'success');
                } else {
                    fetchedData = await fetchViaJina(url);
                }
            } else {
                fetchedData = await fetchViaJina(url);
            }
            instruction = params.instruction || '';
        } else if (mode === 'search') {
            const keyword = params.keyword;
            if (!keyword) throw new Error('Please enter search keywords.');
            const result = await searchWikipedia(keyword);
            fetchedData = result.text ? `## ${result.title}\nSource: ${result.source}\n\n${result.text}` : '';
            instruction = params.instruction || '';
        } else if (mode === 'prompt') {
            instruction = params.prompt;
            if (!instruction) throw new Error('Please enter an instruction.');
        }

        setStepDone('fetch');
        progress.style.width = '30%';

        // ---- Step 2: Preprocess ----
        setStepActive('preprocess');
        await sleep(300);

        if (fetchedData) {
            fetchedData = fetchedData.replace(/\n{3,}/g, '\n\n').trim();
        }

        let existingContext = '';
        if (mode === 'prompt' && params.useContext) {
            const currentDoc = getEditorContent();
            if (currentDoc.trim()) {
                existingContext = currentDoc.length > 1500
                    ? currentDoc.substring(currentDoc.length - 1500)
                    : currentDoc;
            }
        }

        setStepDone('preprocess');
        progress.style.width = '50%';

        // ---- Step 3: Build Prompt ----
        setStepActive('prompt');
        await sleep(200);

        let fullPrompt = '';
        if (mode === 'url') {
            fullPrompt = `Summarize and organize the following web content into well-structured Markdown. ${instruction ? 'Additional instructions: ' + instruction : ''}\n\nContent:\n${fetchedData}`;
        } else if (mode === 'search') {
            fullPrompt = `Based on the following information, write a comprehensive Markdown article. ${instruction ? 'Additional instructions: ' + instruction : ''}\n\nInformation:\n${fetchedData}`;
        } else if (mode === 'prompt') {
            fullPrompt = instruction;
            if (existingContext) {
                fullPrompt = `Context from current document:\n${existingContext}\n\nInstruction: ${instruction}`;
            }
        }

        log(`Prompt built: ${fullPrompt.length} chars.`);
        setStepDone('prompt');
        progress.style.width = '70%';

        // ---- Step 4: Inference ----
        setStepActive('infer');

        let generatedText = '';

        if (AppState.aiPipeline) {
            // Real ONNX inference
            log('Running local ONNX inference...');
            const startTime = performance.now();

            const result = await AppState.aiPipeline(fullPrompt, {
                max_new_tokens: 256,
                temperature: 0.7,
                repetition_penalty: 1.3,
                do_sample: true,
            });

            generatedText = result[0].generated_text;
            const elapsed = ((performance.now() - startTime) / 1000).toFixed(1);
            const tokens = generatedText.split(/\s+/).length;
            const speed = (tokens / parseFloat(elapsed)).toFixed(1);

            document.getElementById('inference-speed').textContent = `${speed} tok/s`;
            log(`Inference complete: ${tokens} tokens in ${elapsed}s (${speed} tok/s)`, 'success');
        } else {
            // No model: directly use fetched data
            log('No AI model loaded — using fetched data directly.', 'warn');

            if (fetchedData) {
                generatedText = fetchedData;
            } else if (instruction) {
                generatedText = `> ⚠️ **AI Model Not Loaded**\n>\n> Load a model from the header to enable AI generation.\n> Your instruction was: "${instruction}"`;
            }
        }

        setStepDone('infer');
        progress.style.width = '100%';

        // ---- Insert Result ----
        if (generatedText) {
            AppState.lastGeneratedContent = generatedText;
            await streamToEditor(generatedText);
            log('Content inserted into editor.', 'success');
        }

        setTimeout(() => { progress.style.width = '0%'; }, 2000);

    } catch (error) {
        log(`Pipeline error: ${error.message}`, 'error');
        alert(`Error: ${error.message}`);
    } finally {
        AppState.isGenerating = false;
        enableActionButtons();
    }
}

function setStepActive(stepId) {
    document.getElementById(`step-${stepId}`).className = 'pipeline-step active';
    document.getElementById(`step-${stepId}-status`).textContent = '⏳';
}

function setStepDone(stepId) {
    document.getElementById(`step-${stepId}`).className = 'pipeline-step done';
    document.getElementById(`step-${stepId}-status`).textContent = '✓';
}

function disableActionButtons() {
    document.querySelectorAll('.action-btn.primary').forEach(btn => btn.disabled = true);
}

function enableActionButtons() {
    document.querySelectorAll('.action-btn.primary').forEach(btn => btn.disabled = false);
}

// ============================================================
// UI Event Handlers
// ============================================================

function initModeTabs() {
    document.querySelectorAll('.mode-tab').forEach(tab => {
        tab.addEventListener('click', () => {
            const mode = tab.dataset.mode;
            document.querySelectorAll('.mode-tab').forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            document.querySelectorAll('.mode-panel').forEach(p => p.classList.remove('active'));
            document.getElementById(`mode-${mode}`).classList.add('active');
        });
    });
}

function initViewToggle() {
    document.querySelectorAll('.view-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const view = btn.dataset.view;
            AppState.currentView = view;
            document.querySelectorAll('.view-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const split = document.getElementById('editor-split');
            split.removeAttribute('data-view');
            if (view !== 'split') split.setAttribute('data-view', view);
        });
    });
}

function initToolbar() {
    document.querySelectorAll('.toolbar-btn[data-action]').forEach(btn => {
        btn.addEventListener('click', () => insertMarkdown(btn.dataset.action));
    });
}

function initPanel() {
    document.getElementById('collapse-panel-btn').addEventListener('click', () => {
        document.getElementById('ai-panel').classList.add('collapsed');
        document.getElementById('expand-panel-btn').classList.remove('hidden');
        AppState.panelCollapsed = true;
    });

    document.getElementById('expand-panel-btn').addEventListener('click', () => {
        document.getElementById('ai-panel').classList.remove('collapsed');
        document.getElementById('expand-panel-btn').classList.add('hidden');
        AppState.panelCollapsed = false;
    });
}

function initSplitHandle() {
    const handle = document.getElementById('split-handle');
    const editorPane = document.getElementById('editor-pane');
    const previewPane = document.getElementById('preview-pane');
    const split = document.getElementById('editor-split');
    let isDragging = false;

    handle.addEventListener('mousedown', (e) => {
        isDragging = true;
        document.body.style.cursor = 'col-resize';
        document.body.style.userSelect = 'none';
        e.preventDefault();
    });

    document.addEventListener('mousemove', (e) => {
        if (!isDragging) return;
        const rect = split.getBoundingClientRect();
        const ratio = (e.clientX - rect.left) / rect.width;
        const clamped = Math.max(0.2, Math.min(0.8, ratio));
        editorPane.style.flex = `0 0 ${clamped * 100}%`;
        previewPane.style.flex = `0 0 ${(1 - clamped) * 100 - 0.5}%`;
    });

    document.addEventListener('mouseup', () => {
        if (isDragging) {
            isDragging = false;
            document.body.style.cursor = '';
            document.body.style.userSelect = '';
        }
    });
}

function initActionButtons() {
    document.getElementById('url-go-btn').addEventListener('click', () => {
        disableActionButtons();
        runPipeline('url', {
            url: document.getElementById('url-input').value.trim(),
            instruction: document.getElementById('url-instruction').value.trim(),
        });
    });

    document.getElementById('search-go-btn').addEventListener('click', () => {
        disableActionButtons();
        runPipeline('search', {
            keyword: document.getElementById('search-input').value.trim(),
            instruction: document.getElementById('search-instruction').value.trim(),
        });
    });

    document.getElementById('prompt-go-btn').addEventListener('click', () => {
        disableActionButtons();
        runPipeline('prompt', {
            prompt: document.getElementById('prompt-input').value.trim(),
            useContext: document.getElementById('use-context').checked,
        });
    });
}

function initModelModal() {
    const modal = document.getElementById('model-modal');

    document.getElementById('model-status-btn').addEventListener('click', () => openModal('model-modal'));
    document.getElementById('model-modal-close').addEventListener('click', () => closeModal('model-modal'));
    document.getElementById('model-cancel-btn').addEventListener('click', () => closeModal('model-modal'));

    document.getElementById('model-load-btn').addEventListener('click', () => {
        const selected = document.querySelector('input[name="model-choice"]:checked');
        if (selected) loadModel(selected.value);
    });

    document.querySelectorAll('.model-option').forEach(option => {
        option.addEventListener('click', () => {
            document.querySelectorAll('.model-option').forEach(o => o.classList.remove('active'));
            option.classList.add('active');
            option.querySelector('input[type="radio"]').checked = true;
        });
    });

    modal.addEventListener('click', (e) => {
        if (e.target === modal) closeModal('model-modal');
    });
}

function openModal(id) {
    document.getElementById(id).classList.add('open');
}

function closeModal(id) {
    document.getElementById(id).classList.remove('open');
}

function initHeaderButtons() {
    document.getElementById('save-btn').addEventListener('click', saveDraft);
    document.getElementById('export-btn').addEventListener('click', exportMarkdown);

    document.getElementById('lang-btn').addEventListener('click', () => {
        const idx = localeOrder.indexOf(AppState.locale);
        AppState.locale = localeOrder[(idx + 1) % localeOrder.length];
        applyI18n();
        log(`Language: ${AppState.locale}`, 'info');
    });
}

function initLogButtons() {
    document.getElementById('clear-log-btn').addEventListener('click', () => {
        document.getElementById('log-window').innerHTML = '';
        log('Logs cleared.');
    });
}

// ============================================================
// Utilities
// ============================================================
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// ============================================================
// App Boot
// ============================================================
async function boot() {
    const loaderBar = document.getElementById('loader-bar');

    try {
        // Phase 1
        loaderBar.style.width = '25%';
        initMarked();
        await sleep(150);

        // Phase 2: UI
        loaderBar.style.width = '50%';
        initModeTabs();
        initViewToggle();
        initToolbar();
        initPanel();
        initSplitHandle();
        initActionButtons();
        initModelModal();
        initHeaderButtons();
        initLogButtons();
        applyI18n();
        await sleep(150);

        // Phase 3: Editor
        loaderBar.style.width = '80%';
        initEditor();
        await sleep(200);

        // Phase 4: Load draft
        loaderBar.style.width = '95%';
        const hasDraft = localStorage.getItem('aimd-draft');
        if (hasDraft) loadDraft();
        await sleep(150);

        // Done
        loaderBar.style.width = '100%';
        await sleep(300);

        // Reveal
        document.getElementById('app-loader').classList.add('fade-out');
        document.getElementById('app').classList.remove('hidden');
        log('AIMD Studio ready.', 'success');

        setTimeout(() => {
            document.getElementById('app-loader').style.display = 'none';
        }, 600);

    } catch (err) {
        console.error('Boot failed:', err);
        loaderBar.style.width = '100%';
        document.getElementById('app-loader').classList.add('fade-out');
        document.getElementById('app').classList.remove('hidden');
    }
}

// ============================================================
// Start
// ============================================================
document.addEventListener('DOMContentLoaded', boot);
