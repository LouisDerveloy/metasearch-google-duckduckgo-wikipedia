export interface SearchResult {
    title: string
    url: string
    description: string
    ads?: boolean
    searchEngine: string
}

export interface EngineResponse {
    engine: string
    results: SearchResult[]
    success: boolean
    error_message?: string
    search_time?: number
}

export interface SearchResponse {
    query: string
    engines_responses: EngineResponse[]
    total_results: number
    search_time: number
}

export interface SearchRequest {
    query: string
    max_results: number
    engines: string[]
}

export interface EngineStatus {
    name: string
    enabled: boolean
    configured: boolean
    status: 'ready' | 'disabled'
}
