const express = require('express');
const mysql = require('mysql2/promise');
const app = express();
const pool = mysql.createPool({
    host: 'localhost',
    user: 'root',
    password: 'minhasenha123',
    database: 'HeyFriend'
});

app.use(express.json());

app.post('/add-post', async (req, res) => {
    const { nome, senha, content } = req.body;
    try {
        const [results] = await pool.execute('INSERT INTO usuarios (nome, senha) VALUES (?, ?)', [nome, senha]);
        res.status(200).json({ message: 'Post e usuário adicionados com sucesso!' });
    } catch (error) {
        console.error('Erro ao adicionar usuário:', error);
        res.status(500).json({ error: 'Erro ao adicionar usuário' });
    }
});

app.listen(3000, () => {
    console.log('Servidor rodando na porta 3000');
});
