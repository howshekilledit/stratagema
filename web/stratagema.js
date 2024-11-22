class IntVector {
    constructor(x, y) {
        this.x = x;
        this.y = y;
    }
}

function setVal(vec, val, grid) {
    const { x, y } = vec;
    const newGrid = grid.map(row => [...row]);
    newGrid[y][x] = val;
    return newGrid;
}

function isDiagonal(pos1, pos2) {
    return Math.abs(pos1.x - pos2.x) + Math.abs(pos1.y - pos2.y) === 2;
}

class Board {
    constructor(width = 2, height = 2, start = null) {
        console.log("Creating board");
        this.width = width;
        this.height = height;

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

            if (new Set(this.grid.flat()).size == 1) {
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

        this.goal = Array.from({ length: height }, () =>
            Array.from({ length: width }, () => this.char)
        );
        this.state = this.stringState();
    }

    stringState(grid = null, pos = null, consoleOutput = false) {
        if (!grid) grid = this.grid;
        if (!pos) pos = this.pos;

        const printGrid = grid.map(row => [...row]);
        printGrid[pos.y][pos.x] = this.char.toUpperCase();

        const stateString = printGrid.map(row => row.join("")).join("\n");

        if (consoleOutput) console.log(stateString);

        return stateString;
    }

    getGrid(state = null) {
        if (!state) state = this.state;
        return state
            .toLowerCase()
            .split("\n")
            .map(row => row.split(""));
    }

    terminal(grid = null) {
        if (!grid) grid = this.grid;
        return new Set(grid.flat()).size === 1;
    }

    neighbors(pos = null) {
        if (!pos) pos = this.pos;
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

    getVal(vec, grid = null) {
        if (!grid) grid = this.grid;
        const { x, y } = vec;
        return grid[y][x];
    }

    makeRandomMove(parent) {
        const moves = this.moves(parent);
        const move = moves[Math.floor(Math.random() * moves.length)];

        this.state = move.state;
        this.pos = move.action;
        this.grid = this.getGrid();
        return move;
    }

    moves(parent) {
        const pos = parent.action;
        const grid = this.getGrid(parent.state);
        const moves = [];

        for (const neighbor of this.neighbors(pos)) {
            let state = null;
            const neighborVal = this.getVal(neighbor, grid);
            const playerVal = this.getVal(pos, grid);

            if (!isDiagonal(pos, neighbor)) {
                state = setVal(neighbor, playerVal, grid);
                state = setVal(pos, neighborVal, state);
            } else if (neighborVal !== playerVal) {
                state = setVal(neighbor, playerVal, grid);
            }

            if (state) {
                const action = isDiagonal(pos, neighbor) ? pos : neighbor;
                moves.push({ state: this.stringState(state, action), action });
            }
        }
        return moves;
    }
	
	//minimax impletemnation


}

