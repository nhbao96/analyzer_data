document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('upload-form');
    const resultDiv = document.getElementById('result');

    form.addEventListener('submit', async function(event) {
        event.preventDefault();  // Ngăn chặn hành vi mặc định của form
        
        // Thu thập dữ liệu form
        const formData = new FormData(form);

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (response.ok) {
                // Hiển thị kết quả thành công
                resultDiv.innerHTML = `✅ ${result.message}. File đã xử lý: <a href="${result.processed_file}" download>Download File</a>`;
            } else {
                // Hiển thị lỗi nếu xảy ra vấn đề
                resultDiv.innerHTML = `❌ Lỗi: ${result.error}`;
            }
        } catch (error) {
            resultDiv.innerHTML = `❌ Đã xảy ra lỗi khi gửi file.`;
        }
    });
});
