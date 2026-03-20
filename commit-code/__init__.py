#!/usr/bin/env python3
"""
commit-code 入口脚本
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """主入口函数"""
    # 获取技能目录
    skill_dir = Path(__file__).parent

    # 运行主要的提交逻辑脚本
    commit_script = skill_dir / "commit.py"

    if not commit_script.exists():
        print("❌ 错误: 未找到提交脚本")
        sys.exit(1)

    # 执行提交脚本
    try:
        result = subprocess.run([sys.executable, str(commit_script)], check=True)
        sys.exit(result.returncode)
    except subprocess.CalledProcessError as e:
        print(f"❌ 脚本执行失败: {e}")
        sys.exit(e.returncode)
    except KeyboardInterrupt:
        print("\n⚠️  用户中断操作")
        sys.exit(1)

if __name__ == "__main__":
    main()