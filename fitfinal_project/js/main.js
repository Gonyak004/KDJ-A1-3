// 탭 전환 함수
function switchTab(targetId) {
  const allTabs = document.querySelectorAll('.tab-content');
  allTabs.forEach(tab => tab.classList.remove('active'));

  const targetTab = document.getElementById(targetId);
  if (targetTab) {
    targetTab.classList.add('active');
  }

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

// 유튜브 검색 함수
function searchYoutube(query) {
  if (!query) return;
  const searchUrl = `https://www.youtube.com/results?search_query=${encodeURIComponent(query)}`;
  window.open(searchUrl, '_blank');
}

document.addEventListener('DOMContentLoaded', () => {
  // 1. 네비게이션 탭 전환
  const navLinks = document.querySelectorAll('.nav-link');
  navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const targetId = link.getAttribute('data-target');
      if (targetId) switchTab(targetId);
    });
  });

  // 2. AI 루틴 생성
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
      recommendBtn.innerText = 'AI가 맞춤 루틴을 분석하는 중...';
      resultArea.classList.remove('hidden');
      resultContent.innerText = '조건에 맞는 최적의 루틴을 생성 중입니다. 잠시만 기다려주세요...';

      try {
        const response = await fetch('/api/recommend', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ goal, level, days }),
        });
        const data = await response.json();
        if (response.ok) {
          resultContent.innerText = data.recommendation;
        } else {
          resultContent.innerText = `오류 발생: ${data.error}`;
        }
      } catch (err) {
        resultContent.innerText = '서버 통신 오류가 발생했습니다.';
      } finally {
        recommendBtn.disabled = false;
        recommendBtn.innerText = 'AI 맞춤 루틴 생성하기';
      }
    });
  }

  // 3. 운동 가이드 검색
  const youtubeForm = document.getElementById('youtube-search-form');
  if (youtubeForm) {
    youtubeForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const query = document.getElementById('exercise-query').value;
      searchYoutube(query);
    });
  }

  // 4. 식단 관리 AI 분석
  const dietForm = document.getElementById('diet-form');
  const dietBtn = document.getElementById('diet-btn');
  const dietResultArea = document.getElementById('diet-result-area');
  const dietResultContent = document.getElementById('diet-result-content');

  if (dietForm) {
    dietForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const height = document.getElementById('height').value;
      const weight = document.getElementById('weight').value;
      const gender = document.getElementById('gender').value;
      const target_weight = document.getElementById('target_weight').value;

      dietBtn.disabled = true;
      dietBtn.innerText = 'AI가 식단 가이드를 계산하는 중...';
      dietResultArea.classList.remove('hidden');
      dietResultContent.innerText = '신체 스펙 데이터를 바탕으로 영양 가이드를 분석 중입니다...';

      try {
        const response = await fetch('/api/diet', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ height, weight, gender, target_weight }),
        });
        const data = await response.json();
        if (response.ok) {
          dietResultContent.innerText = data.recommendation;
        } else {
          dietResultContent.innerText = `오류 발생: ${data.error}`;
        }
      } catch (err) {
        dietResultContent.innerText = '서버 통신 오류가 발생했습니다.';
      } finally {
        dietBtn.disabled = false;
        dietBtn.innerText = '맞춤 식단 플랜 받기';
      }
    });
  }

  // 5. 일일 기록장 저장 및 불러오기 (폰트 유지 및 로컬 스토리지)
  const saveLogBtn = document.getElementById('save-log-btn');
  const logStatus = document.getElementById('log-status');
  const workoutInput = document.getElementById('workout-log');
  const dietInput = document.getElementById('diet-log');

  if (workoutInput && dietInput) {
    const savedWorkout = localStorage.getItem('fitfinal_workout');
    const savedDiet = localStorage.getItem('fitfinal_diet');
    if (savedWorkout) workoutInput.value = savedWorkout;
    if (savedDiet) dietInput.value = savedDiet;
  }

  if (saveLogBtn) {
    saveLogBtn.addEventListener('click', () => {
      const workout = workoutInput.value;
      const diet = dietInput.value;

      if (!workout && !diet) {
        alert('운동이나 식단 내용을 입력해주세요.');
        return;
      }

      localStorage.setItem('fitfinal_workout', workout);
      localStorage.setItem('fitfinal_diet', diet);

      logStatus.innerText = '✅ 오늘 기록이 정상적으로 저장되었습니다!';
      setTimeout(() => { logStatus.innerText = ''; }, 3000);
    });
  }
});