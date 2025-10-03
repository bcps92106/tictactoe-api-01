# tictactoe-api  
A TicTacToe API built with FastAPI, supporting two-player mode with place and move rules, plus reset feature.  
一個基於 FastAPI 實作的井字棋 API，支援雙人模式，具備下子與移子規則，以及重置功能。  

This project provides a RESTful API to play an extended version of TicTacToe, allowing two players to place and move pieces on the board, with a reset option to start a new game.  
本專案提供一個 RESTful API，讓使用者可以進行擴展版的井字棋遊戲，支援雙人下子與移子，並提供重置功能重新開始遊戲。  

# 🎮 TicTacToe API  
A two-player game implemented with **FastAPI**, supporting placing and moving pieces, along with **pytest unit tests**.  
一個基於 **FastAPI** 實作的雙人對弈遊戲（井字棋擴展版），支援下子與移動棋子的規則，並搭配 **pytest 單元測試**。  

This project serves as a demonstration for backend API design, game rule engine construction, and test development, with potential for integration of voice/LLM natural language commands.  
此專案可作為 **後端 API 設計、遊戲規則引擎建構、測試開發** 的示範，同時具備進一步整合 **語音/LLM 自然語言指令** 的潛力。  

---  

## 🚀 功能特色  
Features and Highlights  
功能與特色  

- FastAPI 提供 `/game` 與 `/reset` 介面  
  FastAPI provides `/game` and `/reset` endpoints  
- 棋盤狀態以 JSON 方式回傳  
  Board status returned in JSON format  
- 支援 **place**（下子）與 **move**（移子）兩種動作  
  Supports **place** (placing a piece) and **move** (moving a piece) actions  
- 雙人對弈，支援回合控制  
  Two-player gameplay with turn control  
- 單元測試覆蓋主要遊戲邏輯（pytest）  
  Unit tests covering main game logic using pytest  

---  

## 📦 安裝與執行  
Installation and Running Instructions  
安裝與執行說明  

### 1. 建立虛擬環境  
Create a virtual environment  
建立 Python 虛擬環境  

```bash  
python -m venv .venv  
source .venv/bin/activate   # Mac/Linux  
.venv\Scripts\activate      # Windows  
```  

### 2. 安裝依賴  
Install dependencies  
安裝依賴  

```bash  
pip install -r requirements.txt  
```  

### 3. 啟動伺服器  
Run the API server  
啟動 API 伺服器  

```bash  
uvicorn main:app --reload  
```  

### 4. 執行測試  
Run tests  
執行測試  

```bash  
pytest  
```