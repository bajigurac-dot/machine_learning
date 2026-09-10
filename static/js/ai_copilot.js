/**
 * Studio ML Python - AI Tutor SMK, PRD Jobsheet & Panduan VS Code
 */
const AICopilot = {
  history: [],
  codeSnippets: [],
  apiKey: localStorage.getItem('studio_ml_ai_key') || '',
  provider: localStorage.getItem('studio_ml_ai_provider') || 'local',

  init() {
    this.bindEvents();
    this.renderWelcome();
  },

  bindEvents() {
    const sendBtn = document.getElementById('btn-send-chat');
    const inputField = document.getElementById('chat-input-text');

    if (sendBtn && inputField) {
      sendBtn.addEventListener('click', () => this.sendMessage());
      inputField.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          this.sendMessage();
        }
      });
    }

    // Quick prompt buttons (Belajar Looping, If-Else, Fungsi, List/Dict, ML, PRD)
    document.querySelectorAll('.btn-quick-prompt').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const prompt = e.currentTarget.getAttribute('data-prompt');
        if (inputField) {
          inputField.value = prompt;
          this.sendMessage();
        }
      });
    });

    // Generate Spec Button in tools panel
    const btnGenSpec = document.getElementById('btn-open-spec-modal');
    if (btnGenSpec) {
      btnGenSpec.addEventListener('click', () => {
        document.getElementById('modal-spec-generator').classList.add('open');
      });
    }

    // Submit Generate Spec
    const btnSubmitSpec = document.getElementById('btn-submit-spec');
    if (btnSubmitSpec) {
      btnSubmitSpec.addEventListener('click', () => this.handleGenerateSpec());
    }

    // 1-Click PRD Jobsheet Siswa
    const btnGenPRD = document.getElementById('btn-quick-prd');
    if (btnGenPRD) {
      btnGenPRD.addEventListener('click', () => this.handleGeneratePRD());
    }

    // Download Last AI Message as MD (Jobsheet / Materi)
    const btnDownloadLast = document.getElementById('btn-download-chat-md');
    if (btnDownloadLast) {
      btnDownloadLast.addEventListener('click', () => this.downloadLastOutput());
    }
  },

  renderWelcome() {
    const chatContainer = document.getElementById('chat-messages-container');
    if (!chatContainer || chatContainer.children.length > 0) return;

    this.appendMessage('ai', `### 🎓 Halo Sobat Siswa! Selamat Datang di AI Tutor Python & ML (Mentor: Thoriq Azis, S.Kom)

Saya adalah asisten AI yang siap memandu Anda belajar pemrograman Python secara terstruktur dari nol hingga mahir membuat Machine Learning mandiri dan mempraktikkannya langsung di **Visual Studio Code (VS Code)**!

**📚 Kurikulum Praktik Dasar Python & Database Sesuai Urutan:**
1. 📢 **Materi 1**: Cetak Teks ke Layar (\`print\`) & Format Teks
2. 🏷️ **Materi 2**: Variabel & Tipe Data Dasar (\`str\`, \`int\`, \`float\`, \`bool\`)
3. ⌨️ **Materi 3**: Menerima Input Pengguna (\`input()\`) & Operasi Aritmatika
4. 🔀 **Materi 4**: Percabangan & Logika Kondisi (\`if-elif-else\`)
5. 🔄 **Materi 5**: Perulangan / Looping (\`for\` & \`while\`)
6. 📑 **Materi 6**: Struktur Data Kumpulan (\`List\` & \`Dictionary\`)
7. 📦 **Materi 7**: Membuat Fungsi Modular (\`def\`, parameter & return)
8. 🛡️ **Materi 8**: Penanganan Error / Exception (\`try - except\`)
9. 🤖 **Materi 9**: Praktikum Machine Learning Pertama di VS Code
10. 📄 **Materi 10**: Pembuatan Lembar Kerja Praktikum Siswa (Jobsheet PRD)
11. 🗄️ **Materi 11**: Basis Data & Query SQL (Database Relasional SQLite di Python)

*💡 Tips: Anda bisa mengklik tombol pintasan materi di atas, mengetik nomor materinya (contoh: ketik "11" atau "database"), atau menanyakan kendala koding apa pun!*`);
  },

  async sendMessage() {
    const inputField = document.getElementById('chat-input-text');
    const msg = inputField.value.trim();
    if (!msg) return;

    inputField.value = '';
    this.appendMessage('user', msg);
    this.history.push({ role: 'user', content: msg });

    // Loading indicator
    const loadingId = this.appendLoading();

    try {
      const res = await API.sendAiChat(msg, this.history, this.apiKey, this.provider);
      this.removeLoading(loadingId);

      if (res.success) {
        let meta = null;
        if (res.provider_used && res.provider_used.includes('gemini')) {
          meta = `⚡ Dijawab oleh Google Gemini Cloud LLM (${res.provider_used})`;
        } else if (res.gemini_error) {
          meta = `<span style="color: #d97706;">⚠️ Gemini dialihkan ke Built-in Local Tutor (${res.gemini_error}).</span>`;
        } else {
          meta = '<span style="color: #059669;">🎓 Built-in Local SMK Tutor (Offline & Unlimited)</span>';
        }

        this.appendMessage('ai', res.reply, meta);
        this.history.push({ role: 'assistant', content: res.reply });
      } else {
        this.appendMessage('ai', `⚠️ Terjadi kendala: ${res.error || 'Gagal memproses pesan.'}`);
      }
    } catch (e) {
      this.removeLoading(loadingId);
      this.appendMessage('ai', `⚠️ Terjadi kesalahan jaringan: ${e.message}`);
    }
  },

  async handleGenerateSpec() {
    const name = document.getElementById('spec-feature-name').value.trim() || 'Modul Latihan Looping';
    const goal = document.getElementById('spec-feature-goal').value.trim() || 'Praktik mandiri siswa di VS Code';
    const user = document.getElementById('spec-target-user').value.trim() || 'Siswa SMK & Guru';
    const comp = document.getElementById('spec-complexity').value;

    document.getElementById('modal-spec-generator').classList.remove('open');

    this.appendMessage('user', `Generate Spesifikasi Teknis & Breakdown Task untuk Fitur: "${name}"`);
    const loadingId = this.appendLoading();

    try {
      const res = await API.generateSpec(name, goal, user, comp);
      this.removeLoading(loadingId);

      if (res.success) {
        this.appendMessage('ai', res.spec_markdown);
        this.history.push({ role: 'assistant', content: res.spec_markdown });
      }
    } catch (e) {
      this.removeLoading(loadingId);
      this.appendMessage('ai', `⚠️ Gagal menghasilkan spec: ${e.message}`);
    }
  },

  async handleGeneratePRD() {
    this.appendMessage('user', `Buatkan Lembar Kerja Praktikum Siswa (Jobsheet PRD) Python untuk Latihan Mandiri di VS Code`);
    const loadingId = this.appendLoading();

    try {
      const res = await API.generatePRD("Praktikum Mandiri Python & ML Siswa SMK");
      this.removeLoading(loadingId);

      if (res.success) {
        this.appendMessage('ai', res.prd_markdown);
        this.history.push({ role: 'assistant', content: res.prd_markdown });
      }
    } catch (e) {
      this.removeLoading(loadingId);
      this.appendMessage('ai', `⚠️ Gagal menghasilkan Jobsheet PRD: ${e.message}`);
    }
  },

  downloadLastOutput() {
    const aiMessages = this.history.filter(m => m.role === 'assistant');
    if (aiMessages.length === 0) {
      if (typeof App !== 'undefined') {
        App.showToast("Belum ada dokumen / materi AI yang dapat diunduh.", "error");
      }
      return;
    }
    const lastContent = aiMessages[aiMessages.length - 1].content;
    const filename = `Jobsheet_Praktikum_SMK_${new Date().toISOString().slice(0, 10)}.md`;
    API.downloadMarkdown(lastContent, filename);
    if (typeof App !== 'undefined') {
      App.showToast("Lembar Kerja Praktikum (.md) berhasil diunduh!", "success");
    }
  },

  copySnippet(id) {
    const item = this.codeSnippets[id];
    if (!item) return;

    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(item.code).then(() => {
        if (typeof App !== 'undefined') {
          App.showToast(`Kode "${item.filename}" disalin! Tempel di VS Code (Ctrl + V).`, "success");
        }
      }).catch(() => {
        this.fallbackCopy(item.code, item.filename);
      });
    } else {
      this.fallbackCopy(item.code, item.filename);
    }
  },

  fallbackCopy(code, filename) {
    const ta = document.createElement('textarea');
    ta.value = code;
    document.body.appendChild(ta);
    ta.select();
    document.execCommand('copy');
    ta.remove();
    if (typeof App !== 'undefined') {
      App.showToast(`Kode "${filename}" disalin! Tempel di VS Code.`, "success");
    }
  },

  downloadSnippet(id) {
    const item = this.codeSnippets[id];
    if (!item) return;
    const blob = new Blob([item.code], { type: 'text/x-python;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = item.filename;
    document.body.appendChild(a);
    a.click();
    URL.revokeObjectURL(url);
    a.remove();
    if (typeof App !== 'undefined') {
      App.showToast(`File "${item.filename}" berhasil diunduh! Buka di VS Code.`, "success");
    }
  },

  appendMessage(role, text, meta = null) {
    const container = document.getElementById('chat-messages-container');
    if (!container) return;

    const msgDiv = document.createElement('div');
    msgDiv.className = `chat-msg ${role}`;

    const avatar = role === 'ai' ? '🎓' : '👤';
    const renderedText = this.renderMarkdown(text);
    
    let metaHtml = '';
    if (meta) {
      metaHtml = `<div style="margin-top: 8px; padding-top: 6px; border-top: 1px dashed #e2e8f0; font-size: 0.72rem; color: #047857; font-weight: 600; display: flex; align-items: center; gap: 4px;">${meta}</div>`;
    }

    msgDiv.innerHTML = `
      <div class="chat-avatar">${avatar}</div>
      <div class="chat-bubble">${renderedText}${metaHtml}</div>
    `;

    container.appendChild(msgDiv);
    container.scrollTop = container.scrollHeight;
  },

  appendLoading() {
    const container = document.getElementById('chat-messages-container');
    const id = 'loader-' + Date.now();
    const msgDiv = document.createElement('div');
    msgDiv.id = id;
    msgDiv.className = 'chat-msg ai';
    msgDiv.innerHTML = `
      <div class="chat-avatar">🎓</div>
      <div class="chat-bubble" style="display: flex; align-items: center; gap: 8px;">
        <span class="pulse-loader"></span>
        <span style="font-size: 0.82rem; color: var(--text-muted);">AI Mentor sedang menyiapkan materi dan skrip...</span>
      </div>
    `;
    container.appendChild(msgDiv);
    container.scrollTop = container.scrollHeight;
    return id;
  },

  removeLoading(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
  },

  renderMarkdown(text) {
    if (!text) return '';

    // First replace fenced code blocks before HTML escaping to preserve code formatting
    const codePlaceholders = [];
    let processedText = text.replace(/```([a-zA-Z0-9_-]*)\n([\s\S]*?)```/g, (match, lang, code) => {
      const snippetId = this.codeSnippets.length;
      const cleanLang = (lang || 'python').toLowerCase();
      
      // Auto detect filename from code comments
      let filename = 'latihan_mandiri.py';
      const fileMatch = code.match(/#\s*(?:File|file|Nama File|nama_file):\s*([a-zA-Z0-9_.-]+\.py)/i);
      if (fileMatch && fileMatch[1]) {
        filename = fileMatch[1];
      } else if (cleanLang === 'bash' || cleanLang === 'sh') {
        filename = 'terminal_command.sh';
      }

      this.codeSnippets.push({
        id: snippetId,
        code: code,
        lang: cleanLang,
        filename: filename
      });

      const isPython = cleanLang === 'python' || cleanLang === 'py' || filename.endsWith('.py');
      
      // Safe escaped code for display
      const displayCode = code
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');

      const placeholder = `__CODE_BLOCK_${snippetId}__`;
      codePlaceholders.push({
        placeholder,
        html: `
          <div class="chat-code-card">
            <div class="chat-code-header">
              <div class="code-badge-group">
                <span class="code-lang-pill">🐍 ${cleanLang.toUpperCase()}</span>
                <span class="code-filename-pill">📄 ${filename}</span>
              </div>
              <div class="code-actions-group">
                <button class="btn-code-action" onclick="AICopilot.copySnippet(${snippetId})" title="Salin skrip untuk ditempel di VS Code">
                  📋 Salin Kode
                </button>
                ${isPython ? `
                  <button class="btn-code-action" onclick="AICopilot.downloadSnippet(${snippetId})" title="Unduh file .py langsung ke folder VS Code">
                    📥 Unduh .py
                  </button>
                ` : ''}
              </div>
            </div>
            <pre><code class="lang-${cleanLang}">${displayCode}</code></pre>
          </div>
        `
      });

      return placeholder;
    });

    // Escape basic HTML for the rest of markdown
    let html = processedText
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');

    // Inline code
    html = html.replace(/`([^`]+)`/g, '<code>$1</code>');

    // Headers
    html = html.replace(/^#### (.*$)/gim, '<h5 style="color: #0f172a; margin: 10px 0 4px 0; font-size: 0.9rem; font-weight: 700;">$1</h5>');
    html = html.replace(/^### (.*$)/gim, '<h4 style="color: #0f172a; margin: 14px 0 6px 0; font-size: 0.98rem; font-weight: 700;">$1</h4>');
    html = html.replace(/^## (.*$)/gim, '<h3 style="color: #047857; margin: 16px 0 8px 0; font-size: 1.08rem; font-weight: 700;">$1</h3>');
    html = html.replace(/^# (.*$)/gim, '<h2 style="color: #065f46; margin: 18px 0 10px 0; font-size: 1.25rem; font-weight: 800;">$1</h2>');

    // Bold & Italics
    html = html.replace(/\*\*([^*]+)\*\*/g, '<b>$1</b>');
    html = html.replace(/\*([^*]+)\*/g, '<i>$1</i>');

    // Checkboxes
    html = html.replace(/- \[ \] (.*$)/gim, '<div style="display:flex; align-items:center; gap:8px; margin: 4px 0;"><input type="checkbox" disabled /> <span>$1</span></div>');
    html = html.replace(/- \[x\] (.*$)/gim, '<div style="display:flex; align-items:center; gap:8px; margin: 4px 0;"><input type="checkbox" checked disabled /> <span style="text-decoration: line-through; opacity: 0.7;">$1</span></div>');

    // Bullet Lists
    html = html.replace(/^\* (.*$)/gim, '<li style="margin-left: 20px;">$1</li>');
    html = html.replace(/^- (.*$)/gim, '<li style="margin-left: 20px;">$1</li>');

    // Horizontal Rules
    html = html.replace(/^---$/gim, '<hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 14px 0;" />');

    // Tables
    html = html.replace(/\n\|(.*)\|\n/g, (match) => {
      return `<div style="overflow-x:auto; margin:10px 0;">${match}</div>`;
    });

    // Linebreaks
    html = html.replace(/\n\n/g, '<br/><br/>');

    // Reinsert code block cards
    codePlaceholders.forEach(item => {
      html = html.replace(item.placeholder, item.html);
    });

    return html;
  }
};
