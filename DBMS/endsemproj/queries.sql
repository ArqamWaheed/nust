USE finance_tracker;

-- Q1. Net worth of a user (cash + investments) in PKR
SELECT * FROM v_net_worth WHERE user_id = 1;

-- Q2. Monthly income vs expense for a user (last 6 months)
SELECT DATE_FORMAT(t.txn_date, '%Y-%m') AS month,
       SUM(CASE WHEN t.txn_type = 'income'  THEN t.amount ELSE 0 END) AS income,
       SUM(CASE WHEN t.txn_type = 'expense' THEN t.amount ELSE 0 END) AS expense,
       SUM(CASE WHEN t.txn_type = 'income'  THEN t.amount ELSE 0 END)
     - SUM(CASE WHEN t.txn_type = 'expense' THEN t.amount ELSE 0 END) AS net_savings
FROM transactions t
JOIN accounts a ON a.account_id = t.account_id
WHERE a.user_id = 1
  AND t.txn_date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
GROUP BY DATE_FORMAT(t.txn_date, '%Y-%m')
ORDER BY month;

-- Q3. Budget vs actual for the current month — over/under per category
SELECT category_name, limit_amount, actual_spent, remaining, pct_used,
       CASE WHEN actual_spent > limit_amount THEN 'OVER'
            WHEN actual_spent >= 0.8 * limit_amount THEN 'WARNING'
            ELSE 'OK' END AS status
FROM v_budget_status
WHERE user_id = 1 AND month_year = '2025-05-01'
ORDER BY pct_used DESC;

-- Q4. Top 5 spending categories this month
SELECT c.category_name, SUM(t.amount) AS total_spent
FROM transactions t
JOIN accounts   a ON a.account_id  = t.account_id
JOIN categories c ON c.category_id = t.category_id
WHERE a.user_id = 1
  AND t.txn_type = 'expense'
  AND t.txn_date >= '2025-05-01' AND t.txn_date < '2025-06-01'
GROUP BY c.category_name
ORDER BY total_spent DESC
LIMIT 5;

-- Q5. Portfolio with gain/loss & ROI per holding
SELECT type_name, asset_name, symbol, quantity, buy_price, current_price,
       cost_basis, market_value, gain_loss, roi_pct
FROM v_portfolio
WHERE user_id = 1
ORDER BY gain_loss DESC;

-- Q6. Aggregate portfolio ROI for a user
SELECT ROUND(SUM(gain_loss) / SUM(cost_basis) * 100, 2) AS portfolio_roi_pct,
       SUM(cost_basis)   AS total_invested,
       SUM(market_value) AS total_value,
       SUM(gain_loss)    AS total_gain_loss
FROM v_portfolio
WHERE user_id = 1;

-- Q7. Savings goal progress
SELECT goal_name, target_amount, contributed, pct_complete, status
FROM v_goal_progress
WHERE user_id = 1
ORDER BY pct_complete DESC;

-- Q8. Full transaction history of one account (most recent first)
SELECT t.txn_date, t.txn_type, t.amount, c.category_name, t.description
FROM transactions t
LEFT JOIN categories c ON c.category_id = t.category_id
WHERE t.account_id = 1
ORDER BY t.txn_date DESC, t.txn_id DESC;

-- Q9. Account balances of a user normalised to PKR
SELECT account_name, currency_code, balance, balance_pkr
FROM v_account_balances_pkr
WHERE user_id = 1
ORDER BY balance_pkr DESC;

-- Q10. Users who exceeded ANY budget this month (admin/auditor report)
SELECT u.full_name, c.category_name, b.limit_amount, bs.actual_spent, bs.pct_used
FROM v_budget_status bs
JOIN users      u ON u.user_id     = bs.user_id
JOIN categories c ON c.category_id = bs.category_id
JOIN budgets    b ON b.user_id = bs.user_id AND b.category_id = bs.category_id AND b.month_year = bs.month_year
WHERE bs.month_year = '2025-05-01'
  AND bs.actual_spent > b.limit_amount
ORDER BY bs.pct_used DESC;

-- Q11. Largest single expense per user this year (window-style via correlated subquery)
SELECT a.user_id, t.txn_date, t.amount, c.category_name, t.description
FROM transactions t
JOIN accounts a   ON a.account_id  = t.account_id
JOIN categories c ON c.category_id = t.category_id
WHERE t.txn_type = 'expense'
  AND t.amount = (
        SELECT MAX(t2.amount)
        FROM transactions t2
        JOIN accounts a2 ON a2.account_id = t2.account_id
        WHERE a2.user_id = a.user_id AND t2.txn_type = 'expense'
          AND YEAR(t2.txn_date) = YEAR(t.txn_date)
  );

-- Q12. Average monthly food spend (a UDF-style derived metric)
SELECT ROUND(AVG(monthly_total), 2) AS avg_monthly_food
FROM (
    SELECT DATE_FORMAT(t.txn_date, '%Y-%m') AS m, SUM(t.amount) AS monthly_total
    FROM transactions t
    JOIN accounts   a ON a.account_id  = t.account_id
    JOIN categories c ON c.category_id = t.category_id
    WHERE a.user_id = 1 AND c.category_name = 'Food' AND t.txn_type = 'expense'
    GROUP BY DATE_FORMAT(t.txn_date, '%Y-%m')
) m;
