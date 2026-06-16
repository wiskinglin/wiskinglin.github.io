// 3D Flip Clock Logic & Audio Synth

// --- 1. Audio Synthesis for Snapping Cards ---
class FlipAudioSynth {
    constructor() {
        this.ctx = null;
        this.enabled = true;
    }

    init() {
        if (this.ctx) return;
        try {
            this.ctx = new (window.AudioContext || window.webkitAudioContext)();
        } catch (e) {
            console.error("Web Audio API not supported", e);
        }
    }

    playFlip() {
        if (!this.enabled) return;
        this.init();
        if (!this.ctx) return;

        // Resume if suspended (browser security policy)
        if (this.ctx.state === 'suspended') {
            this.ctx.resume();
        }

        const now = this.ctx.currentTime;

        // Part 1: High-pitch card release snap (very short)
        const osc1 = this.ctx.createOscillator();
        const gain1 = this.ctx.createGain();
        osc1.type = 'triangle';
        osc1.frequency.setValueAtTime(800, now);
        osc1.frequency.exponentialRampToValueAtTime(150, now + 0.006);

        gain1.gain.setValueAtTime(0.08, now);
        gain1.gain.exponentialRampToValueAtTime(0.001, now + 0.006);

        osc1.connect(gain1);
        gain1.connect(this.ctx.destination);
        osc1.start(now);
        osc1.stop(now + 0.01);

        // Part 2: Low-pitch mechanical impact thud (card hitting base)
        // Delayed by ~5ms to simulate the card falling down
        const delay = 0.005;
        const osc2 = this.ctx.createOscillator();
        const gain2 = this.ctx.createGain();
        osc2.type = 'sine';
        osc2.frequency.setValueAtTime(140, now + delay);
        osc2.frequency.exponentialRampToValueAtTime(35, now + delay + 0.02);

        gain2.gain.setValueAtTime(0.18, now + delay);
        gain2.gain.exponentialRampToValueAtTime(0.001, now + delay + 0.02);

        osc2.connect(gain2);
        gain2.connect(this.ctx.destination);
        osc2.start(now + delay);
        osc2.stop(now + delay + 0.03);
    }

    playAlarm() {
        if (!this.enabled) return;
        this.init();
        if (!this.ctx) return;
        if (this.ctx.state === 'suspended') this.ctx.resume();

        const now = this.ctx.currentTime;

        // Play a premium retro chime alarm
        const notes = [523.25, 659.25, 783.99, 1046.50]; // C5, E5, G5, C6
        notes.forEach((freq, index) => {
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();
            osc.type = 'sine';
            osc.frequency.setValueAtTime(freq, now + index * 0.08);

            gain.gain.setValueAtTime(0.2, now + index * 0.08);
            gain.gain.exponentialRampToValueAtTime(0.001, now + index * 0.08 + 0.25);

            osc.connect(gain);
            gain.connect(this.ctx.destination);
            osc.start(now + index * 0.08);
            osc.stop(now + index * 0.08 + 0.3);
        });
    }
}

// Global instance of audio synthesizer
window.flipSynth = new FlipAudioSynth();

// Unlock Audio Context on first click anywhere
document.body.addEventListener('click', () => {
    window.flipSynth.init();
}, { once: true });


// --- 2. 3D Flip Card Component ---
class FlipCardDigit {
    constructor(id) {
        this.el = document.getElementById(id);
        if (!this.el) {
            console.error(`Flip digit container #${id} not found.`);
            return;
        }
        this.cardTop = this.el.querySelector('.card-half.card-top span');
        this.cardBottom = this.el.querySelector('.card-half.card-bottom span');
        this.cardFlip = this.el.querySelector('.card-flip');
        this.cardFlipTop = this.el.querySelector('.card-flip-top span');
        this.cardFlipBottom = this.el.querySelector('.card-flip-bottom span');

        this.currentVal = 0;
        this.isFlipping = false;
        this.timeoutId = null;

        // Initialize visuals
        this.cardTop.textContent = '0';
        this.cardBottom.textContent = '0';
        this.cardFlipTop.textContent = '0';
        this.cardFlipBottom.textContent = '0';
    }

    setVal(newVal, force = false) {
        newVal = parseInt(newVal);
        if (isNaN(newVal)) newVal = 0;

        if (this.currentVal === newVal && !force) return;

        // Fast-forward previous flip if triggered during active flip
        if (this.isFlipping) {
            this.finishFlip(newVal);
            return;
        }

        this.isFlipping = true;

        // Prepare faces
        this.cardTop.textContent = newVal;             // Next top background (hidden initially by flip top card)
        this.cardBottom.textContent = this.currentVal;  // Underneath bottom background (visible initially)
        this.cardFlipTop.textContent = this.currentVal; // Flip card front (visible, facing up)
        this.cardFlipBottom.textContent = newVal;       // Flip card back (hidden, rotated, will land down)

        // Play card drop click sound
        window.flipSynth.playFlip();

        // Trigger transition
        this.cardFlip.classList.add('flipping');

        const endTransition = () => {
            this.cardFlip.removeEventListener('animationend', endTransition);
            this.finishFlip(newVal);
        };

        this.cardFlip.addEventListener('animationend', endTransition);

        // Backup timeout in case tab is in background and transitionend doesn't fire
        if (this.timeoutId) clearTimeout(this.timeoutId);
        this.timeoutId = setTimeout(() => {
            this.cardFlip.removeEventListener('animationend', endTransition);
            this.finishFlip(newVal);
        }, 550);
    }

    finishFlip(val) {
        if (this.timeoutId) clearTimeout(this.timeoutId);

        this.cardFlip.classList.remove('flipping');
        this.cardBottom.textContent = val;
        this.cardFlipTop.textContent = val;
        this.currentVal = val;
        this.isFlipping = false;
    }
}


// --- 3. Dynamic Canvas Particles Background ---
class ParticleBackground {
    constructor() {
        this.canvas = document.getElementById('bg-particles');
        this.ctx = this.canvas.getContext('2d');
        this.particles = [];
        this.enabled = true;
        this.colors = ['#6366f1', '#4f46e5', '#818cf8']; // default indigo shades

        this.resize();
        window.addEventListener('resize', () => this.resize());
        this.initParticles();
        this.animate();
    }

    resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }

    setColors(primaryColorHex) {
        this.colors = [
            primaryColorHex,
            this.adjustColor(primaryColorHex, -20),
            this.adjustColor(primaryColorHex, 20)
        ];
    }

    adjustColor(hex, percent) {
        let num = parseInt(hex.replace("#", ""), 16),
            amt = Math.round(2.55 * percent),
            R = (num >> 16) + amt,
            G = (num >> 8 & 0x00FF) + amt,
            B = (num & 0x0000FF) + amt;
        return "#" + (0x1000000 + (R < 255 ? R < 0 ? 0 : R : 255) * 0x10000 + (G < 255 ? G < 0 ? 0 : G : 255) * 0x100 + (B < 255 ? B < 0 ? 0 : B : 255)).toString(16).slice(1);
    }

    initParticles() {
        this.particles = [];
        const count = Math.min(window.innerWidth / 25, 60);
        for (let i = 0; i < count; i++) {
            this.particles.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                vx: (Math.random() - 0.5) * 0.35,
                vy: (Math.random() - 0.5) * 0.35,
                size: Math.random() * 2.5 + 1.2,
                color: this.colors[Math.floor(Math.random() * this.colors.length)],
                alpha: Math.random() * 0.4 + 0.1
            });
        }
    }

    animate() {
        if (!this.enabled) {
            this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
            requestAnimationFrame(() => this.animate());
            return;
        }

        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        // Draw constellation lines (very faint)
        this.ctx.lineWidth = 0.5;
        for (let i = 0; i < this.particles.length; i++) {
            for (let j = i + 1; j < this.particles.length; j++) {
                const p1 = this.particles[i];
                const p2 = this.particles[j];
                const dx = p1.x - p2.x;
                const dy = p1.y - p2.y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                if (dist < 130) {
                    const alpha = (1 - dist / 130) * 0.04;
                    this.ctx.strokeStyle = `rgba(255, 255, 255, ${alpha})`;
                    this.ctx.beginPath();
                    this.ctx.moveTo(p1.x, p1.y);
                    this.ctx.lineTo(p2.x, p2.y);
                    this.ctx.stroke();
                }
            }
        }

        // Draw particles
        this.particles.forEach(p => {
            p.x += p.vx;
            p.y += p.vy;

            // boundary warp
            if (p.x < 0) p.x = this.canvas.width;
            if (p.x > this.canvas.width) p.x = 0;
            if (p.y < 0) p.y = this.canvas.height;
            if (p.y > this.canvas.height) p.y = 0;

            this.ctx.fillStyle = p.color;
            this.ctx.globalAlpha = p.alpha;
            this.ctx.beginPath();
            this.ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            this.ctx.fill();
        });

        this.ctx.globalAlpha = 1.0;
        requestAnimationFrame(() => this.animate());
    }
}


// --- 4. Main Application Engine ---
class FlipClockApp {
    constructor() {
        // Init Card Objects
        this.digits = {
            hTens: new FlipCardDigit('h-tens'),
            hOnes: new FlipCardDigit('h-ones'),
            mTens: new FlipCardDigit('m-tens'),
            mOnes: new FlipCardDigit('m-ones'),
            sTens: new FlipCardDigit('s-tens'),
            sOnes: new FlipCardDigit('s-ones'),
            msTens: new FlipCardDigit('ms-tens'),
            msOnes: new FlipCardDigit('ms-ones')
        };

        // App States
        this.currentMode = 'clock'; // 'clock', 'pomodoro', 'timer', 'stopwatch'
        this.timeFormat24 = true;
        this.activeTheme = 'dark';
        this.activeCardStyle = 'classic';
        this.activeFont = 'share-tech';

        // Engine Timer variables
        this.engineInterval = null;
        this.lastTimeStr = '';

        // Mode States: Stopwatch
        this.swRunning = false;
        this.swStartTime = 0;
        this.swElapsedTime = 0;
        this.swLaps = [];
        this.swLastLapTime = 0;

        // Mode States: Timer
        this.tmRunning = false;
        this.tmRemainingSeconds = 600; // 10 minutes default
        this.tmDuration = 600;

        // Mode States: Pomodoro
        this.pomoRunning = false;
        this.pomoMode = 'focus'; // 'focus' (25m), 'break' (5m)
        this.pomoRemainingSeconds = 1500; // 25m

        // Background Particles
        this.particlesBg = new ParticleBackground();

        // Bind DOM Events
        this.bindDOMEvents();

        // Start Engine
        this.startEngine();
    }

    bindDOMEvents() {
        // --- Navigation Tabs ---
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const mode = e.currentTarget.getAttribute('data-mode');
                this.switchMode(mode);
                // Highlight tab
                document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
                e.currentTarget.classList.add('active');
            });
        });

        // --- Settings Sidebar ---
        const sidebar = document.getElementById('settings-sidebar');
        const trigger = document.getElementById('settings-trigger');
        const closeBtn = document.getElementById('settings-close');
        const backdrop = document.getElementById('settings-backdrop');

        const openSidebar = () => {
            sidebar.classList.add('open');
            backdrop.classList.add('open');
        };

        const closeSidebar = () => {
            sidebar.classList.remove('open');
            backdrop.classList.remove('open');
        };

        trigger.addEventListener('click', openSidebar);
        closeBtn.addEventListener('click', closeSidebar);
        backdrop.addEventListener('click', closeSidebar);

        // --- Setting: Time Format ---
        document.getElementById('format-12h').addEventListener('click', (e) => {
            this.timeFormat24 = false;
            document.getElementById('format-12h').classList.add('active');
            document.getElementById('format-24h').classList.remove('active');
            this.updateDisplay(true); // force update
        });
        document.getElementById('format-24h').addEventListener('click', (e) => {
            this.timeFormat24 = true;
            document.getElementById('format-24h').classList.add('active');
            document.getElementById('format-12h').classList.remove('active');
            this.updateDisplay(true);
        });

        // --- Setting: Sound ---
        const soundToggle = document.getElementById('sound-toggle');
        soundToggle.addEventListener('change', () => {
            window.flipSynth.enabled = soundToggle.checked;
        });

        // --- Setting: Particle BG ---
        const particleToggle = document.getElementById('particle-toggle');
        particleToggle.addEventListener('change', () => {
            this.particlesBg.enabled = particleToggle.checked;
        });

        // --- Setting: Themes Selection ---
        document.querySelectorAll('#theme-grid .theme-card').forEach(card => {
            card.addEventListener('click', (e) => {
                document.querySelectorAll('#theme-grid .theme-card').forEach(c => c.classList.remove('active'));
                const themeBtn = e.currentTarget;
                themeBtn.classList.add('active');

                const themeName = themeBtn.getAttribute('data-theme');
                this.applyTheme(themeName);
            });
        });

        // --- Setting: Card Style ---
        document.querySelectorAll('#card-style-grid button').forEach(btn => {
            btn.addEventListener('click', (e) => {
                document.querySelectorAll('#card-style-grid button').forEach(b => b.classList.remove('active'));
                e.currentTarget.classList.add('active');

                const cardStyle = e.currentTarget.getAttribute('data-card');
                this.applyCardStyle(cardStyle);
            });
        });

        // --- Setting: Font Selection ---
        document.querySelectorAll('.font-choice-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                document.querySelectorAll('.font-choice-btn').forEach(b => b.classList.remove('active'));
                e.currentTarget.classList.add('active');

                const fontName = e.currentTarget.getAttribute('data-font');
                this.applyFont(fontName);
            });
        });

        // --- Setting: Fullscreen ---
        document.getElementById('fullscreen-btn').addEventListener('click', () => {
            if (!document.fullscreenElement) {
                document.documentElement.requestFullscreen().catch(err => {
                    console.error(`Error attempting to enable fullscreen: ${err.message}`);
                });
            } else {
                document.exitFullscreen();
            }
        });

        // --- Mode Action Controls ---
        const playPauseBtn = document.getElementById('btn-play-pause');
        const secondaryBtn = document.getElementById('btn-action-sec');
        const resetBtn = document.getElementById('btn-reset');

        playPauseBtn.addEventListener('click', () => {
            this.togglePlayPause();
        });

        secondaryBtn.addEventListener('click', () => {
            this.handleSecondaryAction();
        });

        resetBtn.addEventListener('click', () => {
            this.handleResetAction();
        });

        // --- Timer Quick Presets ---
        document.querySelectorAll('.preset-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const sec = parseInt(e.currentTarget.getAttribute('data-sec'));
                if (!isNaN(sec)) {
                    this.tmRemainingSeconds = sec;
                    this.tmDuration = sec;
                    this.tmRunning = false;
                    this.updatePlayPauseButtonUI(false);
                    this.updateDisplay(true);
                    this.showToast("⏳ 已設定倒數時間");
                }
            });
        });

        // --- Custom Timer Modal Dialog ---
        const modal = document.getElementById('timer-modal');
        const modalCancel = document.getElementById('timer-modal-cancel');
        const modalConfirm = document.getElementById('timer-modal-confirm');
        const customTrigger = document.getElementById('custom-timer-trigger');

        customTrigger.addEventListener('click', () => {
            modal.classList.add('open');
        });

        const closeModal = () => {
            modal.classList.remove('open');
        };

        modalCancel.addEventListener('click', closeModal);
        document.getElementById('timer-modal-backdrop').addEventListener('click', closeModal);

        modalConfirm.addEventListener('click', () => {
            const h = Math.max(0, parseInt(document.getElementById('input-h').value) || 0);
            const m = Math.max(0, Math.min(59, parseInt(document.getElementById('input-m').value) || 0));
            const s = Math.max(0, Math.min(59, parseInt(document.getElementById('input-s').value) || 0));

            const totalSec = h * 3600 + m * 60 + s;
            if (totalSec > 0) {
                this.tmRemainingSeconds = totalSec;
                this.tmDuration = totalSec;
                this.tmRunning = false;
                this.updatePlayPauseButtonUI(false);
                this.updateDisplay(true);
                this.showToast(`⏳ 設定計時器: ${h}小時 ${m}分 ${s}秒`);
            }
            closeModal();
        });
    }

    // Toast Alert Notification
    showToast(message, icon = '🛎️') {
        const toast = document.getElementById('toast-banner');
        document.getElementById('toast-icon').textContent = icon;
        document.getElementById('toast-message').textContent = message;

        toast.classList.add('visible');

        if (this.toastTimeout) clearTimeout(this.toastTimeout);
        this.toastTimeout = setTimeout(() => {
            toast.classList.remove('visible');
        }, 3000);
    }

    // Switch Application Modes
    switchMode(mode) {
        if (mode === this.currentMode) return;

        // Save states or clear animations
        this.currentMode = mode;
        this.updateModeUI();
        this.updateDisplay(true); // force redraw
    }

    updateModeUI() {
        const statusHeader = document.getElementById('mode-status');
        const statusLabel = document.getElementById('status-label');
        const dateDisplay = document.getElementById('clock-date');
        const actionControls = document.getElementById('action-controls');
        const timerPresets = document.getElementById('timer-presets');
        const lapRecords = document.getElementById('lap-records');
        const secColon = document.getElementById('sec-colon');
        const secondsGroup = document.getElementById('seconds-group');
        const msGroup = document.getElementById('ms-group');
        const actionSecBtn = document.getElementById('btn-action-sec');

        // Reset display transitions
        statusHeader.classList.remove('hidden');
        actionControls.classList.remove('visible');
        actionControls.classList.add('pointer-events-none');

        // Mode specific elements toggles
        switch (this.currentMode) {
            case 'clock':
                statusHeader.classList.add('hidden');
                dateDisplay.classList.remove('hidden');
                actionControls.classList.add('hidden');
                timerPresets.classList.add('hidden');
                lapRecords.classList.add('hidden');
                secColon.classList.remove('hidden');
                secondsGroup.classList.remove('hidden');
                msGroup.classList.add('hidden');
                break;

            case 'pomodoro':
                statusLabel.textContent = this.pomoMode === 'focus' ? '🍅 POMODORO FOCUS' : '☕ BREAK TIME';
                dateDisplay.classList.add('hidden');
                actionControls.classList.remove('hidden');
                actionControls.classList.remove('pointer-events-none');
                actionControls.classList.add('visible');
                timerPresets.classList.add('hidden');
                lapRecords.classList.add('hidden');
                secColon.classList.remove('hidden');
                secondsGroup.classList.remove('hidden');
                msGroup.classList.add('hidden');

                actionSecBtn.classList.add('hidden'); // No secondary button for pomodoro
                this.updatePlayPauseButtonUI(this.pomoRunning);
                break;

            case 'timer':
                statusLabel.textContent = '⏳ COUNTDOWN TIMER';
                dateDisplay.classList.add('hidden');
                actionControls.classList.remove('hidden');
                actionControls.classList.remove('pointer-events-none');
                actionControls.classList.add('visible');
                timerPresets.classList.remove('hidden');
                lapRecords.classList.add('hidden');
                secColon.classList.remove('hidden');
                secondsGroup.classList.remove('hidden');
                msGroup.classList.add('hidden');

                actionSecBtn.classList.remove('hidden');
                document.getElementById('action-sec-text').textContent = '+1分鐘';
                this.updatePlayPauseButtonUI(this.tmRunning);
                break;

            case 'stopwatch':
                statusLabel.textContent = '⏱️ STOPWATCH';
                dateDisplay.classList.add('hidden');
                actionControls.classList.remove('hidden');
                actionControls.classList.remove('pointer-events-none');
                actionControls.classList.add('visible');
                timerPresets.classList.add('hidden');
                lapRecords.classList.remove('hidden');
                secColon.classList.remove('hidden');
                secondsGroup.classList.remove('hidden');
                msGroup.classList.remove('hidden');

                actionSecBtn.classList.remove('hidden');
                document.getElementById('action-sec-text').textContent = '分圈 (Lap)';
                this.updatePlayPauseButtonUI(this.swRunning);
                this.renderLaps();
                break;
        }
    }

    updatePlayPauseButtonUI(isRunning) {
        const playIcon = document.querySelector('.btn-icon-play');
        const pauseIcon = document.querySelector('.btn-icon-pause');
        const btnText = document.getElementById('play-pause-text');

        if (isRunning) {
            playIcon.classList.add('hidden');
            pauseIcon.classList.remove('hidden');
            btnText.textContent = '暫停';
        } else {
            playIcon.classList.remove('hidden');
            pauseIcon.classList.add('hidden');
            btnText.textContent = '開始';
        }
    }

    // --- Control Actions Handling ---
    togglePlayPause() {
        switch (this.currentMode) {
            case 'pomodoro':
                this.pomoRunning = !this.pomoRunning;
                this.updatePlayPauseButtonUI(this.pomoRunning);
                this.showToast(this.pomoRunning ? "🍅 番茄鐘已啟動" : "🍅 番茄鐘已暫停");
                break;
            case 'timer':
                this.tmRunning = !this.tmRunning;
                this.updatePlayPauseButtonUI(this.tmRunning);
                this.showToast(this.tmRunning ? "⏳ 計時器開始" : "⏳ 計時器暫停");
                break;
            case 'stopwatch':
                this.swRunning = !this.swRunning;
                if (this.swRunning) {
                    this.swStartTime = Date.now() - this.swElapsedTime;
                }
                this.updatePlayPauseButtonUI(this.swRunning);
                this.showToast(this.swRunning ? "⏱️ 碼表啟動" : "⏱️ 碼表暫停");
                break;
        }
    }

    handleSecondaryAction() {
        if (this.currentMode === 'timer') {
            // Add 1 minute to timer duration
            this.tmRemainingSeconds += 60;
            this.tmDuration += 60;
            this.updateDisplay(true);
            this.showToast("➕ 已增加 1 分鐘");
        } else if (this.currentMode === 'stopwatch') {
            if (!this.swRunning && this.swElapsedTime === 0) return;
            // Record split/lap time
            const lapTime = this.swElapsedTime - this.swLastLapTime;
            this.swLaps.unshift({
                id: this.swLaps.length + 1,
                lap: lapTime,
                total: this.swElapsedTime
            });
            this.swLastLapTime = this.swElapsedTime;
            this.renderLaps();

            // Auto scroll to top of laps list
            const list = document.getElementById('lap-records');
            list.classList.remove('hidden');
            list.scrollTop = 0;

            this.showToast("⏱️ 記錄分圈時間");
        }
    }

    handleResetAction() {
        switch (this.currentMode) {
            case 'pomodoro':
                this.pomoRunning = false;
                this.pomoMode = 'focus';
                this.pomoRemainingSeconds = 1500; // 25m
                document.getElementById('status-label').textContent = '🍅 POMODORO FOCUS';
                this.updatePlayPauseButtonUI(false);
                this.updateDisplay(true);
                this.showToast("🍅 番茄鐘已重設");
                break;
            case 'timer':
                this.tmRunning = false;
                this.tmRemainingSeconds = 600; // 10 minutes default
                this.tmDuration = 600;
                this.updatePlayPauseButtonUI(false);
                this.updateDisplay(true);
                this.showToast("⏳ 計時器已重設");
                break;
            case 'stopwatch':
                this.swRunning = false;
                this.swElapsedTime = 0;
                this.swLastLapTime = 0;
                this.swLaps = [];
                this.updatePlayPauseButtonUI(false);
                this.updateDisplay(true);
                this.renderLaps();
                this.showToast("⏱️ 碼表已重設");
                break;
        }
    }

    renderLaps() {
        const lapContainer = document.getElementById('lap-list');
        const containerBox = document.getElementById('lap-records');

        if (this.swLaps.length === 0) {
            lapContainer.innerHTML = '<div class="text-center text-white/30 py-4">無分圈紀錄</div>';
            return;
        }

        lapContainer.innerHTML = '';
        this.swLaps.forEach((lap, idx) => {
            const item = document.createElement('div');
            item.className = 'lap-item flex justify-between py-1 text-white/80 border-b border-white/5';

            const formatTime = (ms) => {
                const totalSec = Math.floor(ms / 1000);
                const hours = Math.floor(totalSec / 3600);
                const minutes = Math.floor((totalSec % 3600) / 60);
                const seconds = totalSec % 60;
                const mils = Math.floor((ms % 1000) / 10);

                const hs = hours > 0 ? `${hours.toString().padStart(2, '0')}:` : '';
                return `${hs}${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}.${mils.toString().padStart(2, '0')}`;
            };

            item.innerHTML = `
                <span class="text-indigo-400">#${this.swLaps.length - idx}</span>
                <span>${formatTime(lap.lap)}</span>
                <span class="text-white/50">${formatTime(lap.total)}</span>
            `;
            lapContainer.appendChild(item);
        });
    }


    // --- Core Engine Loop ---
    startEngine() {
        const tick = () => {
            this.updateData();
            this.updateDisplay();

            // Smoothly runs on requestAnimationFrame for millisecond stopwatch,
            // or falls back to loop
            requestAnimationFrame(tick);
        };
        requestAnimationFrame(tick);
    }

    updateData() {
        if (this.currentMode === 'stopwatch' && this.swRunning) {
            this.swElapsedTime = Date.now() - this.swStartTime;
        }

        // Timers tick per second. We use standard time calculation
        const nowSec = Math.floor(Date.now() / 1000);
        if (this.lastSecondChecked !== nowSec) {
            this.lastSecondChecked = nowSec;

            // Pomodoro countdown
            if (this.currentMode === 'pomodoro' && this.pomoRunning) {
                if (this.pomoRemainingSeconds > 0) {
                    this.pomoRemainingSeconds--;
                } else {
                    // Session finished
                    this.pomoRunning = false;
                    window.flipSynth.playAlarm();

                    if (this.pomoMode === 'focus') {
                        this.pomoMode = 'break';
                        this.pomoRemainingSeconds = 300; // 5m break
                        document.getElementById('status-label').textContent = '☕ BREAK TIME';
                        this.showToast("專注完成！進入休息時間", '☕');
                    } else {
                        this.pomoMode = 'focus';
                        this.pomoRemainingSeconds = 1500; // 25m focus
                        document.getElementById('status-label').textContent = '🍅 POMODORO FOCUS';
                        this.showToast("休息時間結束！開始專注", '🍅');
                    }
                    this.updatePlayPauseButtonUI(false);
                }
            }

            // Countdown Timer
            if (this.currentMode === 'timer' && this.tmRunning) {
                if (this.tmRemainingSeconds > 0) {
                    this.tmRemainingSeconds--;
                } else {
                    this.tmRunning = false;
                    window.flipSynth.playAlarm();
                    this.showToast("計時結束！時間到！", '⏰');
                    this.updatePlayPauseButtonUI(false);
                }
            }
        }
    }

    updateDisplay(force = false) {
        let timeStr = '';
        let msStr = '00';

        switch (this.currentMode) {
            case 'clock':
                const now = new Date();
                let hours = now.getHours();
                const minutes = now.getMinutes();
                const seconds = now.getSeconds();

                // Format Hours for 12/24 Hour format
                let periodText = '';
                if (!this.timeFormat24) {
                    const isPm = hours >= 12;
                    periodText = isPm ? ' 下午 PM' : ' 上午 AM';
                    hours = hours % 12;
                    if (hours === 0) hours = 12;
                }

                timeStr =
                    hours.toString().padStart(2, '0') +
                    minutes.toString().padStart(2, '0') +
                    seconds.toString().padStart(2, '0');

                // Blink colon
                const colonDots = document.querySelectorAll('.colon-dot');
                if (now.getMilliseconds() < 500) {
                    colonDots.forEach(d => d.style.opacity = '1');
                } else {
                    colonDots.forEach(d => d.style.opacity = '0.35');
                }

                // Update date label once in a while
                const days = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六'];
                const dateLabel = `${now.getFullYear()}年${(now.getMonth() + 1).toString().padStart(2, '0')}月${now.getDate().toString().padStart(2, '0')}日 ${days[now.getDay()]}${periodText}`;

                // Only update DOM if text changed
                const dateEl = document.getElementById('clock-date');
                if (dateEl.textContent !== dateLabel) {
                    dateEl.textContent = dateLabel;
                }
                break;

            case 'pomodoro':
                const pMin = Math.floor(this.pomoRemainingSeconds / 60);
                const pSec = this.pomoRemainingSeconds % 60;
                // Hour slots set to 00
                timeStr = '00' + pMin.toString().padStart(2, '0') + pSec.toString().padStart(2, '0');

                // Pulse colon gently if running
                document.querySelectorAll('.colon-dot').forEach(d => d.style.opacity = (this.pomoRunning && (Date.now() % 1000 < 500)) ? '0.3' : '1');
                break;

            case 'timer':
                const tHrs = Math.floor(this.tmRemainingSeconds / 3600);
                const tMin = Math.floor((this.tmRemainingSeconds % 3600) / 60);
                const tSec = this.tmRemainingSeconds % 60;

                timeStr =
                    tHrs.toString().padStart(2, '0') +
                    tMin.toString().padStart(2, '0') +
                    tSec.toString().padStart(2, '0');

                document.querySelectorAll('.colon-dot').forEach(d => d.style.opacity = (this.tmRunning && (Date.now() % 1000 < 500)) ? '0.3' : '1');
                break;

            case 'stopwatch':
                const totalSec = Math.floor(this.swElapsedTime / 1000);
                const swHrs = Math.floor(totalSec / 3600);
                const swMin = Math.floor((totalSec % 3600) / 60);
                const swSec = totalSec % 60;
                const swMs = Math.floor((this.swElapsedTime % 1000) / 10);

                timeStr =
                    swHrs.toString().padStart(2, '0') +
                    swMin.toString().padStart(2, '0') +
                    swSec.toString().padStart(2, '0');

                msStr = swMs.toString().padStart(2, '0');

                // keep dots on for stopwatch
                document.querySelectorAll('.colon-dot').forEach(d => d.style.opacity = '1');
                break;
        }

        // Apply string to FlipCard objects
        if (timeStr !== this.lastTimeStr || force) {
            this.lastTimeStr = timeStr;

            this.digits.hTens.setVal(timeStr[0], force);
            this.digits.hOnes.setVal(timeStr[1], force);
            this.digits.mTens.setVal(timeStr[2], force);
            this.digits.mOnes.setVal(timeStr[3], force);
            this.digits.sTens.setVal(timeStr[4], force);
            this.digits.sOnes.setVal(timeStr[5], force);
        }

        if (this.currentMode === 'stopwatch') {
            this.digits.msTens.setVal(msStr[0], force);
            this.digits.msOnes.setVal(msStr[1], force);
        }
    }


    // --- Settings / Customize methods ---
    applyTheme(themeName) {
        const body = document.body;
        body.className = body.className.replace(/theme-\w+/, `theme-${themeName}`);
        this.activeTheme = themeName;

        // Change backglow and particle colors based on theme colors
        const themeColors = {
            dark: '#6366f1',
            cyber: '#ff007f',
            sakura: '#fda4af',
            forest: '#10b981',
            wood: '#d97706',
            light: '#4f46e5'
        };

        const primaryColor = themeColors[themeName] || '#6366f1';
        this.particlesBg.setColors(primaryColor);

        this.showToast(`🎨 已套用：${this.getThemeDisplayName(themeName)}`);
    }

    getThemeDisplayName(name) {
        const names = {
            dark: '極簡暗黑',
            cyber: '賽博霓虹',
            sakura: '極致櫻花',
            forest: '極光森林',
            wood: '復古木紋',
            light: '經典明亮'
        };
        return names[name] || name;
    }

    applyCardStyle(cardStyle) {
        const container = document.getElementById('clock-container');
        // Remove current card classes
        container.classList.remove('card-classic', 'card-glass', 'card-neon', 'card-wood');
        // Add new class
        container.classList.add(`card-${cardStyle}`);
        this.activeCardStyle = cardStyle;

        this.showToast(`🎴 質感切換：${this.getCardStyleDisplayName(cardStyle)}`);
    }

    getCardStyleDisplayName(style) {
        const styles = {
            classic: '經典霧黑',
            glass: '毛玻璃質感',
            neon: '霓虹外框',
            wood: '胡桃木紋'
        };
        return styles[style] || style;
    }

    applyFont(fontName) {
        const container = document.getElementById('clock-container');
        container.classList.remove('font-mono', 'font-montserrat', 'font-sans');

        if (fontName === 'share-tech') {
            container.classList.add('font-mono');
        } else if (fontName === 'montserrat') {
            container.classList.add('font-montserrat');
        } else if (fontName === 'inter' || fontName === 'noto') {
            container.classList.add('font-sans');
        }

        this.activeFont = fontName;
        this.updateDisplay(true); // Redraw flips because width/font sizes might slightly adjust
        this.showToast('🔤 字體已套用');
    }
}

// Initialise Application when document is fully loaded
document.addEventListener('DOMContentLoaded', () => {
    window.flipClockApp = new FlipClockApp();
});
