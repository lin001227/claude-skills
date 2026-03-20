#!/usr/bin/env python3
"""
commit-code 技能的文件类型检测模块
提供高级的文件类型和分类功能
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import mimetypes


class FileTypeDetector:
    """
    高级文件类型检测器
    """

    # 编程语言映射
    LANGUAGE_MAP = {
        # Web 开发
        '.js': 'javascript',
        '.jsx': 'javascript',
        '.ts': 'typescript',
        '.tsx': 'typescript',
        '.html': 'html',
        '.htm': 'html',
        '.css': 'css',
        '.scss': 'scss',
        '.sass': 'sass',
        '.less': 'less',
        '.vue': 'vue',
        '.svelte': 'svelte',
        '.astro': 'astro',

        # 后端语言
        '.py': 'python',
        '.java': 'java',
        '.scala': 'scala',
        '.kt': 'kotlin',
        '.kts': 'kotlin',
        '.go': 'go',
        '.rs': 'rust',
        '.php': 'php',
        '.rb': 'ruby',
        '.swift': 'swift',
        '.dart': 'dart',
        '.cs': 'csharp',
        '.c': 'c',
        '.cc': 'cpp',
        '.cpp': 'cpp',
        '.cxx': 'cpp',
        '.h': 'c_header',
        '.hpp': 'cpp_header',
        '.lua': 'lua',
        '.r': 'r',
        '.jl': 'julia',
        '.erl': 'erlang',
        '.ex': 'elixir',
        '.exs': 'elixir',
        '.hs': 'haskell',
        '.ml': 'ocaml',
        '.mli': 'ocaml',

        # 配置和数据
        '.json': 'json',
        '.jsonc': 'json',
        '.yaml': 'yaml',
        '.yml': 'yaml',
        '.toml': 'toml',
        '.xml': 'xml',
        '.ini': 'ini',
        '.cfg': 'config',
        '.conf': 'config',
        '.env': 'env',
        '.properties': 'properties',

        # 文档
        '.md': 'markdown',
        '.rst': 'rst',
        '.txt': 'text',
        '.asciidoc': 'asciidoc',
        '.adoc': 'asciidoc',

        # 数据格式
        '.csv': 'csv',
        '.tsv': 'tsv',
        '.sql': 'sql',
        '.graphql': 'graphql',
        '.gql': 'graphql',

        # Shell 和脚本
        '.sh': 'shell',
        '.bash': 'bash',
        '.zsh': 'shell',
        '.fish': 'shell',
        '.ps1': 'powershell',
        '.bat': 'batch',
        '.cmd': 'batch',

        # 构建工具
        '.gradle': 'gradle',
        '.pom.xml': 'maven',
        'pom.xml': 'maven',
        'build.gradle': 'gradle',
        'settings.gradle': 'gradle',
        'Cargo.toml': 'cargo',
        'Cargo.lock': 'cargo',
        'go.mod': 'gomod',
        'go.sum': 'gosum',
    }

    # 文件用途分类规则
    FILE_TYPE_RULES = [
        # 测试文件
        (r'.*\.(test|spec|e2e)\.[^.]+$', 'test'),
        (r'.*_test\.py$', 'test'),
        (r'.*_test\.rb$', 'test'),
        (r'.*_test\.go$', 'test'),
        (r'test_.*\.py$', 'test'),
        (r'test_.*\.rb$', 'test'),
        (r'test_.*\.go$', 'test'),
        (r'^test/', 'test'),

        # 配置文件
        (r'.*(config|configuration|setting).*\.(js|json|yml|yaml|toml|py)$', 'config'),
        (r'^\.env.*', 'config'),
        (r'^\..*rc$', 'config'),
        (r'.*(conf|cfg)$', 'config'),
        (r'package\.json$', 'config'),
        (r'requirements\.txt$', 'config'),
        (r'Pipfile.*', 'config'),
        (r'Gemfile.*', 'config'),
        (r'composer\.json$', 'config'),
        (r'poetry\.lock$', 'config'),
        (r'yarn\.lock$', 'config'),
        (r'package-lock\.json$', 'config'),

        # 文档文件
        (r'.*\.md$', 'documentation'),
        (r'.*\.txt$', 'documentation'),
        (r'.*(readme|README|Readme).*', 'documentation'),
        (r'.*(license|LICENSE|License).*', 'documentation'),
        (r'.*(changelog|CHANGELOG|ChangeLog).*', 'documentation'),
        (r'.*(contributing|CONTRIBUTING|Contributing).*', 'documentation'),
        (r'.*(authors|AUTHORS|Authors).*', 'documentation'),
        (r'.*(todo|TODO|Todo).*', 'documentation'),
        (r'docs?/', 'documentation'),

        # 资源文件
        (r'.*\.(jpg|jpeg|png|gif|svg|webp|bmp|ico)$', 'image'),
        (r'.*\.(mp3|wav|ogg|flac|m4a)$', 'audio'),
        (r'.*\.(mp4|avi|mov|mkv|webm)$', 'video'),
        (r'.*\.(woff|woff2|ttf|otf|eot)$', 'font'),
        (r'assets?/', 'asset'),
        (r'static/', 'asset'),
        (r'public/', 'asset'),
        (r'resources?/', 'asset'),

        # 组件/模块
        (r'src/components?/', 'component'),
        (r'src/pages?/', 'page'),
        (r'src/views?/', 'view'),
        (r'src/utils?/', 'utility'),
        (r'src/helpers?/', 'helper'),
        (r'src/lib/', 'library'),
        (r'src/services?/', 'service'),
        (r'src/models?/', 'model'),
        (r'src/stores?/', 'store'),
        (r'src/hooks?/', 'hook'),
        (r'src/api/', 'api'),
        (r'src/controllers?/', 'controller'),
        (r'src/routes?/', 'route'),
    ]

    @classmethod
    def detect_language(cls, filepath: str) -> str:
        """
        检测文件的主要编程语言
        """
        path_obj = Path(filepath)

        # 首先尝试通过扩展名匹配
        ext = path_obj.suffix.lower()
        if ext in cls.LANGUAGE_MAP:
            return cls.LANGUAGE_MAP[ext]

        # 检查整个文件名（对于没有扩展名的特殊文件）
        full_name = path_obj.name.lower()
        if full_name in cls.LANGUAGE_MAP:
            return cls.LANGUAGE_MAP[full_name]

        # 如果扩展名不明确，使用mimetypes进行猜测
        mime_type, _ = mimetypes.guess_type(filepath)
        if mime_type:
            if mime_type.startswith('text/html'):
                return 'html'
            elif mime_type.startswith('application/json'):
                return 'json'
            elif mime_type.startswith('text/'):
                return 'text'

        return 'unknown'

    @classmethod
    def classify_file_purpose(cls, filepath: str) -> str:
        """
        分类文件用途
        """
        for pattern, file_type in cls.FILE_TYPE_RULES:
            if re.match(pattern, filepath, re.IGNORECASE):
                return file_type

        # 如果没有匹配到特定规则，基于语言类型归类
        lang = cls.detect_language(filepath)

        if lang in ['javascript', 'typescript', 'python', 'java', 'go', 'rust', 'php', 'ruby']:
            return 'code'
        elif lang in ['html', 'css', 'scss', 'sass', 'less']:
            return 'markup_style'
        elif lang in ['json', 'yaml', 'xml', 'toml', 'config']:
            return 'config'
        elif lang in ['markdown', 'text', 'rst']:
            return 'documentation'
        elif lang in ['shell', 'bash']:
            return 'script'
        elif lang in ['image', 'audio', 'video', 'font']:
            return lang

        return 'other'

    @classmethod
    def get_file_metadata(cls, filepath: str) -> Dict:
        """
        获取文件的完整元数据
        """
        path_obj = Path(filepath)

        metadata = {
            'name': path_obj.name,
            'stem': path_obj.stem,
            'suffix': path_obj.suffix,
            'extension': path_obj.suffix.lower(),
            'language': cls.detect_language(filepath),
            'purpose': cls.classify_file_purpose(filepath),
            'is_new': not os.path.exists(filepath) or os.path.getsize(filepath) == 0,
            'relative_path': str(path_obj),
            'directory': str(path_obj.parent),
            'mime_type': mimetypes.guess_type(filepath)[0] or 'unknown',
        }

        return metadata

    @classmethod
    def analyze_file_changes(cls, filepath: str, change_type: str) -> Dict:
        """
        分析单个文件的更改类型
        """
        metadata = cls.get_file_metadata(filepath)

        analysis = {
            'filepath': filepath,
            'metadata': metadata,
            'change_type': change_type,  # A=Added, M=Modified, D=Deleted, R=Rename
            'is_new_file': change_type == 'A',
            'is_modified': change_type == 'M',
            'is_deleted': change_type == 'D',
            'is_renamed': change_type.startswith('R'),
        }

        # 确定文件的重要级别
        if metadata['purpose'] in ['test', 'documentation']:
            analysis['importance'] = 'low'
        elif metadata['purpose'] in ['config', 'utility']:
            analysis['importance'] = 'medium'
        else:
            analysis['importance'] = 'high'

        return analysis


def aggregate_analysis_results(analyses: List[Dict]) -> Dict:
    """
    聚合多个文件的分析结果
    """
    result = {
        'summary': {
            'total_files': len(analyses),
            'by_language': {},
            'by_purpose': {},
            'by_change_type': {},
            'by_importance': {},
        },
        'details': analyses,
        'recommendations': [],
    }

    # 统计各项指标
    for analysis in analyses:
        lang = analysis['metadata']['language']
        purpose = analysis['metadata']['purpose']
        change_type = analysis['change_type']
        importance = analysis['importance']

        result['summary']['by_language'][lang] = result['summary']['by_language'].get(lang, 0) + 1
        result['summary']['by_purpose'][purpose] = result['summary']['by_purpose'].get(purpose, 0) + 1
        result['summary']['by_change_type'][change_type] = result['summary']['by_change_type'].get(change_type, 0) + 1
        result['summary']['by_importance'][importance] = result['summary']['by_importance'].get(importance, 0) + 1

    # 生成建议
    if 'test' in result['summary']['by_purpose']:
        result['recommendations'].append("包含测试文件更新，有助于保证代码质量")

    if 'config' in result['summary']['by_purpose']:
        result['recommendations'].append("包含配置文件更新，确保环境兼容性")

    if result['summary']['by_change_type'].get('A', 0) > result['summary']['by_change_type'].get('M', 0):
        result['recommendations'].append("新增文件较多，可能是新功能实现")

    if result['summary']['by_change_type'].get('M', 0) > result['summary']['by_change_type'].get('A', 0):
        result['recommendations'].append("修改文件较多，可能是重构或优化")

    if result['summary']['by_language'].get('javascript', 0) > 0 or result['summary']['by_language'].get('typescript', 0) > 0:
        if result['summary']['by_purpose'].get('test', 0) == 0:
            result['recommendations'].append("JavaScript/TypeScript代码更新，建议添加相应测试")

    return result


def main():
    """
    主函数，用于测试文件类型检测功能
    """
    print("🔧 文件类型检测器测试")

    # 测试文件路径
    test_paths = [
        "src/components/Button.jsx",
        "src/utils/validation.js",
        "tests/unit/button.test.js",
        "docs/readme.md",
        "src/styles/main.css",
        "config/package.json",
        "public/logo.svg",
        "src/api/users.service.ts",
        ".env.production",
        "scripts/deploy.sh"
    ]

    detector = FileTypeDetector()

    print("\n📁 文件分析结果:")
    print("=" * 60)

    analyses = []
    for path in test_paths:
        analysis = detector.analyze_file_changes(path, 'M')  # 假设都是修改
        analyses.append(analysis)

        metadata = analysis['metadata']
        print(f"文件: {path}")
        print(f"  语言: {metadata['language']}")
        print(f"  用途: {metadata['purpose']}")
        print(f"  类型: {analysis['change_type']}")
        print(f"  重要性: {analysis['importance']}")
        print()

    # 聚合分析结果
    aggregated = aggregate_analysis_results(analyses)

    print("📈 聚合统计:")
    print(f"  总文件数: {aggregated['summary']['total_files']}")
    print(f"  按语言分布: {aggregated['summary']['by_language']}")
    print(f"  按用途分布: {aggregated['summary']['by_purpose']}")
    print(f"  按更改类型: {aggregated['summary']['by_change_type']}")

    print("\n💡 建议:")
    for rec in aggregated['recommendations']:
        print(f"  • {rec}")


if __name__ == "__main__":
    main()