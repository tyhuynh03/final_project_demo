
document.addEventListener("DOMContentLoaded", function () {
    var questions = document.querySelectorAll('.question-card');
    var submitted = false;
    var correctAnswers = 0;
    var totalQuestions = '{{ questions| length }}';


    var score = 0;
    var timerDisplay = document.getElementById("timer");
    var timeLeftDisplay = document.getElementById("time-left");
    var timerSeconds = totalQuestions * 60;
    var timerInterval;

    function updateProgress() {
        var selectedChoices = document.querySelectorAll(".selected");
        var progressText = document.getElementById("progress-text");
        progressText.textContent =
            "Số câu đã làm " +
            selectedChoices.length +
            "/" +
            totalQuestions;
    }

    function searchAndSetImage(questionElement) {
        var PIXABAY_API_KEY = '26083203-47b9c5301cbb2e7ff55fe3990';
        var PIXABAY_API_URL = 'https://pixabay.com/api/?key=' + PIXABAY_API_KEY + '&image_type=photo';

        fetch(PIXABAY_API_URL)
            .then(response => response.json())
            .then(data => {
                if (data.hits.length > 0) {
                    var imageUrl = data.hits[Math.floor(Math.random() * data.hits.length)].webformatURL;
                    var questionImage = questionElement.querySelector('.question-image');
                    questionImage.src = imageUrl;
                    if (questionImage.clientHeight > questionImage.clientWidth) {
                        questionImage.style.width = 'auto';
                        questionImage.style.height = '100%';
                    } else {
                        questionImage.style.width = '100%';
                        questionImage.style.height = 'auto';
                    }
                }
            })
            .catch(error => console.error('Error fetching images from Pixabay:', error));
    }

    questions.forEach(function (question) {
        searchAndSetImage(question);

        var choices = question.querySelectorAll(".choice");
        choices.forEach(function (choice) {
            choice.addEventListener("click", function () {
                if (!submitted) {
                    var questionNumber = choice.dataset.question;
                    var selectedChoices = document.querySelectorAll('.choice[data-question="' + questionNumber + '"].selected');
                    selectedChoices.forEach(function (selectedChoice) {
                        selectedChoice.classList.remove("selected");
                    });

                    choice.classList.add("selected");
                    updateProgress();
                    updateQuestionStatus(); // Cập nhật trạng thái câu hỏi khi có lựa chọn mới
                }
            });

            choice.addEventListener("mouseenter", function () {
                if (!submitted && !choice.classList.contains("selected")) {
                    choice.style.backgroundColor = "#f0f0f0";
                }
            });

            choice.addEventListener("mouseleave", function () {
                if (!submitted && !choice.classList.contains("selected")) {
                    choice.style.backgroundColor = "";
                }
            });
        });
    });

    document.getElementById("submit-button").addEventListener("click", function () {
        if (!submitted) {
            submitted = true;
            clearInterval(timerInterval);
            var quizForm = document.getElementById("quiz-form");
            var selectedChoices = quizForm.querySelectorAll(".selected");

            selectedChoices.forEach(function (selectedChoice) {
                var questionNumber = selectedChoice.dataset.question;
                var questionElement = document.querySelector('.question-card[data-question="' + questionNumber + '"]');
                var correctChoice = questionElement.querySelector('.choice[data-choice="1"]');

                if (selectedChoice === correctChoice) {
                    correctAnswers++;
                }
            });

            score = (correctAnswers / totalQuestions) * 10;

            var resultContainer = document.getElementById("result-container");
            resultContainer.innerHTML = "<p>Số câu đã làm: " + selectedChoices.length + "/" + totalQuestions + "</p>";
            resultContainer.innerHTML += "<p>Số câu làm đúng: " + correctAnswers + "</p>";
            resultContainer.innerHTML += "<p>Số câu làm sai: " + (totalQuestions - correctAnswers) + "</p>";
            resultContainer.innerHTML += timerDisplay.textContent + "</p>";
            resultContainer.innerHTML += "<p>Số điểm đạt được: " + score + "</p>";
            resultContainer.style.display = 'block';

        }
    });

    function startTimer() {
        timerInterval = setInterval(function () {
            timerSeconds--;
            var minutes = Math.floor(timerSeconds / 60);
            var seconds = timerSeconds % 60;
            timerDisplay.textContent = "Thời gian còn lại: " + minutes + " phút " + seconds + " giây";

            if (timerSeconds <= 0) {
                clearInterval(timerInterval);
                timerDisplay.textContent = "Hết thời gian";
                document.getElementById("submit-button").click();
            }
        }, 1000);
    }

    startTimer();

    // Bảng trạng thái câu hỏi
    var questionStatusContainer = document.getElementById("question-status").querySelector("ul");

    questions.forEach(function (question, index) {
        var questionNumber = index + 1;
        var listItem = document.createElement("li");
        listItem.textContent = "Câu " + questionNumber;
        listItem.setAttribute("data-question", questionNumber);
        questionStatusContainer.appendChild(listItem);

        listItem.addEventListener("click", function () {
            var questionIndex = parseInt(listItem.getAttribute("data-question")) - 1;
            questions[questionIndex].scrollIntoView({ behavior: "smooth", block: "center" });
        });
    });

    function updateQuestionStatus() {
        questions.forEach(function (question, index) {
            var questionNumber = index + 1;
            var listItem = questionStatusContainer.querySelector('li[data-question="' + questionNumber + '"]');
            var selectedChoice = question.querySelector(".selected");

            if (selectedChoice) {
                listItem.style.color = "green"; // Chuyển màu chữ thành xanh lá khi câu hỏi đã được làm
            }
        });
    }
    updateQuestionStatus(); // Cập nhật trạng thái ban đầu
});

// thêm tính năng chọn đáp án câu 1 thì chuyển sang câu 2
// Lấy danh sách các lựa chọn từ mỗi câu hỏi
var choices = document.querySelectorAll('.choices .choice');

choices.forEach(function (choice) {
    choice.addEventListener('click', function () {
        // Kiểm tra xem người dùng đã chọn một đáp án chưa
        // Cuộn xuống câu hỏi tiếp theo
        var nextQuestionNumber = parseInt(choice.dataset.question) + 1;
        var nextQuestion = document.querySelector('.question-card[data-question="' + nextQuestionNumber + '"]');
        if (nextQuestion) {
            nextQuestion.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }

    });
});



