def rkm_multiple_pattern(T, Ps, d, q):
    """
    Finds all occurrences of every pattern in Ps within string T.
    @param T (string) - The string to search in.
    @param Ps (list[string]) - A list of string patterns we want to find occurrences of.
    @param d (int) - The radix or number of characters in the alphabet we are using.
    @param q (int) - The prime number to use when computing the hash.
    @returns a dictionary matching each pattern to its list of occurrences (start_index, end_index) in order.
    """
    # No patterns means nothing to check.
    if len(Ps) <= 0:
        return {}
    
    # Set up the results dictionary.
    results = {x: [] for x in Ps}
    n = len(T)

    # Prune out any patterns that cannot have matches due to length.
    Ps = [P for P in Ps if len(P) <= n]

    m_each = [len(P) for P in Ps]
    h = [d**(m-1) % q for m in m_each]
    m_max = max(m_each)

    # Must assert this otherwise the preprocessing will fail.
    n_patterns = len(Ps)
    
    # Setup hashes for all patterns.
    p = [0 for _ in range(n_patterns)]
    t_0 = [0 for _ in range(n_patterns)]

    # Preprocessing
    for i in range(0, m_max):
        for pattern in range(n_patterns):
            if i < m_each[pattern]:
                p[pattern] = (d * p[pattern] + Ps[pattern][i]) % q
                t_0[pattern] = (d * t_0[pattern] + T[i]) % q

    # Matching
    # The ordering of this nesting has little to no effect on the running time
    # however this ordering has the least design complexity.
    # nested the other way around, we would have to go from n-m_max_current and when that goes out of range,
    # remove the pattern with length m_max_current from Ps and recompute the current max length pattern.
    for pattern in range(n_patterns):
        for s in range(-1, n-m_each[pattern]):
            if p[pattern] == t_0[pattern]:
                if Ps[pattern] == T[s+1:s+m_each[pattern]]:
                    results[Ps[pattern]] = (s+1, s+m_each[pattern])
            if s < n - m_each[pattern]:
                t_0[pattern] = (d * (t_0[pattern] - T[s+1] * h) + T[s + m_each[pattern] + 1]) % q
    return results


def find_all_occurrences_with_line_numbers(file, pattern):
    """
    Prints out all occurrences of the pattern in the file along with the line number it was found in.
    @param file (string) - The file name to run the string match on.
    @param pattern (string) - The pattern to match.
    @returns nothing - result will be printed to stdout.
    """
    with open(file, 'r') as fh:
        line_number = 1
        for line in fh:
            matches = kmp_match(line, pattern)
            for match in matches:
                print(f"{line_number}: {match}")


def kruskal_mst(graph):
    A = set()
    d = disjoint_set() # assume this exists with operations make_set, find_set, and union
    for vertex in graph.vertices:
        d.make_set(vertex)
    # Sort the edges in non-decreasing order by weight.
    graph.edges.sort(reverse=True, key=lambda e: e.weight)
    for edge in graph.edges:
        if not d.find_set(edge.u) == d.find_set(edge.v):
            A.union(set([(edge.u, edge.v)]))
            d.union(edge.u, edge.v) # causes find_set(u) to equal find_set(v)
    
    return A
