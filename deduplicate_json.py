import json
import re

def filter_java_entries(input_path, output_path):
    """
    读取 input_path 指定的 JSON 文件（假设包含一个 JSON 数组），
    剔除所有包含 C++, Python, HTML 等关键字的记录，只保留包含 'java' 的记录，
    并将结果写入 output_path。
    """

    # 1. 构造排除关键字的正则表达式，忽略大小写
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

    # 3. 读取原始数据
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)  # 假设文件顶层是数组 :contentReference[oaicite:2]{index=2}

    # 4. 过滤：只保留符合 include_pattern 且不匹配 exclude_pattern 的记录
    filtered = [
        entry for entry in data
        if not exclude_pattern.search(json.dumps(entry))
    ]  # 使用 json.dumps 将整个对象序列化为字符串后检索关键字 :contentReference[oaicite:3]{index=3}

    # 5. 将结果写回新文件
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(filtered, f, ensure_ascii=False, indent=2)  # 美化缩进输出 :contentReference[oaicite:4]{index=4}

if __name__ == '__main__':
    # 直接在这里指定输入和输出文件路径
    input_path  = 'Evol-Instruct-66k-java-only.json'
    output_path = 'final-Evol-Instruct-66k-java-only.json'

    filter_java_entries(input_path, output_path)
    print(f"过滤完成，结果已保存至：{output_path}")

