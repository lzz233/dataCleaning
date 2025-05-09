import json
import re


def is_java_code(text):
    """Java代码检测函数
    特征包括：
    1. Java特有语法结构（带边界检测）
    2. 代码块特征（大括号+分号）
    3. 排除注释干扰
    4. 排除其他语言特征
    """

    # 预编译正则表达式（提升性能[1,3,5](@ref)）
    other_keywords = [
        r'C\+\+', r'C\#', 'SQL', 'HTML', 'JavaScript', 'Python',
        r'PHP', 'Ruby', 'Perl', 'Go', 'XML', 'Kotlin', 'Scala',
        r'Objective-C', 'JavaScript', 'Flutter', 'React', 'Vue', 'Angular',
        r'TypeScript', 'C', 'C\s*\+\s*\+', 'R', 'MATLAB', 'Julia', 'F#',
        r'Clojure', 'Haskell', 'Erlang', 'Elixir', 'ClojureScript', 'Rust',
        r'Perl6', 'Julia', 'F\#', 'COBOL', 'Fortran', 'Pascal', 'Ada',
        r'COBOL', 'Fortran', 'Pascal', 'CSS', 'SQL', 'PL/I',
    ]

    # 构建带转义和严格边界的正则
    other_pattern = re.compile(
        r'(?i)(?<!\S)(?:' + '|'.join([re.escape(kw) for kw in other_keywords]) + r')\b',
        flags=re.IGNORECASE
    )

    if other_pattern.search(text):
        return False

    other_lang_patterns = [
        r'def\s+\w+\s*\(',  # Python函数定义
        r'print\s*\(',  # Python打印
        r'#include\s+<',  # C/C++头文件
        r'using\s+System',  # C# using
        r'SELECT\s+.+\s+FROM',  # SQL查询
        r'<html>',  # HTML标签
        r'<style>',  # CSS标签
        r'\.css\s*\{'  # CSS样式
    ]

    if any(re.search(pattern, text) for pattern in other_lang_patterns):
        return False

    # Java关键字列表
    java_keywords = [
        'java', 'interface', 'Java', 'synchronized'
    ]

    # Java特有语法模式（使用正则精确匹配）
    java_patterns = [
        r'\bnew\s+\w+\s*\(',  # 对象创建
        r'\bthrows\s+\w+',  # 异常声明
        r'@Override\b',  # 注解
        r'implements\s+\w+',  # 接口实现
        r'extends\s+\w+',  # 类继承
        r'synchronized\s*\('  # 同步块
    ]

    # 条件1：检测Java特有语法结构
    pattern_matched = any(
        re.search(pattern, text)
        for pattern in java_patterns
    )

    # 条件2：检测代码块特征（排除空块和注释块）
    block_detected = (
            '{' in text and '}' in text and ';' in text and
            not re.search(r'/\*.*\*/', text)  # 排除多行注释
    )

    # 条件3：Java关键字检测（带边界检查）
    keyword_detected = any(
        re.search(rf'\b{kw}\b', text)
        for kw in java_keywords
    )

    return pattern_matched or block_detected or keyword_detected

def filter_java_from_jsonl(input_path, output_path):
    """从JSONL文件中筛选Java代码"""
    with open(input_path, 'r', encoding='utf-8') as infile, \
            open(output_path, 'w', encoding='utf-8') as outfile:

        for line in infile:
            try:
                data = json.loads(line.strip())
                # 检查instruction和output字段
                instruction_java = is_java_code(data.get("instruction", ""))
                output_java = is_java_code(data.get("output", ""))

                # 保留至少一个字段含Java代码的记录
                if instruction_java or output_java:
                    outfile.write(json.dumps(data) + '\n')
            except json.JSONDecodeError:
                continue  # 跳过无效JSON行


# 使用示例
filter_java_from_jsonl('code_alpaca.jsonl', 'code_alpaca_java_only.jsonl')