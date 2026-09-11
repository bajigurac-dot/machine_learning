/**
 * Studio ML Python - E-Learning, CBT Ujian & Lab Praktik Coding
 */
const ELearning = {
  currentExam: null,
  currentQuestionIdx: 0,
  studentInfo: { name: '', nisn: '', class_name: '' },
  answers: {},
  timerInterval: null,
  totalSeconds: 0,
  remainingSeconds: 0,
  studentSession: null,
  studentAttemptedExamIds: [],
  studentAttemptsMap: {},
  adminToken: localStorage.getItem('elearning_admin_token') || null,
  verifiedQuestions: {},
  sqlSchemaData: null,
  editorFontSize: 13.5,

  init() {
    this.loadStudentSession();
    this.bindEvents();
    this.loadLobbyExams();
  },

  bindEvents() {
    // Tombol Masuk Mode Admin di Lobby
    const btnOpenAdmin = document.getElementById('btn-open-admin-login');
    if (btnOpenAdmin) {
      btnOpenAdmin.addEventListener('click', () => {
        if (this.adminToken) {
          this.switchView('admin');
          this.loadAdminData();
        } else {
          document.getElementById('modal-admin-login').classList.add('open');
        }
      });
    }

    // Submit Login Admin
    const btnSubmitLogin = document.getElementById('btn-submit-admin-login');
    if (btnSubmitLogin) {
      btnSubmitLogin.addEventListener('click', () => this.handleAdminLogin());
    }

    // Input NISN instant check & enter
    const studentNisnInput = document.getElementById('student-login-nisn');
    let nisnDebounce = null;
    if (studentNisnInput) {
      studentNisnInput.addEventListener('input', (e) => {
        clearTimeout(nisnDebounce);
        nisnDebounce = setTimeout(() => {
          this.checkStudentNisnInput(e.target.value);
        }, 250);
      });
      studentNisnInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') this.handleStudentLogin();
      });
    }

    const studentNameInput = document.getElementById('student-login-name');
    if (studentNameInput) {
      studentNameInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') this.handleStudentLogin();
      });
    }

    // Tombol Login Siswa
    const btnStudentLogin = document.getElementById('btn-student-login');
    if (btnStudentLogin) {
      btnStudentLogin.addEventListener('click', () => this.handleStudentLogin());
    }

    // Tombol Cek Kartu Nilai Siswa (Langsung dari Form Login)
    const btnStudentViewCardLogin = document.getElementById('btn-student-view-card-login');
    if (btnStudentViewCardLogin) {
      btnStudentViewCardLogin.addEventListener('click', async () => {
        const nisnInput = document.getElementById('student-login-nisn');
        const nisn = nisnInput ? nisnInput.value.trim() : '';
        if (!nisn) {
          App.showToast("Ketik NISN resmi siswa Anda terlebih dahulu!", "error");
          if (nisnInput) nisnInput.focus();
          return;
        }
        await this.handleStudentLogin();
        if (this.studentSession && this.studentSession.nisn) {
          this.openStudentGradeCard(this.studentSession.nisn);
        }
      });
    }

    // Tombol Buka Kartu Nilai Saya (Saat Siswa Sudah Login)
    const btnOpenStudentGradeCard = document.getElementById('btn-open-student-grade-card');
    if (btnOpenStudentGradeCard) {
      btnOpenStudentGradeCard.addEventListener('click', () => {
        if (!this.studentSession || !this.studentSession.nisn) {
          App.showToast("Silakan login menggunakan NISN siswa terlebih dahulu.", "error");
          return;
        }
        this.openStudentGradeCard(this.studentSession.nisn);
      });
    }

    // Tombol Cetak & Unduh PDF Kartu Nilai
    const onPrintCard = () => {
      const nisn = this.currentCardNisn || (this.studentSession ? this.studentSession.nisn : '');
      if (!nisn) return;
      window.open(`/api/elearning/student/card/print?nisn=${encodeURIComponent(nisn)}`, '_blank');
    };

    const btnCardPrint = document.getElementById('btn-card-print-preview');
    if (btnCardPrint) {
      btnCardPrint.addEventListener('click', onPrintCard);
    }

    const btnCardPrintTop = document.getElementById('btn-card-print-preview-top');
    if (btnCardPrintTop) {
      btnCardPrintTop.addEventListener('click', onPrintCard);
    }

    const btnCardPdf = document.getElementById('btn-card-download-pdf');
    if (btnCardPdf) {
      btnCardPdf.addEventListener('click', () => {
        const nisn = this.currentCardNisn || (this.studentSession ? this.studentSession.nisn : '');
        if (!nisn) return;
        App.showToast("Menyiapkan berkas PDF resmi Kartu Hasil Ujian (KHS)...", "info");
        window.open(`/api/elearning/student/card/pdf?nisn=${encodeURIComponent(nisn)}`, '_blank');
      });
    }

    // Logout Siswa
    const btnStudentLogout = document.getElementById('btn-student-logout');
    if (btnStudentLogout) {
      btnStudentLogout.addEventListener('click', () => this.handleStudentLogout());
    }

    // Admin Add Student
    const btnAdminAddStudent = document.getElementById('btn-admin-add-student');
    if (btnAdminAddStudent) {
      btnAdminAddStudent.addEventListener('click', () => this.handleAdminAddStudent());
    }

    // Logout Admin
    const btnAdminLogout = document.getElementById('btn-admin-logout');
    if (btnAdminLogout) {
      btnAdminLogout.addEventListener('click', () => {
        this.adminToken = null;
        localStorage.removeItem('elearning_admin_token');
        this.switchView('lobby');
        App.showToast("Berhasil keluar dari mode Guru / Admin.", "info");
      });
    }

    // Admin Sub-Navigation (Paket Ujian vs Rekap Nilai)
    document.querySelectorAll('.admin-nav-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        document.querySelectorAll('.admin-nav-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.admin-tab-content').forEach(c => c.classList.add('hidden'));

        e.currentTarget.classList.add('active');
        const targetTab = e.currentTarget.getAttribute('data-admin-tab');
        const content = document.getElementById(targetTab);
        if (content) content.classList.remove('hidden');

        if (targetTab === 'admin-tab-students') {
          this.loadAdminStudents();
        } else if (targetTab === 'admin-tab-scores') {
          this.loadAdminSubmissionsTable();
        } else if (targetTab === 'admin-tab-exams') {
          this.loadAdminExamsTable();
        }
      });
    });

    // Filter Rekap Nilai Siswa (Kelas & Tanggal)
    const filterClass = document.getElementById('filter-score-class');
    if (filterClass) {
      filterClass.addEventListener('change', () => this.loadAdminSubmissionsTable());
    }

    const filterDate = document.getElementById('filter-score-date');
    if (filterDate) {
      filterDate.addEventListener('input', () => this.loadAdminSubmissionsTable());
      filterDate.addEventListener('change', () => this.loadAdminSubmissionsTable());
    }

    const btnResetScoreFilter = document.getElementById('btn-reset-score-filter');
    if (btnResetScoreFilter) {
      btnResetScoreFilter.addEventListener('click', () => {
        if (filterClass) filterClass.value = '';
        if (filterDate) filterDate.value = '';
        this.loadAdminSubmissionsTable();
      });
    }

    // Filter Master Data Siswa (Kelas & Nama/NISN)
    const filterStudentClass = document.getElementById('filter-student-class');
    if (filterStudentClass) {
      filterStudentClass.addEventListener('change', () => this.loadAdminStudents());
    }

    const filterStudentName = document.getElementById('filter-student-name');
    let studentSearchDebounce = null;
    if (filterStudentName) {
      filterStudentName.addEventListener('input', () => {
        clearTimeout(studentSearchDebounce);
        studentSearchDebounce = setTimeout(() => {
          this.loadAdminStudents();
        }, 200);
      });
    }

    const btnResetStudentFilter = document.getElementById('btn-reset-student-filter');
    if (btnResetStudentFilter) {
      btnResetStudentFilter.addEventListener('click', () => {
        if (filterStudentClass) filterStudentClass.value = '';
        if (filterStudentName) filterStudentName.value = '';
        this.loadAdminStudents();
      });
    }

    // Unduh Rekap Nilai PDF (ReportLab)
    const btnExportPdf = document.getElementById('btn-export-scores-pdf');
    if (btnExportPdf) {
      btnExportPdf.addEventListener('click', () => {
        const classFilter = document.getElementById('filter-score-class') ? document.getElementById('filter-score-class').value : '';
        const dateFilter = document.getElementById('filter-score-date') ? document.getElementById('filter-score-date').value : '';
        const params = new URLSearchParams();
        if (classFilter) params.append('class_name', classFilter);
        if (dateFilter) params.append('date', dateFilter);
        const queryStr = params.toString() ? `?${params.toString()}` : '';
        App.showToast("Menyiapkan berkas PDF resmi SMK Cahaya Pertiwi...", "info");
        window.open(`/api/elearning/admin/report/scores/pdf${queryStr}`, '_blank');
      });
    }

    // Pratinjau & Cetak Laporan
    const btnPrintScores = document.getElementById('btn-print-scores');
    if (btnPrintScores) {
      btnPrintScores.addEventListener('click', () => {
        const classFilter = document.getElementById('filter-score-class') ? document.getElementById('filter-score-class').value : '';
        const dateFilter = document.getElementById('filter-score-date') ? document.getElementById('filter-score-date').value : '';
        const params = new URLSearchParams();
        if (classFilter) params.append('class_name', classFilter);
        if (dateFilter) params.append('date', dateFilter);
        const queryStr = params.toString() ? `?${params.toString()}` : '';
        window.open(`/api/elearning/admin/report/scores/print${queryStr}`, '_blank');
      });
    }

    // Modal Create Exam (Admin)
    const btnOpenCreateExam = document.getElementById('btn-open-create-exam-modal');
    if (btnOpenCreateExam) {
      btnOpenCreateExam.addEventListener('click', () => {
        document.getElementById('modal-create-exam').classList.add('open');
      });
    }

    const btnSaveNewExam = document.getElementById('btn-save-new-exam');
    if (btnSaveNewExam) {
      btnSaveNewExam.addEventListener('click', () => this.handleCreateExam());
    }

    // Modal Ubah Password Guru (Admin)
    const btnOpenChangePass = document.getElementById('btn-open-change-password-modal');
    if (btnOpenChangePass) {
      btnOpenChangePass.addEventListener('click', () => {
        const oldInput = document.getElementById('change-pass-old');
        const newInput = document.getElementById('change-pass-new');
        const confirmInput = document.getElementById('change-pass-confirm');
        if (oldInput) oldInput.value = '';
        if (newInput) newInput.value = '';
        if (confirmInput) confirmInput.value = '';
        const errEl = document.getElementById('change-pass-error');
        if (errEl) errEl.style.display = 'none';
        const succEl = document.getElementById('change-pass-success');
        if (succEl) succEl.style.display = 'none';
        const modal = document.getElementById('modal-change-password');
        if (modal) {
          modal.classList.add('open');
          setTimeout(() => { if (oldInput) oldInput.focus(); }, 100);
        }
      });
    }

    const btnSubmitChangePass = document.getElementById('btn-submit-change-password');
    if (btnSubmitChangePass) {
      btnSubmitChangePass.addEventListener('click', () => this.handleChangeAdminPassword());
    }

    const changePassConfirmInput = document.getElementById('change-pass-confirm');
    if (changePassConfirmInput) {
      changePassConfirmInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') this.handleChangeAdminPassword();
      });
    }

    // Modal Edit Nilai Siswa (Admin)
    const btnSaveEditedScore = document.getElementById('btn-save-edited-score');
    if (btnSaveEditedScore) {
      btnSaveEditedScore.addEventListener('click', () => this.handleSaveEditedScore());
    }

    // Modal Add Question (Admin)
    const newQTypeSelect = document.getElementById('new-q-type');
    if (newQTypeSelect) {
      newQTypeSelect.addEventListener('change', (e) => {
        const isMcq = e.target.value === 'mcq';
        document.getElementById('new-q-mcq-fields').classList.toggle('hidden', !isMcq);
        document.getElementById('new-q-code-fields').classList.toggle('hidden', isMcq);
      });
    }

    const btnSaveNewQ = document.getElementById('btn-save-new-question');
    if (btnSaveNewQ) {
      btnSaveNewQ.addEventListener('click', () => this.handleSaveQuestion());
    }

    // Modal Edit Exam & Soal (Admin)
    const btnSaveEditExam = document.getElementById('btn-save-edit-exam');
    if (btnSaveEditExam) {
      btnSaveEditExam.addEventListener('click', () => this.handleSaveEditExam());
    }

    const editQTypeSelect = document.getElementById('edit-q-type');
    if (editQTypeSelect) {
      editQTypeSelect.addEventListener('change', (e) => {
        const isMcq = e.target.value === 'mcq';
        document.getElementById('edit-q-mcq-fields').classList.toggle('hidden', !isMcq);
        document.getElementById('edit-q-code-fields').classList.toggle('hidden', isMcq);
      });
    }

    const btnSaveEditQ = document.getElementById('btn-save-edit-question');
    if (btnSaveEditQ) {
      btnSaveEditQ.addEventListener('click', () => this.handleSaveEditQuestion());
    }

    // Exam Navigation Buttons
    const btnPrev = document.getElementById('btn-prev-question');
    const btnNext = document.getElementById('btn-next-question');
    if (btnPrev) btnPrev.addEventListener('click', () => this.prevQuestion());
    if (btnNext) btnNext.addEventListener('click', () => this.nextQuestion());

    // Run Code Button (Live Testing)
    const btnRunCode = document.getElementById('btn-run-student-code');
    if (btnRunCode) {
      btnRunCode.addEventListener('click', () => this.runStudentCode());
    }

    // Reset Code Button
    const btnResetCode = document.getElementById('btn-reset-code');
    if (btnResetCode) {
      btnResetCode.addEventListener('click', () => this.resetCurrentCode());
    }

    // Finish & Submit Exam Button
    const btnFinish = document.getElementById('btn-finish-exam');
    if (btnFinish) {
      btnFinish.addEventListener('click', () => this.confirmSubmitExam());
    }

    // Back to Lobby from Result View
    const btnBackLobby = document.getElementById('btn-back-to-lobby');
    if (btnBackLobby) {
      btnBackLobby.addEventListener('click', () => {
        this.switchView('lobby');
        this.updateStudentAuthState();
        this.loadLobbyExams();
      });
    }

    // Code Editor Controls & Keybindings
    const codeEditor = document.getElementById('exam-code-editor');
    if (codeEditor) {
      codeEditor.addEventListener('input', () => {
        this.updateLineNumbers();
        this.saveCurrentAnswer();
      });

      codeEditor.addEventListener('scroll', () => {
        this.syncEditorScroll();
      });

      codeEditor.addEventListener('keydown', (e) => {
        // 1. Shortcut Ctrl+Enter atau Cmd+Enter: Jalankan Kode Langsung
        if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
          e.preventDefault();
          this.runStudentCode();
          return;
        }

        // 2. Tab & Shift+Tab Indentasi (4 spasi) tanpa melompat fokus
        if (e.key === 'Tab') {
          e.preventDefault();
          const start = codeEditor.selectionStart;
          const end = codeEditor.selectionEnd;

          if (e.shiftKey) {
            // Unindent 4 spasi pada baris aktif
            const val = codeEditor.value;
            const lineStart = val.lastIndexOf('\n', start - 1) + 1;
            if (val.substring(lineStart, lineStart + 4) === '    ') {
              codeEditor.setRangeText('', lineStart, lineStart + 4, 'end');
              codeEditor.selectionStart = Math.max(lineStart, start - 4);
              codeEditor.selectionEnd = Math.max(lineStart, end - 4);
            }
          } else {
            // Insert 4 spasi mempertahankan history Undo/Redo
            codeEditor.setRangeText('    ', start, end, 'end');
          }
          this.updateLineNumbers();
          this.saveCurrentAnswer();
          return;
        }

        // 3. Enter Auto-indent (melanjutkan indentasi baris sebelumnya)
        if (e.key === 'Enter') {
          const start = codeEditor.selectionStart;
          const val = codeEditor.value;
          const lineStart = val.lastIndexOf('\n', start - 1) + 1;
          const currentLine = val.substring(lineStart, start);
          const matchIndent = currentLine.match(/^\s*/);
          let indent = matchIndent ? matchIndent[0] : '';
          
          // Jika baris berakhir dengan tanda titik dua ':' (blok Python), tambah indentasi 4 spasi
          if (currentLine.trim().endsWith(':')) {
            indent += '    ';
          }

          if (indent.length > 0) {
            e.preventDefault();
            codeEditor.setRangeText('\n' + indent, start, start, 'end');
            this.updateLineNumbers();
            this.saveCurrentAnswer();
          }
        }
      });
    }

    // Font Size Controls (A- / A+)
    const btnFontDec = document.getElementById('btn-font-dec');
    if (btnFontDec) {
      btnFontDec.addEventListener('click', () => {
        this.editorFontSize = Math.max(11, this.editorFontSize - 1);
        this.applyEditorFontSize();
      });
    }

    const btnFontInc = document.getElementById('btn-font-inc');
    if (btnFontInc) {
      btnFontInc.addEventListener('click', () => {
        this.editorFontSize = Math.min(18, this.editorFontSize + 1);
        this.applyEditorFontSize();
      });
    }

    // Toggle SQL Database Schema Drawer
    const btnToggleSql = document.getElementById('btn-toggle-sql-schema');
    if (btnToggleSql) {
      btnToggleSql.addEventListener('click', () => this.toggleSqlSchemaDrawer());
    }

    // SQL Snippet Chips
    document.querySelectorAll('.snippet-chip').forEach(chip => {
      chip.addEventListener('click', (e) => {
        const sql = e.currentTarget.getAttribute('data-sql');
        if (sql) this.insertTextToEditor(sql);
      });
    });
  },

  // ==================== CODE EDITOR HELPERS ====================
  applyEditorFontSize() {
    const editor = document.getElementById('exam-code-editor');
    const lines = document.getElementById('editor-line-numbers');
    if (editor) editor.style.fontSize = `${this.editorFontSize}px`;
    if (lines) lines.style.fontSize = `${this.editorFontSize}px`;
  },

  updateLineNumbers() {
    const editor = document.getElementById('exam-code-editor');
    const lineNumbers = document.getElementById('editor-line-numbers');
    if (!editor || !lineNumbers) return;
    const count = (editor.value || '').split('\n').length;
    let nums = '';
    for (let i = 1; i <= count; i++) {
      nums += i + '\n';
    }
    lineNumbers.textContent = nums;
  },

  syncEditorScroll() {
    const editor = document.getElementById('exam-code-editor');
    const lineNumbers = document.getElementById('editor-line-numbers');
    if (editor && lineNumbers) {
      lineNumbers.scrollTop = editor.scrollTop;
    }
  },

  insertTextToEditor(text) {
    const editor = document.getElementById('exam-code-editor');
    if (!editor) return;
    editor.focus();
    const start = editor.selectionStart;
    const end = editor.selectionEnd;
    const val = editor.value;
    const prefix = (start > 0 && val[start - 1] !== '\n' && val[start - 1] !== ' ') ? ' ' : '';
    editor.setRangeText(prefix + text, start, end, 'end');
    this.updateLineNumbers();
    this.saveCurrentAnswer();
    App.showToast(`Snippet '${text.split(' ')[0]}' disisipkan ke editor!`, "info");
  },

  async toggleSqlSchemaDrawer() {
    const drawer = document.getElementById('sql-schema-drawer');
    const btn = document.getElementById('btn-toggle-sql-schema');
    if (!drawer) return;

    const isHidden = drawer.classList.contains('hidden');
    if (isHidden) {
      drawer.classList.remove('hidden');
      if (btn) btn.innerHTML = '✕ Tutup Skema';
      if (!this.sqlSchemaData) {
        await this.loadSqlSchema();
      }
    } else {
      drawer.classList.add('hidden');
      if (btn) btn.innerHTML = '🗄️ Skema Database & Sampel';
    }
  },

  async loadSqlSchema() {
    const container = document.getElementById('sql-schema-content');
    if (!container) return;
    try {
      container.innerHTML = `<div style="font-size: 0.78rem; color: #64748b; padding: 8px;"><span class="pulse-loader"></span> Memuat struktur database SQLite lab SMK...</div>`;
      const res = await API.getSqlSchema();
      if (res.success && res.tables) {
        this.sqlSchemaData = res.tables;
        this.renderSqlSchema(res.tables);
      } else {
        container.innerHTML = `<div style="font-size: 0.78rem; color: #e11d48; padding: 8px;">Gagal memuat skema: ${res.error || 'Terjadi kesalahan'}</div>`;
      }
    } catch (e) {
      container.innerHTML = `<div style="font-size: 0.78rem; color: #e11d48; padding: 8px;">Error: ${e.message}</div>`;
    }
  },

  renderSqlSchema(tables) {
    const container = document.getElementById('sql-schema-content');
    if (!container) return;

    container.innerHTML = tables.map(t => {
      const colPills = t.columns.map(c => `
        <span class="schema-col-badge" onclick="ELearning.insertTextToEditor('${c.name}')" title="Klik untuk menyalin kolom '${c.name}' ke editor">
          ${c.is_pk ? '🔑 ' : ''}<b>${c.name}</b><span class="schema-col-type">${c.type}</span>
        </span>
      `).join('');

      let sampleHtml = '';
      if (t.sample_rows && t.sample_rows.length > 0) {
        const colNames = t.columns.map(c => c.name);
        sampleHtml = `
          <div style="font-size: 0.72rem; color: #64748b; margin: 6px 0 3px; font-weight: 600;">Data Sampel Tabel '${t.table_name}':</div>
          <div style="overflow-x: auto; max-height: 120px; border: 1px solid #e2e8f0; border-radius: 4px;">
            <table class="exam-table-view" style="font-size: 0.72rem;">
              <thead>
                <tr>${colNames.map(cn => `<th>${cn}</th>`).join('')}</tr>
              </thead>
              <tbody>
                ${t.sample_rows.map(r => `
                  <tr>${colNames.map(cn => `<td>${r[cn] !== undefined && r[cn] !== null ? r[cn] : '-'}</td>`).join('')}</tr>
                `).join('')}
              </tbody>
            </table>
          </div>
        `;
      }

      return `
        <div class="schema-table-card">
          <div class="schema-table-title">
            <span>📋 Tabel <code>${t.table_name}</code></span>
            <button type="button" class="btn-studio-action" style="font-size: 0.68rem; padding: 2px 6px; margin-left: auto;" onclick="ELearning.insertTextToEditor('SELECT * FROM ${t.table_name};')">
              Query Tabel Ini
            </button>
          </div>
          <div class="schema-cols-wrap">${colPills}</div>
          ${sampleHtml}
        </div>
      `;
    }).join('');
  },

  // ==================== VIEW SWITCHER ====================
  switchView(viewName) {
    document.getElementById('elearning-view-lobby').classList.add('hidden');
    document.getElementById('elearning-view-exam').classList.add('hidden');
    document.getElementById('elearning-view-result').classList.add('hidden');
    document.getElementById('elearning-view-admin').classList.add('hidden');

    if (viewName === 'lobby') {
      document.getElementById('elearning-view-lobby').classList.remove('hidden');
    } else if (viewName === 'exam') {
      document.getElementById('elearning-view-exam').classList.remove('hidden');
    } else if (viewName === 'result') {
      document.getElementById('elearning-view-result').classList.remove('hidden');
    } else if (viewName === 'admin') {
      document.getElementById('elearning-view-admin').classList.remove('hidden');
    }
  },

  // ==================== LOBBY & STUDENT AUTH ====================
  async loadStudentSession() {
    try {
      const saved = localStorage.getItem('elearning_student_session');
      if (saved) {
        this.studentSession = JSON.parse(saved);
        if (this.studentSession && this.studentSession.nisn) {
          try {
            const attRes = await API.getStudentAttempts(this.studentSession.nisn);
            if (attRes.success && attRes.attempts) {
              this.studentAttemptedExamIds = attRes.attempts.map(a => a.exam_id);
              this.studentAttemptsMap = {};
              attRes.attempts.forEach(a => { this.studentAttemptsMap[a.exam_id] = a; });
            }
          } catch (err) {
            console.warn("Could not fetch student attempts:", err);
          }
        }
      }
    } catch (e) {
      this.studentSession = null;
    }
    this.updateStudentAuthState();
  },

  updateStudentAuthState() {
    const loginCard = document.getElementById('elearning-student-login-card');
    const activeCard = document.getElementById('elearning-student-active-card');
    
    if (this.studentSession && this.studentSession.name) {
      if (loginCard) loginCard.classList.add('hidden');
      if (activeCard) {
        activeCard.classList.remove('hidden');
        const nameEl = document.getElementById('active-student-name');
        const nisnEl = document.getElementById('active-student-nisn');
        const classEl = document.getElementById('active-student-class');
        const countEl = document.getElementById('active-student-exam-count');
        if (nameEl) nameEl.innerText = this.studentSession.name;
        if (nisnEl) nisnEl.innerText = this.studentSession.nisn || '-';
        if (classEl) classEl.innerText = this.studentSession.class_name || 'XII - SMK Cahaya Pertiwi';
        if (countEl) countEl.innerText = this.studentAttemptedExamIds ? this.studentAttemptedExamIds.length : 0;
      }
    } else {
      if (loginCard) loginCard.classList.remove('hidden');
      if (activeCard) activeCard.classList.add('hidden');
    }
  },

  async checkStudentNisnInput(nisn) {
    const cleanNisn = (nisn || '').trim();
    const statusEl = document.getElementById('student-login-status');
    const nameInput = document.getElementById('student-login-name');
    const classInput = document.getElementById('student-login-class');

    if (!cleanNisn) {
      if (statusEl) statusEl.style.display = 'none';
      if (nameInput) nameInput.value = '';
      if (classInput) classInput.value = '';
      return;
    }

    try {
      const res = await API.checkNisn(cleanNisn);
      if (res.success && res.student) {
        if (nameInput) nameInput.value = res.student.name;
        if (classInput) classInput.value = res.student.class_name;
        if (statusEl) {
          statusEl.style.display = 'block';
          statusEl.style.color = '#059669';
          statusEl.innerHTML = `✅ Terdaftar: <b>${res.student.name}</b> (${res.student.class_name})`;
        }
      } else {
        if (statusEl) {
          statusEl.style.display = 'block';
          statusEl.style.color = '#ef4444';
          statusEl.innerText = `❌ ${res.error || 'NISN tidak terdaftar di Master Database.'}`;
        }
      }
    } catch (e) {
      if (statusEl) {
        statusEl.style.display = 'block';
        statusEl.style.color = '#ef4444';
        statusEl.innerText = `❌ NISN tidak terdaftar di database resmi.`;
      }
    }
  },

  async handleStudentLogin() {
    const nisnInput = document.getElementById('student-login-nisn');
    const nameInput = document.getElementById('student-login-name');
    const statusEl = document.getElementById('student-login-status');

    const nisn = nisnInput ? nisnInput.value.trim() : '';
    const name = nameInput ? nameInput.value.trim() : '';

    if (!nisn) {
      App.showToast("Harap masukkan NISN resmi siswa Anda!", "error");
      if (nisnInput) nisnInput.focus();
      return;
    }

    if (statusEl) {
      statusEl.style.display = 'block';
      statusEl.style.color = '#059669';
      statusEl.innerText = 'Memverifikasi data siswa di Master Database SMK Cahaya Pertiwi...';
    }

    try {
      const res = await API.studentLogin(nisn, name);
      if (res.success && res.student) {
        this.studentSession = res.student;
        this.studentAttemptedExamIds = res.attempted_exam_ids || [];
        this.studentAttemptsMap = {};
        
        // Fetch detailed attempts for scores
        try {
          const attRes = await API.getStudentAttempts(this.studentSession.nisn);
          if (attRes.success && attRes.attempts) {
            this.studentAttemptedExamIds = attRes.attempts.map(a => a.exam_id);
            attRes.attempts.forEach(a => { this.studentAttemptsMap[a.exam_id] = a; });
          }
        } catch (err) {}

        localStorage.setItem('elearning_student_session', JSON.stringify(this.studentSession));
        this.updateStudentAuthState();
        this.loadLobbyExams();
        App.showToast(res.message || `Login berhasil! Selamat datang, ${this.studentSession.name}.`, "success");
        if (statusEl) statusEl.style.display = 'none';
      } else {
        const errMsg = res.error || "NISN atau Nama tidak terdaftar di database sekolah.";
        App.showToast(errMsg, "error");
        if (statusEl) {
          statusEl.style.display = 'block';
          statusEl.style.color = '#ef4444';
          statusEl.innerText = `❌ ${errMsg}`;
        }
      }
    } catch (e) {
      App.showToast(`Gagal login: ${e.message}`, "error");
      if (statusEl) {
        statusEl.style.display = 'block';
        statusEl.style.color = '#ef4444';
        statusEl.innerText = `❌ ${e.message}`;
      }
    }
  },

  handleStudentLogout() {
    this.studentSession = null;
    this.studentAttemptedExamIds = [];
    this.studentAttemptsMap = {};
    localStorage.removeItem('elearning_student_session');
    this.updateStudentAuthState();
    this.loadLobbyExams();
    App.showToast("Anda telah keluar dari sesi siswa. Soal ujian terkunci kembali.", "info");
  },

  promptStudentLogin(examId) {
    App.showToast("🔒 Akses Terkunci: Anda harus login dengan NISN resmi terlebih dahulu sebelum mengerjakan soal!", "error");
    const loginCard = document.getElementById('elearning-student-login-card');
    if (loginCard) {
      loginCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
      loginCard.style.boxShadow = "0 0 20px rgba(239, 68, 68, 0.4)";
      setTimeout(() => {
        loginCard.style.boxShadow = "";
      }, 1500);
    }
    const nisnInput = document.getElementById('student-login-nisn');
    if (nisnInput) nisnInput.focus();
  },

  async loadLobbyExams() {
    const container = document.getElementById('elearning-exams-list');
    if (!container) return;

    const isLoggedIn = !!(this.studentSession && this.studentSession.name);

    try {
      // Refresh attempts if logged in
      if (isLoggedIn && this.studentSession.nisn) {
        try {
          const attRes = await API.getStudentAttempts(this.studentSession.nisn);
          if (attRes.success && attRes.attempts) {
            this.studentAttemptedExamIds = attRes.attempts.map(a => a.exam_id);
            this.studentAttemptsMap = {};
            attRes.attempts.forEach(a => { this.studentAttemptsMap[a.exam_id] = a; });
          }
        } catch (err) {}
      }

      const res = await API.getExams();
      if (res.success && res.exams.length > 0) {
        container.innerHTML = res.exams.map(exam => {
          let actionBtn = '';
          let statusBadge = '';

          let classBadge = '';
          const titleDesc = ((exam.title || '') + ' ' + (exam.description || '')).toLowerCase();
          if (titleDesc.includes('xi') || titleDesc.includes('xii')) {
            classBadge = `<span class="nav-tag amber" style="font-weight: 700; font-size: 0.72rem; padding: 2px 8px;">Kelas XI & XII</span>`;
          } else if (titleDesc.includes('kelas x') || titleDesc.includes('kelas 10')) {
            classBadge = `<span class="nav-tag purple" style="font-weight: 700; font-size: 0.72rem; padding: 2px 8px;">Kelas X</span>`;
          }

          if (!isLoggedIn) {
            statusBadge = `<span class="nav-tag rose" style="font-weight: 700;">🔒 Terkunci (Perlu Login)</span>`;
            actionBtn = `<button class="btn btn-secondary btn-sm" onclick="ELearning.promptStudentLogin(${exam.id})" style="border-color: #fca5a5; color: #be123c; font-weight: 600;">
                           🔒 Login untuk Membuka
                         </button>`;
          } else if (this.studentAttemptedExamIds && this.studentAttemptedExamIds.includes(exam.id)) {
            const att = this.studentAttemptsMap ? this.studentAttemptsMap[exam.id] : null;
            const scoreTxt = att ? `Nilai: ${att.score}` : 'Selesai';
            statusBadge = `<span class="nav-tag green" style="font-weight: 700;">✅ ${scoreTxt}</span>`;
            actionBtn = `<button class="btn btn-secondary btn-sm" disabled style="opacity: 0.65; cursor: not-allowed; font-weight: 600;" title="Anda sudah menyelesaikan ujian ini">
                           🔒 Selesai Dikerjakan
                         </button>`;
          } else {
            statusBadge = `<span class="nav-tag green" style="font-weight: 700;">🟢 Siap Dikerjakan</span>`;
            actionBtn = `<button class="btn btn-primary btn-sm" onclick="ELearning.startExam(${exam.id})">
                           Mulai Ujian 🚀
                         </button>`;
          }

          return `
          <div class="glass-panel exam-card" style="display: flex; flex-direction: column; justify-content: space-between; ${!isLoggedIn ? 'border-color: rgba(239,68,68,0.25); background: rgba(255,255,255,0.7);' : ''}">
            <div>
              <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px; flex-wrap: wrap; gap: 6px;">
                <div style="display: flex; gap: 6px; align-items: center; flex-wrap: wrap;">
                  <span class="nav-tag purple">${exam.subject}</span>
                  ${classBadge}
                </div>
                <div style="display: flex; gap: 6px; align-items: center;">
                  ${statusBadge}
                  <span class="exam-duration-pill">⏱️ ${exam.duration_minutes} Menit</span>
                </div>
              </div>
              <h3 style="font-size: 1.12rem; font-weight: 700; color: var(--text-main); margin-bottom: 6px;">
                ${exam.title}
              </h3>
              <p style="font-size: 0.82rem; color: var(--text-muted); line-height: 1.5; margin-bottom: 14px;">
                ${exam.description || 'Ujian evaluasi kompetensi pemrograman dan pemahaman kecerdasan buatan (AI).'}
              </p>
            </div>

            <div style="border-top: 1px solid var(--border-subtle); padding-top: 14px; display: flex; align-items: center; justify-content: space-between;">
              <span style="font-size: 0.78rem; color: var(--text-dim); font-weight: 600;">
                📝 ${exam.question_count || 0} Soal • ${exam.total_points || 100} Poin
              </span>
              ${actionBtn}
            </div>
          </div>
        `;
        }).join('');
      } else {
        container.innerHTML = `
          <div style="text-align: center; color: var(--text-dim); padding: 32px; grid-column: span 2;">
            Belum ada paket ujian yang aktif. Hubungi guru pembimbing Anda.
          </div>
        `;
      }
    } catch (e) {
      container.innerHTML = `<div style="color: var(--accent-rose); padding: 20px;">Gagal memuat ujian: ${e.message}</div>`;
    }
  },

  async startExam(examId) {
    if (!this.studentSession || !this.studentSession.name) {
      this.promptStudentLogin(examId);
      return;
    }

    if (this.studentAttemptedExamIds && this.studentAttemptedExamIds.includes(examId)) {
      App.showToast("Anda sudah pernah menyelesaikan ujian ini! Sistem hanya mengizinkan 1 kali pengerjaan demi integritas ujian.", "warning");
      return;
    }

    this.studentInfo = {
      name: this.studentSession.name,
      nisn: this.studentSession.nisn || '-',
      class_name: this.studentSession.class_name || 'XII - SMK Cahaya Pertiwi'
    };

    App.showToast(`Menyiapkan lembar ujian untuk ${this.studentInfo.name}...`, "info");

    try {
      const res = await API.getExam(examId);
      if (!res.success) {
        App.showToast(`Gagal memulai ujian: ${res.error}`, "error");
        return;
      }

      this.currentExam = res.exam;
      this.currentQuestionIdx = 0;
      this.answers = {};
      this.verifiedQuestions = {};

      if (!this.currentExam.questions || this.currentExam.questions.length === 0) {
        App.showToast("Paket ujian ini belum memiliki butir soal.", "error");
        return;
      }

      // Pre-fill starter code if coding question
      this.currentExam.questions.forEach(q => {
        if (q.starter_code) {
          this.answers[q.id] = q.starter_code;
        }
      });

      // Update exam room headers
      document.getElementById('exam-active-title').innerText = this.currentExam.title;
      document.getElementById('exam-student-badge').innerText = `${this.studentInfo.name} (${this.studentInfo.class_name})`;

      // Start timer
      this.initTimer(this.currentExam.duration_minutes || 30);

      // Render question palette & first question
      this.renderPalette();
      this.renderQuestion(0);

      this.switchView('exam');
      App.showToast("Ujian dimulai! Selamat mengerjakan dan perhatikan waktu.", "success");
    } catch (e) {
      App.showToast(`Error: ${e.message}`, "error");
    }
  },

  // ==================== TIMER COUNTDOWN SYSTEM ====================
  initTimer(durationMinutes) {
    if (this.timerInterval) clearInterval(this.timerInterval);

    this.totalSeconds = durationMinutes * 60;
    this.remainingSeconds = this.totalSeconds;
    this.updateTimerDisplay();

    this.timerInterval = setInterval(() => {
      this.remainingSeconds--;
      this.updateTimerDisplay();

      if (this.remainingSeconds <= 0) {
        clearInterval(this.timerInterval);
        App.showToast("⏰ Waktu Ujian Telah Habis! Mengumpulkan jawaban secara otomatis...", "error");
        setTimeout(() => this.executeSubmit(), 1200);
      }
    }, 1000);
  },

  updateTimerDisplay() {
    const mins = Math.floor(this.remainingSeconds / 60);
    const secs = this.remainingSeconds % 60;
    const formatted = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;

    const timerDisp = document.getElementById('exam-timer-display');
    const timerBox = document.getElementById('exam-timer-box');
    const progressFill = document.getElementById('exam-timer-progress');

    if (timerDisp) timerDisp.innerText = formatted;

    const pct = Math.max(0, (this.remainingSeconds / this.totalSeconds) * 100);
    if (progressFill) progressFill.style.width = `${pct}%`;

    // Warning and Danger colors
    if (this.remainingSeconds <= 60) {
      if (timerBox) timerBox.className = 'exam-timer-box timer-danger';
    } else if (this.remainingSeconds <= 300) {
      if (timerBox) timerBox.className = 'exam-timer-box timer-warning';
    } else {
      if (timerBox) timerBox.className = 'exam-timer-box';
    }
  },

  // ==================== QUESTION RENDERING & PALETTE ====================
  renderPalette() {
    const container = document.getElementById('exam-palette-container');
    if (!container || !this.currentExam) return;

    container.innerHTML = this.currentExam.questions.map((q, idx) => {
      const isAnswered = this.answers[q.id] && String(this.answers[q.id]).trim() !== '';
      const isActive = idx === this.currentQuestionIdx;
      const isVerified = this.verifiedQuestions && this.verifiedQuestions[q.id] === true;

      let statusClass = '';
      if (isActive) statusClass = 'active';
      else if (isVerified) statusClass = 'verified-pass';
      else if (isAnswered) statusClass = 'answered';

      return `
        <button class="palette-num-btn ${statusClass}" onclick="ELearning.renderQuestion(${idx})" title="Soal Nomor ${idx + 1}${isVerified ? ' (Teruji Benar ✓)' : (isAnswered ? ' (Sudah Dijawab)' : '')}">
          ${idx + 1}
        </button>
      `;
    }).join('');
  },

  renderQuestion(idx) {
    if (!this.currentExam || !this.currentExam.questions[idx]) return;

    // Save current question code if moving away
    this.saveCurrentAnswer();

    this.currentQuestionIdx = idx;
    const q = this.currentExam.questions[idx];
    const totalQ = this.currentExam.questions.length;

    // Header info
    document.getElementById('exam-q-number').innerText = `Soal ${idx + 1} dari ${totalQ}`;
    document.getElementById('exam-q-points').innerText = `${q.points || 20} Poin`;

    const typeBadge = document.getElementById('exam-q-type-badge');
    if (q.question_type === 'mcq') {
      typeBadge.innerText = 'Pilihan Ganda';
      typeBadge.className = 'nav-tag purple';
    } else if (q.question_type === 'code_sql') {
      typeBadge.innerText = 'Esai Coding MySQL';
      typeBadge.className = 'nav-tag green';
    } else {
      typeBadge.innerText = 'Esai Coding Python';
      typeBadge.className = 'nav-tag green';
    }

    // Question Text
    document.getElementById('exam-q-text').innerText = q.question_text;

    // Toggle MCQ vs Code Editor
    const mcqBox = document.getElementById('exam-mcq-container');
    const codeBox = document.getElementById('exam-code-container');

    if (q.question_type === 'mcq') {
      mcqBox.classList.remove('hidden');
      codeBox.classList.add('hidden');

      const savedAnswer = this.answers[q.id] || '';
      const options = q.options || [];

      mcqBox.innerHTML = options.map((optText, optIdx) => {
        const optLetter = optText.charAt(0).toUpperCase();
        const isChecked = savedAnswer === optLetter ? 'checked' : '';
        return `
          <label class="mcq-option-label ${savedAnswer === optLetter ? 'selected' : ''}">
            <input type="radio" name="mcq_answer_${q.id}" value="${optLetter}" ${isChecked} onchange="ELearning.selectMCQAnswer(${q.id}, '${optLetter}')" />
            <span>${optText}</span>
          </label>
        `;
      }).join('');

    } else {
      mcqBox.classList.add('hidden');
      codeBox.classList.remove('hidden');

      const isSql = q.question_type === 'code_sql';
      const langLabel = document.getElementById('exam-code-lang-label');
      const btnToggleSql = document.getElementById('btn-toggle-sql-schema');
      const sqlSnippetsBar = document.getElementById('sql-snippets-bar');
      const sqlDrawer = document.getElementById('sql-schema-drawer');

      if (isSql) {
        langLabel.innerHTML = '🗄️ Editor SQL Interaktif (SQLite DB: tabel siswa)';
        if (btnToggleSql) btnToggleSql.style.display = 'flex';
        if (sqlSnippetsBar) sqlSnippetsBar.classList.remove('hidden');
      } else {
        langLabel.innerHTML = '🐍 Editor Python Interaktif';
        if (btnToggleSql) btnToggleSql.style.display = 'none';
        if (sqlSnippetsBar) sqlSnippetsBar.classList.add('hidden');
        if (sqlDrawer) sqlDrawer.classList.add('hidden');
      }

      const editor = document.getElementById('exam-code-editor');
      editor.value = this.answers[q.id] !== undefined ? this.answers[q.id] : (q.starter_code || '');
      this.applyEditorFontSize();
      this.updateLineNumbers();

      // Status pill update
      const statusPill = document.getElementById('exam-code-status-pill');
      const statusText = document.getElementById('exam-code-status-text');
      if (statusPill && statusText) {
        if (this.verifiedQuestions[q.id] === true) {
          statusPill.className = 'status-pill status-verified';
          statusText.innerText = '✅ Teruji & Lolos Uji Coba';
        } else if (this.verifiedQuestions[q.id] === false) {
          statusPill.className = 'status-pill status-failed';
          statusText.innerText = '❌ Perlu Diperbaiki';
        } else {
          statusPill.className = 'status-pill status-untested';
          statusText.innerText = 'Belum Diuji Coba';
        }
      }

      // Hide feedback box until run
      document.getElementById('exam-code-feedback').classList.add('hidden');
      document.getElementById('exam-code-run-status').innerText = '';
    }

    // Prev / Next button states
    const btnPrev = document.getElementById('btn-prev-question');
    const btnNext = document.getElementById('btn-next-question');
    if (btnPrev) btnPrev.disabled = idx === 0;
    if (btnNext) btnNext.disabled = idx === totalQ - 1;

    this.renderPalette();
  },

  selectMCQAnswer(questionId, optionLetter) {
    this.answers[questionId] = optionLetter;
    this.renderQuestion(this.currentQuestionIdx);
  },

  saveCurrentAnswer() {
    if (!this.currentExam || !this.currentExam.questions[this.currentQuestionIdx]) return;
    const q = this.currentExam.questions[this.currentQuestionIdx];
    if (q.question_type !== 'mcq') {
      const editor = document.getElementById('exam-code-editor');
      if (editor) {
        this.answers[q.id] = editor.value;
      }
    }
  },

  prevQuestion() {
    if (this.currentQuestionIdx > 0) {
      this.renderQuestion(this.currentQuestionIdx - 1);
    }
  },

  nextQuestion() {
    if (this.currentExam && this.currentQuestionIdx < this.currentExam.questions.length - 1) {
      this.renderQuestion(this.currentQuestionIdx + 1);
    }
  },

  resetCurrentCode() {
    const q = this.currentExam.questions[this.currentQuestionIdx];
    const editor = document.getElementById('exam-code-editor');
    if (editor && q.starter_code) {
      editor.value = q.starter_code;
      this.answers[q.id] = q.starter_code;
      this.verifiedQuestions[q.id] = null;
      this.updateLineNumbers();

      const statusPill = document.getElementById('exam-code-status-pill');
      const statusText = document.getElementById('exam-code-status-text');
      if (statusPill && statusText) {
        statusPill.className = 'status-pill status-untested';
        statusText.innerText = 'Belum Diuji Coba';
      }

      document.getElementById('exam-code-feedback').classList.add('hidden');
      document.getElementById('exam-code-run-status').innerText = '';
      this.renderPalette();
      App.showToast("Kode dikembalikan ke template awal.", "info");
    }
  },

  // ==================== LIVE RUN CODE (CHECKLIST VS SILANG) ====================
  async runStudentCode() {
    const q = this.currentExam.questions[this.currentQuestionIdx];
    const editor = document.getElementById('exam-code-editor');
    const code = editor.value;
    this.answers[q.id] = code;

    const statusEl = document.getElementById('exam-code-run-status');
    const feedbackBox = document.getElementById('exam-code-feedback');
    const feedbackBadge = document.getElementById('exam-feedback-badge');
    const statusPill = document.getElementById('exam-code-status-pill');
    const statusText = document.getElementById('exam-code-status-text');

    const sqlFeedbackView = document.getElementById('sql-feedback-view');
    const pyFeedbackView = document.getElementById('python-feedback-view');
    const terminalRawWrap = document.getElementById('terminal-raw-wrap');
    const terminalOutput = document.getElementById('exam-terminal-output');

    statusEl.innerHTML = `<span class="pulse-loader"></span> Menjalankan...`;
    feedbackBox.classList.remove('hidden');

    const language = q.question_type === 'code_sql' ? 'sql' : 'python';

    try {
      const res = await API.runCode(language, code, q.expected_output);
      statusEl.innerText = '';

      this.verifiedQuestions[q.id] = Boolean(res.is_correct);

      if (statusPill && statusText) {
        if (res.is_correct) {
          statusPill.className = 'status-pill status-verified';
          statusText.innerText = '✅ Teruji & Lolos Uji Coba';
        } else {
          statusPill.className = 'status-pill status-failed';
          statusText.innerText = '❌ Perlu Diperbaiki';
        }
      }

      if (res.is_correct) {
        // ✅ Ceklis Hijau
        feedbackBadge.className = 'feedback-badge feedback-success';
        feedbackBadge.innerHTML = `
          <span style="font-size: 1.35rem;">✅</span>
          <div>
            <b>Jawaban Tepat! (Output Sesuai Uji Coba)</b>
            <div style="font-size: 0.74rem; font-weight: normal; opacity: 0.95;">
              ${res.feedback_detail || 'Logika dan hasil eksekusi program Anda berhasil lolos verifikasi otomatis.'}
            </div>
          </div>
        `;
      } else {
        // ❌ Silang Merah
        feedbackBadge.className = 'feedback-badge feedback-error';
        feedbackBadge.innerHTML = `
          <span style="font-size: 1.35rem;">❌</span>
          <div>
            <b>Jawaban Belum Sesuai (Perlu Diperbaiki)</b>
            <div style="font-size: 0.74rem; font-weight: normal; opacity: 0.95;">
              ${res.error || res.feedback_detail || 'Output program berbeda dari target yang ditentukan soal.'}
            </div>
          </div>
        `;
      }

      if (language === 'sql') {
        sqlFeedbackView.classList.remove('hidden');
        pyFeedbackView.classList.add('hidden');

        // Update SQL stats
        const rowCount = res.row_count !== undefined ? res.row_count : (res.rows ? res.rows.length : 0);
        document.getElementById('sql-rows-badge').innerText = `${rowCount} Baris Data`;
        document.getElementById('sql-time-badge').innerText = res.execution_time_ms !== undefined ? `⏱️ ${res.execution_time_ms} ms` : '';

        // Render Table View
        const thead = document.getElementById('exam-sql-output-thead');
        const tbody = document.getElementById('exam-sql-output-tbody');

        if (res.columns && res.columns.length > 0) {
          thead.innerHTML = `<tr>${res.columns.map(c => `<th>${c}</th>`).join('')}</tr>`;
          if (res.rows && res.rows.length > 0) {
            tbody.innerHTML = res.rows.map(r => `
              <tr>${r.map(val => `<td>${val !== null && val !== undefined ? val : '<em>NULL</em>'}</td>`).join('')}</tr>
            `).join('');
          } else {
            tbody.innerHTML = `<tr><td colspan="${res.columns.length}" style="text-align: center; color: #64748b; padding: 14px;">(0 baris data dikembalikan)</td></tr>`;
          }
        } else {
          thead.innerHTML = '';
          tbody.innerHTML = `<tr><td style="text-align: center; color: #64748b; padding: 14px;">(Tidak ada kolom data yang dikembalikan)</td></tr>`;
        }

        // Expected output target display
        const targetWrap = document.getElementById('sql-target-info-wrap');
        const targetTerminal = document.getElementById('sql-target-terminal');
        if (q.expected_output && !res.is_correct) {
          targetWrap.classList.remove('hidden');
          targetTerminal.innerText = q.expected_output;
        } else {
          targetWrap.classList.add('hidden');
        }

      } else {
        // Python
        sqlFeedbackView.classList.add('hidden');
        pyFeedbackView.classList.remove('hidden');

        document.getElementById('py-time-badge').innerText = res.execution_time_ms !== undefined ? `⏱️ ${res.execution_time_ms} ms` : '';
        document.getElementById('exam-py-actual-output').innerText = res.actual_output || '(Tidak ada teks yang dicetak oleh program)';
        document.getElementById('exam-py-expected-output').innerText = q.expected_output || '(Target output tidak ditentukan)';
      }

      // Show terminal log if error occurred
      if (res.error) {
        terminalRawWrap.classList.remove('hidden');
        terminalOutput.innerText = res.error;
      } else {
        terminalRawWrap.classList.add('hidden');
      }

      this.renderPalette();
    } catch (e) {
      statusEl.innerText = '';
      this.verifiedQuestions[q.id] = false;
      if (statusPill && statusText) {
        statusPill.className = 'status-pill status-failed';
        statusText.innerText = '❌ Error Eksekusi';
      }
      feedbackBadge.className = 'feedback-badge feedback-error';
      feedbackBadge.innerHTML = `<span>❌</span> <b>Gagal Mengeksekusi: ${e.message}</b>`;
      terminalRawWrap.classList.remove('hidden');
      terminalOutput.innerText = e.message;
      this.renderPalette();
    }
  },

  // ==================== SUBMIT EXAM & RESULTS ====================
  confirmSubmitExam() {
    this.saveCurrentAnswer();
    const answeredCount = Object.keys(this.answers).filter(k => String(this.answers[k]).trim() !== '').length;
    const totalQ = this.currentExam.questions.length;

    const msg = `Apakah Anda yakin ingin mengumpulkan ujian ini?\n\nAnda telah menjawab ${answeredCount} dari ${totalQ} soal.\nSetelah dikumpulkan, nilai Anda akan langsung dinilai oleh sistem.`;
    if (confirm(msg)) {
      this.executeSubmit();
    }
  },

  async executeSubmit() {
    if (this.timerInterval) clearInterval(this.timerInterval);
    this.saveCurrentAnswer();

    const durationTaken = this.totalSeconds - this.remainingSeconds;
    App.showToast("Menilai lembar jawaban dan menghitung skor akhir...", "info");

    try {
      const res = await API.submitExam(
        this.currentExam.id,
        this.studentInfo,
        this.answers,
        durationTaken
      );

      if (res.success) {
        if (!this.studentAttemptedExamIds.includes(this.currentExam.id)) {
          this.studentAttemptedExamIds.push(this.currentExam.id);
        }
        this.updateStudentAuthState();
        this.renderResult(res.result, durationTaken);
        this.switchView('result');
        App.showToast("Ujian berhasil dikumpulkan!", "success");
      } else {
        App.showToast(`Gagal mengumpulkan: ${res.error}`, "error");
      }
    } catch (e) {
      App.showToast(`Error submit: ${e.message}`, "error");
    }
  },

  renderResult(res, durationTaken) {
    document.getElementById('result-exam-title-display').innerText = this.currentExam.title;
    document.getElementById('result-score-val').innerText = res.score.toFixed(1);

    const predBadge = document.getElementById('result-predicate-badge');
    predBadge.innerText = res.predicate;
    if (res.is_passed) {
      predBadge.className = 'result-predicate-pill pass';
      document.getElementById('result-trophy-icon').innerText = '🏆';
    } else {
      predBadge.className = 'result-predicate-pill remedial';
      document.getElementById('result-trophy-icon').innerText = '📝';
    }

    document.getElementById('result-student-name').innerText = this.studentInfo.name;
    document.getElementById('result-student-class').innerText = `${this.studentInfo.class_name} • NISN: ${this.studentInfo.nisn}`;
    document.getElementById('result-points-earned').innerText = `${res.earned_points} / ${res.total_points}`;

    const mins = Math.floor(durationTaken / 60);
    const secs = durationTaken % 60;
    document.getElementById('result-duration-val').innerText = `${String(mins).padStart(2, '0')}m ${String(secs).padStart(2, '0')}s`;

    // Render detailed breakdown list
    const list = document.getElementById('result-breakdown-list');
    list.innerHTML = res.results.map((item, i) => `
      <div class="result-item-card ${item.is_correct ? 'correct' : 'incorrect'}">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px;">
          <div style="display: flex; align-items: center; gap: 8px;">
            <span style="font-size: 1.15rem;">${item.is_correct ? '✅' : '❌'}</span>
            <b style="font-size: 0.9rem; color: var(--text-main);">Nomor ${i + 1} (${item.question_type === 'mcq' ? 'Pilihan Ganda' : 'Praktik Coding'})</b>
          </div>
          <span style="font-size: 0.76rem; font-weight: 700; color: ${item.is_correct ? '#059669' : '#e11d48'};">
            ${item.is_correct ? `+${item.points} Poin` : '0 Poin'}
          </span>
        </div>
        <p style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 6px;">${item.question_text}</p>
        <div style="font-size: 0.74rem; background: #ffffff; padding: 6px 10px; border-radius: 4px; border: 1px solid var(--border-subtle); font-family: var(--font-mono);">
          <b>Status Output / Jawaban:</b> ${item.output_info}
        </div>
      </div>
    `).join('');
  },

  // ==================== ADMIN DASHBOARD ====================
  async handleAdminLogin() {
    const user = document.getElementById('admin-login-user').value.trim();
    const pass = document.getElementById('admin-login-pass').value.trim();
    const errEl = document.getElementById('admin-login-error');

    errEl.style.display = 'none';

    try {
      const res = await API.adminLogin(user, pass);
      if (res.success) {
        this.adminToken = res.token;
        localStorage.setItem('elearning_admin_token', res.token);
        document.getElementById('modal-admin-login').classList.remove('open');
        this.switchView('admin');
        this.loadAdminData();
        App.showToast("Login Guru Berhasil!", "success");
      } else {
        errEl.innerText = res.error || "Login gagal.";
        errEl.style.display = 'block';
      }
    } catch (e) {
      errEl.innerText = e.message;
      errEl.style.display = 'block';
    }
  },

  async loadAdminData() {
    this.loadAdminExamsTable();
    this.loadAdminSubmissionsTable();
    this.loadAdminStudents();
  },

  async loadAdminExamsTable() {
    const tbody = document.getElementById('admin-exams-table-body');
    if (!tbody) return;

    try {
      const res = await API.getExams();
      if (res.success && res.exams.length > 0) {
        tbody.innerHTML = res.exams.map(exam => {
          let classBadge = '';
          const titleDesc = ((exam.title || '') + ' ' + (exam.description || '')).toLowerCase();
          if (titleDesc.includes('xi') || titleDesc.includes('xii')) {
            classBadge = ` <span class="nav-tag amber" style="font-size: 0.68rem; font-weight: 700; padding: 1px 6px;">Kelas XI & XII</span>`;
          } else if (titleDesc.includes('kelas x') || titleDesc.includes('kelas 10')) {
            classBadge = ` <span class="nav-tag purple" style="font-size: 0.68rem; font-weight: 700; padding: 1px 6px;">Kelas X</span>`;
          }

          return `
          <tr>
            <td>#${exam.id}</td>
            <td><b>${exam.title}</b></td>
            <td><span class="nav-tag purple">${exam.subject}</span>${classBadge}</td>
            <td><b>⏱️ ${exam.duration_minutes} Menit</b></td>
            <td>${exam.question_count || 0} Soal (${exam.total_points || 0} Poin)</td>
            <td>
              <div style="display: flex; gap: 6px;">
                <button class="btn btn-secondary btn-sm" onclick="ELearning.openEditExamModal(${exam.id})" title="Edit Paket Kuis & Kelola Soal">
                  ✏️ Edit
                </button>
                <button class="btn btn-secondary btn-sm" onclick="ELearning.openAddQuestionModal(${exam.id})" title="Tambah Butir Soal">
                  ➕ Soal
                </button>
                <button class="btn btn-secondary btn-sm" style="color: var(--accent-rose);" onclick="ELearning.handleDeleteExam(${exam.id})" title="Hapus Paket Ujian">
                  🗑️
                </button>
              </div>
            </td>
          </tr>
        `;
        }).join('');
      } else {
        tbody.innerHTML = `<tr><td colspan="6" style="text-align: center; color: var(--text-dim);">Belum ada paket ujian. Klik "Buat Paket Ujian Baru".</td></tr>`;
      }
    } catch (e) {
      tbody.innerHTML = `<tr><td colspan="6" style="color: var(--accent-rose);">Error: ${e.message}</td></tr>`;
    }
  },

  async loadAdminSubmissionsTable() {
    const tbody = document.getElementById('admin-submissions-table-body');
    if (!tbody) return;

    const classEl = document.getElementById('filter-score-class');
    const dateEl = document.getElementById('filter-score-date');
    const classFilter = classEl ? classEl.value.trim() : '';
    const dateFilter = dateEl ? dateEl.value.trim() : '';

    try {
      const res = await API.getAdminSubmissions(null, classFilter, dateFilter);
      if (res.success && res.submissions.length > 0) {
        tbody.innerHTML = res.submissions.map(sub => {
          const mins = Math.floor(sub.duration_seconds / 60);
          const secs = sub.duration_seconds % 60;
          const durStr = `${String(mins).padStart(2, '0')}m ${String(secs).padStart(2, '0')}s`;
          const isPass = sub.score >= 75.0;

          return `
            <tr>
              <td><small>${sub.submitted_at.slice(0, 16)}</small></td>
              <td><b>${sub.student_name}</b></td>
              <td>${sub.student_nisn}</td>
              <td><span class="nav-tag green">${sub.student_class}</span></td>
              <td>${sub.exam_title}</td>
              <td><b style="font-size: 1.05rem; color: ${isPass ? '#059669' : '#e11d48'};">${sub.score.toFixed(1)}</b></td>
              <td>
                <span class="result-predicate-pill ${isPass ? 'pass' : 'remedial'}" style="font-size: 0.68rem; padding: 2px 8px;">
                  ${isPass ? 'KOMPETEN' : 'REMEDIAL'}
                </span>
              </td>
              <td><small>${durStr}</small></td>
              <td>
                <div style="display: flex; gap: 6px;">
                  <button class="btn btn-secondary btn-sm" style="padding: 3px 8px; font-size: 0.74rem; color: #0284c7;" onclick="ELearning.openEditScoreModal(${sub.id}, ${sub.score}, '${sub.student_name.replace(/'/g, "\\'")}', '${sub.exam_title.replace(/'/g, "\\'")}')" title="Edit Nilai">
                    ✏️ Edit
                  </button>
                  <button class="btn btn-secondary btn-sm" style="padding: 3px 8px; font-size: 0.74rem; color: var(--accent-rose);" onclick="ELearning.handleDeleteSubmission(${sub.id}, '${sub.student_name.replace(/'/g, "\\'")}', '${sub.exam_title.replace(/'/g, "\\'")}')" title="Hapus Nilai">
                    🗑️ Hapus
                  </button>
                </div>
              </td>
            </tr>
          `;
        }).join('');
      } else {
        const filterNotice = (classFilter || dateFilter) ? ' yang cocok dengan kriteria filter' : '';
        tbody.innerHTML = `<tr><td colspan="9" style="text-align: center; color: var(--text-dim); padding: 24px;">Belum ada riwayat nilai siswa${filterNotice}.</td></tr>`;
      }
    } catch (e) {
      tbody.innerHTML = `<tr><td colspan="8" style="color: var(--accent-rose);">Error: ${e.message}</td></tr>`;
    }
  },

  async handleCreateExam() {
    const title = document.getElementById('new-exam-title').value.trim();
    const subject = document.getElementById('new-exam-subject').value.trim();
    const duration = parseInt(document.getElementById('new-exam-duration').value) || 30;
    const desc = document.getElementById('new-exam-desc').value.trim();

    if (!title || !subject) {
      App.showToast("Judul dan Mata Pelajaran wajib diisi!", "error");
      return;
    }

    try {
      const res = await API.createExam(title, desc, subject, duration);
      if (res.success) {
        document.getElementById('modal-create-exam').classList.remove('open');
        this.loadAdminExamsTable();
        App.showToast("Paket ujian baru berhasil disimpan!", "success");
      } else {
        App.showToast(res.error, "error");
      }
    } catch (e) {
      App.showToast(e.message, "error");
    }
  },

  openAddQuestionModal(examId) {
    document.getElementById('modal-q-exam-id').value = examId;
    document.getElementById('new-q-text').value = '';
    document.getElementById('new-q-starter-code').value = '';
    document.getElementById('new-q-expected-output').value = '';
    document.getElementById('modal-add-question').classList.add('open');
  },

  async handleSaveQuestion() {
    const examId = parseInt(document.getElementById('modal-q-exam-id').value);
    const qType = document.getElementById('new-q-type').value;
    const qText = document.getElementById('new-q-text').value.trim();
    const points = parseInt(document.getElementById('new-q-points').value) || 20;

    if (!qText) {
      App.showToast("Teks pertanyaan tidak boleh kosong!", "error");
      return;
    }

    let options = null;
    let correctAnswer = null;
    let starterCode = null;
    let expectedOutput = null;

    if (qType === 'mcq') {
      const optA = document.getElementById('new-q-opt-a').value.trim() || 'Pilihan A';
      const optB = document.getElementById('new-q-opt-b').value.trim() || 'Pilihan B';
      const optC = document.getElementById('new-q-opt-c').value.trim() || 'Pilihan C';
      const optD = document.getElementById('new-q-opt-d').value.trim() || 'Pilihan D';
      options = [`A. ${optA}`, `B. ${optB}`, `C. ${optC}`, `D. ${optD}`];
      correctAnswer = document.getElementById('new-q-correct-ans').value;
    } else {
      starterCode = document.getElementById('new-q-starter-code').value;
      expectedOutput = document.getElementById('new-q-expected-output').value;
    }

    try {
      const res = await API.addQuestion(examId, qType, qText, options, correctAnswer, starterCode, expectedOutput, points);
      if (res.success) {
        document.getElementById('modal-add-question').classList.remove('open');
        this.loadAdminExamsTable();
        if (this.currentAdminExam && this.currentAdminExam.id === examId) {
          this.openEditExamModal(examId);
        }
        App.showToast("Butir soal berhasil ditambahkan!", "success");
      } else {
        App.showToast(res.error, "error");
      }
    } catch (e) {
      App.showToast(e.message, "error");
    }
  },

  async handleDeleteExam(examId) {
    if (confirm(`Yakin ingin menghapus paket ujian #${examId}? Seluruh butir soal dan data nilai ujian ini akan ikut terhapus.`)) {
      try {
        const res = await API.deleteExam(examId);
        if (res.success) {
          this.loadAdminExamsTable();
          App.showToast("Paket ujian berhasil dihapus.", "success");
        }
      } catch (e) {
        App.showToast(e.message, "error");
      }
    }
  },

  // ==================== ADMIN EDIT EXAM & KELOLA SOAL ====================
  currentAdminExam: null,

  async openEditExamModal(examId) {
    try {
      const res = await API.getAdminExam(examId);
      if (!res.success || !res.exam) {
        App.showToast("Gagal memuat data paket kuis: " + (res.error || 'Ujian tidak ditemukan'), "error");
        return;
      }

      const exam = res.exam;
      this.currentAdminExam = exam;

      document.getElementById('edit-exam-id').value = exam.id;
      document.getElementById('edit-exam-title').value = exam.title || '';
      document.getElementById('edit-exam-subject').value = exam.subject || '';
      document.getElementById('edit-exam-duration').value = exam.duration_minutes || 30;
      document.getElementById('edit-exam-desc').value = exam.description || '';

      const addBtn = document.getElementById('btn-edit-exam-add-q');
      if (addBtn) {
        addBtn.onclick = () => {
          this.openAddQuestionModal(exam.id);
        };
      }

      this.renderAdminExamQuestions(exam);

      const modal = document.getElementById('modal-edit-exam');
      if (modal) modal.classList.add('open');
    } catch (e) {
      App.showToast(`Error: ${e.message}`, "error");
    }
  },

  closeEditExamModal() {
    const modal = document.getElementById('modal-edit-exam');
    if (modal) modal.classList.remove('open');
  },

  async handleSaveEditExam() {
    const examId = parseInt(document.getElementById('edit-exam-id').value);
    const title = document.getElementById('edit-exam-title').value.trim();
    const subject = document.getElementById('edit-exam-subject').value.trim();
    const duration = parseInt(document.getElementById('edit-exam-duration').value) || 30;
    const desc = document.getElementById('edit-exam-desc').value.trim();

    if (!title || !subject) {
      App.showToast("Judul kuis dan mata pelajaran wajib diisi!", "error");
      return;
    }

    try {
      const res = await API.updateExam(examId, {
        title: title,
        subject: subject,
        duration_minutes: duration,
        description: desc,
        is_active: 1
      });

      if (res.success) {
        App.showToast("Informasi paket kuis berhasil diperbarui! 🎉", "success");
        this.loadAdminExamsTable();
        if (this.currentAdminExam && this.currentAdminExam.id === examId) {
          this.currentAdminExam.title = title;
          this.currentAdminExam.subject = subject;
          this.currentAdminExam.duration_minutes = duration;
          this.currentAdminExam.description = desc;
        }
      } else {
        App.showToast(res.error || "Gagal memperbarui paket kuis.", "error");
      }
    } catch (e) {
      App.showToast(`Error: ${e.message}`, "error");
    }
  },

  renderAdminExamQuestions(exam) {
    const container = document.getElementById('edit-exam-questions-list');
    const badge = document.getElementById('edit-exam-q-count-badge');
    if (!container) return;

    const questions = exam.questions || [];
    const totalPoints = questions.reduce((acc, q) => acc + (q.points || 0), 0);

    if (badge) {
      badge.innerText = `${questions.length} Butir Soal (${totalPoints} Poin)`;
    }

    if (questions.length === 0) {
      container.innerHTML = `
        <div style="text-align: center; color: var(--text-dim); padding: 24px; border: 1px dashed var(--border-subtle); border-radius: 8px;">
          Belum ada butir soal di paket kuis ini. Klik tombol <b>"➕ Tambah Butir Soal Baru"</b> di atas.
        </div>
      `;
      return;
    }

    container.innerHTML = questions.map((q, idx) => {
      let typeLabel = 'Pilihan Ganda';
      let typeClass = 'purple';
      let typeIcon = '🔘';

      if (q.question_type === 'code_python') {
        typeLabel = 'Coding Python';
        typeClass = 'green';
        typeIcon = '🐍';
      } else if (q.question_type === 'code_sql') {
        typeLabel = 'Coding SQL';
        typeClass = 'cyan';
        typeIcon = '🗄️';
      }

      let answerSnippet = '';
      if (q.question_type === 'mcq') {
        const correct = q.correct_answer || '-';
        answerSnippet = `<span style="font-size: 0.75rem; color: #059669; font-weight: 600;">Kunci: <b>${correct}</b></span>`;
      } else {
        const exp = (q.expected_output || '').trim();
        const shortExp = exp.length > 40 ? exp.slice(0, 37) + '...' : exp;
        answerSnippet = `<span style="font-size: 0.72rem; color: #4b5563; font-family: var(--font-mono);">Output: <code>${shortExp || '-'}</code></span>`;
      }

      return `
        <div style="background: #ffffff; border: 1px solid var(--border-subtle); border-radius: 8px; padding: 10px 12px; display: flex; flex-direction: column; gap: 6px;">
          <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 6px;">
            <div style="display: flex; align-items: center; gap: 8px;">
              <b style="font-size: 0.85rem; color: var(--text-main);">No. ${idx + 1}</b>
              <span class="nav-tag ${typeClass}" style="font-size: 0.7rem; padding: 2px 7px;">${typeIcon} ${typeLabel}</span>
              <span style="font-size: 0.74rem; font-weight: 700; color: #2563eb; background: rgba(37, 99, 235, 0.08); padding: 2px 8px; border-radius: 9999px;">
                ${q.points} Poin
              </span>
            </div>
            <div style="display: flex; align-items: center; gap: 6px;">
              <button class="btn btn-secondary btn-sm" onclick="ELearning.openEditQuestionModal(${q.id})" style="padding: 3px 8px; font-size: 0.75rem;" title="Edit isi butir soal">
                ✏️ Edit
              </button>
              <button class="btn btn-secondary btn-sm" style="padding: 3px 8px; font-size: 0.75rem; color: var(--accent-rose);" onclick="ELearning.handleDeleteQuestionFromExam(${q.id}, ${exam.id})" title="Hapus butir soal">
                🗑️
              </button>
            </div>
          </div>
          <div style="font-size: 0.82rem; color: var(--text-main); font-weight: 500; line-height: 1.4;">
            ${q.question_text}
          </div>
          <div style="display: flex; align-items: center; justify-content: space-between; background: #f8fafc; padding: 4px 8px; border-radius: 4px; border: 1px solid #e2e8f0;">
            ${answerSnippet}
            <span style="font-size: 0.68rem; color: var(--text-dim);">ID #${q.id}</span>
          </div>
        </div>
      `;
    }).join('');
  },

  async openEditQuestionModal(questionId) {
    let q = null;
    if (this.currentAdminExam && this.currentAdminExam.questions) {
      q = this.currentAdminExam.questions.find(item => item.id === questionId);
    }
    if (!q) {
      try {
        const res = await API.getQuestion(questionId);
        if (res.success && res.question) q = res.question;
      } catch (e) {
        console.warn("Could not fetch question via API:", e);
      }
    }

    if (!q) {
      App.showToast("Butir soal tidak ditemukan.", "error");
      return;
    }

    document.getElementById('edit-q-id').value = q.id;
    document.getElementById('edit-q-exam-id').value = q.exam_id;
    document.getElementById('edit-q-type').value = q.question_type || 'mcq';
    document.getElementById('edit-q-points').value = q.points || 20;
    document.getElementById('edit-q-text').value = q.question_text || '';

    const isMcq = (q.question_type === 'mcq');
    document.getElementById('edit-q-mcq-fields').classList.toggle('hidden', !isMcq);
    document.getElementById('edit-q-code-fields').classList.toggle('hidden', isMcq);

    if (isMcq) {
      const opts = q.options || [];
      const stripPrefix = (str, prefix) => {
        if (!str) return '';
        if (str.startsWith(prefix + '. ') || str.startsWith(prefix + ') ') || str.startsWith(prefix + ' : ')) {
          return str.slice(3).trim();
        }
        return str;
      };

      document.getElementById('edit-q-opt-a').value = stripPrefix(opts[0] || '', 'A');
      document.getElementById('edit-q-opt-b').value = stripPrefix(opts[1] || '', 'B');
      document.getElementById('edit-q-opt-c').value = stripPrefix(opts[2] || '', 'C');
      document.getElementById('edit-q-opt-d').value = stripPrefix(opts[3] || '', 'D');
      document.getElementById('edit-q-correct-ans').value = (q.correct_answer || 'A').toUpperCase().trim();
    } else {
      document.getElementById('edit-q-starter-code').value = q.starter_code || '';
      document.getElementById('edit-q-expected-output').value = q.expected_output || '';
    }

    const modal = document.getElementById('modal-edit-question');
    if (modal) modal.classList.add('open');
  },

  closeEditQuestionModal() {
    const modal = document.getElementById('modal-edit-question');
    if (modal) modal.classList.remove('open');
  },

  async handleSaveEditQuestion() {
    const qId = parseInt(document.getElementById('edit-q-id').value);
    const examId = parseInt(document.getElementById('edit-q-exam-id').value);
    const qType = document.getElementById('edit-q-type').value;
    const qText = document.getElementById('edit-q-text').value.trim();
    const points = parseInt(document.getElementById('edit-q-points').value) || 20;

    if (!qText) {
      App.showToast("Teks pertanyaan tidak boleh kosong!", "error");
      return;
    }

    let options = null;
    let correctAnswer = null;
    let starterCode = null;
    let expectedOutput = null;

    if (qType === 'mcq') {
      const optA = document.getElementById('edit-q-opt-a').value.trim() || 'Pilihan A';
      const optB = document.getElementById('edit-q-opt-b').value.trim() || 'Pilihan B';
      const optC = document.getElementById('edit-q-opt-c').value.trim() || 'Pilihan C';
      const optD = document.getElementById('edit-q-opt-d').value.trim() || 'Pilihan D';
      options = [`A. ${optA}`, `B. ${optB}`, `C. ${optC}`, `D. ${optD}`];
      correctAnswer = document.getElementById('edit-q-correct-ans').value;
    } else {
      starterCode = document.getElementById('edit-q-starter-code').value;
      expectedOutput = document.getElementById('edit-q-expected-output').value;
    }

    try {
      const res = await API.updateQuestion(qId, {
        question_type: qType,
        question_text: qText,
        options: options,
        correct_answer: correctAnswer,
        starter_code: starterCode,
        expected_output: expectedOutput,
        points: points
      });

      if (res.success) {
        this.closeEditQuestionModal();
        App.showToast("Butir soal berhasil diperbarui! 🎉", "success");
        if (examId) {
          await this.openEditExamModal(examId);
        }
        this.loadAdminExamsTable();
      } else {
        App.showToast(res.error || "Gagal memperbarui soal.", "error");
      }
    } catch (e) {
      App.showToast(`Error: ${e.message}`, "error");
    }
  },

  async handleDeleteQuestionFromExam(questionId, examId) {
    if (confirm(`Yakin ingin menghapus butir soal #${questionId} ini?`)) {
      try {
        const res = await API.deleteQuestion(questionId);
        if (res.success) {
          App.showToast("Butir soal berhasil dihapus.", "success");
          if (examId) {
            await this.openEditExamModal(examId);
          }
          this.loadAdminExamsTable();
        } else {
          App.showToast(res.error || "Gagal menghapus butir soal.", "error");
        }
      } catch (e) {
        App.showToast(`Error: ${e.message}`, "error");
      }
    }
  },

  // ==================== ADMIN MASTER DATA SISWA ====================
  async loadAdminStudents() {
    const tbody = document.getElementById('admin-students-table-body');
    if (!tbody) return;

    const classEl = document.getElementById('filter-student-class');
    const nameEl = document.getElementById('filter-student-name');
    const countBadge = document.getElementById('admin-students-count-badge');

    const className = classEl ? classEl.value.trim() : '';
    const studentName = nameEl ? nameEl.value.trim() : '';

    try {
      const res = await API.getAdminStudents(className, studentName);
      if (res.success && res.students && res.students.length > 0) {
        if (countBadge) countBadge.innerText = `${res.students.length} Siswa`;
        tbody.innerHTML = res.students.map(st => `
          <tr>
            <td>#${st.id}</td>
            <td><b style="font-family: var(--font-mono); color: #065f46;">${st.nisn}</b></td>
            <td><b>${st.name}</b></td>
            <td><span class="nav-tag green">${st.class_name}</span></td>
            <td><small>${(st.created_at || '').slice(0, 16)}</small></td>
            <td>
              <button class="btn btn-secondary btn-sm" style="color: var(--accent-rose);" onclick="ELearning.deleteAdminStudent(${st.id}, '${st.name.replace(/'/g, "\\'")}')">
                🗑️ Hapus
              </button>
            </td>
          </tr>
        `).join('');
      } else {
        if (countBadge) countBadge.innerText = `0 Siswa`;
        tbody.innerHTML = `<tr><td colspan="6" style="text-align: center; color: var(--text-dim); padding: 24px;">Tidak ada siswa yang sesuai dengan filter kelas atau kata kunci pencarian.</td></tr>`;
      }
    } catch (e) {
      if (countBadge) countBadge.innerText = `Error`;
      tbody.innerHTML = `<tr><td colspan="6" style="color: var(--accent-rose);">Error: ${e.message}</td></tr>`;
    }
  },

  async handleAdminAddStudent() {
    const nisnInput = document.getElementById('admin-new-student-nisn');
    const nameInput = document.getElementById('admin-new-student-name');
    const classSelect = document.getElementById('admin-new-student-class');

    const nisn = nisnInput ? nisnInput.value.trim() : '';
    const name = nameInput ? nameInput.value.trim() : '';
    const className = classSelect ? classSelect.value.trim() : 'XII - SMK Cahaya Pertiwi';

    if (!nisn || !name) {
      App.showToast("NISN dan Nama Lengkap Siswa wajib diisi!", "error");
      return;
    }

    try {
      const res = await API.addAdminStudent(nisn, name, className);
      if (res.success) {
        if (nisnInput) nisnInput.value = '';
        if (nameInput) nameInput.value = '';
        this.loadAdminStudents();
        App.showToast(`Siswa ${name} (NISN: ${nisn}) berhasil didaftarkan ke Master Database!`, "success");
      } else {
        App.showToast(`Gagal mendaftarkan siswa: ${res.error}`, "error");
      }
    } catch (e) {
      App.showToast(`Error: ${e.message}`, "error");
    }
  },

  async deleteAdminStudent(studentId, studentName) {
    if (confirm(`Yakin ingin menghapus siswa ${studentName} (ID #${studentId}) dari Master Database SMK Cahaya Pertiwi? Siswa ini tidak akan bisa login lagi.`)) {
      try {
        const res = await API.deleteAdminStudent(studentId);
        if (res.success) {
          this.loadAdminStudents();
          App.showToast(`Data siswa ${studentName} berhasil dihapus.`, "success");
        } else {
          App.showToast(`Gagal menghapus: ${res.error}`, "error");
        }
      } catch (e) {
        App.showToast(`Error: ${e.message}`, "error");
      }
    }
  },

  // ==================== EDIT & HAPUS NILAI SISWA ====================
  openEditScoreModal(subId, currentScore, studentName, examTitle) {
    const subIdInput = document.getElementById('edit-score-sub-id');
    const nameInput = document.getElementById('edit-score-student-name');
    const titleInput = document.getElementById('edit-score-exam-title');
    const scoreInput = document.getElementById('edit-score-val');
    const modal = document.getElementById('modal-edit-score');

    if (subIdInput) subIdInput.value = subId;
    if (nameInput) nameInput.value = studentName;
    if (titleInput) titleInput.value = examTitle;
    if (scoreInput) scoreInput.value = parseFloat(currentScore).toFixed(1);
    if (modal) {
      modal.classList.add('open');
      setTimeout(() => { if (scoreInput) scoreInput.focus(); }, 100);
    }
  },

  async handleSaveEditedScore() {
    const subId = parseInt(document.getElementById('edit-score-sub-id').value);
    const scoreVal = parseFloat(document.getElementById('edit-score-val').value);

    if (isNaN(scoreVal) || scoreVal < 0 || scoreVal > 100) {
      App.showToast("Harap masukkan nilai valid antara 0 sampai 100!", "error");
      return;
    }

    try {
      const res = await API.updateSubmissionScore(subId, scoreVal);
      if (res.success) {
        const modal = document.getElementById('modal-edit-score');
        if (modal) modal.classList.remove('open');
        this.loadAdminSubmissionsTable();
        App.showToast(res.message || `Nilai berhasil diperbarui menjadi ${scoreVal}!`, "success");
      } else {
        App.showToast(`Gagal menyimpan perubahan: ${res.error}`, "error");
      }
    } catch (e) {
      App.showToast(`Error: ${e.message}`, "error");
    }
  },

  async handleDeleteSubmission(subId, studentName, examTitle) {
    const confirmMsg = `Yakin ingin menghapus rekaman nilai siswa berikut?\n\n• Nama: ${studentName}\n• Ujian: ${examTitle}\n\nSetelah dihapus, rekaman nilai ini akan hilang dari rekapitulasi dan siswa akan dapat mengerjakan ulang ujian tersebut.`;
    if (confirm(confirmMsg)) {
      try {
        const res = await API.deleteSubmission(subId);
        if (res.success) {
          this.loadAdminSubmissionsTable();
          App.showToast(`Data nilai ${studentName} berhasil dihapus.`, "success");
        } else {
          App.showToast(`Gagal menghapus nilai: ${res.error}`, "error");
        }
      } catch (e) {
        App.showToast(`Error: ${e.message}`, "error");
      }
    }
  },

  async handleChangeAdminPassword() {
    const oldPass = (document.getElementById('change-pass-old')?.value || '').trim();
    const newPass = (document.getElementById('change-pass-new')?.value || '').trim();
    const confirmPass = (document.getElementById('change-pass-confirm')?.value || '').trim();
    const errEl = document.getElementById('change-pass-error');
    const succEl = document.getElementById('change-pass-success');

    if (errEl) errEl.style.display = 'none';
    if (succEl) succEl.style.display = 'none';

    if (!oldPass || !newPass) {
      if (errEl) {
        errEl.innerText = "Password lama dan password baru wajib diisi.";
        errEl.style.display = 'block';
      }
      return;
    }

    if (newPass.length < 5) {
      if (errEl) {
        errEl.innerText = "Password baru minimal 5 karakter demi keamanan.";
        errEl.style.display = 'block';
      }
      return;
    }

    if (newPass !== confirmPass) {
      if (errEl) {
        errEl.innerText = "Konfirmasi password baru tidak cocok!";
        errEl.style.display = 'block';
      }
      return;
    }

    try {
      const res = await API.adminChangePassword(oldPass, newPass, confirmPass, 'guru');
      if (res.success) {
        if (succEl) {
          succEl.innerText = res.message || "Password berhasil diperbarui!";
          succEl.style.display = 'block';
        }
        App.showToast("Password akun Guru berhasil diubah!", "success");
        setTimeout(() => {
          const modal = document.getElementById('modal-change-password');
          if (modal) modal.classList.remove('open');
        }, 1200);
      } else {
        if (errEl) {
          errEl.innerText = res.error || "Gagal mengubah password.";
          errEl.style.display = 'block';
        }
      }
    } catch (e) {
      if (errEl) {
        errEl.innerText = e.message;
        errEl.style.display = 'block';
      }
    }
  },

  currentCardNisn: null,
  currentCardAttempts: [],

  async openStudentGradeCard(nisn) {
    const cleanNisn = (nisn || '').trim();
    if (!cleanNisn) return;
    this.currentCardNisn = cleanNisn;

    const modal = document.getElementById('modal-student-grade-card');
    const tbody = document.getElementById('card-exams-tbody');
    const breakdownBox = document.getElementById('card-detail-breakdown-box');
    if (breakdownBox) breakdownBox.style.display = 'none';

    if (modal) modal.classList.add('open');
    if (tbody) {
      tbody.innerHTML = `<tr><td colspan="7" style="text-align:center; padding:20px; color:var(--text-dim);">Memuat data kartu nilai...</td></tr>`;
    }

    try {
      const res = await API.getStudentCardData(cleanNisn);
      if (!res.success || !res.data) {
        App.showToast(res.error || "Gagal memuat kartu nilai siswa.", "error");
        if (tbody) tbody.innerHTML = `<tr><td colspan="7" style="text-align:center; padding:20px; color:#ef4444;">${res.error || 'Data tidak ditemukan.'}</td></tr>`;
        return;
      }

      const { student, attempts, summary } = res.data;
      this.currentCardAttempts = attempts || [];

      // Update student profile info
      const nameEl = document.getElementById('card-student-name');
      const nisnEl = document.getElementById('card-student-nisn');
      const classEl = document.getElementById('card-student-class');
      if (nameEl) nameEl.innerText = student.name;
      if (nisnEl) nisnEl.innerText = student.nisn;
      if (classEl) classEl.innerText = student.class_name;

      // Update summary KPI
      const totalEl = document.getElementById('card-total-exams');
      const avgEl = document.getElementById('card-avg-score');
      const statusEl = document.getElementById('card-status-badge');
      const passFailEl = document.getElementById('card-pass-fail-count');
      const predicateEl = document.getElementById('card-predicate');

      if (totalEl) totalEl.innerText = `${summary.total_exams} Paket`;
      if (avgEl) {
        avgEl.innerText = summary.average_score.toFixed(1);
        avgEl.style.color = summary.overall_passed ? '#059669' : '#e11d48';
      }
      if (statusEl) {
        statusEl.innerText = summary.overall_passed ? '✅ KOMPETEN' : (summary.total_exams > 0 ? '⚠️ REMEDIAL' : '-');
        statusEl.style.color = summary.overall_passed ? '#059669' : '#e11d48';
      }
      if (passFailEl) {
        passFailEl.innerText = `${summary.passed_count} Lulus / ${summary.remedial_count} Remedial`;
      }
      if (predicateEl) {
        predicateEl.innerText = summary.predicate;
      }

      // Update Active Card counter too
      const activeCountEl = document.getElementById('active-student-exam-count');
      if (activeCountEl) activeCountEl.innerText = summary.total_exams;

      // Render Table
      if (!attempts || attempts.length === 0) {
        if (tbody) {
          tbody.innerHTML = `
            <tr>
              <td colspan="7" style="text-align: center; padding: 28px 16px; color: var(--text-muted);">
                <div style="font-size: 1.8rem; margin-bottom: 6px;">📚</div>
                <b>Belum Ada Riwayat Ujian</b>
                <p style="font-size: 0.74rem; color: var(--text-dim); margin-top: 4px;">
                  Siswa ini belum pernah menyelesaikan paket kuis atau ulangan CBT. Silakan kerjakan paket soal yang tersedia di lobi.
                </p>
              </td>
            </tr>
          `;
        }
        return;
      }

      if (tbody) {
        tbody.innerHTML = attempts.map((att, idx) => {
          const score = parseFloat(att.score || 0);
          const isPassed = (att.is_passed === 1 || score >= 75.0);
          const durSec = att.duration_seconds || 0;
          const durStr = `${Math.floor(durSec / 60)}m ${durSec % 60}s`;
          const subTime = (att.submitted_at || '').substring(0, 16).replace('T', ' ');

          return `
            <tr>
              <td style="text-align: center;">${idx + 1}</td>
              <td>
                <b>${att.exam_title}</b>
                <span class="nav-tag purple" style="font-size: 0.68rem; margin-left: 6px;">${att.exam_subject || 'Umum'}</span>
              </td>
              <td style="text-align: center; font-size: 0.74rem; color: var(--text-muted);">${subTime}</td>
              <td style="text-align: center;"><b>⏱️ ${durStr}</b></td>
              <td style="text-align: center; font-size: 0.92rem; font-weight: 800; color: ${isPassed ? '#059669' : '#e11d48'};">
                ${score.toFixed(1)}
              </td>
              <td style="text-align: center;">
                <span class="nav-tag ${isPassed ? 'green' : 'rose'}" style="font-weight: 700; font-size: 0.7rem;">
                  ${isPassed ? '✅ KOMPETEN' : '⚠️ REMEDIAL'}
                </span>
              </td>
              <td style="text-align: center;">
                <button class="btn btn-secondary btn-sm" onclick="elearning.showCardExamDetail(${att.id})" style="font-size: 0.72rem; padding: 3px 8px;" title="Lihat rincian jawaban butir soal">
                  🔍 Rincian
                </button>
              </td>
            </tr>
          `;
        }).join('');
      }
    } catch (e) {
      App.showToast(`Error: ${e.message}`, "error");
      if (tbody) {
        tbody.innerHTML = `<tr><td colspan="7" style="text-align:center; padding:20px; color:#ef4444;">Error: ${e.message}</td></tr>`;
      }
    }
  },

  showCardExamDetail(attemptId) {
    const att = (this.currentCardAttempts || []).find(a => a.id === attemptId);
    if (!att) return;

    const breakdownBox = document.getElementById('card-detail-breakdown-box');
    const titleEl = document.getElementById('card-detail-title');
    const listEl = document.getElementById('card-detail-list');
    if (!breakdownBox || !listEl) return;

    titleEl.innerText = `🔍 Rincian Butir Soal: ${att.exam_title} (Skor: ${parseFloat(att.score).toFixed(1)} / 100)`;
    
    const details = att.results_detail || [];
    if (details.length === 0) {
      listEl.innerHTML = `<div style="font-size: 0.78rem; color: var(--text-dim); padding: 8px;">Rincian evaluasi butir soal tidak tersedia.</div>`;
    } else {
      listEl.innerHTML = details.map((d, i) => `
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 6px; padding: 8px 12px; font-size: 0.78rem;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
            <div>
              <span style="font-size: 0.95rem; margin-right: 6px;">${d.is_correct ? '✅' : '❌'}</span>
              <b>Nomor ${i + 1} (${d.question_type === 'mcq' ? 'Pilihan Ganda' : 'Praktik Coding'})</b>
            </div>
            <span style="font-weight: 700; color: ${d.is_correct ? '#059669' : '#e11d48'};">
              ${d.is_correct ? `+${d.points} Poin` : '0 Poin'}
            </span>
          </div>
          <div style="color: var(--text-muted); font-size: 0.74rem; margin-bottom: 4px;">${d.question_text || ''}</div>
          <div style="background: #f8fafc; padding: 4px 8px; border-radius: 4px; font-family: var(--font-mono); font-size: 0.72rem; color: #0f172a;">
            <b>Status:</b> ${d.output_info || (d.is_correct ? 'Jawaban Benar' : 'Jawaban Salah')}
          </div>
        </div>
      `).join('');
    }

    breakdownBox.style.display = 'block';
    breakdownBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }
};
