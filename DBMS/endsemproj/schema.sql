DROP DATABASE IF EXISTS finance_tracker;
CREATE DATABASE finance_tracker
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;
USE finance_tracker;

-- 1. USERS — every person with an account in the system
CREATE TABLE users (
    user_id        INT          NOT NULL AUTO_INCREMENT,
    full_name      VARCHAR(100) NOT NULL,
    email          VARCHAR(150) NOT NULL,
    password_hash  CHAR(60)     NOT NULL,                  -- bcrypt
    role           ENUM('user','admin','auditor') NOT NULL DEFAULT 'user',
    joined_at      DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active      BOOLEAN      NOT NULL DEFAULT TRUE,
    PRIMARY KEY (user_id),
    UNIQUE KEY uq_users_email (email),
    CHECK (email LIKE '%@%.%')
) ENGINE=InnoDB;

-- 2. CURRENCIES + EXCHANGE RATES
CREATE TABLE currencies (
    currency_code VARCHAR(10)     NOT NULL,    -- ticker (PKR, USD, USDT, ...)
    currency_name VARCHAR(50) NOT NULL,
    symbol        VARCHAR(5)  NOT NULL,
    PRIMARY KEY (currency_code)
) ENGINE=InnoDB;

CREATE TABLE exchange_rates (
    rate_id        INT          NOT NULL AUTO_INCREMENT,
    from_currency  VARCHAR(10)      NOT NULL,
    to_currency    VARCHAR(10)      NOT NULL,
    rate           DECIMAL(18,8) NOT NULL,
    effective_date DATE         NOT NULL,
    PRIMARY KEY (rate_id),
    UNIQUE KEY uq_rate (from_currency, to_currency, effective_date),
    FOREIGN KEY (from_currency) REFERENCES currencies(currency_code),
    FOREIGN KEY (to_currency)   REFERENCES currencies(currency_code),
    CHECK (rate > 0),
    CHECK (from_currency <> to_currency)
) ENGINE=InnoDB;

CREATE INDEX idx_rate_lookup ON exchange_rates (from_currency, to_currency, effective_date DESC);

-- 3. ACCOUNT TYPES + ACCOUNTS
CREATE TABLE account_types (
    type_id   INT         NOT NULL AUTO_INCREMENT,
    type_name VARCHAR(40) NOT NULL,
    PRIMARY KEY (type_id),
    UNIQUE KEY uq_type_name (type_name)
) ENGINE=InnoDB;

CREATE TABLE accounts (
    account_id     INT           NOT NULL AUTO_INCREMENT,
    user_id        INT           NOT NULL,
    account_name   VARCHAR(80)   NOT NULL,
    type_id        INT           NOT NULL,
    currency_code  VARCHAR(10)       NOT NULL,
    balance        DECIMAL(18,2) NOT NULL DEFAULT 0.00,    -- maintained by trigger
    created_at     DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active      BOOLEAN       NOT NULL DEFAULT TRUE,
    PRIMARY KEY (account_id),
    UNIQUE KEY uq_user_account (user_id, account_name),
    FOREIGN KEY (user_id)       REFERENCES users(user_id)            ON DELETE CASCADE,
    FOREIGN KEY (type_id)       REFERENCES account_types(type_id),
    FOREIGN KEY (currency_code) REFERENCES currencies(currency_code)
) ENGINE=InnoDB;

CREATE INDEX idx_accounts_user ON accounts (user_id);

-- 4. CATEGORIES — global taxonomy (system-managed)
CREATE TABLE categories (
    category_id   INT          NOT NULL AUTO_INCREMENT,
    category_name VARCHAR(50)  NOT NULL,
    kind          ENUM('income','expense') NOT NULL,
    is_system     BOOLEAN      NOT NULL DEFAULT TRUE,
    PRIMARY KEY (category_id),
    UNIQUE KEY uq_cat (category_name, kind)
) ENGINE=InnoDB;

-- 5. TRANSACTIONS 
-- Transfers are modelled as TWO linked rows (transfer_out + transfer_in) sharing a linked_txn_id, giving us double-entry semantics for transfers while keeping income/expense as simple single rows.
CREATE TABLE transactions (
    txn_id         BIGINT        NOT NULL AUTO_INCREMENT,
    account_id     INT           NOT NULL,
    category_id    INT           NULL,                   -- NULL for transfers
    txn_type       ENUM('income','expense','transfer_in','transfer_out') NOT NULL,
    amount         DECIMAL(18,2) NOT NULL,
    txn_date       DATE          NOT NULL,
    description    VARCHAR(255)  NULL,
    linked_txn_id  BIGINT        NULL,                   -- self-FK for transfer pair
    created_at     DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (txn_id),
    FOREIGN KEY (account_id)    REFERENCES accounts(account_id)   ON DELETE CASCADE,
    FOREIGN KEY (category_id)   REFERENCES categories(category_id),
    FOREIGN KEY (linked_txn_id) REFERENCES transactions(txn_id)   ON DELETE SET NULL,
    CHECK (amount > 0),
    CHECK (
        (txn_type IN ('income','expense') AND category_id IS NOT NULL)
     OR (txn_type IN ('transfer_in','transfer_out') AND category_id IS NULL)
    )
) ENGINE=InnoDB;

CREATE INDEX idx_txn_account_date ON transactions (account_id, txn_date);
CREATE INDEX idx_txn_category     ON transactions (category_id);
CREATE INDEX idx_txn_date         ON transactions (txn_date);

-- 6. BUDGETS — one cap per (user, category, month)
CREATE TABLE budgets (
    budget_id     INT           NOT NULL AUTO_INCREMENT,
    user_id       INT           NOT NULL,
    category_id   INT           NOT NULL,
    month_year    DATE          NOT NULL,                -- always store first of month
    limit_amount  DECIMAL(18,2) NOT NULL,
    currency_code VARCHAR(10)       NOT NULL DEFAULT 'PKR',
    PRIMARY KEY (budget_id),
    UNIQUE KEY uq_budget (user_id, category_id, month_year),
    FOREIGN KEY (user_id)       REFERENCES users(user_id)         ON DELETE CASCADE,
    FOREIGN KEY (category_id)   REFERENCES categories(category_id),
    FOREIGN KEY (currency_code) REFERENCES currencies(currency_code),
    CHECK (limit_amount > 0),
    CHECK (DAY(month_year) = 1)
) ENGINE=InnoDB;

-- 7. GOALS + CONTRIBUTIONS
CREATE TABLE goals (
    goal_id       INT           NOT NULL AUTO_INCREMENT,
    user_id       INT           NOT NULL,
    goal_name     VARCHAR(100)  NOT NULL,
    target_amount DECIMAL(18,2) NOT NULL,
    currency_code VARCHAR(10)       NOT NULL DEFAULT 'PKR',
    target_date   DATE          NULL,
    status        ENUM('active','achieved','cancelled') NOT NULL DEFAULT 'active',
    created_at    DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (goal_id),
    UNIQUE KEY uq_user_goal (user_id, goal_name),
    FOREIGN KEY (user_id)       REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (currency_code) REFERENCES currencies(currency_code),
    CHECK (target_amount > 0)
) ENGINE=InnoDB;

CREATE TABLE goal_contributions (
    contribution_id   INT           NOT NULL AUTO_INCREMENT,
    goal_id           INT           NOT NULL,
    amount            DECIMAL(18,2) NOT NULL,
    contribution_date DATE          NOT NULL,
    source_account_id INT           NULL,                -- traceable to an account
    note              VARCHAR(255)  NULL,
    PRIMARY KEY (contribution_id),
    FOREIGN KEY (goal_id)           REFERENCES goals(goal_id) ON DELETE CASCADE,
    FOREIGN KEY (source_account_id) REFERENCES accounts(account_id) ON DELETE SET NULL,
    CHECK (amount > 0)
) ENGINE=InnoDB;

CREATE INDEX idx_contrib_goal ON goal_contributions (goal_id);

-- 8. INVESTMENTS — what the user owns
-- current_price is NOT stored here. It lives in asset_prices, otherwise it'd be a 3nf violation
CREATE TABLE investment_types (
    inv_type_id INT         NOT NULL AUTO_INCREMENT,
    type_name   VARCHAR(40) NOT NULL,                    -- Stock, Crypto, Gold, Bond
    unit_label  VARCHAR(20) NOT NULL,                    -- shares, coins, grams
    PRIMARY KEY (inv_type_id),
    UNIQUE KEY uq_inv_type (type_name)
) ENGINE=InnoDB;

CREATE TABLE investments (
    investment_id INT           NOT NULL AUTO_INCREMENT,
    user_id       INT           NOT NULL,
    inv_type_id   INT           NOT NULL,
    asset_name    VARCHAR(80)   NOT NULL,                -- "Apple Inc.", "Bitcoin", "24K Gold"
    symbol        VARCHAR(20)   NOT NULL,                -- AAPL, BTC, XAU
    quantity      DECIMAL(18,8) NOT NULL,
    buy_price     DECIMAL(18,4) NOT NULL,                -- per unit, in currency_code
    currency_code VARCHAR(10)       NOT NULL,
    buy_date      DATE          NOT NULL,
    PRIMARY KEY (investment_id),
    FOREIGN KEY (user_id)       REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (inv_type_id)   REFERENCES investment_types(inv_type_id),
    FOREIGN KEY (currency_code) REFERENCES currencies(currency_code),
    CHECK (quantity  > 0),
    CHECK (buy_price > 0)
) ENGINE=InnoDB;

CREATE INDEX idx_investments_user ON investments (user_id);

CREATE TABLE asset_prices (
    price_id      INT           NOT NULL AUTO_INCREMENT,
    inv_type_id   INT           NOT NULL,
    symbol        VARCHAR(20)   NOT NULL,
    price         DECIMAL(18,4) NOT NULL,
    currency_code VARCHAR(10)       NOT NULL,
    price_date    DATE          NOT NULL,
    PRIMARY KEY (price_id),
    UNIQUE KEY uq_price (inv_type_id, symbol, price_date),
    FOREIGN KEY (inv_type_id)   REFERENCES investment_types(inv_type_id),
    FOREIGN KEY (currency_code) REFERENCES currencies(currency_code),
    CHECK (price > 0)
) ENGINE=InnoDB;

CREATE INDEX idx_price_lookup ON asset_prices (inv_type_id, symbol, price_date DESC);

-- TRIGGERS — keep accounts.balance consistent with transactions
-- (Justification: balance is denormalised for read performance. The trigger is the integrity contract that makes the denormalisation safe.)

DELIMITER $$

CREATE TRIGGER trg_txn_after_insert
AFTER INSERT ON transactions
FOR EACH ROW
BEGIN
    IF NEW.txn_type IN ('income','transfer_in') THEN
        UPDATE accounts SET balance = balance + NEW.amount WHERE account_id = NEW.account_id;
    ELSE
        UPDATE accounts SET balance = balance - NEW.amount WHERE account_id = NEW.account_id;
    END IF;
END$$

CREATE TRIGGER trg_txn_after_delete
AFTER DELETE ON transactions
FOR EACH ROW
BEGIN
    IF OLD.txn_type IN ('income','transfer_in') THEN
        UPDATE accounts SET balance = balance - OLD.amount WHERE account_id = OLD.account_id;
    ELSE
        UPDATE accounts SET balance = balance + OLD.amount WHERE account_id = OLD.account_id;
    END IF;
END$$

-- STORED PROCEDURE — atomic transfer between two accounts.
CREATE PROCEDURE sp_record_transfer (
    IN p_from_account INT,
    IN p_to_account   INT,
    IN p_amount       DECIMAL(18,2),
    IN p_date         DATE,
    IN p_note         VARCHAR(255)
)
BEGIN
    DECLARE v_out_id BIGINT;
    DECLARE v_in_id  BIGINT;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    INSERT INTO transactions (account_id, category_id, txn_type, amount, txn_date, description)
    VALUES (p_from_account, NULL, 'transfer_out', p_amount, p_date, p_note);
    SET v_out_id = LAST_INSERT_ID();

    INSERT INTO transactions (account_id, category_id, txn_type, amount, txn_date, description, linked_txn_id)
    VALUES (p_to_account,   NULL, 'transfer_in',  p_amount, p_date, p_note, v_out_id);
    SET v_in_id = LAST_INSERT_ID();

    UPDATE transactions SET linked_txn_id = v_in_id WHERE txn_id = v_out_id;

    COMMIT;
END$$

DELIMITER ;

-- VIEWS — cleanly expose computed reports

-- Most recent exchange rate per currency pair
CREATE OR REPLACE VIEW v_latest_rates AS
SELECT er.from_currency, er.to_currency, er.rate
FROM exchange_rates er
JOIN (
    SELECT from_currency, to_currency, MAX(effective_date) AS d
    FROM exchange_rates
    GROUP BY from_currency, to_currency
) latest
  ON er.from_currency = latest.from_currency
 AND er.to_currency   = latest.to_currency
 AND er.effective_date = latest.d;

-- Account balances normalised to PKR
CREATE OR REPLACE VIEW v_account_balances_pkr AS
SELECT a.user_id,
       a.account_id,
       a.account_name,
       a.balance,
       a.currency_code,
       CASE WHEN a.currency_code = 'PKR' THEN a.balance
            ELSE a.balance * COALESCE(r.rate, 0)
       END AS balance_pkr
FROM accounts a
LEFT JOIN v_latest_rates r
       ON r.from_currency = a.currency_code
      AND r.to_currency   = 'PKR';

-- Net worth per user (cash + investments at latest market price)
CREATE OR REPLACE VIEW v_net_worth AS
SELECT u.user_id,
       u.full_name,
       COALESCE(cash.cash_pkr, 0)         AS cash_pkr,
       COALESCE(inv.invest_pkr, 0)        AS investments_pkr,
       COALESCE(cash.cash_pkr, 0) + COALESCE(inv.invest_pkr, 0) AS net_worth_pkr
FROM users u
LEFT JOIN (
    SELECT user_id, SUM(balance_pkr) AS cash_pkr
    FROM v_account_balances_pkr
    GROUP BY user_id
) cash ON cash.user_id = u.user_id
LEFT JOIN (
    SELECT i.user_id,
           SUM( i.quantity * COALESCE(p.price, i.buy_price)
                * CASE WHEN i.currency_code='PKR' THEN 1 ELSE COALESCE(r.rate, 0) END
              ) AS invest_pkr
    FROM investments i
    LEFT JOIN (
        SELECT ap.inv_type_id, ap.symbol, ap.price
        FROM asset_prices ap
        JOIN (
            SELECT inv_type_id, symbol, MAX(price_date) AS d
            FROM asset_prices GROUP BY inv_type_id, symbol
        ) latest
          ON ap.inv_type_id = latest.inv_type_id
         AND ap.symbol      = latest.symbol
         AND ap.price_date  = latest.d
    ) p ON p.inv_type_id = i.inv_type_id AND p.symbol = i.symbol
    LEFT JOIN v_latest_rates r
           ON r.from_currency = i.currency_code AND r.to_currency = 'PKR'
    GROUP BY i.user_id
) inv ON inv.user_id = u.user_id;

-- Budget vs actual spending per (user, category, month)
CREATE OR REPLACE VIEW v_budget_status AS
SELECT b.user_id,
       b.category_id,
       c.category_name,
       b.month_year,
       b.limit_amount,
       COALESCE(spent.spent, 0)                         AS actual_spent,
       b.limit_amount - COALESCE(spent.spent, 0)        AS remaining,
       ROUND(COALESCE(spent.spent, 0) / b.limit_amount * 100, 2) AS pct_used
FROM budgets b
JOIN categories c ON c.category_id = b.category_id
LEFT JOIN (
    SELECT a.user_id,
           t.category_id,
           DATE_FORMAT(t.txn_date, '%Y-%m-01') AS month_year,
           SUM(t.amount) AS spent
    FROM transactions t
    JOIN accounts a ON a.account_id = t.account_id
    WHERE t.txn_type = 'expense'
    GROUP BY a.user_id, t.category_id, DATE_FORMAT(t.txn_date, '%Y-%m-01')
) spent
  ON spent.user_id     = b.user_id
 AND spent.category_id = b.category_id
 AND spent.month_year  = b.month_year;

-- Goal progress
CREATE OR REPLACE VIEW v_goal_progress AS
SELECT g.goal_id,
       g.user_id,
       g.goal_name,
       g.target_amount,
       COALESCE(SUM(gc.amount), 0)                                            AS contributed,
       ROUND(COALESCE(SUM(gc.amount),0) / g.target_amount * 100, 2)           AS pct_complete,
       g.status
FROM goals g
LEFT JOIN goal_contributions gc ON gc.goal_id = g.goal_id
GROUP BY g.goal_id, g.user_id, g.goal_name, g.target_amount, g.status;

-- Portfolio with gain/loss & ROI
CREATE OR REPLACE VIEW v_portfolio AS
SELECT i.investment_id,
       i.user_id,
       it.type_name,
       i.asset_name,
       i.symbol,
       i.quantity,
       i.buy_price,
       COALESCE(p.price, i.buy_price)                                    AS current_price,
       i.currency_code,
       (i.quantity * i.buy_price)                                        AS cost_basis,
       (i.quantity * COALESCE(p.price, i.buy_price))                     AS market_value,
       (i.quantity * (COALESCE(p.price, i.buy_price) - i.buy_price))     AS gain_loss,
       ROUND( (COALESCE(p.price, i.buy_price) - i.buy_price)
              / i.buy_price * 100, 2)                                    AS roi_pct
FROM investments i
JOIN investment_types it ON it.inv_type_id = i.inv_type_id
LEFT JOIN (
    SELECT ap.inv_type_id, ap.symbol, ap.price
    FROM asset_prices ap
    JOIN (
        SELECT inv_type_id, symbol, MAX(price_date) AS d
        FROM asset_prices GROUP BY inv_type_id, symbol
    ) latest
      ON ap.inv_type_id = latest.inv_type_id
     AND ap.symbol      = latest.symbol
     AND ap.price_date  = latest.d
) p ON p.inv_type_id = i.inv_type_id AND p.symbol = i.symbol;
