#!/usr/bin/env python3
"""
commit-code 技能主入口点
"""

import os
import sys
from pathlib import Path

def main():
    """主入口函数"""
    # 获取技能目录
    skill_dir = Path(__file__).parent

    # 优先使用增强版提交脚本
    enhanced_script = skill_dir / "enhanced_commit.py"

    if enhanced_script.exists():
        # 导入并运行增强版功能
        import importlib.util
        spec = importlib.util.spec_from_file_location("enhanced_commit", enhanced_script)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # 调用主函数
        module.main()
    else:
        # 如果增强版不存在，回退到基础版
        basic_script = skill_dir / "commit.py"
        if basic_script.exists():
            import importlib.util
            spec = importlib.util.spec_from_file_location("commit", basic_script)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # 调用主函数
            module.main()
        else:
            print("❌ 错误: 未找到提交脚本")
            sys.exit(1)

if __name__ == "__main__":
    main()