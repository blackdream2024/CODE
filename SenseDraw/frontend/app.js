// SenseDraw 智能系统图生成器 - 前端逻辑

const API_BASE = 'http://localhost:3456';

// 应用状态
const state = {
  currentPage: 'home',
  mode: 'text_to_image',
  imageMode: 'exact', // exact=精准还原, extend=延展发挥
  imageUrl: null,
  history: JSON.parse(localStorage.getItem('sensedraw_history') || '[]')
};

// DOM 元素
const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => document.querySelectorAll(selector);

// 初始化应用
document.addEventListener('DOMContentLoaded', () => {
  console.log('[初始化] DOM 已加载，开始初始化...');
  
  // 延迟初始化，确保所有元素都已加载
  setTimeout(() => {
    console.log('[初始化] 开始绑定事件...');
    
    // 调试：检查所有关键元素
    debugElements();
    
    initNavigation();
    initModeSelector();
    initImageUpload();
    initRecognizeButton();
    initDocumentAnalysisModal();
    initAttachmentUpload();
    initAdvancedOptions();
    initEnhanceButton();
    initFormSubmit();
    initHistoryPage();
    updateStats();
    renderRecentList();
    updateApiUsage(); // 获取 API 使用情况
    
    // 定期更新 API 使用情况
    setInterval(updateApiUsage, 60000); // 每分钟更新一次
    
    console.log('[初始化] 所有事件绑定完成');
    
    // 额外调试：检查按钮状态
    setTimeout(() => {
      debugButtonStatus();
    }, 500);
  }, 100);
});

// 导航功能
function initNavigation() {
  const navItems = $$('.nav-item');
  if (navItems.length === 0) return;
  
  navItems.forEach(item => {
    item.addEventListener('click', (e) => {
      e.preventDefault();
      const page = item.dataset.page;
      navigateTo(page);
    });
  });
}

function navigateTo(page) {
  // 更新导航状态
  $$('.nav-item').forEach(item => item.classList.remove('active'));
  const activeNav = $(`.nav-item[data-page="${page}"]`);
  if (activeNav) activeNav.classList.add('active');
  
  // 切换页面
  $$('.page').forEach(p => p.style.display = 'none');
  const targetPage = $(`#page-${page}`);
  if (targetPage) targetPage.style.display = 'block';
  
  state.currentPage = page;
  
  // 特殊页面处理
  if (page === 'history') {
    renderHistoryList();
  }
}

// 模式选择器
function initModeSelector() {
  console.log('[初始化] 模式选择器');
  
  // 主模式选择 - 使用更通用的选择器
  document.querySelectorAll('input[name="mode"]').forEach(input => {
    input.addEventListener('change', (e) => {
      console.log('[模式切换]', e.target.value);
      state.mode = e.target.value;
      updateModeUI();
    });
  });
  
  // 图生图模式选择
  document.querySelectorAll('input[name="imageMode"]').forEach(input => {
    input.addEventListener('change', (e) => {
      console.log('[图生图模式切换]', e.target.value);
      state.imageMode = e.target.value;
      updateImageModeUI();
    });
  });
  
  // 初始化 UI
  updateModeUI();
}

function updateModeUI() {
  console.log('[更新UI] 当前模式:', state.mode);
  
  // 更新主模式状态 - 所有包含 mode input 的选项
  document.querySelectorAll('.mode-option').forEach(option => {
    const input = option.querySelector('input[name="mode"]');
    if (input) {
      option.classList.toggle('active', input.value === state.mode);
    }
  });
  
  // 显示/隐藏图片上传区域和图生图模式选项
  const uploadSection = document.getElementById('imageUploadSection');
  const imageModeSection = document.getElementById('imageModeSection');
  
  if (uploadSection) {
    uploadSection.style.display = state.mode === 'image_to_image' ? 'block' : 'none';
  }
  if (imageModeSection) {
    imageModeSection.style.display = state.mode === 'image_to_image' ? 'block' : 'none';
  }
}

function updateImageModeUI() {
  document.querySelectorAll('#imageModeSection .mode-option').forEach(option => {
    const input = option.querySelector('input[name="imageMode"]');
    if (input) {
      option.classList.toggle('active', input.value === state.imageMode);
    }
  });
}

// 图片上传
function initImageUpload() {
  const uploadArea = $('#uploadArea');
  const fileInput = $('#imageFile');
  const urlInput = $('#imageUrl');
  const previewArea = $('#previewArea');
  const previewImage = $('#previewImage');
  const removeBtn = $('#removeImage');
  
  if (!uploadArea || !fileInput || !urlInput || !previewArea || !previewImage || !removeBtn) return;
  
  // 点击上传
  uploadArea.addEventListener('click', (e) => {
    if (e.target !== urlInput) {
      fileInput.click();
    }
  });
  
  // 文件选择
  fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
      handleImageFile(file);
    }
  });
  
  // 拖拽上传
  uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.style.borderColor = 'var(--primary-color)';
    uploadArea.style.background = '#eff6ff';
  });
  
  uploadArea.addEventListener('dragleave', () => {
    uploadArea.style.borderColor = '';
    uploadArea.style.background = '';
  });
  
  uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.style.borderColor = '';
    uploadArea.style.background = '';
    
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
      handleImageFile(file);
    }
  });
  
  // URL 输入
  urlInput.addEventListener('change', () => {
    if (urlInput.value) {
      state.imageUrl = urlInput.value;
      showPreview(urlInput.value);
    }
  });
  
  // 移除图片
  removeBtn.addEventListener('click', () => {
    state.imageUrl = null;
    previewArea.style.display = 'none';
    uploadArea.style.display = 'block';
    fileInput.value = '';
    urlInput.value = '';
  });
}

function handleImageFile(file) {
  const reader = new FileReader();
  reader.onload = (e) => {
    state.imageUrl = e.target.result;
    showPreview(e.target.result);
  };
  reader.readAsDataURL(file);
}

function showPreview(url) {
  $('#previewImage').src = url;
  $('#previewArea').style.display = 'block';
  $('#uploadArea').style.display = 'none';
}

// 识图功能
function initRecognizeButton() {
  const recognizeBtn = $('#recognizeBtn');
  const recognizeModal = $('#recognizeModal');
  const recognizeModalClose = $('#recognizeModalClose');
  const recognizeRetryBtn = $('#recognizeRetryBtn');
  const recognizeCancelBtn = $('#recognizeCancelBtn');
  const recognizeApplyBtn = $('#recognizeApplyBtn');
  const recognizeEnhanceBtn = $('#recognizeEnhanceBtn');
  const recognizeResultText = $('#recognizeResultText');
  
  if (!recognizeBtn || !recognizeModal) return;
  
  // 当前识别结果
  let currentRecognizedText = '';
  
  // 识图按钮点击
  recognizeBtn.addEventListener('click', async () => {
    if (!state.imageUrl) {
      showToast('请先上传图片', 'error');
      return;
    }
    
    // 禁用按钮
    recognizeBtn.disabled = true;
    recognizeBtn.innerHTML = '<span>⏳</span> 识别中...';
    
    try {
      const response = await fetch(`${API_BASE}/api/analyze-image`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ image_url: state.imageUrl })
      });
      
      const data = await response.json();
      
      if (data.success) {
        currentRecognizedText = data.analysis;
        if (recognizeResultText) {
          recognizeResultText.textContent = currentRecognizedText;
        }
        recognizeModal.style.display = 'flex';
        
        // 更新 API 使用情况
        if (data.usage) {
          updateApiUsageFromResponse(data.usage);
        }
      } else {
        throw new Error(data.error || '图片识别失败');
      }
    } catch (error) {
      console.error('[识图] 错误:', error);
      showToast(error.message || '图片识别失败，请稍后重试', 'error');
    } finally {
      recognizeBtn.disabled = false;
      recognizeBtn.innerHTML = '<span>🔍</span> 识图';
    }
  });
  
  // 关闭弹窗
  if (recognizeModalClose) {
    recognizeModalClose.addEventListener('click', () => {
      recognizeModal.style.display = 'none';
    });
  }
  
  // 取消按钮
  if (recognizeCancelBtn) {
    recognizeCancelBtn.addEventListener('click', () => {
      recognizeModal.style.display = 'none';
    });
  }
  
  // 重新识别按钮
  if (recognizeRetryBtn) {
    recognizeRetryBtn.addEventListener('click', () => {
      recognizeModal.style.display = 'none';
      recognizeBtn.click();
    });
  }
  
  // 采用按钮
  if (recognizeApplyBtn) {
    recognizeApplyBtn.addEventListener('click', () => {
      const promptInput = $('#userPrompt');
      if (promptInput && currentRecognizedText) {
        promptInput.value = currentRecognizedText;
        showToast('已采用识别结果作为描述', 'success');
      }
      recognizeModal.style.display = 'none';
    });
  }
  
  // 文字增强按钮
  if (recognizeEnhanceBtn) {
    recognizeEnhanceBtn.addEventListener('click', async () => {
      if (!currentRecognizedText) {
        showToast('没有可增强的文字内容', 'error');
        return;
      }
      
      // 禁用按钮
      recognizeEnhanceBtn.disabled = true;
      recognizeEnhanceBtn.innerHTML = '<span>⏳</span> 增强中...';
      
      try {
        const response = await fetch(`${API_BASE}/api/enhance-prompt`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ prompt: currentRecognizedText })
        });
        
        const data = await response.json();
        
        if (data.success) {
          currentRecognizedText = data.enhancedPrompt;
          if (recognizeResultText) {
            recognizeResultText.textContent = currentRecognizedText;
          }
          showToast('文字增强完成', 'success');
          
          // 更新 API 使用情况
          if (data.usage) {
            updateApiUsageFromResponse(data.usage);
          }
        } else {
          throw new Error(data.error || '文字增强失败');
        }
      } catch (error) {
        console.error('[文字增强] 错误:', error);
        showToast(error.message || '文字增强失败，请稍后重试', 'error');
      } finally {
        recognizeEnhanceBtn.disabled = false;
        recognizeEnhanceBtn.innerHTML = '<span>🧠</span> 文字增强';
      }
    });
  }
  
  // 点击遮罩关闭
  recognizeModal.addEventListener('click', (e) => {
    if (e.target === recognizeModal) {
      recognizeModal.style.display = 'none';
    }
  });
}

// 初始化文档分析模态框
function initDocumentAnalysisModal() {
  const modal = $('#documentModal');
  const modalClose = $('#documentModalClose');
  const retryBtn = $('#documentRetryBtn');
  const cancelBtn = $('#documentCancelBtn');
  const applyBtn = $('#documentApplyBtn');
  
  if (!modal) return;
  
  // 关闭按钮
  if (modalClose) {
    modalClose.addEventListener('click', () => {
      modal.style.display = 'none';
    });
  }
  
  // 取消按钮
  if (cancelBtn) {
    cancelBtn.addEventListener('click', () => {
      modal.style.display = 'none';
    });
  }
  
  // 重新分析按钮
  if (retryBtn) {
    retryBtn.addEventListener('click', async () => {
      if (!attachmentData || !attachmentData.content) {
        showToast('没有可分析的文档内容', 'error');
        return;
      }
      
      retryBtn.disabled = true;
      retryBtn.innerHTML = '<span>⏳</span> 分析中...';
      
      try {
        const response = await fetch(`${API_BASE}/api/analyze-document`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            content: attachmentData.content,
            fileName: attachmentData.name
          })
        });
        
        const data = await response.json();
        
        if (data.success) {
          // 更新存储的分析结果
          documentAnalysisData = {
            summary: data.summary,
            prompt: data.prompt,
            fileName: attachmentData.name
          };
          
          // 更新模态框内容
          const summaryText = $('#documentSummaryText');
          const promptText = $('#documentPromptText');
          if (summaryText) summaryText.textContent = data.summary;
          if (promptText) promptText.textContent = data.prompt;
          
          showToast('文档重新分析完成', 'success');
          
          // 更新 API 使用情况
          if (data.usage) {
            updateApiUsageFromResponse(data.usage);
          }
        } else {
          throw new Error(data.error || '文档分析失败');
        }
      } catch (error) {
        console.error('[文档重新分析] 错误:', error);
        showToast(error.message || '文档重新分析失败，请稍后重试', 'error');
      } finally {
        retryBtn.disabled = false;
        retryBtn.innerHTML = '<span>🔄 重新分析</span>';
      }
    });
  }
  
  // 采纳按钮
  if (applyBtn) {
    applyBtn.addEventListener('click', () => {
      if (documentAnalysisData && documentAnalysisData.prompt) {
        const promptInput = $('#userPrompt');
        if (promptInput) {
          promptInput.value = documentAnalysisData.prompt;
          showToast('已采纳文档分析生成的提示词', 'success');
        }
      }
      modal.style.display = 'none';
    });
  }
  
  // 点击遮罩关闭
  modal.addEventListener('click', (e) => {
    if (e.target === modal) {
      modal.style.display = 'none';
    }
  });
}

// 附件上传
let attachmentData = null;
let documentAnalysisData = null;

function initAttachmentUpload() {
  const uploadArea = $('#attachmentUpload');
  const fileInput = $('#attachmentFile');
  const preview = $('#attachmentPreview');
  const nameEl = $('#attachmentName');
  const sizeEl = $('#attachmentSize');
  const removeBtn = $('#removeAttachment');
  
  if (!uploadArea || !fileInput || !preview || !nameEl || !sizeEl || !removeBtn) return;
  
  // 点击上传
  uploadArea.addEventListener('click', () => {
    fileInput.click();
  });
  
  // 文件选择
  fileInput.addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (file) {
      await handleAttachmentFile(file);
    }
  });
  
  // 移除附件
  removeBtn.addEventListener('click', () => {
    attachmentData = null;
    preview.style.display = 'none';
    uploadArea.style.display = 'flex';
    fileInput.value = '';
    
    // 恢复 placeholder
    const promptInput = $('#userPrompt');
    if (promptInput) {
      promptInput.placeholder = '文生图：描述你想生成的系统架构、流程或图表...\n图生图：描述你希望如何优化参考图片...';
    }
  });
}

async function handleAttachmentFile(file) {
  const uploadArea = $('#attachmentUpload');
  const preview = $('#attachmentPreview');
  const nameEl = $('#attachmentName');
  const sizeEl = $('#attachmentSize');
  
  // 显示文件信息
  nameEl.textContent = file.name;
  sizeEl.textContent = formatFileSize(file.size);
  preview.style.display = 'flex';
  uploadArea.style.display = 'none';
  
  // 读取文件内容
  try {
    let content = '';
    
    if (file.name.endsWith('.txt')) {
      content = await readTextFile(file);
    } else if (file.name.endsWith('.pdf')) {
      showToast('正在解析 PDF 文件...', 'info');
      content = await readPDFFile(file);
    } else if (file.name.endsWith('.doc') || file.name.endsWith('.docx')) {
      showToast('DOC 文件请复制内容到文本框，或转换为 TXT/PDF 格式', 'info');
      content = '';
    } else {
      showToast('不支持的文件格式，请使用 TXT 或 PDF 格式', 'error');
      content = '';
    }
    
    if (content) {
      attachmentData = {
        name: file.name,
        content: content
      };
      
      // 调用文档分析接口
      showToast('正在分析文档内容...', 'info');
      
      try {
        const response = await fetch(`${API_BASE}/api/analyze-document`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            content: content,
            fileName: file.name
          })
        });
        
        const data = await response.json();
        
        if (data.success) {
          // 存储分析结果
          documentAnalysisData = {
            summary: data.summary,
            prompt: data.prompt,
            fileName: file.name
          };
          
          // 显示文档分析模态框
          showDocumentAnalysisModal(data.summary, data.prompt);
          showToast('文档分析完成，请查看结果', 'success');
        } else {
          showToast('文档分析失败: ' + (data.error || '未知错误'), 'error');
          // 失败时仍然填充原始内容
          fillDocumentContent(content);
        }
      } catch (error) {
        console.error('[文档分析] 请求失败:', error);
        showToast('文档分析请求失败，已填充原始内容', 'error');
        // 失败时仍然填充原始内容
        fillDocumentContent(content);
      }
    }
  } catch (error) {
    console.error('[附件] 读取失败:', error);
    showToast('文件读取失败，请重试', 'error');
  }
}

// 填充文档内容到文本框（用于分析失败时的回退方案）
function fillDocumentContent(content) {
  const promptInput = $('#userPrompt');
  if (promptInput) {
    // 如果文本框为空，直接填充
    if (!promptInput.value.trim()) {
      promptInput.value = `基于以下文档内容生成系统架构图：\n\n${content.substring(0, 3000)}`;
    } else {
      // 如果已有内容，追加
      promptInput.value += `\n\n--- 文档内容 ---\n${content.substring(0, 2000)}`;
    }
  }
}

// 显示文档分析模态框
function showDocumentAnalysisModal(summary, prompt) {
  const modal = $('#documentModal');
  const summaryText = $('#documentSummaryText');
  const promptText = $('#documentPromptText');
  
  if (!modal || !summaryText || !promptText) {
    console.error('[文档分析] 找不到模态框元素');
    return;
  }
  
  // 设置内容
  summaryText.textContent = summary;
  promptText.textContent = prompt;
  
  // 显示模态框
  modal.style.display = 'flex';
}

function readTextFile(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = (e) => resolve(e.target.result);
    reader.onerror = reject;
    reader.readAsText(file);
  });
}

// 解析 PDF 文件
async function readPDFFile(file) {
  try {
    // 设置 PDF.js worker
    if (window.pdfjsLib) {
      window.pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
    }
    
    const arrayBuffer = await file.arrayBuffer();
    const pdf = await window.pdfjsLib.getDocument({ data: arrayBuffer }).promise;
    
    let fullText = '';
    
    // 遍历所有页面
    for (let i = 1; i <= pdf.numPages; i++) {
      const page = await pdf.getPage(i);
      const textContent = await page.getTextContent();
      const pageText = textContent.items.map(item => item.str).join(' ');
      fullText += pageText + '\n';
    }
    
    console.log('[PDF解析] 成功，页数:', pdf.numPages, '文字长度:', fullText.length);
    return fullText.trim();
    
  } catch (error) {
    console.error('[PDF解析] 失败:', error);
    showToast('PDF 解析失败，请复制内容到文本框', 'error');
    return '';
  }
}

function formatFileSize(bytes) {
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}

// 高级选项
function initAdvancedOptions() {
  const toggle = $('#advancedToggle');
  const options = $('#advancedOptions');
  
  if (!toggle || !options) return;
  
  toggle.addEventListener('click', () => {
    const isExpanded = options.style.display !== 'none';
    options.style.display = isExpanded ? 'none' : 'block';
    const toggleIcon = toggle.querySelector('.toggle-icon');
    if (toggleIcon) toggleIcon.classList.toggle('expanded', !isExpanded);
  });
}

// 提示词增强功能
function initEnhanceButton() {
  const enhanceBtn = $('#enhanceBtn');
  const enhanceSection = $('#enhanceSection');
  const enhanceModal = $('#enhanceModal');
  const enhanceModalClose = $('#enhanceModalClose');
  const enhanceRetryBtn = $('#enhanceRetryBtn');
  const enhanceCancelBtn = $('#enhanceCancelBtn');
  const enhanceApplyBtn = $('#enhanceApplyBtn');
  const enhanceResultText = $('#enhanceResultText');
  
  if (!enhanceBtn || !enhanceSection) return;
  
  // 当前增强结果
  let currentEnhancedText = '';
  
  // 增强按钮在两种模式下都显示（文生图直接增强，图生图通过识图后增强）
  
  // 增强按钮点击
  enhanceBtn.addEventListener('click', async () => {
    const promptInput = $('#userPrompt');
    const prompt = promptInput ? promptInput.value.trim() : '';
    
    if (!prompt) {
      showToast('请先输入描述内容', 'error');
      return;
    }
    
    // 禁用按钮
    enhanceBtn.disabled = true;
    enhanceBtn.querySelector('.enhance-btn-text').textContent = '正在增强...';
    
    try {
      const response = await fetch(`${API_BASE}/api/enhance-prompt`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ prompt })
      });
      
      const data = await response.json();
      
      if (data.success) {
        currentEnhancedText = data.enhancedPrompt;
        if (enhanceResultText) {
          enhanceResultText.textContent = currentEnhancedText;
        }
        if (enhanceModal) {
          enhanceModal.style.display = 'flex';
        }
        
        // 更新 API 使用情况
        if (data.usage) {
          updateApiUsageFromResponse(data.usage);
        }
      } else {
        throw new Error(data.error || '提示词增强失败');
      }
    } catch (error) {
      console.error('[提示词增强] 错误:', error);
      showToast(error.message || '提示词增强失败，请稍后重试', 'error');
    } finally {
      enhanceBtn.disabled = false;
      enhanceBtn.querySelector('.enhance-btn-text').textContent = '提示词增强';
    }
  });
  
  // 关闭弹窗
  if (enhanceModalClose) {
    enhanceModalClose.addEventListener('click', () => {
      if (enhanceModal) enhanceModal.style.display = 'none';
    });
  }
  
  // 取消按钮
  if (enhanceCancelBtn) {
    enhanceCancelBtn.addEventListener('click', () => {
      if (enhanceModal) enhanceModal.style.display = 'none';
    });
  }
  
  // 重新生成按钮
  if (enhanceRetryBtn) {
    enhanceRetryBtn.addEventListener('click', async () => {
      if (enhanceModal) enhanceModal.style.display = 'none';
      enhanceBtn.click();
    });
  }
  
  // 采用按钮
  if (enhanceApplyBtn) {
    enhanceApplyBtn.addEventListener('click', () => {
      const promptInput = $('#userPrompt');
      if (promptInput && currentEnhancedText) {
        promptInput.value = currentEnhancedText;
        showToast('已采用增强后的描述', 'success');
      }
      if (enhanceModal) enhanceModal.style.display = 'none';
    });
  }
  
  // 点击遮罩关闭
  if (enhanceModal) {
    enhanceModal.addEventListener('click', (e) => {
      if (e.target === enhanceModal) {
        enhanceModal.style.display = 'none';
      }
    });
  }
}

// 表单提交
function initFormSubmit() {
  const form = $('#createForm');
  
  if (!form) return;
  
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const promptInput = $('#userPrompt');
    const prompt = promptInput ? promptInput.value.trim() : '';
    
    if (!prompt) {
      showToast('请输入描述内容', 'error');
      return;
    }
    
    if (state.mode === 'image_to_image' && !state.imageUrl) {
      showToast('请上传参考图片', 'error');
      return;
    }
    
    await generateImage(prompt);
  });
}

async function generateImage(prompt) {
  const submitBtn = $('#submitBtn');
  if (!submitBtn) return;
  
  const btnText = submitBtn.querySelector('.btn-text');
  const btnLoading = submitBtn.querySelector('.btn-loading');
  
  // 显示加载状态
  submitBtn.disabled = true;
  if (btnText) btnText.style.display = 'none';
  if (btnLoading) btnLoading.style.display = 'inline-flex';
  
  try {
    const outputFormat = $('#outputFormat') ? $('#outputFormat').value : 'png';
    
    const requestBody = {
      mode: state.mode,
      prompt: prompt,
      size: $('#imageSize').value || '2752x1536',
      n: 1,
      outputFormat: outputFormat
    };
    
    if (state.mode === 'image_to_image') {
      requestBody.image_url = state.imageUrl;
      requestBody.imageMode = state.imageMode;
    }
    
    const response = await fetch(`${API_BASE}/api/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestBody)
    });
    
    const data = await response.json();
    
    if (data.success) {
      // 保存到历史
      const record = {
        id: Date.now().toString(),
        mode: state.mode,
        imageMode: state.imageMode,
        prompt: prompt,
        finalPrompt: data.prompt || data.meta?.prompt || prompt,
        outputFormat: data.outputFormat || 'png',
        imageUrl: data.images ? data.images[0] : null,
        svgCode: data.svgCode || null,
        analysis: data.analysis?.full_analysis,
        structure: data.structure || null,
        optimization: data.optimization || null,
        size: requestBody.size,
        createdAt: new Date().toISOString()
      };
      
      state.history.unshift(record);
      localStorage.setItem('sensedraw_history', JSON.stringify(state.history));
      
      // 显示结果
      showResult(record);
      updateStats();
      renderRecentList();
      
      // 更新 API 使用情况
      if (data.usage) {
        updateApiUsageFromResponse(data.usage);
      } else {
        updateApiUsage();
      }
      
      showToast('生成成功！', 'success');
    } else {
      throw new Error(data.error || '生成失败');
    }
    
  } catch (error) {
    console.error('生成错误:', error);
    showToast(error.message || '生成失败，请稍后重试', 'error');
  } finally {
    // 恢复按钮状态
    if (submitBtn) submitBtn.disabled = false;
    if (btnText) btnText.style.display = 'inline';
    if (btnLoading) btnLoading.style.display = 'none';
  }
}

// 显示结果
function showResult(record) {
  const resultImage = $('#resultImage');
  const infoMode = $('#infoMode');
  const infoSize = $('#infoSize');
  const infoTime = $('#infoTime');
  const finalPrompt = $('#finalPrompt');
  const analysisCard = $('#analysisCard');
  const analysisContent = $('#analysisContent');
  const downloadBtn = $('#downloadBtn');
  const cloneBtn = $('#cloneBtn');
  const backBtn = $('#backBtn');
  
  // 显示图片或 SVG
  if (record.outputFormat === 'svg' && record.svgCode) {
    // SVG 格式
    if (resultImage) {
      resultImage.style.display = 'none';
    }
    // 创建 SVG 容器
    let svgContainer = $('#svgContainer');
    if (!svgContainer) {
      svgContainer = document.createElement('div');
      svgContainer.id = 'svgContainer';
      svgContainer.className = 'svg-container';
      resultImage.parentNode.insertBefore(svgContainer, resultImage);
    }
    svgContainer.innerHTML = record.svgCode;
    svgContainer.style.display = 'block';
  } else {
    // PNG 格式
    if (resultImage) {
      resultImage.src = record.imageUrl;
      resultImage.style.display = 'block';
    }
    const svgContainer = $('#svgContainer');
    if (svgContainer) svgContainer.style.display = 'none';
  }
  
  if (infoMode) {
    let modeText = record.mode === 'text_to_image' ? '文生图' : '图生图';
    if (record.mode === 'image_to_image' && record.imageMode) {
      if (record.imageMode === 'exact') {
        modeText += '（精准还原）';
      } else if (record.imageMode === 'extend') {
        modeText += '（延展发挥）';
      } else if (record.imageMode === 'structure_locked') {
        modeText += '（结构锁定）';
      }
    }
    if (record.outputFormat === 'svg') {
      modeText += ' [SVG]';
    }
    infoMode.textContent = modeText;
  }
  if (infoSize) infoSize.textContent = record.outputFormat === 'svg' ? '矢量图' : record.size;
  if (infoTime) infoTime.textContent = new Date(record.createdAt).toLocaleString('zh-CN');
  if (finalPrompt) finalPrompt.textContent = record.finalPrompt || '-';
  
  // AI 分析或结构信息
  if (record.structure) {
    // 结构锁定模式 - 显示结构信息
    if (analysisCard) analysisCard.style.display = 'block';
    if (analysisContent) {
      const structureInfo = `结构提取完成：
- 模块数量：${record.structure.modules?.length || 0} 个
- 连接数量：${record.structure.connections?.length || 0} 个
- 画布尺寸：${record.structure.canvas?.width || 2752} × ${record.structure.canvas?.height || 1536}

模块列表：
${record.structure.modules?.map(m => `• ${m.label} (${m.bounds?.x},${m.bounds?.y}) ${m.bounds?.w}×${m.bounds?.h}`).join('\n') || '无'}

连接关系：
${record.structure.connections?.map(c => {
  const from = record.structure.modules?.find(m => m.id === c.from);
  const to = record.structure.modules?.find(m => m.id === c.to);
  return `• ${from?.label || c.from} → ${to?.label || c.to} (${c.type})`;
}).join('\n') || '无'}`;
      analysisContent.textContent = structureInfo;
    }
  } else if (record.analysis) {
    if (analysisCard) analysisCard.style.display = 'block';
    if (analysisContent) analysisContent.textContent = record.analysis;
  } else {
    if (analysisCard) analysisCard.style.display = 'none';
  }
  
  // 绑定按钮事件
  if (downloadBtn) {
    if (record.outputFormat === 'svg' && record.svgCode) {
      downloadBtn.onclick = () => downloadSVG(record.svgCode);
      downloadBtn.textContent = '💾 下载 SVG';
    } else {
      downloadBtn.onclick = () => downloadImage(record.imageUrl);
      downloadBtn.textContent = '💾 下载图片';
    }
  }
  if (cloneBtn) cloneBtn.onclick = () => {
    const userPrompt = $('#userPrompt');
    if (userPrompt) userPrompt.value = record.prompt;
    navigateTo('create');
  };
  if (backBtn) backBtn.onclick = () => navigateTo('home');
  
  navigateTo('result');
}

// 下载图片
function downloadImage(url) {
  const a = document.createElement('a');
  a.href = url;
  a.download = `系统图工具-${Date.now()}.png`;
  a.target = '_blank';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}

// 下载 SVG
function downloadSVG(svgCode) {
  const blob = new Blob([svgCode], { type: 'image/svg+xml' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `系统图工具-${Date.now()}.svg`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

// 历史记录页面
function initHistoryPage() {
  // 历史页面初始化
}

function renderHistoryList() {
  const list = $('#historyList');
  
  if (state.history.length === 0) {
    list.innerHTML = '<div class="empty-state">暂无历史记录</div>';
    return;
  }
  
  list.innerHTML = state.history.map(item => {
    return `
      <div class="history-item" data-id="${item.id}">
        <img class="history-thumb" src="${item.imageUrl}" alt="缩略图">
        <div class="history-info">
          <h4>${item.prompt.substring(0, 50)}${item.prompt.length > 50 ? '...' : ''}</h4>
          <div class="history-meta">
            <span>${item.mode === 'text_to_image' ? '✏️ 文生图' : '🖼️ 图生图'}</span>
            <span>🕐 ${new Date(item.createdAt).toLocaleDateString('zh-CN')}</span>
          </div>
        </div>
      </div>
    `;
  }).join('');
  
  // 绑定点击事件
  $$('.history-item').forEach(item => {
    item.addEventListener('click', () => {
      const record = state.history.find(h => h.id === item.dataset.id);
      if (record) {
        showResult(record);
      }
    });
  });
}

// 最近记录列表
function renderRecentList() {
  const list = $('#recentList');
  const recent = state.history.slice(0, 5);
  
  if (recent.length === 0) {
    list.innerHTML = '<div class="empty-state">暂无生成记录</div>';
    return;
  }
  
  list.innerHTML = recent.map(item => {
    return `
      <div class="history-item" data-id="${item.id}" style="padding: 12px;">
        <img class="history-thumb" src="${item.imageUrl}" alt="缩略图" style="width: 60px; height: 40px;">
        <div class="history-info">
          <h4 style="font-size: 14px;">${item.prompt.substring(0, 30)}...</h4>
        </div>
      </div>
    `;
  }).join('');
  
  // 绑定点击事件
  $$('#recentList .history-item').forEach(item => {
    item.addEventListener('click', () => {
      const record = state.history.find(h => h.id === item.dataset.id);
      if (record) {
        showResult(record);
      }
    });
  });
}

// 更新统计数据
function updateStats() {
  const total = state.history.length;
  const textCount = state.history.filter(h => h.mode === 'text_to_image').length;
  const imageCount = state.history.filter(h => h.mode === 'image_to_image').length;
  
  // 今日生成
  const today = new Date().toDateString();
  const todayCount = state.history.filter(h => 
    new Date(h.createdAt).toDateString() === today
  ).length;
  
  const statTotal = $('#statTotal');
  const statText = $('#statText');
  const statImage = $('#statImage');
  const statToday = $('#statToday');
  
  if (statTotal) statTotal.textContent = total;
  if (statText) statText.textContent = textCount;
  if (statImage) statImage.textContent = imageCount;
  if (statToday) statToday.textContent = todayCount;
}

// 更新 API 使用情况
async function updateApiUsage() {
  try {
    const response = await fetch(`${API_BASE}/api/usage`);
    const data = await response.json();
    
    if (data.success) {
      const usage = data.usage;
      
      // 更新进度条
      const progressFill = $('#apiProgressFill');
      const progressText = $('#apiProgressText');
      const apiRemaining = $('#apiRemaining');
      const apiResetTime = $('#apiResetTime');
      
      if (progressFill) {
        const percentage = (usage.used / usage.limit) * 100;
        progressFill.style.width = `${percentage}%`;
        
        // 根据使用量改变颜色
        if (percentage > 80) {
          progressFill.style.background = 'linear-gradient(90deg, var(--error-color), var(--warning-color))';
        } else if (percentage > 60) {
          progressFill.style.background = 'linear-gradient(90deg, var(--warning-color), var(--success-color))';
        } else {
          progressFill.style.background = 'linear-gradient(90deg, var(--primary-color), var(--success-color))';
        }
      }
      
      if (progressText) {
        progressText.textContent = `${usage.used}/${usage.limit}`;
      }
      
      if (apiRemaining) {
        apiRemaining.textContent = `剩余: ${usage.remaining}`;
        
        // 根据剩余次数改变颜色
        if (usage.remaining <= 0) {
          apiRemaining.style.color = 'var(--error-color)';
        } else if (usage.remaining < 100) {
          apiRemaining.style.color = 'var(--warning-color)';
        } else {
          apiRemaining.style.color = 'var(--success-color)';
        }
      }
      
      if (apiResetTime && usage.resetTime) {
        const resetDate = new Date(usage.resetTime);
        const now = new Date();
        const diffMs = resetDate - now;
        const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
        const diffMinutes = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60));
        
        if (diffMs > 0) {
          apiResetTime.textContent = `重置: ${diffHours}小时${diffMinutes}分钟后`;
        } else {
          apiResetTime.textContent = '重置时间: 已重置';
        }
      } else {
        if (apiResetTime) {
          apiResetTime.textContent = '重置时间: --';
        }
      }
      
      console.log('[API使用情况]', usage);
    }
  } catch (error) {
    console.error('[API使用情况] 获取失败:', error);
  }
}

// 从响应中更新 API 使用情况
function updateApiUsageFromResponse(usage) {
  try {
    // 更新进度条
    const progressFill = $('#apiProgressFill');
    const progressText = $('#apiProgressText');
    const apiRemaining = $('#apiRemaining');
    const apiResetTime = $('#apiResetTime');
    
    if (progressFill) {
      const percentage = (usage.used / usage.limit) * 100;
      progressFill.style.width = `${percentage}%`;
      
      // 根据使用量改变颜色
      if (percentage > 80) {
        progressFill.style.background = 'linear-gradient(90deg, var(--error-color), var(--warning-color))';
      } else if (percentage > 60) {
        progressFill.style.background = 'linear-gradient(90deg, var(--warning-color), var(--success-color))';
      } else {
        progressFill.style.background = 'linear-gradient(90deg, var(--primary-color), var(--success-color))';
      }
    }
    
    if (progressText) {
      progressText.textContent = `${usage.used}/${usage.limit}`;
    }
    
    if (apiRemaining) {
      apiRemaining.textContent = `剩余: ${usage.remaining}`;
      
      // 根据剩余次数改变颜色
      if (usage.remaining <= 0) {
        apiRemaining.style.color = 'var(--error-color)';
      } else if (usage.remaining < 100) {
        apiRemaining.style.color = 'var(--warning-color)';
      } else {
        apiRemaining.style.color = 'var(--success-color)';
      }
    }
    
    if (apiResetTime && usage.resetTime) {
      const resetDate = new Date(usage.resetTime);
      const now = new Date();
      const diffMs = resetDate - now;
      const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
      const diffMinutes = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60));
      
      if (diffMs > 0) {
        apiResetTime.textContent = `重置: ${diffHours}小时${diffMinutes}分钟后`;
      } else {
        apiResetTime.textContent = '重置时间: 已重置';
      }
    } else {
      if (apiResetTime) {
        apiResetTime.textContent = '重置时间: --';
      }
    }
    
    console.log('[API使用情况] 从响应更新:', usage);
  } catch (error) {
    console.error('[API使用情况] 更新失败:', error);
  }
}

// 消息提示
function showToast(message, type = 'info') {
  const toast = $('#toast');
  if (!toast) {
    console.log(`[${type}] ${message}`);
    return;
  }
  
  toast.textContent = message;
  toast.className = `toast ${type}`;
  toast.style.display = 'block';
  
  setTimeout(() => {
    toast.style.display = 'none';
  }, 3000);
}

// 调试函数：检查关键元素
function debugElements() {
  console.log('[调试] 检查关键元素...');
  
  const elements = {
    'createForm': $('#createForm'),
    'submitBtn': $('#submitBtn'),
    'userPrompt': $('#userPrompt'),
    'imageSize': $('#imageSize'),
    'uploadArea': $('#uploadArea'),
    'imageFile': $('#imageFile'),
    'imageUrl': $('#imageUrl'),
    'previewArea': $('#previewArea'),
    'previewImage': $('#previewImage'),
    'removeImage': $('#removeImage'),
    'advancedToggle': $('#advancedToggle'),
    'advancedOptions': $('#advancedOptions'),
    'imageUploadSection': $('#imageUploadSection'),
    'imageModeSection': $('#imageModeSection'),
    'toast': $('#toast')
  };
  
  Object.entries(elements).forEach(([name, element]) => {
    if (element) {
      console.log(`[调试] ✅ ${name}: 找到`);
    } else {
      console.warn(`[调试] ❌ ${name}: 未找到`);
    }
  });
  
  // 检查模式选择器
  const modeInputs = document.querySelectorAll('input[name="mode"]');
  console.log(`[调试] 模式选择器: 找到 ${modeInputs.length} 个`);
  
  // 检查导航项
  const navItems = $$('.nav-item');
  console.log(`[调试] 导航项: 找到 ${navItems.length} 个`);
}

// 调试函数：检查按钮状态
function debugButtonStatus() {
  console.log('[调试] 检查按钮状态...');
  
  // 检查提交按钮
  const submitBtn = $('#submitBtn');
  if (submitBtn) {
    console.log(`[调试] 提交按钮: disabled=${submitBtn.disabled}, text="${submitBtn.textContent.trim()}"`);
    
    // 添加点击测试
    submitBtn.addEventListener('click', (e) => {
      console.log('[调试] 提交按钮被点击');
    });
  }
  
  // 检查模式选择器
  document.querySelectorAll('input[name="mode"]').forEach((input, index) => {
    console.log(`[调试] 模式选择器 ${index}: value="${input.value}", checked=${input.checked}`);
    
    // 添加变化监听
    input.addEventListener('change', (e) => {
      console.log(`[调试] 模式选择器变化: ${e.target.value}`);
    });
  });
}

// 导出全局函数
window.navigateTo = navigateTo;
