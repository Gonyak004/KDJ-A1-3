document.addEventListener('DOMContentLoaded', () => {
  // 1. 상단 메뉴 클릭 시 스크롤 이동 이벤트 처리
  const navLinks = document.querySelectorAll('.nav-link');

  navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      
      // active 클래스 변경
      navLinks.forEach(l => l.classList.remove('active'));
      link.classList.add('active');

      // target 섹션으로 스크롤 이동
      const targetId = link.getAttribute('href');
      const targetSection = document.querySelector(targetId);

      if (targetSection) {
        targetSection.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });

  // 2. AI 추천 버튼 통신 (백엔드 /api/recommend 호출)
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

      // 로딩 상태 표시
      recommendBtn.disabled = true;
      recommendBtn.innerText = 'AI가 루틴을 생성하는 중...';
      resultArea.classList.remove('hidden');
      resultContent.innerText = '맞춤 운동 루틴을 분석하고 있습니다. 잠시만 기다려주세요...';

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
        resultContent.innerText = '서버와의 통신에 실패했습니다. 다시 시도해 주세요.';
        console.error(err);
      } finally {
        recommendBtn.disabled = false;
        recommendBtn.innerText = 'AI 루틴 생성하기';
      }
    });
  }

  // 3. 기록장 저장 버튼 (로컬 스토리지에 가볍게 저장)
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

      logStatus.innerText = '✅ 성공적으로 저장되었습니다!';
      setTimeout(() => {
        logStatus.innerText = '';
      }, 3000);
    });
  }
});