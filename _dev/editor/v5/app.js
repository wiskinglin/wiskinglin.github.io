// iTW Editor V5 - Premium App Engine
document.addEventListener('DOMContentLoaded', () => {
    // State Management
    const appState = {
        mode: 'text', // text, slide, table, image
        ast: [], // The internal representation of .itw file
    };

    // DOM Elements
    const themeToggle = document.getElementById('theme-toggle');
    const navItems = document.querySelectorAll('.nav-item');
    const canvasDoc = document.getElementById('canvas-document');
    const docTitle = document.getElementById('doc-title');
    const saveStatus = document.getElementById('save-status');
    const aiPanel = document.getElementById('ai-panel');
    const closeAiBtn = document.getElementById('close-ai');
    const settingsBtn = document.querySelector('.nav-group.bottom .nav-item');

    // --- 1. Theme Toggle ---
    themeToggle.addEventListener('click', () => {
        document.body.classList.toggle('light-theme');
        const isLight = document.body.classList.contains('light-theme');
        themeToggle.innerHTML = isLight ? '<i class="fa-solid fa-sun"></i>' : '<i class="fa-solid fa-moon"></i>';
    });

    // --- 2. Navigation & Mode Switching ---
    navItems.forEach(item => {
        item.addEventListener('click', () => {
            if (item === settingsBtn) return; // Settings/AI toggle handled separately
            
            navItems.forEach(nav => nav.classList.remove('active'));
            item.classList.add('active');
            
            const mode = item.getAttribute('data-tool');
            switchMode(mode);
        });
    });

    function switchMode(mode) {
        appState.mode = mode;
        canvasDoc.className = 'canvas-document'; // reset
        canvasDoc.classList.add(`mode-${mode}`);
        
        // Scenario-specific setups
        if (mode === 'slide') {
            const blocks = canvasDoc.querySelectorAll('.itw-block');
            blocks.forEach(b => b.classList.add('slide-item'));
        } else if (mode === 'table') {
            createDataGrid();
        } else if (mode === 'image') {
            createVisualCanvas();
        } else {
            const slides = canvasDoc.querySelectorAll('.slide-item');
            slides.forEach(s => s.classList.remove('slide-item'));
        }
    }

    // --- 3. Block Manager & Slash Commands ---
    let slashMenu = null;
    function createSlashMenu() {
        if(slashMenu) return;
        slashMenu = document.createElement('div');
        slashMenu.className = 'slash-menu glass-panel hidden';
        slashMenu.innerHTML = `
            <div class="slash-item" data-type="h1"><i class="fa-solid fa-heading"></i> Heading 1</div>
            <div class="slash-item" data-type="h2"><i class="fa-solid fa-heading" style="font-size:0.8em"></i> Heading 2</div>
            <div class="slash-item" data-type="p"><i class="fa-solid fa-paragraph"></i> Paragraph</div>
            <div class="slash-item" data-type="quote"><i class="fa-solid fa-quote-left"></i> Quote</div>
            <div class="slash-item" data-type="slide-break"><i class="fa-solid fa-arrows-split-up-and-left"></i> New Slide (---SLIDE---)</div>
            <div class="slash-item" data-type="divider"><i class="fa-solid fa-minus"></i> Divider</div>
        `;
        document.body.appendChild(slashMenu);

        slashMenu.addEventListener('mousedown', (e) => {
            e.preventDefault();
            const item = e.target.closest('.slash-item');
            if(item) {
                insertBlock(item.dataset.type);
                hideSlashMenu();
            }
        });
    }
    createSlashMenu();

    function showSlashMenu(rect) {
        slashMenu.style.top = `${rect.bottom + window.scrollY + 10}px`;
        slashMenu.style.left = `${rect.left + window.scrollX}px`;
        slashMenu.classList.remove('hidden');
    }

    function hideSlashMenu() {
        if(slashMenu) slashMenu.classList.add('hidden');
    }

    let currentBlock = null;

    canvasDoc.addEventListener('input', (e) => {
        if (appState.mode !== 'text' && appState.mode !== 'slide') return;
        triggerSave();
        const selection = window.getSelection();
        if(!selection.rangeCount) return;
        const range = selection.getRangeAt(0);
        
        currentBlock = e.target.closest('.itw-block');
        if(!currentBlock) return;
        
        const text = currentBlock.innerText;
        if(text.endsWith('/')) {
            const rect = range.getBoundingClientRect();
            showSlashMenu(rect);
        } else {
            hideSlashMenu();
        }
    });

    canvasDoc.addEventListener('keydown', (e) => {
        if (appState.mode !== 'text' && appState.mode !== 'slide') return;
        
        if(e.key === 'Escape') hideSlashMenu();
        if(e.key === 'Enter' && !e.shiftKey) {
            if(!slashMenu.classList.contains('hidden')) {
                e.preventDefault();
            } else {
                e.preventDefault();
                const newBlock = document.createElement('div');
                newBlock.className = 'itw-block text-block';
                newBlock.contentEditable = true;
                newBlock.dataset.type = 'MD';
                newBlock.dataset.placeholder = "Type '/' for commands...";
                
                const current = e.target.closest('.itw-block');
                if(current) {
                    current.parentNode.insertBefore(newBlock, current.nextSibling);
                } else {
                    canvasDoc.appendChild(newBlock);
                }
                newBlock.focus();
            }
        }
        
        if(e.key === 'Backspace') {
            const el = e.target.closest('.itw-block');
            if(el && (el.innerText.trim() === '' || el.innerHTML === '<br>')) {
                e.preventDefault();
                const prev = el.previousElementSibling;
                if(prev && el !== canvasDoc.firstElementChild) {
                    el.remove();
                    prev.focus();
                    const range = document.createRange();
                    const sel = window.getSelection();
                    range.selectNodeContents(prev);
                    range.collapse(false);
                    sel.removeAllRanges();
                    sel.addRange(range);
                }
            }
        }
    });

    function insertBlock(type) {
        if(!currentBlock) return;
        currentBlock.innerText = currentBlock.innerText.slice(0, -1); 
        
        const newBlock = document.createElement('div');
        newBlock.className = 'itw-block text-block';
        newBlock.contentEditable = true;
        newBlock.dataset.placeholder = "Type '/' for commands...";
        applyTypeToBlock(newBlock, type);
        
        if(currentBlock.innerText.trim() === '') {
            currentBlock.parentNode.replaceChild(newBlock, currentBlock);
        } else {
            currentBlock.parentNode.insertBefore(newBlock, currentBlock.nextSibling);
        }
        
        if(type !== 'divider' && type !== 'slide-break') {
            newBlock.focus();
            const range = document.createRange();
            const sel = window.getSelection();
            if(newBlock.firstChild) {
                range.selectNodeContents(newBlock.firstChild);
                range.collapse(true);
                sel.removeAllRanges();
                sel.addRange(range);
            }
        }
    }

    function applyTypeToBlock(block, type) {
        block.innerHTML = '';
        if(type === 'h1') {
            block.innerHTML = '<h1 class="block-title"></h1>';
        } else if(type === 'h2') {
            block.innerHTML = '<h2 class="block-h2"></h2>';
        } else if(type === 'quote') {
            block.innerHTML = '<blockquote class="block-quote"></blockquote>';
        } else if(type === 'slide-break') {
            block.innerHTML = '<hr class="block-divider" data-meta="---SLIDE---" style="border-top: 2px dashed var(--accent-3);">';
            block.contentEditable = false;
        } else if(type === 'divider') {
            block.innerHTML = '<hr class="block-divider">';
            block.contentEditable = false;
        } else {
            block.innerHTML = '<p class="block-text"></p>';
        }
    }

    // --- 4. Floating Format Toolbar ---
    const formatToolbar = document.getElementById('format-toolbar');
    canvasDoc.addEventListener('mouseup', () => {
        if(appState.mode !== 'text' && appState.mode !== 'slide') return;
        const selection = window.getSelection();
        if (selection.toString().length > 0) {
            const range = selection.getRangeAt(0);
            const rect = range.getBoundingClientRect();
            
            formatToolbar.style.top = `${rect.top - formatToolbar.offsetHeight - 10}px`;
            formatToolbar.style.left = `${rect.left + (rect.width / 2) - (formatToolbar.offsetWidth / 2)}px`;
            formatToolbar.classList.remove('hidden');
        } else {
            formatToolbar.classList.add('hidden');
        }
    });

    canvasDoc.addEventListener('keyup', (e) => {
        if(e.key !== 'Shift' && e.key.indexOf('Arrow') === -1) {
            formatToolbar.classList.add('hidden');
        }
    });

    const formatBtns = document.querySelectorAll('#format-toolbar button');
    formatBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const format = btn.getAttribute('data-format');
            if(format === 'h1' || format === 'h2') {
                document.execCommand('formatBlock', false, format.toUpperCase());
            } else {
                document.execCommand(format, false, null);
            }
        });
    });

    // --- 5. DataGrid / Excel Mode (CSV via PapaParse) ---
    // A robust CSV grid implementation
    function createDataGrid() {
        if(canvasDoc.querySelector('.datagrid-container')) return;
        
        // Hide standard blocks
        const existingBlocks = canvasDoc.querySelectorAll('.itw-block');
        existingBlocks.forEach(b => b.style.display = 'none');
        
        const gridContainer = document.createElement('div');
        gridContainer.className = 'datagrid-container';
        
        const header = document.createElement('div');
        header.className = 'datagrid-header';
        header.innerHTML = `<h3><i class="fa-solid fa-table"></i> Data Engine (---CSV---)</h3>`;
        gridContainer.appendChild(header);

        // Demo Data
        const csvData = `Quarter,Revenue,Cost,Profit
Q1,5000,2000,3000
Q2,6000,2200,3800
Q3,5500,2100,3400
Q4,8000,3000,5000`;

        const parsed = Papa.parse(csvData).data;
        const table = document.createElement('table');
        table.className = 'itw-datagrid';
        
        parsed.forEach((row, rIndex) => {
            const tr = document.createElement('tr');
            row.forEach((cell, cIndex) => {
                const td = document.createElement('td');
                td.contentEditable = true;
                td.innerText = cell;
                if(rIndex === 0) td.classList.add('grid-th');
                
                td.addEventListener('input', triggerSave);
                tr.appendChild(td);
            });
            table.appendChild(tr);
        });
        
        gridContainer.appendChild(table);
        canvasDoc.appendChild(gridContainer);
    }

    // --- 6. Visual Mode (Image Base64 Dropzone) ---
    function createVisualCanvas() {
        if(canvasDoc.querySelector('.visual-canvas-container')) return;
        
        const existingBlocks = canvasDoc.querySelectorAll('.itw-block');
        existingBlocks.forEach(b => b.style.display = 'none');
        if(canvasDoc.querySelector('.datagrid-container')) {
            canvasDoc.querySelector('.datagrid-container').style.display = 'none';
        }
        
        const visualContainer = document.createElement('div');
        visualContainer.className = 'visual-canvas-container';
        
        const title = document.createElement('h2');
        title.className = 'visual-title';
        title.innerHTML = '<i class="fa-solid fa-image"></i> Visual Asset (---IMG---)';
        
        const imgPlaceholder = document.createElement('div');
        imgPlaceholder.className = 'visual-dropzone';
        imgPlaceholder.id = 'img-dropzone';
        imgPlaceholder.innerHTML = '<i class="fa-solid fa-cloud-arrow-up"></i> Drop image to embed as Base64';
        
        const controls = document.createElement('div');
        controls.className = 'visual-controls';
        controls.innerHTML = `
            <button class="btn-primary" id="ai-enhance-btn"><i class="fa-solid fa-wand-magic-sparkles"></i> AI Enhance</button>
            <button class="btn-icon" style="border: 1px solid var(--border-color)"><i class="fa-solid fa-crop"></i></button>
        `;
        
        visualContainer.appendChild(title);
        visualContainer.appendChild(imgPlaceholder);
        visualContainer.appendChild(controls);
        canvasDoc.appendChild(visualContainer);

        // Drag and Drop Logic
        imgPlaceholder.addEventListener('dragover', (e) => {
            e.preventDefault();
            imgPlaceholder.style.borderColor = 'var(--accent-1)';
        });
        imgPlaceholder.addEventListener('dragleave', () => {
            imgPlaceholder.style.borderColor = 'var(--text-muted)';
        });
        imgPlaceholder.addEventListener('drop', (e) => {
            e.preventDefault();
            imgPlaceholder.style.borderColor = 'var(--text-muted)';
            const file = e.dataTransfer.files[0];
            if (file && file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = (event) => {
                    imgPlaceholder.innerHTML = `<img src="${event.target.result}" style="max-width:100%; max-height:100%; border-radius:var(--radius-sm);">`;
                    triggerSave();
                };
                reader.readAsDataURL(file);
            }
        });
    }

    // --- 7. AI Engine Integration (ITW_03) ---
    settingsBtn.addEventListener('click', () => {
        aiPanel.classList.toggle('open');
    });

    closeAiBtn.addEventListener('click', () => {
        aiPanel.classList.remove('open');
    });

    const aiExtractBtn = document.getElementById('ai-extract-btn');
    const aiUrlInput = document.getElementById('ai-url-input');
    const aiResult = document.getElementById('ai-result');

    aiExtractBtn.addEventListener('click', async () => {
        const url = aiUrlInput.value.trim();
        if(!url) return;
        
        aiResult.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Extracting knowledge via Jina...';
        try {
            // Browser-Native AI extraction (CORS bypass via r.jina.ai)
            const response = await fetch(`https://r.jina.ai/${url}`);
            const text = await response.text();
            
            // Show preview
            aiResult.innerHTML = `<div style="max-height: 200px; overflow-y: auto; font-family: var(--font-mono); font-size: 11px; white-space: pre-wrap;">${text.substring(0, 500)}...</div>`;
            
            // Automatically patch into the editor context (MD Patcher)
            const newBlock = document.createElement('div');
            newBlock.className = 'itw-block text-block';
            newBlock.contentEditable = true;
            newBlock.innerHTML = `<blockquote><strong>AI Extracted:</strong><br>${text.substring(0, 200)}...</blockquote>`;
            canvasDoc.appendChild(newBlock);
            triggerSave();
            
        } catch (err) {
            aiResult.innerHTML = `<span style="color:var(--accent-2)"><i class="fa-solid fa-triangle-exclamation"></i> Extraction failed.</span>`;
        }
    });

    const aiGenBtn = document.getElementById('ai-gen-btn');
    const aiPromptInput = document.getElementById('ai-prompt-input');
    
    aiGenBtn.addEventListener('click', () => {
        const prompt = aiPromptInput.value;
        if(!prompt) return;
        
        // Simulating ONNX Local Reasoning Streaming
        aiResult.innerHTML = '';
        const responseText = "Based on your context, here is a localized, scenario-driven suggestion... [ONNX Streaming Demo]";
        let i = 0;
        
        const interval = setInterval(() => {
            if (i < responseText.length) {
                aiResult.innerHTML += responseText.charAt(i);
                i++;
            } else {
                clearInterval(interval);
            }
        }, 30);
    });

    // --- 8. Auto-Save Simulator ---
    let saveTimeout;
    const triggerSave = () => {
        saveStatus.innerHTML = '<i class="fa-solid fa-arrows-rotate fa-spin"></i> Saving';
        saveStatus.style.color = 'var(--accent-1)';
        
        clearTimeout(saveTimeout);
        saveTimeout = setTimeout(() => {
            saveStatus.innerHTML = '<i class="fa-solid fa-cloud-check"></i> Synced (AST Built)';
            saveStatus.style.color = 'var(--text-muted)';
        }, 1500);
    };

    docTitle.addEventListener('input', triggerSave);
});
