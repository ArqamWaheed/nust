USE finance_tracker;

-- ---------- Currencies ----------
INSERT INTO currencies (currency_code, currency_name, symbol) VALUES
  ('PKR',  'Pakistani Rupee', 'Rs.'),
  ('USD',  'US Dollar',       '$'),
  ('USDT', 'Tether',          '$'),
  ('AED',  'UAE Dirham',      'د.إ');

-- ---------- Exchange rates (to PKR) ----------
INSERT INTO exchange_rates (from_currency, to_currency, rate, effective_date) VALUES
  ('USD',  'PKR', 278.50, '2025-04-01'),
  ('USD',  'PKR', 281.20, '2025-05-01'),
  ('USDT', 'PKR', 281.00, '2025-05-01'),
  ('AED',  'PKR',  76.50, '2025-05-01');

-- ---------- Account types ----------
INSERT INTO account_types (type_name) VALUES
  ('Bank Account'),
  ('Mobile Wallet'),
  ('Cash'),
  ('Crypto Exchange'),
  ('Brokerage');

-- ---------- Categories (system-managed taxonomy) ----------
INSERT INTO categories (category_name, kind, is_system) VALUES
  ('Salary',        'income',  TRUE),
  ('Freelance',     'income',  TRUE),
  ('Business',      'income',  TRUE),
  ('Gift',          'income',  TRUE),
  ('Food',          'expense', TRUE),
  ('Transport',     'expense', TRUE),
  ('Rent',          'expense', TRUE),
  ('Utilities',     'expense', TRUE),
  ('Entertainment', 'expense', TRUE),
  ('Health',        'expense', TRUE),
  ('Education',     'expense', TRUE),
  ('Shopping',      'expense', TRUE);

-- ---------- Investment types ----------
INSERT INTO investment_types (type_name, unit_label) VALUES
  ('Stock',  'shares'),
  ('Crypto', 'coins'),
  ('Gold',   'grams');

-- ---------- Users (3 stakeholders represented) ----------
-- password_hash values are illustrative bcrypt strings
INSERT INTO users (full_name, email, password_hash, role) VALUES
  ('Arqam Waheed',     'arqam@example.com',   '$2b$12$abcdefghijklmnopqrstuu1234567890ABCDEFGHIJKLMNOPQRST', 'user'),
  ('Hira Khan',        'hira@example.com',    '$2b$12$bcdefghijklmnopqrstuvv2345678901BCDEFGHIJKLMNOPQRSTU', 'user'),
  ('System Admin',     'admin@example.com',   '$2b$12$cdefghijklmnopqrstuvww3456789012CDEFGHIJKLMNOPQRSTUV', 'admin'),
  ('Audit Reviewer',   'auditor@example.com', '$2b$12$defghijklmnopqrstuvwxx4567890123DEFGHIJKLMNOPQRSTUVW', 'auditor');

-- ---------- Accounts ----------
INSERT INTO accounts (user_id, account_name, type_id, currency_code) VALUES
  (1, 'Meezan Bank',   1, 'PKR'),
  (1, 'JazzCash',      2, 'PKR'),
  (1, 'Cash in Hand',  3, 'PKR'),
  (1, 'Binance',       4, 'USDT'),
  (1, 'Zerodha',       5, 'USD'),
  (2, 'HBL Savings',   1, 'PKR'),
  (2, 'EasyPaisa',     2, 'PKR');

-- ---------- Transactions: income & expense ----------
-- (Triggers will update accounts.balance automatically.)
INSERT INTO transactions (account_id, category_id, txn_type, amount, txn_date, description) VALUES
  (1, 1, 'income',  150000.00, '2025-05-01', 'Monthly salary'),
  (1, 7, 'expense',  35000.00, '2025-05-02', 'Rent — May'),
  (1, 8, 'expense',   8500.00, '2025-05-03', 'Electricity bill'),
  (2, 5, 'expense',   2400.00, '2025-05-04', 'Groceries'),
  (2, 6, 'expense',   1200.00, '2025-05-05', 'Careem'),
  (2, 5, 'expense',    900.00, '2025-05-07', 'Lunch with friends'),
  (3, 5, 'expense',    600.00, '2025-05-08', 'Tuck shop'),
  (1, 2, 'income',   60000.00, '2025-05-10', 'Freelance gig'),
  (1, 9, 'expense',   3500.00, '2025-05-12', 'Cinema + dinner'),
  (1,11, 'expense',  12000.00, '2025-05-14', 'Online course'),
  (6, 1, 'income',  220000.00, '2025-05-01', 'Salary'),
  (6, 7, 'expense',  60000.00, '2025-05-02', 'Rent'),
  (7, 5, 'expense',   4500.00, '2025-05-06', 'Weekly grocery');

-- ---------- Transfers (use stored proc — atomic) ----------
CALL sp_record_transfer(1, 2, 5000.00,  '2025-05-06', 'Top up JazzCash');
CALL sp_record_transfer(1, 3, 2000.00,  '2025-05-09', 'Withdraw cash');
CALL sp_record_transfer(6, 7, 3000.00,  '2025-05-04', 'Top up EasyPaisa');

-- ---------- Budgets ----------
INSERT INTO budgets (user_id, category_id, month_year, limit_amount) VALUES
  (1, 5, '2025-05-01',  10000.00),   -- Food
  (1, 6, '2025-05-01',   5000.00),   -- Transport
  (1, 9, '2025-05-01',   4000.00),   -- Entertainment
  (1, 7, '2025-05-01',  40000.00),   -- Rent
  (2, 5, '2025-05-01',  15000.00);

-- ---------- Goals & contributions ----------
INSERT INTO goals (user_id, goal_name, target_amount, target_date) VALUES
  (1, 'Custom TT Racket', 15000.00,  '2025-08-01'),
  (1, 'New GPU',          80000.00,  '2025-12-01'),
  (1, 'Emergency Fund',  200000.00,  '2026-06-01'),
  (2, 'Hajj Savings',    600000.00,  '2027-01-01');

INSERT INTO goal_contributions (goal_id, amount, contribution_date, source_account_id, note) VALUES
  (1,  5000.00, '2025-05-10', 1, 'First chunk'),
  (1,  3000.00, '2025-05-20', 2, 'Side income'),
  (2, 20000.00, '2025-05-15', 1, 'Saved from freelance'),
  (3, 15000.00, '2025-05-15', 1, 'Monthly auto-save'),
  (4, 25000.00, '2025-05-12', 6, 'Monthly contribution');

-- ---------- Investments ----------
INSERT INTO investments (user_id, inv_type_id, asset_name, symbol, quantity, buy_price, currency_code, buy_date) VALUES
  (1, 1, 'Apple Inc.',          'AAPL',  10,        180.50,  'USD', '2024-11-15'),
  (1, 2, 'Bitcoin',             'BTC',    0.05,   42000.00,  'USD', '2024-09-01'),
  (1, 2, 'Ethereum',            'ETH',    0.80,    2200.00,  'USD', '2025-01-10'),
  (1, 3, '24K Gold',            'XAU',   20.00,   23500.00,  'PKR', '2024-12-20'),
  (2, 1, 'Engro Corp',          'ENGRO', 50,        285.00,  'PKR', '2025-02-01'),
  (2, 3, '24K Gold',            'XAU',   10.00,   24000.00,  'PKR', '2025-03-05');

-- ---------- Asset prices (admin feed) ----------
INSERT INTO asset_prices (inv_type_id, symbol, price, currency_code, price_date) VALUES
  (1, 'AAPL',   210.00, 'USD', '2025-04-30'),
  (1, 'AAPL',   215.50, 'USD', '2025-05-10'),
  (1, 'ENGRO',  320.00, 'PKR', '2025-05-10'),
  (2, 'BTC',  62000.00, 'USD', '2025-05-10'),
  (2, 'ETH',   2900.00, 'USD', '2025-05-10'),
  (3, 'XAU',  26500.00, 'PKR', '2025-05-10');
