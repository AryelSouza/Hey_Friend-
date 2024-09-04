// Dados iniciais dos posts
let posts = [];

// Função para criar um elemento HTML de post
function createPostElement(post) {
    const postElement = document.createElement('div');
    postElement.className = 'post';
    postElement.innerHTML = `
        <div class="post-header">
            <img src="/placeholder.svg?height=48&width=48" alt="User Avatar" class="post-avatar">
            <div>
                <span class="post-user">${post.user}</span>
                <span class="post-username">${post.username}</span>
            </div>
        </div>
        <div class="post-content">
            <p>${post.content}</p>
        </div>
        <div class="post-actions">
            <button class="comment-button">💬 ${post.comments}</button>
            <button class="retweet-button">🔁 ${post.retweets}</button>
            <button class="like-button" data-post-id="${post.id}">❤️ ${post.likes}</button>
        </div>
    `;
    return postElement;
}

// Função para renderizar todos os posts
function renderPosts() {
    const postsContainer = document.getElementById('posts-container');
    postsContainer.innerHTML = '';
    posts.forEach(post => {
        postsContainer.appendChild(createPostElement(post));
    });
}

// Função para adicionar um novo post
function addNewPost(content) {
    const newPost = {
        id: posts.length + 1,
        user: "Current User",
        username: "@currentuser",
        content: content,
        likes: 0,
        comments: 0,
        retweets: 0
    };
    posts.unshift(newPost);
    renderPosts();

    // Envia o novo post para o servidor
    fetch('/add-post', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            nome: 'Maria da Silva',
            senha: 'senha123',
            content: content
        })
    })
    .then(response => response.json())
    .then(data => console.log(data.message))
    .catch(error => console.error('Erro:', error));
}

// Função para lidar com o clique no botão de curtir
function handleLike(postId) {
    const post = posts.find(p => p.id === postId);
    if (post) {
        post.likes++;
        renderPosts();
    }
}

// Event listener para o botão de postagem
document.getElementById('post-button').addEventListener('click', () => {
    const content = document.getElementById('new-post-content').value;
    if (content.trim()) {
        addNewPost(content);
        document.getElementById('new-post-content').value = '';
    }
});

// Event delegation para os botões de curtir
document.getElementById('posts-container').addEventListener('click', (event) => {
    if (event.target.classList.contains('like-button')) {
        const postId = parseInt(event.target.getAttribute('data-post-id'));
        handleLike(postId);
    }
});

// Renderização inicial
renderPosts();
