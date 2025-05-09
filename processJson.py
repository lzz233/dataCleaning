import json
import re

def is_java_code(text):
    """Java代码检测函数"""
    # 防止 NoneType 传入
    if not isinstance(text, str):
        text = ""

    # 排除其他语言关键词
    other_keywords = [
        r'C\+\+', r'C\#', 'SQL', 'HTML', 'JavaScript', 'Python',
        r'PHP', 'Ruby', 'Perl', 'Go', 'XML', 'Kotlin', 'Scala',
        r'Objective-C', 'Flutter', 'React', 'Vue', 'Angular',
        r'TypeScript', 'R', 'MATLAB', 'Julia', 'F#',
        r'Clojure', 'Haskell', 'Erlang', 'Elixir', 'Rust',
        r'COBOL', 'Fortran', 'Pascal', 'Ada', 'CSS', 'PL/I'
    ]
    other_pat = re.compile(
        r'(?i)(?<!\S)(?:' + '|'.join(map(re.escape, other_keywords)) + r')\b'
    )
    if other_pat.search(text):
        return False

    # 排除常见非 Java 语言结构
    other_lang = [
        r'def\s+\w+\s*\(', r'print\s*\(', r'#include\s+<',
        r'using\s+System', r'SELECT\s+.+\s+FROM',
        r'<html>', r'<style>', r'\.css\s*\{'
    ]
    if any(re.search(p, text) for p in other_lang):
        return False

    # Java 特征模式合集 + 分数机制
    PATTERNS = {
        # 包和导入
        'package':      (re.compile(r'^\s*package\s+[\w\.]+;', re.MULTILINE), 5),
        'import':       (re.compile(r'^\s*import\s+(?:java|javax)\.[\w\.]+\*?;', re.MULTILINE), 5),
        # 类／接口／枚举定义
        'class_def':    (re.compile(
                            r'\b(?:public|private|protected)?\s*'
                            r'(?:abstract\s+|final\s+)?'
                            r'(?:class|interface|enum)\s+\w+'
                         ), 5),
        # 方法签名
        'method_def':   (re.compile(
                            r'\b(?:public|private|protected|static)\s+'
                            r'[\w\<\>\[\]]+\s+'      
                            r'\w+\s*\([^)]*\)\s*\{'
                         ), 5),
        # 注解／Javadoc
        'annotation':   (re.compile(r'@\w+'), 3),
        'javadoc':      (re.compile(r'/\*\*[\s\S]*?\*/'), 2),
        # 对象与泛型
        'generic_new':  (re.compile(r'new\s+\w+<[^>]+>\s*\('), 4),
        'new_obj':      (re.compile(r'new\s+\w+\s*\('), 2),
        # 并发与异常
        'synchronized': (re.compile(r'\bsynchronized\s*\('), 3),
        'throws':       (re.compile(r'\bthrows\s+\w+'), 2),
        # 最后兜底：块+分号
        'brace_semi':   (re.compile(r'\{[^}]*;[^}]*\}'), 1),
    }
    score = sum(pts for (pat, pts) in PATTERNS.values() if pat.search(text))
    return score >= 6


def filter_java_from_json(input_path, output_path):
    """
    从标准 JSON 数组文件中筛选出含 Java 代码的记录，
    并以 JSON 数组形式写出。
    """
    # 1) 读取整个 JSON 数组
    with open(input_path, 'r', encoding='utf-8') as f:
        records = json.load(f)

    # 2) 过滤
    java_only = []
    for rec in records:
        instr = rec.get("instruction") or ""
        outp  = rec.get("output") or ""
        if is_java_code(instr) or is_java_code(outp):
            java_only.append(rec)

    # 3) 输出为 JSON 数组
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(java_only, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    # 调用示例
    filter_java_from_json(
        "Evol-Instruct-66k.json",
        "Evol-Instruct-66k_java_only.json"
    )
