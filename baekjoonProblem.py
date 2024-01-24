import requests
from bs4 import BeautifulSoup
import csv
from tqdm import tqdm

def clean_text(text):
    text = text.replace('\\', '\\\\')  # 역슬래시 이스케이프 처리
    text = text.replace('"', '""')  # 큰따옴표 이스케이프 처리
    return f'"{text}"'

def crawl_problem(problem_number):
    url = f"https://www.acmicpc.net/problem/{problem_number}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers, allow_redirects=True)
    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.find('span', id='problem_title').text.strip() if soup.find('span', id='problem_title') else "N/A"
    description = soup.find('div', id='problem_description')
    input_description = soup.find('div', id='problem_input').text.strip() if soup.find('div', id='problem_input') else "N/A"
    output_description = soup.find('div', id='problem_output').text.strip() if soup.find('div', id='problem_output') else "N/A"

    if description:
        if description:
            images = description.find_all('img')
        for img in images:
            # Extract the image URL and replace the image tag with the image URL in the description text
            image_url = img.get('src')
            img.replace_with(image_url)

        description_texts = []
        for element in description.contents:
            text = ''
            if element.name == 'p':
                text = element.get_text(separator=' ', strip=True)
            elif element.name == 'pre':
                text = element.get_text(separator='\n', strip=True)
            else:
                continue
            description_texts.append(text)
        description_text = '\n'.join(description_texts).strip()
    else:
        description_text = "N/A"

    sample_input = soup.find('pre', id='sample-input-1').get_text(separator='\n').strip() if soup.find('pre', id='sample-input-1') else "N/A"
    sample_output = soup.find('pre', id='sample-output-1').get_text(separator='\n').strip() if soup.find('pre', id='sample-output-1') else "N/A"

    return {
        "ID": problem_number,
        "Title": clean_text(title),
        "Description": clean_text(description_text),
        "Input Description": clean_text(input_description),
        "Output Description": clean_text(output_description),
        "Sample Input": clean_text(sample_input),
        "Sample Output": clean_text(sample_output)
    }

def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["ID", "Title", "Description", "Input Description", "Output Description", "Sample Input", "Sample Output"])
        writer.writeheader()
        for row in data:
            writer.writerow(row)

problem_range = range(1000, 31227)
problems = []

for i in tqdm(problem_range, desc="Crawling Problems"):
    problems.append(crawl_problem(i))

save_to_csv(problems, 'baekjoon_problems.csv')
print("Crawling completed and saved to 'baekjoon_problems.csv'")