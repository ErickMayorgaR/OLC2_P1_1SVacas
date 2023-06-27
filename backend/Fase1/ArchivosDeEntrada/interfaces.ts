interface Actor {
    nombre: string;
    edad: number;
}

interface Pelicula {
    nombre: string;
    posicion: number;
}

interface Contrato {
    actor: Actor;
    pelicula: Pelicula;
}

actores = ["Elizabeth Olsen", "Adam Sandler", "Christian Bale", "Jennifer Aniston"];
peliculas = ["Avengers: Age of Ultron", "Mr. Deeds", "Batman: The Dark Knight", "Marley & Me"];

function contratar(actor: Actor, pelicula: Pelicula){
    return {
        actor,
        pelicula
    };
};

function crearActor(nombre: string, edad: number){
    return {
        nombre,
        edad
};
};

function crearPelicula(nombre: string, posicion: number){
    return {
        nombre,
        posicion
    };
};
function imprimir(contrato: Contrato){
    console.log("Actor:", contrato.actor.nombre, "   Edad:", contrato.actor.edad);
    console.log("Pelicula:", contrato.pelicula.nombre, "   Genero:", contrato.pelicula.posicion);
};
function contratos(){
    for (let i = 2; i < 4; i++) {
        let contrato: Contrato = {
        actor: { nombre: "", edad: 0 },
        pelicula: { nombre: "", posicion: 0 }
        };
        if (i < 5) {
        actor = crearActor(actores[i - 1], i + 38);
        pelicula = crearPelicula(peliculas[i - 1], i-1);
        contrato = contratar(actor, pelicula);
        };
        imprimir(contrato);
    };
};

contratos();