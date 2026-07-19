export function getStyleClass(style: string): string {

    const value = style.toLowerCase();

    if (value.includes("title")) {
        return "titleBlock";
    }

    if (value.includes("heading 1")) {
        return "headingBlock";
    }

    if (value.includes("heading")) {
        return "headingBlock";
    }

    if (value.includes("list")) {
        return "bulletBlock";
    }

    return "";

}