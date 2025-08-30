document.addEventListener('DOMContentLoaded', function() {
    const likeBtn = document.querySelector('.like-btn');            // Кнопка лайка по CSS классу
    const dislikeBtn = document.querySelector('.dislike-btn');      // Кнопка дизлайка по CSS классу
    const quoteId = document.getElementById('quote-id').value;      // id цитаты
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Обработчик события клика на кнопку лайка
    likeBtn.addEventListener('click', function() {
        fetch(`/like/${quoteId}/`, {                // POST запрос для лайка
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Обновление счетчиков
                document.getElementById('likes-count').textContent = data.likes;
                document.getElementById('dislikes-count').textContent = data.dislikes;
                
                // Обновление стилей кнопок
                if (likeBtn.classList.contains('btn-dark')) {
                    likeBtn.classList.remove('btn-dark');
                    likeBtn.classList.add('btn-outline-dark');
                } else {
                    likeBtn.classList.remove('btn-outline-dark');
                    likeBtn.classList.add('btn-dark');
                    dislikeBtn.classList.remove('btn-dark');
                    dislikeBtn.classList.add('btn-outline-dark');
                }
            }
        });
    });

    // Для дизлайка
    dislikeBtn.addEventListener('click', function() {
        fetch(`/dislike/${quoteId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('likes-count').textContent = data.likes;
                document.getElementById('dislikes-count').textContent = data.dislikes;
                
                // Обновляем стили кнопок
                if (dislikeBtn.classList.contains('btn-dark')) {
                    dislikeBtn.classList.remove('btn-dark');
                    dislikeBtn.classList.add('btn-outline-dark');
                } else {
                    dislikeBtn.classList.remove('btn-outline-dark');
                    dislikeBtn.classList.add('btn-dark');
                    likeBtn.classList.remove('btn-dark');
                    likeBtn.classList.add('btn-outline-dark');
                }
            }
        });
    });
});