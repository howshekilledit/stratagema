class Node {
    constructor(state, parent, action) {
        this.state = state;
        this.parent = parent;
        this.action = action;
    }
}

class StackFrontier {
    constructor() {
        this.frontier = [];
    }

    add(node) {
        // Add node to the stack (last in, first out)
        this.frontier.push(node);
    }

    containsState(state) {
        // Check if a state already exists in the frontier
        return this.frontier.some(node => node.state === state);
    }

    isEmpty() {
        // Check if the frontier is empty
        return this.frontier.length === 0;
    }

    remove() {
        // Remove the last node added (stack behavior)
        if (this.isEmpty()) {
            throw new Error("Empty frontier");
        } else {
            return this.frontier.pop();
        }
    }
}

class QueueFrontier extends StackFrontier {
    remove() {
        // Remove the first node added (queue behavior)
        if (this.isEmpty()) {
            throw new Error("Empty frontier");
        } else {
            return this.frontier.shift();
        }
    }
}

