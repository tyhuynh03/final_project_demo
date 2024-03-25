const question = [
    {
        question: "What is larget animal in the world?",
        answers: [
            { text: "Elephant", correct: false },
            { text: "Blue Whale", correct: true },
            { text: "Giraffe", correct: false },
            { text: "Hippopotamus", correct: false }
        ]
    }
    ,
    {
        question: "What is the capital of France?",
        answers: [
            { text: "London", correct: false },
            { text: "Paris", correct: true },
            { text: "Berlin", correct: false },
            { text: "Rome", correct: false }
        ]
    },
    {
        question: "What is the capital of Vietnam?",
        answers: [
            { text: "Hanoi", correct: true },
            { text: "Ho Chi Minh City", correct: false },
            { text: "Da Nang", correct: false },
            { text: "Hue", correct: false }
        ]
    },
    {
        question: "What is the capital of Japan?",
        answers: [
            { text: "Tokyo", correct: true },
            { text: "Osaka", correct: false },
            { text: "Kyoto", correct: false },
            { text: "Nagoya", correct: false }
        ]
    },
    {
        question: "What is the capital of South Korea?",
        answers: [
            { text: "Seoul", correct: true },
            { text: "Busan", correct: false },
            { text: "Daegu", correct: false },
            { text: "Incheon", correct: false }
        ]
    }


];
// Lấy các phần tử HTML cần thêm dữ liệu vào
const questionElement = document.getElementById('question');
const answerButtons = document.getElementById('answer-buttons');
const nextButton = document.getElementById('next-btn');

let currentQuestionIndex = 0;
let score = 0;
// Hàm này cập nhật nội dung câu hỏi và các phương án trả lời lên trang HTML
function showQuestion(question) {
    questionElement.innerText = question.question;
    // Xóa bất kỳ nút trả lời cũ nào
    while (answerButtons.firstChild) {
        answerButtons.removeChild(answerButtons.firstChild);
    }
    // Thêm các nút trả lời mới
    question.answers.forEach(answer => {
        const button = document.createElement('button');
        button.innerText = answer.text;
        button.classList.add('btn');
        // Đặt thuộc tính data-correct để kiểm tra xem người dùng đã chọn đúng câu trả lời hay không
        if (answer.correct) {
            button.dataset.correct = answer.correct;
        }
        button.addEventListener('click', selectAnswer);
        answerButtons.appendChild(button);
    });
}

// Hàm này được gọi khi người dùng chọn một phương án trả lời
function selectAnswer(e) {
    const selectedButton = e.target;
    // Kiểm tra xem người dùng đã chọn đúng câu trả lời hay không
    const correct = selectedButton.dataset.correct;
    if (correct) {
        // Thêm lớp CSS để chỉ ra câu trả lời đúng
        selectedButton.classList.add('correct');
        // Tăng điểm
        score++;
    } else {
        // Thêm lớp CSS để chỉ ra câu trả lời sai
        selectedButton.classList.add('incorrect');
        const correctButton = Array.from(answerButtons.children).find(button => button.dataset.correct === 'true');
        correctButton.classList.add('correct');

    }
    // Vô hiệu hóa sự kiện click trên tất cả các nút trả lời sau khi người dùng đã chọn
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.removeEventListener('click', selectAnswer);
        button.disabled = true;
    });
    // Hiển thị nút "Next" sau khi người dùng đã chọn câu trả lời
    nextButton.style.display = 'block';
}

// Hàm này được gọi khi người dùng nhấp vào nút "Next"
function nextQuestion() {
    // Tăng chỉ số của câu hỏi hiện tại lên một đơn vị
    currentQuestionIndex++;
    // Nếu đã đến câu hỏi cuối cùng, ẩn nút "Next"
    if (currentQuestionIndex >= question.length) {
        nextButton.style.display = 'none';
        // Có thể thêm hành động khác ở đây sau khi kết thúc trắc nghiệm
        showScore(score);
    } else {
        // Hiển thị câu hỏi tiếp theo
        showQuestion(question[currentQuestionIndex]);
    }
}

resetState = () => {
    nextButton.style.display = 'none';
    while (answerButtons.firstChild) {
        answerButtons.removeChild(answerButtons.firstChild);
    }

}
function showScore() {
    resetState();
    questionElement.innerText = `Your score: ${score} out of ${question.length}! `;
    nextButton.innerHTML = "Play Again";
    nextButton.style.display = 'block';
    nextButton.addEventListener('click', playAgain);
}

// Hàm để khởi động lại trò chơi
function playAgain() {
    // Đặt lại điểm số về 0
    score = 0;
    // Đặt lại chỉ số câu hỏi về 0
    currentQuestionIndex = 0;
    // Đặt lại trạng thái của trò chơi
    resetState();
    // Hiển thị câu hỏi đầu tiên
    showQuestion(question[currentQuestionIndex]);
    // Ẩn nút "Next" sau khi đã đặt lại trạng thái
    nextButton.style.display = 'none';
    // Loại bỏ sự kiện nghe trên nút "Next" để tránh xảy ra lỗi khi nhấp vào "Play Again" nhiều lần
    nextButton.removeEventListener('click', playAgain);
    nextButton.innerHTML = "Next";

}
// Gán sự kiện cho nút "Next"
nextButton.addEventListener('click', nextQuestion)

// Hiển thị câu hỏi đầu tiên khi trang được tải
showQuestion(question[currentQuestionIndex]);
