/**
 * Comparative Dhivehi Dialect Explorer - Main JavaScript App
 */

// Application State
const state = {
  data: [],
  filteredData: [],
  searchTerm: '',
  selectedCategory: 'ALL',
  scriptMode: 'both', // 'both' | 'thaana' | 'latin'
  viewMode: 'table',  // 'table' | 'cards'
  sortColumn: 'id',
  sortAsc: true,
  visibleCols: {
    male: true,
    addu: true,
    huvadhu: true,
    fuvahmulah: true,
    maliku: true,
    sinhala: true,
    malayalam: true,
    arabic: true,
  },
  theme: localStorage.getItem('theme') || 'dark',
  activeTab: 'explorer', // 'explorer' | 'proximity'
  proxSearch: '',
  proxCategory: 'ALL',
  proxSort: 'id-asc',
};

// Dialect metadata mapping
const DIALECTS = [
  { key: 'male', label: "Male' (Std)", latinCol: "Male' - Latin", thaanaCol: "Male' - Thaana", color: 'var(--col-male)' },
  { key: 'addu', label: 'Addu', latinCol: 'Addu - Latin', thaanaCol: 'Addu - Thaana', color: 'var(--col-addu)' },
  { key: 'huvadhu', label: 'Huvadhu', latinCol: 'Huvadhu - Latin', thaanaCol: 'Huvadhu - Thaana', color: 'var(--col-huvadhu)' },
  { key: 'fuvahmulah', label: 'Fuvahmulah', latinCol: 'Fuvahmulah - Latin', thaanaCol: 'Fuvahmulah - Thaana', color: 'var(--col-fuvahmulah)' },
  { key: 'maliku', label: 'Maliku (Mahl)', latinCol: 'Maliku - Latin', thaanaCol: 'Maliku - Thaana', color: 'var(--col-maliku)' },
];

const COGNATES = [
  { key: 'sinhala', label: 'Sinhala', col: 'Sinhala', color: 'var(--col-sinhala)' },
  { key: 'malayalam', label: 'Malayalam', col: 'Malayalam', color: 'var(--col-malayalam)' },
  { key: 'arabic', label: 'Arabic', col: 'Arabic', color: 'var(--col-arabic)' },
];

// DOM Elements
const DOM = {
  themeToggleBtn: document.getElementById('themeToggleBtn'),
  searchInput: document.getElementById('searchInput'),
  clearSearchBtn: document.getElementById('clearSearchBtn'),
  scriptModeGroup: document.getElementById('scriptModeGroup'),
  viewModeGroup: document.getElementById('viewModeGroup'),
  categoryChipsContainer: document.getElementById('categoryChipsContainer'),
  columnCheckboxesContainer: document.getElementById('columnCheckboxesContainer'),
  downloadCsvBtn: document.getElementById('downloadCsvBtn'),
  statTotalWords: document.getElementById('statTotalWords'),
  statCategories: document.getElementById('statCategories'),
  resultsCount: document.getElementById('resultsCount'),
  activeFiltersSummary: document.getElementById('activeFiltersSummary'),
  loadingState: document.getElementById('loadingState'),
  emptyState: document.getElementById('emptyState'),
  resetFiltersBtn: document.getElementById('resetFiltersBtn'),
  tableViewWrapper: document.getElementById('tableViewWrapper'),
  cardsViewWrapper: document.getElementById('cardsViewWrapper'),
  tableBody: document.getElementById('tableBody'),
  dialectTable: document.getElementById('dialectTable'),
  wordModal: document.getElementById('wordModal'),
  closeModalBtn: document.getElementById('closeModalBtn'),
  modalId: document.getElementById('modalId'),
  modalCategory: document.getElementById('modalCategory'),
  modalWordList: document.getElementById('modalWordList'),
  modalEnglish: document.getElementById('modalEnglish'),
  modalDialectsGrid: document.getElementById('modalDialectsGrid'),
  modalCognatesGrid: document.getElementById('modalCognatesGrid'),
  modalNotesSection: document.getElementById('modalNotesSection'),
  modalNotes: document.getElementById('modalNotes'),
  copyJsonBtn: document.getElementById('copyJsonBtn'),
  toast: document.getElementById('toast'),
  // Navigation Tabs
  navTabExplorer: document.getElementById('navTabExplorer'),
  navTabProximity: document.getElementById('navTabProximity'),
  tabContentExplorer: document.getElementById('tabContentExplorer'),
  tabContentProximity: document.getElementById('tabContentProximity'),
  // Proximity View Elements
  proximitySummaryCards: document.getElementById('proximitySummaryCards'),
  matrixTableContainer: document.getElementById('matrixTableContainer'),
  proxSearchInput: document.getElementById('proxSearchInput'),
  proxCategorySelect: document.getElementById('proxCategorySelect'),
  proxSortSelect: document.getElementById('proxSortSelect'),
  proxResultsCount: document.getElementById('proxResultsCount'),
  conceptProxGrid: document.getElementById('conceptProxGrid'),
};

let currentModalItem = null;

// ==========================================
// Initialization & Data Loading
// ==========================================
async function initApp() {
  applyTheme(state.theme);
  setupEventListeners();
  loadUrlParams();

  try {
    const csvData = await fetchCsvData();
    parseAndInitData(csvData);
  } catch (err) {
    console.error('Error fetching CSV:', err);
    DOM.loadingState.innerHTML = `
      <div class="empty-icon">⚠️</div>
      <h3>Could not load CSV file</h3>
      <p>${err.message}</p>
    `;
  }
}

async function fetchCsvData() {
  const csvUrl = 'dhivehi_language_comparision.csv';
  const response = await fetch(csvUrl);
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return await response.text();
}

function parseAndInitData(csvText) {
  Papa.parse(csvText, {
    header: true,
    skipEmptyLines: true,
    complete: (results) => {
      // Clean and normalize rows
      state.data = results.data.map((row, idx) => ({
        id: (row['ID'] || `W-${idx + 1}`).trim(),
        wordList: (row['Word List'] || 'General').trim(),
        category: (row['Category'] || 'Uncategorized').trim(),
        english: (row['English'] || '').trim(),
        maleLatin: (row["Male' - Latin"] || '').trim(),
        maleThaana: (row["Male' - Thaana"] || '').trim(),
        adduLatin: (row['Addu - Latin'] || '').trim(),
        adduThaana: (row['Addu - Thaana'] || '').trim(),
        huvadhuLatin: (row['Huvadhu - Latin'] || '').trim(),
        huvadhuThaana: (row['Huvadhu - Thaana'] || '').trim(),
        fuvahmulahLatin: (row['Fuvahmulah - Latin'] || '').trim(),
        fuvahmulahThaana: (row['Fuvahmulah - Thaana'] || '').trim(),
        malikuLatin: (row['Maliku - Latin'] || '').trim(),
        malikuThaana: (row['Maliku - Thaana'] || '').trim(),
        sinhala: (row['Sinhala'] || '').trim(),
        malayalam: (row['Malayalam'] || '').trim(),
        arabic: (row['Arabic'] || '').trim(),
        notes: (row['Notes'] || '').trim(),
        raw: row,
      }));

      // Render categories
      populateCategories();
      updateStats();
      applyFilters();
      DOM.loadingState.style.display = 'none';

      // Check URL for direct ID inspect
      const urlParams = new URLSearchParams(window.location.search);
      const openId = urlParams.get('id');
      if (openId) {
        const item = state.data.find(d => d.id.toLowerCase() === openId.toLowerCase());
        if (item) openModal(item);
      }
    },
    error: (err) => {
      console.error('PapaParse error:', err);
      DOM.loadingState.innerHTML = `<p>Error parsing CSV: ${err.message}</p>`;
    }
  });
}

// ==========================================
// Filtering & Sorting
// ==========================================
function applyFilters() {
  const query = state.searchTerm.toLowerCase().trim();
  const cat = state.selectedCategory;

  state.filteredData = state.data.filter(item => {
    // Category match
    if (cat !== 'ALL' && item.category !== cat) {
      return false;
    }

    // Search query match
    if (query) {
      const searchFields = [
        item.id,
        item.category,
        item.english,
        item.maleLatin,
        item.maleThaana,
        item.adduLatin,
        item.adduThaana,
        item.huvadhuLatin,
        item.huvadhuThaana,
        item.fuvahmulahLatin,
        item.fuvahmulahThaana,
        item.malikuLatin,
        item.malikuThaana,
        item.sinhala,
        item.malayalam,
        item.arabic,
        item.notes
      ];

      const matches = searchFields.some(field => field && field.toLowerCase().includes(query));
      if (!matches) return false;
    }

    return true;
  });

  // Sort
  sortData();

  // Render view
  renderCurrentView();
  updateResultsCount();
  updateUrlParams();
}

function sortData() {
  const col = state.sortColumn;
  const asc = state.sortAsc ? 1 : -1;

  state.filteredData.sort((a, b) => {
    let valA = '';
    let valB = '';

    switch (col) {
      case 'id': valA = a.id; valB = b.id; break;
      case 'category': valA = a.category; valB = b.category; break;
      case 'english': valA = a.english; valB = b.english; break;
      case 'male': valA = a.maleLatin || a.maleThaana; valB = b.maleLatin || b.maleThaana; break;
      case 'addu': valA = a.adduLatin || a.adduThaana; valB = b.adduLatin || b.adduThaana; break;
      case 'huvadhu': valA = a.huvadhuLatin || a.huvadhuThaana; valB = b.huvadhuLatin || b.huvadhuThaana; break;
      case 'fuvahmulah': valA = a.fuvahmulahLatin || a.fuvahmulahThaana; valB = b.fuvahmulahLatin || b.fuvahmulahThaana; break;
      case 'maliku': valA = a.malikuLatin || a.malikuThaana; valB = b.malikuLatin || b.malikuThaana; break;
      case 'sinhala': valA = a.sinhala; valB = b.sinhala; break;
      case 'malayalam': valA = a.malayalam; valB = b.malayalam; break;
      case 'arabic': valA = a.arabic; valB = b.arabic; break;
      default: valA = a.id; valB = b.id;
    }

    return valA.localeCompare(valB, undefined, { numeric: true, sensitivity: 'base' }) * asc;
  });
}

// ==========================================
// Rendering Functions
// ==========================================
function renderCurrentView() {
  if (state.filteredData.length === 0) {
    DOM.tableViewWrapper.style.display = 'none';
    DOM.cardsViewWrapper.style.display = 'none';
    DOM.emptyState.style.display = 'flex';
    return;
  }

  DOM.emptyState.style.display = 'none';

  if (state.viewMode === 'table') {
    DOM.cardsViewWrapper.style.display = 'none';
    DOM.tableViewWrapper.style.display = 'block';
    renderTable();
  } else {
    DOM.tableViewWrapper.style.display = 'none';
    DOM.cardsViewWrapper.style.display = 'grid';
    renderCards();
  }
}

function renderTable() {
  DOM.tableBody.innerHTML = state.filteredData.map(item => `
    <tr data-id="${item.id}" onclick="window.appOpenModal('${item.id}')" style="cursor:pointer;">
      <td><span class="badge badge-id">${escapeHtml(item.id)}</span></td>
      <td><span class="badge badge-category">${escapeHtml(item.category)}</span></td>
      <td style="font-weight:600; color:var(--text-main);">${escapeHtml(item.english)}</td>
      <td class="col-male" ${state.visibleCols.male ? '' : 'style="display:none;"'}>${renderDialectCell(item.maleThaana, item.maleLatin)}</td>
      <td class="col-addu" ${state.visibleCols.addu ? '' : 'style="display:none;"'}>${renderDialectCell(item.adduThaana, item.adduLatin)}</td>
      <td class="col-huvadhu" ${state.visibleCols.huvadhu ? '' : 'style="display:none;"'}>${renderDialectCell(item.huvadhuThaana, item.huvadhuLatin)}</td>
      <td class="col-fuvahmulah" ${state.visibleCols.fuvahmulah ? '' : 'style="display:none;"'}>${renderDialectCell(item.fuvahmulahThaana, item.fuvahmulahLatin)}</td>
      <td class="col-maliku" ${state.visibleCols.maliku ? '' : 'style="display:none;"'}>${renderDialectCell(item.malikuThaana, item.malikuLatin)}</td>
      <td class="col-sinhala" ${state.visibleCols.sinhala ? '' : 'style="display:none;"'}>${renderCognateCell(item.sinhala)}</td>
      <td class="col-malayalam" ${state.visibleCols.malayalam ? '' : 'style="display:none;"'}>${renderCognateCell(item.malayalam)}</td>
      <td class="col-arabic" ${state.visibleCols.arabic ? '' : 'style="display:none;"'}>${renderCognateCell(item.arabic)}</td>
      <td>
        <button class="btn btn-secondary btn-sm" onclick="event.stopPropagation(); window.appOpenModal('${item.id}')" title="Inspect word">
          <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
        </button>
      </td>
    </tr>
  `).join('');

  updateTableColumnVisibility();
}

function renderCards() {
  DOM.cardsViewWrapper.innerHTML = state.filteredData.map(item => `
    <div class="word-card" onclick="window.appOpenModal('${item.id}')">
      <div class="card-top-bar">
        <div style="display:flex; gap:0.4rem; align-items:center;">
          <span class="badge badge-id">${escapeHtml(item.id)}</span>
          <span class="badge badge-category">${escapeHtml(item.category)}</span>
        </div>
      </div>
      
      <div class="card-english-title">${escapeHtml(item.english)}</div>

      <div class="card-dialects-list">
        ${state.visibleCols.male ? `
          <div class="card-dialect-row" style="border-left-color: var(--col-male);">
            <span class="card-dialect-name">Male'</span>
            <div style="text-align:right;">${renderDialectCell(item.maleThaana, item.maleLatin)}</div>
          </div>` : ''}

        ${state.visibleCols.addu ? `
          <div class="card-dialect-row" style="border-left-color: var(--col-addu);">
            <span class="card-dialect-name">Addu</span>
            <div style="text-align:right;">${renderDialectCell(item.adduThaana, item.adduLatin)}</div>
          </div>` : ''}

        ${state.visibleCols.huvadhu ? `
          <div class="card-dialect-row" style="border-left-color: var(--col-huvadhu);">
            <span class="card-dialect-name">Huvadhu</span>
            <div style="text-align:right;">${renderDialectCell(item.huvadhuThaana, item.huvadhuLatin)}</div>
          </div>` : ''}

        ${state.visibleCols.fuvahmulah ? `
          <div class="card-dialect-row" style="border-left-color: var(--col-fuvahmulah);">
            <span class="card-dialect-name">Fuvahmulah</span>
            <div style="text-align:right;">${renderDialectCell(item.fuvahmulahThaana, item.fuvahmulahLatin)}</div>
          </div>` : ''}

        ${state.visibleCols.maliku ? `
          <div class="card-dialect-row" style="border-left-color: var(--col-maliku);">
            <span class="card-dialect-name">Maliku</span>
            <div style="text-align:right;">${renderDialectCell(item.malikuThaana, item.malikuLatin)}</div>
          </div>` : ''}

        ${state.visibleCols.sinhala && item.sinhala ? `
          <div class="card-dialect-row" style="border-left-color: var(--col-sinhala);">
            <span class="card-dialect-name">Sinhala</span>
            <div style="text-align:right;">${renderCognateCell(item.sinhala)}</div>
          </div>` : ''}

        ${state.visibleCols.malayalam && item.malayalam ? `
          <div class="card-dialect-row" style="border-left-color: var(--col-malayalam);">
            <span class="card-dialect-name">Malayalam</span>
            <div style="text-align:right;">${renderCognateCell(item.malayalam)}</div>
          </div>` : ''}

        ${state.visibleCols.arabic && item.arabic ? `
          <div class="card-dialect-row" style="border-left-color: var(--col-arabic);">
            <span class="card-dialect-name">Arabic</span>
            <div style="text-align:right;">${renderCognateCell(item.arabic)}</div>
          </div>` : ''}
      </div>
    </div>
  `).join('');
}

function renderDialectCell(thaana, latin) {
  const hasThaana = !!thaana && thaana.trim() !== '';
  const hasLatin = !!latin && latin.trim() !== '';

  if (!hasThaana && !hasLatin) {
    return '<div class="empty-cell-dash">—</div>';
  }

  const thaanaParts = hasThaana ? thaana.split(/\s*\/\s*/).map(s => s.trim()).filter(Boolean) : [];
  const latinParts = hasLatin ? latin.split(/\s*\/\s*/).map(s => s.trim()).filter(Boolean) : [];

  const maxLen = Math.max(thaanaParts.length, latinParts.length);
  const mode = state.scriptMode;

  let html = '<div class="dialect-cell-wrapper">';

  for (let i = 0; i < maxLen; i++) {
    const t = thaanaParts[i] || (thaanaParts.length === 1 && latinParts.length > 1 ? thaanaParts[0] : '');
    const l = latinParts[i] || (latinParts.length === 1 && thaanaParts.length > 1 ? latinParts[0] : '');

    html += `<div class="variant-item">`;
    if ((mode === 'both' || mode === 'thaana') && t) {
      html += `<div class="thaana-text">${escapeHtml(t)}</div>`;
    }
    if ((mode === 'both' || mode === 'latin') && l) {
      html += `<div class="latin-text">${escapeHtml(l)}</div>`;
    }
    if (mode === 'thaana' && !t && l) {
      html += `<div class="latin-text text-fallback">${escapeHtml(l)}</div>`;
    }
    if (mode === 'latin' && !l && t) {
      html += `<div class="thaana-text text-fallback">${escapeHtml(t)}</div>`;
    }
    html += `</div>`;
  }

  html += '</div>';
  return html;
}

function renderCognateCell(text) {
  if (!text || text.trim() === '') return '<div class="empty-cell-dash">—</div>';
  
  const parts = text.split(/\s*\/\s*/).map(s => s.trim()).filter(Boolean);
  if (parts.length === 1) {
    return `<div class="cognate-single">${escapeHtml(parts[0])}</div>`;
  }

  return `
    <div class="cognate-list">
      ${parts.map(p => `<div class="cognate-item">${escapeHtml(p)}</div>`).join('')}
    </div>
  `;
}

function updateTableColumnVisibility() {
  const cols = ['male', 'addu', 'huvadhu', 'fuvahmulah', 'maliku', 'sinhala', 'malayalam', 'arabic'];
  
  let visibleDialectsCount = 0;
  let visibleCognatesCount = 0;

  const dialectKeys = ['male', 'addu', 'huvadhu', 'fuvahmulah', 'maliku'];
  const cognateKeys = ['sinhala', 'malayalam', 'arabic'];

  dialectKeys.forEach(col => {
    if (state.visibleCols[col]) visibleDialectsCount++;
  });

  cognateKeys.forEach(col => {
    if (state.visibleCols[col]) visibleCognatesCount++;
  });

  // Adjust table group header colspans
  const thGroupDialects = document.querySelector('.th-group-dialects');
  if (thGroupDialects) {
    if (visibleDialectsCount === 0) {
      thGroupDialects.style.display = 'none';
    } else {
      thGroupDialects.style.display = '';
      thGroupDialects.colSpan = visibleDialectsCount;
    }
  }

  const thGroupCognates = document.querySelector('.th-group-cognates');
  if (thGroupCognates) {
    if (visibleCognatesCount === 0) {
      thGroupCognates.style.display = 'none';
    } else {
      thGroupCognates.style.display = '';
      thGroupCognates.colSpan = visibleCognatesCount;
    }
  }

  cols.forEach(col => {
    const isVisible = state.visibleCols[col];
    const elements = document.querySelectorAll(`.col-${col}`);
    elements.forEach(el => {
      el.style.display = isVisible ? '' : 'none';
    });
  });
}

function populateCategories() {
  const categories = [...new Set(state.data.map(d => d.category))].filter(Boolean).sort();
  
  DOM.statCategories.textContent = categories.length;

  const chipsHtml = [
    `<button class="chip ${state.selectedCategory === 'ALL' ? 'active' : ''}" data-category="ALL">All Concepts (${state.data.length})</button>`
  ];

  categories.forEach(cat => {
    const count = state.data.filter(d => d.category === cat).length;
    chipsHtml.push(
      `<button class="chip ${state.selectedCategory === cat ? 'active' : ''}" data-category="${escapeHtml(cat)}">${escapeHtml(cat)} (${count})</button>`
    );
  });

  DOM.categoryChipsContainer.innerHTML = chipsHtml.join('');
}

function updateStats() {
  DOM.statTotalWords.textContent = state.data.length;
}

function updateResultsCount() {
  DOM.resultsCount.textContent = `Showing ${state.filteredData.length} of ${state.data.length} concepts`;

  const filters = [];
  if (state.searchTerm) filters.push(`Search: "${state.searchTerm}"`);
  if (state.selectedCategory !== 'ALL') filters.push(`Category: ${state.selectedCategory}`);

  DOM.activeFiltersSummary.innerHTML = filters.map(f => `<span class="chip">${escapeHtml(f)}</span>`).join('');
}

// ==========================================
// Modal & Detail View
// ==========================================
window.appOpenModal = function(id) {
  const item = state.data.find(d => d.id === id);
  if (!item) return;
  openModal(item);
};

function openModal(item) {
  currentModalItem = item;
  DOM.modalId.textContent = item.id;
  DOM.modalCategory.textContent = item.category;
  DOM.modalWordList.textContent = item.wordList;
  DOM.modalEnglish.textContent = item.english;

  // Build dialect grid
  DOM.modalDialectsGrid.innerHTML = DIALECTS.map(d => {
    const latin = item.raw[d.latinCol] || '';
    const thaana = item.raw[d.thaanaCol] || '';
    const hasData = (latin && latin.trim() !== '') || (thaana && thaana.trim() !== '');

    if (!hasData) {
      return `
        <div class="detail-card" style="border-left: 3px solid ${d.color};">
          <span class="detail-card-label">${d.label}</span>
          <span class="empty-cell-dash">Unattested</span>
        </div>
      `;
    }

    const tParts = thaana ? thaana.split(/\s*\/\s*/).map(s => s.trim()).filter(Boolean) : [];
    const lParts = latin ? latin.split(/\s*\/\s*/).map(s => s.trim()).filter(Boolean) : [];
    const maxL = Math.max(tParts.length, lParts.length);

    let contentHtml = '';
    for (let i = 0; i < maxL; i++) {
      const t = tParts[i] || (tParts.length === 1 ? tParts[0] : '');
      const l = lParts[i] || (lParts.length === 1 ? lParts[0] : '');
      contentHtml += `
        <div class="modal-variant-item">
          ${t ? `<div class="thaana-text" style="font-size:1.3rem;">${escapeHtml(t)}</div>` : ''}
          ${l ? `<div class="latin-text" style="font-size:0.95rem; font-weight:600; color:var(--text-main);">${escapeHtml(l)}</div>` : ''}
        </div>
      `;
    }

    return `
      <div class="detail-card" style="border-left: 3px solid ${d.color};">
        <span class="detail-card-label">${d.label}</span>
        <div class="modal-variant-list">${contentHtml}</div>
      </div>
    `;
  }).join('');

  // Build cognates grid
  DOM.modalCognatesGrid.innerHTML = COGNATES.map(c => {
    const text = item.raw[c.col] || '';
    const parts = text ? text.split(/\s*\/\s*/).map(s => s.trim()).filter(Boolean) : [];

    return `
      <div class="detail-card" style="border-left: 3px solid ${c.color};">
        <span class="detail-card-label">${c.label}</span>
        ${parts.length > 0 ? `
          <div class="cognate-list">
            ${parts.map(p => `<div class="cognate-item" style="font-size:0.92rem; color:var(--text-main);">${escapeHtml(p)}</div>`).join('')}
          </div>
        ` : '<span class="empty-cell-dash">—</span>'}
      </div>
    `;
  }).join('');

  // Notes
  if (item.notes) {
    DOM.modalNotesSection.style.display = 'block';
    DOM.modalNotes.textContent = item.notes;
  } else {
    DOM.modalNotesSection.style.display = 'none';
  }

  DOM.wordModal.showModal();
}

function closeModal() {
  DOM.wordModal.close();
  currentModalItem = null;
}

// ==========================================
// Event Listeners & Interactions
// ==========================================
function setupEventListeners() {
  // Theme toggle
  DOM.themeToggleBtn.addEventListener('click', () => {
    const nextTheme = state.theme === 'dark' ? 'light' : 'dark';
    applyTheme(nextTheme);
  });

  // Search input
  DOM.searchInput.addEventListener('input', (e) => {
    state.searchTerm = e.target.value;
    DOM.clearSearchBtn.style.display = state.searchTerm ? 'block' : 'none';
    applyFilters();
  });

  DOM.clearSearchBtn.addEventListener('click', () => {
    DOM.searchInput.value = '';
    state.searchTerm = '';
    DOM.clearSearchBtn.style.display = 'none';
    applyFilters();
  });

  // Category filter click
  DOM.categoryChipsContainer.addEventListener('click', (e) => {
    const chip = e.target.closest('.chip');
    if (!chip) return;
    const cat = chip.dataset.category;
    state.selectedCategory = cat;

    DOM.categoryChipsContainer.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
    chip.classList.add('active');
    applyFilters();
  });

  // Script display mode toggles
  DOM.scriptModeGroup.addEventListener('click', (e) => {
    const btn = e.target.closest('.toggle-btn');
    if (!btn) return;
    state.scriptMode = btn.dataset.script;

    DOM.scriptModeGroup.querySelectorAll('.toggle-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    renderCurrentView();
  });

  // View mode toggles (table vs cards)
  DOM.viewModeGroup.addEventListener('click', (e) => {
    const btn = e.target.closest('.toggle-btn');
    if (!btn) return;
    state.viewMode = btn.dataset.view;

    DOM.viewModeGroup.querySelectorAll('.toggle-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    renderCurrentView();
  });

  // Column checkboxes
  DOM.columnCheckboxesContainer.addEventListener('change', (e) => {
    const checkbox = e.target;
    const col = checkbox.dataset.col;
    state.visibleCols[col] = checkbox.checked;
    renderCurrentView();
  });

  // Table header sorting
  DOM.dialectTable.querySelectorAll('th[data-sort]').forEach(th => {
    th.addEventListener('click', () => {
      const col = th.dataset.sort;
      if (state.sortColumn === col) {
        state.sortAsc = !state.sortAsc;
      } else {
        state.sortColumn = col;
        state.sortAsc = true;
      }

      // Update indicators
      DOM.dialectTable.querySelectorAll('.sort-indicator').forEach(ind => ind.textContent = '');
      th.querySelector('.sort-indicator').textContent = state.sortAsc ? '▲' : '▼';

      applyFilters();
    });
  });

  // Export filtered CSV
  DOM.downloadCsvBtn.addEventListener('click', exportFilteredCsv);

  // Modal controls
  DOM.closeModalBtn.addEventListener('click', closeModal);
  DOM.wordModal.addEventListener('click', (e) => {
    if (e.target === DOM.wordModal) closeModal();
  });

  // Copy JSON button
  DOM.copyJsonBtn.addEventListener('click', () => {
    if (!currentModalItem) return;
    navigator.clipboard.writeText(JSON.stringify(currentModalItem.raw, null, 2))
      .then(() => showToast('Copied JSON to clipboard!'))
      .catch(() => showToast('Failed to copy JSON.'));
  });

  // Navigation Tabs
  if (DOM.navTabExplorer && DOM.navTabProximity) {
    DOM.navTabExplorer.addEventListener('click', () => switchTab('explorer'));
    DOM.navTabProximity.addEventListener('click', () => switchTab('proximity'));
  }

  // Proximity View Controls
  if (DOM.proxSearchInput) {
    DOM.proxSearchInput.addEventListener('input', (e) => {
      state.proxSearch = e.target.value.toLowerCase().trim();
      renderConceptProximityGrid();
    });
  }

  if (DOM.proxCategorySelect) {
    DOM.proxCategorySelect.addEventListener('change', (e) => {
      state.proxCategory = e.target.value;
      renderConceptProximityGrid();
    });
  }

  if (DOM.proxSortSelect) {
    DOM.proxSortSelect.addEventListener('change', (e) => {
      state.proxSort = e.target.value;
      renderConceptProximityGrid();
    });
  }

  // Reset filters
  DOM.resetFiltersBtn.addEventListener('click', () => {
    DOM.searchInput.value = '';
    state.searchTerm = '';
    state.selectedCategory = 'ALL';
    DOM.clearSearchBtn.style.display = 'none';
    populateCategories();
    applyFilters();
  });
}

function switchTab(tabName) {
  state.activeTab = tabName;
  if (tabName === 'proximity') {
    DOM.navTabExplorer.classList.remove('active');
    DOM.navTabProximity.classList.add('active');
    DOM.tabContentExplorer.style.display = 'none';
    DOM.tabContentProximity.style.display = 'block';
    renderProximityView();
  } else {
    DOM.navTabProximity.classList.remove('active');
    DOM.navTabExplorer.classList.add('active');
    DOM.tabContentProximity.style.display = 'none';
    DOM.tabContentExplorer.style.display = 'block';
  }
  updateUrlParams();
}

// ==========================================
// Distance Algorithms & Proximity Logic
// ==========================================
function levenshteinDistance(s1, s2) {
  if (s1 === s2) return 0;
  if (!s1) return s2.length;
  if (!s2) return s1.length;
  const v0 = Array.from({ length: s2.length + 1 }, (_, i) => i);
  const v1 = new Array(s2.length + 1).fill(0);
  for (let i = 0; i < s1.length; i++) {
    v1[0] = i + 1;
    for (let j = 0; j < s2.length; j++) {
      const cost = s1[i] === s2[j] ? 0 : 1;
      v1[j + 1] = Math.min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost);
    }
    for (let j = 0; j <= s2.length; j++) v0[j] = v1[j];
  }
  return v0[s2.length];
}

function cleanWordToken(token) {
  if (!token) return '';
  let t = token.replace(/\(.*?\)/g, '');
  t = t.replace(/^[\s,?!.*"'[\]\-–—]+|[\s,?!.*"'[\]\-–—]+$/g, '');
  if (['-', '--', '---', 'N/A', 'n/a', '?', '???'].includes(t)) return '';
  return t.trim();
}

function parseWordList(cellValue) {
  if (!cellValue) return [];
  return cellValue.split('/')
    .map(cleanWordToken)
    .filter(w => w.length > 0);
}

function findBestMatch(wordsA, wordsB) {
  if (!wordsA || !wordsA.length || !wordsB || !wordsB.length) return null;
  let best = null;
  let minNorm = Infinity;
  let minRaw = Infinity;

  for (const wa of wordsA) {
    for (const wb of wordsB) {
      const waLower = wa.toLowerCase();
      const wbLower = wb.toLowerCase();
      const rawDist = levenshteinDistance(waLower, wbLower);
      const maxLen = Math.max(waLower.length, wbLower.length);
      const normDist = maxLen > 0 ? (rawDist / maxLen) : 0;
      const simPct = Math.round((1.0 - normDist) * 1000) / 10;

      if (normDist < minNorm || (normDist === minNorm && rawDist < minRaw)) {
        minNorm = normDist;
        minRaw = rawDist;
        best = {
          wordA: wa,
          wordB: wb,
          rawDist,
          normDist: Math.round(normDist * 10000) / 10000,
          simPct
        };
      }
    }
  }
  return best;
}

// All varieties to compare
const ALL_COMPARE_ENTITIES = [
  { key: 'male', label: "Male' (Std)", latinCol: "Male' - Latin", thaanaCol: "Male' - Thaana", color: 'var(--col-male)', isDhivehi: true },
  { key: 'addu', label: 'Addu', latinCol: 'Addu - Latin', thaanaCol: 'Addu - Thaana', color: 'var(--col-addu)', isDhivehi: true },
  { key: 'huvadhu', label: 'Huvadhu', latinCol: 'Huvadhu - Latin', thaanaCol: 'Huvadhu - Thaana', color: 'var(--col-huvadhu)', isDhivehi: true },
  { key: 'fuvahmulah', label: 'Fuvahmulah', latinCol: 'Fuvahmulah - Latin', thaanaCol: 'Fuvahmulah - Thaana', color: 'var(--col-fuvahmulah)', isDhivehi: true },
  { key: 'maliku', label: 'Maliku', latinCol: 'Maliku - Latin', thaanaCol: 'Maliku - Thaana', color: 'var(--col-maliku)', isDhivehi: true },
  { key: 'sinhala', label: 'Sinhala', latinCol: 'Sinhala', color: 'var(--col-sinhala)', isDhivehi: false },
  { key: 'malayalam', label: 'Malayalam', latinCol: 'Malayalam', color: 'var(--col-malayalam)', isDhivehi: false },
  { key: 'arabic', label: 'Arabic', latinCol: 'Arabic', color: 'var(--col-arabic)', isDhivehi: false },
];

function computeConceptProximity(item) {
  const maleWords = parseWordList(item.raw["Male' - Latin"]);
  const comparisons = [];
  let closestDhivehi = null;
  let maxDhivehiSim = -1;

  ALL_COMPARE_ENTITIES.forEach(entity => {
    if (entity.key === 'male') return;
    const targetWords = parseWordList(item.raw[entity.latinCol]);
    const match = findBestMatch(maleWords, targetWords);

    const comp = {
      entity,
      match,
      hasData: targetWords.length > 0,
    };
    comparisons.push(comp);

    if (entity.isDhivehi && match && match.simPct > maxDhivehiSim) {
      maxDhivehiSim = match.simPct;
      closestDhivehi = { entity, match };
    }
  });

  return {
    maleWords,
    comparisons,
    closestDhivehi,
    maxDhivehiSim: maxDhivehiSim >= 0 ? maxDhivehiSim : null
  };
}

// ==========================================
// Proximity View Rendering
// ==========================================
function renderProximityView() {
  populateProxCategories();
  renderProximityMacroMatrix();
  renderConceptProximityGrid();
}

function populateProxCategories() {
  if (!DOM.proxCategorySelect) return;
  const currentVal = state.proxCategory;
  const categories = Array.from(new Set(state.data.map(d => d.category).filter(Boolean))).sort();
  
  DOM.proxCategorySelect.innerHTML = `<option value="ALL">All Categories (${state.data.length})</option>` +
    categories.map(cat => {
      const count = state.data.filter(d => d.category === cat).length;
      return `<option value="${escapeHtml(cat)}"${cat === currentVal ? ' selected' : ''}>${escapeHtml(cat)} (${count})</option>`;
    }).join('');
}

function renderProximityMacroMatrix() {
  const accum = {};
  ALL_COMPARE_ENTITIES.forEach(e1 => {
    accum[e1.key] = {};
    ALL_COMPARE_ENTITIES.forEach(e2 => {
      accum[e1.key][e2.key] = { totalSim: 0, count: 0 };
    });
  });

  state.data.forEach(item => {
    ALL_COMPARE_ENTITIES.forEach(e1 => {
      const words1 = parseWordList(item.raw[e1.latinCol]);
      ALL_COMPARE_ENTITIES.forEach(e2 => {
        if (e1.key >= e2.key) return;
        const words2 = parseWordList(item.raw[e2.latinCol]);
        const match = findBestMatch(words1, words2);
        if (match) {
          accum[e1.key][e2.key].totalSim += match.simPct;
          accum[e1.key][e2.key].count += 1;

          accum[e2.key][e1.key].totalSim += match.simPct;
          accum[e2.key][e1.key].count += 1;
        }
      });
    });
  });

  // Render Highlight Cards
  const pairsToHighlight = [
    { a: 'male', b: 'addu', desc: 'Southernmost atoll; high phonological overlap with Standard Male\'' },
    { a: 'male', b: 'huvadhu', desc: 'Archaic morphology and unique vowel shifts' },
    { a: 'male', b: 'sinhala', desc: 'Close Indo-Aryan sibling language baseline' },
  ];

  if (DOM.proximitySummaryCards) {
    DOM.proximitySummaryCards.innerHTML = pairsToHighlight.map(p => {
      const entityA = ALL_COMPARE_ENTITIES.find(e => e.key === p.a);
      const entityB = ALL_COMPARE_ENTITIES.find(e => e.key === p.b);
      const cell = accum[p.a][p.b];
      const avgSim = cell.count > 0 ? (cell.totalSim / cell.count).toFixed(1) : '—';
      const fillPct = cell.count > 0 ? (cell.totalSim / cell.count) : 0;
      const color = fillPct >= 70 ? 'var(--accent-emerald)' : (fillPct >= 40 ? 'var(--accent-amber)' : 'var(--accent-rose)');

      return `
        <div class="proximity-summary-card">
          <div class="summary-card-header">
            <span class="summary-card-title">${entityA.label} ⟷ ${entityB.label}</span>
            <span class="badge badge-list">${cell.count} words</span>
          </div>
          <div class="summary-card-score">
            <span>${avgSim}${cell.count > 0 ? '%' : ''}</span>
            <small>similarity</small>
          </div>
          <div class="summary-card-bar-bg">
            <div class="summary-card-bar-fill" style="width:${fillPct}%; background:${color};"></div>
          </div>
          <p class="summary-card-desc">${p.desc}</p>
        </div>
      `;
    }).join('');
  }

  // Render Heatmap Matrix Table
  if (DOM.matrixTableContainer) {
    let tableHtml = `
      <table class="matrix-table">
        <thead>
          <tr>
            <th>Variety</th>
            ${ALL_COMPARE_ENTITIES.map(e => `<th>${escapeHtml(e.label)}</th>`).join('')}
          </tr>
        </thead>
        <tbody>
    `;

    ALL_COMPARE_ENTITIES.forEach(e1 => {
      tableHtml += `<tr><th>${escapeHtml(e1.label)}</th>`;
      ALL_COMPARE_ENTITIES.forEach(e2 => {
        if (e1.key === e2.key) {
          tableHtml += `<td class="matrix-cell cell-self">100%</td>`;
        } else {
          const cell = accum[e1.key][e2.key];
          if (cell.count > 0) {
            const avg = (cell.totalSim / cell.count).toFixed(1);
            const num = Number(avg);
            const cellClass = num >= 70 ? 'cell-high' : (num >= 40 ? 'cell-mid' : 'cell-low');
            tableHtml += `<td class="matrix-cell ${cellClass}" title="${e1.label} vs ${e2.label}: ${avg}% based on ${cell.count} words">${avg}% <small style="opacity:0.75; font-size:0.7rem;">(n=${cell.count})</small></td>`;
          } else {
            tableHtml += `<td class="matrix-cell cell-empty">—</td>`;
          }
        }
      });
      tableHtml += `</tr>`;
    });

    tableHtml += `</tbody></table>`;
    DOM.matrixTableContainer.innerHTML = tableHtml;
  }
}

function renderConceptProximityGrid() {
  if (!DOM.conceptProxGrid) return;

  const query = state.proxSearch;
  const cat = state.proxCategory;
  const sortMode = state.proxSort;

  // Filter items
  let items = state.data.filter(item => {
    if (cat !== 'ALL' && item.category !== cat) return false;
    if (query) {
      const text = `${item.id} ${item.english} ${item.category} ${item.maleLatin} ${item.maleThaana}`.toLowerCase();
      if (!text.includes(query)) return false;
    }
    return true;
  });

  // Calculate proximity info for items
  const processedItems = items.map(item => ({
    item,
    prox: computeConceptProximity(item)
  }));

  // Sort items
  processedItems.sort((a, b) => {
    if (sortMode === 'sim-desc') {
      const simA = a.prox.maxDhivehiSim ?? -1;
      const simB = b.prox.maxDhivehiSim ?? -1;
      return simB - simA;
    }
    if (sortMode === 'sim-asc') {
      const simA = a.prox.maxDhivehiSim ?? 999;
      const simB = b.prox.maxDhivehiSim ?? 999;
      return simA - simB;
    }
    if (sortMode === 'alpha-asc') {
      return a.item.english.localeCompare(b.item.english);
    }
    return a.item.id.localeCompare(b.item.id, undefined, { numeric: true });
  });

  if (DOM.proxResultsCount) {
    DOM.proxResultsCount.textContent = `Showing ${processedItems.length} concepts (${state.data.length} total in corpus)`;
  }

  if (processedItems.length === 0) {
    DOM.conceptProxGrid.innerHTML = `
      <div class="empty-state" style="grid-column: 1 / -1; padding: 3rem 1rem;">
        <div class="empty-icon">🔍</div>
        <h3>No matching concepts</h3>
        <p>Try searching for words like "big", "water", "bird", or change the category filter.</p>
      </div>
    `;
    return;
  }

  DOM.conceptProxGrid.innerHTML = processedItems.map(({ item, prox }) => {
    const maleLatin = item.maleLatin || '—';
    const maleThaana = item.maleThaana || '';

    // Champion badge
    let champHtml = '';
    if (prox.closestDhivehi && prox.closestDhivehi.match) {
      const cd = prox.closestDhivehi;
      champHtml = `
        <div class="cprox-champion-badge" title="Closest attested dialect for this concept">
          <span>🏆 Closest: <strong>${cd.entity.label}</strong> (${cd.match.simPct}% sim)</span>
        </div>
      `;
    }

    // Comparison Bars
    const barsHtml = prox.comparisons.map(c => {
      if (!c.hasData) {
        return `
          <div class="cprox-bar-item">
            <div class="cprox-bar-row">
              <span class="cprox-dialect-name"><span class="dialect-dot" style="background:${c.entity.color}"></span>${c.entity.label}</span>
              <span class="cprox-awaiting-badge">Awaiting field data</span>
            </div>
          </div>
        `;
      }

      const match = c.match;
      if (!match) return '';

      const sim = match.simPct;
      let fillClass = 'fill-rose';
      if (sim >= 80) fillClass = 'fill-green';
      else if (sim >= 50) fillClass = 'fill-yellow';
      else if (sim >= 25) fillClass = 'fill-orange';

      const editLabel = match.rawDist === 0 ? 'Exact match' : `${match.rawDist} edit${match.rawDist > 1 ? 's' : ''}`;

      return `
        <div class="cprox-bar-item">
          <div class="cprox-bar-row">
            <span class="cprox-dialect-name"><span class="dialect-dot" style="background:${c.entity.color}"></span>${c.entity.label} <span class="cprox-word-matched">(${escapeHtml(match.wordB)})</span></span>
            <span class="cprox-score-badge" title="${editLabel}">${sim}%</span>
          </div>
          <div class="cprox-progress-track">
            <div class="cprox-progress-fill ${fillClass}" style="width:${sim}%;"></div>
          </div>
        </div>
      `;
    }).join('');

    return `
      <div class="concept-prox-card" onclick="window.appOpenModal('${escapeHtml(item.id)}')">
        <div class="cprox-header">
          <div>
            <h3 class="cprox-concept-title">${escapeHtml(item.english)}</h3>
            <div class="cprox-meta">
              <span class="badge badge-id">${escapeHtml(item.id)}</span>
              <span class="badge badge-category">${escapeHtml(item.category)}</span>
            </div>
          </div>
        </div>

        <div class="cprox-anchor">
          <span class="cprox-anchor-label">Standard Anchor (Male')</span>
          <div class="cprox-anchor-words">
            <span class="cprox-anchor-latin">${escapeHtml(maleLatin)}</span>
            ${maleThaana ? `<span class="cprox-anchor-thaana">${escapeHtml(maleThaana)}</span>` : ''}
          </div>
        </div>

        ${champHtml}

        <div class="cprox-bars-list">
          ${barsHtml}
        </div>
      </div>
    `;
  }).join('');
}

function applyTheme(theme) {
  state.theme = theme;
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('theme', theme);
}

function exportFilteredCsv() {
  if (state.filteredData.length === 0) {
    showToast('No data to export.');
    return;
  }

  const rawRows = state.filteredData.map(d => d.raw);
  const csvString = Papa.unparse(rawRows);
  const blob = new Blob([csvString], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.setAttribute('href', url);
  link.setAttribute('download', `dhivehi_dialect_export_${new Date().toISOString().slice(0,10)}.csv`);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  showToast(`Exported ${rawRows.length} concepts as CSV!`);
}

function showToast(message) {
  DOM.toast.textContent = message;
  DOM.toast.classList.add('show');
  setTimeout(() => {
    DOM.toast.classList.remove('show');
  }, 2500);
}

function updateUrlParams() {
  const url = new URL(window.location);
  if (state.activeTab && state.activeTab !== 'explorer') {
    url.searchParams.set('tab', state.activeTab);
  } else {
    url.searchParams.delete('tab');
  }

  if (state.searchTerm) {
    url.searchParams.set('search', state.searchTerm);
  } else {
    url.searchParams.delete('search');
  }

  if (state.selectedCategory !== 'ALL') {
    url.searchParams.set('category', state.selectedCategory);
  } else {
    url.searchParams.delete('category');
  }

  window.history.replaceState({}, '', url);
}

function loadUrlParams() {
  const params = new URLSearchParams(window.location.search);
  const tab = params.get('tab');
  const search = params.get('search');
  const cat = params.get('category');

  if (tab === 'proximity') {
    state.activeTab = 'proximity';
    switchTab('proximity');
  }
  if (search) {
    state.searchTerm = search;
    DOM.searchInput.value = search;
    DOM.clearSearchBtn.style.display = 'block';
  }
  if (cat) {
    state.selectedCategory = cat;
  }
}

function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

// Start application when DOM is ready
document.addEventListener('DOMContentLoaded', initApp);
