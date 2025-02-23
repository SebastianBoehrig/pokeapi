export type TypesType = {
    name: string;
    img: string;
};

export type Pokemon = {
    name: string;
    weight: string;
    height: string;
    types: string[];
    img: {
        default: string;
        shiny: string;
    };
};