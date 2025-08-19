

# Guide to Creating Knowledge Base Data (JSON V2.0)

## Hướng dẫn Tạo Dữ liệu cho Cơ sở Tri thức (JSON V2.0)

---

### **English Version**

#### Introduction

This document is the official guide for creating and structuring the JSON data files that form the AI's knowledge base. These files, located in `data/algorithms/`, are the foundation of the `StrategyAgent`'s intelligence.

The quality of these files directly impacts the system's performance. A well-structured, detailed, and descriptive JSON file will enable the Retrieval-Augmented Generation (RAG) system to find highly relevant information and help the LLM generate accurate strategies and code.

#### File Location and Naming

-   **Location:** All knowledge files must be placed in the `data/algorithms/` directory.
-   **Naming:** Use a descriptive, lowercase name with underscores instead of spaces. For example, `disjoint_set_union.json`, `segment_tree_lazy.json`.

#### The JSON V2.0 Structure

Each `.json` file must be a single JSON object with the following fields.

| Field | Type | Required? | Description |
| :--- | :--- | :--- | :--- |
| `title` | String | Yes | The official name of the algorithm or data structure. (e.g., "Disjoint Set Union (DSU)") |
| `aliases` | Array of Strings | No | Other common names for the algorithm. **Crucial for search.** (e.g., `["Union-Find", "Merge-Find Set"]`) |
| `categories` | Array of Strings | Yes | Broad categories the algorithm belongs to. Helps in finding general solutions. (e.g., `["graph", "data_structure", "connectivity"]`) |
| `summary` | String | Yes | A concise, one-sentence, keyword-rich summary. This is often the first thing the RAG system looks at. |
| `prerequisites` | Array of Strings | No | Concepts a user should know before learning this one. (e.g., `["Arrays", "Trees", "Recursion"]`) |
| `complexity` | Object | Yes | A structured object for time and space complexities. (e.g., `{"operation": "O(α(N))", "space": "O(N)"}`) |
| `theory` | String | Yes | A detailed explanation of how the algorithm works, its core ideas, and its applications. |
| `implementations`| Array of Objects | Yes | Contains one or more C++ code implementations for different variations. Each object has `name`, `language`, and `code`. |
| `common_pitfalls`| Array of Strings | No | A list of common mistakes or bugs when implementing this algorithm. Helps the `CodingAgent` write more robust code. |
| `example_problems`| Array of Objects | Yes | **The most important field for RAG.** Describes classic problems that use this algorithm. Each object has `id`, `link`, `description`, `tags`, and `variation`. |

#### In-Depth Field Explanations

-   **`implementations` Object Structure:**
    ```json
    {
      "name": "DSU with Path Compression and Union by Size",
      "language": "cpp",
      "code": "#include <vector>\\n\\nstruct DSU { ... };"
    }
    ```
    **Important:** The `code` field must be a single string. All newlines must be escaped as `\n`, and all double quotes must be escaped as `\"`.

-   **`example_problems` Object Structure:**
    This is what makes the RAG system "intelligent".
    ```json
    {
      "id": "CSES Road Construction",
      "link": "https://cses.fi/problemset/task/1676",
      "description": "This problem asks to report the number of connected components... This is a direct application of DSU...",
      "tags": ["connectivity", "dsu", "union-find"],
      "variation": "Tracking component count and max size"
    }
    ```
    The **`description`** field is critical. It should explain *why* and *how* the algorithm solves this specific problem. The RAG system performs a **semantic search** on this text. A detailed description allows the system to match a new, unseen problem to a known problem pattern.

#### Complete Example: `disjoint_set_union.json`

Use this as a template for creating new files.

```json
{
  "title": "Disjoint Set Union (DSU)",
  "aliases": ["Union-Find", "Merge-Find Set"],
  "categories": ["data_structure", "graph", "connectivity"],
  "summary": "A highly efficient data structure to track a set of elements partitioned into a number of disjoint (non-overlapping) subsets. Used for connectivity problems in graphs or grouping elements.",
  "prerequisites": ["Array", "Tree", "Recursion"],
  "complexity": {
    "operation": "O(α(N)) - Nearly constant time",
    "space": "O(N)"
  },
  "theory": "DSU maintains a collection of disjoint sets. It provides two main operations: `find`, which determines which subset an element is in (by finding its root), and `unite`, which merges two subsets. Its efficiency comes from two key optimizations: 'Union by Size/Rank' and 'Path Compression', which keep the internal trees very flat, making operations nearly O(1).",
  "implementations": [
    {
      "name": "DSU with Path Compression and Union by Size",
      "language": "cpp",
      "code": "#include <vector>\\n#include <numeric>\\n\\nstruct DSU {\\n    std::vector<int> parent;\\n    std::vector<int> sz;\\n    int components;\\n\\n    DSU(int n) {\\n        parent.resize(n + 1);\\n        std::iota(parent.begin(), parent.end(), 0);\\n        sz.assign(n + 1, 1);\\n        components = n;\\n    }\\n\\n    int find(int i) {\\n        if (parent[i] == i) return i;\\n        return parent[i] = find(parent[i]);\\n    }\\n\\n    void unite(int i, int j) {\\n        int root_i = find(i);\\n        int root_j = find(j);\\n        if (root_i != root_j) {\\n            if (sz[root_i] < sz[root_j]) std::swap(root_i, root_j);\\n            parent[root_j] = root_i;\\n            sz[root_i] += sz[root_j];\\n            components--;\\n        }\\n    }\\n};"
    }
  ],
  "common_pitfalls": [
    "Using 0-based instead of 1-based indexing without careful array initialization.",
    "Forgetting to initialize the DSU, where each element is its own parent.",
    "Implementing `find` without path compression, which severely degrades performance."
  ],
  "example_problems": [
    {
      "id": "CSES Road Construction",
      "link": "https://cses.fi/problemset/task/1676",
      "description": "The problem asks to process a series of newly built roads and, after each addition, report the number of connected components and the size of the largest one. This is a direct application of DSU: each city is an element, and each road is a `unite` operation. The number of components and max size can be tracked easily.",
      "tags": ["connectivity", "dsu", "union-find", "components"],
      "variation": "Tracking component count and max size"
    }
  ]
}
```

#### **❗ Final, Mandatory Step**

After you **add, edit, or delete any `.json` file** in the `data/algorithms/` directory, you **MUST** rebuild the knowledge base:

1.  Delete the existing `vectorstore/` directory.
2.  Run the command: `python rag_system.py`

Your AI will not learn about the new data until you perform this step.

---

### **Phiên bản Tiếng Việt**

#### Giới thiệu

Tài liệu này là hướng dẫn chính thức để tạo và cấu trúc các file dữ liệu JSON, vốn là nền tảng cho cơ sở tri thức của AI. Các file này, đặt tại `data/algorithms/`, là trái tim của trí thông minh của `StrategyAgent`.

Chất lượng của các file này ảnh hưởng trực tiếp đến hiệu suất của hệ thống. Một file JSON có cấu trúc tốt, chi tiết và giàu mô tả sẽ cho phép hệ thống RAG (Retrieval-Augmented Generation) tìm thấy thông tin liên quan cao và giúp LLM tạo ra các chiến lược và mã nguồn chính xác.

#### Vị trí và Tên file

-   **Vị trí:** Tất cả các file kiến thức phải được đặt trong thư mục `data/algorithms/`.
-   **Tên file:** Sử dụng tên mô tả, viết thường, có dấu gạch dưới thay vì khoảng trắng. Ví dụ: `disjoint_set_union.json`, `segment_tree_lazy.json`.

#### Cấu trúc JSON V2.0

Mỗi file `.json` phải là một đối tượng JSON duy nhất với các trường sau.

| Trường (Field) | Kiểu (Type) | Bắt buộc? | Mô tả |
| :--- | :--- | :--- | :--- |
| `title` | String | Có | Tên chính thức của thuật toán hoặc cấu trúc dữ liệu. (ví dụ: "Disjoint Set Union (DSU)") |
| `aliases` | Mảng chuỗi | Không | Các tên gọi phổ biến khác của thuật toán. **Rất quan trọng cho việc tìm kiếm.** (ví dụ: `["Union-Find", "Hợp nhất-Tìm kiếm"]`) |
| `categories` | Mảng chuỗi | Có | Các danh mục lớn mà thuật toán thuộc về. Giúp tìm các giải pháp chung. (ví dụ: `["graph", "data_structure", "connectivity"]`) |
| `summary` | String | Có | Một câu tóm tắt ngắn gọn, giàu từ khóa. Đây thường là thứ đầu tiên hệ thống RAG xem xét. |
| `prerequisites` | Mảng chuỗi | Không | Các khái niệm người dùng nên biết trước khi học khái niệm này. (ví dụ: `["Arrays", "Trees", "Recursion"]`) |
| `complexity` | Object | Có | Một đối tượng có cấu trúc cho độ phức tạp về thời gian và không gian. (ví dụ: `{"operation": "O(α(N))", "space": "O(N)"}`) |
| `theory` | String | Có | Giải thích chi tiết về cách thuật toán hoạt động, ý tưởng cốt lõi và các ứng dụng. |
| `implementations`| Mảng Object | Có | Chứa một hoặc nhiều phiên bản cài đặt bằng C++ cho các biến thể khác nhau. Mỗi object có `name`, `language`, và `code`. |
| `common_pitfalls`| Mảng chuỗi | Không | Danh sách các lỗi hoặc nhầm lẫn phổ biến khi cài đặt thuật toán này. Giúp `CodingAgent` viết code an toàn hơn. |
| `example_problems`| Mảng Object | Có | **Trường quan trọng nhất cho RAG.** Mô tả các bài toán kinh điển sử dụng thuật toán này. Mỗi object có `id`, `link`, `description`, `tags`, và `variation`. |

#### Giải thích Chi tiết các Trường

-   **Cấu trúc Object `implementations`:**
    ```json
    {
      "name": "DSU with Path Compression and Union by Size",
      "language": "cpp",
      "code": "#include <vector>\\n\\nstruct DSU { ... };"
    }
    ```
    **Lưu ý:** Trường `code` phải là một chuỗi duy nhất. Tất cả các ký tự xuống dòng phải được thay thế bằng `\n`, và tất cả dấu ngoặc kép phải được thay thế bằng `\"`.

-   **Cấu trúc Object `example_problems`:**
    Đây là thứ làm cho hệ thống RAG trở nên "thông minh".
    ```json
    {
      "id": "CSES Road Construction",
      "link": "https://cses.fi/problemset/task/1676",
      "description": "Bài toán yêu cầu báo cáo số lượng thành phần liên thông... Đây là một ứng dụng trực tiếp của DSU...",
      "tags": ["connectivity", "dsu", "union-find"],
      "variation": "Tracking component count and max size"
    }
    ```
    Trường **`description`** là cực kỳ quan trọng. Nó nên giải thích *tại sao* và *làm thế nào* thuật toán giải quyết bài toán cụ thể này. Hệ thống RAG thực hiện một **tìm kiếm ngữ nghĩa** (semantic search) trên văn bản này. Một mô tả chi tiết cho phép hệ thống đối sánh một bài toán mới, chưa từng thấy với một dạng bài đã biết.

#### Ví dụ Hoàn chỉnh: `disjoint_set_union.json`

Sử dụng file này như một mẫu để tạo các file mới.

```json
{
  "title": "Disjoint Set Union (DSU)",
  "aliases": ["Union-Find", "Hợp nhất-Tìm kiếm"],
  "categories": ["data_structure", "graph", "connectivity"],
  "summary": "Một cấu trúc dữ liệu cực kỳ hiệu quả để theo dõi các tập hợp không giao nhau. Thường dùng để giải các bài toán liên quan đến tính liên thông trong đồ thị hoặc nhóm các phần tử.",
  "prerequisites": ["Array", "Tree", "Recursion"],
  "complexity": {
    "operation": "O(α(N)) - Gần như hằng số",
    "space": "O(N)"
  },
  "theory": "DSU duy trì một tập hợp các phần tử được chia thành nhiều tập con không giao nhau. Nó cung cấp hai hoạt động chính: `find`, để xác định xem một phần tử thuộc tập con nào (bằng cách tìm gốc của nó), và `unite`, để hợp nhất hai tập con thành một. Hiệu quả của nó đến từ hai kỹ thuật tối ưu quan trọng: 'Union by Size/Rank' và 'Path Compression', giúp cây luôn nông và các hoạt động gần như là O(1).",
  "implementations": [
    {
      "name": "DSU with Path Compression and Union by Size",
      "language": "cpp",
      "code": "#include <vector>\\n#include <numeric>\\n\\nstruct DSU {\\n    std::vector<int> parent;\\n    std::vector<int> sz;\\n    int components;\\n\\n    DSU(int n) {\\n        parent.resize(n + 1);\\n        std::iota(parent.begin(), parent.end(), 0);\\n        sz.assign(n + 1, 1);\\n        components = n;\\n    }\\n\\n    int find(int i) {\\n        if (parent[i] == i) return i;\\n        return parent[i] = find(parent[i]);\\n    }\\n\\n    void unite(int i, int j) {\\n        int root_i = find(i);\\n        int root_j = find(j);\\n        if (root_i != root_j) {\\n            if (sz[root_i] < sz[root_j]) std::swap(root_i, root_j);\\n            parent[root_j] = root_i;\\n            sz[root_i] += sz[root_j];\\n            components--;\\n        }\\n    }\\n};"
    }
  ],
  "common_pitfalls": [
    "Sử dụng chỉ số 0-based thay vì 1-based có thể gây nhầm lẫn nếu không cẩn thận khởi tạo mảng.",
    "Quên khởi tạo DSU, khiến mỗi phần tử không phải là gốc của chính nó ban đầu.",
    "Implment `find` mà không có 'Path Compression' sẽ làm giảm đáng kể hiệu suất."
  ],
  "example_problems": [
    {
      "id": "CSES Road Construction",
      "link": "https://cses.fi/problemset/task/1676",
      "description": "Bài toán yêu cầu xử lý một loạt các con đường mới được xây dựng và sau mỗi lần xây, báo cáo số lượng thành phần liên thông và kích thước của thành phần liên thông lớn nhất. Đây là ứng dụng trực tiếp của DSU: mỗi thành phố là một phần tử, mỗi con đường là một phép `unite`. Số thành phần liên thông và kích thước lớn nhất có thể được theo dõi dễ dàng.",
      "tags": ["connectivity", "dsu", "union-find", "components"],
      "variation": "Tracking component count and max size"
    }
  ]
}
```

#### **❗ Bước cuối cùng, Bắt buộc**

Sau khi bạn **thêm, sửa, hoặc xóa bất kỳ file `.json` nào** trong thư mục `data/algorithms/`, bạn **PHẢI** xây dựng lại cơ sở tri thức:

1.  Xóa thư mục `vectorstore/` hiện có.
2.  Chạy lệnh: `python rag_system.py`

AI của bạn sẽ không "học" được dữ liệu mới cho đến khi bạn thực hiện bước này.