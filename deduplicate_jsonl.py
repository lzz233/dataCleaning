import json
import re


def filter_java_entries(input_path, output_path):
    """
    读取 input_path 指定的 JSONL 文件（每行一个JSON对象），
    剔除所有包含 C++, Python, HTML 等关键字的记录，只保留包含 'java' 的记录，
    并将结果写入 output_path（同样为JSONL格式）。
    """
    # 构造排除关键字的正则表达式
    exclude_pattern = re.compile(
        r'(?<![A-Za-z0-9])'
        r'(C\+\+|Python|HTML|JavaScript|Kotlin|Go|Scala|'
        r'Ruby|PHP|Swift|Objective-C|C|C#|SQL|Perl|MATLAB|R|Julia|'
        r'TypeScript|SwiftUI|React|Vue.js|CSS|Ionic|Xamarin|Flutter|'
        r'React Native|Node.js|Electron|TensorFlow|OpenCV|XML|'
        r'NoSQL|cURL|Rust|Language Integrated Query|shell|'
        r'PowerShell|Bash|Amazon Web Services|Apache Flink|'
        r'scikit|pandas|NumPy|SciPy|Matplotlib|Seaborn|REST|'
        r'Natural Language Processing|Machine Learning|'
        r'Deep Learning|neural network|CNN|RNN|LSTM|GRU|Keras|'
        r'PostgreSQL|MySQL|JSON|MongoDB|script|API|query|jQuery|'
        r'Docker|pseudocode|pseudo-code|DynamoDB|XPATH|Tkinter)'
        r'(?![A-Za-z0-9])',
        flags=re.IGNORECASE
    )

    # 读取并过滤JSONL文件
    with open(input_path, 'r', encoding='utf-8') as f_in, \
            open(output_path, 'w', encoding='utf-8') as f_out:

        for line in f_in:
            line = line.strip()
            if not line:
                continue

            try:
                entry = json.loads(line)
                # 检查是否包含排除关键词
                if not exclude_pattern.search(json.dumps(entry)):
                    # 写入符合条件的记录（保持JSONL格式）
                    f_out.write(json.dumps(entry, ensure_ascii=False) + '\n')
            except json.JSONDecodeError as e:
                print(f"跳过无效行（解析失败）: {line[:50]}... 错误: {e}")


if __name__ == '__main__':
    input_path  = 'code_alpaca.jsonl'
    output_path = 'final-code_alpaca.jsonl'

    filter_java_entries(input_path, output_path)
    print(f"过滤完成，结果已保存至：{output_path}")