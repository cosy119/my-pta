-- 本地 AI 出题 + 批改平台 · 数据库结构
-- 全部 CREATE TABLE IF NOT EXISTS，可重复执行

PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;
PRAGMA busy_timeout = 5000;
PRAGMA foreign_keys = ON;

-- 讲义索引（供题目回链锚点）
CREATE TABLE IF NOT EXISTS lectures (
  id         INTEGER PRIMARY KEY,
  path       TEXT NOT NULL UNIQUE,
  line       TEXT DEFAULT 'python',
  title      TEXT DEFAULT '',
  sha1       TEXT DEFAULT '',
  mtime      TEXT DEFAULT '',
  scanned_at TEXT DEFAULT ''
);

-- 题目
CREATE TABLE IF NOT EXISTS problems (
  id                 INTEGER PRIMARY KEY,
  line               TEXT NOT NULL DEFAULT 'python',   -- python | cpp | shell
  title              TEXT NOT NULL,
  difficulty         INTEGER DEFAULT 2,                -- 1..5
  total_score        INTEGER DEFAULT 100,              -- 本题满分（= 各测试点分值之和）
  tags               TEXT DEFAULT '[]',                -- JSON 数组字符串
  statement_md       TEXT DEFAULT '',
  input_format       TEXT DEFAULT '',
  output_format      TEXT DEFAULT '',
  constraints_md     TEXT DEFAULT '',
  time_limit_ms      INTEGER DEFAULT 1000,
  memory_limit_mb    INTEGER DEFAULT 256,
  reference_solution TEXT DEFAULT '',
  ref_interpreter    TEXT DEFAULT 'py313',
  checker            TEXT DEFAULT 'standard',          -- standard | ignore_trailing | token | float
  float_eps          REAL DEFAULT 1e-6,
  origin             TEXT DEFAULT 'manual',            -- seed | ai | manual
  source_lecture_id  INTEGER REFERENCES lectures(id),
  source_section     TEXT DEFAULT '',
  source_anchor      TEXT DEFAULT '',
  ai_model           TEXT DEFAULT '',
  ai_meta            TEXT DEFAULT '',
  status             TEXT DEFAULT 'draft',             -- draft | verified | quarantined | published
  created_at         TEXT DEFAULT ''
);

-- 测试用例（= PTA 的「测试点」，每个测试点独立带分值）
CREATE TABLE IF NOT EXISTS testcases (
  id              INTEGER PRIMARY KEY,
  problem_id      INTEGER NOT NULL REFERENCES problems(id) ON DELETE CASCADE,
  ord             INTEGER DEFAULT 0,
  kind            TEXT DEFAULT 'manual',               -- sample | manual | ai | oracle
  stdin           TEXT DEFAULT '',
  expected_stdout TEXT DEFAULT '',
  is_sample       INTEGER DEFAULT 0,
  points          INTEGER DEFAULT 0,                   -- 本测试点分值（0 = 由题目满分均分）
  explanation     TEXT DEFAULT ''
);
CREATE INDEX IF NOT EXISTS idx_tc_problem ON testcases(problem_id, ord);

-- 提交（每次提交都留档；分数按通过的测试点分值累加）
CREATE TABLE IF NOT EXISTS submissions (
  id            INTEGER PRIMARY KEY,
  problem_id    INTEGER REFERENCES problems(id),
  lang          TEXT DEFAULT 'python',
  interpreter   TEXT DEFAULT 'py313',
  code          TEXT DEFAULT '',
  verdict       TEXT DEFAULT 'pending',
  score         INTEGER DEFAULT 0,      -- 本次实得分
  max_score     INTEGER DEFAULT 0,      -- 本次判题时的满分快照
  passed        INTEGER DEFAULT 0,
  total         INTEGER DEFAULT 0,
  time_ms       INTEGER DEFAULT 0,
  mem_kb        INTEGER DEFAULT 0,
  dual_mismatch INTEGER DEFAULT 0,
  message       TEXT DEFAULT '',
  created_at    TEXT DEFAULT '',
  judged_at     TEXT DEFAULT '',
  judge_ms      INTEGER DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_sub_problem ON submissions(problem_id, created_at);

-- 单用例明细（记下该测试点是否拿到分，便于回看「差在哪个测试点」）
CREATE TABLE IF NOT EXISTS submission_cases (
  id            INTEGER PRIMARY KEY,
  submission_id INTEGER NOT NULL REFERENCES submissions(id) ON DELETE CASCADE,
  case_id       INTEGER DEFAULT 0,
  ord           INTEGER DEFAULT 0,
  verdict       TEXT DEFAULT '',
  points        INTEGER DEFAULT 0,      -- 本测试点分值
  earned        INTEGER DEFAULT 0,      -- 实际拿到（AC 才等于 points）
  time_ms       INTEGER DEFAULT 0,
  mem_kb        INTEGER DEFAULT 0,
  stdout        TEXT DEFAULT '',
  stderr        TEXT DEFAULT '',
  expected      TEXT DEFAULT '',
  stdin         TEXT DEFAULT '',
  exit_code     INTEGER DEFAULT 0,
  detail        TEXT DEFAULT ''
);
CREATE INDEX IF NOT EXISTS idx_sc_sub ON submission_cases(submission_id, ord);

-- 掌握度 / 错题本 / 每题进度（单用户，每题一行）
CREATE TABLE IF NOT EXISTS mastery (
  problem_id         INTEGER PRIMARY KEY REFERENCES problems(id) ON DELETE CASCADE,
  attempts           INTEGER DEFAULT 0,
  ac_count           INTEGER DEFAULT 0,     -- 满分（AC）次数
  best_score         INTEGER DEFAULT 0,     -- 历史最高得分
  best_submission_id INTEGER,               -- 取得最高分的那次提交
  last_submission_id INTEGER,               -- 最后一次提交（打开题目时回填它的代码）
  last_verdict       TEXT DEFAULT '',
  last_at            TEXT DEFAULT '',
  solved_at          TEXT DEFAULT '',       -- 首次满分的时间
  is_starred         INTEGER DEFAULT 0,
  level              INTEGER DEFAULT 0,     -- 0 未掌握 1 薄弱 2 熟练
  note               TEXT DEFAULT ''
);

-- AI 配置（可多套，一条 active）
CREATE TABLE IF NOT EXISTS ai_config (
  id          INTEGER PRIMARY KEY,
  name        TEXT NOT NULL,
  base_url    TEXT NOT NULL,
  api_key     TEXT DEFAULT '',
  api_key_env TEXT DEFAULT '',
  model       TEXT NOT NULL,
  temperature REAL DEFAULT 0.3,
  is_active   INTEGER DEFAULT 0,
  extra_json  TEXT DEFAULT '',
  created_at  TEXT DEFAULT ''
);

-- AI 调用留证
CREATE TABLE IF NOT EXISTS ai_calls (
  id            INTEGER PRIMARY KEY,
  kind          TEXT DEFAULT '',        -- generate | explain | oracle | ping
  problem_id    INTEGER,
  submission_id INTEGER,
  model         TEXT DEFAULT '',
  base_url      TEXT DEFAULT '',
  tokens_in     INTEGER DEFAULT 0,
  tokens_out    INTEGER DEFAULT 0,
  req_path      TEXT DEFAULT '',
  resp_path     TEXT DEFAULT '',
  ok            INTEGER DEFAULT 0,
  err           TEXT DEFAULT '',
  created_at    TEXT DEFAULT ''
);

-- 键值设置
CREATE TABLE IF NOT EXISTS settings (
  k TEXT PRIMARY KEY,
  v TEXT
);
