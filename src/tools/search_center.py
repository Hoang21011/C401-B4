import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

def search_course_info(query: str) -> str:
    """
    HÃY SỬ DỤNG công cụ này khi cần tra cứu thông tin thực tế về khóa học (học phí, địa điểm, lịch học...).
    
    Lưu ý về tham số 'query':
    - Phải là từ khóa tìm kiếm ngắn gọn, trúng đích.
    
    Đầu ra (Output) sẽ là một chuỗi JSON có cấu trúc. Bạn cần phân tích cú pháp JSON này 
    để trích xuất các thông tin cần thiết như tên trung tâm, học phí, và thời lượng.
    """
    print(f"  [Tool Execution] Đang dùng Google Search: '{query}'...")
    
    api_key = os.environ.get("SERPER_API_KEY")
    if not api_key:
        return json.dumps({"status": "error", "message": "Thiếu SERPER_API_KEY"})

    url = "https://google.serper.dev/search"
    
    # Cấu hình tìm kiếm: gl=vn (Việt Nam), hl=vi (Tiếng Việt)
    payload = json.dumps({
        "q": query,
        "gl": "vn",
        "hl": "vi",
        "num": 5 # Lấy 5 kết quả
    })
    headers = {
        'X-API-KEY': api_key,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        response_data = response.json()
        
        # Kiểm tra xem có kết quả organic (kết quả tự nhiên) không
        if "organic" not in response_data or len(response_data["organic"]) == 0:
            return json.dumps({"status": "failed", "message": "Không có kết quả."})

        structured_data = []
        for i, res in enumerate(response_data["organic"], 1):
            structured_data.append({
                "id": i,
                "tieu_de": res.get("title", ""),
                "trich_dan": res.get("snippet", ""),
                "link": res.get("link", "")
            })
            
        final_output = {
            "status": "success",
            "tong_so": len(structured_data),
            "data": structured_data
        }
        return json.dumps(final_output, ensure_ascii=False, indent=2)

    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})
