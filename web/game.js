class IntVector {
	constructor(x, y) {
		this.x = x;
		this.y = y;
	}
}

function isDiagonal(pos1, pos2) {
	return Math.abs(pos1.x - pos2.x) + Math.abs(pos1.y - pos2.y) === 2;
}

class Board {
	constructor(width = 3, height = 3, start = null, currentPlayer = 1) {
		this.width = width;
		this.height = height;
		this.player1 = "c"; // Player 1: Cyan
		this.player2 = "m"; // Player 2: Magenta

		if (!start) {
			this.grid = Array.from({ length: height }, () =>
				Array.from({ length: width }, () =>
					Math.random() < 0.5 ? "m" : "c"
				)
			);
			// chose any cyan cell as player 1
			// get all cells with value c
			const cCells = [];
			for (let y = 0; y < height; y++) {
				for (let x = 0; x < width; x++) {
					if (this.grid[y][x] === "c") {
						cCells.push(new IntVector(x, y));
					}
				}
			}
			this.pos1 = cCells[Math.floor(Math.random() * cCells.length)];
			// chose any magenta cell as player 2
			// get all cells with value m
			const mCells = [];
			for (let y = 0; y < height; y++) {
				for (let x = 0; x < width; x++) {
					if (this.grid[y][x] === "m") {
						mCells.push(new IntVector(x, y));
					}
				}
			}
			this.pos2 = mCells[Math.floor(Math.random() * mCells.length)];

			
		

			// Ensure there is at least one difference in grid
			if (new Set(this.grid.flat()).size === 1) {
				const { x, y } = this.pos1;
				this.grid[y][x] = this.grid[y][x] === "m" ? "c" : "m";
			}
		} else {
			//decode start from string state
			this.grid = start.split("\n").map(row => row.split(""));
			//get capital letters from grid and assign to pos1 and pos2
			for (let y = 0; y < height; y++) {
				for (let x = 0; x < width; x++) {
					if (this.grid[y][x] === "C") {
						this.pos1 = new IntVector(x, y);
						// lower case in grid
							
					}
					if (this.grid[y][x] === "M") {
						this.pos2 = new IntVector(x, y);
						// lower case in grid
					}
				}
			}

		}
		// lowercase all cells in grid
		for (let y = 0; y < height; y++) {
			for (let x = 0; x < width; x++) {
				this.grid[y][x] = this.grid[y][x].toLowerCase();
			}
		}
		this.char1 = this.getVal(this.pos1);
		this.char2 = this.getVal(this.pos2);
		this.currentPlayer = currentPlayer; // 1 for Player 1, 2 for Player 2
	}

	getVal(vec) {
		const { x, y } = vec;
		return this.grid[y][x];
	}

	setVal(vec, val) {
		const { x, y } = vec;
		this.grid[y][x] = val;
	}

	neighbors(pos) {
		const { x, y } = pos;
		const neighbors = [];
		if (x > 0 && y > 0) neighbors.push(new IntVector(x - 1, y - 1));
		if (x < this.width - 1 && y > 0) neighbors.push(new IntVector(x + 1, y - 1));
		if (x > 0 && y < this.height - 1) neighbors.push(new IntVector(x - 1, y + 1));
		if (x < this.width - 1 && y < this.height - 1) neighbors.push(new IntVector(x + 1, y + 1));

		if (x > 0) neighbors.push(new IntVector(x - 1, y));
		if (x < this.width - 1) neighbors.push(new IntVector(x + 1, y));
		if (y > 0) neighbors.push(new IntVector(x, y - 1));
		if (y < this.height - 1) neighbors.push(new IntVector(x, y + 1));
		return neighbors;
	}

	validMoves(pos, char) {
		let valid = [];
		for (const n of this.neighbors(pos)) {
			// check that other player isn't there and it's not the current position
			//if (!(n.x === this.pos1.x & n.y === this.pos1.y) & !(n.x === this.pos2.x & n.y === this.pos2.y)) {
				if (isDiagonal(pos, n)) {
					if (this.getVal(n).toLowerCase() !== char.toLowerCase()) {
						valid.push(n);
					}
				} else {
					valid.push(n);
				}
			//}
		}
		return valid;
	}

	makeMove(pos, player) {
		const currentPos = player === 1 ? this.pos1 : this.pos2;
		const currentChar = player === 1 ? this.char1 : this.char2;
		if (!this.validMoves(currentPos, currentChar).some(n => n.x === pos.x && n.y === pos.y)) {
			return false; // Invalid move
		}

		if (isDiagonal(currentPos, pos)) {
			this.setVal(pos, currentChar);
		} else {
			let swap_color = this.getVal(pos);
			this.setVal(pos, currentChar);
			this.setVal(currentPos, swap_color);
		}

		if (player === 1) {
			this.pos1 = pos;
			if(this.pos1.x === this.pos2.x && this.pos1.y === this.pos2.y){
			// if currentPos color is player 2 color
				if (this.getVal(currentPos) === this.char2) {
					this.pos2 = currentPos; //swap if swap move 
				} else {
					// if spread move, move other player to any square that is their color
					//move player 2 to any square that is their oolor
					const mCells = [];
					for (let y = 0; y < this.height; y++) {
						for (let x = 0; x < this.width; x++) {
							if (this.grid[y][x].toLowerCase() === "m") {
								mCells.push(new IntVector(x, y));
							}
						}
					}
					this.pos2 = mCells[Math.floor(Math.random() * mCells.length)];
				}
			}
		} else {
			this.pos2 = pos;
			if(this.pos1.x === this.pos2.x && this.pos1.y === this.pos2.y){
			// if currentPos color is player 1 color
				if (this.getVal(currentPos) === this.char1) {
					this.pos1 = currentPos;
				} else {
					//move player 1 to any square that is their color
					const cCells = [];
					for (let y = 0; y < this.height; y++) {
						for (let x = 0; x < this.width; x++) {
							if (this.grid[y][x].toLowerCase() === "c") {
								cCells.push(new IntVector(x, y));
							}
						}
					}
					this.pos1 = cCells[Math.floor(Math.random() * cCells.length)];
				}

			}
		}
		return true;
	}
	switchPlayer() {
		this.currentPlayer = this.currentPlayer === 1 ? 2 : 1;
	}
	terminal() {
		// lowercase grid
		let grid = this.grid.map(row => row.map(cell => cell.toLowerCase()));
		return new Set(grid.flat()).size === 1;
	}

	winner() {
		return this.grid.flat()[0];
	}
	result(grid, move) {
		// Returns the board state after applying the move
		const newBoard = new Board(this.width, this.height, grid, this.currentPlayer);
		newBoard.makeMove(move, this.currentPlayer);
		return newBoard;
	}
	evaluate(grid = this.grid) {
		// Evaluation logic for the board state
		const player1Score = grid.flat().filter(c => c === "c").length;
		const player2Score = grid.flat().filter(c => c === "m").length;
		return player2Score - player1Score;
	}
	stringState() {
		// capitalize playe rpositions
		const grid = this.grid;
		grid[this.pos1.y][this.pos1.x] = "C";
		grid[this.pos2.y][this.pos2.x] = "M";
		return grid.map(row => row.join("")).join("\n");
	}
	minimax(depth, alpha, beta, grid, isMaximizing) {
		if (depth === 0 || this.terminal()) {
			return this.evaluate();
		}

		if (isMaximizing) {
			let maxEval = -Infinity;
			for (const move of this.validMoves(this.pos2, this.char2)) {
				let result = this.result(this.stringState(), move);
				const evaluation = this.minimax(depth - 1, alpha, beta, result, false);
				maxEval = Math.max(maxEval, evaluation);
				alpha = Math.max(alpha, evaluation);
				if (beta <= alpha) break;

			}
			return maxEval;
		} else {
			let minEval = Infinity;
			for (const move of this.validMoves(this.pos1, this.char1)) {
				let result = this.result(this.stringState(), move);
				const evaluation = this.minimax(depth - 1, alpha, beta, result, true);
				minEval = Math.min(minEval, evaluation);
				beta = Math.min(beta, evaluation);
				if (beta <= alpha) break;
			}
			return minEval;
		}
	}

	findBestMove() {
		let bestEval = -Infinity;
		let bestMove = null;
		for (const move of this.validMoves(this.pos2, this.char2)) {
			const evaluation = this.minimax(3, -Infinity, Infinity, this.grid, true);
			if (evaluation > bestEval) {
				bestEval = evaluation;
				bestMove = move;
			}
		}
		return bestMove;
	}


}


function initializeSVG(board) {
	const draw = SVG().addTo("#game").size(400, 400);
	const cellSize = 400 / board.width;

	const board_shapes = [];
	for (let y = 0; y < board.height; y++) {
		const row = [];
		for (let x = 0; x < board.width; x++) {
			const color = board.grid[y][x] === "m" ? "#FF00FF" : "#00FFFF";
			const rect = draw
				.rect(cellSize, cellSize)
				.attr({ x: x * cellSize, y: y * cellSize, fill: color, stroke: "none" })
				.data({ x, y })
				.click(() => handleCellClick(x, y, board, board_shapes, cellSize))
				.mouseover(() => rect.attr({ stroke: "#fff", "stroke-width": 2 }))
				.mouseout(() => rect.attr({ stroke: "none" }));
			row.push(rect);
		}
		board_shapes.push(row);
	}
	let player1 = draw.circle(10).attr({ fill: "#f06" });
	player1.move(board.pos1.x * cellSize + cellSize / 2, board.pos1.y * cellSize + cellSize / 2);
	board_shapes.push(player1);

	let player2 = draw.circle(10).attr({ fill: "#000" });
	player2.move(board.pos2.x * cellSize + cellSize / 2, board.pos2.y * cellSize + cellSize / 2);
	board_shapes.push(player2);

	return board_shapes;
}

function handleCellClick(x, y, board, board_shapes, cellSize) {
	const clickedPos = new IntVector(x, y);

	if (board.currentPlayer === 1) {
		board.makeMove(clickedPos, 1);
		redrawGrid(board, board_shapes, cellSize);
	}
	// check fo rwinner
	if (board.terminal()) {
		alert(`Winner is ${board.winner()}`);
	}
}

function redrawGrid(board, board_shapes, cellSize) {
	for (let y = 0; y < board.height; y++) {
		for (let x = 0; x < board.width; x++) {
			const color = (board.grid[y][x] === "m" | board.grid[y][x] === 'M') ? "#FF00FF" : "#00FFFF";
			board_shapes[y][x].attr({ fill: color });
		}
	}
	if (board.terminal()) {
		alert(`Winner is ${board.winner()}`);
	
	} else {

		// Update positions of Player 1 and Player 2
		const player1 = board_shapes[board_shapes.length - 2];
		const player2 = board_shapes[board_shapes.length - 1];

		player1.move(board.pos1.x * cellSize + cellSize / 2, board.pos1.y * cellSize + cellSize / 2);
		player2.move(board.pos2.x * cellSize + cellSize / 2, board.pos2.y * cellSize + cellSize / 2);
	}

	}

board = new Board(3, 3);
board_shapes = initializeSVG(board);

// create an indicator with whose turn it is
let turnIndicator = document.createElement("div");
turnIndicator.innerHTML = "Player 1's turn";
document.body.appendChild(turnIndicator);
// turnIndicator is cyan
turnIndicator.style.color = "#00FFFF";
// turn Indicator stuck to top left
turnIndicator.style.position = "absolute";
turnIndicator.style.top = "0";
turnIndicator.style.left = "0"

let play = setInterval(() => {
	if (board.currentPlayer === 2) {
		// player 2 keeps making moves for three seconds
		let i = 0;
		let ai_plays = setInterval(() => {
			const bestMove = board.findBestMove();
			board.makeMove(bestMove, 2);
			redrawGrid(board, board_shapes, 400 / board.width);
			if (board.terminal()) {
				clearInterval(ai_plays);
				clearInterval(play);
			}
			i++;
			if (i === 2) {
				clearInterval(ai_plays);
			}
			
		}, 500);
		setTimeout(() => {
			turnIndicator.innerHTML = "Player 1's turn";
			turnIndicator.style.color = "#00FFFF";
		
			board.switchPlayer();
					}, 1500);
	} else {
		setTimeout(() => {
		turnIndicator.innerHTML = "Player 2's turn";
		turnIndicator.style.color = "#FF00FF";
		board.switchPlayer();
		if (board.terminal()) {
			clearInterval(play);
		}
		}, 1800);
	}
}, 4000); 
