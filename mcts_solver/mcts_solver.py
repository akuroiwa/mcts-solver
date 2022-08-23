from mcts import mcts, treeNode

class AntLionTreeNode(treeNode):

    def __init__(self, state, parent):
        super().__init__(state, parent)
        self.value = None

class AntLionMcts(mcts):

    def __init__(self, timeLimit=None, iterationLimit=None):
        super().__init__(timeLimit, iterationLimit)
        self.dl = False
        self.regression = False

    def dl_method(self, bestChild):
        '''Rewards output by deep learning that you can override.
        '''
        pass

    def mctsSolver(self, node):
        '''This is based on pseudocode from the following paper:
        `Winands, Mark & Björnsson, Yngvi & Saito, Jahn-Takeshi. (2008). Monte-Carlo Tree Search Solver. 25-36. 10.1007/978-3-540-87608-3_3.
        <https://www.researchgate.net/publication/220962507_Monte-Carlo_Tree_Search_Solver>`__
        '''
        if node.isTerminal:
            if  node.state.getReward() == 1:
                node.value = float("inf")
            elif node.state.getReward() == -1:
                node.value = float("-inf")
            else:
                return 0

        bestChild = node

        if bestChild.value != float("-inf") and bestChild.value != float("inf"):
            if bestChild.numVisits == 0:
                if self.dl:
                    reward = self.dl_method(bestChild)
                else:
                    reward = bestChild.state.getCurrentPlayer() * -self.rollout(bestChild.state)
                reward = bestChild.state.getCurrentPlayer() * -self.rollout(bestChild.state)
                return reward
            else:
                reward = -self.mctsSolver(bestChild)
        else:
            reward = bestChild.value

        if reward == float("inf"):
            node.parent.value = float("-inf")
            return reward
        else:
            if reward == float("-inf"):
                for child in node.parent.children.values():
                    try:
                        if child.value != reward:
                            reward = -1
                            return reward
                    except:
                        node.parent.value = float("inf")
                        return reward
        return reward

    def selectNode_num(self, node, explorationConstant):
        while not node.isTerminal:
            if node.isFullyExpanded:
                node = self.getBestChild(node, explorationConstant)
            else:
                return self.expand(node)
        return node

    def expand(self, node):
        actions = node.state.getPossibleActions()
        for action in actions:
            if action not in node.children:
                newNode = AntLionTreeNode(node.state.takeAction(action), node)
                node.children[action] = newNode
                if len(actions) == len(node.children):
                    node.isFullyExpanded = True
                return newNode

        raise Exception("Should never reach here")

    def search(self, initialState, needDetails=False):
        self.root = AntLionTreeNode(initialState, None)

        if self.limitType == 'time':
            timeLimit = time.time() + self.timeLimit / 1000
            while time.time() < timeLimit:
                self.executeRound()
        else:
            for i in range(self.searchLimit):
                self.executeRound()

        bestChild = self.getBestChild(self.root, 0)
        action=(action for action, node in self.root.children.items() if node is bestChild).__next__()
        if needDetails:
            return {"action": action, "expectedReward": bestChild.totalReward / bestChild.numVisits}
        else:
            return action

    def executeRound(self):
        """
            execute a selection-expansion-simulation-backpropagation round
        """
        node = self.selectNode(self.root)
        # reward = self.rollout(node.state)
        reward = self.mctsSolver(node)
        self.backpropogate(node, reward)
