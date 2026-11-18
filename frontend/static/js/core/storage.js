/**
 * JUSTBADDO — Safe Local Storage Manager
 * Wraps localStorage with fallback memory storage for private browsing or restricted environments.
 */

window.JustBaddoStorage = {
  prefix: 'jb_',
  memoryStore: {},

  get(key, defaultValue = null) {
    const fullKey = this.prefix + key;
    try {
      if (typeof window !== 'undefined' && window.localStorage) {
        const item = window.localStorage.getItem(fullKey);
        return item !== null ? JSON.parse(item) : defaultValue;
      }
    } catch (e) {
      console.warn('[JustBaddoStorage] LocalStorage read failed, falling back to memory store:', e);
    }
    return this.memoryStore[fullKey] !== undefined ? this.memoryStore[fullKey] : defaultValue;
  },

  set(key, value) {
    const fullKey = this.prefix + key;
    try {
      if (typeof window !== 'undefined' && window.localStorage) {
        window.localStorage.setItem(fullKey, JSON.stringify(value));
        return true;
      }
    } catch (e) {
      console.warn('[JustBaddoStorage] LocalStorage write failed, falling back to memory store:', e);
    }
    this.memoryStore[fullKey] = value;
    return true;
  },

  remove(key) {
    const fullKey = this.prefix + key;
    try {
      if (typeof window !== 'undefined' && window.localStorage) {
        window.localStorage.removeItem(fullKey);
      }
    } catch (e) {
      console.warn('[JustBaddoStorage] LocalStorage remove failed:', e);
    }
    delete this.memoryStore[fullKey];
  }
};
