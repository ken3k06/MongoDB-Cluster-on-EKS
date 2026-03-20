# Ghi chú

- Xem đầy đủ tại đây: https://ken3k06.github.io/mongodb.html


## Quy trình push code lên github

- Đầu tiên chạy `git init` trong thư mục hiện tại. git
- Sau đó chạy `git status` để kiểm tra những thay đổi. 
- Trước khi chạy `git add` ta cần tạo một file `.gitignore` trong thư mục root để bỏ qua những file không cần thiết hoặc các biến môi trường chứa credentials nhạy cảm. Tạo `touch .gitignore` rồi config trong đấy. 
- Sau đó chạy `git add .` để thêm tất cả các file đã thay đổi vào staging area. 
- Tạo nhánh chính bằng `git branch -M main`. 
- Kết nối với github: `git remote add origin <url>` . Trước đó thì cần tạo một repo trên Github rồi dán url vào. 
- Cuối cùng là đẩy code lên github bằng `git push -u origin main`. 


Lưu ý là phải thêm file `.gitignore` trước khi chạy `git add.` 


## Test app
Toàn bộ thư mục App được mình prompt phục vụ cho mục đích test deploy AWS. 

