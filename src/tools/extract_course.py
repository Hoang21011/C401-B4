import re
import requests
from bs4 import BeautifulSoup

def extract_course(link: str, level: str = "beginner", topic: str = "AI", format: str = "offline") -> dict:
    """
    Crawls a training center's website using BeautifulSoup to find course duration and price.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(link, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Lấy toàn bộ text từ trang web
        text = soup.get_text(separator=' ', strip=True).lower()
        
            # Các logic pattern đơn giản để tìm giá và thời lượng
            # Tìm giá (vd: 15.000.000 VNĐ, 15,000,000đ, 15 triệu)
        price_match = re.search(r'(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d+)?\s*(?:vnđ|vnd|đ|triệu))', text)
        price = price_match.group(1).upper() if price_match else "Liên hệ"
        
        # Tìm thời lượng (vd: 3 tháng, 12 tuần, 4 months)
        duration_match = re.search(r'(\d+\s*(?:tháng|tuần|giờ|buổi|months|weeks|hours))', text)
        duration = duration_match.group(1).capitalize() if duration_match else "Chưa xác định"
        
        return {
            "price": price,
            "duration": duration
        }
        
    except requests.RequestException as e:
        return {"error": f"Failed to crawl {link}: {str(e)}"}
    except Exception as e:
        return {"error": str(e)}

# Tool definition JSON
TOOL_INFO = {
  "name": "extract_course_information",
  "description": "Used to scrape or retrieve detailed course information from a training center's website. This tool extracts course duration and tuition fees. ONLY use this tool when a valid website link is already available from the output of the 'search_course_by_location' tool.",
  "parameters": {
    "type": "object",
    "properties": {
      "link": {
        "type": "string",
        "description": "A valid URL of the training center (e.g., https://example-center.com/courses). This value must be obtained from the output of the 'search_course_by_location' tool."
      },
      "level": {
        "type": "string",
        "enum": ["beginner", "intermediate", "advanced"],
        "description": "The target course level. Use 'beginner' for entry-level learners."
      },
      "topic": {
        "type": "string",
        "description": "The subject of the course (e.g., 'AI', 'Machine Learning', 'Data Science')."
      },
      "format": {
        "type": "string",
        "enum": ["offline", "online", "hybrid"],
        "description": "The learning format used to filter relevant course information."
      }
    },
    "required": ["link", "level", "topic", "format"]
  }
}
