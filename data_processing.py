import os
import pandas as pd

class DataPreprocessingFramework:
    def __init__(self, file_path):
        self.file_path = file_path
        self.excel_data = pd.ExcelFile(file_path)  # Mở file Excel
        self.sheet_names = self.excel_data.sheet_names
        self.cleaned_sheets = {}

    def clean_data(self, data):
        # Loại bỏ các cột trống hoàn toàn
        data_cleaned = data.dropna(how='all', axis=1)

        # Loại bỏ các hàng trống hoàn toàn
        data_cleaned = data_cleaned.dropna(how='all', axis=0)

        # Reset lại chỉ số cho dữ liệu sạch
        data_cleaned.reset_index(drop=True, inplace=True)

        # Đổi tên các cột nếu hàng đầu tiên chứa tên cột
        if data_cleaned.iloc[0].isnull().sum() == 0:  # Nếu hàng đầu không có giá trị null, xem như tiêu đề cột
            data_cleaned.columns = data_cleaned.iloc[0]
            data_cleaned = data_cleaned.drop(0).reset_index(drop=True)

        # Loại bỏ các hàng thiếu thông tin chính (nếu cần)
        if data_cleaned.columns[0] not in [None, '']:  # Đảm bảo cột đầu tiên phải có giá trị
            data_cleaned.dropna(subset=[data_cleaned.columns[0]], inplace=True)

        # Loại bỏ các hàng trùng lặp
        data_cleaned = data_cleaned.drop_duplicates()

        return data_cleaned

    def preprocess_all_sheets(self):
        # Lặp qua tất cả các sheet và làm sạch dữ liệu
        for sheet in self.sheet_names:
            sheet_data = pd.read_excel(self.file_path, sheet_name=sheet)
            self.cleaned_sheets[sheet] = self.clean_data(sheet_data)

    def save_cleaned_data(self, output_file_path):
        # Lưu tất cả các sheet đã được làm sạch vào một file Excel mới
        with pd.ExcelWriter(output_file_path, engine='xlsxwriter') as writer:
            for sheet_name, cleaned_data in self.cleaned_sheets.items():
                cleaned_data.to_excel(writer, sheet_name=sheet_name, index=False)
        print(f"Dữ liệu đã làm sạch đã được lưu vào {output_file_path}")

def process_excel_file(input_file, output_folder):
    """
    Hàm xử lý file Excel và lưu với tên {tên_file_upload}_Cleaned.xlsx
    """
    data_processor = DataPreprocessingFramework(input_file)
    data_processor.preprocess_all_sheets()

    # Lấy tên file từ đường dẫn input_file và thêm hậu tố _Cleaned
    base_filename = os.path.splitext(os.path.basename(input_file))[0]
    cleaned_filename = f"{base_filename}_Cleaned.xlsx"

    # Lưu file vào thư mục output_folder với tên mới
    output_file = os.path.join(output_folder, cleaned_filename)
    data_processor.save_cleaned_data(output_file)

    return output_file
