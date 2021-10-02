/**
 * Caso #3
 * Mónica Alfaro Parrales - 2020132572 
 * Max Richard Lee Chung - 2019185076
*/

const mongoose = require('mongoose');

main().catch(err => console.log(err));

async function main() {
  //Conexion con la base de Mongo
  await mongoose.connect('mongodb://localhost:27017/caso3');
}


//Esquema
const saleSchema = new mongoose.Schema({
    nombreDuennio: String,
    emailDuennio: String,
    nombreArticulo: String,
    detalle: String,
    urlFoto: String,
    precioInicial: Number,
    annoAntiguedad: Number,
    fechaMaxima: Date,
    activo: Boolean,
    preciosSubasta: [
        {
            nombreArticulo: String, 
            nombreSubastador: String,
            precio: Number
        }
    ]
});

//Modelo de la subasta
module.exports = mongoose.model('Sales', saleSchema);
Sales = mongoose.model('Sales', saleSchema);