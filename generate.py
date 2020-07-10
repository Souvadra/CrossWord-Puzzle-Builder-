import sys
from crossword import *
import queue 
from random import randint

class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            if word != set(): word = word.pop() 
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        keys = list(self.domains.keys())
        for i in range(0,len(keys)):
            if self.domains.get(keys[i]) == set():
                return None 
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        var = list(self.domains.keys())
        for i in range(0,len(var)):
            l = var[i].length
            List = list(self.domains.get(var[i]))
            remv = []
            for j in range(0, len(List)):
                if len(List[j]) != l:
                    remv.append(List[j])
            for j in range(0,len(remv)):
                List.remove(remv[j])
            tmp = {var[i]:set(List)}
            self.domains.update(tmp)
        #raise NotImplementedError

    def revise(self, x, y, Domains):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        x_words = list(Domains.get(x))
        y_words = set(Domains.get(y))
        y_word_list = list(y_words)
        remove_x_words = []
        collision = self.crossword.overlaps[x, y]
        if collision == None:
            return False 
        else:
            collision = list({collision})
            index_y = []
            for i in range(0,len(collision)):
                index_y.append(collision[i][1])

            index_x = []
            for i in range(0,len(collision)):
                index_x.append(collision[i][0])

            for i in range(0,len(x_words)):
                found = False 
                l1 = []
                word1 = x_words[i]
                for k in range(0,len(index_x)):
                    l1.append(word1[index_x[k]])
                for j in range(0,len(y_word_list)):
                    l2 = []
                    word2 = y_word_list[j]
                    for kk in range(0,len(index_y)):
                        l2.append(word2[index_y[kk]])
                    if (word1 != word2) and (l1 == l2):
                        found = True 
                if found == False:
                    remove_x_words.append(word1)

            if remove_x_words == []:
                return False 
            else:
                for i in range(0,len(remove_x_words)):
                    x_words.remove(remove_x_words[i])
                tmp = {x:set(x_words)}
                Domains.update(tmp)
                return True 
        raise NotImplementedError

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        Arc = queue.Queue()
        Domains = self.domains.copy()
        if arcs == None:
            var = list(Domains.keys())
            for i in range(0,len(var)):
                ngbr = list(self.crossword.neighbors(var[i]))
                for j in range(0,len(ngbr)):
                    Arc.put((var[i],ngbr[j]))
        else:
            Arc = arcs  

        while Arc.empty() != True :
            tmp_tuple = Arc.get() 
            init_value = Domains.get(tmp_tuple[0])
            xx = self.revise(tmp_tuple[0],tmp_tuple[1],Domains)
            if xx == True and Domains.get(tmp_tuple[0]) == None:
                Domains.update({tmp_tuple[0]: init_value})
                return False
            if xx == True:
                N = list(self.crossword.neighbors(tmp_tuple[0]))
                for k in range(0,len(N)):
                    Arc.put((tmp_tuple[0],N[k]))

        self.domains.update(Domains)
        return True 
        raise NotImplementedError

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        list_var = list(assignment.keys())
        for i in range(0,len(list_var)):
            if assignment.get(list_var[i]) == None:
                return False 
        return True 
        raise NotImplementedError

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        list_var = list(assignment.keys())
        for i in range(0,len(list_var)):
            xx = assignment.get(list_var[i])
            sx = set(xx)
            lx = list(xx)
            for k in range(0,len(lx)):
                if len(lx[k]) != list_var[i].length:
                    return False 

            for j in range(i+1,len(list_var)):
                yy = assignment.get(list_var[j])
                sy = set(yy)
                if sx.intersection(sy) != set(): # If they have common words 
                    return False 

                ly = list(yy)
                for k in range(0,len(ly)):
                    if len(ly[k]) != list_var[j].length: # if length does not match 
                        return False 

                collision = self.crossword.overlaps[list_var[i], list_var[j]]
                if collision != None:
                    collision = list({collision})
                    x_index = []
                    y_index = []
                    for ii in range(0,len(collision)):
                        x_index.append(collision[ii][0])
                        y_index.append(collision[ii][1])
                    for i1 in range(0,len(lx)): 
                        l1 = []
                        word1 = lx[i1]
                        for k1 in range(0,len(x_index)):
                            l1.append(word1[x_index[k1]])
                        for j1 in range(0,len(ly)):
                            l2 = []
                            word2 = ly[j1]
                            for k2 in range(0,len(y_index)):
                                l2.append(word2[y_index[k2]])
                            if (l1 != l2): # if the overlaps do not match 
                                return False  
        return True 
        raise NotImplementedError

    '''
    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        w = self.crossword.neighbors(var)
        # Right now, returning in random order, that still solves the problem, 
        # Once, the whole algorithms starts working properly, I shall come back 
        # and modify it to optimise the algorithm more 
        w = list({w})
        return w  
        raise NotImplementedError
    '''

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        assigned_vars = set(assignment.keys())
        total_vars = set(self.domains.keys())
        unassigned_vars = total_vars - assigned_vars
        # Right now, returning in random order, that still solves the problem, 
        # Once, the whole algorithms starts working properly, I shall come back 
        # and modify it to optimise the algorithm more
        if len(unassigned_vars) != 0:
            un_listed = list(unassigned_vars)
            min_val_var = un_listed[0]
            min_num_val = len({self.domains.get(un_listed[0])})
            for i in range(1,len(un_listed)):
                num_val = len({self.domains.get(un_listed[i])})
                if num_val < min_num_val:
                    min_num_val = num_val
                    min_val_var = un_listed[i]
            return min_val_var
        else:
            return None 
        raise NotImplementedError

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        ## if ac3 on whole domain itself can give the solution, then good.. No need for BackTracking
        if assignment == dict():
            x = self.ac3()
            if x == True :
                assignment = self.domains 
                ans = self.consistent(assignment)
                if ans == True: 
                    return assignment

        ## if ac3 can not solve the whole domain, now, Backtracking is essential
        arcs = queue.Queue()
        L = list(assignment.keys())
        for i in range(0,len(L)):
            arcs.put(L[i])
        
        got = self.select_unassigned_variable(assignment)
        while got != None:
            gVal = self.domains.get(got)
            gDic = {got: gVal}
            arcs2 = arcs.copy()
            arcs2 = acrs2.put(got)
            y = ac3(arcs2)
            if y == True:
                assignent2 = assignment.update(gDic)
                if danger == True:
                    self.bad_vars = self.bad_vars - {got}
                self.backtrack(assignent2)
            else:
                return None
        return assignment
        raise NotImplementedError


def main():

    # Check usage
    if len(sys.argv) != 3:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    #output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        #if output:
        #    creator.save(assignment, output)


if __name__ == "__main__":
    main()
