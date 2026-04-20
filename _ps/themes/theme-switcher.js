/* ============================================
 * Museum Theme Switcher
 * Manages the dynamic loading and switching of museum-themed CSS.
 * ============================================ */

class ThemeSwitcher {
  constructor() {
    this.currentTheme = localStorage.getItem('museum-theme') || 'default';
    this.themeLink = null;
    this.init();
  }

  init() {
    // Ensure base styles are loaded
    this.loadBaseStyles();
    
    // Create theme switcher UI element (if needed)
    // For now, we provide a programmatic API. 
    // In actual reports, a UI menu could be added.
    
    // Apply initial theme
    this.switchTheme(this.currentTheme);
    
    console.log('🏛️ Museum Theme Switcher Initialized', this.currentTheme);
  }

  loadBaseStyles() {
    if (!document.querySelector('link[href*="_base.css"]')) {
      const baseLink = document.createElement('link');
      baseLink.rel = 'stylesheet';
      baseLink.href = '../themes/_base.css'; // Adjust path based on relative position
      document.head.appendChild(baseLink);
    }
    
    if (!document.querySelector('link[href*="_base-responsive.css"]')) {
      const respLink = document.createElement('link');
      respLink.rel = 'stylesheet';
      respLink.href = '../themes/_base-responsive.css';
      document.head.appendChild(respLink);
    }
  }

  /**
   * Switches the active museum theme.
   * @param {string} themeName - The ID of the theme (e.g., '01-bento-grid')
   */
  async switchTheme(themeName) {
    if (!themeName) return;
    
    // Remove existing theme link
    if (this.themeLink) {
      this.themeLink.remove();
    }
    
    if (themeName === 'default') {
      document.documentElement.removeAttribute('data-theme');
      localStorage.removeItem('museum-theme');
      return;
    }

    const themeUrl = `../themes/${themeName}.css`;
    
    this.themeLink = document.createElement('link');
    this.themeLink.rel = 'stylesheet';
    this.themeLink.href = themeUrl;
    this.themeLink.id = 'active-museum-theme';
    
    document.head.appendChild(this.themeLink);
    document.documentElement.setAttribute('data-theme', themeName.replace(/^\d+-/, ''));
    
    this.currentTheme = themeName;
    localStorage.setItem('museum-theme', themeName);
    
    return new Promise((resolve) => {
      this.themeLink.onload = () => resolve();
    });
  }
}

// Global instance
window.museumTheme = new ThemeSwitcher();
