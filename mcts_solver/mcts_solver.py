from mcts import mcts, treeNode
import multiprocessing
from multiprocessing import Lock

class AntLionTreeNode(treeNode):

    def __init__(self, state, parent):
        super().__init__(state, parent)
        self.value = None

class AntLionMcts(mcts):

    def __init__(self, timeLimit=None, iterationLimit=None):
        super().__init__(timeLimit, iterationLimit)
        self.dl = False
        self.regression = False
        self.lock = Lock()

    def dl_method(self, state):
        '''Rewards output by deep learning that you can override.
        '''
        pass

    def mctsSolver(self, node):
        '''This is based on pseudocode from the following paper:
        `Winands, Mark & Björnsson, Yngvi & Saito, Jahn-Takeshi. (2008). Monte-Carlo Tree Search Solver. 25-36. 10.1007/978-3-540-87608-3_3.
        <https://www.researchgate.net/publication/220962507_Monte-Carlo_Tree_Search_Solver>`__
        Parallel processing is possible thanks to OpenAI's ChatGPT advice.
        '''
        with self.lock:
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
                        reward = self.dl_method(bestChild.state)
                    else:
                        reward = bestChild.state.getCurrentPlayer() * -self.rollout(bestChild.state)

                        # with self.lock:
                        #     reward = bestChild.state.getCurrentPlayer() * -self.rollout(bestChild.state)

                        # with multiprocessing.Pool() as pool:
                        #     num_processes = multiprocessing.cpu_count()
                        #     multiple_results = [pool.apply_async(self.rollout, args=(bestChild.state,)) for i in range(num_processes)]
                        #     pool.close()
                        #     pool.join()
                        #     results = [res for res in multiple_results if res.ready() and res.successful()]
                        #     if results:
                        #         # reward = bestChild.state.getCurrentPlayer() * max([-res.get() for res in results])
                        #         reward = bestChild.state.getCurrentPlayer() * min([-res.get() for res in results])
                        #     else:
                        #         reward = 0
                    return reward
                else:
                    # with multiprocessing.Pool() as pool:
                    #     m = pool.apply_async(self.mctsSolver, args=(bestChild,))
                    #     reward = -m.get()

                    # with self.lock:
                    #     reward = -self.mctsSolver(bestChild)

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
        '''Parallel processing is possible thanks to Google Bard and OpenAI's ChatGPT advice.
        '''
        with self.lock:
            while not node.isTerminal:
                if node.isFullyExpanded:
                    node = self.getBestChild(node, explorationConstant)

                    # with self.lock:
                    #     node = self.getBestChild(node, explorationConstant)
                else:
                    return self.expand(node)

                    # with self.lock:
                    #     return self.expand(node)
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
