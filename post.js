// Dados iniciais dos posts
let posts = [
    {
        id: 1,
        user: "Movie Buff",
        username: "@moviebuff123",
        content: "Just watched Inception - Mind blown! Christopher Nolan does it again! The plot twists, the visuals, the soundtrack - everything was perfect. What did you guys think about the ending? Let's discuss!",
        likes: 296,
        comments: 42,
        retweets: 128
    },
    {
        id: 2,
        user: "Gamer Girl",
        username: "@gamergirl456",
        content: "New God of War game announced! Just saw the trailer and the graphics look insane. The story seems to be taking an interesting turn. Who's excited to play it?",
        likes: 512,
        comments: 78,
        retweets: 256
    },
    {
        id: 3,
        user: "Binge Watcher",
        username: "@bingewatcher789",
        content: "Stranger Things Season 5 theories: After that cliffhanger in Season 4, I can't stop thinking about what might happen next. Any theories on how they'll defeat Vecna? Will Eleven's powers be enough?",
        likes: 421,
        comments: 103,
        retweets: 189
    }
];

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
