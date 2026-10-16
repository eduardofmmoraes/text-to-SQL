SELECT p.nome
FROM projetos p
JOIN alocacoes a ON p.id = a.projeto_id
GROUP BY p.id, p.nome
HAVING COUNT(DISTINCT a.funcionario_id) >= 5;