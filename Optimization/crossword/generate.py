import sys

from crossword import *


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

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var, values in self.domains.items():
            # set comprehension would be slightly faster than self.domain[var].remove(x)
            values = {value for value in values if len(value) == var.length}
            self.domains[var] = values

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        overlap = self.crossword.overlaps[x, y]
        if not overlap:
            return revised

        i_pos, j_pos = overlap
        for x_domain in self.domains[x].copy():
            for y_domain in self.domains[y].copy():
                if x_domain[i_pos] == y_domain[j_pos]:
                    break
            else:
                self.domains[x].remove(x_domain)
                revised = True

        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if not arcs:
            arcs = set()
            for var in self.domains:
                neighbors = self.crossword.neighbors(var)
                arcs.update([(var, neighbor) for neighbor in neighbors])

        arcs = list(arcs)
        while arcs:
            x, y = arcs.pop(0)
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for domain in self.crossword.neighbors(x) - {y}:
                    arcs.append((domain, x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        return len(assignment) == len(self.domains)

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # 1. all domain values must be distinct
        assignment_values = assignment.values()
        if not len(assignment_values) == len(set(assignment_values)):
            return False

        # 2. all domain values are of the correct length
        for var, value in assignment.items():
            if not var.length == len(value):
                return False

        # 3. No conflicts between neighboring values
        for var, value in assignment.items():
            for neighbor in self.crossword.neighbors(var):
                overlap = self.crossword.overlaps[var, neighbor]
                if overlap:
                    i_pos, j_pos = overlap

                if overlap and assignment.get(neighbor)\
                and not value[i_pos] == assignment[neighbor][j_pos]:
                    return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # naive implementation
        # ruled_out = set(assignment.values())
        # return [value for value in self.domains[var] if value not in ruled_out]

        domain_values = {}
        neighbors = self.crossword.neighbors(var)
        overlaps = {neighbor: self.crossword.overlaps[var, neighbor]
            for neighbor in neighbors}.items()
        assigned = set(assignment.values())

        for value in self.domains[var]:
            if value in assigned:
                continue
            order = 0
            for neighbor, crossing in overlaps:
                if not crossing:
                    continue
                i_pos, j_pos = crossing
                for domain in self.domains[neighbor]:
                    if value[i_pos] != domain[j_pos]:
                        order += 1
            domain_values[value] = order

        return [k for k,v in sorted(domain_values.items(), key = lambda x: x[1])]

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # naive approach
        # for var in self.domains:
        #     if var not in assignment:
        #         return var
        mrv = []
        count_mrv = float('inf')

        # selecting all variables with Minimum Remaining Values
        for var, value in self.domains.items():
            if var in assignment:
                continue
            if len(value) == count_mrv:
                mrv.append(var)
            elif len(value) < count_mrv:
                mrv = []
                mrv.append(var)
                count_mrv = len(value)

        if len(mrv) == 1:
            return mrv[0]

        # selecting the variable with the highest degree
        highest_degree = 0
        best_var = None
        for var in mrv:
            neighbors = self.crossword.neighbors(var)
            if len(neighbors) > highest_degree:
                highest_degree = len(neighbors)
                best_var = var

        return best_var

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            assignment[var] = value
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result:
                    return result

            assignment.pop(var)

        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
