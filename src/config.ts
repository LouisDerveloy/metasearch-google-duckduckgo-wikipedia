export interface Rule {
    identifier: string;
    name: string;
    aliases?: string[];
    url: string; // ex: https://wwww.google.com/search?q={} here when the user type !google rick roll the {} will be replaced by rick roll
    urlWithNoArg?: string;
}

export const rules: Array<Rule> = [
    {
        identifier: "google",
        aliases: [
            "goo"
        ],
        name: "Google Search",
        url: "https://www.google.com/search?q={}",
        urlWithNoArg: "https://www.google.com/"
    },
    {
        identifier: "duckduckgo",
        aliases: [
            "duck",
            "duckgo"
        ],
        name: "Duckduckgo Search",
        url: "https://duckduckgo.com/?t=ffab&q={}",
        urlWithNoArg: "https://duckduckgo.com/?t=ffab"
    },
    {
        identifier: "githubstars",
        aliases: [
            "stars",
            "starsrepo",
            "repostars"
        ],
        name: "Github repositories with stars",
        url: "https://github.com/LouisDerveloy?submit=Search&q={}&tab=stars&type&sort&direction&submit=Search",
        urlWithNoArg: "https://github.com/LouisDerveloy?tab=stars"
    },
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
        url: "https://github.com/search?q={}&type=repositories",
        urlWithNoArg: "https://github.com/trending"
    },
    {
        identifier: "repository",
        aliases: [
            "repo",
            "rep",
            "re"
        ],
        name: "Github repository",
        url: "https://github.com/LouisDerveloy?tab=repositories&q={}&type&language&sort",
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
            "wifr"
        ],
        name: "Wikipedia Français",
        url: "https://fr.wikipedia.org/wiki/Sp%C3%A9cial:Recherche?search=test",
        urlWithNoArg: "https://fr.wikipedia.org/"
    },
    {
        identifier: "wikipedia",
        aliases: [
            "wiki",
            "wikien",
            "wien"
        ],
        name: "Wikipedia",
        url: "https://en.wikipedia.org/w/index.php?search={}&title=Special%3ASearch&ns0=1",
        urlWithNoArg: "https://en.wikipedia.org/"
    },
    {
        identifier: "stackoverflow",
        aliases: [
            "stack",
            "overflow",
            "bug"
        ],
        name: "Stackoverflow",
        url: "https://stackoverflow.com/search?q={}",
        urlWithNoArg: "https://stackoverflow.com/questions"
    },
    {
        identifier: "reddit",
        aliases: [
            "redit",
            "red",
            "forum"
        ],
        name: "Reddit",
        url: "https://www.reddit.com/search/?q={}",
        urlWithNoArg: "https://www.reddit.com/r/popular/"
    },
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
        url: "https://mammouth.ai/app/a/default",
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