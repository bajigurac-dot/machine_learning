/**
 * Studio ML Python - Visual Charts & Confusion Matrix Renderer
 * Minimalist Light Green Styling
 */
const Charts = {
  renderConfusionMatrix(containerId, cmData) {
    const container = document.getElementById(containerId);
    if (!container || !cmData || !cmData.matrix) return;

    const matrix = cmData.matrix;
    const labels = cmData.labels || matrix.map((_, i) => `Class ${i}`);

    let html = `
      <div style="text-align: center; margin-bottom: 8px;">
        <span style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase; font-weight: 600;">
          Sumbu Y: Aktual | Sumbu X: Prediksi
        </span>
      </div>
      <table class="confusion-matrix-table">
        <thead>
          <tr>
            <th style="border: none; background: transparent;"></th>
            ${labels.map(l => `<th title="Prediksi: ${l}">Prediksi: <b>${l}</b></th>`).join('')}
          </tr>
        </thead>
        <tbody>
    `;

    matrix.forEach((row, i) => {
      html += `<tr><th>Aktual: <b>${labels[i]}</b></th>`;
      row.forEach((val, j) => {
        const isDiag = (i === j);
        html += `<td class="cm-cell ${isDiag ? 'diagonal' : ''}" title="Aktual ${labels[i]} -> Prediksi ${labels[j]}: ${val}">${val}</td>`;
      });
      html += `</tr>`;
    });

    html += `</tbody></table>`;
    container.innerHTML = html;
  },

  renderFeatureImportance(containerId, features) {
    const container = document.getElementById(containerId);
    if (!container) return;

    if (!features || features.length === 0) {
      container.innerHTML = `<p style="color: var(--text-muted); font-size: 0.82rem;">Informasi bobot fitur tidak tersedia untuk model ini.</p>`;
      return;
    }

    const maxScore = Math.max(...features.map(f => f.score), 0.001);

    let html = `<div style="display: flex; flex-direction: column; gap: 10px;">`;
    features.forEach(f => {
      const pct = Math.round((f.score / maxScore) * 100);
      html += `
        <div>
          <div style="display: flex; justify-content: space-between; font-size: 0.8rem; margin-bottom: 4px;">
            <span style="font-weight: 600; color: var(--text-main);">${f.feature}</span>
            <span style="color: var(--accent-primary-hover); font-family: var(--font-mono); font-weight: 600;">${f.score}</span>
          </div>
          <div style="height: 7px; background: #f1f5f9; border-radius: 4px; overflow: hidden;">
            <div style="width: ${pct}%; height: 100%; background: linear-gradient(90deg, #10b981, #34d399); border-radius: 4px; transition: width 0.5s ease;"></div>
          </div>
        </div>
      `;
    });
    html += `</div>`;
    container.innerHTML = html;
  },

  renderLeaderboardBar(containerId, leaderboard) {
    const container = document.getElementById(containerId);
    if (!container || !leaderboard) return;

    let html = `<div style="display: flex; flex-direction: column; gap: 8px;">`;
    leaderboard.forEach(item => {
      const isWinner = item.is_winner;
      const scoreVal = typeof item.score === 'number' ? item.score : parseFloat(item.score);
      const widthPct = Math.min(100, Math.max(10, scoreVal));

      html += `
        <div style="display: flex; align-items: center; gap: 12px;">
          <span style="width: 140px; font-size: 0.82rem; font-weight: 600; color: ${isWinner ? '#047857' : 'var(--text-main)'}; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
            ${item.model_name}
          </span>
          <div style="flex: 1; height: 10px; background: #f1f5f9; border-radius: 6px; overflow: hidden;">
            <div style="width: ${widthPct}%; height: 100%; background: ${isWinner ? 'linear-gradient(90deg, #10b981, #059669)' : 'linear-gradient(90deg, #6ee7b7, #34d399)'}; border-radius: 6px;"></div>
          </div>
          <span style="width: 70px; text-align: right; font-size: 0.82rem; font-weight: 700; color: ${isWinner ? '#047857' : 'var(--text-body)'}; font-family: var(--font-mono);">
            ${item.score_display}
          </span>
        </div>
      `;
    });
    html += `</div>`;
    container.innerHTML = html;
  }
};
