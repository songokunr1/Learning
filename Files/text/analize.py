from dataclasses import dataclass, field
from typing import Optional, List
import pandas as pd


@dataclass
class JobPosting:
    position: str
    salary_raw: str
    salary_from: Optional[int] = field(init=False)
    salary_to: Optional[int] = field(init=False)
    tags: List[str]
    company: str

    def __post_init__(self):
        self.salary_from, self.salary_to = self._parse_salary(self.salary_raw)

    @staticmethod
    def _parse_salary(salary_raw: str) -> (Optional[int], Optional[int]):
        try:
            range_part = salary_raw.split('PLN')[0].strip()  # Remove 'PLN'
            salary_from_str, salary_to_str = range_part.split('–')

            salary_from = int(salary_from_str.replace(' ', ''))
            salary_to = int(salary_to_str.replace(' ', ''))

            return salary_from, salary_to
        except (AttributeError, ValueError, IndexError):
            return None, None


with open('Files/text/zarobki3.txt', 'r', encoding='utf-8') as f:
    fil = f.read()
    offers = fil.split('Company logo')
    print(len(offers))
    offers = offers[1:]


def extract_tags(text):
    print(text)
    if 'Salary Match' in text:
        tags = text.split('Salary Match')[1].split(' ')[0].split('\n')
        return tags
    try:

        tags = text.split('PLN')[1].split(' ')[0].split('\n')
        return tags[1:-1]
    except:
        return []


def extract_position(text):
    return text.split('\n')[1]


def extract_salary_raw(text):
    return text.split('\n')[3]


def extract_company(text):
    cleaned = [row for row in text.split('\n') if row]
    company = [row for row in cleaned if row[0] == ' ']
    try:
        return company[0].strip()
    except:
        return ''


jobs = [JobPosting(
    position=extract_position(offer),
    salary_raw=extract_salary_raw(offer),
    tags=extract_tags(offer),
    company=extract_company(offer)
) for offer in offers]


df = pd.DataFrame(jobs)
print(df)

df_exploded = df.explode('tags')
df_exploded['salary_mean'] = (df_exploded['salary_from'] + df_exploded['salary_to']) / 2
# Group by tags and calculate the count and mean for salary_from and salary_to
result = df_exploded.groupby('tags').agg(
    count=('tags', 'size'),
    mean_salary_from=('salary_from', 'mean'),
    mean_salary_to=('salary_to', 'mean'),
    mean_salary_mean=('salary_mean', 'mean')

).reset_index()
result = result[result['count'] > 10]
result = result.sort_values(by='count', ascending=False).head(20)

print(result)