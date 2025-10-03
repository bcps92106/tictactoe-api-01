import gradio as gr
import requests

API_URL = "http://127.0.0.1:8000"

# --- 包裝 API 呼叫 ---
def reset_board():
    res = requests.post(f"{API_URL}/reset").json()
    return render_board(res["board"]), f"遊戲已重置，輪到 {res['turn']}"

def player_move(player, action, pos, from_pos=None):
    payload = {"player": player, "action": action, "pos": pos, "from_pos": from_pos}
    res = requests.post(f"{API_URL}/game", json=payload).json()
    return render_board(res["board"]), f"{res['message']} | Winner: {res['winner']} | Turn: {res['turn']}"

def ai_move(player):
    res = requests.post(f"{API_URL}/ai_move", json={"player": player}).json()
    return render_board(res["board"]), f"AI: {res['msg']} | Winner: {res['winner']} | Turn: {res['turn']}"

def llm_decision(prompt):
    res = requests.post(f"{API_URL}/llm_move", json={"prompt": prompt}).json()
    decision = res["decision"]
    return str(decision), f"LLM 原始輸出: {res['raw']}"

# --- 簡單棋盤渲染 ---
def render_board(board_state):
    grid = ""
    for i, (pos, val) in enumerate(board_state.items()):
        cell = val if val else "⬜"
        grid += cell + (" | " if (i+1) % 3 else "\n")
    return grid

# --- Gradio 介面 ---
with gr.Blocks() as demo:
    gr.Markdown("## 🎮 Tic Tac Toe + AI Demo")

    board_display = gr.Textbox(label="棋盤狀態", interactive=False)
    status = gr.Textbox(label="訊息", interactive=False)

    with gr.Row():
        player = gr.Dropdown(["X", "O"], label="玩家")
        action = gr.Dropdown(["place", "move"], label="動作")
        pos = gr.Textbox(label="位置 (如 a1)")
        from_pos = gr.Textbox(label="移動起點 (僅 move 用)")

    with gr.Row():
        btn_move = gr.Button("玩家下棋")
        btn_ai = gr.Button("AI 下棋")
        btn_reset = gr.Button("重置棋盤")

    btn_move.click(player_move, inputs=[player, action, pos, from_pos], outputs=[board_display, status])
    btn_ai.click(ai_move, inputs=[player], outputs=[board_display, status])
    btn_reset.click(reset_board, outputs=[board_display, status])

    gr.Markdown("### 🤖 LLM 輔助決策")
    llm_prompt = gr.Textbox(label="輸入自然語言指令")
    llm_decision_box = gr.Textbox(label="LLM 決策")
    llm_raw_box = gr.Textbox(label="原始回應")
    btn_llm = gr.Button("讓 LLM 決定")

    btn_llm.click(llm_decision, inputs=[llm_prompt], outputs=[llm_decision_box, llm_raw_box])

demo.launch()