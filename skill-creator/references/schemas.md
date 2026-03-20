# JSON 模式

本文档定义了 skill-creator 使用的 JSON 模式。

---

## evals.json

定义技能的评估。位于技能目录内的 `evals/evals.json`。

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "用户示例提示",
      "expected_output": "预期结果描述",
      "files": ["evals/files/sample1.pdf"],
      "expectations": [
        "输出包含X",
        "技能使用了脚本Y"
      ]
    }
  ]
}
```

**字段：**
- `skill_name`: 与技能 frontmatter 匹配的名称
- `evals[].id`: 唯一整数标识符
- `evals[].prompt`: 要执行的任务
- `evals[].expected_output`: 成功的人类可读描述
- `evals[].files`: 输入文件路径的可选列表（相对于技能根目录）
- `evals[].expectations`: 可验证语句的列表

---

## history.json

跟踪改进模式中的版本进展。位于工作区根目录。

```json
{
  "started_at": "2026-01-15T10:30:00Z",
  "skill_name": "pdf",
  "current_best": "v2",
  "iterations": [
    {
      "version": "v0",
      "parent": null,
      "expectation_pass_rate": 0.65,
      "grading_result": "baseline",
      "is_current_best": false
    },
    {
      "version": "v1",
      "parent": "v0",
      "expectation_pass_rate": 0.75,
      "grading_result": "won",
      "is_current_best": false
    },
    {
      "version": "v2",
      "parent": "v1",
      "expectation_pass_rate": 0.85,
      "grading_result": "won",
      "is_current_best": true
    }
  ]
}
```

**字段：**
- `started_at`: 改进开始的ISO时间戳
- `skill_name`: 正在改进的技能名称
- `current_best`: 最佳表现版本的标识符
- `iterations[].version`: 版本标识符（v0、v1、...）
- `iterations[].parent`: 派生此版本的父版本
- `iterations[].expectation_pass_rate`: 来自评分的通过率
- `iterations[].grading_result`: "baseline"、"won"、"lost" 或 "tie"
- `iterations[].is_current_best`: 是否为当前最佳版本

---

## grading.json

评分代理的输出。位于 `<run-dir>/grading.json`。

```json
{
  "expectations": [
    {
      "text": "输出包含名称'John Smith'",
      "passed": true,
      "evidence": "在记录第3步中找到：'提取的名称：John Smith, Sarah Johnson'"
    },
    {
      "text": "电子表格在单元格B10中有SUM公式",
      "passed": false,
      "evidence": "未创建电子表格。输出是文本文件。"
    }
  ],
  "summary": {
    "passed": 2,
    "failed": 1,
    "total": 3,
    "pass_rate": 0.67
  },
  "execution_metrics": {
    "tool_calls": {
      "Read": 5,
      "Write": 2,
      "Bash": 8
    },
    "total_tool_calls": 15,
    "total_steps": 6,
    "errors_encountered": 0,
    "output_chars": 12450,
    "transcript_chars": 3200
  },
  "timing": {
    "executor_duration_seconds": 165.0,
    "grader_duration_seconds": 26.0,
    "total_duration_seconds": 191.0
  },
  "claims": [
    {
      "claim": "表单有12个可填写字段",
      "type": "factual",
      "verified": true,
      "evidence": "在field_info.json中计算了12个字段"
    }
  ],
  "user_notes_summary": {
    "uncertainties": ["使用了2023年数据，可能过时"],
    "needs_review": [],
    "workarounds": ["对不可填充字段回落到文本覆盖"]
  },
  "eval_feedback": {
    "suggestions": [
      {
        "assertion": "输出包含名称'John Smith'",
        "reason": "提及名称的虚构文档也会通过"
      }
    ],
    "overall": "断言检查存在但不检查正确性。"
  }
}
```

**字段：**
- `expectations[]`: 带有证据的评分期望
- `summary`: 总计通过/失败数量
- `execution_metrics`: 工具使用和输出大小（来自执行器的 metrics.json）
- `timing`: 墙钟时间（来自 timing.json）
- `claims`: 从输出中提取和验证的声明
- `user_notes_summary`: 执行器标记的问题
- `eval_feedback`: （可选）对评估的改进建议，仅当评分器识别出值得关注的问题时存在

---

## metrics.json

执行器代理的输出。位于 `<run-dir>/outputs/metrics.json`。

```json
{
  "tool_calls": {
    "Read": 5,
    "Write": 2,
    "Bash": 8,
    "Edit": 1,
    "Glob": 2,
    "Grep": 0
  },
  "total_tool_calls": 18,
  "total_steps": 6,
  "files_created": ["filled_form.pdf", "field_values.json"],
  "errors_encountered": 0,
  "output_chars": 12450,
  "transcript_chars": 3200
}
```

**字段：**
- `tool_calls`: 每种工具类型的计数
- `total_tool_calls`: 所有工具调用的总和
- `total_steps`: 主要执行步骤的数量
- `files_created`: 创建的输出文件列表
- `errors_encountered`: 执行期间遇到的错误数
- `output_chars`: 输出文件的总字符数
- `transcript_chars`: 记录的字符数

---

## timing.json

运行的墙钟时间。位于 `<run-dir>/timing.json`。

**如何捕获：** 当子代理任务完成时，任务通知包括 `total_tokens` 和 `duration_ms`。立即保存这些数据——它们不会在其他地方持久化，事后无法恢复。

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3,
  "executor_start": "2026-01-15T10:30:00Z",
  "executor_end": "2026-01-15T10:32:45Z",
  "executor_duration_seconds": 165.0,
  "grader_start": "2026-01-15T10:32:46Z",
  "grader_end": "2026-01-15T10:33:12Z",
  "grader_duration_seconds": 26.0
}
```

---

## benchmark.json

基准模式的输出。位于 `benchmarks/<timestamp>/benchmark.json`。

```json
{
  "metadata": {
    "skill_name": "pdf",
    "skill_path": "/path/to/pdf",
    "executor_model": "claude-sonnet-4-20250514",
    "analyzer_model": "most-capable-model",
    "timestamp": "2026-01-15T10:30:00Z",
    "evals_run": [1, 2, 3],
    "runs_per_configuration": 3
  },

  "runs": [
    {
      "eval_id": 1,
      "eval_name": "Ocean",
      "configuration": "with_skill",
      "run_number": 1,
      "result": {
        "pass_rate": 0.85,
        "passed": 6,
        "failed": 1,
        "total": 7,
        "time_seconds": 42.5,
        "tokens": 3800,
        "tool_calls": 18,
        "errors": 0
      },
      "expectations": [
        {"text": "...", "passed": true, "evidence": "..."}
      ],
      "notes": [
        "使用了2023年数据，可能过时",
        "对不可填充字段回落到文本覆盖"
      ]
    }
  ],

  "run_summary": {
    "with_skill": {
      "pass_rate": {"mean": 0.85, "stddev": 0.05, "min": 0.80, "max": 0.90},
      "time_seconds": {"mean": 45.0, "stddev": 12.0, "min": 32.0, "max": 58.0},
      "tokens": {"mean": 3800, "stddev": 400, "min": 3200, "max": 4100}
    },
    "without_skill": {
      "pass_rate": {"mean": 0.35, "stddev": 0.08, "min": 0.28, "max": 0.45},
      "time_seconds": {"mean": 32.0, "stddev": 8.0, "min": 24.0, "max": 42.0},
      "tokens": {"mean": 2100, "stddev": 300, "min": 1800, "max": 2500}
    },
    "delta": {
      "pass_rate": "+0.50",
      "time_seconds": "+13.0",
      "tokens": "+1700"
    }
  },

  "notes": [
    "断言'输出是PDF文件'在两种配置中都100%通过 - 可能不会区分技能价值",
    "评估3显示高方差（50% ± 40%）- 可能不稳定或模型依赖",
    "无技能运行在表提取期望上始终失败",
    "技能增加13秒平均执行时间但提高50%通过率"
  ]
}
```

**字段：**
- `metadata`: 关于基准运行的信息
  - `skill_name`: 技能名称
  - `timestamp`: 运行基准的时间
  - `evals_run`: 评估名称或ID列表
  - `runs_per_configuration`: 每种配置的运行次数（例如3）
- `runs[]`: 单独运行结果
  - `eval_id`: 数字评估标识符
  - `eval_name`: 人类可读的评估名称（在查看器中用作节标题）
  - `configuration`: 必须是 `"with_skill"` 或 `"without_skill"`（查看器使用此精确字符串进行分组和颜色编码）
  - `run_number`: 整数运行编号（1、2、3...）
  - `result`: 包含 `pass_rate`、`passed`、`total`、`time_seconds`、`tokens`、`errors` 的嵌套对象
- `run_summary`: 每种配置的统计聚合
  - `with_skill` / `without_skill`: 每个包含 `pass_rate`、`time_seconds`、`tokens` 对象，带有 `mean` 和 `stddev` 字段
  - `delta`: 差异字符串如 `"+0.50"`、`"+13.0"`、`"+1700"`
- `notes`: 来自分析器的自由格式观察

**重要：** 查看器精确读取这些字段名。使用 `config` 而不是 `configuration`，或将 `pass_rate` 放在运行的顶级而不是嵌套在 `result` 下，会导致查看器显示空值/零值。手动生成 benchmark.json 时始终参考此模式。

---

## comparison.json

盲比较器的输出。位于 `<grading-dir>/comparison-N.json`。

```json
{
  "winner": "A",
  "reasoning": "输出A提供了完整的解决方案，格式正确，包含所有必需字段。输出B缺少日期字段，格式不一致。",
  "rubric": {
    "A": {
      "content": {
        "correctness": 5,
        "completeness": 5,
        "accuracy": 4
      },
      "structure": {
        "organization": 4,
        "formatting": 5,
        "usability": 4
      },
      "content_score": 4.7,
      "structure_score": 4.3,
      "overall_score": 9.0
    },
    "B": {
      "content": {
        "correctness": 3,
        "completeness": 2,
        "accuracy": 3
      },
      "structure": {
        "organization": 3,
        "formatting": 2,
        "usability": 3
      },
      "content_score": 2.7,
      "structure_score": 2.7,
      "overall_score": 5.4
    }
  },
  "output_quality": {
    "A": {
      "score": 9,
      "strengths": ["完整解决方案", "格式良好", "所有字段都存在"],
      "weaknesses": ["标题中的小样式不一致"]
    },
    "B": {
      "score": 5,
      "strengths": ["可读输出", "正确的基本结构"],
      "weaknesses": ["缺少日期字段", "格式不一致", "部分数据提取"]
    }
  },
  "expectation_results": {
    "A": {
      "passed": 4,
      "total": 5,
      "pass_rate": 0.80,
      "details": [
        {"text": "输出包含名称", "passed": true}
      ]
    },
    "B": {
      "passed": 3,
      "total": 5,
      "pass_rate": 0.60,
      "details": [
        {"text": "输出包含名称", "passed": true}
      ]
    }
  }
}
```

---

## analysis.json

事后分析器的输出。位于 `<grading-dir>/analysis.json`。

```json
{
  "comparison_summary": {
    "winner": "A",
    "winner_skill": "path/to/winner/skill",
    "loser_skill": "path/to/loser/skill",
    "comparator_reasoning": "比较器选择赢家原因的简要总结"
  },
  "winner_strengths": [
    "处理多页文档的清晰逐步说明",
    "包含捕获格式错误的验证脚本"
  ],
  "loser_weaknesses": [
    "模糊说明'适当处理文档'导致不一致的行为",
    "没有验证脚本，代理不得不即兴发挥"
  ],
  "instruction_following": {
    "winner": {
      "score": 9,
      "issues": ["小问题：跳过了可选的日志步骤"]
    },
    "loser": {
      "score": 6,
      "issues": [
        "未使用技能的格式模板",
        "创造了自己的方法而不是遵循第3步"
      ]
    }
  },
  "improvement_suggestions": [
    {
      "priority": "high",
      "category": "instructions",
      "suggestion": "将'适当处理文档'替换为明确步骤",
      "expected_impact": "将消除导致不一致行为的歧义"
    }
  ],
  "transcript_insights": {
    "winner_execution_pattern": "阅读技能 -> 遵循5步流程 -> 使用验证脚本",
    "loser_execution_pattern": "阅读技能 -> 对方法不确定 -> 尝试3种不同方法"
  }
}
```
