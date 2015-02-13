Gremlin.defineStep('taintForward', [Vertex, Pipe], {
    identifier, k ->
    _()
    .copySplit(
        _(),
        _().outE("REACHES").filter{it.var == identifier}.inV(),
        _().outE("REACHES").filter{it.var == identifier}.inV().out("REACHES").simplePath().loop(2){it.loops < k-1}{true},
    ).fairMerge().dedup()
});

Gremlin.defineStep('taintBackward', [Vertex, Pipe], {
    identifier, k ->
    _()
    .copySplit(
        _(),
        _().inE("REACHES").filter{it.var == identifier}.outV(),
        _().inE("REACHES").filter{it.var == identifier}.outV().in("REACHES").simplePath().loop(2){it.loops < k-1}{true},
    ).fairMerge().dedup()
});

Gremlin.defineStep('sliceForward', [Vertex, Pipe], {
    identifier, k ->
    _()
    .copySplit(
        _(),
        _().outE("REACHES", "CONTROLS").filter{it.var == identifier | it.label == "CONTROLS"}.inV(),
        _().outE("REACHES", "CONTROLS").filter{it.var == identifier | it.label == "CONTROLS"}.inV().out("REACHES", "CONTROLS").simplePath().loop(2){it.loops < k-1}{true},
    ).fairMerge().dedup()
});

Gremlin.defineStep('sliceBackward', [Vertex, Pipe], {
    identifier, k ->
    _()
    .copySplit(
        _(),
        _().inE("REACHES", "CONTROLS").filter{it.var == identifier | it.label == "CONTROLS"}.outV(),
        _().inE("REACHES", "CONTROLS").filter{it.var == identifier | it.label == "CONTROLS"}.outV().in("REACHES", "CONTROLS").simplePath().loop(2){it.loops < k-1}{true},
    ).fairMerge().dedup()
});
