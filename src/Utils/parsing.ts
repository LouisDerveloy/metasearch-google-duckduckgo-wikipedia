// ex query = "!youtube how to get better at coding"
// ex query = "!youtube"
import type {SearchResult} from "../types/search.ts";

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

export function parse_google(html: any): Array<SearchResult> {
    console.log(typeof html);
    console.dir(html);
    //...
}

export function parse_duck(html: any): Array<SearchResult> {
    console.log(typeof html);
    console.dir(html);
    //...
}