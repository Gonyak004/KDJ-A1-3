document.addEventListener("DOMContentLoaded", () => {
  setupNavigation();
  setupRoutineForm();
  setupDietForm();
  setupYoutubeForm();
  setupTrackerForm();
});

// 탭 전환 기능
function switchTab(targetId) {
  const tabs = document.querySelectorAll(".tab-content");
  const navLinks = document.querySelectorAll(".nav-link");

  tabs.forEach((tab) => tab.classList.remove("active"));
  navLinks.forEach((link) => link.classList.remove("active"));

  const targetTab = document.getElementById(targetId);
  if (targetTab) targetTab.classList.add("active");

  const activeLink = document.querySelector(`.nav-link[data-target="${targetId}"]`);
  if (activeLink) activeLink.classList.add("active");

  window.scrollTo({ top: 0, behavior: "smooth" });
}

function setupNavigation() {
  const navLinks = document.querySelectorAll(".nav-link");
  navLinks.forEach((link) => {
    link.addEventListener("click", (e) => {
      e.preventDefault();
      const targetId = link.getAttribute("data-target");
      switchTab(targetId);
    });
  });
}

// 1. AI 운동 루틴 생성
function setupRoutineForm() {
  const form = document.getElementById("recommend-form");
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const goal = document.getElementById("goal").value;
    const level = document.getElementById("level").value;
    const days = document.getElementById("days").value;

    const btn = document.getElementById("recommend-btn");
    const resultArea = document.getElementById("result-area");
    const resultContent = document.getElementById("result-content");

    btn.disabled = true;
    btn.textContent = "AI 분석 중...";
    resultArea.classList.remove("hidden");
    resultContent.innerHTML = "<p class='loading'>AI가 맞춤형 운동 루틴을 생성하고 있습니다...</p>";

    try {
      const response = await fetch("/api/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ goal, level, days }),
      });

      const data = await response.json();

      if (response.ok) {
        resultContent.innerHTML = formatMarkdown(data.recommendation);
      } else {
        resultContent.innerHTML = `<p style="color:red;">오류: ${data.error || "추천 생성 실패"}</p>`;
      }
    } catch (err) {
      resultContent.innerHTML = `<p style="color:red;">서버 연결 오류: ${err.message}</p>`;
    } finally {
      btn.disabled = false;
      btn.textContent = "AI 맞춤 루틴 생성하기";
    }
  });
}

// 2. AI 식단 가이드
function setupDietForm() {
  const form = document.getElementById("diet-form");
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const height = document.getElementById("height").value;
    const weight = document.getElementById("weight").value;
    const gender = document.getElementById("gender").value;
    const target_weight = document.getElementById("target_weight").value;

    const btn = document.getElementById("diet-btn");
    const resultArea = document.getElementById("diet-result-area");
    const resultContent = document.getElementById("diet-result-content");

    btn.disabled = true;
    btn.textContent = "식단 가이드 생성 중...";
    resultArea.classList.remove("hidden");
    resultContent.innerHTML = "<p class='loading'>AI 영양사가 맞춤 식단을 구성 중입니다...</p>";

    try {
      const response = await fetch("/api/diet", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ height, weight, gender, target_weight }),
      });

      const data = await response.json();

      if (response.ok) {
        resultContent.innerHTML = formatMarkdown(data.recommendation);
      } else {
        resultContent.innerHTML = `<p style="color:red;">오류: ${data.error || "식단 생성 실패"}</p>`;
      }
    } catch (err) {
      resultContent.innerHTML = `<p style="color:red;">서버 연결 오류: ${err.message}</p>`;
    } finally {
      btn.disabled = false;
      btn.textContent = "맞춤 식단 플랜 받기";
    }
  });
}

// 3. YouTube Data API v3 검색 프론트엔드 연동
function setupYoutubeForm() {
  const form = document.getElementById("youtube-search-form");
  if (!form) return;

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const query = document.getElementById("exercise-query").value;
    if (query.trim()) {
      searchYoutube(query);
    }
  });
}

async function searchYoutube(query) {
  const container = document.getElementById("youtube-result-container");
  const input = document.getElementById("exercise-query");
  if (input) input.value = query;

  if (!container) return;

  container.innerHTML = "<p class='loading'>YouTube Data API v3로 영상 가이드를 가져오는 중입니다...</p>";

  try {
    const response = await fetch(`/api/youtube?query=${encodeURIComponent(query)}`);
    const data = await response.json();

    if (!response.ok) {
      container.innerHTML = `<p style="color: red;">검색 오류: ${data.error}</p>`;
      return;
    }

    if (!data.videos || data.videos.length === 0) {
      container.innerHTML = "<p>검색 결과가 없습니다.</p>";
      return;
    }

    let html = `<h3 style="margin-bottom: 1rem; color: var(--primary);">🔍 '${query}' 유튜브 가이드 영상</h3>`;
    html += '<div class="youtube-grid">';

    data.videos.forEach((video) => {
      html += `
        <div class="youtube-card">
          <a href="${video.url}" target="_blank" rel="noopener noreferrer">
            <div class="thumb-wrap">
              <img src="${video.thumbnail}" alt="${video.title}">
              <div class="play-icon">▶</div>
            </div>
          </a>
          <div class="video-info">
            <h4 class="video-title">
              <a href="${video.url}" target="_blank" rel="noopener noreferrer">${video.title}</a>
            </h4>
            <p class="channel-name">${video.channelTitle}</p>
          </div>
        </div>
      `;
    });

    html += "</div>";
    container.innerHTML = html;
  } catch (err) {
    container.innerHTML = `<p style="color: red;">통신 오류: ${err.message}</p>`;
  }
}

// 4. 일일 기록장
function setupTrackerForm() {
  const btn = document.getElementById("save-log-btn");
  if (!btn) return;

  btn.addEventListener("click", () => {
    const workout = document.getElementById("workout-log").value;
    const diet = document.getElementById("diet-log").value;
    const status = document.getElementById("log-status");

    if (!workout && !diet) {
      alert("운동이나 식단 내용을 입력해주세요!");
      return;
    }

    const today = new Date().toISOString().split("T")[0];
    const logData = { date: today, workout, diet };

    localStorage.setItem(`fit_log_${today}`, JSON.stringify(logData));

    if (status) {
      status.textContent = `✅ [${today}] 일지가 저장되었습니다!`;
      setTimeout(() => {
        status.textContent = "";
      }, 3000);
    }
  });
}

// 마크다운 줄바꿈 처리
function formatMarkdown(text) {
  if (!text) return "";
  let formatted = text
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/### (.*?)\n/g, "<h3>$1</h3>")
    .replace(/## (.*?)\n/g, "<h2>$1</h2>")
    .replace(/\n/g, "<br>");
  return formatted;
}