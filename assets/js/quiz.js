/* ============================================================
   Reusable interactive quiz engine.
   Usage on a chapter page:
     <div id="quiz-root"></div>
     <script>
       window.QUIZ_ID = "ch01";
       window.QUIZ_DATA = [
         { q:"...", options:["A","B","C","D"], answer:1, explain:"..." }, ...
       ];
     </script>
     <script src="../assets/js/quiz.js"></script>

   Behaviour:
   - Renders multiple-choice questions.
   - Selections persist in localStorage (key: quiz-<QUIZ_ID>), so the reader can
     leave for the book content and come back without losing answers.
   - "Check Answers" grades, marks correct/incorrect, shows explanations & a score.
   - Reader keeps their answers, can fix the wrong ones, and re-check until 100%.
   - "Reset" clears everything for a fresh attempt.
   ============================================================ */
(function () {
  const root = document.getElementById("quiz-root");
  if (!root || !window.QUIZ_DATA) return;

  const ID = window.QUIZ_ID || "quiz";
  const KEY = "quiz-" + ID;
  const DATA = window.QUIZ_DATA;
  const N = DATA.length;

  // Restore saved answers (object: { qIndex: optionIndex })
  let answers = {};
  try { answers = JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { answers = {}; }

  const save = () => localStorage.setItem(KEY, JSON.stringify(answers));

  // ---- Build the markup ----
  let html = `
    <div class="quiz" id="quiz-${ID}">
      <div class="quiz-head">
        <h3>🧠 Check Your Understanding</h3>
        <span class="quiz-progress" id="qprog">0 / ${N} answered</span>
      </div>
      <p class="quiz-sub">Answer the questions, then press <b>Check Answers</b>. You can fix any you miss and
         check again — your progress is saved automatically, so you can pop back to the chapter anytime.</p>
      <div class="quiz-score" id="qscore"></div>
      <form id="qform">`;

  DATA.forEach((item, i) => {
    html += `<div class="q-card" data-q="${i}">
        <div class="q-text"><span class="qn">${i + 1}</span><span>${item.q}</span></div>
        <div class="q-opts">`;
    item.options.forEach((opt, j) => {
      const checked = answers[i] === j ? "checked" : "";
      const sel = answers[i] === j ? "selected" : "";
      html += `<label class="q-opt ${sel}" data-opt="${j}">
                 <input type="radio" name="q${i}" value="${j}" ${checked}>
                 <span class="opt-text">${opt}</span>
                 <span class="mark"></span>
               </label>`;
    });
    html += `</div><div class="q-explain" data-explain="${i}"></div></div>`;
  });

  html += `
      </form>
      <div class="quiz-actions">
        <button type="button" class="btn-check" id="qcheck">Check Answers</button>
        <button type="button" class="btn-reset" id="qreset">Reset</button>
      </div>
      <p class="quiz-note">Stuck? Scroll back up to review the chapter — your answers stay put.
         Want to work it out in code? Open the <a href="#notebook">companion notebook</a>.</p>
    </div>`;

  root.innerHTML = html;

  // ---- Element refs ----
  const form  = document.getElementById("qform");
  const prog  = document.getElementById("qprog");
  const score = document.getElementById("qscore");

  function answeredCount() { return Object.keys(answers).length; }
  function updateProgress() { prog.textContent = `${answeredCount()} / ${N} answered`; }

  // ---- Selection handling ----
  form.addEventListener("change", (e) => {
    if (e.target.type !== "radio") return;
    const qi = parseInt(e.target.name.slice(1), 10);
    answers[qi] = parseInt(e.target.value, 10);
    save();
    // refresh selected styling within this question
    const card = form.querySelector(`.q-card[data-q="${qi}"]`);
    card.querySelectorAll(".q-opt").forEach((lab) => {
      lab.classList.toggle("selected",
        parseInt(lab.dataset.opt, 10) === answers[qi]);
    });
    updateProgress();
  });

  // ---- Grade ----
  function grade() {
    let correct = 0;
    DATA.forEach((item, i) => {
      const card = form.querySelector(`.q-card[data-q="${i}"]`);
      const chosen = answers[i];
      card.querySelectorAll(".q-opt").forEach((lab) => {
        const j = parseInt(lab.dataset.opt, 10);
        lab.classList.remove("correct", "incorrect");
        const mark = lab.querySelector(".mark");
        mark.textContent = "";
        if (j === item.answer) {
          lab.classList.add("correct");
          if (chosen !== undefined) mark.textContent = "✓";
        } else if (chosen === j) {
          lab.classList.add("incorrect");
          mark.textContent = "✗";
        }
      });
      // explanation
      const ex = card.querySelector(".q-explain");
      ex.innerHTML = `<b>${chosen === item.answer ? "Correct!" : "Answer:"}</b> ${item.explain}`;
      ex.classList.add("show");
      if (chosen === item.answer) correct++;
    });

    // score banner
    const pct = Math.round((correct / N) * 100);
    score.className = "quiz-score show " + (correct === N ? "pass" : "partial");
    if (correct === N) {
      score.innerHTML = `<span class="qs-emoji">🎉</span>
        <span class="qs-text"><b>Perfect — ${correct}/${N} (100%)!</b><br>You've got this chapter down. On to the next!</span>`;
    } else {
      score.innerHTML = `<span class="qs-emoji">💪</span>
        <span class="qs-text"><b>${correct}/${N} correct (${pct}%)</b><br>Review the ones marked in red, adjust your answers, and Check again.</span>`;
    }
    score.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }

  // ---- Reset ----
  function reset() {
    answers = {};
    localStorage.removeItem(KEY);
    form.querySelectorAll("input[type=radio]").forEach((r) => (r.checked = false));
    form.querySelectorAll(".q-opt").forEach((l) => l.classList.remove("selected", "correct", "incorrect"));
    form.querySelectorAll(".mark").forEach((m) => (m.textContent = ""));
    form.querySelectorAll(".q-explain").forEach((e) => e.classList.remove("show"));
    score.className = "quiz-score";
    updateProgress();
  }

  document.getElementById("qcheck").addEventListener("click", grade);
  document.getElementById("qreset").addEventListener("click", reset);
  updateProgress();
})();
