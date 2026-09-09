/**
 * Studio ML Python - Main Application Controller
 */
const App = {
  state: {
    activeTab: 'tab-automl',
    currentDataset: 'titanic',
    targetColumn: 'Survived',
    taskType: 'classification',
    analysis: null,
    recommendations: null,
    selectedModelId: 'random_forest',
    activeModelResult: null,
    automlResult: null,
    projects: []
  },

  init() {
    this.bindNavigation();
    this.bindDataWrangler();
    this.bindModelSelection();
    this.bindTrainingEvents();
    this.bindCodeEvents();
    this.bindProjectEvents();
    this.bindSettingsModal();
    
    AICopilot.init();
    
    // Initial load default dataset
    this.loadDataset('titanic');
    this.refreshProjectList();
  },

  // ==================== NAVIGATION TABS & MOBILE DRAWER ====================
  bindNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
      item.addEventListener('click', (e) => {
        const tabId = e.currentTarget.getAttribute('data-tab');
        this.switchTab(tabId);
      });
    });

    // Mobile bottom navigation items
    const mobileNavBtns = document.querySelectorAll('.mobile-nav-btn[data-tab]');
    mobileNavBtns.forEach(btn => {
      btn.addEventListener('click', (e) => {
        const tabId = e.currentTarget.getAttribute('data-tab');
        this.switchTab(tabId);
      });
    });

    // Mobile drawer toggle & close
    const sidebar = document.querySelector('.sidebar');
    const backdrop = document.getElementById('sidebar-backdrop');
    const toggleBtn = document.getElementById('btn-toggle-sidebar');
    const closeBtn = document.getElementById('btn-close-sidebar');
    const moreBtn = document.getElementById('mob-nav-more');

    const openSidebar = () => {
      if (sidebar) sidebar.classList.add('open');
      if (backdrop) backdrop.classList.add('active');
    };

    const closeSidebar = () => {
      if (sidebar) sidebar.classList.remove('open');
      if (backdrop) backdrop.classList.remove('active');
    };

    if (toggleBtn) toggleBtn.addEventListener('click', openSidebar);
    if (moreBtn) moreBtn.addEventListener('click', openSidebar);
    if (closeBtn) closeBtn.addEventListener('click', closeSidebar);
    if (backdrop) backdrop.addEventListener('click', closeSidebar);
  },

  switchTab(tabId) {
    this.state.activeTab = tabId;

    // Close mobile drawer if open
    const sidebar = document.querySelector('.sidebar');
    const backdrop = document.getElementById('sidebar-backdrop');
    if (sidebar) sidebar.classList.remove('open');
    if (backdrop) backdrop.classList.remove('active');

    // Update active class on sidebar nav
    document.querySelectorAll('.nav-item').forEach(item => {
      if (item.getAttribute('data-tab') === tabId) {
        item.classList.add('active');
      } else {
        item.classList.remove('active');
      }
    });

    // Update active class on mobile bottom nav
    document.querySelectorAll('.mobile-nav-btn[data-tab]').forEach(btn => {
      if (btn.getAttribute('data-tab') === tabId) {
        btn.classList.add('active');
      } else {
        btn.classList.remove('active');
      }
    });

    // Show active tab view
    document.querySelectorAll('.tab-view').forEach(view => {
      if (view.id === tabId) {
        view.classList.remove('hidden');
      } else {
        view.classList.add('hidden');
      }
    });

    // Update page title
    const titles = {
      'tab-automl': '🚀 Coba Langsung (AutoML 1-Klik)',
      'tab-data': '📊 Kelola & Bersihkan Data',
      'tab-models': '🧠 Pilih & Atur Model ML',
      'tab-eval': '📈 Evaluasi Hasil & Prediksi Live',
      'tab-ai': '🎓 AI Tutor SMK — Belajar Python, ML & Jobsheet PRD',
      'tab-elearning': '📝 E-Learning & Ujian CBT Siswa SMK',
      'tab-projects': '💾 Simpan & Kelola Proyek',
      'tab-code': '🐍 Generator Kode Python'
    };
    const titleEl = document.getElementById('top-page-title');
    if (titleEl && titles[tabId]) {
      titleEl.innerText = titles[tabId];
    }

    // Refresh elearning if navigated
    if (tabId === 'tab-elearning' && typeof ELearning !== 'undefined') {
      ELearning.loadLobbyExams();
    }

    // Refresh code tab if navigated to code
    if (tabId === 'tab-code') {
      this.refreshPythonCode();
    }
  },

  // ==================== DATASET HANDLING ====================
  async loadDataset(datasetId) {
    this.showToast(`Memuat dataset ${datasetId}...`, "info");
    try {
      const res = await API.loadDataset(datasetId);
      if (res.success) {
        this.state.currentDataset = datasetId;
        this.state.targetColumn = res.default_target;
        this.state.analysis = res.analysis;

        this.updateTopBarBadge(datasetId);
        this.renderDataOverview(res.analysis, res.table_preview);
        this.populateColumnSelectors(res.analysis.columns, res.default_target);
        
        // Fetch recommendations
        await this.fetchRecommendations(res.default_target);

        this.showToast(`Dataset ${datasetId} berhasil dimuat!`, "success");
      }
    } catch (e) {
      this.showToast(`Gagal memuat dataset: ${e.message}`, "error");
    }
  },

  updateTopBarBadge(name) {
    const el = document.getElementById('badge-active-dataset');
    if (el) {
      el.innerText = `📂 ${name}`;
    }
  },

  populateColumnSelectors(columns, defaultTarget) {
    const selects = [
      document.getElementById('quick-target-select'),
      document.getElementById('data-target-select'),
      document.getElementById('model-target-select')
    ];

    selects.forEach(sel => {
      if (!sel) return;
      sel.innerHTML = '';
      columns.forEach(c => {
        const opt = document.createElement('option');
        opt.value = c.name;
        opt.innerText = `${c.name} (${c.type})`;
        if (c.name === defaultTarget) {
          opt.selected = true;
        }
        sel.appendChild(opt);
      });
    });
  },

  renderDataOverview(analysis, previewRows) {
    // Stat counters
    const elRows = document.getElementById('stat-total-rows');
    const elCols = document.getElementById('stat-total-cols');
    const elDups = document.getElementById('stat-dup-rows');

    if (elRows) elRows.innerText = analysis.total_rows.toLocaleString();
    if (elCols) elCols.innerText = analysis.total_cols;
    if (elDups) elDups.innerText = analysis.duplicate_rows;

    // Table preview
    const tableEl = document.getElementById('preview-data-table');
    if (tableEl && previewRows && previewRows.length > 0) {
      const cols = Object.keys(previewRows[0]);
      let html = `<thead><tr>${cols.map(c => `<th>${c}</th>`).join('')}</tr></thead><tbody>`;
      previewRows.forEach(r => {
        html += `<tr>${cols.map(c => `<td>${r[c]}</td>`).join('')}</tr>`;
      });
      html += `</tbody>`;
      tableEl.innerHTML = html;
    }

    // Column list in Data Tab
    const colListContainer = document.getElementById('columns-summary-list');
    if (colListContainer) {
      let colHtml = '';
      analysis.columns.forEach(c => {
        const isMiss = c.missing_count > 0;
        colHtml += `
          <div style="background: #ffffff; padding: 12px; border-radius: 8px; border: 1px solid var(--border-subtle); display: flex; justify-content: space-between; align-items: center; box-shadow: var(--shadow-sm);">
            <div>
              <div style="font-weight: 700; font-size: 0.9rem; color: var(--text-main);">${c.name}</div>
              <div style="font-size: 0.75rem; color: var(--text-muted);">Tipe: <b style="color: var(--accent-primary-hover);">${c.type}</b> | Nilai Unik: ${c.unique_count}</div>
            </div>
            <div>
              ${isMiss ? `<span class="nav-tag" style="background: #fef2f2; color: #dc2626; border: 1px solid #fecaca;">${c.missing_count} Kosong (${c.missing_pct}%)</span>` : `<span class="nav-tag green">100% Lengkap</span>`}
            </div>
          </div>
        `;
      });
      colListContainer.innerHTML = colHtml;
    }
  },

  bindDataWrangler() {
    // Sample dataset dropdown quick-change
    const sampleSelect = document.getElementById('quick-dataset-select');
    if (sampleSelect) {
      sampleSelect.addEventListener('change', (e) => {
        this.loadDataset(e.target.value);
      });
    }

    // Target column quick change
    const targetSelect = document.getElementById('quick-target-select');
    if (targetSelect) {
      targetSelect.addEventListener('change', (e) => {
        this.state.targetColumn = e.target.value;
        this.fetchRecommendations(e.target.value);
      });
    }

    // Upload zone
    const dropzone = document.getElementById('upload-dropzone');
    const fileInput = document.getElementById('file-upload-input');

    if (dropzone && fileInput) {
      dropzone.addEventListener('click', () => fileInput.click());
      fileInput.addEventListener('change', async (e) => {
        if (e.target.files.length > 0) {
          const file = e.target.files[0];
          this.showToast(`Mengunggah file ${file.name}...`, "info");
          try {
            const res = await API.uploadDataset(file);
            if (res.success) {
              this.state.currentDataset = res.dataset_name;
              this.state.targetColumn = res.default_target;
              this.state.analysis = res.analysis;

              this.updateTopBarBadge(res.dataset_name);
              this.renderDataOverview(res.analysis, res.table_preview);
              this.populateColumnSelectors(res.analysis.columns, res.default_target);
              await this.fetchRecommendations(res.default_target);

              this.showToast(`File ${file.name} berhasil diunggah!`, "success");
            }
          } catch (err) {
            this.showToast(`Gagal mengunggah: ${err.message}`, "error");
          }
        }
      });
    }

    // Clean data button
    const btnClean = document.getElementById('btn-apply-cleaning');
    if (btnClean) {
      btnClean.addEventListener('click', async () => {
        const numStrat = document.getElementById('clean-num-strategy').value;
        const catStrat = document.getElementById('clean-cat-strategy').value;
        const dropDups = document.getElementById('clean-drop-duplicates').checked;

        this.showToast("Membersihkan data...", "info");
        try {
          const res = await API.cleanDataset({
            missing_numeric: numStrat,
            missing_categorical: catStrat,
            drop_duplicates: dropDups
          });
          if (res.success) {
            this.state.analysis = res.analysis;
            this.renderDataOverview(res.analysis, res.table_preview);
            this.showToast(res.message, "success");
          }
        } catch (e) {
          this.showToast(`Pembersihan gagal: ${e.message}`, "error");
        }
      });
    }
  },

  // ==================== RECOMMENDATIONS & MODEL CARDS ====================
  async fetchRecommendations(targetColumn) {
    try {
      const res = await API.getRecommendations(targetColumn);
      if (res.success) {
        this.state.taskType = res.task_type;
        this.state.recommendations = res.recommendations;

        // Render Recommendation Box in AutoML & Model Tab
        this.renderRecommendationBox(res.recommendations);
        this.renderModelCards(res.recommendations.all_models);

        // Update task type pill
        const taskPill = document.getElementById('task-type-badge');
        if (taskPill) {
          taskPill.innerText = res.task_type === 'classification' ? '🎯 Klasifikasi' : '📈 Regresi';
        }
      }
    } catch (e) {
      console.error("Gagal mendapatkan rekomendasi:", e);
    }
  },

  renderRecommendationBox(recom) {
    const box = document.getElementById('recom-explanation-box');
    if (!box || !recom) return;

    box.innerHTML = `
      <div style="display: flex; gap: 14px; align-items: flex-start;">
        <div style="font-size: 2rem;">💡</div>
        <div>
          <div style="font-weight: 700; font-size: 0.95rem; color: var(--text-main); margin-bottom: 4px;">
            Rekomendasi Utama: <span style="color: #047857; font-weight: 800;">${recom.primary_recommendation.model_id.replace(/_/g, ' ').toUpperCase()}</span>
          </div>
          <p style="font-size: 0.82rem; color: var(--text-muted); line-height: 1.5;">
            ${recom.primary_recommendation.reason}
          </p>
          <div style="font-size: 0.78rem; color: var(--text-dim); margin-top: 6px;">
            Alternatif: <b>${recom.alternative_recommendation.model_id.replace(/_/g, ' ')}</b> — ${recom.alternative_recommendation.reason}
          </div>
        </div>
      </div>
    `;
  },

  renderModelCards(models) {
    const container = document.getElementById('models-cards-container');
    if (!container || !models) return;

    let html = '';
    models.forEach(m => {
      const isSelected = (m.id === this.state.selectedModelId);
      html += `
        <div class="model-card ${isSelected ? 'selected' : ''}" data-model-id="${m.id}">
          <div class="model-card-top">
            <div class="model-card-icon">${m.icon}</div>
            <div class="model-card-badge">${m.badge}</div>
          </div>
          <div class="model-card-title">${m.name}</div>
          <div class="model-card-desc">${m.description}</div>
          <div style="margin-top: auto; display: flex; align-items: center; justify-content: space-between;">
            <span style="font-size: 0.72rem; color: var(--text-dim);">Tipe: ${this.state.taskType}</span>
            <button class="btn btn-sm ${isSelected ? 'btn-primary' : 'btn-secondary'} btn-select-model" data-id="${m.id}">
              ${isSelected ? '✓ Terpilih' : 'Pilih Model'}
            </button>
          </div>
        </div>
      `;
    });
    container.innerHTML = html;

    // Attach click handlers
    container.querySelectorAll('.model-card').forEach(card => {
      card.addEventListener('click', (e) => {
        const id = card.getAttribute('data-model-id');
        this.selectModel(id);
      });
    });

    // Populate Hyperparameter Panel for selected model
    this.renderHyperparametersPanel();
  },

  selectModel(modelId) {
    this.state.selectedModelId = modelId;
    document.querySelectorAll('.model-card').forEach(c => {
      if (c.getAttribute('data-model-id') === modelId) {
        c.classList.add('selected');
        c.querySelector('.btn-select-model').innerText = '✓ Terpilih';
        c.querySelector('.btn-select-model').className = 'btn btn-sm btn-primary btn-select-model';
      } else {
        c.classList.remove('selected');
        c.querySelector('.btn-select-model').innerText = 'Pilih Model';
        c.querySelector('.btn-select-model').className = 'btn btn-sm btn-secondary btn-select-model';
      }
    });

    this.renderHyperparametersPanel();
  },

  renderHyperparametersPanel() {
    const container = document.getElementById('hyperparam-controls-container');
    if (!container || !this.state.recommendations) return;

    const all = this.state.recommendations.all_models || [];
    const model = all.find(m => m.id === this.state.selectedModelId) || all[0];
    if (!model || !model.params) return;

    let html = `
      <div style="margin-bottom: 12px; font-weight: 700; font-size: 0.95rem; color: var(--text-main); display: flex; align-items: center; gap: 8px;">
        <span>${model.icon}</span> ${model.name}
      </div>
    `;

    for (const [key, schema] of Object.entries(model.params)) {
      if (schema.type === 'int' || schema.type === 'float') {
        html += `
          <div class="hyperparam-group">
            <div class="hyperparam-header">
              <span>${schema.label || key}</span>
              <span id="val-${key}" style="font-family: var(--font-mono); color: var(--accent-primary-hover); font-weight: 600;">${schema.default}</span>
            </div>
            <input type="range" class="app-slider hyper-slider" data-key="${key}" min="${schema.min}" max="${schema.max}" step="${schema.step}" value="${schema.default}" oninput="document.getElementById('val-${key}').innerText = this.value" />
          </div>
        `;
      } else if (schema.type === 'choice') {
        html += `
          <div class="hyperparam-group">
            <div class="hyperparam-header"><span>${schema.label || key}</span></div>
            <select class="app-select hyper-select" data-key="${key}" style="width: 100%;">
              ${schema.options.map(opt => `<option value="${opt}" ${opt === schema.default ? 'selected' : ''}>${opt}</option>`).join('')}
            </select>
          </div>
        `;
      }
    }
    container.innerHTML = html;
  },

  getHyperparameters() {
    const params = {};
    document.querySelectorAll('.hyper-slider').forEach(input => {
      params[input.getAttribute('data-key')] = input.value;
    });
    document.querySelectorAll('.hyper-select').forEach(sel => {
      params[sel.getAttribute('data-key')] = sel.value;
    });
    return params;
  },

  bindModelSelection() {
    // Model search / filter if needed
  },

  // ==================== TRAINING & AUTOML ====================
  bindTrainingEvents() {
    // 1-Click AutoML Button
    const btnAutoML = document.getElementById('btn-run-automl');
    if (btnAutoML) {
      btnAutoML.addEventListener('click', () => this.runAutoML());
    }

    // Manual Train Single Model Button
    const btnTrainSingle = document.getElementById('btn-train-single-model');
    if (btnTrainSingle) {
      btnTrainSingle.addEventListener('click', () => this.trainSingle());
    }
  },

  async runAutoML() {
    const targetCol = document.getElementById('quick-target-select').value;
    const testSize = parseFloat(document.getElementById('quick-split-ratio').value) || 0.2;

    const btn = document.getElementById('btn-run-automl');
    btn.disabled = true;
    btn.innerHTML = `<span class="pulse-loader"></span> Melatih Semua Model...`;

    this.showToast("Menjalankan AutoML... Menguji dan membandingkan seluruh model!", "info");

    try {
      const res = await API.trainAutoML(targetCol, testSize);
      btn.disabled = false;
      btn.innerHTML = `⚡ Mulai Belajar Mandiri (AutoML)`;

      if (res.success) {
        this.state.automlResult = res;
        this.renderAutoMLLeaderboard(res.leaderboard, res.winner);
        this.showToast(`AutoML Selesai! Model Pemenang: ${res.winner.model_name} (${res.winner.score_display})`, "success");

        // Switch to Evaluation Tab to show deep insights
        setTimeout(() => {
          this.switchTab('tab-eval');
          this.renderEvaluationResults(res.winner.metrics, res.winner.model_name, res.winner.feature_importance);
        }, 1200);
      }
    } catch (e) {
      btn.disabled = false;
      btn.innerHTML = `⚡ Mulai Belajar Mandiri (AutoML)`;
      this.showToast(`AutoML gagal: ${e.message}`, "error");
    }
  },

  async trainSingle() {
    const targetCol = document.getElementById('model-target-select').value;
    const testSize = parseFloat(document.getElementById('model-split-ratio').value) || 0.2;
    const params = this.getHyperparameters();
    const modelId = this.state.selectedModelId;

    const btn = document.getElementById('btn-train-single-model');
    btn.disabled = true;
    btn.innerHTML = `<span class="pulse-loader"></span> Melatih Model...`;

    this.showToast(`Melatih model ${modelId}...`, "info");

    try {
      const res = await API.trainSingleModel(modelId, targetCol, params, testSize);
      btn.disabled = false;
      btn.innerHTML = `🚀 Latih Model Ini Sekarang`;

      if (res.success) {
        this.state.activeModelResult = res.result;
        this.showToast(`Pelatihan ${res.result.model_name} Sukses! Skor: ${res.result.metrics.score_display}`, "success");

        // Switch to evaluation
        this.switchTab('tab-eval');
        this.renderEvaluationResults(res.result.metrics, res.result.model_name, res.result.feature_importance);
      }
    } catch (e) {
      btn.disabled = false;
      btn.innerHTML = `🚀 Latih Model Ini Sekarang`;
      this.showToast(`Pelatihan gagal: ${e.message}`, "error");
    }
  },

  renderAutoMLLeaderboard(leaderboard, winner) {
    const container = document.getElementById('automl-leaderboard-container');
    if (!container || !leaderboard) return;

    let html = '';
    leaderboard.forEach(item => {
      const isWinner = item.is_winner;
      html += `
        <div class="leaderboard-item ${isWinner ? 'winner' : ''}">
          <div class="rank-badge">${isWinner ? '🏆' : '#' + item.rank}</div>
          <div class="model-info-col">
            <div class="model-name-row">
              <span>${item.model_name}</span>
              ${isWinner ? '<span class="winner-crown">★ Model Terbaik (Winner)</span>' : ''}
            </div>
            <div style="font-size: 0.76rem; color: var(--text-dim); margin-top: 2px;">
              Waktu Latih: ${item.duration}s | Metrik: ${item.metric_name}
            </div>
          </div>
          <div class="metric-pill-large">
            ${item.score_display}
          </div>
        </div>
      `;
    });
    container.innerHTML = html;

    // Leaderboard visual bar
    Charts.renderLeaderboardBar('automl-leaderboard-chart', leaderboard);
  },

  renderEvaluationResults(metrics, modelName, featureImportance) {
    // Model name header
    const nameEl = document.getElementById('eval-active-model-name');
    if (nameEl) nameEl.innerText = modelName;

    // Primary score
    const scoreValEl = document.getElementById('eval-primary-score-val');
    const scoreNameEl = document.getElementById('eval-primary-score-name');
    if (scoreValEl && scoreNameEl) {
      scoreValEl.innerText = metrics.score_display;
      scoreNameEl.innerText = metrics.primary_metric_name;
    }

    // Specific metrics for Classification vs Regression
    const classContainer = document.getElementById('eval-classification-metrics');
    const regContainer = document.getElementById('eval-regression-metrics');

    if (this.state.taskType === 'classification') {
      if (classContainer) classContainer.classList.remove('hidden');
      if (regContainer) regContainer.classList.add('hidden');

      document.getElementById('metric-accuracy-val').innerText = `${metrics.accuracy}%`;
      document.getElementById('metric-precision-val').innerText = `${metrics.precision}%`;
      document.getElementById('metric-recall-val').innerText = `${metrics.recall}%`;
      document.getElementById('metric-f1-val').innerText = `${metrics.f1_score}%`;

      // Render Confusion Matrix
      if (metrics.confusion_matrix) {
        Charts.renderConfusionMatrix('confusion-matrix-container', metrics.confusion_matrix);
      }
    } else {
      if (classContainer) classContainer.classList.add('hidden');
      if (regContainer) regContainer.classList.remove('hidden');

      document.getElementById('metric-r2-val').innerText = metrics.r2_score;
      document.getElementById('metric-rmse-val').innerText = metrics.rmse;
      document.getElementById('metric-mae-val').innerText = metrics.mae;

      // Render Sample predictions
      const sampleContainer = document.getElementById('reg-sample-predictions-table');
      if (sampleContainer && metrics.sample_predictions) {
        let rows = metrics.sample_predictions.map(s => `
          <tr>
            <td>${s.actual}</td>
            <td style="color: var(--accent-emerald); font-weight: 600;">${s.predicted}</td>
            <td style="color: var(--text-dim);">${s.diff}</td>
          </tr>
        `).join('');
        sampleContainer.innerHTML = rows;
      }
    }

    // Render Feature Importance
    Charts.renderFeatureImportance('feature-importance-container', featureImportance);

    // Build Live Prediction Form
    this.buildLivePredictionForm();
  },

  buildLivePredictionForm() {
    const container = document.getElementById('live-prediction-inputs');
    if (!container || !this.state.analysis) return;

    let html = '';
    const target = this.state.targetColumn;
    const features = this.state.analysis.columns.filter(c => c.name !== target);

    features.forEach(f => {
      if (f.type === 'numeric') {
        const defVal = f.stats ? f.stats.median : 0;
        html += `
          <div style="display: flex; flex-direction: column; gap: 4px;">
            <label style="font-size: 0.78rem; font-weight: 600; color: var(--text-muted);">${f.name}</label>
            <input type="number" step="any" class="app-input live-pred-input" data-col="${f.name}" value="${defVal}" />
          </div>
        `;
      } else {
        const topOpts = f.top_values ? Object.keys(f.top_values) : ['Sample'];
        html += `
          <div style="display: flex; flex-direction: column; gap: 4px;">
            <label style="font-size: 0.78rem; font-weight: 600; color: var(--text-muted);">${f.name}</label>
            <select class="app-select live-pred-input" data-col="${f.name}">
              ${topOpts.map(o => `<option value="${o}">${o}</option>`).join('')}
            </select>
          </div>
        `;
      }
    });

    container.innerHTML = html;

    // Attach Predict button listener
    const btnPredict = document.getElementById('btn-run-live-predict');
    if (btnPredict) {
      btnPredict.onclick = () => this.runLivePrediction();
    }
  },

  async runLivePrediction() {
    const inputValues = {};
    document.querySelectorAll('.live-pred-input').forEach(input => {
      inputValues[input.getAttribute('data-col')] = input.value;
    });

    try {
      const res = await API.predict(inputValues);
      if (res.success) {
        const resultValEl = document.getElementById('live-pred-result-val');
        const probContainer = document.getElementById('live-pred-probabilities');

        if (resultValEl) {
          resultValEl.innerText = res.prediction;
        }

        if (probContainer) {
          if (res.probabilities && Object.keys(res.probabilities).length > 0) {
            let probHtml = '<div style="font-size: 0.78rem; color: var(--text-dim); margin-bottom: 6px;">Probabilitas Keyakinan Model:</div>';
            for (const [cls, prob] of Object.entries(res.probabilities)) {
              probHtml += `
                <div style="display: flex; align-items: center; justify-content: space-between; font-size: 0.8rem; margin-bottom: 4px;">
                  <span>${cls}</span>
                  <span style="font-weight: 700; color: #059669;">${prob}%</span>
                </div>
              `;
            }
            probContainer.innerHTML = probHtml;
          } else {
            probContainer.innerHTML = '';
          }
        }

        this.showToast("Prediksi berhasil dijalankan!", "success");
      }
    } catch (e) {
      this.showToast(`Gagal memprediksi: ${e.message}`, "error");
    }
  },

  // ==================== CODE GENERATOR ====================
  bindCodeEvents() {
    const btnCopy = document.getElementById('btn-copy-code');
    if (btnCopy) {
      btnCopy.addEventListener('click', () => {
        const codeText = document.getElementById('python-code-display').innerText;
        navigator.clipboard.writeText(codeText);
        this.showToast("Kode Python berhasil disalin ke clipboard!", "success");
      });
    }

    const btnDownload = document.getElementById('btn-download-code');
    if (btnDownload) {
      btnDownload.addEventListener('click', () => {
        window.location.href = '/api/code/download';
      });
    }
  },

  async refreshPythonCode() {
    try {
      const res = await API.getPythonCode();
      if (res.success) {
        const el = document.getElementById('python-code-display');
        if (el) el.innerText = res.script;
      }
    } catch (e) {
      console.error("Gagal memuat kode:", e);
    }
  },

  // ==================== PROJECT STORAGE ====================
  bindProjectEvents() {
    const btnSave = document.getElementById('btn-save-project-modal');
    if (btnSave) {
      btnSave.addEventListener('click', () => {
        document.getElementById('modal-save-project').classList.add('open');
      });
    }

    const btnConfirmSave = document.getElementById('btn-confirm-save-project');
    if (btnConfirmSave) {
      btnConfirmSave.addEventListener('click', async () => {
        const name = document.getElementById('input-project-name').value.trim() || `Proyek ML ${this.state.currentDataset}`;
        const desc = document.getElementById('input-project-desc').value.trim() || 'Eksperimen Studio ML';
        
        try {
          const res = await API.saveProject(name, desc);
          document.getElementById('modal-save-project').classList.remove('open');
          if (res.success) {
            this.showToast(res.message, "success");
            this.refreshProjectList();
          }
        } catch (e) {
          this.showToast(`Gagal menyimpan proyek: ${e.message}`, "error");
        }
      });
    }
  },

  async refreshProjectList() {
    try {
      const res = await API.getProjects();
      if (res.success) {
        this.state.projects = res.projects;
        this.renderProjectsList(res.projects);
      }
    } catch (e) {
      console.error("Gagal memuat proyek:", e);
    }
  },

  renderProjectsList(projects) {
    const container = document.getElementById('projects-table-tbody');
    if (!container) return;

    if (!projects || projects.length === 0) {
      container.innerHTML = `<tr><td colspan="6" style="text-align: center; color: var(--text-dim); padding: 24px;">Belum ada proyek tersimpan. Klik "Simpan Proyek Ini" untuk menyimpan eksperimen.</td></tr>`;
      return;
    }

    let html = '';
    projects.forEach(p => {
      html += `
        <tr>
          <td><b style="color: var(--text-main);">${p.name}</b><br/><span style="font-size: 0.72rem; color: var(--text-dim);">${p.description || ''}</span></td>
          <td>${p.dataset_name}</td>
          <td><span class="nav-tag">${p.task_type}</span></td>
          <td>${p.target_column}</td>
          <td>${p.created_at}</td>
          <td>
            <button class="btn btn-sm btn-secondary" onclick="App.deleteProject(${p.id})">Hapus</button>
          </td>
        </tr>
      `;
    });
    container.innerHTML = html;
  },

  async deleteProject(id) {
    if (confirm("Apakah Anda yakin ingin menghapus proyek ini?")) {
      try {
        const res = await API.deleteProject(id);
        if (res.success) {
          this.showToast(res.message, "success");
          this.refreshProjectList();
        }
      } catch (e) {
        this.showToast(`Gagal menghapus: ${e.message}`, "error");
      }
    }
  },

  // ==================== SETTINGS MODAL ====================
  bindSettingsModal() {
    const btnOpenSettings = document.getElementById('btn-open-settings');
    const modalSettings = document.getElementById('modal-settings');
    const btnSaveSettings = document.getElementById('btn-save-settings');
    const btnTestGemini = document.getElementById('btn-test-gemini');
    const testResultBox = document.getElementById('gemini-test-result');

    this.updateProviderBadge();

    if (btnOpenSettings && modalSettings) {
      btnOpenSettings.addEventListener('click', () => {
        document.getElementById('settings-ai-key').value = localStorage.getItem('studio_ml_ai_key') || '';
        document.getElementById('settings-ai-provider').value = localStorage.getItem('studio_ml_ai_provider') || 'local';
        if (testResultBox) {
          testResultBox.style.display = 'none';
        }
        modalSettings.classList.add('open');
      });
    }

    if (btnTestGemini) {
      btnTestGemini.addEventListener('click', async () => {
        const key = document.getElementById('settings-ai-key').value.trim();
        if (!key) {
          if (testResultBox) {
            testResultBox.style.display = 'block';
            testResultBox.style.background = '#fef2f2';
            testResultBox.style.border = '1px solid #fecaca';
            testResultBox.style.color = '#dc2626';
            testResultBox.innerHTML = '⚠️ Masukkan API Key terlebih dahulu.';
          }
          return;
        }

        btnTestGemini.disabled = true;
        btnTestGemini.innerText = '⏳ Menguji...';
        if (testResultBox) {
          testResultBox.style.display = 'block';
          testResultBox.style.background = '#f8fafc';
          testResultBox.style.border = '1px solid #e2e8f0';
          testResultBox.style.color = '#64748b';
          testResultBox.innerHTML = 'Menghubungi server Google Gemini API...';
        }

        try {
          const res = await API.testGemini(key);
          btnTestGemini.disabled = false;
          btnTestGemini.innerText = '🔌 Uji Koneksi';

          if (res.success) {
            testResultBox.style.background = '#ecfdf5';
            testResultBox.style.border = '1px solid #a7f3d0';
            testResultBox.style.color = '#047857';
            testResultBox.innerHTML = `<b>✓ Terhubung!</b> ${res.message}`;
          } else {
            testResultBox.style.background = '#fef2f2';
            testResultBox.style.border = '1px solid #fecaca';
            testResultBox.style.color = '#dc2626';
            testResultBox.innerHTML = `<b>✕ Gagal:</b> ${res.error}`;
          }
        } catch (e) {
          btnTestGemini.disabled = false;
          btnTestGemini.innerText = '🔌 Uji Koneksi';
          testResultBox.style.background = '#fef2f2';
          testResultBox.style.border = '1px solid #fecaca';
          testResultBox.style.color = '#dc2626';
          testResultBox.innerHTML = `<b>✕ Kesalahan Jaringan:</b> ${e.message}`;
        }
      });
    }

    if (btnSaveSettings && modalSettings) {
      btnSaveSettings.addEventListener('click', () => {
        const key = document.getElementById('settings-ai-key').value.trim();
        const prov = document.getElementById('settings-ai-provider').value;
        localStorage.setItem('studio_ml_ai_key', key);
        localStorage.setItem('studio_ml_ai_provider', prov);

        AICopilot.apiKey = key;
        AICopilot.provider = prov;

        this.updateProviderBadge();

        modalSettings.classList.remove('open');
        this.showToast("Pengaturan AI Copilot berhasil disimpan!", "success");
      });
    }

    // Global modal close on backdrop click or close button
    document.querySelectorAll('.modal-close, .modal-backdrop').forEach(el => {
      el.addEventListener('click', (e) => {
        if (e.target === el) {
          document.querySelectorAll('.modal-backdrop').forEach(m => m.classList.remove('open'));
        }
      });
    });
  },

  updateProviderBadge() {
    const badge = document.getElementById('ai-active-provider-badge');
    if (!badge) return;

    const prov = localStorage.getItem('studio_ml_ai_provider') || 'local';
    const key = localStorage.getItem('studio_ml_ai_key') || '';

    if (prov === 'gemini' && key) {
      badge.innerHTML = `<span style="color: #059669;">🟢 Google Gemini AI (Cloud LLM Aktif)</span>`;
    } else if (prov === 'gemini' && !key) {
      badge.innerHTML = `<span style="color: #d97706;">⚠️ Gemini Dipilih (API Key Belum Diisi)</span>`;
    } else {
      badge.innerHTML = `<span style="color: #059669;">🟢 Built-in Local Expert (Offline & Unlimited)</span>`;
    }
  },

  // ==================== TOAST NOTIFICATION ====================
  showToast(message, type = "info") {
    const toast = document.getElementById('app-toast');
    if (!toast) return;

    toast.innerText = message;
    toast.className = `toast show ${type}`;

    setTimeout(() => {
      toast.classList.remove('show');
    }, 3200);
  }
};

// Start app on DOM ready
document.addEventListener('DOMContentLoaded', () => {
  App.init();
  if (typeof ELearning !== 'undefined') {
    ELearning.init();
  }
});
