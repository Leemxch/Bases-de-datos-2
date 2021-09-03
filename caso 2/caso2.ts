/**
 * CASO #2
 * Max Richard Lee Chung - 2019185076
 */

const mongoose = require('mongoose');

main().catch(err => console.log(err));

async function main() {
  //Conexion con la base de Mongo
  await mongoose.connect('mongodb://localhost:27017/caso2');
  //Verificar el estado de conexion
  console.log(mongoose.connection.readyState);
  /**
   * 0: disconnected
   * 1: connected
   * 2: connecting
   * 3: disconnecting
   */
   
}

//Schema de PedidosYa 
const PedidosYaSchema = new mongoose.Schema({
  id:Number,
  nombre: String,
  ubicacion: String,
  costo: [Number],
  rating: Number
});

//Modelo a partir del esquema PedidosYaSchema
const PedidosYa = mongoose.model('PedidosYa',PedidosYaSchema);

//Schema de Newt
const NewtSchema = new mongoose.Schema({
  id: Number,
  ubicacion: String,
  estado: String,
  distanciaRecorrida: [Number],
  costo:Number,
  rating: Number,
  bateria: Number
})

//Modelo a partir del esquema NewtSchema
const Newt = mongoose.model('Newt', NewtSchema)

/*
//Insertar 1 fila
const hamburguesa = new PedidosYa ({id: 1, nombre: 'hamburguesa', ubicacion: 'San Jose', costo: [5000,3000], rating: 4.1});
hamburguesa.save();

//Insertar mas de 1 fila
PedidosYa.insertMany([
  {id: 2, nombre: 'hamburguesa2', ubicacion: 'San Jose', costo: [5000,3000], rating: 4.1},
  {id: 3, nombre: 'hamburguesa3', ubicacion: 'San Jose', costo: [5000,3000], rating: 4.1},
  {id: 4, nombre: 'hamburguesa4', ubicacion: 'San Jose', costo: [5000,3000], rating: 4.1}
])*/