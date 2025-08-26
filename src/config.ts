export interface Rule {
    identifier: string;
    name: string;
    aliases?: string[];
    url: string; // ex: https://wwww.google.com/search?q={} here when the user type !google rick roll the {} will be replaced by rick roll
    urlWithNoArg?: string;
}

export const rules: Array<Rule> = [
    {
        identifier: "youtube",
        name: "Youtube Search",
        aliases: [
            "yt"
        ],
        url: "https://www.youtube.com/results?search_query={}",
        urlWithNoArg: "https://www.youtube.com"

    },
    {
        identifier: "github",
        aliases: [
            "git",
            "gt"
        ],
        name: "Github",
        url: "https://github.com/search?q={}",
        urlWithNoArg: "https://github.com/trending"
    },
    {
        identifier: "repo",
        aliases: [
            "rep",
            "re"
        ],
        name: "Github repository",
        url: "https://www.github.com/search?q={}&type=repositories",
        urlWithNoArg: "https://www.github.com/LouisDerveloy?tab=repositories"
    },
    {
        identifier: "esilv",
        aliases: [
            "school",
            "ecole",
            "portail"
        ],
        name: "Esilv portail numérique",
        url: "https://www.leonard-de-vinci.net/student/print/dashboard"
    },
    {
        identifier: "promotion",
        aliases: [
            "promo"
        ],
        name: "Esilv promotion",
        url: "https://www.leonard-de-vinci.net/promotion",
    },
    {
        identifier: "wikipediafr",
        aliases: [
            "wikifr",
        ],
        name: "Wikipedia",
        url: "https://fr.wikipedia.org/wiki/Sp%C3%A9cial:Recherche?search=test",
        urlWithNoArg: "https://fr.wikipedia.org/"
    },
    //TODO: wikipedia english version
    //TODO: Stackoverflow
    //TODO: Reddit
    {
        identifier: "crunchyroll",
        aliases: [
            "crunch",
            "anime",
            "animes"
        ],
        name: "Crunchyroll",
        url: "https://www.crunchyroll.com/fr/search?q={}",
        urlWithNoArg: "https://www.crunchyroll.com/fr/videos/new"
    },
    {
        identifier: "mammouth",
        aliases: [
            "ai",
            "chat",
            "aichat",
            "chatai",
            "gpt",
            "chatgpt"
        ],
        name: "Mammouth ai",
        url: "https://mammouth.ai/app/", // TODO: To complete
        urlWithNoArg: "https://mammouth.ai/app/"
    },
    {
        identifier: "crate",
        aliases: [
            "rust",
            "rustcrate",
            "craterust"
        ],
        name: "Rust crate",
        url: "https://crates.io/search?q={}",
        urlWithNoArg: "https://crates.io/"
    },
    {
        identifier: "amazon",
        aliases: [
            "store",
            "onlinestore",
            "shoping",
            "onlineshoping",
            "ama",
            "buy"
        ],
        name: "Amazon",
        url: "https://www.amazon.fr/s?k={}",
        urlWithNoArg: "https://www.amazon.fr/",
    }
]