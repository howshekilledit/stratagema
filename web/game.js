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
	this.pos_selected = False;
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
        if (x > 0) neighbors.push(new IntVector(x - 1, y));
        if (x < this.width - 1) neighbors.push(new IntVector(x + 1, y));
        if (y > 0) neighbors.push(new IntVector(x, y - 1));
        if (y < this.height - 1) neighbors.push(new IntVector(x, y + 1));
        if (x > 0 && y > 0) neighbors.push(new IntVector(x - 1, y - 1));
        if (x < this.width - 1 && y > 0) neighbors.push(new IntVector(x + 1, y - 1));
        if (x > 0 && y < this.height - 1) neighbors.push(new IntVector(x - 1, y + 1));
        if (x < this.width - 1 && y < this.height - 1) neighbors.push(new IntVector(x + 1, y + 1));
        return neighbors;
    }
    click(){
	// get position 
    }
}

function initializeSVG(board) {
    const draw = SVG().addTo("#game").size(400, 400);
    const cellSize = 400 / board.width;

    const rects = [];
    for (let y = 0; y < board.height; y++) {
        const row = [];
        for (let x = 0; x < board.width; x++) {
            const color = board.grid[y][x] === "m" ? "#FF00FF" : "#00FFFF";
            const rect = draw
                .rect(cellSize, cellSize)
                .attr({ x: x * cellSize, y: y * cellSize, fill: color, stroke: "#000", "stroke-width": 2 })
               .data({ x, y })
                .click(() => handleCellClick(x, y, board, rects, cellSize));
            row.push(rect);
        }
        rects.push(row);
    }
    return rects;
}

function handleCellClick(x, y, board, rects, cellSize) {
    const clickedPos = new IntVector(x, y);
	console.log(clickedPos);
    
	const isNeighbor = board.neighbors(board.pos).some(
        neighbor => neighbor.x === clickedPos.x && neighbor.y === clickedPos.y
    );

    if (isNeighbor) {
        const currentChar = board.getVal(board.pos);
        const clickedChar = board.getVal(clickedPos);

        // Swap values
        board.setVal(board.pos, clickedChar);
        board.setVal(clickedPos, currentChar);

        // Update the player position
        board.pos = clickedPos;

        // Redraw grid
        redrawGrid(board, rects, cellSize);
    }
}

function redrawGrid(board, rects, cellSize) {
    for (let y = 0; y < board.height; y++) {
        for (let x = 0; x < board.width; x++) {
            const color = board.grid[y][x] === "m" ? "#FF00FF" : "#00FFFF";
            rects[y][x].attr({ fill: color });
        }
    }
}

// Initialize the game
const board = new Board(4, 4); // Create a 4x4 grid
const rects = initializeSVG(board);
 
