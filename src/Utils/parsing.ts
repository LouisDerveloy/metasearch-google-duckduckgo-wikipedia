// ex query = "!youtube how to get better at coding"
// ex query = "!youtube"
export function parse_query(query: string): { identifier: string, arg?: string } {
    let _query = query.trim()
    _query = _query.slice(1, _query.length) // remove "!" from the query
    const arg_start = _query.search(" ");

    if (arg_start == -1) {
        return { identifier: _query };
    } else {
        let identifier = _query.slice(undefined, arg_start)
        let arg = _query.slice(arg_start + 1, undefined)

        arg = encodeURIComponent(arg)

        return {identifier: identifier, arg: arg}
    }
}