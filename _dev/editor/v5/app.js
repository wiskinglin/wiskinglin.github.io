// iTW Editor V5 - Premium App Engine
document.addEventListener('DOMContentLoaded', () => {
    // Theme Toggle
    const themeToggle = document.getElementById('theme-toggle');
    themeToggle.addEventListener('click', () => {
        document.body.classList.toggle('light-theme');
        const isLight = document.body.classList.contains('light-theme');
        themeToggle.innerHTML = isLight ? '<i class="fa-solid fa-sun"></i>' : '<i class="fa-solid fa-moon"></i>';
    });

    // Navigation Active State & Mode Switching
    const navItems = document.querySelectorAll('.nav-item');
    const canvasDoc = document.getElementById('canvas-document');
    let currentMode = 'text';

    navItems.forEach(item => {
        item.addEventListener('click', () => {
            navItems.forEach(nav => nav.classList.remove('active'));
            item.classList.add('active');
            
            const mode = item.getAttribute('data-tool');
            switchMode(mode);
        });
    });

    function switchMode(mode) {
        currentMode = mode;
        canvasDoc.className = 'canvas-document'; // reset
        canvasDoc.classList.add(`mode-${mode}`);
        
        // Specific logic for modes
        if (mode === 'slide') {
            // Apply slide formatting if not already present
            const blocks = canvasDoc.querySelectorAll('.itw-block');
            blocks.forEach(b => b.classList.add('slide-item'));
        } else if (mode === 'table') {
            // DataGrid mode logic
            createDataGrid();
        } else if (mode === 'image') {
            // Visual mode logic
            createVisualCanvas();
        } else {
            // Text mode
            const slides = canvasDoc.querySelectorAll('.slide-item');
            slides.forEach(s => s.classList.remove('slide-item'));
        }
    }

    // --- Block Manager & Slash Commands ---
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
        if (currentMode !== 'text') return;
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
        if (currentMode !== 'text') return;
        
        if(e.key === 'Escape') hideSlashMenu();
        if(e.key === 'Enter' && !e.shiftKey) {
            if(!slashMenu.classList.contains('hidden')) {
                // simple logic: prevent default to not add new line if menu open
                e.preventDefault();
            } else {
                e.preventDefault();
                // Create new paragraph block
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
            const el = e.target;
            if(el.innerText.trim() === '' || el.innerHTML === '<br>') {
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
        currentBlock.innerText = currentBlock.innerText.slice(0, -1); // remove '/'
        
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
        
        // Focus new block
        if(type !== 'divider') {
            newBlock.focus();
            const range = document.createRange();
            const sel = window.getSelection();
            // Try to place cursor inside the specific element created
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
        } else if(type === 'divider') {
            block.innerHTML = '<hr class="block-divider">';
            block.contentEditable = false;
        } else {
            block.innerHTML = '<p class="block-text"></p>';
        }
    }

    // --- DataGrid / Excel Mode (Cycle 4) ---
    function createDataGrid() {
        if(canvasDoc.querySelector('.datagrid-container')) return;
        
        // Keep existing blocks but hide them, or just clear for demo
        canvasDoc.innerHTML = ''; 
        
        const gridContainer = document.createElement('div');
        gridContainer.className = 'datagrid-container';
        
        const header = document.createElement('div');
        header.className = 'datagrid-header';
        header.innerHTML = `<h3>Financial Projection 2026</h3>`;
        gridContainer.appendChild(header);

        const table = document.createElement('table');
        table.className = 'itw-datagrid';
        
        // Gen rows
        for(let r = 0; r < 6; r++) {
            const tr = document.createElement('tr');
            for(let c = 0; c < 4; c++) {
                const td = document.createElement('td');
                td.contentEditable = true;
                if(r === 0) {
                    td.classList.add('grid-th');
                    td.innerText = ['Quarter', 'Revenue', 'Cost', 'Profit'][c];
                } else {
                    if(c===0) td.innerText = \`Q\${r}\`;
                    else td.innerText = Math.floor(Math.random() * 5000);
                }
                tr.appendChild(td);
            }
            table.appendChild(tr);
        }
        
        gridContainer.appendChild(table);
        canvasDoc.appendChild(gridContainer);
    }

    // --- Visual Mode (Cycle 5) ---
    function createVisualCanvas() {
        if(canvasDoc.querySelector('.visual-canvas-container')) return;
        canvasDoc.innerHTML = '';
        
        const visualContainer = document.createElement('div');
        visualContainer.className = 'visual-canvas-container';
        
        const title = document.createElement('h2');
        title.className = 'visual-title';
        title.innerText = 'Social Media Asset';
        
        const imgPlaceholder = document.createElement('div');
        imgPlaceholder.className = 'visual-dropzone';
        imgPlaceholder.innerHTML = '<i class="fa-solid fa-cloud-arrow-up"></i> Drop image or generate with AI';
        
        const controls = document.createElement('div');
        controls.className = 'visual-controls';
        controls.innerHTML = `
            <button class="btn-primary"><i class="fa-solid fa-wand-magic-sparkles"></i> AI Enhance</button>
            <button class="btn-icon" style="border: 1px solid var(--border-color)"><i class="fa-solid fa-crop"></i></button>
        `;
        
        visualContainer.appendChild(title);
        visualContainer.appendChild(imgPlaceholder);
        visualContainer.appendChild(controls);
        canvasDoc.appendChild(visualContainer);
    }

    // --- Floating Format Toolbar Logic ---
    const formatToolbar = document.getElementById('format-toolbar');

    canvasDoc.addEventListener('mouseup', () => {
        if(currentMode !== 'text') return;
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
    
    // Auto-save simulation
    const docTitle = document.getElementById('doc-title');
    const saveStatus = document.getElementById('save-status');
    
    let saveTimeout;
    const triggerSave = () => {
        saveStatus.innerHTML = '<i class="fa-solid fa-arrows-rotate fa-spin"></i> Saving';
        saveStatus.style.color = 'var(--accent-1)';
        
        clearTimeout(saveTimeout);
        saveTimeout = setTimeout(() => {
            saveStatus.innerHTML = '<i class="fa-solid fa-cloud-check"></i> Synced';
            saveStatus.style.color = 'var(--text-muted)';
        }, 1000);
    };

    docTitle.addEventListener('input', triggerSave);
});
