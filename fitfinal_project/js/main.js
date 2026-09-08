// 탭 전환 함수
function switchTab(targetId) {
  // 모든 탭 숨기기
  const allTabs = document.querySelectorAll('.tab-content');
  allTabs.forEach(tab => tab.classList.remove('active'));

  // 선택한 탭 보이기
  const targetTab = document.getElementById(targetId);
  if (targetTab) {
    targetTab.classList.add('active');
  }

  // 메뉴 하이라이트 변경
  const navLinks = document.querySelectorAll('.nav-link');
  navLinks.forEach(link => {
    if (link.getAttribute('data-target') === targetId) {
      link.classList.add('active');
    } else {
      link.classList.remove('active');
    }
  });

  window.scrollTo({ top: 0, behavior: 'smooth' });
}

document.addEventListener('DOMContentLoaded', () => {
  // 1. 메뉴 클릭시 화면 전환 이벤트
  const navLinks = document.querySelectorAll('.nav-link');
  navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const targetId = link.getAttribute('data-target');
      if (targetId) {
        switchTab(targetId);
      }
    });
  });

  // 2. AI 추천 버튼 폼 제출 이벤트
  const recommendForm = document.getElementById('recommend-form');
  const recommendBtn = document.getElementById('recommend-btn');
  const resultArea = document.getElementById('result-area');
  const resultContent = document.getElementById('result-content');

  if (recommendForm) {
    recommendForm.addEventListener('submit', async (e) => {
      e.preventDefault();

      const goal = document.getElementById('goal').value;
      const level = document.getElementById('level').value;
      const days = document.getElementById('days').value;

      recommendBtn.disabled = true;
      recommendBtn.innerText = 'AI가 맞춤 루틴을 생성하는 중...';
      resultArea.classList.remove('hidden');
      resultContent.innerText = '입력하신 조건에 맞는 최적의 루틴을 분석하고 있습니다. 잠시만 기다려주세요...';

      try {
        const response = await fetch('/api/recommend', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ goal, level, days }),
        });

        const data = await response.json();

        if (response.ok) {
          resultContent.innerText = data.recommendation;
        } else {
          resultContent.innerText = `오류 발생: ${data.error || '루틴 생성 실패'}`;
        }
      } catch (err) {
        resultContent.innerText = '서버 통신 오류가 발생했습니다. 다시 시도해주세요.';
        console.error(err);
      } finally {
        recommendBtn.disabled = false;
        recommendBtn.innerText = 'AI 맞춤 루틴 생성하기';
      }
    });
  }

  // 3. 기록장 저장 로직
  const saveLogBtn = document.getElementById('save-log-btn');
  const logStatus = document.getElementById('log-status');

  if (saveLogBtn) {
    saveLogBtn.addEventListener('click', () => {
      const workout = document.getElementById('workout-log').value;
      const diet = document.getElementById('diet-log').value;

      if (!workout && !diet) {
        alert('운동이나 식단 내용을 입력해주세요.');
        return;
      }

      localStorage.setItem('fitfinal_workout', workout);
      localStorage.setItem('fitfinal_diet', diet);

      logStatus.innerText = '✅ 오늘 기록이 성공적으로 저장되었습니다!';
      setTimeout(() => {
        logStatus.innerText = '';
      }, 3000);
    });
  }
});