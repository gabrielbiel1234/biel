document.addEventListener('DOMContentLoaded', function() {
    const startButton = document.getElementById('start-game');
    const stopButton = document.getElementById('stop-game');
    const gameContainer = document.querySelector('.game-container');
    const field = document.querySelectorAll('.field');
    const ball = document.querySelectorAll('.ball');
    const goal = document.querySelectorAll('.goal');

    startButton.addEventListener('click', function() {
        gameContainer.style.display = 'block';
    });

    stopButton.addEventListener('click', function() {
        gameContainer.style.display = 'none';
    });

    field.forEach(function(field) {
        field.addEventListener('click', function() {
            ball.forEach(function(ball) {
                ball.style.transform = 'translateX(-50%) translateY(-50%)';
            });
        });
    });

    ball.forEach(function(ball) {
        ball.addEventListener('click', function() {
            goal.forEach(function(goal) {
                goal.style.transform = 'translateX(-50%) translateY(-50%)';
            });
        });
    });
});