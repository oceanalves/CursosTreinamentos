class heroi{
    constructor(nome, idade, tipo){
    this.nome =  nome
    this.idade = idade
    this.tipo = tipo
    }

    atacar(){
        console.log(`O ${this.tipo} atacou usando ${this.ataque()}`)
    }

    ataque(){
        if (this.tipo == "mago"){
            this.tipo = "magia"
        } else if (this.tipo == "guerreiro"){
            this.tipo = "espada"
        } else if (this.tipo == "monge"){
            this.tipo = "artes marciais"
        } else {
            this.tipo = "shuriken"
        }
        return this.tipo
    }
}

let classeMago = new heroi("Luke","23","mago")
let classeGuerreiro = new heroi("Mando","35","guerreiro")
let classeMonge = new heroi("Lea","25","monge")
let classeNinja = new heroi("Bobah","41","ninja")

classeMago.atacar()
classeGuerreiro.atacar()
classeMonge.atacar()
classeNinja.atacar()