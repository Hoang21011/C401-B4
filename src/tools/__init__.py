from .search_center import search_course_info
from .calculate_course_fee import calculate_course_fee 
from .extract_course import extract_course

# 2. KHAI BÁO TOOL_REGISTRY (Nhồi vào System Prompt cho AI đọc)
TOOL_REGISTRY = [
    {
        "name": "search_course_info",
        "description": "Tra cứu thông tin thực tế về khóa học trên internet (học phí, địa điểm...). Đầu vào là một từ khóa ngắn gọn.",
        "args": ["query"]
    },
    {
        "name": "calculate_fee",
        "description": "Tính toán chi phí, học phí, tiền giảm giá. Đầu vào phải là một biểu thức toán học hợp lệ (VD: '12000000 * 0.9').",
        "args": ["expression"]
    },
    {
        "name": "extract_pdf_data",
        "description": "Trích xuất thông tin chi tiết hoặc bảng biểu từ tài liệu/PDF nội bộ. Sử dụng khi cần đọc thông tin từ file người dùng cung cấp.",
        "args": ["file_path_or_query"]
    }
]

# 3. KHAI BÁO TOOL_FUNCTIONS (Bản đồ để file agent.py biết đường gọi đúng code)
TOOL_FUNCTIONS = {
    "search_course_info": search_course_info,
    "calculate_course_fee": calculate_course_fee,
    "extract_course": extract_course
}