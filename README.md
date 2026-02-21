WOFA – Workflow Automation IDE
整合積累經驗，提升企業智慧
Integrate & Accumulate Experiences, Elevate Corporation Intelligence

https://img.shields.io/badge/license-MIT-blue.svg

https://img.shields.io/badge/python-3.8%252B-blue

中文版
📖 簡介
WOFA 是一套專為人工智慧程式設計師打造的工作流程自動化工具。透過直觀的圖形化介面，您可以快速構建融合了最新 AI 技術的複雜商業或工業流程。WOFA 不僅整合了常用的 AI 模型（如 LLM、OCR、語音識別、圖像生成），還提供了邏輯控制、程式碼執行以及多種輸入/輸出節點，讓您能夠將業務智慧沉澱到自動化流程中，大幅減少人為錯誤並提升效率。

WOFA 提供桌面整合開發環境 (IDE) 和伺服器運行時版本，可與現有 ERP 系統無縫整合，部署簡單，無需依賴 Docker 等複雜工具。

✨ 主要特色
視覺化工作流設計 – 拖放式節點編排，即時調整連線位置，支援多層嵌套迴圈。

豐富的節點模組

邏輯節點：分支、迴圈、Python 程式碼執行、結束節點。

AI 模型節點：詢問 LLM、LLM 分類、知識庫檢索、OCR、語音辨識、文字生成圖片、檔案翻譯。

輸入/輸出節點：HTTP 請求、FTP 上傳、發送/接收郵件。

內建除錯功能 – 支援單步執行、單節點執行，方便流程驗證。

知識庫管理 – 支援 chunk 與 QA_pair 兩種儲存類型，可將文件、問答對向量化，供後續查詢。

多 LLM 整合 – 可同時呼叫多個 LLM 並彙總結果，支援常用 LLM API 參數儲存與複用。

變數共享機制 – 所有節點透過專案變數表交換資料，符合程式設計直覺。

彈性部署 – 提供 Windows IDE 安裝程式，另有伺服器版本可與企業系統整合。

🚀 快速開始
系統需求
Windows 7/10/11

Python 3.8+ （若需自訂程式碼節點）

安裝
下載安裝程式 wofa_ide_win_installer.exe 從 Releases 頁面。

雙擊執行，依指示完成安裝。

安裝後會在 C:\Users\{用戶名}\AppData\Roaming\WOFA_IDE 目錄下產生 wofa_ide_win.exe 及 languages.xlsx。

第一個流程
開啟 WOFA IDE，點擊「新增」建立專案。

從左側面板拖曳「詢問 LLM」節點至畫布。

在右側編輯區設定 LLM API（可從「設定」預先儲存常用 API）。

連接「開始」節點與「詢問 LLM」節點，再連接至「結束」節點。

點擊「執行」按鈕，查看 LLM 回應結果。

詳細操作請參閱 使用手冊。

🧩 節點一覽
邏輯：分支、循環、Python 執行器、結束

AI 模型：詢問 LLM、LLM 分類、知識檢索、OCR、語音辨識、文字生圖、檔案翻譯

I/O：HTTP 請求、FTP 上傳、發送郵件、接收郵件

🤝 貢獻
歡迎提交 Issue 或 Pull Request。如有任何建議，可來信聯絡： syntak.tw@msa.hinet.net

📄 授權
本專案採用 MIT 授權條款，詳見 LICENSE 文件。

English Version
📖 Introduction
WOFA is a workflow automation IDE tailored for AI programmers. With its intuitive graphical interface, you can rapidly build complex business or industrial processes that incorporate cutting-edge AI technologies. WOFA integrates commonly used AI modules (LLM, OCR, speech recognition, image generation) along with logic control, code execution, and various I/O nodes, allowing you to embed business intelligence into automated workflows—significantly reducing human errors and boosting efficiency.

WOFA offers both a desktop IDE and a server runtime version, enabling seamless integration with existing ERP systems. Deployment is straightforward and does not require Docker or similar tools.

✨ Key Features
Visual Workflow Design – Drag-and-drop node orchestration, real-time connection adjustment, and support for nested loops.

Rich Node Modules

Logic Nodes: Branch, Iteration, Python Executor, End.

AI Model Nodes: Ask LLM, Categorize by LLM, Knowledge Retriever, OCR, Voice Recognize, Generate Image from Text, File Translation.

I/O Nodes: HTTP Request, FTP Upload, Send/Receive Email.

Built-in Debugger – Step-by-step or single-node execution for easy validation.

Knowledge Base Management – Supports chunk and QA_pair storage; vectorize documents or Q&A pairs for semantic retrieval.

Multi‑LLM Integration – Invoke multiple LLMs simultaneously and summarize results; save and reuse common LLM API settings.

Shared Variable Mechanism – All nodes exchange data via a project variable table, aligning with programmer intuition.

Flexible Deployment – Windows IDE installer available; server version for enterprise integration.

🚀 Quick Start
System Requirements
Windows 7/10/11

Python 3.8+ (if you plan to use custom code nodes)

Installation
Download the installer wofa_ide_win_installer.exe from the Releases page.

Double‑click and follow the installation wizard.

After installation, the files wofa_ide_win.exe and languages.xlsx will be located in C:\Users\{username}\AppData\Roaming\WOFA_IDE.

Your First Workflow
Launch WOFA IDE and click New to create a project.

Drag an Ask LLM node from the left palette onto the canvas.

In the right editor panel, configure the LLM API (you can pre‑save common APIs under Settings).

Connect the Start node to the Ask LLM node, then to an End node.

Click Run and observe the LLM response.

For detailed instructions, refer to the User Manual.

🧩 Node Overview
Logic: Branch, Iteration, Python Executor, End

AI Models: Ask LLM, Categorize by LLM, Knowledge Retriever, OCR, Voice Recognize, Generate Image from Text, File Translation

I/O: HTTP Request, FTP Upload, Send Email, Receive Email

🤝 Contributing
Issues and pull requests are welcome. For any questions or suggestions, feel free to contact us at syntak.tw@msa.hinet.net.

📄 License
This project is licensed under the MIT License – see the LICENSE file for details.
