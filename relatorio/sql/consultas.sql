-- 1. Posts por data de publicação
SELECT *
FROM portfolio_post
ORDER BY date DESC, id DESC;

-- 2. Comentários do Carrinho Autônomo
SELECT c.*
FROM portfolio_comment AS c
JOIN portfolio_post AS p ON p.id = c.post_id
WHERE p.title = 'Projeto de Carrinho Autônomo'
ORDER BY c.date DESC, c.id DESC;

-- 3. Comentários com os dados de publicação
SELECT c.id, c.text, c.date, c.author_id, p.title, p.date AS post_date
FROM portfolio_comment AS c
JOIN portfolio_post AS p ON p.id = c.post_id
WHERE p.title = 'Projeto de Carrinho Autônomo'
ORDER BY c.date DESC, c.id DESC;

-- 4. Projetos de Mecatrônica
SELECT cat.id AS category_id, cat.name, cat.description,
       p.id AS post_id, p.title, p.content, p.date
FROM portfolio_category AS cat
JOIN portfolio_post_categories AS pc ON pc.category_id = cat.id
JOIN portfolio_post AS p ON p.id = pc.post_id
WHERE cat.name = 'Mecatrônica'
ORDER BY p.title;

-- 5. Categorias com dois ou mais projetos
SELECT cat.id, cat.name, COUNT(DISTINCT pc.post_id) AS total_posts
FROM portfolio_category AS cat
JOIN portfolio_post_categories AS pc ON pc.category_id = cat.id
GROUP BY cat.id, cat.name
HAVING COUNT(DISTINCT pc.post_id) >= 2
ORDER BY cat.name;
