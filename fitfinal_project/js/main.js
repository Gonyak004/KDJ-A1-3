document.addEventListener('DOMContentLoaded', () => {
  const recommendForm = document.getElementById('recommend-form');
  const recommendBtn = document.getElementById('recommend-btn');
  const resultArea = document.getElementById('result-area');
  const resultContent = document.getElementById('result-content');
  const saveLogBtn = document.getElementById('save-log-btn');
  const logStatus = document.getElementById('log-status');

  // 1. AI 루틴 생성 버튼 클릭 시
  if (recommendForm) {
    recommendForm.addEventListener('submit', async (e) => {
      e.preventDefault();

      const goal = document.getElementById('goal').value;
      const level = document.getElementById('level').value;
      const days = document.getElementById('days').value;

      recommendBtn.disabled = true;
      recommendBtn.innerText = 'AI가 루틴을 생성하는 중...';
      resultArea.classList.remove('hidden');
      resultContent.innerText = 'AI 분석 진행 중입니다. 잠시만 기다려주세요...';

      try {
        // FastAPI 라우트 엔드포인트(/api/recommend)로 수정
        const response = await fetch('/api/recommend', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ goal, level, days })
        });

        const data = await response.json();

        if (response.ok) {
          resultContent.innerText = data.recommendation || data.result;
        } else {
          resultContent.innerText = '오류 발생: ' + (data.error || '루틴을 가져오지 못했습니다.');
        }
      } catch (err) {
        resultContent.innerText = '통신 에러가 발생했습니다. 잠시 후 다시 시도해주세요.';
      } finally {
        recommendBtn.disabled = false;
        recommendBtn.innerText = 'AI 루틴 생성하기';
      }
    });
  }

  // 2. 기록장 저장 버튼 클릭 시
  if (saveLogBtn) {
    saveLogBtn.addEventListener('click', () => {
      const workout = document.getElementById('workout-log').value;
      const diet = document.getElementById('diet-log').value;

      if (!workout && !diet) {
        alert('운동이나 식단 중 하나 이상을 입력해주세요!');
        return;
      }

      logStatus.innerText = '✓ 오늘의 기록이 성공적으로 저장되었습니다!';
      setTimeout(() => { logStatus.innerText = ''; }, 3000);
    });
  }
});