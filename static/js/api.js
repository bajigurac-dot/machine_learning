/**
 * Studio ML Python - API Client
 */
const API = {
  async getDatasets() {
    const res = await fetch('/api/datasets');
    return await res.json();
  },

  async loadDataset(datasetId) {
    const res = await fetch('/api/dataset/load', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ dataset_id: datasetId })
    });
    return await res.json();
  },

  async uploadDataset(file) {
    const formData = new FormData();
    formData.append('file', file);
    const res = await fetch('/api/dataset/upload', {
      method: 'POST',
      body: formData
    });
    return await res.json();
  },

  async cleanDataset(actions) {
    const res = await fetch('/api/dataset/clean', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(actions)
    });
    return await res.json();
  },

  async getRecommendations(targetColumn) {
    const res = await fetch('/api/models/recommend', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ target_column: targetColumn })
    });
    return await res.json();
  },

  async trainSingleModel(modelId, targetColumn, params, testSize = 0.2) {
    const res = await fetch('/api/train/single', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model_id: modelId,
        target_column: targetColumn,
        params: params,
        test_size: testSize
      })
    });
    return await res.json();
  },

  async trainAutoML(targetColumn, testSize = 0.2) {
    const res = await fetch('/api/train/automl', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        target_column: targetColumn,
        test_size: testSize
      })
    });
    return await res.json();
  },

  async predict(inputValues) {
    const res = await fetch('/api/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(inputValues)
    });
    return await res.json();
  },

  async getPythonCode() {
    const res = await fetch('/api/code/generate');
    return await res.json();
  },

  async getProjects() {
    const res = await fetch('/api/projects');
    return await res.json();
  },

  async saveProject(name, description) {
    const res = await fetch('/api/projects/save', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, description })
    });
    return await res.json();
  },

  async deleteProject(id) {
    const res = await fetch(`/api/projects/${id}`, {
      method: 'DELETE'
    });
    return await res.json();
  },

  // AI Copilot Endpoints
  async testGemini(apiKey) {
    const res = await fetch('/api/ai/test_gemini', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ api_key: apiKey })
    });
    return await res.json();
  },

  async sendAiChat(message, history, apiKey, provider) {
    const res = await fetch('/api/ai/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message,
        history,
        api_key: apiKey,
        provider
      })
    });
    return await res.json();
  },

  async generateSpec(featureName, goal, targetUser, complexity) {
    const res = await fetch('/api/ai/generate_spec', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        feature_name: featureName,
        goal,
        target_user: targetUser,
        complexity
      })
    });
    return await res.json();
  },

  async generatePRD(projectName) {
    const res = await fetch('/api/ai/generate_prd', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ project_name: projectName })
    });
    return await res.json();
  },

  async downloadMarkdown(content, filename) {
    const res = await fetch('/api/ai/download_markdown', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content, filename })
    });
    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    a.remove();
  },

  // ==================== E-LEARNING & CBT API ====================
  async getExams() {
    const res = await fetch('/api/elearning/exams');
    return await res.json();
  },

  async getExam(id) {
    const res = await fetch(`/api/elearning/exams/${id}`);
    return await res.json();
  },

  async runCode(language, code, expectedOutput) {
    const res = await fetch('/api/elearning/code/run', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ language, code, expected_output: expectedOutput })
    });
    return await res.json();
  },

  async submitExam(examId, studentInfo, answers, durationSeconds) {
    const res = await fetch('/api/elearning/submissions/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        exam_id: examId,
        student_info: studentInfo,
        answers: answers,
        duration_seconds: durationSeconds
      })
    });
    return await res.json();
  },

  async studentLogin(nisn, name = '') {
    const res = await fetch('/api/elearning/student/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ nisn, name })
    });
    return await res.json();
  },

  async checkNisn(nisn) {
    const res = await fetch(`/api/elearning/student/check-nisn/${encodeURIComponent(nisn)}`);
    return await res.json();
  },

  async getStudentAttempts(nisn) {
    const res = await fetch(`/api/elearning/student/attempts?nisn=${encodeURIComponent(nisn)}`);
    return await res.json();
  },

  async getStudentCardData(nisn) {
    const res = await fetch(`/api/elearning/student/card/data?nisn=${encodeURIComponent(nisn)}`);
    return await res.json();
  },

  async adminLogin(username, password) {
    const res = await fetch('/api/elearning/admin/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    return await res.json();
  },

  async adminChangePassword(oldPassword, newPassword, confirmPassword, username = 'guru') {
    const res = await fetch('/api/elearning/admin/change-password', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username,
        old_password: oldPassword,
        new_password: newPassword,
        confirm_password: confirmPassword
      })
    });
    return await res.json();
  },

  async createExam(title, description, subject, durationMinutes) {
    const res = await fetch('/api/elearning/exams/create', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        title, description, subject, duration_minutes: durationMinutes
      })
    });
    return await res.json();
  },

  async deleteExam(id) {
    const res = await fetch(`/api/elearning/exams/${id}`, { method: 'DELETE' });
    return await res.json();
  },

  async addQuestion(examId, questionType, questionText, options, correctAnswer, starterCode, expectedOutput, points) {
    const res = await fetch('/api/elearning/questions/add', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        exam_id: examId,
        question_type: questionType,
        question_text: questionText,
        options,
        correct_answer: correctAnswer,
        starter_code: starterCode,
        expected_output: expectedOutput,
        points
      })
    });
    return await res.json();
  },

  async getAdminSubmissions(examId = null, className = null, date = null) {
    const params = new URLSearchParams();
    if (examId) params.append('exam_id', examId);
    if (className) params.append('class_name', className);
    if (date) params.append('date', date);
    const queryString = params.toString() ? `?${params.toString()}` : '';
    const res = await fetch(`/api/elearning/admin/submissions${queryString}`);
    return await res.json();
  },

  async getAdminStudents(className = '') {
    const url = className ? `/api/elearning/admin/students?class_name=${encodeURIComponent(className)}` : '/api/elearning/admin/students';
    const res = await fetch(url);
    return await res.json();
  },

  async addAdminStudent(nisn, name, className) {
    const res = await fetch('/api/elearning/admin/students', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ nisn, name, class_name: className })
    });
    return await res.json();
  },

  async deleteAdminStudent(studentId) {
    const res = await fetch(`/api/elearning/admin/students/${studentId}`, { method: 'DELETE' });
    return await res.json();
  },

  async updateSubmissionScore(submissionId, score) {
    const res = await fetch(`/api/elearning/admin/submissions/${submissionId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ score })
    });
    return await res.json();
  },

  async deleteSubmission(submissionId) {
    const res = await fetch(`/api/elearning/admin/submissions/${submissionId}`, {
      method: 'DELETE'
    });
    return await res.json();
  }
};
