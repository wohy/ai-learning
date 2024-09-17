export const formatString = (str: string) => {
    const regex = /{\n\s*"content": "(.*?)",\n\s*"image": "(.*?)"\s*}/g;
    const events = [];
    let match;

    while ((match = regex.exec(str)) !== null) {
        events.push({
            content: match[1].trim(),
            image: match[2].trim(),
        });
    }

    return events;
}