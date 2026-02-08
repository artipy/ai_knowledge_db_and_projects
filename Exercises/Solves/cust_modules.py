import re
def clean_response(text):
    # Паттерн ищет всё между <think> и </think>, включая переносы строк
    pattern = r"<think>.*?</think>"
    
    # Заменяем найденное на пустоту и убираем лишние пробелы по краям
    cleaned_text = re.sub(pattern, "", text, flags=re.DOTALL).strip()
    return cleaned_text