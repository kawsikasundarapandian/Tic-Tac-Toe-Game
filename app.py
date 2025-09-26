from IPython.display import HTML, display

html = """
<div id="ttt_root" style="font-family: Arial, sans-serif; max-width:300px;">
  <h3 style="margin:6px 0 8px 0; text-align:center;">Tic-Tac-Toe</h3>
  <div id="status" style="text-align:center; margin-bottom:8px; font-weight:600;">Player X's turn</div>

  <div id="board" style="display:grid; grid-template-columns: repeat(3, 1fr); gap:6px;">
    <button class="cell" data-i="0"></button>
    <button class="cell" data-i="1"></button>
    <button class="cell" data-i="2"></button>
    <button class="cell" data-i="3"></button>
    <button class="cell" data-i="4"></button>
    <button class="cell" data-i="5"></button>
    <button class="cell" data-i="6"></button>
    <button class="cell" data-i="7"></button>
    <button class="cell" data-i="8"></button>
  </div>

  <div style="display:flex; justify-content:space-between; margin-top:10px;">
    <button id="reset" style="flex:1; padding:8px; margin-right:6px; cursor:pointer;">Reset</button>
    <button id="suggest" style="flex:1; padding:8px; margin-left:6px; cursor:pointer;">Suggest Move</button>
  </div>
  <div style="font-size:12px; color:#666; margin-top:8px; text-align:center;">Two-player local game. Click a cell to place X or O.</div>
</div>

<style>
  #ttt_root .cell {
    width: 100%;
    height: 80px;
    font-size: 40px;
    font-weight:700;
    border: 2px solid #444;
    background: #fff;
    cursor: pointer;
    outline: none;
    border-radius: 8px;
  }
  #ttt_root .cell:hover { background:#f7f7f7; }
  #ttt_root .cell.disabled { cursor: default; opacity: 0.85; }
  #ttt_root button { border-radius:8px; }
</style>

<script>
(function(){
  const root = document.getElementById('ttt_root');
  const cells = Array.from(root.querySelectorAll('.cell'));
  const status = root.querySelector('#status');
  const resetBtn = root.querySelector('#reset');
  const suggestBtn = root.querySelector('#suggest');

  let board = Array(9).fill('');
  let current = 'X';
  let gameOver = false;

  const wins = [
    [0,1,2],[3,4,5],[6,7,8],
    [0,3,6],[1,4,7],[2,5,8],
    [0,4,8],[2,4,6]
  ];

  function checkWinner(arr){
    for (const [a,b,c] of wins){
      if (arr[a] && arr[a] === arr[b] && arr[a] === arr[c]) return arr[a];
    }
    if (arr.every(x => x !== '')) return 'Draw';
    return null;
  }

  function render(){
    cells.forEach((cell,i) => {
      cell.textContent = board[i];
      if (board[i]) {
        cell.classList.add('disabled');
      } else {
        cell.classList.remove('disabled');
      }
    });
  }

  cells.forEach((cell, i) => {
    cell.addEventListener('click', () => {
      if (gameOver) return;
      if (board[i]) return;

      board[i] = current;
      const result = checkWinner(board);
      if (result){
        gameOver = true;
        if (result === 'Draw') status.textContent = "It's a draw!";
        else status.textContent = `Winner: ${result}`;
      } else {
        current = (current === 'X') ? 'O' : 'X';
        status.textContent = `Player ${current}'s turn`;
      }
      render();
    });
  });

  resetBtn.addEventListener('click', () => {
    board = Array(9).fill('');
    current = 'X';
    gameOver = false;
    status.textContent = "Player X's turn";
    render();
  });

  // Very small helper: suggest a non-losing/random move (not a full AI).
  suggestBtn.addEventListener('click', () => {
    if (gameOver) return;
    // Try to find a winning move for current
    for (let i=0;i<9;i++){
      if (!board[i]){
        let copy = board.slice(); copy[i] = current;
        if (checkWinner(copy) === current){
          status.textContent = `Suggested: place at ${i+1} (winning)`;
          return;
        }
      }
    }
    // Block opponent's winning move
    const opponent = current === 'X' ? 'O' : 'X';
    for (let i=0;i<9;i++){
      if (!board[i]){
        let copy = board.slice(); copy[i] = opponent;
        if (checkWinner(copy) === opponent){
          status.textContent = `Suggested: place at ${i+1} (block)`;
          return;
        }
      }
    }
    // Otherwise pick first empty
    const idx = board.findIndex(x => !x);
    if (idx >= 0) status.textContent = `Suggested: place at ${idx+1}`;
    else status.textContent = "No moves left!";
  });

  // initial render
  render();
})();
</script>
"""

display(HTML(html))
