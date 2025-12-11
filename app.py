from flask import Flask, render_template, request

app = Flask(__name__)

# ---------------------------------------------
# 1. Parse Grammar into tokens
# ---------------------------------------------
def parse_grammar(grammar_str):
    grammar = {}
    for line in grammar_str.strip().split("\n"):
        if "->" not in line:
            continue
        
        lhs, rhs = line.split("->")
        lhs = lhs.strip()
        
        rhs_alts = []
        for alt in rhs.split("|"):
            alt = alt.strip()
            symbols = []
            i = 0
            while i < len(alt):
                if alt[i].isupper():  
                    # variable (A, B, S, etc.)
                    symbols.append(alt[i])
                else:
                    # terminal (a, b, c ...)
                    symbols.append(alt[i])
                i += 1
            rhs_alts.append(symbols)

        grammar[lhs] = rhs_alts
    return grammar


# ---------------------------------------------
# 2. Remove ε-productions
# ---------------------------------------------
def eliminate_epsilon(grammar, keep_start_epsilon=False):
    nullable = set()

    # Find initial nullable variables
    for lhs, alts in grammar.items():
        for rhs in alts:
            if rhs == ['ε']:
                nullable.add(lhs)

    changed = True
    while changed:
        changed = False
        for lhs, alts in grammar.items():
            for rhs in alts:
                if rhs and all((symbol.isupper() and symbol in nullable) for symbol in rhs):
                    if lhs not in nullable:
                        nullable.add(lhs)
                        changed = True

    # Construct new grammar without ε
    new_grammar = {}
    for lhs, alts in grammar.items():
        new_alts = []
        for rhs in alts:
            if rhs == ['ε']:
                continue

            # generate combinations removing nullable symbols
            def generate_combinations(seq):
                results = [[]]
                for sym in seq:
                    new_results = []
                    for r in results:
                        new_results.append(r + [sym])
                        if sym.isupper() and sym in nullable:
                            new_results.append(r)
                    results = new_results
                return [r for r in results if r]  # Remove empty combinations

            combos = generate_combinations(rhs)
            for c in combos:
                if c not in new_alts:
                    new_alts.append(c)

        new_grammar[lhs] = new_alts

    # Only keep S → ε if explicitly requested AND S doesn't appear on RHS
    if keep_start_epsilon and "S" in nullable:
        # Check if S appears on RHS of any production
        s_on_rhs = any(
            'S' in rhs 
            for alts in new_grammar.values() 
            for rhs in alts
        )
        if not s_on_rhs:
            new_grammar["S"].append(["ε"])

    return new_grammar


# ---------------------------------------------
# 3. Eliminate unit productions (A -> B)
# ---------------------------------------------
def eliminate_unit_productions(grammar):
    unit_pairs = set()

    # find all unit productions
    for A in grammar:
        for rhs in grammar[A]:
            if len(rhs) == 1 and rhs[0].isupper():
                unit_pairs.add((A, rhs[0]))

    # closure of unit productions
    changed = True
    while changed:
        changed = False
        for A, B in list(unit_pairs):
            for rhs in grammar.get(B, []):
                if len(rhs) == 1 and rhs[0].isupper():
                    if (A, rhs[0]) not in unit_pairs:
                        unit_pairs.add((A, rhs[0]))
                        changed = True

    # build new grammar
    new_grammar = {A: [] for A in grammar}
    for A in grammar:
        for rhs in grammar[A]:
            if not (len(rhs) == 1 and rhs[0].isupper()):
                new_grammar[A].append(rhs)

    # A → B absorbs all B productions
    for A, B in unit_pairs:
        for rhs in grammar[B]:
            if not (len(rhs) == 1 and rhs[0].isupper()):
                if rhs not in new_grammar[A]:
                    new_grammar[A].append(rhs)

    return new_grammar


# ---------------------------------------------
# 4. Remove long rules (A → B C D ...)
# ---------------------------------------------
def eliminate_long_rules(grammar):
    new_rules = {}
    counter = 1

    for A in grammar:
        new_alts = []
        for rhs in grammar[A]:
            if len(rhs) <= 2:
                new_alts.append(rhs)
            else:
                prev = rhs[0]
                for i in range(1, len(rhs) - 1):
                    new_var = f"N{counter}"
                    counter += 1
                    new_rules[new_var] = [[prev, rhs[i]]]
                    prev = new_var
                new_alts.append([prev, rhs[-1]])

        grammar[A] = new_alts

    grammar.update(new_rules)
    return grammar


# ---------------------------------------------
# 5. Replace terminals in pairs (A → aB becomes A → T1 B)
# ---------------------------------------------
def terminals_in_pairs(grammar):
    new_rules = {}
    terminal_map = {}
    counter = 1

    for A in grammar:
        new_alts = []
        for rhs in grammar[A]:
            if len(rhs) == 2:
                new_rhs = []
                for sym in rhs:
                    if sym.islower():
                        if sym in terminal_map:
                            new_var = terminal_map[sym]
                        else:
                            new_var = f"T{counter}"
                            counter += 1
                            terminal_map[sym] = new_var
                            new_rules[new_var] = [[sym]]
                        new_rhs.append(new_var)
                    else:
                        new_rhs.append(sym)
                new_alts.append(new_rhs)
            else:
                new_alts.append(rhs)

        grammar[A] = new_alts

    grammar.update(new_rules)
    return grammar


# ---------------------------------------------
# 6. Convert entire grammar to CNF
# ---------------------------------------------
def format_grammar(grammar):
    lines = []
    for lhs, alts in grammar.items():
        formatted = [" ".join(rhs) for rhs in alts]
        lines.append(f"{lhs} → {' | '.join(formatted)}")
    return "\n".join(lines)


def convert_to_cnf(grammar_str):
    steps = []

    grammar = parse_grammar(grammar_str)
    steps.append("Parsed Grammar:\n" + format_grammar(grammar))

    grammar = eliminate_epsilon(grammar)
    steps.append("After ε-Elimination:\n" + format_grammar(grammar))

    grammar = eliminate_unit_productions(grammar)
    steps.append("After Unit Production Elimination:\n" + format_grammar(grammar))

    grammar = eliminate_long_rules(grammar)
    steps.append("After Long Rule Elimination:\n" + format_grammar(grammar))

    grammar = terminals_in_pairs(grammar)
    steps.append("After Terminal Pair Replacement:\n" + format_grammar(grammar))

    return grammar, steps




# ---------------------------------------------
# Flask Routing
# ---------------------------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    cnf = None
    applied_steps = None
    cnf_output = ""
    if request.method == "POST":
        grammar_input = request.form["grammar"]
        cnf, applied_steps = convert_to_cnf(grammar_input)

        lines = []
        for lhs, alts in cnf.items():
            formatted = ["".join(rhs) for rhs in alts]
            lines.append(f"{lhs} → {' | '.join(formatted)}")

        cnf_output = "\n".join(lines)

    return render_template("index.html", cnf_output=cnf_output, steps=applied_steps)



if __name__ == "__main__":
    app.run(debug=True)
