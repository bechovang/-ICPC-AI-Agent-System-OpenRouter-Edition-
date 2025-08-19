# Hệ thống Agent AI cho ICPC (Phiên bản OpenRouter)

Một hệ thống multi-agent (đa tác tử) tự động được thiết kế để hỗ trợ giải các bài toán lập trình thi đấu, được cung cấp sức mạnh bởi các Mô hình Ngôn ngữ Lớn (LLM) hiệu năng cao thông qua API của OpenRouter. Hệ thống này phân tích đề bài, xây dựng chiến lược, sinh mã nguồn C++, và kiểm thử giải pháp trong một quy trình được tối ưu hóa.

## 🏆 Triết lý Cốt lõi

Mục tiêu của dự án không phải là để thay thế lập trình viên, mà là để đóng vai trò một **Trợ lý AI** siêu nhanh và giàu kiến thức. Bằng cách tận dụng các LLM mạnh mẽ từ xa, nó tự động hóa các tác vụ suy luận và lập trình phức tạp, cho phép người thi tập trung vào chiến lược cấp cao và giải quyết các khía cạnh tinh vi của bài toán.

## ✨ Tại sao lại dùng OpenRouter?

Phiên bản này chuyển từ việc chạy LLM local sang sử dụng API của OpenRouter, mang lại nhiều lợi ích chính:

1.  **Tiếp cận các Model Hàng đầu:** Sử dụng các model mạnh mẽ, độc quyền (như GPT-4o, Claude 3 Opus, và nhiều phiên bản DeepSeek) vốn quá lớn để chạy trên máy cá nhân.
2.  **Không tốn Tài nguyên Máy tính:** Mọi tính toán chuyên sâu đều được xử lý trên đám mây. Điều này giải phóng CPU và RAM của máy tính, cho phép hệ thống chạy mượt mà ngay cả trên các laptop yếu.
3.  **Linh hoạt:** Dễ dàng chuyển đổi giữa các model khác nhau—bao gồm cả các model miễn phí—chỉ bằng cách thay đổi một dòng code, cho phép bạn cân bằng giữa chi phí, tốc độ và độ thông minh.
4.  **Luôn được Cập nhật:** Ngay lập tức tiếp cận được các model mới nhất và tốt nhất ngay khi chúng được thêm vào nền tảng OpenRouter.

## 🛠️ Kiến trúc Hệ thống

Hệ thống hoạt động như một "dây chuyền sản xuất" gồm các Agent chuyên biệt, được quản lý bởi một "nhạc trưởng":

1.  **Orchestrator (`main.py`):** Điểm khởi đầu chính. Nó nhận đề bài thô làm đầu vào và điều phối luồng công việc giữa các Agent.
2.  **Analysis Agent (Agent Phân tích):** Phân tích văn bản thô của đề bài, trích xuất dữ liệu có cấu trúc như tiêu đề, các bài toán con (subtask), ràng buộc (constraints), và các ví dụ đầu vào/đầu ra (sample cases).
3.  **Strategy Agent (Agent Chiến lược):** "Huấn luyện viên" của đội. Với mỗi subtask, nó truy vấn cơ sở tri thức RAG để tìm ra thuật toán hoặc cấu trúc dữ liệu phù hợp nhất.
4.  **Coding Agent (Agent Viết Code):** Lập trình viên chủ lực. Nó nhận chiến lược và ngữ cảnh bài toán, sau đó yêu cầu LLM từ xa thông qua OpenRouter sinh ra một giải pháp C++ hoàn chỉnh và có thể chạy được.
5.  **Validation Agent (Agent Kiểm thử):** "Tester" của đội. Nó tự động biên dịch mã C++ được sinh ra (sử dụng trình biên dịch G++ local) và chạy thử với các ví dụ.

## 🚀 Bắt đầu

### Yêu cầu
-   Python 3.9+
-   Một trình biên dịch C++ (G++). Xem [**Hướng dẫn Cài đặt G++**](./INSTALL_GXX.md) để biết thêm chi tiết.
-   Kết nối Internet.

### 1. (QUAN TRỌNG) Lấy và Thiết lập API Key của OpenRouter

Hệ thống này yêu cầu một API key để giao tiếp với OpenRouter.

#### a. Lấy Key của bạn

1.  Truy cập [OpenRouter.ai](https://openrouter.ai/) và đăng nhập.
2.  Nhấp vào biểu tượng profile ở góc trên bên phải, sau đó chọn **Keys**.
3.  Nhấp **+ Create Key**, đặt tên cho key (ví dụ: `icpc-assistant`), và nhấp **Create**.
4.  **Sao chép key ngay lập tức.** Nó sẽ chỉ được hiển thị một lần duy nhất. Key có dạng `sk-or-...`.

#### b. Thiết lập Biến Môi trường

Bạn phải lưu key của mình dưới dạng biến môi trường để bảo mật. **Không bao giờ dán key trực tiếp vào code.**

**Trên Windows:**

1.  Mở Command Prompt (cmd) **với quyền Administrator**.
2.  Chạy lệnh sau, thay thế `<YOUR_API_KEY>` bằng key bạn đã sao chép:
    ```cmd
    setx OPENROUTER_API_KEY "<YOUR_API_KEY>"
    ```
3.  **Đóng và mở lại** tất cả các cửa sổ terminal hoặc trình soạn thảo code để thay đổi có hiệu lực.

**Trên macOS / Linux:**

1.  Mở terminal của bạn.
2.  Chỉnh sửa file cấu hình shell (ví dụ: `~/.zshrc`, `~/.bashrc`):
    ```bash
    nano ~/.zshrc
    ```
3.  Thêm dòng này vào cuối file, thay thế `<YOUR_API_KEY>`:
    ```bash
    export OPENROUTER_API_KEY="<YOUR_API_KEY>"
    ```
4.  Lưu file, thoát, và áp dụng thay đổi bằng cách chạy `source ~/.zshrc` hoặc khởi động lại terminal.

### 2. Cài đặt Dự án

Sao chép repository và cài đặt các gói Python cần thiết bằng môi trường ảo.

```bash
# Sao chép repository
git clone <đường-dẫn-repo-của-bạn>
cd ICPC_AI_Assistant_openrouter

# Tạo và kích hoạt môi trường ảo
python -m venv venv
# Trên Windows:
.\venv\Scripts\activate
# Trên macOS/Linux:
# source venv/bin/activate

# Cài đặt tất cả các gói cần thiết
pip install -r requirements.txt
```

### 3. Chọn LLM của bạn

Mở file `rag_system.py` và tìm đến hàm `setup_llm`. Bạn có thể thay đổi chuỗi `model` thành bất kỳ model nào có sẵn trên OpenRouter. Mặc định hiện tại là một model miễn phí và mạnh mẽ.

```python
# Trong file rag_system.py
self.llm = ChatOpenAI(
    # Tìm tên model trên openrouter.ai/models
    model="deepseek/deepseek-r1-0528:free", 
    ...
)
```

### 4. Xây dựng Cơ sở Tri thức

Trước lần chạy đầu tiên, hoặc bất cứ khi nào bạn cập nhật thư mục `data/`, bạn phải xây dựng lại kho vector:

```bash
# Lệnh này sẽ đọc tất cả các file JSON, xử lý chúng, và tạo ra thư mục `vectorstore`.
python rag_system.py
```

### 5. Chạy Hệ thống

Để giải một bài toán, hãy chạy "nhạc trưởng":

```bash
python main.py
```

Hệ thống sẽ yêu cầu bạn dán đề bài vào. Sau khi dán, gõ `---` trên một dòng mới và nhấn Enter. Các Agent sẽ bắt đầu làm việc, giao tiếp với OpenRouter để tạo ra một giải pháp.

---

## 🚧 Các Vấn đề Hiện tại & Lộ trình Phát triển

Dự án này đang trong giai đoạn phát triển. Dưới đây là các vấn đề đã biết và các lĩnh vực cần cải thiện trong tương lai.

### 📌 Vấn đề đã biết (Cần sửa trong ngắn hạn)

1.  **Phụ thuộc Mạng & Lỗi kết nối:**
    -   **Vấn đề:** Hệ thống hoàn toàn phụ thuộc vào kết nối internet và trạng thái của API OpenRouter. Lỗi timeout mạng hoặc lỗi API có thể làm ngưng toàn bộ quy trình.
    -   **Giải pháp đề xuất:** Một `request_timeout` đã được thêm vào. Các cải tiến tiếp theo sẽ bao gồm việc triển khai cơ chế thử lại (ví dụ: sử dụng thư viện `tenacity`) để tự động thử lại các lệnh gọi API bị lỗi.

2.  **Độ nhạy của Prompt:**
    -   **Vấn đề:** Chất lượng của code được sinh ra rất nhạy cảm với prompt được gửi đến `CodingAgent`. Một thay đổi nhỏ trong cách diễn đạt của đề bài đôi khi có thể làm LLM bối rối.
    -   **Giải pháp đề xuất:** Liên tục tinh chỉnh các prompt trong `agents.py`. Triển khai kỹ thuật "Few-Shot Prompting", trong đó prompt bao gồm 1-2 ví dụ về bộ ba (đề bài, chiến lược, code) để cung cấp cho model một mẫu tốt hơn để noi theo.

3.  **Giới hạn Cửa sổ Ngữ cảnh (Context Window):**
    -   **Vấn đề:** Đối với các đề bài cực dài hoặc các mục trong cơ sở tri thức quá chi tiết, ngữ cảnh kết hợp có thể vượt quá giới hạn cửa sổ của model, dẫn đến lỗi hoặc thông tin bị cắt bớt.
    -   **Giải pháp đề xuất:** Chuyển đổi loại của chuỗi `RetrievalQA` từ `"stuff"` (nhồi tất cả ngữ cảnh vào một lần) sang một loại nâng cao hơn như `"map_reduce"` hoặc `"refine"`, có thể xử lý lượng ngữ cảnh lớn hơn bằng cách xử lý theo từng đoạn.

### 🌱 Lộ trình Phát triển (Tầm nhìn Dài hạn)

1.  **Agent Tự động Chọn Model:**
    -   **Tầm nhìn:** Tạo một agent "kiểm soát chi phí" chạy trước `StrategyAgent`. Nó sẽ phân tích độ khó của bài toán và quyết định nên sử dụng model nào. Đối với các bài toán ad-hoc dễ, nó có thể chọn một model nhanh, rẻ. Đối với các bài đồ thị hoặc DP phức tạp, nó sẽ leo thang lên một model hàng đầu như GPT-4o hoặc Claude 3 Opus để đảm bảo chất lượng chiến lược và code cao nhất.

2.  **Tự động Mở rộng Cơ sở Tri thức:**
    -   **Tầm nhìn:** Tạo một agent có khả năng duyệt các trang thi đấu như Codeforces. Khi nó tìm thấy một bài toán mới và "editorial" (bài giải thích chính thức), nó có thể tự động sử dụng một LLM mạnh để phân tích bài giải và các lời giải được chấp nhận, từ đó tạo ra một file kiến thức `.json` mới để thêm vào `data/algorithms`. Điều này sẽ giúp hệ thống tự cải thiện.

3.  **Agent Gỡ lỗi Tương tác:**
    -   **Tầm nhìn:** Khi một giải pháp thất bại trong quá trình kiểm thử, một `InteractiveDebuggerAgent` sẽ lấy code và test case bị lỗi. Sau đó, nó sẽ sử dụng LLM để phân tích code, đưa ra giả thuyết về vị trí của lỗi, và đề xuất các bản sửa lỗi cụ thể hoặc các câu lệnh in để thêm vào, mô phỏng một buổi gỡ lỗi lập trình đôi.

4.  **Cơ chế Dự phòng Local:**
    -   **Tầm nhìn:** Để sử dụng ngoại tuyến hoặc khi API gặp lỗi, hệ thống có thể tự động chuyển về sử dụng một LLM local (như Ollama với một model nhỏ). Orchestrator `main.py` sẽ phát hiện việc thiếu API key hoặc kết nối mạng và tự động chuyển đổi `llm` trong các agent sang một phiên bản chạy local.


-----------------------------------------------------


## Installation Guide for G++ (MinGW-w64) on Windows using MSYS2



### **Phiên bản Tiếng Việt**

#### Giới thiệu

Tài liệu này hướng dẫn chi tiết cách cài đặt bộ công cụ biên dịch GNU C/C++ (bao gồm `g++`) trên hệ điều hành Windows. Đây là bước bắt buộc để `ValidationAgent` trong dự án có thể biên dịch và kiểm thử các file C++ do AI tạo ra.

Chúng ta sẽ sử dụng **MSYS2**, một nền tảng phân phối phần mềm hiện đại và mạnh mẽ, để cài đặt phiên bản mới nhất của MinGW-w64.

#### Các bước Cài đặt

##### Bước 1: Tải về MSYS2

1.  Truy cập trang chủ chính thức của MSYS2: [https://www.msys2.org/](https://www.msys2.org/)
2.  Nhấp vào nút tải về để tải file cài đặt (ví dụ: `msys2-x86_64-YYYYMMDD.exe`).

##### Bước 2: Cài đặt MSYS2

1.  Chạy file cài đặt bạn vừa tải về.
2.  Làm theo các hướng dẫn trên màn hình.
3.  **❗ Quan trọng:** Chúng tôi thực sự khuyên bạn nên giữ nguyên đường dẫn cài đặt mặc định là `C:\msys64` để các bước cấu hình sau này được chính xác.

##### Bước 3: Cập nhật CSDL Gói (Package Database)

1.  Sau khi cài đặt xong, một cửa sổ terminal của MSYS2 sẽ tự động mở ra. Nếu không, hãy tìm "MSYS2 UCRT64" trong Start Menu và mở nó.
2.  Chạy lệnh sau để cập nhật toàn bộ hệ thống gói:
    ```bash
    pacman -Syu
    ```3.  Quá trình này có thể yêu cầu bạn đóng cửa sổ terminal. Nếu có thông báo `warning: terminate MSYS2 without returning to shell? [Y/n]`, hãy gõ `Y` và nhấn Enter. Sau đó, **mở lại "MSYS2 UCRT64" từ Start Menu** và chạy lại lệnh `pacman -Syu` một lần nữa để hoàn tất cập nhật.

##### Bước 4: Cài đặt Bộ công cụ Biên dịch C++ (Toolchain)

1.  Trong cửa sổ terminal MSYS2, chạy lệnh sau để cài đặt bộ công cụ MinGW-w64 cần thiết (bao gồm `gcc`, `g++`, `gdb`, `make`...):
    ```bash
    pacman -S --needed base-devel mingw-w64-ucrt-x86_64-toolchain
    ```
2.  Hệ thống sẽ liệt kê các gói trong bộ công cụ và hỏi bạn lựa chọn.
    
    *   `Enter a selection (default=all):`
    *   Chỉ cần **nhấn Enter** để chấp nhận lựa chọn mặc định (cài đặt tất cả).
3.  Hệ thống sẽ hỏi bạn xác nhận lần nữa. Gõ `Y` và nhấn `Enter` để bắt đầu quá trình tải về và cài đặt.

##### Bước 5: (QUAN TRỌNG NHẤT) Cấu hình Biến Môi trường PATH

Để Windows có thể tìm thấy lệnh `g++` từ bất kỳ đâu, bạn phải thêm đường dẫn của nó vào biến môi trường `PATH`.

1.  Mở Start Menu, gõ `env` và chọn **"Edit the system environment variables"**.
2.  Trong cửa sổ System Properties, nhấp vào nút **"Environment Variables..."**.
3.  Trong ô **"System variables"** (ô dưới), tìm và chọn biến có tên là `Path`, sau đó nhấp **"Edit..."**.
4.  Trong cửa sổ Edit environment variable, nhấp **"New"**.
5.  Dán đường dẫn chính xác đến thư mục `bin` của trình biên dịch. Nếu bạn đã cài đặt ở vị trí mặc định, đường dẫn sẽ là:
    ```
    C:\msys64\ucrt64\bin
    ```
6.  Nhấp **OK** trên tất cả các cửa sổ để lưu lại thay đổi.

##### Bước 6: Xác minh Cài đặt

1.  **❗ Cực kỳ quan trọng:** **Đóng tất cả** các cửa sổ Terminal, Command Prompt, PowerShell, và trình soạn thảo code (VS Code) đang mở.
2.  Mở một cửa sổ **Command Prompt (cmd) mới**.
3.  Gõ lệnh sau và nhấn Enter:
    ```bash
    g++ --version
    ```
4.  Nếu cài đặt thành công, bạn sẽ thấy output tương tự như sau, hiển thị phiên bản của G++:
    ```
    g++ (ucrt64-14.0.0-1) 14.0.0
    Copyright (C) 2024 Free Software Foundation, Inc.
    ...
    ```
5.  Nếu bạn nhận được lỗi `'g++' is not recognized...`, hãy kiểm tra lại cẩn thận **Bước 5**, đảm bảo bạn đã nhập đúng đường dẫn và đã khởi động lại Terminal.

**🚀 Chúc mừng! Môi trường biên dịch C++ của bạn đã sẵn sàng hoạt động.**
