document.getElementById('ai-form').addEventListener('submit', async (e) => {
  e.preventDefault();

  const goal = document.getElementById('goal').value;
  const level = document.getElementById('level').value;
  const days = document.getElementById('days').value;

  const statusMsg = document.getElementById('status-msg');
  const resultBox = document.getElementById('ai-result');
  const submitBtn = document.getElementById('submit-btn');

  // 초기화
  statusMsg.className = 'status-msg';
  statusMsg.textContent = '';
  resultBox.classList.add('hidden');

  // 1. 빈 입력값 검증 (클라이언트 측)
  if (!goal || !level || !days) {
    statusMsg.className = 'status-msg error';
    statusMsg.textContent = '⚠️ 모든 필수 입력 항목을 채워주세요.';
    return;
  }

  // 로딩 상태 표시
  statusMsg.className = 'status-msg loading';
  statusMsg.textContent = '⏳ AI 매니저가 맞춤 루틴을 생성 중입니다... (약 3~5초 소요)';
  submitBtn.disabled = true;

  // 타임아웃 처리용 Controller
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 12000); // 12초 타임아웃

  try {
    const response = await fetch('/api/recommend', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ goal, level, days }),
      signal: controller.signal
    });

    clearTimeout(timeoutId);

    // 2. HTTP 에러 상태 처리 (4xx, 5xx)
    if (!response.ok) {
      const errData = await response.json().catch(() => ({}));
      throw new Error(errData.error || `서버 오류가 발생했습니다. (상태 코드: ${response.status})`);
    }

    const data = await response.json();
    
    // 정상 출력
    statusMsg.textContent = '';
    resultBox.textContent = data.recommendation;
    resultBox.classList.remove('hidden');

  } catch (err) {
    statusMsg.className = 'status-msg error';
    
    // 3. 지연/타임아웃 또는 기타 에러 처리
    if (err.name === 'AbortError') {
      statusMsg.textContent = '⏱️ 응답 시간이 초과되었습니다. 잠시 후 다시 시도해주세요.';
    } else {
      statusMsg.textContent = `❌ ${err.message || '요청 중 오류가 발생했습니다.'}`;
    }
  } finally {
    submitBtn.disabled = false;
  }
});