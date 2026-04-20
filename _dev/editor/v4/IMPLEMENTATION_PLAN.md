# V4 iTaiwan Editor — Implementation Plan

## Overview
V4 is the first implementation that truly aligns with the ITW design docs (ITW_01/02/03).
It's a **scenario-driven Web App engine** — one `.itw` file = one dedicated application.

## Architecture
- **Single HTML file** (index.html) with embedded CSS + modular JS
- **Core Parser**: Regex-based .itw block parser (---TYPE--- barrier lines)
- **Block Editor Engine**: Contenteditable blocks with live MD preview
- **Scenario UI Matrix**: Template-based dynamic UI generation per app type

---

## Stage 1: Core Parser & File Format
**Goal**: Implement .itw parser/serializer that handles all block types
**Success Criteria**: Can parse sample .itw → AST → render blocks → serialize back
**Tests**: Round-trip parse/serialize of example .itw content
**Status**: ✅ Complete

## Stage 2: Block Editor Engine & App Shell
**Goal**: Build the editor UI shell, block-based editing, source toggle
**Success Criteria**: Working editor with block creation, drag-reorder, MD/CSV/JSON editing
**Tests**: Create/edit/delete blocks, switch between source and rendered view
**Status**: ✅ Complete

## Stage 3: Scenario Templates & Dynamic UI
**Goal**: Template dialog + scenario-specific UI generation (Pitch Deck, DataGrid, Document, Visual)
**Success Criteria**: Selecting a template correctly configures the editor toolbar and layout
**Tests**: Each template type renders its specific workspace
**Status**: ✅ Complete

## Stage 4: File I/O & Persistence
**Goal**: File System Access API, IndexedDB drafts, .itw export/import
**Success Criteria**: Open/save .itw files, auto-draft recovery
**Tests**: Save → close → reopen workflow
**Status**: ✅ Complete

## Stage 5: Polish & AI Integration Stub
**Goal**: Loading animation, transitions, AI panel placeholder, PWA manifest
**Success Criteria**: Professional-grade UX with smooth animations
**Tests**: Visual inspection, performance check
**Status**: 🔄 In Progress
