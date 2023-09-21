
export const normalizeSemester = (string) => {
    return string.split(" ")[1];
}

export const normalizeYear = (string) => {
    string = string.toLowerCase().trim();
    if (string === 'all') return 0;
    return string.split(" ")[1];
}