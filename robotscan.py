import requests
from urllib.parse import urljoin
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class RobotsTxtEntry:
    user_agent: str
    rules: List[str] = field(default_factory=list)

class RobotsScanner:
    def __init__(self):
        self.base_url: str = ""
        self.target: str = ""
        self.entries: List[RobotsTxtEntry] = []

    def scan(self) -> bool:
        try:
            response = requests.get(self.target)
            if response.status_code == 200:
                self._parse_robots_txt(response.text)
                return True
            return False
        except requests.RequestException:
            return False

    def _parse_robots_txt(self, content: str) -> None:
        current_entry: Optional[RobotsTxtEntry] = None

        for line in content.split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            if line.lower().startswith('user-agent:'):
                if current_entry:
                    self.entries.append(current_entry)
                current_entry = RobotsTxtEntry(user_agent=line.split(':', 1)[1].strip())
            elif current_entry and ':' in line:
                current_entry.rules.append(line)

        if current_entry:
            self.entries.append(current_entry)

    def print_entries(self) -> None:
        if not self.entries:
            print(f"No robots.txt file found at {self.target}")
            return

        print(f"Robots.txt entries for {self.base_url}:")
        for entry in self.entries:
            print(f"\nUser-agent: {entry.user_agent}")
            for rule in entry.rules:
                print(f"  {rule}")
    
    def run(self):
        self.base_url = input("Enter the website URL to scan (e.g., https://www.example.com): ")
        self.target = urljoin(self.base_url, '/robots.txt')
        if self.scan():
            self.print_entries()
        else:
            print(f"Failed to retrieve robots.txt from {self.base_url}")
            