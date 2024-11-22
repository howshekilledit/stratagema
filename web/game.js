// Include svg.js in your HTML file to run this script
// <script src="https://cdn.jsdelivr.net/npm/@svgdotjs/svg.js"></script>

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
	constructor(width = 2, height = 2, start = null) {
		this.width = width;
		this.height = height;
		this.player1 = "m";
		this.player2 = "c";
		if (!start) {
			this.grid = Array.from({ length: height }, () =>
				Array.from({ length: width }, () =>
					Math.random() < 0.5 ? "m" : "c"
				)
			);
			this.pos = new IntVector(
				Math.floor(Math.random() * width),
				Math.floor(Math.random() * height)
			);
			this.char = this.getVal(this.pos);

			if (new Set(this.grid.flat()).size === 1) {
				const { x, y } = this.pos;
				this.grid[y][x] = this.grid[y][x] === "m" ? "c" : "m";
			}
		} else {
			this.grid = start.map(row => [...row]);
			for (let y = 0; y < start.length; y++) {
				for (let x = 0; x < start[0].length; x++) {
					if (start[y][x] === start[y][x].toUpperCase()) {
						this.pos = new IntVector(x, y);
						this.char = start[y][x].toLowerCase();
						this.grid[y][x] = this.char;
					}
				}
			}
		}
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
	validMoves(pos) {
		// get color of pos
		const char = this.getVal(pos);
		let valid = [];
		for (const n of this.neighbors(pos)) {
			if(isDiagonal(pos, n)){
				if (this.getVal(n) !== char) { // spread moves must spread to other color
					valid.push(n);
				}
			} else {
				valid.push(n); // swap moves can be to any color
			}
		}
		return valid;
	}
	makeMove(pos) {
		// if move is not valid, return
		if (!this.validMoves(this.pos).some(n => n.x === pos.x && n.y === pos.y)) {
			return;
		} else { //
			// if diagonal move, spread player's color to pos
			// otherwise, swap colors
			if(isDiagonal(this.pos, pos) ){
				this.setVal(pos, this.char);
			} else {
				let swap_color = this.getVal(pos);
				this.setVal(pos, this.char);
				this.setVal(this.pos, swap_color);
			}
			this.pos = pos;
		}

	}
	terminal() {
		return new Set(this.grid.flat()).size === 1;
	}
	winner() {
		return this.grid.flat()[0];
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
				.attr({ x: x * cellSize, y: y * cellSize, fill: color, stroke: "none"})
				.data({ x, y })
				.click(() => handleCellClick(x, y, board, board_shapes, cellSize))
			// toggle white stroke on hover
				.mouseover(() => rect.attr({ stroke: "#fff", "stroke-width": 2 }))
				.mouseout(() => rect.attr({ stroke: "none" }));
			row.push(rect);
		}
		board_shapes.push(row);
	}
	// add invisible circle to board
	player = draw.circle(10).attr({ fill: "#f06" });
	// move player to board.pos
	player.move(board.pos.x * cellSize + cellSize / 2, board.pos.y * cellSize + cellSize / 2);
	board_shapes.push(player);

	return board_shapes;
}

function handleCellClick(x, y, board, board_shapes, cellSize) {	
	const clickedPos = new IntVector(x, y);

	// Check if the clicked cell is a neighbor of the player
	board.makeMove(clickedPos);
	// Redraw grid
	redrawGrid(board, board_shapes, cellSize);
	// hide player
	const player = board_shapes[board_shapes.length-1];
	player.attr({ fill: "#f06" });

}

function redrawGrid(board, board_shapes, cellSize) {
	for (let y = 0; y < board.height; y++) {
		for (let x = 0; x < board.width; x++) {
			const color = board.grid[y][x] === "m" ? "#FF00FF" : "#00FFFF";
			board_shapes[y][x].attr({ fill: color });
		}
	}
	// move player to board.pos
	const player = board_shapes[board_shapes.length-1];
	player.move(board.pos.x * cellSize + cellSize / 2, board.pos.y * cellSize + cellSize / 2);
	if (board.terminal()) {
		alert(`Winner is ${board.winner()}`);
	}
}

// Initialize the game
const board = new Board(2, 2); // Create a 4x4 grid
const draw = initializeSVG(board);

