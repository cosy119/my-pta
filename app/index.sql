-- 索引：**必须在迁移之后执行**
--
-- 为什么单独一个文件：老库的 mastery 没有 user_id、submissions 没有 user_id，
-- 直接建索引会报 `no such column`。init_db 的顺序是
--   executescript(schema.sql) → _migrate() → executescript(index.sql)
-- 全部 IF NOT EXISTS，可重复执行。

CREATE INDEX IF NOT EXISTS idx_users_token ON users(token);

CREATE INDEX IF NOT EXISTS idx_tc_problem ON testcases(problem_id, ord);

CREATE INDEX IF NOT EXISTS idx_sub_problem ON submissions(problem_id, created_at);
CREATE INDEX IF NOT EXISTS idx_sub_user ON submissions(user_id, problem_id, created_at);

CREATE INDEX IF NOT EXISTS idx_sc_sub ON submission_cases(submission_id, ord);

CREATE INDEX IF NOT EXISTS idx_mastery_user ON mastery(user_id);
