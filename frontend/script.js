// ==================== BASE URL ===========================
const BASE_URL = "https://quizzo-backend-086b.onrender.com";

// ==================== AUTH MODULE ===========================

function setupSignupForm() {
    const form = document.getElementById("signup-form");
    if (!form) return;
    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        const username = document.getElementById("signup-username").value;
        const email = document.getElementById("signup-email").value;
        const password = document.getElementById("signup-password").value;
        const role = document.getElementById("signup-role").value;
        const response = await fetch(`${BASE_URL}/auth/signup`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, email, password, role })
        });
        const data = await response.json();
        if (response.ok) {
            alert("Signup successful! Redirecting you to log in page");
            window.location.href = "login.html";
        } else {
            alert(`Signup failed: ${data.detail}`);
        }
    });
}

function setupLoginForm() {
    const form = document.getElementById("login-form");
    if (!form) return;
    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        const username = document.getElementById("login-username").value;
        const password = document.getElementById("login-password").value;
        const response = await fetch(`${BASE_URL}/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        });
        const data = await response.json();
        if (response.ok) {
            localStorage.setItem("username", username);
            fetch(`${BASE_URL}/user-id-by-username/${username}`)
                .then(res => res.json())
                .then(userData => {
                    if (userData.user_id) {
                        localStorage.setItem("user_id", userData.user_id);
                    }
                    fetch(`${BASE_URL}/quizzes/role/${username}`)
                        .then(roleRes => roleRes.json())
                        .then(roleData => {
                            if (roleData.role === "admin") {
                                window.location.href = "CreateQuiz.html";
                            } else if (roleData.role === "student") {
                                window.location.href = "JoinQuiz.html";
                            } else {
                                alert("Role of the user doesn't exist");
                            }
                        })
                        .catch(() => {
                            alert("Failed to fetch role. Please try again.");
                        });
                })
                .catch(() => {
                    alert("Failed to fetch user id.");
                });
        } else {
            alert(`Login failed: ${data.detail}`);
        }
    });
}

function setupGoogleLogin() {
    const googleBtn = document.getElementById("google-login");
    if (googleBtn) {
        googleBtn.addEventListener("click", () => {
            window.location.href = `${BASE_URL}/auth/google/login`;
        });
    }
}

function handleGoogleCallback() {
    const params = new URLSearchParams(window.location.search);
    const email = params.get("email");
    if (!email) return;
    localStorage.setItem("email", email);
    fetch(`${BASE_URL}/username-by-email/${email}`)
        .then(res => res.json())
        .then(userData => {
            if (!userData.username) {
                alert("No username found for this email.");
                window.location.href = "login.html";
                return;
            }
            localStorage.setItem("username", userData.username);
            fetch(`${BASE_URL}/user-id-by-username/${userData.username}`)
                .then(res => res.json())
                .then(idData => {
                    if (idData.user_id) {
                        localStorage.setItem("user_id", idData.user_id);
                    }
                    fetch(`${BASE_URL}/quizzes/role/${userData.username}`)
                        .then(res => res.json())
                        .then(data => {
                            if (data.role === "admin") {
                                window.location.href = "CreateQuiz.html";
                            } else if (data.role === "student") {
                                window.location.href = "JoinQuiz.html";
                            } else {
                                alert("Role of the user doesn't exist");
                                window.location.href = "login.html";
                            }
                        })
                        .catch(() => {
                            alert("Could not determine user role.");
                            window.location.href = "login.html";
                        });
                })
                .catch(() => {
                    alert("Could not fetch user id for this username.");
                    window.location.href = "login.html";
                });
        })
        .catch(() => {
            alert("Could not fetch username for this email.");
            window.location.href = "login.html";
        });
    window.history.replaceState({}, document.title, window.location.pathname);
}

// ==================== QUIZ CREATION MODULE ===========================
function setupCreateQuizPage() {
    const form = document.getElementById("create-quiz-form");
    const quizzesList = document.getElementById("quizzes-list");
    const username = localStorage.getItem("username");
    if (!form || !quizzesList) return;
    if (!username) {
        alert("Please log in first.");
        window.location.href = "login.html";
        return;
    }
    fetch(`${BASE_URL}/quizzes/user/${username}`)
        .then(response => {
            if (!response.ok) throw new Error("Failed to fetch quizzes");
            return response.json();
        })
        .then(quizzes => {
            quizzes.forEach(displayQuiz);
        })
        .catch(error => {
            alert("Error: " + error.message);
        });

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        const title = document.getElementById("quiz-title").value;
        const description = document.getElementById("quiz-description").value;
        const timeLimit = parseInt(document.getElementById("quiz-time-limit").value);
        if (!title || !description || isNaN(timeLimit)) {
            alert("Please fill all fields correctly.");
            return;
        }
        const quizData = { title, description, time_limit: timeLimit, created_by: username };
        try {
            const response = await fetch(`${BASE_URL}/quizzes/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(quizData)
            });
            if (!response.ok) throw new Error("Failed to create quiz");
            const newQuiz = await response.json();
            alert("Quiz created successfully!");
            form.reset();
            displayQuiz(newQuiz);
        } catch (error) {
            alert("Error: " + error.message);
        }
    });

    function displayQuiz(quiz) {
        const quizzesList = document.getElementById("quizzes-list");
        const quizDiv = document.createElement("div");
        quizDiv.innerHTML = `
        <div class="quiz-item" role="region" aria-label="Quiz titled Sample Quiz 1">
            <h3>${quiz.title}</h3>
            <p><strong>Quiz ID:</strong> ${quiz.id} (Share this id with your students!)</p>
            <p><strong>Description:</strong> ${quiz.description}</p>
            <p><strong>Time Limit:</strong> ${quiz.time_limit} minutes</p>
            <button class="edit-btn" data-id="${quiz.id}">EDIT</button>
            <button class="leaderboard-btn" data-id="${quiz.id}">LEADERBOARD</button>
            <hr>
        </div>
        `;
        quizzesList.prepend(quizDiv);
        quizDiv.querySelector(".edit-btn").addEventListener("click", () => {
            localStorage.setItem("quiz_id", quiz.id);
            window.location.href = "questions.html";
        });
        quizDiv.querySelector(".leaderboard-btn").addEventListener("click", () => {
            localStorage.setItem("quiz_id", quiz.id);
            window.location.href = "leaderboard.html";
        });
    }
}

// ==================== QUESTION EDITOR MODULE ===========================
function setupQuestionEditor() {
    const form = document.getElementById("create-question");
    const questionInput = document.getElementById("question");
    const A = document.getElementById("op1");
    const B = document.getElementById("op2");
    const C = document.getElementById("op3");
    const D = document.getElementById("op4");
    const correct = document.getElementById("co_op");
    const quiz_id = localStorage.getItem("quiz_id");
    const questionsList = document.getElementById("Questions-list");
    if (!form || !questionsList) return;
    if (!quiz_id) {
        alert("Quiz ID not found. Please select a quiz first.");
        return;
    }
    async function loadQuestions() {
        questionsList.innerHTML = "";
        try {
            const response = await fetch(`${BASE_URL}/questions/quiz/${quiz_id}`);
            const questions = await response.json();
            questions.forEach(q => {
                const div = document.createElement("div");
                div.innerHTML = `
                    <strong>Q:</strong> ${q.question}<br>
                    A: ${q.A} | B: ${q.B} | C: ${q.C} | D: ${q.D} <br>
                    Correct: ${q.correct}
                    <br>
                    <button class="edit-btn" data-id="${q.id}">Edit</button>
                    <button class="delete-btn" data-id="${q.id}">Delete</button>
                    <hr>
                `;
                questionsList.appendChild(div);
            });
        } catch (error) {
            console.error("Error loading questions:", error);
        }
    }
    loadQuestions();
    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const questionData = {
            quiz_id: parseInt(quiz_id),
            question: questionInput.value,
            A: A.value,
            B: B.value,
            C: C.value,
            D: D.value,
            correct: correct.value
        };
        try {
            const response = await fetch(`${BASE_URL}/questions/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(questionData)
            });
            if (response.ok) {
                questionInput.value = "";
                A.value = "";
                B.value = "";
                C.value = "";
                D.value = "";
                correct.value = "";
                await loadQuestions();
            } else {
                alert("Failed to create question.");
            }
        } catch (error) {
            console.error("Error creating question:", error);
        }
    });
    questionsList.addEventListener("click", async (e) => {
        const id = e.target.dataset.id;
        if (e.target.classList.contains("delete-btn")) {
            await fetch(`${BASE_URL}/questions/${id}`, { method: "DELETE" });
            await loadQuestions();
        }
        if (e.target.classList.contains("edit-btn")) {
            const newQuestion = prompt("Enter new question text:");
            const newA = prompt("Enter new Option A:");
            const newB = prompt("Enter new Option B:");
            const newC = prompt("Enter new Option C:");
            const newD = prompt("Enter new Option D:");
            const newCorrect = prompt("Enter new correct option (A/B/C/D):");
            const updatedQuestion = {
                quiz_id: parseInt(quiz_id),
                question: newQuestion,
                A: newA,
                B: newB,
                C: newC,
                D: newD,
                correct: newCorrect
            };
            await fetch(`${BASE_URL}/questions/${id}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(updatedQuestion)
            });
            await loadQuestions();
        }
    });
}

// ==================== QUIZ JOIN & PLAY MODULE ===========================
function setupJoinQuizPage() {
    const fetchBtn = document.getElementById("fetch-quiz-btn");
    if (!fetchBtn) return;
    fetchBtn.addEventListener("click", fetchQuizDetails);
}

async function fetchQuizDetails() {
    const quizId = document.getElementById("quiz-id-input").value;
    try {
        const response = await fetch(`${BASE_URL}/quizzes/${quizId}`);
        if (!response.ok) {
            alert("Quiz not found");
            return;
        }
        const quiz = await response.json();
        document.getElementById("quiz-info-section").style.display = "block";
        document.getElementById("quiz-title").textContent = `Title: ${quiz.title}`;
        document.getElementById("quiz-desc").textContent = `Description: ${quiz.description}`;
        document.getElementById("quiz-time").textContent = `Time Limit: ${quiz.time_limit} minutes`;
        sessionStorage.setItem("quiz_id", quizId);
    } catch (error) {
        console.error("Error fetching quiz:", error);
        alert("Server error");
    }
}

function startQuiz() {
     const quizId = document.getElementById("quiz-id-input").value;
    if (!quizId) {
        alert("Please enter a Quiz ID");
        return;
    }
    sessionStorage.setItem("quiz_id", quizId);
    window.location.href = `quiz.html?quiz_id=${quizId}`;
}

async function setupQuizPage() {
    if (!window.location.pathname.endsWith("quiz.html")) return;

    let quizId = sessionStorage.getItem("quiz_id");
    const user_id = localStorage.getItem("user_id");

    if (quizId) {
        localStorage.setItem("quiz_id", quizId);  // Sync to avoid issues
    }

    if (!quizId || !user_id) {
        alert("Quiz ID or user ID missing!");
        return;
    }

    console.log("Using quiz_id:", quizId); // Optional debug

    try {
        const checkRes = await fetch(`${BASE_URL}/results/${user_id}/${quizId}`);
        if (checkRes.ok) {
            alert("You've already completed this quiz.");
            window.location.href = "result.html";
            return;
        }
    } catch (err) {
        if (err instanceof TypeError || err.message.includes("Failed to fetch")) {
            alert("Unable to connect to server. Please check your backend.");
            return;
        }
    }
    const questionsContainer = document.getElementById("questions");
    if (!questionsContainer) {
        alert("Questions container not found in HTML!");
        return;
    }
    let questions = [];
    let currentQuestion = parseInt(localStorage.getItem("currentQuestion")) || 0;
    let correctAnswers = parseInt(localStorage.getItem("correctAnswers")) || 0;
    let totalQuestions = 0;
    let timeLimit = 60;
    let startTime = parseInt(localStorage.getItem("startTime"));
    if (!startTime) {
        startTime = Date.now();
        localStorage.setItem("startTime", startTime);
    }
    const timerEl = document.createElement("div");
    timerEl.style.fontSize = "20px";
    timerEl.style.marginBottom = "10px";
    document.body.insertBefore(timerEl, document.body.firstChild);
    function updateTimer() {
        const elapsed = Math.floor((Date.now() - startTime) / 1000);
        const remaining = timeLimit - elapsed;
        if (remaining <= 0) {
            submitQuiz();
            return;
        }
        timerEl.textContent = `⏱️ Time Left: ${Math.floor(remaining / 60)}:${String(remaining % 60).padStart(2, "0")}`;
    }
    const timerInterval = setInterval(updateTimer, 1000);
    history.pushState(null, null, location.href);
    window.onpopstate = () => history.go(1);
    try {
        const res = await fetch(`${BASE_URL}/questions/quiz/${quizId}`);
        questions = await res.json();
        totalQuestions = questions.length;
    } catch (err) {
        alert("Error loading quiz questions.");
        return;
    }
    try {
        const quizRes = await fetch(`${BASE_URL}/quizzes/${quizId}`);
        const quiz = await quizRes.json();
        timeLimit = quiz.time_limit * 60;
    } catch (err) {
        console.warn("Could not fetch quiz time limit. Using default.");
    }
    function renderQuestion() {
        if (!questions[currentQuestion]) {
            alert("⚠️ Question data is missing.");
            return;
        }
        const q = questions[currentQuestion];
        questionsContainer.innerHTML = "";
        const questionTitle = document.createElement("h4");
        questionTitle.textContent = `Q${currentQuestion + 1}. ${q.question}`;
        questionsContainer.appendChild(questionTitle);
        const optionMap = [q.A, q.B, q.C, q.D];
        optionMap.forEach((optionText, i) => {
            const optionId = `op${i + 1}`;
            const labelId = `label${i + 1}`;
            const optionWrapper = document.createElement("div");
            optionWrapper.innerHTML = `
                <input type="radio" name="option" id="${optionId}">
                <label for="${optionId}" id="${labelId}">${String.fromCharCode(65 + i)}. ${optionText}</label>
            `;
            questionsContainer.appendChild(optionWrapper);
            const radio = optionWrapper.querySelector(`#${optionId}`);
            radio.addEventListener("change", () => {
                handleAnswer(i);
            });
        });
    }
    function disableOptions(correctIndex, selectedIndex) {
        [questions[currentQuestion].A, questions[currentQuestion].B, questions[currentQuestion].C, questions[currentQuestion].D].forEach((_, i) => {
            const input = document.getElementById(`op${i + 1}`);
            const label = document.getElementById(`label${i + 1}`);
            if (input) input.disabled = true;
            const mark = document.createElement("span");
            if (i === correctIndex) {
                mark.textContent = " ✔️";
                mark.style.color = "green";
            } else if (i === selectedIndex) {
                mark.textContent = " ❌";
                mark.style.color = "red";
            }
            if (label) label.appendChild(mark);
        });
    }
    function handleAnswer(selectedIndex) {
        const q = questions[currentQuestion];
        const correctIndex = ["A", "B", "C", "D"].indexOf(q.correct);
        if (selectedIndex === correctIndex) correctAnswers++;
        disableOptions(correctIndex, selectedIndex);
        localStorage.setItem("correctAnswers", correctAnswers);
        localStorage.setItem("currentQuestion", currentQuestion + 1);
        setTimeout(() => {
            currentQuestion++;
            if (currentQuestion >= questions.length) {
                submitQuiz();
            } else {
                renderQuestion();
            }
        }, 1000);
    }
    function submitQuiz() {
        clearInterval(timerInterval);
        const endTime = Date.now();
        const timeTaken = Math.floor((endTime - startTime) / 1000);
        const score = Math.round((((timeTaken / timeLimit) * 100) + ((correctAnswers / totalQuestions) * 100)) / 2);
        fetch(`${BASE_URL}/results/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                user_id: parseInt(localStorage.getItem("user_id")),
                quiz_id: parseInt(quizId),
                score,
                total_questions: totalQuestions,
                submitted_at: new Date().toISOString(),
                username: localStorage.getItem("username")
            })
        })
        .then(res => res.json())
        .then(data => {
            alert(`✅ Quiz Submitted! Your Score: ${score}`);
            localStorage.removeItem("currentQuestion");
            localStorage.removeItem("correctAnswers");
            localStorage.removeItem("startTime");
            window.location.href = "result.html";
        })
        .catch(err => {
            console.error("Error submitting result:", err);
            alert("Error submitting result");
        });
    }
    renderQuestion();
    updateTimer();
}

// ==================== RESULT MODULE ===========================
async function loadResult() {
    const user_id = localStorage.getItem("user_id");
    const quizId = localStorage.getItem("quiz_id");
    if (!user_id || !quizId) {
        alert("Missing user or quiz information.");
        return;
    }
    try {
        const res = await fetch(`${BASE_URL}/results/${user_id}/${quizId}`);
        if (!res.ok) throw new Error("Result not found.");
        const data = await res.json();
        document.getElementById("username").textContent = `👤 User ID: ${user_id}`;
        document.getElementById("quiz-id").textContent = `📝 Quiz ID: ${quizId}`;
        document.getElementById("score").textContent = `✅ Score: ${data.score}`;
        document.getElementById("total-questions").textContent = `📊 Total Questions: ${data.total_questions}`;
        document.getElementById("submitted-at").textContent = `📅 Submitted At: ${new Date(data.submitted_at).toLocaleString()}`;
    } catch (err) {
        console.error(err);
        alert("Could not load result.");
    }
}

function goToDashboard() {
    window.location.href = "JoinQuiz.html";
}

// ==================== LEADERBOARD MODULE ===========================
function setupLeaderboardPage() {
    const quizId = localStorage.getItem("quiz_id");
    const leaderboardBody = document.getElementById("leaderboard-body");
    if (!quizId || !leaderboardBody) return;
    async function fetchLeaderboard() {
        try {
            const res = await fetch(`${BASE_URL}/leaderboard/${quizId}`);
            if (!res.ok) throw new Error("Failed to fetch leaderboard");
            const data = await res.json();
            leaderboardBody.innerHTML = "";
            data.forEach((entry, index) => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${index + 1}</td>
                    <td>${entry.username}</td>
                    <td>${entry.score}</td>
                    <td>${entry.total_questions}</td>
                    <td>${new Date(entry.submitted_at).toLocaleString()}</td>
                `;
                leaderboardBody.appendChild(row);
            });
        } catch (err) {
            console.error("Error:", err.message);
        }
    }
    fetchLeaderboard();
    setInterval(fetchLeaderboard, 5000);
}

window.addEventListener("load", async () => {
  try {
    const response = await fetch(`${BASE_URL}/latest-quizzes`);
    const quizzes = await response.json();

    const section = document.getElementById("latest-quizzes");
    section.innerHTML = quizzes.map(quiz => `
      <article class="feature-card">
        <h3 class="feature-title">${quiz.title}</h3>
        <p class="feature-desc">${quiz.description}</p>
        <p class="feature-desc"><strong>Time Limit:</strong> ${quiz.time_limit} min</p>
      </article>
    `).join("");
  } catch (error) {
    console.error("Error fetching latest quizzes:", error);
  }
});


// ==================== MAIN ENTRY ===========================
document.addEventListener("DOMContentLoaded", () => {
    setupSignupForm();
    setupLoginForm();
    setupGoogleLogin();
    handleGoogleCallback();
    setupCreateQuizPage();
    setupQuestionEditor();
    setupJoinQuizPage();
    if (window.location.pathname.endsWith("CreateQuiz.html")) {
        setupCreateQuizPage();
    }
    setupLeaderboardPage();
    if (window.location.pathname.endsWith("result.html")) loadResult();
});