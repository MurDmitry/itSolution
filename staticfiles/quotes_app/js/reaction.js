document.addEventListener('DOMContentLoaded', function() {
    const likeBtn = document.querySelector('.like-btn');
    const dislikeBtn = document.querySelector('.dislike-btn');
    const quoteId = document.getElementById('quote-id').value;
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    likeBtn.addEventListener('click', function() {
        fetch(`/like/${quoteId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Обновляем счетчики
                document.getElementById('likes-count').textContent = data.likes;
                document.getElementById('dislikes-count').textContent = data.dislikes;
                
                // Обновляем стили кнопок
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
                // Обновляем счетчики
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