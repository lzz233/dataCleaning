import json
import os
import hashlib
import chardet
from pathlib import Path

def deduplicate_json_files(input_path: str, output_dir: str = "deduplicated"):

    """
    增强版JSON/JSONL去重脚本
    改进点：
    1. 自动检测文件编码
    2. 增加编码错误容错
    3. 支持大文件流式处理
    """
    Path(output_dir).mkdir(exist_ok=True)

    def detect_encoding(file_path: str) -> str:
        with open(file_path, 'rb') as f:
            result = chardet.detect(f.read())
            # 优先返回UTF-8系列编码（解决GBK误判问题）
            return result['encoding'] if 'utf' in result['encoding'].lower() else 'utf-8'

    def hash_item(item: dict) -> str:
        """生成标准化哈希"""
        normalized = json.dumps(item, sort_keys=True, separators=(',', ':'))
        return hashlib.sha256(normalized.encode()).hexdigest()

    encoding = detect_encoding(input_path)
    seen = set()
    duplicates = []

    if input_path.endswith('.json'):
        with open(input_path, 'r', encoding=encoding) as f:  # 移除errors='replace'
            data = json.load(f)

        with open(f"{output_dir}/clean_{os.path.basename(input_path)}", 'w',
                  encoding='utf-8') as f:  # 确保输出UTF-8
            json.dump(
                [item for item in data if hash_item(item) not in seen],
                f,
                ensure_ascii=False,  # 关键参数
                indent=2
            )

    elif input_path.endswith('.jsonl'):
        with open(input_path, 'r', encoding=encoding) as infile, \
                open(f"{output_dir}/clean_{os.path.basename(input_path)}", 'w',
                     encoding='utf-8') as outfile:
            for line in infile:
                try:
                    item = json.loads(line)
                    if (item_hash := hash_item(item)) not in seen:
                        seen.add(item_hash)
                        outfile.write(json.dumps(item, ensure_ascii=False) + '\n')  # 行尾换号
                except json.JSONDecodeError:
                    continue


    # 生成报告
    report = {
        "input_file": input_path,
        "detected_encoding": encoding,
        "duplicates_count": len(duplicates),
        "sample_duplicates": duplicates[:3]
    }

    with open(f"{output_dir}/report.json", 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    deduplicate_json_files("Evol-Instruct-66k_java_only.json")  # 或 input.jsonl