const fs = require('fs');
const path = require('path');

const mobileDir = path.join(__dirname, '..', 'mobile');
const files = fs.readdirSync(mobileDir).filter(f => f.endsWith('.html'));

const skipFiles = ['260327_M_Ateam_v2.html', '260327_M_gtc2026.html'];

const newMobileStyles = `    <!-- Auto-injected Mobile Overrides -->
    <style>
        body { 
            background-color: #f8fafc !important; 
            margin: 0 !important; 
            padding: 0 !important; 
            display: flex !important; 
            flex-direction: column !important; 
            align-items: center !important; 
        }
        .a4-page, .page-container, .document-wrapper, #document-wrapper, #content-root, .a4-landscape, .slide-page {
            width: 100% !important;
            max-width: 100% !important;
            height: auto !important;
            min-height: 100dvh !important;
            max-height: none !important;
            margin: 0 !important;
            box-shadow: none !important;
            border-radius: 0 !important;
            padding: 24px 16px !important; /* Fix oversized padding for ALL layouts */
        }
        
        /* Typography overrides for small screens */
        .text-6xl { font-size: 2.5rem !important; line-height: 1.1 !important; }
        .text-5xl { font-size: 2rem !important; line-height: 1.2 !important; }
        .text-4xl { font-size: 1.5rem !important; line-height: 1.3 !important; }
        .text-3xl { font-size: 1.25rem !important; line-height: 1.4 !important; }
        
        /* Container Spacing optimizations */
        .p-8, .p-10 { padding: 20px !important; }
        .p-6, .px-8 { padding: 16px !important; }
        .gap-6, .gap-8, .gap-10, .gap-12 { gap: 16px !important; }
        
        /* Table responsive fixes */
        table {
            display: block !important;
            width: 100% !important;
            overflow-x: auto !important;
            white-space: nowrap !important;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            -webkit-overflow-scrolling: touch;
        }
        td, th {
            padding: 12px 16px !important;
            white-space: normal !important;
            min-width: 140px !important;
        }
        th { background: #f1f5f9 !important; color: #334155 !important; }

        /* Make sure texts wrap gracefully */
        * { word-wrap: break-word; }
        .text-justify { text-align: left !important; } 
        p { 
            font-size: 16px !important; 
            line-height: 1.65 !important; 
        }
    </style>
</head>`;

files.forEach(file => {
    if (skipFiles.includes(file)) {
        console.log("Skipping " + file);
        return;
    }

    const filePath = path.join(mobileDir, file);
    let content = fs.readFileSync(filePath, 'utf8');

    // Remove editing UI and scripts
    content = content.replace(/<div[^>]*id="control-panel"[^>]*>[\s\S]*?<\/div>\s*/gi, '');
    content = content.replace(/<script>[\s\S]*?(?:let isEditing|toggleEdit)[\s\S]*?<\/script>/gi, '');
    content = content.replace(/<!--\s*(?:互動|多功能)?控制面板(?:[\s\S]*?)-->/gi, '');

    // Cleanup residual style
    content = content.replace(/<!-- Auto-injected Mobile Overrides -->[\s\S]*?<\/head>/m, newMobileStyles);

    // If for some reason the old block was not found, try to inject at </head>
    if (!content.includes('Auto-injected Mobile Overrides')) {
        content = content.replace(/<\/head>/i, '\\n' + newMobileStyles);
    }

    fs.writeFileSync(filePath, content);
    console.log("Completely optimized layout & cleaned scripts for " + file);
});

console.log('Mobile layout optimization V2 pass completed.');
