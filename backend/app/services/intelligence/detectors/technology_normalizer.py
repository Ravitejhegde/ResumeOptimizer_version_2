import re


class TechnologyNormalizer:

    ALIASES = {

        # -----------------------------------
        # HTML
        # -----------------------------------

        "html 5": "html5",

        "html-5": "html5",

        "html5": "html5",

        # -----------------------------------
        # CSS
        # -----------------------------------

        "css 3": "css3",

        "css-3": "css3",

        "css3": "css3",

        # -----------------------------------
        # JavaScript
        # -----------------------------------

        "java script": "javascript",

        "javascript": "javascript",

        "js": "javascript",

        # -----------------------------------
        # TypeScript
        # -----------------------------------

        "type script": "typescript",

        "typescript": "typescript",

        "ts": "typescript",

        # -----------------------------------
        # React
        # -----------------------------------

        "reactjs": "react",

        "react js": "react",

        "react.js": "react",

        "react": "react",

        # -----------------------------------
        # Angular
        # -----------------------------------

        "angularjs": "angular",

        "angular js": "angular",

        "angular": "angular",

        # -----------------------------------
        # Vue
        # -----------------------------------

        "vuejs": "vue",

        "vue js": "vue",

        "vue.js": "vue",

        "vue": "vue",

        # -----------------------------------
        # Node
        # -----------------------------------

        "nodejs": "node.js",

        "node js": "node.js",

        "node-js": "node.js",

        "node.js": "node.js",

        # -----------------------------------
        # REST
        # -----------------------------------

        "restful api": "rest api",

        "restful apis": "rest api",

        "rest api": "rest api",

        "rest apis": "rest api",

        # -----------------------------------
        # CI/CD
        # -----------------------------------

        "ci cd": "ci/cd",

        "ci-cd": "ci/cd",

        "continuous integration": "ci/cd",

        "continuous deployment": "ci/cd",

        # -----------------------------------
        # GitHub
        # -----------------------------------

        "github": "github",

        "git hub": "github",

        # -----------------------------------
        # C#
        # -----------------------------------

        "c sharp": "c#",

        "c#": "c#",

        # -----------------------------------
        # ASP.NET
        # -----------------------------------

        "asp net": "asp.net",

        "asp.net": "asp.net",

        # -----------------------------------
        # SQL Server
        # -----------------------------------

        "ms sql": "sql server",

        "mssql": "sql server",

        "sql server": "sql server",

    }

    @staticmethod
    def normalize(

        text: str,

    ) -> str:

        normalized = text.lower()

        for alias, canonical in sorted(

            TechnologyNormalizer.ALIASES.items(),

            key=lambda x: len(x[0]),

            reverse=True,

        ):

            normalized = re.sub(

                rf"\b{re.escape(alias)}\b",

                canonical,

                normalized,

                flags=re.IGNORECASE,

            )

        return normalized